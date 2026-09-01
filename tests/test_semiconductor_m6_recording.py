"""Narrow guards for the Semiconductor M6 Operations evidence record."""

import json
import subprocess
from pathlib import Path

from tools.operations_agent_layer import build_known_evidence_index


ROOT = Path(__file__).resolve().parents[1]
AUDIT_MD = ROOT / "audits" / "semiconductor-qualification-remediation-m6-2026-09-01.md"
AUDIT_JSON = ROOT / "audits" / "semiconductor-qualification-remediation-m6-2026-09-01.json"
KNOWN = ROOT / "standards" / "operations" / "known-evidence-index.json"
SEMICONDUCTOR_SHA = "688b71a93b4988b5ce52ce85e46f09080b9a7948"
SMARTWATCH_SHA = "a631421e276b58ce3499787cc2bc72218648ce72"
STANDARDS_SHA = "3f729b9ff169105487cd875bd8ed9a0722b22f6e"


def _record():
    return json.loads(AUDIT_JSON.read_text(encoding="utf-8"))


def test_m6_record_has_exact_target_and_narrow_closed_verdict():
    record = _record()
    assert record["standards_clank_head"] == STANDARDS_SHA
    assert record["semiconductor"]["head"] == SEMICONDUCTOR_SHA
    assert record["semiconductor"]["origin_main"] == SEMICONDUCTOR_SHA
    assert record["semiconductor"]["standard"] == "STD-OPS-COM-003"
    assert record["semiconductor"]["state"] == "CONFORMS"
    assert record["semiconductor"]["lifecycle"] == "CLOSED"
    assert record["semiconductor"]["scope"] == "source-level qualification provenance/reset remediation only"


def test_m6_preserves_original_six_and_leaves_five_insufficient():
    record = _record()
    lineage = record["source_lineage"]
    assert lineage["m1_original_state"] == "INSUFFICIENT_EVIDENCE"
    assert lineage["m1_applicable"] == 23
    assert lineage["m1_conforms"] == 17
    assert lineage["m1_non_conforming"] == 0
    assert lineage["m1_insufficient_evidence"] == 6
    assert lineage["m1_insufficient_standards"] == [
        "STD-UI-COM-006", "STD-UI-COM-007", "STD-UI-COM-011",
        "STD-OPS-COM-003", "STD-DEPLOY-COM-001", "STD-DEPLOY-COM-002",
    ]
    assert record["remaining_m1_insufficiencies"] == {
        "STD-UI-COM-006": "INSUFFICIENT_EVIDENCE",
        "STD-UI-COM-007": "INSUFFICIENT_EVIDENCE",
        "STD-UI-COM-011": "INSUFFICIENT_EVIDENCE",
        "STD-DEPLOY-COM-001": "INSUFFICIENT_EVIDENCE",
        "STD-DEPLOY-COM-002": "INSUFFICIENT_EVIDENCE",
    }
    assert record["known_evidence_admission"]["prior_m1_preserved"] is True


def test_m6_validation_records_full_suite_and_attribution_honestly():
    record = _record()
    validation = record["validation"]
    assert validation["focused_qualification"] == {"passed": 21}
    assert validation["baseline"] == {
        "revision": "8a356a3bc87bea0f0d95e66c072c8e8a629156d5",
        "passed": 877,
        "skipped": 1,
        "failed": 2,
        "exit_code": 1,
        "failures": "notification-adapter assertions",
    }
    assert validation["final"] == {
        "revision": SEMICONDUCTOR_SHA,
        "passed": 898,
        "skipped": 1,
        "failed": 2,
        "warnings": 38541,
        "elapsed_seconds": 1244.62,
        "exit_code": 1,
        "failures": "notification-adapter assertions",
    }
    attribution = validation["baseline_attribution"]
    assert attribution["classification"] == "PRE_EXISTING / BASELINE_ATTRIBUTED"
    assert attribution["same_failures_at_baseline_and_remediation"] is True
    assert attribution["new_qualification_failures"] is False
    assert attribution["new_migration_failures"] is False
    assert attribution["new_failures_introduced_by_m6"] is False
    assert attribution["focused_coverage_green"] is True
    assert attribution["full_suite_claim"] == "not green"


def test_m6_family_validation_is_limited_to_two_rich_orm_job_targets():
    family = _record()["family_status"]
    assert family["conclusion"] == "RICH_ORM_JOB_RECIPE_VALIDATED"
    assert family["descriptive_only"] is True
    assert family["members"] == {
        "smartwatch-clank": SMARTWATCH_SHA,
        "semiconductor-intelligence": SEMICONDUCTOR_SHA,
    }
    assert family["evidence_inheritance"] is False
    assert family["other_target_conformance_inferred"] is False


def test_m6_known_evidence_admission_is_exact_and_generated():
    entries = json.loads(KNOWN.read_text(encoding="utf-8"))
    assert entries == build_known_evidence_index()
    semiconductor = [entry for entry in entries if entry["subject"] == "semiconductor-intelligence"]
    assert len(semiconductor) == 1
    entry = semiconductor[0]
    assert entry["standard"] == "STD-OPS-COM-003"
    assert entry["kind"] == "known_conformance"
    assert entry["source"] == "audit"
    assert entry["source_reference"] == "audits/semiconductor-qualification-remediation-m6-2026-09-01.md"
    assert SEMICONDUCTOR_SHA in entry["summary"]
    assert "CONFORMS / CLOSED" in entry["summary"]
    assert {item["standard"] for item in entries if item["subject"] == "semiconductor-intelligence"} == {
        "STD-OPS-COM-003",
    }
    assert all(item["subject"] != "oem-radar" for item in entries)


def test_m6_audit_prose_declares_scope_and_non_green_suite():
    text = AUDIT_MD.read_text(encoding="utf-8")
    for marker in (
        "CONFORMS / CLOSED",
        SEMICONDUCTOR_SHA,
        "STD-UI-COM-006",
        "STD-UI-COM-007",
        "STD-UI-COM-011",
        "STD-DEPLOY-COM-001",
        "STD-DEPLOY-COM-002",
        "PRE_EXISTING / BASELINE_ATTRIBUTED",
        "RICH_ORM_JOB_RECIPE_VALIDATED",
        "The full suite is not green",
        "No host, deployment, live collector, live proof, or production-database action occurred",
    ):
        assert marker in text


def test_m6_frozen_standard_files_and_tags_remain_unchanged():
    standard_files = sorted((ROOT / "standards" / "operations").glob("STD-OPS-*.json"))
    for path in standard_files:
        tagged = subprocess.run(
            ["git", "show", f"operations-standards-v1.0:{path.relative_to(ROOT).as_posix()}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            stdin=subprocess.DEVNULL,
            check=True,
        ).stdout
        assert path.read_text(encoding="utf-8") == tagged

    expected_tags = {
        "ui-standards-v1.0": "d11320704aed69a3d8f854c9264b184e392ec80f",
        "data-ontology-standards-v1.0": "464a8057ea5dc26ef83248a20bafa0be5aa31148",
        "operations-standards-v1.0": "7100f294a83c30594f2ff9e953f7c9f77a95747f",
        "deployment-standards-v1.0": "33cc38849180716fd4d06b1356cf70c49d3d41d2",
    }
    for tag, expected in expected_tags.items():
        actual = subprocess.run(
            ["git", "rev-parse", f"{tag}^{{commit}}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            stdin=subprocess.DEVNULL,
            check=True,
        ).stdout.strip()
        assert actual == expected
