"""Per-principal quotas by verification tier."""
from datetime import timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from agentshub.config import QUOTAS_BY_TIER
from agentshub.db import utcnow
from agentshub.errors import QuotaExceeded
from agentshub.models import Intent, IntentStatus, Interest, Principal, SessionMessage


def _count(db: Session, query) -> int:
    return db.scalar(select(func.count()).select_from(query.subquery()))


def ensure_can_open_intent(db: Session, principal: Principal) -> None:
    limit = QUOTAS_BY_TIER[principal.tier].open_intents
    query = select(Intent.id).where(Intent.principal_id == principal.id, Intent.status == IntentStatus.OPEN,
                                    Intent.expires_at > utcnow())
    if _count(db, query) >= limit:
        raise QuotaExceeded(f"Tier {principal.tier} allows {limit} open intents. Close one or verify to raise it")


def ensure_can_express_interest(db: Session, principal: Principal) -> None:
    limit = QUOTAS_BY_TIER[principal.tier].interests_per_day
    since = utcnow() - timedelta(days=1)
    query = select(Interest.id).where(Interest.principal_id == principal.id, Interest.created_at > since)
    if _count(db, query) >= limit:
        raise QuotaExceeded(f"Tier {principal.tier} allows {limit} expressions of interest per day")


def ensure_can_send_message(db: Session, principal: Principal) -> None:
    limit = QUOTAS_BY_TIER[principal.tier].messages_per_day
    since = utcnow() - timedelta(days=1)
    query = select(SessionMessage.id).where(SessionMessage.sender_principal_id == principal.id,
                                            SessionMessage.created_at > since)
    if _count(db, query) >= limit:
        raise QuotaExceeded(f"Tier {principal.tier} allows {limit} session messages per day")
