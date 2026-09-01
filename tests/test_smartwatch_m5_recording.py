"""Narrow guards for the Smartwatch M5 Operations evidence record."""

import json
import subprocess
from pathlib import Path

from tools.operations_agent_layer import build_known_evidence_index


ROOT = Path(__file__).resolve().parents[1]
AUDIT_MD = ROOT / "audits" / "smartwatch-clank-qualification-remediation-m5-2026-09-01.md"
AUDIT_JSON = ROOT / "audits" / "smartwatch-clank-qualification-remediation-m5-2026-09-01.json"
KNOWN = ROOT / "standards" / "operations" / "known-evidence-index.json"
SMARTWATCH_SHA = "a631421e276b58ce3499787cc2bc72218648ce72"
STANDARDS_SHA = "a56e8dc1ddce54e229096ec55bec90c1e2ec6e15"


def _record():
    return json.loads(AUDIT_JSON.read_text(encoding="utf-8"))


def test_m5_record_has_exact_target_and_narrow_closed_verdict():
    record = _record()
    assert record["standards_clank_head"] == STANDARDS_SHA
    assert record["smartwatch"]["head"] == SMARTWATCH_SHA
    assert record["smartwatch"]["origin_main"] == SMARTWATCH_SHA
    assert record["smartwatch"]["standard"] == "STD-OPS-COM-003"
    assert record["smartwatch"]["state"] == "CONFORMS"
    assert record["smartwatch"]["lifecycle"] == "CLOSED"
    assert record["smartwatch"]["scope"] == "source-level qualification provenance/reset remediation only"


def test_m5_preserves_three_m1_insufficiencies_and_history():
    record = _record()
    assert record["source_lineage"]["m1_original_state"] == "INSUFFICIENT_EVIDENCE"
    assert record["source_lineage"]["m1_insufficient_standards"] == [
        "STD-UI-COM-011",
        "STD-OPS-COM-003",
        "STD-DEPLOY-COM-001",
        "STD-DEPLOY-COM-002",
    ]
    assert record["remaining_m1_insufficiencies"] == {
        "STD-UI-COM-011": "INSUFFICIENT_EVIDENCE",
        "STD-DEPLOY-COM-001": "INSUFFICIENT_EVIDENCE",
        "STD-DEPLOY-COM-002": "INSUFFICIENT_EVIDENCE",
    }
    assert record["known_evidence_admission"]["historical_m1_preserved"] is True


def test_m5_validation_records_baseline_attribution_honestly():
    validation = _record()["validation"]
    assert validation["focused_qualification_provenance"]["passed"] == 40
    assert validation["final_gate_focused_rerun"]["passed"] == 13
    assert validation["full_remediation"] == {
        "passed": 243,
        "skipped": 1,
        "failed": 2,
        "warnings": 0,
        "exit_code": 1,
        "elapsed_seconds": 20.99,
    }
    assert validation["baseline"]["passed"] == 235
    assert validation["baseline"]["skipped"] == 1
    assert validation["baseline"]["failed"] == 2
    attribution = validation["baseline_attribution"]
    assert attribution["classification"] == "PRE_EXISTING / BASELINE_ATTRIBUTED"
    assert attribution["same_failures_at_baseline_and_remediation"] is True
    assert attribution["new_failures_introduced"] is False
    assert attribution["full_suite_claim"] != "green"


def test_m5_family_statement_does_not_close_semiconductor():
    family = _record()["family_status"]
    assert family["statement"] == "FIRST VALIDATED MEMBER OF THE RICH ORM/JOB QUALIFICATION REMEDIATION FAMILY"
    assert family["descriptive_only"] is True
    assert family["semiconductor_status"] == "INDEPENDENT IMPLEMENTATION AND PROOF REQUIRED"
    assert family["evidence_inheritance"] is False


def test_m5_known_evidence_admission_is_exact_and_generated():
    entries = json.loads(KNOWN.read_text(encoding="utf-8"))
    assert entries == build_known_evidence_index()
    smartwatch = [entry for entry in entries if entry["subject"] == "smartwatch-clank"]
    assert len(smartwatch) == 1
    entry = smartwatch[0]
    assert entry["standard"] == "STD-OPS-COM-003"
    assert entry["kind"] == "known_conformance"
    assert entry["source_reference"] == "audits/smartwatch-clank-qualification-remediation-m5-2026-09-01.md"
    assert SMARTWATCH_SHA in entry["summary"]
    assert "CONFORMS / CLOSED" in entry["summary"]
    assert {entry["standard"] for entry in entries if entry["subject"] == "smartwatch-clank"} == {"STD-OPS-COM-003"}


def test_m5_audit_prose_declares_scope_and_no_live_action():
    text = AUDIT_MD.read_text(encoding="utf-8")
    for marker in (
        "CONFORMS / CLOSED",
        SMARTWATCH_SHA,
        "STD-UI-COM-011",
        "STD-DEPLOY-COM-001",
        "STD-DEPLOY-COM-002",
        "PRE_EXISTING / BASELINE_ATTRIBUTED",
        "FIRST VALIDATED MEMBER OF THE RICH ORM/JOB QUALIFICATION REMEDIATION FAMILY",
        "Semiconductor still requires independent",
        "No host, deployment, live collector, or live-proof action occurred",
    ):
        assert marker in text


def test_m5_frozen_standard_files_and_tags_remain_unchanged():
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
