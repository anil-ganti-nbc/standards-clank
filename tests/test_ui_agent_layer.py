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
    build_known_evidence_index,
    build_ratified_index,
    load_audit_findings,
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


def test_index_entries_have_no_extra_fields():
    """Guards specifically against known-evidence-index.json content (or
    anything else) ever getting merged into the normative ratified-index —
    a blind audit's promise depends on this file staying free of per-Clank
    history. See docs/ui/agent-implementation-workflow.md's 'Two modes'
    section."""
    required = {
        "id", "title", "level", "applies_to", "version",
        "requirement_summary", "source_file", "ratification_decision",
    }
    for entry in _load_index():
        assert entry.keys() == required, f"{entry['id']}: unexpected extra fields {entry.keys() - required}"


def test_checklist_entries_have_no_extra_fields():
    required = {"standard", "question", "failure_means"}
    for item in _load_checklist():
        assert item.keys() == required, f"{item['standard']}: unexpected extra fields {item.keys() - required}"


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

# -- known-evidence-index.json: mechanically generated from audits/*.md, structurally separate --

def _load_known_evidence():
    return json.loads((STANDARDS_UI_DIR / "known-evidence-index.json").read_text())


def test_known_evidence_index_matches_generator_output():
    assert _load_known_evidence() == build_known_evidence_index()


def test_known_evidence_entries_reference_ratified_standards():
    ratified_ids = _ratified_ids()
    for entry in _load_known_evidence():
        assert entry["standard"] in ratified_ids, (
            f"known-evidence-index.json cites non-ratified id {entry['standard']!r}"
        )


def test_known_evidence_entries_reference_existing_audit_files():
    for entry in _load_known_evidence():
        path = REPO_ROOT / entry["source_reference"]
        assert path.is_file(), f"known-evidence-index.json entry points at missing file {entry['source_reference']!r}"


def test_known_evidence_index_exactly_matches_active_violation_findings():
    """Mechanical wiring invariant that holds in ANY state: the index is
    exactly the set of kind:violation findings from active (non-superseded)
    audits — nothing more, nothing less. A fully-remediated fleet therefore
    legitimately yields an empty index (all known findings verified fixed);
    the committed-file-vs-generator drift test still proves the pipeline
    itself is wired."""
    audit_files = {p.name for p in (REPO_ROOT / "audits").glob("*.md") if p.name != "README.md"}
    superseded_files = {
        p.name for p, block in load_audit_findings() if block.get("superseded_by")
    }
    expected = []
    for path, block in load_audit_findings():
        if block.get("superseded_by"):
            continue
        for finding in block["findings"]:
            if finding.get("kind") == "violation":
                expected.append((finding["standard"], block["clank"], path.name))

    actual = [
        (entry["standard"], entry["subject"], entry["source_reference"].split("/", 1)[1])
        for entry in _load_known_evidence()
    ]
    assert sorted(actual) == sorted(expected)
    referenced_files = {name for _, _, name in actual}
    assert referenced_files <= (audit_files - superseded_files)


def test_superseded_audit_is_excluded_from_known_evidence_index():
    """The pass-1 smartphone audit still contains COM-003/004 'violation'
    findings in its (preserved) structured block, but it was superseded by
    the second blind validation, whose refined assessment classifies them
    N/A. The stale violations must never reach the index."""
    pass1 = REPO_ROOT / "audits" / "smartphone-clank-2026-08-30-pass1.md"
    assert pass1.is_file(), "superseded pass-1 audit must be preserved, not deleted"
    pass1_block = dict(load_audit_findings())[pass1]
    assert pass1_block.get("superseded_by") == "audits/smartphone-clank-2026-08-30.md"
    kinds = {f["standard"]: f["kind"] for f in pass1_block["findings"]}
    assert kinds["STD-UI-COM-003"] == "violation", "precondition: pass-1 block still holds the stale classification"
    referenced = {entry["source_reference"] for entry in _load_known_evidence()}
    assert "audits/smartphone-clank-2026-08-30-pass1.md" not in referenced


def test_superseded_by_references_resolve_to_active_audits():
    for path, block in load_audit_findings():
        ref = block.get("superseded_by")
        if not ref:
            continue
        target = REPO_ROOT / ref
        assert target.is_file(), f"{path.name}: superseded_by target {ref!r} missing"
        assert f"audits/{path.name}" != ref, f"{path.name}: superseded_by points at itself"


def test_known_evidence_index_generation_is_deterministic():
    assert build_known_evidence_index() == build_known_evidence_index()


# -- smartphone-clank second validation (current assessment) --

def _smartphone_audit_kinds() -> dict[str, str]:
    path = REPO_ROOT / "audits" / "smartphone-clank-2026-08-30.md"
    block = dict(load_audit_findings())[path]
    assert not block.get("superseded_by")
    return {f["standard"]: f["kind"] for f in block["findings"]}


