"""Tests for the agent-facing UI layer: standards/ui/ratified-index.json,
standards/ui/agent-checklist.json, and docs/ui/constitution.md, checked
against the authoritative standards/ui/*.json files — not against each
other, so a stale generated file or a stale doc can't hide behind
agreement with another stale artefact.
"""

import json
import re
from pathlib import Path

import pytest

from tools.ui_agent_layer import (
    REPO_ROOT,
    STANDARDS_UI_DIR,
    build_agent_checklist,
    build_ratified_index,
    load_ratified_ui_standards,
    load_ui_standards,
)

CONSTITUTION_PATH = REPO_ROOT / "docs" / "ui" / "constitution.md"
STD_ID_RE = re.compile(r"STD-UI-[A-Z0-9]+-\d{3}")


def _load_index():
    return json.loads((STANDARDS_UI_DIR / "ratified-index.json").read_text())


def _load_checklist():
    return json.loads((STANDARDS_UI_DIR / "agent-checklist.json").read_text())


def _ratified_ids():
    return {s["id"] for s in load_ratified_ui_standards()}


def _proposed_ids():
    return {s["id"] for s in load_ui_standards() if s["status"] == "PROPOSED"}


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
    assert len(index_ids) == len(set(index_ids)), f"duplicate ids in ratified-index.json: {index_ids}"


def test_no_proposed_rule_appears_in_ratified_index():
    index_ids = {entry["id"] for entry in _load_index()}
    assert index_ids.isdisjoint(_proposed_ids())


def test_index_entries_have_required_fields():
    required = {
        "id", "title", "level", "applies_to", "version",
        "requirement_summary", "source_file", "ratification_decision",
    }
    for entry in _load_index():
        assert required <= entry.keys(), f"{entry['id']} missing fields: {required - entry.keys()}"
        assert entry["level"] == "MUST", f"{entry['id']}: expected MUST for a ratified standard"


# -- agent-checklist.json coverage --

def test_every_checklist_item_references_an_existing_ratified_rule():
    ratified_ids = _ratified_ids()
    for item in _load_checklist():
        assert item["standard"] in ratified_ids, f"checklist references non-ratified id {item['standard']!r}"


def test_no_proposed_rule_appears_in_checklist():
    checklist_ids = {item["standard"] for item in _load_checklist()}
    assert checklist_ids.isdisjoint(_proposed_ids())


def test_checklist_covers_every_ratified_rule_exactly_once():
    checklist_ids = [item["standard"] for item in _load_checklist()]
    assert set(checklist_ids) == _ratified_ids()
    assert len(checklist_ids) == len(set(checklist_ids)), f"duplicate ids in agent-checklist.json: {checklist_ids}"


def test_checklist_items_have_required_fields():
    for item in _load_checklist():
        assert item.get("question"), f"{item['standard']}: missing question"
        assert item.get("failure_means"), f"{item['standard']}: missing failure_means"


# -- ratification decision references resolve --

def test_all_ratification_decision_references_resolve_to_existing_files():
    for entry in _load_index():
        ref = entry["ratification_decision"]
        assert ref.startswith("decisions/"), f"{entry['id']}: unexpected ratification_decision format {ref!r}"
        path = REPO_ROOT / ref
        assert path.is_file(), f"{entry['id']}: ratification_decision {ref!r} does not exist"


# -- constitution.md checks --

def _constitution_text() -> str:
    return CONSTITUTION_PATH.read_text()


def _constitution_body_and_pending(text: str) -> tuple[str, str]:
    marker = "## Pending / Not Yet Normative"
    assert marker in text, "constitution.md is missing the Pending / Not Yet Normative section"
    body, _, pending = text.partition(marker)
    return body, pending


def test_constitution_exists_and_is_nonempty():
    assert CONSTITUTION_PATH.is_file()
    assert len(_constitution_text()) > 500


