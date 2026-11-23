"""Web lite agent: pages for people without their own agent (docs/SYSTEM_DESIGN.md §8.5).

Every page acts through the principal's *hosted* agent and the same services as the APIs.
Hand-off approvals use the signed-in human's principal token (cookie), never the agent.
"""
from pathlib import Path
from typing import Annotated, Any

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.datastructures import FormData

from agentshub.errors import Unauthorized, ValidationFailed
from agentshub.intent_types import INTENT_TYPES, RemotePolicy, Seniority
from agentshub.interfaces.deps import DB, AppSettings
from agentshub.models import Principal
from agentshub.schemas import (
    DecideApprovalInput,
    ExpressInterestInput,
    IntentIdInput,
    PostIntentInput,
    RegisterPrincipalInput,
    SendMessageInput,
    SessionIdInput,
)
from agentshub.services import handoff, identity, intents, interests, matching, negotiation
from agentshub.services.outbox import emails_for

TEMPLATES = Jinja2Templates(directory=Path(__file__).parent / "templates")
COOKIE_NAME = "agentshub_principal"
router = APIRouter(include_in_schema=False)


def page(request: Request, template: str, status_code: int = 200, **context: Any) -> HTMLResponse:
    return TEMPLATES.TemplateResponse(request, template, context, status_code=status_code)


def error_page(request: Request, status_code: int, message: str) -> HTMLResponse:
    return page(request, "message.html", status_code=status_code, title="Something went wrong", message=message,
                signed_in=COOKIE_NAME in request.cookies)


def redirect(url: str) -> RedirectResponse:
    return RedirectResponse(url, status_code=303)


def signed_in_principal(request: Request, db: Session) -> Principal:
    if COOKIE_NAME not in request.cookies:
        raise Unauthorized("Sign in first. Go to the home page to sign up or sign in.")
    return identity.authenticate_principal(db, request.cookies[COOKIE_NAME])


def with_session_cookie(response: Response, token: str) -> Response:
    response.set_cookie(COOKIE_NAME, token, httponly=True, samesite="strict", max_age=60 * 60 * 24 * 30)
    return response

# ---------------------------------------------------------------- form parsing


def _text(form: FormData, name: str) -> str:
    return str(form[name]).strip()


def _csv(form: FormData, name: str) -> list[str]:
    return [part.strip() for part in _text(form, name).split(",") if part.strip()]


def _whole_number(form: FormData, name: str) -> int:
    value = _text(form, name).replace(",", "")
    if not value.isdigit():
        raise ValidationFailed(f"'{name}' must be a whole number")
    return int(value)


def _key_values(form: FormData, name: str) -> dict[str, str]:
    pairs = {}
    for line in _text(form, name).splitlines():
        if not line.strip():
            continue
        key, separator, value = line.partition(":")
        if not separator:
            raise ValidationFailed(f"Each line of '{name}' must look like 'key: value'")
        pairs[key.strip()] = value.strip()
    return pairs


def _job_offer_payload(form: FormData) -> dict[str, Any]:
    return {
        "title": _text(form, "title"), "company_name": _text(form, "company_name"),
        "seniority": _text(form, "seniority"), "skills_required": _csv(form, "skills_required"),
        "skills_preferred": _csv(form, "skills_preferred"), "remote_policy": _text(form, "remote_policy"),
        "locations": _csv(form, "locations"), "salary_min": _whole_number(form, "salary_min"),
        "salary_max": _whole_number(form, "salary_max"), "currency": _text(form, "currency").upper(),
        "visa_sponsorship": "visa_sponsorship" in form, "description": _text(form, "description"),
    }


def _job_seek_payload(form: FormData) -> dict[str, Any]:
    return {
        "headline": _text(form, "headline"), "seniority": _text(form, "seniority"),
        "skills": _csv(form, "skills"), "interests": _csv(form, "interests"),
        "years_experience": _whole_number(form, "years_experience"),
        "remote_preferences": [str(value) for value in form.getlist("remote_preferences")],
        "locations": _csv(form, "locations"), "salary_floor": _whole_number(form, "salary_floor"),
        "currency": _text(form, "currency").upper(), "needs_visa_sponsorship": "needs_visa_sponsorship" in form,
        "summary": _text(form, "summary"), "deal_breakers": _csv(form, "deal_breakers"),
    }