def test_smartphone_audit_classifies_com003_com004_as_not_applicable():
    kinds = _smartphone_audit_kinds()
    assert kinds["STD-UI-COM-003"] == "not_applicable"
    assert kinds["STD-UI-COM-004"] == "not_applicable"


def test_smartphone_violations_are_remediated_and_verified():
    """The smartphone-clank remediation (5684cf2) was independently
    verified 2026-08-31: COM-002/009/010 are remediated with the original
    findings preserved in the summaries, and the audit records
    REMEDIATION_VERIFIED."""
    kinds = _smartphone_audit_kinds()
    for sid in ("STD-UI-COM-002", "STD-UI-COM-009", "STD-UI-COM-010"):
        assert kinds[sid] == "conformance", sid
    summaries = {
        f["standard"]: f["summary"]
        for f in dict(load_audit_findings())[
            REPO_ROOT / "audits" / "smartphone-clank-2026-08-30.md"
        ]["findings"]
    }
    for sid in ("STD-UI-COM-002", "STD-UI-COM-009", "STD-UI-COM-010"):
        assert summaries[sid].startswith("REMEDIATED"), sid
        assert "5684cf2" in summaries[sid], sid
    audit_text = (REPO_ROOT / "audits" / "smartphone-clank-2026-08-30.md").read_text()
    assert "REMEDIATION_VERIFIED" in audit_text
    assert "Product/remediation backlog (non-normative)" in audit_text


def test_smartphone_com009_remediation_preserves_interpretation_history():
    """COM-009's path: interpretation accepted (decisions/0006) -> FAIL ->
    remediated (smartphone-clank 5684cf2) -> REMEDIATION_VERIFIED. The
    audit must keep the full verdict history visible, and the accepted
    interpretation decision must stay on record."""
    proposal = (REPO_ROOT / "decisions" / "0006-com009-equivalent-structured-record.md").read_text()
    assert "Status: Accepted" in proposal
    audit_text = (REPO_ROOT / "audits" / "smartphone-clank-2026-08-30.md").read_text()
    assert "PARTIAL" in audit_text and "FAIL" in audit_text, (
        "audit must preserve the prior PARTIAL/unresolved and FAIL verdict states in its history"
    )
    assert "REMEDIATION_VERIFIED" in audit_text
    kinds = _smartphone_audit_kinds()
    assert kinds["STD-UI-COM-009"] == "conformance"


def test_smartphone_audit_structured_block_covers_every_then_ratified_standard():
    """The smartphone audit was written when 12 standards were RATIFIED
    (COM-007/012/SKU-001 were ratified later, in the Pass 3 resolution) —
    the block must cover exactly that 12."""
    expected = _ratified_ids() - {"STD-UI-COM-007", "STD-UI-COM-012", "STD-UI-SKU-001"}
    kinds = _smartphone_audit_kinds()
    assert set(kinds) == expected


def test_known_evidence_index_is_not_referenced_by_ratified_index_or_checklist():
    """The whole point of this file is that it stays out of the normative
    layer. Guard against a future edit accidentally wiring it in."""
    index_text = (STANDARDS_UI_DIR / "ratified-index.json").read_text()
    checklist_text = (STANDARDS_UI_DIR / "agent-checklist.json").read_text()
    assert "known-evidence" not in index_text
    assert "known-evidence" not in checklist_text
    assert "prior_evidence" not in index_text
    assert "prior_evidence" not in checklist_text


def test_agent_workflow_doc_documents_the_two_modes_and_reverification_rule():
    path = REPO_ROOT / "docs" / "ui" / "agent-implementation-workflow.md"
    text = path.read_text()
    assert "BLIND AUDIT" in text
    assert "INFORMED REMEDIATION" in text
    assert "hypotheses, not" in text
    assert "known-evidence-index.json" in text


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


# -- workflow audit methodology (decisions/0005 interpretation pass) --

WORKFLOW_PATH = REPO_ROOT / "docs" / "ui" / "agent-implementation-workflow.md"


def _workflow_text() -> str:
    return WORKFLOW_PATH.read_text()


def test_agent_workflow_requires_inventory_of_nongui_mutation_paths():
    """A GUI-first inventory missed smartphone-clank's CLI-only qc-action
    write path (second validation, 2026-08-30). The workflow must now
    require sweeping operator-relevant backend mutation paths even when
    the GUI does not expose them."""
    text = _workflow_text()
    assert "operator-relevant backend mutation paths" in text
    assert "CLI QC/operator commands" in text
    assert "native launcher actions" in text
    assert "append-only" in text and "operator action stores" in text
    assert "schema migrations" in text