def test_constitution_references_no_nonexistent_rule_ids():
    """An id may be named specifically to say it doesn't exist (e.g.
    'STD-UI-SKU-002 does not exist') — that's a deliberate, useful
    statement, not a broken reference. Any other mention of an id not
    backed by a real standard file is a real error."""
    all_ids = {s["id"] for s in load_ui_standards()}
    unknown = set()
    for line in _constitution_text().splitlines():
        if "does not exist" in line:
            continue
        unknown |= set(STD_ID_RE.findall(line)) - all_ids
    assert not unknown, f"constitution.md references nonexistent rule ids: {unknown}"


def test_constitution_normative_body_cites_only_ratified_ids():
    """Every STD-UI-* id appearing before the Pending section must be a
    RATIFIED id — a PROPOSED id must never be cited as if it were
    normative authority in the constitution's main body."""
    body, _ = _constitution_body_and_pending(_constitution_text())
    ratified_ids = _ratified_ids()
    referenced_in_body = set(STD_ID_RE.findall(body))
    non_ratified = referenced_in_body - ratified_ids
    assert not non_ratified, f"non-ratified ids cited in the constitution's normative body: {non_ratified}"


def test_constitution_pending_section_lists_exactly_the_proposed_ids():
    """An id explicitly flagged as nonexistent ('does not exist') is not
    a pending item and is excluded from this comparison."""
    _, pending = _constitution_body_and_pending(_constitution_text())
    referenced_in_pending = set()
    for line in pending.splitlines():
        if "does not exist" in line:
            continue
        referenced_in_pending |= set(STD_ID_RE.findall(line))
    assert referenced_in_pending == _proposed_ids(), (
        f"Pending section lists {referenced_in_pending}, but PROPOSED ids are {_proposed_ids()}"
    )


PRINCIPLE_MARKER_RE = re.compile(r"^\*\*[A-Z]\d+\.\*\*")


def test_constitution_does_not_label_pending_ids_as_numbered_principles():
    """A PROPOSED id must never be given one of the constitution's own
    numbered-principle markers (the '**A1.**' style used throughout
    sections A-J for ratified requirements) — that format is reserved for
    ratified, normative statements. Quoting a pending rule's own title
    (which may itself contain the word 'must', since that's the rule's
    working title) is fine and expected; what's forbidden is this
    document asserting it as one of its own live principles."""
    body, pending = _constitution_body_and_pending(_constitution_text())
    proposed = _proposed_ids()
    for line in body.splitlines() + pending.splitlines():
        ids_on_line = set(STD_ID_RE.findall(line))
        if ids_on_line & proposed:
            assert not PRINCIPLE_MARKER_RE.match(line.strip()), (
                f"a PROPOSED id is attached to a numbered-principle marker: {line!r}"
            )


def test_constitution_covers_every_ratified_id_at_least_once():
    body, _ = _constitution_body_and_pending(_constitution_text())
    referenced_in_body = set(STD_ID_RE.findall(body))
    missing = _ratified_ids() - referenced_in_body
    assert not missing, f"ratified ids missing from the constitution's normative body: {missing}"


# -- principle count sanity (approximately 20-30 per the task) --

def test_constitution_principle_count_is_in_range():
    body, _ = _constitution_body_and_pending(_constitution_text())
    principle_markers = re.findall(r"^\*\*[A-Z]\d+\.\*\*", body, flags=re.MULTILINE)
    assert 20 <= len(principle_markers) <= 32, f"expected ~20-30 principles, found {len(principle_markers)}"


# -- workflow doc exists and mentions the required sequence/report fields --

def test_agent_workflow_doc_exists_and_has_required_report_fields():
    path = REPO_ROOT / "docs" / "ui" / "agent-implementation-workflow.md"
    assert path.is_file()
    text = path.read_text()
    required_fields = [
        "Clank family",
        "Applicable RATIFIED standards",
        "Current conformances",
        "Current violations",
        "Standards that are N/A",
        "Specialist surfaces to preserve",
        "Files expected to change",
        "Proposed exceptions",
        "Unresolved semantic questions",
    ]
    for field in required_fields:
        assert field in text, f"agent-implementation-workflow.md missing required report field: {field!r}"
    assert "Never self-approve exceptions" in text
