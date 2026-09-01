"""Narrow guards for the KTW M8 Operations evidence record."""

import json
import subprocess
from pathlib import Path

from tools.operations_agent_layer import build_known_evidence_index


ROOT = Path(__file__).resolve().parents[1]
AUDIT_MD = ROOT / "audits" / "ktw-qualification-remediation-m8-2026-09-01.md"
AUDIT_JSON = ROOT / "audits" / "ktw-qualification-remediation-m8-2026-09-01.json"
KNOWN = ROOT / "standards" / "operations" / "known-evidence-index.json"
KTW_SHA = "2040af82136d8a8f181c464e7d62ce408dd2696d"
KTW_PARENT = "afb4aada1d4fae09ada4658fe9fcf8dfa38eb23d"
STANDARDS_SHA = "ea0549fa94aa4ffbda7deee00f13d71a3d203bdb"


def _record():
    return json.loads(AUDIT_JSON.read_text(encoding="utf-8"))


def test_m8_records_exact_target_lineage_and_narrow_verdict():
    record = _record()
    assert record["standards_clank_head"] == STANDARDS_SHA
    target = record["ktw"]
    assert target["head"] == KTW_SHA
    assert target["origin_main"] == KTW_SHA
    assert target["parent"] == KTW_PARENT
    assert target["standard"] == "STD-OPS-COM-003"
    assert target["state"] == "CONFORMS"
    assert target["lifecycle"] == "CLOSED"
    assert target["scope"] == "source-level qualification provenance/reset remediation only"


def test_m8_preserves_m1_insufficiencies_without_unrelated_closure():
    record = _record()
    assert record["source_lineage"]["m1_original_state"] == "INSUFFICIENT_EVIDENCE"
    assert record["source_lineage"]["m1_applicable"] == 23
    assert record["source_lineage"]["m1_conforms"] == 18
    assert record["source_lineage"]["m1_non_conforming"] == 0
    assert record["source_lineage"]["m1_insufficient_evidence"] == 5
    assert record["source_lineage"]["m1_insufficient_standards"] == [
        "STD-DATA-COM-001",
        "STD-UI-COM-011",
        "STD-OPS-COM-003",
        "STD-DEPLOY-COM-001",
        "STD-DEPLOY-COM-002",
    ]
    assert record["remaining_m1_insufficiencies"] == {
        "STD-DATA-COM-001": "INSUFFICIENT_EVIDENCE",
        "STD-UI-COM-011": "INSUFFICIENT_EVIDENCE",
        "STD-DEPLOY-COM-001": "INSUFFICIENT_EVIDENCE",
        "STD-DEPLOY-COM-002": "INSUFFICIENT_EVIDENCE",
    }
    assert record["known_evidence_admission"]["historical_m1_preserved"] is True
    assert record["known_evidence_admission"]["unrelated_standards_admitted"] is False
    assert record["guards"]["full_target_conformance_claim"] is False


def test_m8_records_all_qualification_invariants_and_additive_migration():
    record = _record()
    assert set(record["implementation_checks"].values()) == {"YES"}
    migration = record["migration"]
    assert migration["revision"] == 5
    assert migration["additive"] is True
    assert migration["legacy_history_preserved"] is True
    assert migration["legacy_unknown_provenance_preserved"] is True
    assert migration["destructive_reset"] is False
    assert record["validation"]["full_suite"] == {
        "passed": 92,
        "skipped": 0,
        "failed": 0,
        "exit_code": 0,
    }


def test_m8_family_statement_is_descriptive_and_independent():
    family = _record()["family_status"]
    assert family["conclusion"] == "THIRD_ARCHITECTURAL_SHAPE_UNDER_SHARED_OPS_COM_003_CONTRACT"
    assert family["descriptive_only"] is True
    assert family["architecture"] == "AGGREGATE_SQLITE_HEALTH_HISTORY"
    assert family["ktw_independently_validated"] is True
    assert family["evidence_inheritance"] is False
    assert family["other_target_conformance_inferred"] is False
    assert family["oem_radar_applicability_inferred"] is False


def test_m8_known_evidence_adds_exactly_one_operations_fact():
    record = _record()
    admission = record["known_evidence_admission"]
    assert admission["admission_count"] == 1
    assert admission["admitted"] == {
        "subject": "korean-tech-wire",
        "revision": KTW_SHA,
        "standard": "STD-OPS-COM-003",
        "state": "CONFORMS",
        "lifecycle": "CLOSED",
    }
    entries = json.loads(KNOWN.read_text(encoding="utf-8"))
    assert entries == build_known_evidence_index()
    ktw = [entry for entry in entries if entry["subject"] == "korean-tech-wire"]
    assert len(ktw) == 1
    assert ktw[0]["standard"] == "STD-OPS-COM-003"
    assert ktw[0]["kind"] == "known_conformance"
    assert ktw[0]["source_reference"] == "audits/ktw-qualification-remediation-m8-2026-09-01.md"
    assert KTW_SHA in ktw[0]["summary"]
    assert "CONFORMS / CLOSED" in ktw[0]["summary"]
    assert all(entry["subject"] != "oem-radar" for entry in entries)


def test_m8_prose_declares_scope_safety_and_third_shape():
    text = AUDIT_MD.read_text(encoding="utf-8")
    for marker in (
        "CONFORMS / CLOSED",
        KTW_SHA,
        KTW_PARENT,
        "STD-DATA-COM-001",
        "STD-UI-COM-011",
        "STD-DEPLOY-COM-001",
        "STD-DEPLOY-COM-002",
        "aggregate SQLite health-history",
        "third architectural shape",
        "No Deployment evidence",
        "No host",
        "OEM Radar remains unresolved",
    ):
        assert marker in text
    assert "No overall target conformance claim" in text


def test_m8_frozen_standards_and_tags_unchanged():
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
