"""REST API under /v1 (docs/SYSTEM_DESIGN.md §8.2)."""
import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, Header

from agentshub.errors import Forbidden, Unauthorized
from agentshub.interfaces.deps import DB, AppSettings
from agentshub.models import Agent, AgentKind, Principal
from agentshub.schemas import (
    ApprovalList,
    ApprovalView,
    AuditVerification,
    CreatedAgent,
    CreateAgentInput,
    DecideApprovalInput,
    ExpressInterestInput,
    IntentIdInput,
    IntentList,
    IntentOut,
    IntentTypeList,
    InterestOut,
    MatchBatch,
    Me,
    PostIntentInput,
    PrincipalOut,
    RegisteredPrincipal,
    RegisterPrincipalInput,
    SendMessageInput,
    SessionIdInput,
    SessionList,
    SessionView,
    SetTierInput,
    VerifyEmailInput,
)
from agentshub.security import bearer_token
from agentshub.services import audit, handoff, identity, intents, interests, matching, negotiation

router = APIRouter(prefix="/v1")


def _token(authorization: str | None) -> str:
    if authorization is None:
        raise Unauthorized("Missing 'Authorization: Bearer <token>' header")
    return bearer_token(authorization)


def current_agent(db: DB, authorization: Annotated[str | None, Header()] = None) -> Agent:
    return identity.authenticate_agent(db, _token(authorization))


def current_principal(db: DB, authorization: Annotated[str | None, Header()] = None) -> Principal:
    return identity.authenticate_principal(db, _token(authorization))


def require_admin(settings: AppSettings, authorization: Annotated[str | None, Header()] = None) -> None:
    if settings.admin_token is None:
        raise Forbidden("The admin API is disabled. Set AGENTSHUB_ADMIN_TOKEN to enable it")
    if not secrets.compare_digest(_token(authorization), settings.admin_token):
        raise Unauthorized("Invalid admin token")


CurrentAgent = Annotated[Agent, Depends(current_agent)]
CurrentPrincipal = Annotated[Principal, Depends(current_principal)]

# ---------------------------------------------------------------- humans (principal token)


@router.post("/principals", status_code=201, tags=["principals"])
def register_principal(db: DB, settings: AppSettings, data: RegisterPrincipalInput) -> RegisteredPrincipal:
    return identity.register_principal(db, data, settings.base_url)


@router.post("/principals/verify-email", tags=["principals"])
def verify_email(db: DB, data: VerifyEmailInput) -> PrincipalOut:
    return identity.verify_email(db, data.token)


@router.post("/principals/verify-domain", tags=["principals"])
def verify_domain(db: DB, principal: CurrentPrincipal) -> PrincipalOut:
    return identity.verify_domain(db, principal)


@router.post("/agents", status_code=201, tags=["principals"])
def create_agent(db: DB, principal: CurrentPrincipal, data: CreateAgentInput) -> CreatedAgent:
    return identity.create_agent(db, principal, data, AgentKind.BRING_YOUR_OWN)


@router.get("/approvals", tags=["approvals"])
def list_approvals(db: DB, principal: CurrentPrincipal) -> ApprovalList:
    return handoff.list_pending_approvals(db, principal)


@router.post("/approvals/{session_id}", tags=["approvals"])
def decide_approval(db: DB, principal: CurrentPrincipal, session_id: str, data: DecideApprovalInput) -> ApprovalView:
    return handoff.decide(db, principal, session_id, data)

# ---------------------------------------------------------------- agents (API key)


@router.get("/me", tags=["agents"])
def whoami(db: DB, agent: CurrentAgent) -> Me:
    return identity.me(db, agent)


@router.get("/intent-types", tags=["intents"])
def list_intent_types() -> IntentTypeList:
    return intents.intent_type_list()


@router.post("/intents", status_code=201, tags=["intents"])
def post_intent(db: DB, agent: CurrentAgent, data: PostIntentInput) -> IntentOut:
    return intents.post_intent(db, agent, data)


@router.get("/intents", tags=["intents"])
def list_my_intents(db: DB, agent: CurrentAgent) -> IntentList:
    return intents.list_my_intents(db, agent)


@router.get("/intents/{intent_id}", tags=["intents"])
def get_intent(db: DB, agent: CurrentAgent, intent_id: str) -> IntentOut:
    return intents.get_my_intent(db, agent, IntentIdInput(intent_id=intent_id))


@router.post("/intents/{intent_id}/close", tags=["intents"])
def close_intent(db: DB, agent: CurrentAgent, intent_id: str) -> IntentOut:
    return intents.close_intent(db, agent, IntentIdInput(intent_id=intent_id))


@router.get("/intents/{intent_id}/matches", tags=["matching"])
def find_matches(db: DB, agent: CurrentAgent, intent_id: str) -> MatchBatch:
    return matching.find_matches(db, agent, IntentIdInput(intent_id=intent_id))


@router.post("/interests", tags=["matching"])
def express_interest(db: DB, agent: CurrentAgent, settings: AppSettings, data: ExpressInterestInput) -> InterestOut:
    return interests.express_interest(db, agent, data, settings.base_url)


@router.get("/sessions", tags=["sessions"])
def list_sessions(db: DB, agent: CurrentAgent) -> SessionList:
    return negotiation.list_sessions(db, agent)


@router.get("/sessions/{session_id}", tags=["sessions"])
def get_session(db: DB, agent: CurrentAgent, session_id: str) -> SessionView:
    return negotiation.get_session(db, agent, SessionIdInput(session_id=session_id))


@router.post("/sessions/{session_id}/messages", tags=["sessions"])
def send_message(db: DB, agent: CurrentAgent, session_id: str, data: SendMessageInput) -> SessionView:
    if data.session_id != session_id:
        raise Forbidden("session_id in the body must match the URL")
    return negotiation.send_message(db, agent, data)


@router.post("/sessions/{session_id}/handoff", tags=["sessions"])
def request_handoff(db: DB, agent: CurrentAgent, settings: AppSettings, session_id: str) -> SessionView:
    return negotiation.request_handoff(db, agent, SessionIdInput(session_id=session_id), settings.base_url)

# ---------------------------------------------------------------- admin


@router.get("/admin/audit/verify", tags=["admin"], dependencies=[Depends(require_admin)])
def verify_audit(db: DB) -> AuditVerification:
    return audit.verify_chain(db)


@router.post("/admin/principals/{principal_id}/tier", tags=["admin"], dependencies=[Depends(require_admin)])
def set_tier(db: DB, principal_id: str, data: SetTierInput) -> PrincipalOut:
    return identity.set_tier(db, principal_id, data.tier)