def test_agent_workflow_states_applicability_is_semantic_not_label_based():
    text = _workflow_text()
    assert "semantics and behaviour, not labels" in text
    assert "query/filter semantics" in text
    assert "write paths" in text
    assert "entity lifecycle" in text
    assert "intended operator workflow" in text
    # The catalogue-vs-queue trap must be named.
    assert "catalogue" in text


def test_agent_workflow_distinguishes_action_contract_from_queue_surface_applicability():
    """Underlying action contracts (e.g. COM-002) apply wherever the
    operator action exists, GUI or not; queue-surface standards (COM-003/
    004) apply only where a real queue semantic exists. Both statements,
    and the boundary between them, must stay explicit."""
    text = _workflow_text()
    assert "Underlying action contracts" in text
    assert "does NOT automatically make them N/A" in text
    assert "Queue-surface standards" in text
    assert "No queue semantics" in text
    assert "broaden them beyond it" in text


def test_agent_workflow_requires_na_verdicts_to_cite_the_trigger_clause():
    text = _workflow_text()
    assert "trigger" in text
    assert "constitution section J2" in text


# -- the interpretation pass must not have moved ratification state --

def test_rule_counts_after_ratification_closure():
    """15 RATIFIED / 0 PROPOSED since the Pass 3 ratification closure
    (decisions/0007-0009, 2026-08-31)."""
    assert len(_ratified_ids()) == 15
    assert not _proposed_ids()


def test_com009_v3_encodes_the_accepted_applicability_boundary():
    """The v3 revision (operator acceptance of decisions/0006) must encode
    the boundary in the standard itself: per-run, phase-attributable
    structured outcomes qualify regardless of record shape; aggregate or
    windowed metrics alone do not trigger the rule. This is what stops a
    future agent from reading any aggregate metric as stage data — or
    from dismissing a flat per-run record as 'not a stage ledger'."""
    com009 = json.loads((STANDARDS_UI_DIR / "STD-UI-COM-009.json").read_text())
    assert com009["status"] == "RATIFIED"
    assert com009["version"] == 3
    # Traceability: original ratification decision first (feeds the
    # generated index), v3 revision decision also cited.
    notes = com009["notes"]
    assert notes.index("decisions/0004-") < notes.index("decisions/0006-")
    # Requirement: the trigger clause carries both sides of the boundary.
    requirement = com009["requirement"]
    assert "per-run, phase-attributable" in requirement
    assert "NOT required" in requirement  # ordered ledger sufficient, not required
    assert "aggregate or windowed counters alone do not" in requirement
    # Acceptance: an explicit boundary criterion exists.
    acceptance_text = " ".join(com009["acceptance"])
    assert "per-run, phase-attributable" in acceptance_text
    assert "aggregate or windowed metrics alone do not trigger it" in acceptance_text
    # Forbidden: treating aggregates as stage data is named as forbidden.
    forbidden_text = " ".join(com009["forbidden"])
    assert "aggregate or windowed health metrics alone" in forbidden_text


def test_com009_boundary_is_encoded_in_the_generated_agent_layer():
    """A constitution/checklist-only auditor must hit the same boundary:
    the generated summary and checklist question carry both sides (flat
    per-run records qualify; window aggregates alone do not)."""
    summary = next(e for e in _load_index() if e["id"] == "STD-UI-COM-009")["requirement_summary"]
    assert "per-run, phase-attributable" in summary
    assert "aggregate or windowed metrics alone do not trigger this" in summary
    checklist_item = next(i for i in _load_checklist() if i["standard"] == "STD-UI-COM-009")
    assert "not just window aggregates" in checklist_item["question"]
    assert "aggregate/window health metrics alone" in checklist_item["failure_means"]


def test_constitution_f1_carries_the_com009_boundary():
    body, _ = _constitution_body_and_pending(_constitution_text())
    f1_section = body.split("**F2.**")[0]
    assert "per-run, phase-attributable outcome fields" in f1_section
    assert "aggregate or windowed metrics alone do not trigger this" in f1_section


def test_qc_gui_absence_is_backlog_not_violation():
    """The operator ruled (2026-08-30, decisions/0006 review) that
    smartphone-clank's absent QC GUI is product/remediation backlog, and
    that COM-003/004 remain N/A. The evidence index must not carry any
    smartphone COM-003/004 entry, and the audit must state the backlog
    classification explicitly."""
    index_subjects = {
        (e["standard"], e["subject"]) for e in _load_known_evidence()
    }
    assert ("STD-UI-COM-003", "smartphone-clank") not in index_subjects
    assert ("STD-UI-COM-004", "smartphone-clank") not in index_subjects
    audit_text = (REPO_ROOT / "audits" / "smartphone-clank-2026-08-30.md").read_text()
    assert "Product/remediation backlog (non-normative)" in audit_text
    assert "remain N/A" in audit_text
