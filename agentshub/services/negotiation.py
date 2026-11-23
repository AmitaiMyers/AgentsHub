"""Bounded, typed negotiation sessions (docs/SYSTEM_DESIGN.md §7.3)."""
from collections.abc import Callable
from dataclasses import dataclass

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from agentshub.config import MAX_SESSION_MESSAGES, MAX_SESSION_PROPOSALS
from agentshub.db import utcnow
from agentshub.errors import Conflict, NotFound, ValidationFailed
from agentshub.intent_types import Stage, get_spec, job_pair, parse_payload, salary_zone, validate_terms, visible_fields
from agentshub.models import (
    Agent,
    ApprovalDecision,
    HandoffApproval,
    Intent,
    NegotiationSession,
    Principal,
    SessionMessage,
    SessionState,
)
from agentshub.schemas import (
    ApprovalStatus,
    ContactOut,
    CounterpartView,
    MessageOut,
    SendMessageInput,
    SessionIdInput,
    SessionList,
    SessionSummary,
    SessionView,
    ZoneOfAgreement,
)
from agentshub.security import new_id
from agentshub.services import audit, quotas
from agentshub.services.matching import counterpart_badge
from agentshub.services.outbox import queue_email


@dataclass(frozen=True)
class Parties:
    session: NegotiationSession
    mine: Intent
    theirs: Intent


def _intent(db: Session, intent_id: str) -> Intent:
    intent = db.get(Intent, intent_id)
    assert intent is not None, f"session references missing intent {intent_id}"
    return intent


def parties_for(db: Session, principal_id: str, session_id: str) -> Parties:
    session = db.get(NegotiationSession, session_id)
    if session is None:
        raise NotFound(f"Session {session_id} not found")
    intent_a, intent_b = _intent(db, session.intent_a_id), _intent(db, session.intent_b_id)
    if intent_a.principal_id == principal_id:
        return Parties(session, intent_a, intent_b)
    if intent_b.principal_id == principal_id:
        return Parties(session, intent_b, intent_a)
    raise NotFound(f"Session {session_id} not found")


def _zone(parties: Parties) -> ZoneOfAgreement | None:
    spec = get_spec(parties.mine.intent_type)
    if spec.family != "job":
        return None
    other_spec = get_spec(parties.theirs.intent_type)
    offer, seek = job_pair(spec, parse_payload(spec, parties.mine.payload),
                           parse_payload(other_spec, parties.theirs.payload))
    zone = salary_zone(offer, seek)
    return ZoneOfAgreement(low=zone.low, high=zone.high, currency=zone.currency)


def _approvals(db: Session, parties: Parties) -> ApprovalStatus | None:
    rows = list(db.scalars(select(HandoffApproval).where(HandoffApproval.session_id == parties.session.id)))
    if not rows:
        return None
    by_principal = {row.principal_id: row.decision for row in rows}
    return ApprovalStatus(mine=by_principal[parties.mine.principal_id],
                          counterpart=by_principal[parties.theirs.principal_id])


def _contact(db: Session, principal_id: str) -> ContactOut:
    principal = db.get(Principal, principal_id)
    assert principal is not None
    return ContactOut(display_name=principal.display_name, contact_email=principal.contact_email)


def session_view(db: Session, parties: Parties) -> SessionView:
    session = parties.session
    handed_off = session.state == SessionState.HANDED_OFF
    their_spec = get_spec(parties.theirs.intent_type)
    stage = Stage.HANDOFF if handed_off else Stage.MUTUAL
    messages = db.scalars(select(SessionMessage).where(SessionMessage.session_id == session.id)
                          .order_by(SessionMessage.created_at))
    return SessionView(
        id=session.id, state=session.state, my_intent_id=parties.mine.id,
        counterpart=CounterpartView(
            intent_id=parties.theirs.id, intent_type=parties.theirs.intent_type,
            badge=counterpart_badge(db, parties.theirs),
            fields=visible_fields(their_spec, parties.theirs.payload, stage),
            contact=_contact(db, parties.theirs.principal_id) if handed_off else None,
        ),
        zone_of_agreement=_zone(parties),
        latest_proposal=session.latest_proposal,
        latest_proposal_is_mine=(session.latest_proposal_by == parties.mine.id
                                 if session.latest_proposal_by is not None else None),
        agreed_terms=session.agreed_terms,
        messages_left=MAX_SESSION_MESSAGES - session.message_count,
        proposals_left=MAX_SESSION_PROPOSALS - session.proposal_count,
        approvals=_approvals(db, parties),
        messages=[
            MessageOut(id=message.id, sender="me" if message.sender_intent_id == parties.mine.id else "counterpart",
                       kind=message.kind, untrusted_text=message.untrusted_text, terms=message.terms,
                       created_at=message.created_at)
            for message in messages
        ],
    )


def get_session(db: Session, agent: Agent, data: SessionIdInput) -> SessionView:
    return session_view(db, parties_for(db, agent.principal_id, data.session_id))