def _generic_payload(form: FormData) -> dict[str, Any]:
    region = _text(form, "region")
    return {
        "category": _text(form, "category").lower(), "title": _text(form, "title"), "tags": _csv(form, "tags"),
        "region": region or None, "description": _text(form, "description"),
        "attributes": _key_values(form, "attributes"),
    }


PAYLOAD_BUILDERS = {
    "job_offer": _job_offer_payload,
    "job_seek": _job_seek_payload,
    "generic_need": _generic_payload,
    "generic_offer": _generic_payload,
}


def _terms(form: FormData, family: str) -> dict[str, Any]:
    if family == "job":
        return {"base_salary": _whole_number(form, "base_salary"), "currency": _text(form, "currency").upper(),
                "start_date": _text(form, "start_date"), "remote_policy": _text(form, "remote_policy")}
    price = _text(form, "price")
    return {"summary": _text(form, "summary"), "price": _whole_number(form, "price") if price else None,
            "currency": _text(form, "currency").upper() or None}

# ---------------------------------------------------------------- account pages


@router.get("/")
def home(request: Request) -> Response:
    if COOKIE_NAME in request.cookies:
        return redirect("/dashboard")
    return page(request, "home.html", signed_in=False)


@router.post("/signup")
def signup(request: Request, db: DB, settings: AppSettings, kind: Annotated[str, Form()],
           display_name: Annotated[str, Form()], contact_email: Annotated[str, Form()],
           org_domain: Annotated[str, Form()] = "") -> Response:
    registered = identity.register_principal(db, RegisterPrincipalInput(
        kind=kind, display_name=display_name, contact_email=contact_email,
        org_domain=org_domain.strip() or None), settings.base_url)
    identity.ensure_hosted_agent(db, identity.authenticate_principal(db, registered.principal_token))
    response = page(request, "welcome.html", signed_in=True, principal=registered.principal,
                    token=registered.principal_token)
    return with_session_cookie(response, registered.principal_token)


@router.post("/signin")
def signin(db: DB, token: Annotated[str, Form()]) -> Response:
    identity.ensure_hosted_agent(db, identity.authenticate_principal(db, token.strip()))
    return with_session_cookie(redirect("/dashboard"), token.strip())


@router.post("/signout")
def signout() -> Response:
    response = redirect("/")
    response.delete_cookie(COOKIE_NAME)
    return response


@router.get("/verify-email")
def verify_email(request: Request, db: DB, token: str) -> Response:
    principal = identity.verify_email(db, token)
    return page(request, "message.html", signed_in=COOKIE_NAME in request.cookies, title="E-mail verified",
                message=f"Thanks, {principal.display_name}. Your verification tier is now {principal.tier}.")


@router.post("/verify-domain")
def verify_domain(request: Request, db: DB) -> Response:
    identity.verify_domain(db, signed_in_principal(request, db))
    return redirect("/dashboard")


@router.get("/dashboard")
def dashboard(request: Request, db: DB, settings: AppSettings) -> Response:
    principal = signed_in_principal(request, db)
    agent = identity.hosted_agent_of(db, principal)
    postable = [spec for spec in INTENT_TYPES.values()
                if (spec.allowed_kind is None or spec.allowed_kind == principal.kind) and principal.tier >= spec.min_tier]
    return page(request, "dashboard.html", signed_in=True, principal=identity.principal_out(principal),
                intents=intents.list_my_intents(db, agent).items,
                sessions=negotiation.list_sessions(db, agent).items,
                approvals=handoff.list_pending_approvals(db, principal).items,
                postable=postable,
                outbox=emails_for(db, principal.contact_email) if settings.show_dev_outbox else [])

# ---------------------------------------------------------------- intents and matches


@router.get("/intents/new/{intent_type}")
def new_intent_form(request: Request, db: DB, intent_type: str) -> Response:
    signed_in_principal(request, db)
    if intent_type not in PAYLOAD_BUILDERS:
        raise ValidationFailed(f"Unknown intent type '{intent_type}'")
    return page(request, "intent_form.html", signed_in=True, intent_type=intent_type,
                seniorities=list(Seniority), remote_policies=list(RemotePolicy))


