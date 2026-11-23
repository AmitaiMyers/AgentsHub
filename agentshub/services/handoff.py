"""Human approval of introductions and staged contact disclosure. Principals only, never agents."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from agentshub.db import utcnow
from agentshub.errors import Conflict, NotFound
from agentshub.intent_types import Stage, get_spec, visible_fields
from agentshub.models import ApprovalDecision, HandoffApproval, Principal, SessionState
from agentshub.schemas import ApprovalList, ApprovalView, DecideApprovalInput
from agentshub.services import audit
from agentshub.services.negotiation import Parties, parties_for
from agentshub.services.outbox import queue_email


def _approval_view(parties: Parties, approval: HandoffApproval) -> ApprovalView:
    their_spec = get_spec(parties.theirs.intent_type)
    return ApprovalView(session_id=parties.session.id, session_state=parties.session.state,
                        my_intent_id=parties.mine.id, my_intent_type=parties.mine.intent_type,
                        counterpart_fields=visible_fields(their_spec, parties.theirs.payload, Stage.MUTUAL),
                        agreed_terms=parties.session.agreed_terms, decision=approval.decision)


def list_pending_approvals(db: Session, principal: Principal) -> ApprovalList:
    query = select(HandoffApproval).where(HandoffApproval.principal_id == principal.id,
                                          HandoffApproval.decision == ApprovalDecision.PENDING)
    items = [_approval_view(parties_for(db, principal.id, approval.session_id), approval)
             for approval in db.scalars(query)]
    return ApprovalList(items=items)


def _approval_row(db: Session, session_id: str, principal_id: str) -> HandoffApproval:
    query = select(HandoffApproval).where(HandoffApproval.session_id == session_id,
                                          HandoffApproval.principal_id == principal_id)
    approval = db.scalars(query).first()
    if approval is None:
        raise NotFound("No hand-off approval is waiting for you in this session")
    return approval


def _disclose_contacts(db: Session, parties: Parties) -> None:
    principals = [db.get(Principal, intent.principal_id) for intent in (parties.mine, parties.theirs)]
    assert all(principal is not None for principal in principals)
    for recipient, other in ((principals[0], principals[1]), (principals[1], principals[0])):
        queue_email(db, to_email=recipient.contact_email, subject="Your AgentsHub introduction",
                    body=f"You are now introduced to {other.display_name} <{other.contact_email}>.")
    audit.record(db, actor_type="system", actor_id="hub", action="disclosure.contacts",
                 subject_type="session", subject_id=parties.session.id,
                 data={"recipients": [principal.id for principal in principals]})


def decide(db: Session, principal: Principal, session_id: str, data: DecideApprovalInput) -> ApprovalView:
    parties = parties_for(db, principal.id, session_id)
    session = parties.session
    approval = _approval_row(db, session.id, principal.id)
    if session.state != SessionState.HANDOFF_PENDING or approval.decision != ApprovalDecision.PENDING:
        raise Conflict("This hand-off is not waiting for your decision")
    approval.decision = ApprovalDecision.APPROVED if data.decision == "approve" else ApprovalDecision.DECLINED
    approval.decided_at = utcnow()
    session.updated_at = utcnow()
    audit.record(db, actor_type="principal", actor_id=principal.id, action=f"handoff.{approval.decision}",
                 subject_type="session", subject_id=session.id, data={})
    if approval.decision == ApprovalDecision.DECLINED:
        session.state = SessionState.DECLINED
        return _approval_view(parties, approval)
    decisions = db.scalars(select(HandoffApproval.decision).where(HandoffApproval.session_id == session.id))
    if all(decision == ApprovalDecision.APPROVED for decision in decisions):
        session.state = SessionState.HANDED_OFF
        _disclose_contacts(db, parties)
    return _approval_view(parties, approval)
