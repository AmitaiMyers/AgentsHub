"""Intent type schemas, disclosure stages, matching rules and negotiation terms.

Every principal-facing rule about *what* can be posted, *who* can see it and
*which* pairs are compatible lives here. Services only orchestrate.
"""
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from enum import IntEnum, StrEnum
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

from agentshub.config import MAX_TEXT_LENGTH
from agentshub.errors import ValidationFailed
from agentshub.models import PrincipalKind


class Stage(IntEnum):
    """How far a relationship must progress before a field is visible to the counterpart."""

    PUBLIC = 1
    MUTUAL = 2
    HANDOFF = 3


class Seniority(StrEnum):
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    STAFF = "staff"
    PRINCIPAL = "principal"


class RemotePolicy(StrEnum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"


ShortText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=80)]
LongText = Annotated[str, StringConstraints(strip_whitespace=True, max_length=MAX_TEXT_LENGTH)]
CurrencyCode = Annotated[str, StringConstraints(pattern=r"^[A-Z]{3}$")]
CategorySlug = Annotated[str, StringConstraints(pattern=r"^[a-z0-9][a-z0-9-]{1,39}$")]


def public(**kwargs: Any) -> Any:
    return Field(json_schema_extra={"stage": Stage.PUBLIC.name.lower()}, **kwargs)


def mutual(**kwargs: Any) -> Any:
    return Field(json_schema_extra={"stage": Stage.MUTUAL.name.lower()}, **kwargs)


class Payload(BaseModel):
    model_config = ConfigDict(extra="forbid")


class JobOffer(Payload):
    title: ShortText = public()
    company_name: ShortText = mutual()
    seniority: Seniority = public()
    skills_required: list[ShortText] = public(max_length=30)
    skills_preferred: list[ShortText] = public(default_factory=list, max_length=30)
    remote_policy: RemotePolicy = public()
    locations: list[ShortText] = public(default_factory=list, max_length=20)
    salary_min: int = public(gt=0)
    salary_max: int = public(gt=0)
    currency: CurrencyCode = public()
    visa_sponsorship: bool = public()
    description: LongText = public(default="")

    @model_validator(mode="after")
    def check_consistency(self) -> "JobOffer":
        if self.salary_min > self.salary_max:
            raise ValueError("salary_min must not exceed salary_max")
        if self.remote_policy != RemotePolicy.REMOTE and not self.locations:
            raise ValueError("locations are required unless the role is fully remote")
        return self


class JobSeek(Payload):
    headline: ShortText = public()
    seniority: Seniority = public()
    skills: list[ShortText] = public(min_length=1, max_length=50)
    interests: list[ShortText] = public(default_factory=list, max_length=30)
    years_experience: int = public(ge=0, le=60)
    remote_preferences: list[RemotePolicy] = public(min_length=1, max_length=3)
    locations: list[ShortText] = public(default_factory=list, max_length=20)
    salary_floor: int = public(gt=0)
    currency: CurrencyCode = public()
    needs_visa_sponsorship: bool = public()
    summary: LongText = mutual(default="")
    deal_breakers: list[ShortText] = mutual(default_factory=list, max_length=20)

    @model_validator(mode="after")
    def check_consistency(self) -> "JobSeek":
        accepts_on_site_work = any(policy != RemotePolicy.REMOTE for policy in self.remote_preferences)
        if accepts_on_site_work and not self.locations:
            raise ValueError("locations are required when hybrid or onsite work is acceptable")
        return self


class GenericIntent(Payload):
    category: CategorySlug = public()
    title: ShortText = public()
    tags: list[ShortText] = public(default_factory=list, max_length=20)
    region: ShortText | None = public(default=None)
    description: LongText = public(default="")
    attributes: dict[ShortText, ShortText] = mutual(default_factory=dict, max_length=20)


class GenericNeed(GenericIntent):
    pass


class GenericOffer(GenericIntent):
    pass


# ---------------------------------------------------------------- negotiation terms


class JobTerms(Payload):
    base_salary: int = Field(gt=0)
    currency: CurrencyCode
    start_date: date
    remote_policy: RemotePolicy


