"""SQLAlchemy tables. See docs/SYSTEM_DESIGN.md §5."""
from datetime import datetime
from enum import StrEnum
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from agentshub.db import Base, utcnow


class PrincipalKind(StrEnum):
    PERSON = "person"
    ORGANIZATION = "organization"


class AgentKind(StrEnum):
    BRING_YOUR_OWN = "byo"
    HOSTED = "hosted"


class IntentStatus(StrEnum):
    OPEN = "open"
    CLOSED = "closed"


class SessionState(StrEnum):
    OPEN = "open"
    TERMS_AGREED = "terms_agreed"
    HANDOFF_PENDING = "handoff_pending"
    HANDED_OFF = "handed_off"
    DECLINED = "declined"


class ApprovalDecision(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"


class Principal(Base):
    __tablename__ = "principals"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    kind: Mapped[str] = mapped_column(String(20))
    display_name: Mapped[str] = mapped_column(String(120))
    contact_email: Mapped[str] = mapped_column(String(254), unique=True)
    org_domain: Mapped[str | None] = mapped_column(String(253))
    tier: Mapped[int] = mapped_column(Integer, default=0)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    email_verification_hash: Mapped[str | None] = mapped_column(String(64), index=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    principal_id: Mapped[str] = mapped_column(ForeignKey("principals.id"), index=True)
    name: Mapped[str] = mapped_column(String(80))
    kind: Mapped[str] = mapped_column(String(10))
    key_prefix: Mapped[str] = mapped_column(String(12))
    key_hash: Mapped[str] = mapped_column(String(64), unique=True)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class Intent(Base):
    __tablename__ = "intents"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    agent_id: Mapped[str] = mapped_column(ForeignKey("agents.id"), index=True)
    principal_id: Mapped[str] = mapped_column(ForeignKey("principals.id"), index=True)
    intent_type: Mapped[str] = mapped_column(String(40), index=True)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String(10), default=IntentStatus.OPEN, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    expires_at: Mapped[datetime] = mapped_column(DateTime)


class Interest(Base):
    __tablename__ = "interests"
    __table_args__ = (UniqueConstraint("from_intent_id", "to_intent_id"),)

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    from_intent_id: Mapped[str] = mapped_column(ForeignKey("intents.id"), index=True)
    to_intent_id: Mapped[str] = mapped_column(ForeignKey("intents.id"), index=True)
    principal_id: Mapped[str] = mapped_column(ForeignKey("principals.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class NegotiationSession(Base):
    __tablename__ = "negotiation_sessions"
    __table_args__ = (UniqueConstraint("intent_a_id", "intent_b_id"),)

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    intent_a_id: Mapped[str] = mapped_column(ForeignKey("intents.id"), index=True)
    intent_b_id: Mapped[str] = mapped_column(ForeignKey("intents.id"), index=True)
    state: Mapped[str] = mapped_column(String(20), default=SessionState.OPEN)
    message_count: Mapped[int] = mapped_column(Integer, default=0)
    proposal_count: Mapped[int] = mapped_column(Integer, default=0)
    latest_proposal: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    latest_proposal_by: Mapped[str | None] = mapped_column(String(32))
    agreed_terms: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class SessionMessage(Base):
    __tablename__ = "session_messages"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("negotiation_sessions.id"), index=True)
    sender_intent_id: Mapped[str] = mapped_column(ForeignKey("intents.id"))
    sender_principal_id: Mapped[str] = mapped_column(ForeignKey("principals.id"), index=True)
    kind: Mapped[str] = mapped_column(String(20))
    untrusted_text: Mapped[str | None] = mapped_column(Text)
    terms: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class HandoffApproval(Base):
    __tablename__ = "handoff_approvals"
    __table_args__ = (UniqueConstraint("session_id", "principal_id"),)

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("negotiation_sessions.id"), index=True)
    principal_id: Mapped[str] = mapped_column(ForeignKey("principals.id"), index=True)
    decision: Mapped[str] = mapped_column(String(10), default=ApprovalDecision.PENDING)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime)


class AuditEvent(Base):
    __tablename__ = "audit_events"

    seq: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    actor_type: Mapped[str] = mapped_column(String(20))
    actor_id: Mapped[str] = mapped_column(String(32))
    action: Mapped[str] = mapped_column(String(60))
    subject_type: Mapped[str] = mapped_column(String(30))
    subject_id: Mapped[str] = mapped_column(String(32))
    data: Mapped[dict[str, Any]] = mapped_column(JSON)
    prev_hash: Mapped[str] = mapped_column(String(64))
    hash: Mapped[str] = mapped_column(String(64))


class OutboxEmail(Base):
    __tablename__ = "outbox"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    to_email: Mapped[str] = mapped_column(String(254), index=True)
    subject: Mapped[str] = mapped_column(String(200))
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class A2ATask(Base):
    __tablename__ = "a2a_tasks"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    agent_id: Mapped[str] = mapped_column(ForeignKey("agents.id"), index=True)
    context_id: Mapped[str] = mapped_column(String(64))
    skill: Mapped[str] = mapped_column(String(40))
    state: Mapped[str] = mapped_column(String(30))
    result: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