@router.post("/intents/new/{intent_type}")
async def create_intent(request: Request, db: DB, intent_type: str) -> Response:
    principal = signed_in_principal(request, db)
    if intent_type not in PAYLOAD_BUILDERS:
        raise ValidationFailed(f"Unknown intent type '{intent_type}'")
    payload = PAYLOAD_BUILDERS[intent_type](await request.form())
    intent = intents.post_intent(db, identity.hosted_agent_of(db, principal),
                                 PostIntentInput(intent_type=intent_type, payload=payload))
    return redirect(f"/intents/{intent.id}/matches")


@router.get("/intents/{intent_id}/matches")
def intent_matches(request: Request, db: DB, intent_id: str, notice: str = "") -> Response:
    principal = signed_in_principal(request, db)
    agent = identity.hosted_agent_of(db, principal)
    intent = intents.get_my_intent(db, agent, IntentIdInput(intent_id=intent_id))
    batch = matching.find_matches(db, agent, IntentIdInput(intent_id=intent_id))
    return page(request, "matches.html", signed_in=True, intent=intent, batch=batch, notice=notice)


@router.post("/intents/{intent_id}/close")
def close_intent(request: Request, db: DB, intent_id: str) -> Response:
    principal = signed_in_principal(request, db)
    intents.close_intent(db, identity.hosted_agent_of(db, principal), IntentIdInput(intent_id=intent_id))
    return redirect("/dashboard")


@router.post("/interests")
def express_interest(request: Request, db: DB, settings: AppSettings, from_intent_id: Annotated[str, Form()],
                     to_intent_id: Annotated[str, Form()]) -> Response:
    principal = signed_in_principal(request, db)
    result = interests.express_interest(db, identity.hosted_agent_of(db, principal),
                                        ExpressInterestInput(from_intent_id=from_intent_id, to_intent_id=to_intent_id),
                                        settings.base_url)
    if result.session_id is not None:
        return redirect(f"/sessions/{result.session_id}")
    return redirect(f"/intents/{from_intent_id}/matches?notice=Interest+sent.+A+session+opens+when+they+opt+in+too.")

# ---------------------------------------------------------------- sessions and approvals


@router.get("/sessions/{session_id}")
def session_page(request: Request, db: DB, session_id: str) -> Response:
    principal = signed_in_principal(request, db)
    view = negotiation.get_session(db, identity.hosted_agent_of(db, principal), SessionIdInput(session_id=session_id))
    family = INTENT_TYPES[view.counterpart.intent_type].family
    return page(request, "session.html", signed_in=True, session=view, family=family,
                remote_policies=list(RemotePolicy))


@router.post("/sessions/{session_id}/messages")
async def send_message(request: Request, db: DB, session_id: str) -> Response:
    principal = signed_in_principal(request, db)
    agent = identity.hosted_agent_of(db, principal)
    form = await request.form()
    kind = _text(form, "kind")
    view = negotiation.get_session(db, agent, SessionIdInput(session_id=session_id))
    terms = _terms(form, INTENT_TYPES[view.counterpart.intent_type].family) if kind == "propose_terms" else None
    text = _text(form, "text") if "text" in form else ""
    negotiation.send_message(db, agent, SendMessageInput(session_id=session_id, kind=kind, text=text or None,
                                                         terms=terms))
    return redirect(f"/sessions/{session_id}")


@router.post("/sessions/{session_id}/handoff")
def request_handoff(request: Request, db: DB, settings: AppSettings, session_id: str) -> Response:
    principal = signed_in_principal(request, db)
    negotiation.request_handoff(db, identity.hosted_agent_of(db, principal), SessionIdInput(session_id=session_id),
                                settings.base_url)
    return redirect(f"/sessions/{session_id}")


@router.post("/sessions/{session_id}/approval")
def decide_approval(request: Request, db: DB, session_id: str, decision: Annotated[str, Form()]) -> Response:
    principal = signed_in_principal(request, db)
    handoff.decide(db, principal, session_id, DecideApprovalInput(decision=decision))
    return redirect(f"/sessions/{session_id}")
