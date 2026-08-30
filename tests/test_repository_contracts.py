"""Tests for this repository's own contracts (schema shape, id format,
no duplicate ids). These validate repository structure, not any
application behaviour — Standards Clank has no runtime application yet.
"""

import json
from pathlib import Path

import pytest

from validators import (
    ValidationError,
    validate_exception,
    validate_profile,
    validate_standard,
)

FIXTURES = Path(__file__).parent / "fixtures"


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text())


# -- standard.schema.json fixtures -----------------------------------------

def test_valid_proposed_standard_accepted():
    validate_standard(load("valid_standard_proposed.json"))


def test_valid_ratified_standard_accepted():
    validate_standard(load("valid_standard_ratified.json"))


def test_rejects_bad_level():
    with pytest.raises(ValidationError):
        validate_standard(load("invalid_standard_bad_level.json"))


def test_rejects_bad_status():
    with pytest.raises(ValidationError):
        validate_standard(load("invalid_standard_bad_status.json"))


def test_rejects_bad_id_format():
    with pytest.raises(ValidationError):
        validate_standard(load("invalid_standard_bad_id.json"))


def test_ratified_standard_requires_normative_fields():
    with pytest.raises(ValidationError):
        validate_standard(load("invalid_standard_ratified_missing_fields.json"))


# -- exception.schema.json fixtures -----------------------------------------

def test_valid_exception_accepted():
    validate_exception(load("valid_exception.json"))


def test_approved_exception_requires_approver():
    with pytest.raises(ValidationError):
        validate_exception(load("invalid_exception_approved_without_approver.json"))


# -- profile.schema.json fixtures --------------------------------------------

def test_valid_profile_accepted():
    validate_profile(load("valid_profile.json"))


def test_profile_rejects_bad_id():
    with pytest.raises(ValidationError):
        validate_profile(load("invalid_profile_bad_id.json"))


# -- id format ----------------------------------------------------------------

@pytest.mark.parametrize(
    "std_id",
    ["STD-UI-COM-001", "STD-UI-NEWS-001", "STD-COL-001", "STD-SRC-001", "STD-EVT-001"],
)
def test_id_format_examples_from_spec_are_valid(std_id):
    from validators import STANDARD_ID_RE
    assert STANDARD_ID_RE.match(std_id)


@pytest.mark.parametrize("bad_id", ["CVC-UI-001", "STD-ui-001", "STD-001", "STD-UI-1"])
def test_id_format_rejects_bad_examples(bad_id):
    from validators import STANDARD_ID_RE
    assert not STANDARD_ID_RE.match(bad_id)


# -- duplicate id detection across real fixtures -----------------------------

def test_no_duplicate_standard_ids_among_valid_fixtures():
    ids = []
    for name in ["valid_standard_proposed.json", "valid_standard_ratified.json"]:
        ids.append(load(name)["id"])
    assert len(ids) == len(set(ids)), f"duplicate standard ids: {ids}"


def test_duplicate_id_fixtures_are_in_fact_duplicates():
    duplicates_dir = FIXTURES / "duplicates"
    ids = [json.loads(p.read_text())["id"] for p in sorted(duplicates_dir.glob("*.json"))]
    assert len(ids) == 2
    assert len(set(ids)) == 1, "duplicates/ fixtures were expected to share one id"


def detect_duplicate_ids(objs: list[dict]) -> list[str]:
    """Return ids that appear more than once. Used by the check above and
    intended to be reused by any future `standards/` directory scanner."""
    seen: dict[str, int] = {}
    for obj in objs:
        seen[obj["id"]] = seen.get(obj["id"], 0) + 1
    return [i for i, count in seen.items() if count > 1]


def test_detect_duplicate_ids_helper_flags_the_duplicates_fixture():
    duplicates_dir = FIXTURES / "duplicates"
    objs = [json.loads(p.read_text()) for p in duplicates_dir.glob("*.json")]
    assert detect_duplicate_ids(objs) == ["STD-COL-999"]


def _all_standard_files():
    standards_dir = Path(__file__).parent.parent / "standards"
    return sorted(standards_dir.rglob("*.json"))


def test_every_ratified_standard_traces_to_a_decision_record():
    """A standard may only be RATIFIED/REVIEWED alongside a recorded operator
    decision — see docs/governance.md. This doesn't prove the decision was
    genuine, but it does guard against a status flip landing with no
    traceable review/ratification artefact referenced at all."""
    decisions_dir = Path(__file__).parent.parent / "decisions"
    decision_files = {p.name for p in decisions_dir.glob("*.md")}
    for path in _all_standard_files():
        obj = json.loads(path.read_text())
        if obj["status"] in {"RATIFIED", "REVIEWED"}:
            notes = obj.get("notes", "")
            referenced = [d for d in decision_files if d in notes]
            assert referenced, (
                f"{path} has status {obj['status']!r} but its notes field does not "
                "reference a decisions/*.md file recording the review/ratification act"
            )


def test_every_standard_file_is_schema_valid():
    for path in _all_standard_files():
        obj = json.loads(path.read_text())
        validate_standard(obj)


def test_no_duplicate_standard_ids_in_standards_directory():
    objs = [json.loads(p.read_text()) for p in _all_standard_files()]
    ids = [o["id"] for o in objs]
    assert len(ids) == len(set(ids)), f"duplicate standard ids in standards/: {ids}"


def test_every_standard_filename_matches_its_id():
    for path in _all_standard_files():
        obj = json.loads(path.read_text())
        assert path.stem == obj["id"], f"{path} filename does not match id {obj['id']!r}"


def _all_profile_files():
    profiles_dir = Path(__file__).parent.parent / "profiles"
    return sorted(profiles_dir.glob("*.json"))


def test_every_profile_file_is_schema_valid():
    for path in _all_profile_files():
        validate_profile(json.loads(path.read_text()))


def test_every_profile_filename_matches_its_id():
    for path in _all_profile_files():
        obj = json.loads(path.read_text())
        assert path.stem == obj["id"], f"{path} filename does not match id {obj['id']!r}"


def test_standard_applies_to_references_a_real_profile():
    profile_ids = {json.loads(p.read_text())["id"] for p in _all_profile_files()}
    for path in _all_standard_files():
        obj = json.loads(path.read_text())
        for ref in obj.get("applies_to", []):
            assert ref in profile_ids, f"{path} applies_to references unknown profile {ref!r}"