class GenericTerms(Payload):
    summary: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=500)]
    price: int | None = Field(default=None, ge=0)
    currency: CurrencyCode | None = None

    @model_validator(mode="after")
    def check_price_currency(self) -> "GenericTerms":
        if (self.price is None) != (self.currency is None):
            raise ValueError("price and currency must be given together")
        return self


# ---------------------------------------------------------------- type registry


@dataclass(frozen=True)
class IntentTypeSpec:
    name: str
    description: str
    payload_model: type[Payload]
    complement: str
    allowed_kind: PrincipalKind | None
    min_tier: int
    family: str


INTENT_TYPES: dict[str, IntentTypeSpec] = {
    spec.name: spec
    for spec in (
        IntentTypeSpec("job_offer", "An organization offering a job.", JobOffer, "job_seek",
                       PrincipalKind.ORGANIZATION, min_tier=2, family="job"),
        IntentTypeSpec("job_seek", "A person looking for a job.", JobSeek, "job_offer",
                       PrincipalKind.PERSON, min_tier=0, family="job"),
        IntentTypeSpec("generic_need", "Anyone needing something in a category.", GenericNeed, "generic_offer",
                       None, min_tier=0, family="generic"),
        IntentTypeSpec("generic_offer", "Anyone offering something in a category.", GenericOffer, "generic_need",
                       None, min_tier=0, family="generic"),
    )
}


def get_spec(intent_type: str) -> IntentTypeSpec:
    if intent_type not in INTENT_TYPES:
        raise ValidationFailed(f"Unknown intent_type '{intent_type}'. Known types: {sorted(INTENT_TYPES)}")
    return INTENT_TYPES[intent_type]


def field_stages(spec: IntentTypeSpec) -> dict[str, Stage]:
    stages = {}
    for name, field in spec.payload_model.model_fields.items():
        extra = field.json_schema_extra
        assert isinstance(extra, dict), f"{spec.name}.{name} must declare a disclosure stage"
        stages[name] = Stage[str(extra["stage"]).upper()]
    return stages


def visible_fields(spec: IntentTypeSpec, payload: dict[str, Any], reached: Stage) -> dict[str, Any]:
    stages = field_stages(spec)
    return {name: value for name, value in payload.items() if stages[name] <= reached}


# ---------------------------------------------------------------- prohibited fields

PROHIBITED_FIELD_NAMES = frozenset({
    "age", "date_of_birth", "dob", "birth_year", "gender", "sex", "race", "ethnicity", "religion",
    "nationality", "national_origin", "citizenship", "marital_status", "pregnancy", "disability",
    "sexual_orientation", "salary_history", "previous_salary", "photo", "genetic_information",
})


def _normalize_key(key: str) -> str:
    return key.strip().lower().replace("-", "_").replace(" ", "_")


