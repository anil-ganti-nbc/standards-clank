"""Lightweight, dependency-free fixture validators.

The `jsonschema` package is not installed in this environment, and this
repo's tooling is meant to stay dependency-light. These validators check the
same constraints as the JSON Schema files in schemas/ (required fields,
enums, id pattern, the RATIFIED/APPROVED conditional requirements) directly
in Python, rather than interpreting the schema documents at runtime. The
schema files remain the source of truth for external tooling (IDEs, CI in
other languages, editor validation); if you change a schema's constraints,
update the matching checks here too.
"""

from __future__ import annotations

import re

STANDARD_ID_RE = re.compile(r"^STD-[A-Z0-9]+(-[A-Z0-9]+)*-[0-9]{3}$")
PROFILE_ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

STANDARD_DOMAINS = {
    "ui", "collectors", "sources", "classification", "events",
    "evidence", "health", "delivery", "soak", "security", "operator-workflow",
    "data-ontology", "operations",
}
STANDARD_LEVELS = {"MUST", "SHOULD", "MAY"}
STANDARD_STATUSES = {"PROPOSED", "REVIEWED", "RATIFIED", "SUPERSEDED", "RETIRED"}
STANDARD_ORIGINS = {
    "OPERATOR_REQUIREMENT", "DIAGNOSTIC_INCIDENT", "CROSS_CLANK_BEST_PRACTICE",
    "ARCHITECTURAL_INVARIANT", "REGRESSION", "EXPERIMENTAL_FINDING",
}
STANDARD_REQUIRED = {"id", "title", "domain", "level", "status", "version", "requirement"}
STANDARD_RATIFIED_REQUIRED = STANDARD_REQUIRED | {"rationale", "acceptance", "origin", "introduced"}

EXCEPTION_STATUSES = {"PROPOSED", "APPROVED", "REJECTED", "EXPIRED", "SUPERSEDED"}
EXCEPTION_REQUIRED = {"standard_id", "clank", "reason", "proposed_by", "status", "introduced"}


class ValidationError(Exception):
    pass


def validate_standard(obj: dict) -> None:
    missing = STANDARD_REQUIRED - obj.keys()
    if missing:
        raise ValidationError(f"missing required field(s): {sorted(missing)}")

    if not STANDARD_ID_RE.match(obj["id"]):
        raise ValidationError(f"id {obj['id']!r} does not match STD-<DOMAIN...>-NNN")

    if obj["domain"] not in STANDARD_DOMAINS:
        raise ValidationError(f"domain {obj['domain']!r} not a known domain")

    if obj["level"] not in STANDARD_LEVELS:
        raise ValidationError(f"level {obj['level']!r} not one of {sorted(STANDARD_LEVELS)}")

    if obj["status"] not in STANDARD_STATUSES:
        raise ValidationError(f"status {obj['status']!r} not one of {sorted(STANDARD_STATUSES)}")

    if not isinstance(obj["version"], int) or obj["version"] < 1:
        raise ValidationError("version must be an integer >= 1")

    origin = obj.get("origin")
    if origin is not None and origin not in STANDARD_ORIGINS:
        raise ValidationError(f"origin {origin!r} not one of {sorted(STANDARD_ORIGINS)}")

    if obj["status"] == "RATIFIED":
        missing_ratified = STANDARD_RATIFIED_REQUIRED - obj.keys()
        if missing_ratified:
            raise ValidationError(
                f"RATIFIED standard missing required field(s): {sorted(missing_ratified)}"
            )


def validate_exception(obj: dict) -> None:
    missing = EXCEPTION_REQUIRED - obj.keys()
    if missing:
        raise ValidationError(f"missing required field(s): {sorted(missing)}")

    if not STANDARD_ID_RE.match(obj["standard_id"]):
        raise ValidationError(f"standard_id {obj['standard_id']!r} does not match STD-<DOMAIN...>-NNN")

    if obj["status"] not in EXCEPTION_STATUSES:
        raise ValidationError(f"status {obj['status']!r} not one of {sorted(EXCEPTION_STATUSES)}")

    if obj["status"] == "APPROVED" and not obj.get("approved_by"):
        raise ValidationError("APPROVED exception must set approved_by")


def validate_profile(obj: dict) -> None:
    required = {"id", "title"}
    missing = required - obj.keys()
    if missing:
        raise ValidationError(f"missing required field(s): {sorted(missing)}")

    if not PROFILE_ID_RE.match(obj["id"]):
        raise ValidationError(f"id {obj['id']!r} must be kebab-case")

    for std_id in obj.get("standards", []):
        if not STANDARD_ID_RE.match(std_id):
            raise ValidationError(f"standards[] entry {std_id!r} does not match STD-<DOMAIN...>-NNN")