def list_sessions(db: Session, agent: Agent) -> SessionList:
    my_intent_ids = select(Intent.id).where(Intent.principal_id == agent.principal_id)
    query = (select(NegotiationSession)
             .where(or_(NegotiationSession.intent_a_id.in_(my_intent_ids),
                        NegotiationSession.intent_b_id.in_(my_intent_ids)))
             .order_by(NegotiationSession.updated_at.desc()))
    items = []
    for session in db.scalars(query):
        parties = parties_for(db, agent.principal_id, session.id)
        items.append(SessionSummary(id=session.id, state=session.state, my_intent_id=parties.mine.id,
                                    counterpart_intent_id=parties.theirs.id,
                                    counterpart_intent_type=parties.theirs.intent_type,
                                    updated_at=session.updated_at))
    return SessionList(items=items)

# ---------------------------------------------------------------- message kinds


def _require_state(session: NegotiationSession, allowed: set[SessionState], action: str) -> None:
    if session.state not in allowed:
        raise Conflict(f"Cannot {action} while the session is '{session.state}'")


def _require_text(data: SendMessageInput) -> str:
    if not data.text:
        raise ValidationFailed(f"'{data.kind}' needs non-empty text")
    return data.text


def _forbid_terms(data: SendMessageInput) -> None:
    if data.terms is not None:
        raise ValidationFailed(f"'{data.kind}' does not take terms")


def _handle_text_move(parties: Parties, data: SendMessageInput) -> tuple[str | None, dict | None]:
    _require_state(parties.session, {SessionState.OPEN}, f"send a {data.kind}")
    _forbid_terms(data)
    return _require_text(data), None


def _handle_proposal(parties: Parties, data: SendMessageInput) -> tuple[str | None, dict | None]:
    session = parties.session
    _require_state(session, {SessionState.OPEN}, "propose terms")
    if data.terms is None:
        raise ValidationFailed("'propose_terms' needs terms")
    if session.proposal_count >= MAX_SESSION_PROPOSALS:
        raise Conflict(f"This session already used its {MAX_SESSION_PROPOSALS} proposals")
    spec, their_spec = get_spec(parties.mine.intent_type), get_spec(parties.theirs.intent_type)
    terms = validate_terms(spec, parse_payload(spec, parties.mine.payload),
                           parse_payload(their_spec, parties.theirs.payload), data.terms)
    session.latest_proposal = terms
    session.latest_proposal_by = parties.mine.id
    session.proposal_count += 1
    return data.text, terms


def _handle_accept(parties: Parties, data: SendMessageInput) -> tuple[str | None, dict | None]:
    session = parties.session
    _require_state(session, {SessionState.OPEN}, "accept terms")
    _forbid_terms(data)
    if session.latest_proposal is None or session.latest_proposal_by == parties.mine.id:
        raise Conflict("There is no counterpart proposal to accept")
    session.agreed_terms = session.latest_proposal
    session.state = SessionState.TERMS_AGREED
    return data.text, session.agreed_terms


def _handle_decline(parties: Parties, data: SendMessageInput) -> tuple[str | None, dict | None]:
    _require_state(parties.session, {SessionState.OPEN, SessionState.TERMS_AGREED}, "decline")
    _forbid_terms(data)
    parties.session.state = SessionState.DECLINED
    return data.text, None


MESSAGE_HANDLERS: dict[str, Callable[[Parties, SendMessageInput], tuple[str | None, dict | None]]] = {
    "question": _handle_text_move,
    "answer": _handle_text_move,
    "propose_terms": _handle_proposal,
    "accept_terms": _handle_accept,
    "decline": _handle_decline,
}


def send_message(db: Session, agent: Agent, data: SendMessageInput) -> SessionView:
    parties = parties_for(db, agent.principal_id, data.session_id)
    session = parties.session
    if session.message_count >= MAX_SESSION_MESSAGES:
        raise Conflict(f"This session reached its {MAX_SESSION_MESSAGES}-message limit")
    principal = db.get(Principal, agent.principal_id)
    assert principal is not None
    quotas.ensure_can_send_message(db, principal)
    text, terms = MESSAGE_HANDLERS[data.kind](parties, data)
    db.add(SessionMessage(id=new_id(), session_id=session.id, sender_intent_id=parties.mine.id,
                          sender_principal_id=principal.id, kind=data.kind, untrusted_text=text, terms=terms,
                          created_at=utcnow()))
    session.message_count += 1
    session.updated_at = utcnow()
    db.flush()
    audit.record(db, actor_type="agent", actor_id=agent.id, action=f"session.{data.kind}",
                 subject_type="session", subject_id=session.id, data={"state": session.state})
    return session_view(db, parties)


def request_handoff(db: Session, agent: Agent, data: SessionIdInput, base_url: str) -> SessionView:
    parties = parties_for(db, agent.principal_id, data.session_id)
    session = parties.session
    _require_state(session, {SessionState.OPEN, SessionState.TERMS_AGREED}, "request a hand-off")
    session.state = SessionState.HANDOFF_PENDING
    session.updated_at = utcnow()
    for intent in (parties.mine, parties.theirs):
        db.add(HandoffApproval(id=new_id(), session_id=session.id, principal_id=intent.principal_id,
                               decision=ApprovalDecision.PENDING))
        recipient = db.get(Principal, intent.principal_id)
        assert recipient is not None
        queue_email(db, to_email=recipient.contact_email, subject="Approve an introduction on AgentsHub",
                    body=f"An agent asked to introduce you. Review and approve or decline: {base_url}/sessions/{session.id}")
    db.flush()
    audit.record(db, actor_type="agent", actor_id=agent.id, action="handoff.requested",
                 subject_type="session", subject_id=session.id, data={})
    return session_view(db, parties)
