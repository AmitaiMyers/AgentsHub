"""E-mail outbox. Stands in for real delivery in the MVP."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from agentshub.models import OutboxEmail
from agentshub.security import new_id


def queue_email(db: Session, *, to_email: str, subject: str, body: str) -> None:
    db.add(OutboxEmail(id=new_id(), to_email=to_email, subject=subject, body=body))
    db.flush()


def emails_for(db: Session, to_email: str) -> list[OutboxEmail]:
    query = select(OutboxEmail).where(OutboxEmail.to_email == to_email).order_by(OutboxEmail.created_at.desc())
    return list(db.scalars(query))
