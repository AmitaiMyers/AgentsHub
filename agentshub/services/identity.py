"""Principals, agents, credentials and verification tiers."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from agentshub.errors import Conflict, Forbidden, NotFound, Unauthorized, ValidationFailed
from agentshub.models import Agent, AgentKind, Principal, PrincipalKind
from agentshub.schemas import (
    AgentOut,
    CreatedAgent,
    CreateAgentInput,
    Me,
    PrincipalOut,
    RegisteredPrincipal,
    RegisterPrincipalInput,
)
from agentshub.security import (
    AGENT_KEY_PREFIX,
    EMAIL_TOKEN_PREFIX,
    PRINCIPAL_TOKEN_PREFIX,
    hash_secret,
    new_id,
    new_secret,
)
from agentshub.services import audit
from agentshub.services.outbox import queue_email


def principal_out(principal: Principal) -> PrincipalOut:
    return PrincipalOut(id=principal.id, kind=principal.kind, display_name=principal.display_name,
                        contact_email=principal.contact_email, org_domain=principal.org_domain,
                        tier=principal.tier, email_verified=principal.email_verified)


def agent_out(agent: Agent) -> AgentOut:
    return AgentOut(id=agent.id, principal_id=agent.principal_id, name=agent.name,
                    kind=agent.kind, key_prefix=agent.key_prefix)


def register_principal(db: Session, data: RegisterPrincipalInput, base_url: str) -> RegisteredPrincipal:
    email = data.contact_email.lower()
    if db.scalars(select(Principal).where(Principal.contact_email == email)).first() is not None:
        raise Conflict("A principal with this contact e-mail already exists")
    if data.kind == PrincipalKind.ORGANIZATION and data.org_domain is None:
        raise ValidationFailed("Organizations must provide org_domain")
    if data.kind == PrincipalKind.PERSON and data.org_domain is not None:
        raise ValidationFailed("org_domain is only for organizations")
    token = new_secret(PRINCIPAL_TOKEN_PREFIX)
    email_token = new_secret(EMAIL_TOKEN_PREFIX)
    principal = Principal(id=new_id(), kind=data.kind, display_name=data.display_name, contact_email=email,
                          org_domain=data.org_domain, tier=0, email_verified=False,
                          email_verification_hash=hash_secret(email_token), token_hash=hash_secret(token))
    db.add(principal)
    db.flush()
    queue_email(db, to_email=email, subject="Verify your AgentsHub e-mail",
                body=f"Open this link to verify your e-mail: {base_url}/verify-email?token={email_token}")
    audit.record(db, actor_type="principal", actor_id=principal.id, action="principal.registered",
                 subject_type="principal", subject_id=principal.id, data={"kind": principal.kind})
    return RegisteredPrincipal(principal=principal_out(principal), principal_token=token)


def verify_email(db: Session, token: str) -> PrincipalOut:
    query = select(Principal).where(Principal.email_verification_hash == hash_secret(token))
    principal = db.scalars(query).first()
    if principal is None:
        raise NotFound("Verification link is invalid or already used")
    principal.email_verified = True
    principal.email_verification_hash = None
    principal.tier = max(principal.tier, 1)
    audit.record(db, actor_type="principal", actor_id=principal.id, action="principal.email_verified",
                 subject_type="principal", subject_id=principal.id, data={"tier": principal.tier})
    return principal_out(principal)


def verify_domain(db: Session, principal: Principal) -> PrincipalOut:
    """MVP check: verified contact e-mail on the claimed domain. DNS TXT proof is planned."""
    if principal.kind != PrincipalKind.ORGANIZATION:
        raise Forbidden("Only organizations verify a domain")
    if not principal.email_verified:
        raise Forbidden("Verify the contact e-mail first")
    assert principal.org_domain is not None, "organizations always have org_domain"
    email_domain = principal.contact_email.rsplit("@", 1)[1]
    if email_domain != principal.org_domain:
        raise Forbidden(f"Contact e-mail domain '{email_domain}' does not match '{principal.org_domain}'")
    principal.tier = max(principal.tier, 2)
    audit.record(db, actor_type="principal", actor_id=principal.id, action="principal.domain_verified",
                 subject_type="principal", subject_id=principal.id, data={"tier": principal.tier})
    return principal_out(principal)


def set_tier(db: Session, principal_id: str, tier: int) -> PrincipalOut:
    principal = db.get(Principal, principal_id)
    if principal is None:
        raise NotFound("Principal not found")
    principal.tier = tier
    audit.record(db, actor_type="admin", actor_id="admin", action="principal.tier_set",
                 subject_type="principal", subject_id=principal.id, data={"tier": tier})
    return principal_out(principal)


def create_agent(db: Session, principal: Principal, data: CreateAgentInput, kind: AgentKind) -> CreatedAgent:
    api_key = new_secret(AGENT_KEY_PREFIX)
    agent = Agent(id=new_id(), principal_id=principal.id, name=data.name, kind=kind,
                  key_prefix=api_key[:12], key_hash=hash_secret(api_key), revoked=False)
    db.add(agent)
    db.flush()
    audit.record(db, actor_type="principal", actor_id=principal.id, action="agent.created",
                 subject_type="agent", subject_id=agent.id, data={"kind": kind, "name": agent.name})
    return CreatedAgent(agent=agent_out(agent), api_key=api_key)


def authenticate_agent(db: Session, api_key: str) -> Agent:
    agent = db.scalars(select(Agent).where(Agent.key_hash == hash_secret(api_key))).first()
    if agent is None or agent.revoked:
        raise Unauthorized("Invalid or revoked agent API key")
    return agent


def authenticate_principal(db: Session, token: str) -> Principal:
    principal = db.scalars(select(Principal).where(Principal.token_hash == hash_secret(token))).first()
    if principal is None:
        raise Unauthorized("Invalid principal token")
    return principal


def principal_of(db: Session, agent: Agent) -> Principal:
    principal = db.get(Principal, agent.principal_id)
    assert principal is not None, f"agent {agent.id} has no principal"
    return principal


HOSTED_AGENT_NAME = "Web lite agent"


def _find_hosted_agent(db: Session, principal: Principal) -> Agent | None:
    query = select(Agent).where(Agent.principal_id == principal.id, Agent.kind == AgentKind.HOSTED,
                                Agent.revoked.is_(False))
    return db.scalars(query).first()


def hosted_agent_of(db: Session, principal: Principal) -> Agent:
    agent = _find_hosted_agent(db, principal)
    if agent is None:
        raise NotFound("This principal has no hosted agent. Sign in again to create one")
    return agent


def ensure_hosted_agent(db: Session, principal: Principal) -> None:
    """Give principals who registered through the API a hosted agent on their first web sign-in."""
    if _find_hosted_agent(db, principal) is None:
        create_agent(db, principal, CreateAgentInput(name=HOSTED_AGENT_NAME), AgentKind.HOSTED)


def me(db: Session, agent: Agent) -> Me:
    return Me(agent=agent_out(agent), principal=principal_out(principal_of(db, agent)))
