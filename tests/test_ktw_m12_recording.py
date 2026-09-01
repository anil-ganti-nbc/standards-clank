"""Narrow Standards guards for the KTW M12 Deployment evidence record."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from tools.deployment_agent_layer import build_known_evidence_index


ROOT = Path(__file__).resolve().parents[1]
AUDIT_JSON = ROOT / "audits" / "ktw-persistent-state-remediation-m12-2026-09-02.json"
AUDIT_MD = ROOT / "audits" / "ktw-persistent-state-remediation-m12-2026-09-02.md"
KNOWN = ROOT / "standards" / "deployment" / "known-evidence-index.json"
STANDARDS_SHA = "30c573eb151013a4174a22f62bb284fbcfcc5ed2"
KTW_PARENT = "2040af82136d8a8f181c464e7d62ce408dd2696d"
KTW_SHA = "354cb7aed0b174923393a0c71e7c4c6230cda28c"


def _record() -> dict:
    return json.loads(AUDIT_JSON.read_text(encoding="utf-8"))


def test_m12_records_exact_lineage_two_authorities_and_narrow_verdict():
    record = _record()
    assert record["standards_clank_head"] == STANDARDS_SHA
    target = record["ktw"]
    assert target["head"] == KTW_SHA
    assert target["origin_main"] == KTW_SHA
    assert target["parent"] == KTW_PARENT
    assert target["standard"] == "STD-DEPLOY-COM-002"
    assert target["state"] == "CONFORMS"
    assert target["lifecycle"] == "CLOSED"
    authorities = record["persistent_state_authorities"]
    assert authorities["main_collector_database"]["expected_version"] == 5
    assert authorities["qc_archive"]["expected_version"] == 1


def test_m12_preserves_history_and_only_closes_deploy_compatibility():
    record = _record()
    assert record["source_lineage"]["m1_original_state"] == "INSUFFICIENT_EVIDENCE"
    assert record["source_lineage"]["m1_insufficient_evidence"] == 5
    assert record["remaining_m1_insufficiencies"] == {
        "STD-DATA-COM-001": "INSUFFICIENT_EVIDENCE",
        "STD-UI-COM-011": "INSUFFICIENT_EVIDENCE",
        "STD-DEPLOY-COM-001": "INSUFFICIENT_EVIDENCE",
    }
    assert record["prior_closed_after_m1"] == ["STD-OPS-COM-003"]
    assert record["known_evidence_admission"]["historical_m1_preserved"] is True
    assert record["known_evidence_admission"]["unrelated_ktw_standards_admitted"] is False


def test_m12_records_named_fail_closed_contract_and_green_validation():
    record = _record()
    model = record["compatibility_model"]
    assert model["states"] == ["FRESH", "MIGRATION_REQUIRED", "COMPATIBLE", "INCOMPATIBLE_NEWER", "UNKNOWN", "CORRUPT", "PARTIAL"]
    assert model["normal_work_ready_state"] == "COMPATIBLE"
    assert "non-empty" in model["fresh_vs_unknown"]
    checks = record["implementation_checks"]
    assert all(value == "YES" for key, value in checks.items() if key[0] in "ABHIKMN")
    assert all(value == "NO" for key, value in checks.items() if key[0] in "CDEFGJL")
    contract = record["remediation_contract"]
    assert contract["production_migration"] is False
    assert contract["rollback"] == "no rollback compatibility guarantee is claimed"
    assert record["validation"]["compatibility"]["passed"] == 7
    assert record["validation"]["focused"]["passed"] == 57
    assert record["validation"]["full_suite"] == {"passed": 99, "skipped": 0, "failed": 0, "warnings": 0, "elapsed_seconds": 22.25, "exit_code": 0}
    assert record["validation"]["full_suite_green"] is True


def test_m12_admits_exactly_one_ktw_deploy_fact_without_inheritance():
    record = _record()
    admission = record["known_evidence_admission"]
    assert admission["admission_count"] == 1
    assert admission["admitted"] == {
        "subject": "korean-tech-wire",
        "revision": KTW_SHA,
        "standard": "STD-DEPLOY-COM-002",
        "state": "CONFORMS",
        "lifecycle": "CLOSED",
    }
    entries = json.loads(KNOWN.read_text(encoding="utf-8"))
    assert entries == build_known_evidence_index()
    ktw = [entry for entry in entries if entry["subject"] == "korean-tech-wire"]
    assert len(ktw) == 1
    assert ktw[0]["standard"] == "STD-DEPLOY-COM-002"
    assert KTW_SHA in ktw[0]["summary"]
    assert any(entry["subject"] == "watch-clank" for entry in entries)
    assert any(entry["subject"] == "semiconductor-intelligence" for entry in entries)
    family = record["family_status"]
    assert family["conclusion"] == "FIRST_VALIDATED_MEMBER_OF_NUMBERED_SQLITE_COMPATIBILITY_FAMILY"
    assert family["tablet_inherits_conformance"] is False
    assert family["evidence_inheritance"] is False


def test_m12_prose_scope_and_frozen_deployment_standard_guard():
    text = AUDIT_MD.read_text(encoding="utf-8")
    for marker in (
        "CONFORMS / CLOSED", KTW_SHA, KTW_PARENT, "v5", "v1",
        "FRESH", "UNKNOWN", "99 passed", "DEPLOY-COM-001` remains unresolved",
        "first validated member of the numbered-SQLite", "Tablet inherits nothing", "No host",
    ):
        assert marker in text
    assert "no overall KTW" in text and "conformance is claimed" in text
    for path in sorted((ROOT / "standards" / "deployment").glob("STD-DEPLOY-*.json")):
        tagged = subprocess.run(
            ["git", "show", f"deployment-standards-v1.0:{path.relative_to(ROOT).as_posix()}"],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL, check=True,
        ).stdout
        assert path.read_text(encoding="utf-8") == tagged
    tag = subprocess.run(
        ["git", "rev-parse", "deployment-standards-v1.0^{commit}"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL, check=True,
    ).stdout.strip()
    assert tag == "33cc38849180716fd4d06b1356cf70c49d3d41d2"