def find_prohibited_keys(value: Any) -> list[str]:
    """Return every key, at any depth, that names a protected trait."""
    found: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            if _normalize_key(str(key)) in PROHIBITED_FIELD_NAMES:
                found.append(str(key))
            found.extend(find_prohibited_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            found.extend(find_prohibited_keys(nested))
    return found


# ---------------------------------------------------------------- matching rules


def _lower_set(values: list[str]) -> set[str]:
    return {value.strip().lower() for value in values}


@dataclass(frozen=True)
class Rule:
    description: str
    holds: Callable[[Any, Any], bool]


def _shares_location(offer: JobOffer, seek: JobSeek) -> bool:
    if offer.remote_policy == RemotePolicy.REMOTE:
        return True
    return bool(_lower_set(offer.locations) & _lower_set(seek.locations))


JOB_RULES: tuple[Rule, ...] = (
    Rule("same seniority", lambda offer, seek: offer.seniority == seek.seniority),
    Rule("work arrangement accepted by the seeker", lambda offer, seek: offer.remote_policy in seek.remote_preferences),
    Rule("shared location for non-remote work", _shares_location),
    Rule("same salary currency", lambda offer, seek: offer.currency == seek.currency),
    Rule("salary range reaches the seeker's floor", lambda offer, seek: offer.salary_max >= seek.salary_floor),
    Rule("visa sponsorship available if needed",
         lambda offer, seek: offer.visa_sponsorship or not seek.needs_visa_sponsorship),
    Rule("seeker has every required skill",
         lambda offer, seek: _lower_set(offer.skills_required) <= _lower_set(seek.skills)),
)

GENERIC_RULES: tuple[Rule, ...] = (
    Rule("same category", lambda need, offer: need.category == offer.category),
    Rule("compatible region",
         lambda need, offer: need.region is None or offer.region is None
         or need.region.lower() == offer.region.lower()),
)


@dataclass(frozen=True)
class PairCheck:
    compatible: bool
    rules_passed: tuple[str, ...]
    first_failed_rule: str | None


def _oriented(spec: IntentTypeSpec, payload: Payload, other: Payload) -> tuple[Payload, Payload]:
    """Return the pair as (offer-like, seek-like) for job, (need, offer) for generic."""
    first_is_offer_side = spec.name in ("job_offer", "generic_need")
    return (payload, other) if first_is_offer_side else (other, payload)


def check_pair(spec: IntentTypeSpec, payload: Payload, other_spec: IntentTypeSpec, other: Payload) -> PairCheck:
    if spec.complement != other_spec.name:
        return PairCheck(False, (), f"{spec.name} does not pair with {other_spec.name}")
    rules = JOB_RULES if spec.family == "job" else GENERIC_RULES
    left, right = _oriented(spec, payload, other)
    passed: list[str] = []
    for rule in rules:
        if not rule.holds(left, right):
            return PairCheck(False, tuple(passed), rule.description)
        passed.append(rule.description)
    return PairCheck(True, tuple(passed), None)


def own_preference_overlap(spec: IntentTypeSpec, own: Payload, candidate: Payload) -> int:
    """How many of the requester's *own* declared preferences the candidate meets. Not a fit score."""
    if isinstance(own, JobOffer):
        assert isinstance(candidate, JobSeek)
        return len(_lower_set(own.skills_preferred) & _lower_set(candidate.skills))
    if isinstance(own, JobSeek):
        assert isinstance(candidate, JobOffer)
        return len(_lower_set(own.interests) & _lower_set(candidate.skills_required + candidate.skills_preferred))
    assert isinstance(own, GenericIntent) and isinstance(candidate, GenericIntent), spec.name
    return len(_lower_set(own.tags) & _lower_set(candidate.tags))


# ---------------------------------------------------------------- terms and zone of agreement


@dataclass(frozen=True)
class SalaryZone:
    low: int
    high: int
    currency: str


def salary_zone(offer: JobOffer, seek: JobSeek) -> SalaryZone:
    return SalaryZone(low=max(offer.salary_min, seek.salary_floor), high=offer.salary_max, currency=offer.currency)


def job_pair(spec: IntentTypeSpec, payload: Payload, other: Payload) -> tuple[JobOffer, JobSeek]:
    offer, seek = _oriented(spec, payload, other)
    assert isinstance(offer, JobOffer) and isinstance(seek, JobSeek)
    return offer, seek


def validate_terms(spec: IntentTypeSpec, payload: Payload, other: Payload, raw_terms: dict[str, Any]) -> dict[str, Any]:
    """Validate proposed terms for this pair and return their JSON form."""
    if spec.family == "generic":
        return GenericTerms.model_validate(raw_terms).model_dump(mode="json")
    terms = JobTerms.model_validate(raw_terms)
    offer, seek = job_pair(spec, payload, other)
    zone = salary_zone(offer, seek)
    if terms.currency != zone.currency:
        raise ValidationFailed(f"Terms currency must be {zone.currency}")
    if not zone.low <= terms.base_salary <= zone.high:
        raise ValidationFailed(f"base_salary must be inside the zone of agreement {zone.low}-{zone.high} {zone.currency}")
    if terms.remote_policy != offer.remote_policy:
        raise ValidationFailed(f"remote_policy must match the role's policy '{offer.remote_policy}'")
    return terms.model_dump(mode="json")


def parse_payload(spec: IntentTypeSpec, payload: dict[str, Any]) -> Payload:
    return spec.payload_model.model_validate(payload)
