"""Posting and managing intents."""
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from agentshub.config import INTENT_TTL_DAYS
from agentshub.db import utcnow
from agentshub.errors import Conflict, Forbidden, NotFound, ValidationFailed
from agentshub.intent_types import INTENT_TYPES, field_stages, find_prohibited_keys, get_spec, parse_payload
from agentshub.models import Agent, Intent, IntentStatus
from agentshub.schemas import IntentIdInput, IntentList, IntentOut, IntentTypeList, IntentTypeOut, PostIntentInput
from agentshub.security import new_id
from agentshub.services import audit, quotas
from agentshub.services.identity import principal_of


def intent_out(intent: Intent) -> IntentOut:
    return IntentOut(id=intent.id, intent_type=intent.intent_type, status=intent.status, payload=intent.payload,
                     created_at=intent.created_at, expires_at=intent.expires_at)


def intent_type_list() -> IntentTypeList:
    items = [
        IntentTypeOut(
            name=spec.name, description=spec.description, complement=spec.complement,
            allowed_principal_kind=spec.allowed_kind.value if spec.allowed_kind is not None else None,
            min_tier=spec.min_tier,
            field_stages={name: stage.name.lower() for name, stage in field_stages(spec).items()},
            payload_schema=spec.payload_model.model_json_schema(),
        )
        for spec in INTENT_TYPES.values()
    ]
    return IntentTypeList(items=items)


def is_live(intent: Intent) -> bool:
    return intent.status == IntentStatus.OPEN and intent.expires_at > utcnow()


def require_live(intent: Intent) -> None:
    if not is_live(intent):
        raise Conflict(f"Intent {intent.id} is closed or expired")


def load_intent(db: Session, intent_id: str) -> Intent:
    intent = db.get(Intent, intent_id)
    if intent is None:
        raise NotFound(f"Intent {intent_id} not found")
    return intent


def owned_intent(db: Session, principal_id: str, intent_id: str) -> Intent:
    intent = load_intent(db, intent_id)
    if intent.principal_id != principal_id:
        raise NotFound(f"Intent {intent_id} not found")
    return intent


def post_intent(db: Session, agent: Agent, data: PostIntentInput) -> IntentOut:
    spec = get_spec(data.intent_type)
    prohibited = find_prohibited_keys(data.payload)
    if prohibited:
        raise ValidationFailed(f"Protected-trait fields are not allowed: {sorted(set(prohibited))}")
    payload = parse_payload(spec, data.payload)
    principal = principal_of(db, agent)
    if spec.allowed_kind is not None and principal.kind != spec.allowed_kind:
        raise Forbidden(f"Only {spec.allowed_kind} principals can post {spec.name}")
    if principal.tier < spec.min_tier:
        raise Forbidden(f"{spec.name} requires verification tier {spec.min_tier}; this principal is tier {principal.tier}")
    quotas.ensure_can_open_intent(db, principal)
    now = utcnow()
    intent = Intent(id=new_id(), agent_id=agent.id, principal_id=principal.id, intent_type=spec.name,
                    payload=payload.model_dump(mode="json"), status=IntentStatus.OPEN, created_at=now,
                    expires_at=now + timedelta(days=INTENT_TTL_DAYS))
    db.add(intent)
    db.flush()
    audit.record(db, actor_type="agent", actor_id=agent.id, action="intent.posted",
                 subject_type="intent", subject_id=intent.id, data={"intent_type": spec.name})
    return intent_out(intent)


def list_my_intents(db: Session, agent: Agent) -> IntentList:
    query = select(Intent).where(Intent.principal_id == agent.principal_id).order_by(Intent.created_at.desc())
    return IntentList(items=[intent_out(intent) for intent in db.scalars(query)])


def get_my_intent(db: Session, agent: Agent, data: IntentIdInput) -> IntentOut:
    return intent_out(owned_intent(db, agent.principal_id, data.intent_id))


def close_intent(db: Session, agent: Agent, data: IntentIdInput) -> IntentOut:
    intent = owned_intent(db, agent.principal_id, data.intent_id)
    if intent.status == IntentStatus.CLOSED:
        raise Conflict("Intent is already closed")
    intent.status = IntentStatus.CLOSED
    audit.record(db, actor_type="agent", actor_id=agent.id, action="intent.closed",
                 subject_type="intent", subject_id=intent.id, data={})
    return intent_out(intent)
