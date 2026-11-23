"""Append-only, hash-chained audit log."""
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from agentshub.db import utcnow
from agentshub.models import AuditEvent
from agentshub.schemas import AuditVerification
from agentshub.security import canonical_json, sha256_hex

GENESIS_HASH = "0" * 64


def _event_body(event: AuditEvent) -> dict[str, Any]:
    return {
        "created_at": event.created_at.isoformat(),
        "actor_type": event.actor_type,
        "actor_id": event.actor_id,
        "action": event.action,
        "subject_type": event.subject_type,
        "subject_id": event.subject_id,
        "data": event.data,
    }


def _chain_hash(prev_hash: str, event: AuditEvent) -> str:
    return sha256_hex(prev_hash + canonical_json(_event_body(event)))


def record(db: Session, *, actor_type: str, actor_id: str, action: str,
           subject_type: str, subject_id: str, data: dict[str, Any]) -> None:
    """Append one event. Single-writer assumption: SQLite serialises writes; PostgreSQL needs a lock."""
    last = db.scalars(select(AuditEvent).order_by(AuditEvent.seq.desc()).limit(1)).first()
    prev_hash = last.hash if last is not None else GENESIS_HASH
    event = AuditEvent(created_at=utcnow(), actor_type=actor_type, actor_id=actor_id, action=action,
                       subject_type=subject_type, subject_id=subject_id, data=data, prev_hash=prev_hash, hash="")
    event.hash = _chain_hash(prev_hash, event)
    db.add(event)
    db.flush()


def verify_chain(db: Session) -> AuditVerification:
    expected_prev = GENESIS_HASH
    checked = 0
    for event in db.scalars(select(AuditEvent).order_by(AuditEvent.seq)):
        checked += 1
        if event.prev_hash != expected_prev or event.hash != _chain_hash(event.prev_hash, event):
            return AuditVerification(valid=False, events_checked=checked, first_invalid_seq=event.seq)
        expected_prev = event.hash
    return AuditVerification(valid=True, events_checked=checked, first_invalid_seq=None)
