"""Tests for the agent-facing Deployment layer:
standards/deployment/ratified-index.json, standards/deployment/agent-checklist.json,
and docs/deployment/constitution.md, checked against the authoritative
standards/deployment/*.json files — not against each other, so a stale
generated file or a stale doc can't hide behind agreement with another
stale artefact. Mirrors tests/test_operations_agent_layer.py's design,
including the known-evidence-index checks generated from active Deployment
audit blocks.

Building this layer is mechanical housekeeping commissioned alongside the
operator's ratification closure: no normative standard text changed as
part of it, and no deployment freeze tag exists yet.
"""

import json
import re
from pathlib import Path

from tools.deployment_agent_layer import (
    REPO_ROOT,
    STANDARDS_DEPLOYMENT_DIR,
    build_agent_checklist,
    build_known_evidence_index,
    build_ratified_index,
    load_deployment_standards,
    load_ratified_deployment_standards,
)

CONSTITUTION_PATH = REPO_ROOT / "docs" / "deployment" / "constitution.md"
STD_ID_RE = re.compile(r"STD-DEPLOY-[A-Z0-9]+-\d{3}")

MERGED_REHOMED_REJECTED_MARKERS = [
    "Running revision identity (cluster 02)",
    "Partial deployment wiring (cluster 04)",
    "Target environment identity (cluster 06)",
    "Destructive state mutation / rollback & recovery (cluster 05)",
]


def _load_index():
    return json.loads((STANDARDS_DEPLOYMENT_DIR / "ratified-index.json").read_text(encoding="utf-8"))


def _load_checklist():
    return json.loads((STANDARDS_DEPLOYMENT_DIR / "agent-checklist.json").read_text(encoding="utf-8"))


def _load_known_evidence():
    return json.loads((STANDARDS_DEPLOYMENT_DIR / "known-evidence-index.json").read_text(encoding="utf-8"))


def _ratified_ids():
    return {s["id"] for s in load_ratified_deployment_standards()}


def _proposed_ids():
    return {s["id"] for s in load_deployment_standards() if s["status"] == "PROPOSED"}


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
    assert len(index_ids) == 2
    assert len(index_ids) == len(set(index_ids))


def test_no_proposed_rule_appears_in_ratified_index():
    index_ids = {entry["id"] for entry in _load_index()}
    assert index_ids.isdisjoint(_proposed_ids())
    assert _proposed_ids() == set(), "Deployment closed at 2/0 -- no PROPOSED standard should exist"


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
    assert len(checklist_ids) == 2
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


# -- constitution.md checks (no Pending section: both are RATIFIED) --

def _constitution_text() -> str:
    return CONSTITUTION_PATH.read_text(encoding="utf-8")


def test_constitution_exists_and_is_nonempty():
    assert CONSTITUTION_PATH.is_file()
    assert len(_constitution_text()) > 3000


def test_constitution_has_no_pending_section():
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
    assert referenced, "constitution's normative body cites no STD-DEPLOY-* id at all"
    assert referenced == _ratified_ids(), f"unexpected ids in normative body: {referenced - _ratified_ids()}"


def test_constitution_places_merged_rehomed_rejected_only_in_not_a_standard_section():
    text = _constitution_text()
    marker = "## Not a standard"
    assert marker in text, "constitution.md must have an explicit non-normative section for merged/rehomed/rejected candidates"
    body, _, held_section = text.partition(marker)
    for name in MERGED_REHOMED_REJECTED_MARKERS:
        assert name not in body, f"{name!r} appears in the constitution's normative body, not just the held section"
        assert name in held_section, f"{name!r} missing from the merged/rehomed/rejected section"


