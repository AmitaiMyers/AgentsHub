"""Mutual opt-in. A session opens only when both sides expressed interest."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from agentshub.errors import Conflict, Forbidden
from agentshub.intent_types import check_pair, get_spec, parse_payload
from agentshub.models import Agent, Interest, NegotiationSession, Principal, SessionState
from agentshub.schemas import ExpressInterestInput, InterestOut
from agentshub.security import new_id
from agentshub.services import audit, quotas
from agentshub.services.identity import principal_of
from agentshub.services.intents import load_intent, owned_intent, require_live
from agentshub.services.outbox import queue_email


def _find_interest(db: Session, from_intent_id: str, to_intent_id: str) -> Interest | None:
    query = select(Interest).where(Interest.from_intent_id == from_intent_id, Interest.to_intent_id == to_intent_id)
    return db.scalars(query).first()


def express_interest(db: Session, agent: Agent, data: ExpressInterestInput, base_url: str) -> InterestOut:
    principal = principal_of(db, agent)
    own = owned_intent(db, principal.id, data.from_intent_id)
    target = load_intent(db, data.to_intent_id)
    require_live(own)
    require_live(target)
    if target.principal_id == principal.id:
        raise Forbidden("You cannot express interest in your own intent")
    spec, target_spec = get_spec(own.intent_type), get_spec(target.intent_type)
    check = check_pair(spec, parse_payload(spec, own.payload), target_spec, parse_payload(target_spec, target.payload))
    if not check.compatible:
        raise Conflict(f"These intents are not compatible: {check.first_failed_rule}")
    if _find_interest(db, own.id, target.id) is not None:
        raise Conflict("Interest already expressed")
    quotas.ensure_can_express_interest(db, principal)
    db.add(Interest(id=new_id(), from_intent_id=own.id, to_intent_id=target.id, principal_id=principal.id))
    db.flush()
    audit.record(db, actor_type="agent", actor_id=agent.id, action="interest.expressed",
                 subject_type="intent", subject_id=target.id, data={"from_intent_id": own.id})
    if _find_interest(db, target.id, own.id) is None:
        return InterestOut(status="waiting_for_counterpart", session_id=None)
    session = NegotiationSession(id=new_id(), intent_a_id=target.id, intent_b_id=own.id, state=SessionState.OPEN,
                                 message_count=0, proposal_count=0)
    db.add(session)
    db.flush()
    audit.record(db, actor_type="system", actor_id="hub", action="session.opened",
                 subject_type="session", subject_id=session.id,
                 data={"intent_a_id": session.intent_a_id, "intent_b_id": session.intent_b_id})
    for principal_id in (principal.id, target.principal_id):
        recipient = db.get(Principal, principal_id)
        assert recipient is not None
        queue_email(db, to_email=recipient.contact_email, subject="Mutual interest on AgentsHub",
                    body=f"Your agent and another agent are both interested. Follow along: {base_url}/sessions/{session.id}")
    return InterestOut(status="session_opened", session_id=session.id)
