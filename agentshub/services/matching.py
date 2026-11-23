"""Rule-based discovery. No hub-computed fit scores (docs/SYSTEM_DESIGN.md §3, §6)."""
import random
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from agentshub.config import MATCH_BATCH_SIZE
from agentshub.db import utcnow
from agentshub.intent_types import (
    PairCheck,
    Stage,
    check_pair,
    get_spec,
    own_preference_overlap,
    parse_payload,
    visible_fields,
)
from agentshub.models import Agent, Intent, IntentStatus, Interest, Principal
from agentshub.schemas import CounterpartBadge, IntentIdInput, MatchBatch, MatchView
from agentshub.services.intents import owned_intent, require_live

BATCH_NOTE = ("Filtered by both principals' declared rules and ordered only by YOUR declared preferences, "
              "ties in random order. The hub does not score or rank people.")


@dataclass(frozen=True)
class Candidate:
    intent: Intent
    check: PairCheck
    overlap: int


def counterpart_badge(db: Session, intent: Intent) -> CounterpartBadge:
    principal = db.get(Principal, intent.principal_id)
    agent = db.get(Agent, intent.agent_id)
    assert principal is not None and agent is not None, f"intent {intent.id} lost its owner"
    return CounterpartBadge(principal_kind=principal.kind, verification_tier=principal.tier, agent_kind=agent.kind)


def _ids(db: Session, query) -> set[str]:
    return set(db.scalars(query))


def find_matches(db: Session, agent: Agent, data: IntentIdInput) -> MatchBatch:
    own = owned_intent(db, agent.principal_id, data.intent_id)
    require_live(own)
    spec = get_spec(own.intent_type)
    other_spec = get_spec(spec.complement)
    own_payload = parse_payload(spec, own.payload)
    already_interested = _ids(db, select(Interest.to_intent_id).where(Interest.from_intent_id == own.id))
    interested_in_me = _ids(db, select(Interest.from_intent_id).where(Interest.to_intent_id == own.id))
    query = select(Intent).where(Intent.intent_type == other_spec.name, Intent.status == IntentStatus.OPEN,
                                 Intent.expires_at > utcnow(), Intent.principal_id != own.principal_id)
    candidates: list[Candidate] = []
    for intent in db.scalars(query):
        if intent.id in already_interested:
            continue
        payload = parse_payload(other_spec, intent.payload)
        check = check_pair(spec, own_payload, other_spec, payload)
        if check.compatible:
            candidates.append(Candidate(intent, check, own_preference_overlap(spec, own_payload, payload)))
    random.SystemRandom().shuffle(candidates)
    candidates.sort(key=lambda candidate: candidate.overlap, reverse=True)
    items = [
        MatchView(
            intent_id=candidate.intent.id, intent_type=candidate.intent.intent_type,
            counterpart=counterpart_badge(db, candidate.intent),
            public_fields=visible_fields(other_spec, candidate.intent.payload, Stage.PUBLIC),
            rules_passed=list(candidate.check.rules_passed), your_preference_overlap=candidate.overlap,
            counterpart_already_interested=candidate.intent.id in interested_in_me,
        )
        for candidate in candidates[:MATCH_BATCH_SIZE]
    ]
    return MatchBatch(for_intent_id=own.id, items=items, note=BATCH_NOTE)
