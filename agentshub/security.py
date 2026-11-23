"""Secrets, identifiers and hashing."""
import hashlib
import json
import secrets
import uuid
from typing import Any

from agentshub.errors import Unauthorized

AGENT_KEY_PREFIX = "ahk_"
PRINCIPAL_TOKEN_PREFIX = "ahp_"
EMAIL_TOKEN_PREFIX = "ahv_"


def new_id() -> str:
    return uuid.uuid4().hex


def new_secret(prefix: str) -> str:
    return prefix + secrets.token_urlsafe(32)


def hash_secret(secret: str) -> str:
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def bearer_token(authorization_header: str) -> str:
    scheme, _, token = authorization_header.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        raise Unauthorized("Authorization header must be 'Bearer <token>'")
    return token.strip()
