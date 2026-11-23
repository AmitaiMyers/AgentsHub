"""Runtime settings and fixed product limits."""
import os
from dataclasses import dataclass

MATCH_BATCH_SIZE = 5
MAX_SESSION_MESSAGES = 40
MAX_SESSION_PROPOSALS = 6
MAX_TEXT_LENGTH = 2000
INTENT_TTL_DAYS = 60


@dataclass(frozen=True)
class TierQuota:
    open_intents: int
    interests_per_day: int
    messages_per_day: int


QUOTAS_BY_TIER: dict[int, TierQuota] = {
    0: TierQuota(open_intents=3, interests_per_day=10, messages_per_day=50),
    1: TierQuota(open_intents=10, interests_per_day=30, messages_per_day=200),
    2: TierQuota(open_intents=25, interests_per_day=100, messages_per_day=1000),
    3: TierQuota(open_intents=100, interests_per_day=500, messages_per_day=5000),
}


@dataclass(frozen=True)
class Settings:
    database_url: str
    base_url: str
    admin_token: str | None
    show_dev_outbox: bool
    allowed_hosts: tuple[str, ...]


def _env(name: str, default: str) -> str:
    return os.environ[name] if name in os.environ else default


def load_settings() -> Settings:
    admin_token = _env("AGENTSHUB_ADMIN_TOKEN", "")
    return Settings(
        database_url=_env("AGENTSHUB_DATABASE_URL", "sqlite:///./agentshub.db"),
        base_url=_env("AGENTSHUB_BASE_URL", "http://localhost:8000").rstrip("/"),
        admin_token=admin_token or None,
        show_dev_outbox=_env("AGENTSHUB_SHOW_DEV_OUTBOX", "true") == "true",
        allowed_hosts=tuple(_env("AGENTSHUB_ALLOWED_HOSTS", "127.0.0.1:*,localhost:*").split(",")),
    )