def test_constitution_states_fleet_law_relationship_for_each_standard():
    text = _constitution_text()
    section = text.split("## Relationship to `clank-architecture`")[1].split("## Not a standard")[0]
    for sid in ("STD-DEPLOY-COM-001", "STD-DEPLOY-COM-002"):
        assert sid in section, f"{sid} missing from the clank-architecture relationship section"
    for governance in ("Fleet Law 5", "Fleet Law 6", "Law 9", "ADR-0009"):
        assert governance in section, f"{governance} missing from the clank-architecture relationship section"
    assert "PROPOSED — REVIEWED DRAFT" in section, "ADR-0009 status must be stated as not ACTIVE"


# -- principle count sanity --

def test_constitution_principle_count_is_reasonable():
    text = _constitution_text()
    body = text.split("## Not a standard")[0]
    principle_markers = re.findall(r"^\*\*[A-Z]\d+\.\*\*", body, flags=re.MULTILINE)
    assert 5 <= len(principle_markers) <= 12, f"expected ~5-12 principles for 2 standards, found {len(principle_markers)}"


# -- Deployment known-evidence admission is generated from active audit blocks --

def test_known_evidence_index_matches_generator_output():
    assert _load_known_evidence() == build_known_evidence_index()


def test_known_evidence_admits_only_confirmed_deployment_conformance():
    entries = _load_known_evidence()
    assert len(entries) == 10
    by_subject = {entry["subject"]: entry for entry in entries}
    assert set(by_subject) == {"watch-clank", "semiconductor-intelligence", "korean-tech-wire", "tablet-clank", "feature-phone-clank", "oem-radar", "chinese-tech-wire", "smartwatch-clank"}

    watch = by_subject["watch-clank"]
    assert watch["standard"] == "STD-DEPLOY-COM-001"
    assert watch["kind"] == "known_conformance"
    assert watch["source"] == "audit"
    assert watch["source_reference"] == "audits/watch-clank-cross-domain-2026-09-01-final.md"
    assert "LIVE_PROOF_CONFIRMED" in watch["summary"]
    assert "d03bc4b2f90289686331af0447d5ca4e8cf55822" in watch["summary"]

    semiconductor = by_subject["semiconductor-intelligence"]
    assert semiconductor["standard"] == "STD-DEPLOY-COM-002"
    assert semiconductor["kind"] == "known_conformance"
    assert semiconductor["source"] == "audit"
    assert semiconductor["source_reference"] == "audits/semiconductor-persistent-state-remediation-m11-2026-09-01.md"
    assert "CONFORMS / CLOSED" in semiconductor["summary"]
    assert "8085a1bbd1a4e133680702e8c1d916b71bb78a14" in semiconductor["summary"]

    ktw = by_subject["korean-tech-wire"]
    assert ktw["standard"] == "STD-DEPLOY-COM-002"
    assert ktw["kind"] == "known_conformance"
    assert ktw["source"] == "audit"
    assert ktw["source_reference"] == "audits/ktw-persistent-state-remediation-m12-2026-09-02.md"
    assert "CONFORMS / CLOSED" in ktw["summary"]
    assert "354cb7aed0b174923393a0c71e7c4c6230cda28c" in ktw["summary"]

    tablet = by_subject["tablet-clank"]
    assert tablet["standard"] == "STD-DEPLOY-COM-002"
    assert tablet["kind"] == "known_conformance"
    assert tablet["source_reference"] == "audits/tablet-persistent-state-remediation-m13-2026-09-02.md"
    assert "b3088ebc716227b99e1d8aa66942c8a6e87bbfcb" in tablet["summary"]

    feature_phone = by_subject["feature-phone-clank"]
    assert feature_phone["standard"] == "STD-DEPLOY-COM-002"
    assert feature_phone["kind"] == "known_conformance"
    assert feature_phone["source_reference"] == "audits/feature-phone-persistent-state-remediation-m14-2026-09-02.md"
    assert "CONFORMS / CLOSED" in feature_phone["summary"]
    assert "b60e881319b16d36625268d9ba2d66cb8ea8f818" in feature_phone["summary"]

    oem_radar = by_subject["oem-radar"]
    assert oem_radar["standard"] == "STD-DEPLOY-COM-002"
    assert oem_radar["kind"] == "known_conformance"
    assert oem_radar["source_reference"] == "audits/oem-radar-persistent-state-remediation-m15-2026-09-02.md"
    assert "CONFORMS / CLOSED" in oem_radar["summary"]
    assert "79fbee63ee3a43badad085671ba5bf6837b627f7" in oem_radar["summary"]

    ctw = by_subject["chinese-tech-wire"]
    assert ctw["standard"] == "STD-DEPLOY-COM-002"
    assert ctw["kind"] == "known_conformance"
    assert ctw["source_reference"] == "audits/ctw-persistent-state-remediation-m17-2026-09-02.md"
    assert "CONFORMS / CLOSED" in ctw["summary"]
    assert "c340a45ac8cfbab58d749dcbf78a7d703ca9cdb1" in ctw["summary"]

    smartwatch = by_subject["smartwatch-clank"]
    assert smartwatch["standard"] == "STD-DEPLOY-COM-002"
    assert smartwatch["kind"] == "known_conformance"
    assert smartwatch["source_reference"] == "audits/smartwatch-persistent-state-remediation-m18-2026-09-02.md"
    assert "CONFORMS / CLOSED" in smartwatch["summary"]
    assert "a93355480bb11e1bd16ae7837256ce9002fc2aa7" in smartwatch["summary"]

    # Smartwatch joins COM-001 at M22 as its second Deployment fact; the
    # by_subject dict above keeps the (later-sorted) M18 COM-002 entry, so
    # the COM-001 fact is checked directly from the list.
    sw_com001 = [e for e in entries
                 if e["subject"] == "smartwatch-clank" and e["standard"] == "STD-DEPLOY-COM-001"]
    assert len(sw_com001) == 1
    assert sw_com001[0]["source_reference"] == "audits/smartwatch-deployment-proof-m22-2026-09-02.md"
    assert "LIVE_PROOF_CONFIRMED" in sw_com001[0]["summary"]
    assert "hetzner/ubuntu-4gb-hel1-1:cron-docker-compose-staging" in sw_com001[0]["summary"]

    # Feature Phone joins COM-001 at M25 as its second Deployment fact; the
    # by_subject dict above keeps the (later-sorted) M14 COM-002 entry, so
    # the COM-001 fact is checked directly from the list.
    fp_com001 = [e for e in entries
                 if e["subject"] == "feature-phone-clank" and e["standard"] == "STD-DEPLOY-COM-001"]
    assert len(fp_com001) == 1
    assert fp_com001[0]["source_reference"] == "audits/feature-phone-deployment-proof-m25-2026-09-02.md"
    assert "LIVE_PROOF_CONFIRMED" in fp_com001[0]["summary"]
    assert "hetzner/ubuntu-4gb-hel1-1:cron-docker-compose-staging" in fp_com001[0]["summary"]


# -- this housekeeping pass must not have changed any normative standard text, and no freeze tag exists yet --

def test_no_standard_version_changed():
    for sid in ("STD-DEPLOY-COM-001", "STD-DEPLOY-COM-002"):
        obj = json.loads((STANDARDS_DEPLOYMENT_DIR / f"{sid}.json").read_text(encoding="utf-8"))
        assert obj["status"] == "RATIFIED"
        assert obj["version"] == 1


def test_deployment_freeze_tag_is_verified_by_the_baseline_guard_after_freeze():
    """The agent-layer task predated the authorized V1 freeze. The dedicated
    baseline guard owns tag verification, allowing the required pre-tag suite
    to remain green while still checking the pushed tag afterwards."""
    import subprocess

    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "tag", "-l", "deployment-standards*"],
        capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL, check=True,
    )
    assert result.stdout.strip() in {"", "deployment-standards-v1.0"}
