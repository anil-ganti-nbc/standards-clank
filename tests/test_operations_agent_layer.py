"""Tests for the agent-facing Operations layer:
standards/operations/ratified-index.json, standards/operations/agent-checklist.json,
and docs/operations/constitution.md, checked against the authoritative
standards/operations/*.json files — not against each other, so a stale
generated file or a stale doc can't hide behind agreement with another
stale artefact. Mirrors tests/test_ui_agent_layer.py's design (minus the
known-evidence-index checks: no Operations conformance audit exists yet,
same as the Data/Ontology domain at this stage — see
tools/operations_agent_layer.py's own docstring).

Building this layer is mechanical housekeeping, commissioned after the
operations-standards-v1.0 freeze: no normative standard text changes as
part of it, and the frozen tag (operations-standards-v1.0 -> 7100f29)
is untouched.
"""

import json
import re
from pathlib import Path

from tools.operations_agent_layer import (
    REPO_ROOT,
    STANDARDS_OPERATIONS_DIR,
    build_agent_checklist,
    build_ratified_index,
    load_operations_standards,
    load_ratified_operations_standards,
)

CONSTITUTION_PATH = REPO_ROOT / "docs" / "operations" / "constitution.md"
STD_ID_RE = re.compile(r"STD-OPS-[A-Z0-9]+-\d{3}")

HELD_DEFERRED_REHOMED_MARKERS = [
    "Lifecycle-state model: BLOCKED is prose, not code",
    "Destructive production-action authority",
    "Config drift, remote-host deployment truth, schema/deploy fail-closed",
    "Retry/restart notification idempotency",
]


def _load_index():
    return json.loads((STANDARDS_OPERATIONS_DIR / "ratified-index.json").read_text(encoding="utf-8"))


def _load_checklist():
    return json.loads((STANDARDS_OPERATIONS_DIR / "agent-checklist.json").read_text(encoding="utf-8"))


def _ratified_ids():
    return {s["id"] for s in load_ratified_operations_standards()}


def _proposed_ids():
    return {s["id"] for s in load_operations_standards() if s["status"] == "PROPOSED"}


# -- generated-file drift: the committed JSON must match what the builder produces from the source files --

def test_ratified_index_matches_generator_output():
    assert _load_index() == build_ratified_index()


def test_agent_checklist_matches_generator_output():
    assert _load_checklist() == build_agent_checklist()


# -- ratified-index.json coverage --

def test_every_ratified_standard_appears_exactly_once_in_index():
    index_ids = [entry["id"] for entry in _load_index()]
    ratified_ids = _ratified_ids()
    assert set(index_ids) == ratified_ids
    assert len(index_ids) == 4
    assert len(index_ids) == len(set(index_ids))


def test_no_proposed_rule_appears_in_ratified_index():
    index_ids = {entry["id"] for entry in _load_index()}
    assert index_ids.isdisjoint(_proposed_ids())
    assert _proposed_ids() == set(), "Operations is frozen at 4/0 -- no PROPOSED standard should exist"


def test_index_entries_have_required_fields_and_no_extras():
    required = {
        "id", "title", "level", "applies_to", "version",
        "requirement_summary", "source_file", "ratification_decision",
    }
    for entry in _load_index():
        assert entry.keys() == required, f"{entry['id']}: unexpected fields {entry.keys() - required}"
        assert entry["level"] == "MUST"


def test_checklist_entries_have_no_extra_fields():
    required = {"standard", "question", "failure_means"}
    for item in _load_checklist():
        assert item.keys() == required, f"{item['standard']}: unexpected extra fields {item.keys() - required}"


# -- agent-checklist.json coverage --

def test_checklist_covers_every_ratified_rule_exactly_once():
    checklist_ids = [item["standard"] for item in _load_checklist()]
    assert set(checklist_ids) == _ratified_ids()
    assert len(checklist_ids) == 4
    assert len(checklist_ids) == len(set(checklist_ids))


def test_checklist_items_have_required_fields():
    for item in _load_checklist():
        assert item.get("question")
        assert item.get("failure_means")


# -- ratification decision references resolve --

def test_all_ratification_decision_references_resolve_to_existing_files():
    for entry in _load_index():
        ref = entry["ratification_decision"]
        assert ref.startswith("decisions/")
        assert (REPO_ROOT / ref).is_file(), f"{entry['id']}: {ref!r} does not exist"


def test_ratification_decisions_are_all_accepted():
    for entry in _load_index():
        text = (REPO_ROOT / entry["ratification_decision"]).read_text(encoding="utf-8")
        assert "Status: Accepted" in text, f"{entry['id']}: decision not Accepted"


# -- constitution.md checks (no Pending section: all four are RATIFIED, mirrors data-ontology) --

def _constitution_text() -> str:
    return CONSTITUTION_PATH.read_text(encoding="utf-8")


def test_constitution_exists_and_is_nonempty():
    assert CONSTITUTION_PATH.is_file()
    assert len(_constitution_text()) > 3000


def test_constitution_has_no_pending_section():
    """All four Operations standards are RATIFIED -- there is no
    'Pending' section of unratified rules the way the UI constitution
    has one, mirroring docs/data-ontology/constitution.md's design."""
    text = _constitution_text()
    assert "## Pending" not in text


def test_constitution_covers_every_ratified_id_at_least_once():
    text = _constitution_text()
    body = text.split("## Not a standard")[0]
    referenced = set(STD_ID_RE.findall(body))
    missing = _ratified_ids() - referenced
    assert not missing, f"ratified ids missing from the constitution's normative body: {missing}"


def test_constitution_normative_body_cites_only_ratified_ids():
    text = _constitution_text()
    body = text.split("## Not a standard")[0]
    referenced = set(STD_ID_RE.findall(body))
    assert referenced, "constitution's normative body cites no STD-OPS-* id at all"
    assert referenced == _ratified_ids(), f"unexpected ids in normative body: {referenced - _ratified_ids()}"


def test_constitution_places_held_deferred_rehomed_only_in_not_a_standard_section():
    text = _constitution_text()
    marker = "## Not a standard"
    assert marker in text, "constitution.md must have an explicit non-normative section for held/deferred/rehomed candidates"
    body, _, held_section = text.partition(marker)
    for name in HELD_DEFERRED_REHOMED_MARKERS:
        assert name not in body, f"{name!r} appears in the constitution's normative body, not just the held section"
        assert name in held_section, f"{name!r} missing from the held/deferred/rehomed section"


def test_constitution_states_fleet_law_relationship_for_each_standard():
    """This domain's defining difference from UI/Data-Ontology: several
    standards are narrow complements to ACTIVE (not just proposed) Fleet
    Laws. The constitution must say so explicitly, per standard."""
    text = _constitution_text()
    section = text.split("## Relationship to `clank-architecture`")[1].split("## Not a standard")[0]
    for sid in ("STD-OPS-COM-001", "STD-OPS-COM-002", "STD-OPS-COM-003", "STD-OPS-COM-004"):
        assert sid in section, f"{sid} missing from the clank-architecture relationship section"
    for law in ("Fleet Law 3", "Fleet Law 5", "Fleet Law 7", "Fleet Law 8"):
        assert law in section, f"{law} missing from the clank-architecture relationship section"
    assert "does not claim" in text.lower() or "not read any of the above as" in text.lower()


def test_constitution_status_section_states_frozen():
    text = _constitution_text()
    assert "FROZEN as `operations-standards-v1.0`" in text
    assert "NO ESSENTIAL OPERATIONS CONTRACT MISSING" in text


# -- principle count sanity --

def test_constitution_principle_count_is_reasonable():
    text = _constitution_text()
    body = text.split("## Not a standard")[0]
    principle_markers = re.findall(r"^\*\*[A-Z]\d+\.\*\*", body, flags=re.MULTILINE)
    assert 10 <= len(principle_markers) <= 20, f"expected ~10-20 principles for 4 standards, found {len(principle_markers)}"


# -- no known-evidence-index exists yet (same reasoning as Data/Ontology) --

def test_no_known_evidence_index_exists_yet():
    assert not (STANDARDS_OPERATIONS_DIR / "known-evidence-index.json").exists()
    assert "no Operations conformance audit has been performed" in Path(
        REPO_ROOT / "tools" / "operations_agent_layer.py"
    ).read_text(encoding="utf-8")


# -- this housekeeping pass must not have changed any normative standard text or the frozen tag --

def test_no_standard_status_or_version_changed():
    for sid in ("STD-OPS-COM-001", "STD-OPS-COM-002", "STD-OPS-COM-003", "STD-OPS-COM-004"):
        obj = json.loads((STANDARDS_OPERATIONS_DIR / f"{sid}.json").read_text(encoding="utf-8"))
        assert obj["status"] == "RATIFIED"
        assert obj["version"] == 1


def test_frozen_tag_still_resolves_to_its_original_commit():
    import subprocess

    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "rev-parse", "operations-standards-v1.0^{commit}"],
        capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL, check=True,
    )
    assert result.stdout.strip() == "7100f294a83c30594f2ff9e953f7c9f77a95747f"
