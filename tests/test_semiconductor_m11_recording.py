"""Narrow Standards guards for Semiconductor M11 Deployment evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from tools.deployment_agent_layer import build_known_evidence_index


ROOT = Path(__file__).resolve().parents[1]
AUDIT_JSON = ROOT / "audits" / "semiconductor-persistent-state-remediation-m11-2026-09-01.json"
AUDIT_MD = ROOT / "audits" / "semiconductor-persistent-state-remediation-m11-2026-09-01.md"
KNOWN = ROOT / "standards" / "deployment" / "known-evidence-index.json"
STANDARDS_HEAD = "5d1309fd4dff3d427aad095fadb26aedb2a7c5fd"
SEMICONDUCTOR_SHA = "8085a1bbd1a4e133680702e8c1d916b71bb78a14"
EXPECTED_HEAD = "c7d8e9f0a1b2"


def _record() -> dict:
    return json.loads(AUDIT_JSON.read_text(encoding="utf-8"))


def test_m11_records_exact_target_lineage_and_narrow_verdict():
    record = _record()
    assert record["standards_clank_head"] == STANDARDS_HEAD
    target = record["semiconductor"]
    assert target["target"] == "semiconductor-intelligence"
    assert target["head"] == SEMICONDUCTOR_SHA
    assert target["origin_main"] == SEMICONDUCTOR_SHA
    assert target["standard"] == "STD-DEPLOY-COM-002"
    assert target["state"] == "CONFORMS"
    assert target["lifecycle"] == "CLOSED"
    assert record["remaining_m1_insufficiencies"] == {
        "STD-UI-COM-006": "INSUFFICIENT_EVIDENCE",
        "STD-UI-COM-007": "INSUFFICIENT_EVIDENCE",
        "STD-UI-COM-011": "INSUFFICIENT_EVIDENCE",
        "STD-DEPLOY-COM-001": "INSUFFICIENT_EVIDENCE",
    }
    assert record["source_lineage"]["prior_closed_after_m1"] == ["STD-OPS-COM-003"]


def test_m11_records_exact_head_barrier_and_all_source_checks():
    record = _record()
    assert set(record["implementation_checks"].values()) == {"YES"}
    contract = record["remediation_contract"]
    assert contract["expected_head"] == EXPECTED_HEAD
    assert contract["create_all_compatibility_admission"] is False
    assert contract["automatic_stamp_fallback"] is False
    assert contract["no_production_migration"] is True
    assert "CLI _session" in contract["normal_entry_points"]
    assert "dashboard request dependency" in contract["normal_entry_points"]
    assert "runtime_bridge health/identity" in contract["normal_entry_points"]


def test_m11_preserves_migration_distinction_and_honest_full_suite_attribution():
    record = _record()
    migration = record["migration"]
    assert migration["added"] is False
    assert migration["production_migration"] is False
    assert migration["compatibility_barrier_is_read_only"] is True
    validation = record["validation"]
    assert validation["focused"] == {"passed": 21, "skipped": 0, "failed": 0, "exit_code": 0}
    assert validation["full_suite"] == {
        "passed": 894,
        "skipped": 1,
        "failed": 11,
        "warnings": 38254,
        "elapsed_seconds": 1622.52,
        "exit_code": 1,
    }
    assert validation["full_suite_green"] is False
    attribution = validation["failure_attribution"]
    assert attribution["classification"] == "ENVIRONMENTAL / BASELINE-UNRELATED TO M11"
    assert attribution["windows_winerror_50_subprocess_failures"] == 10
    assert attribution["node_dashboard_parse_failures"] == 1
    assert attribution["m11_implementation_failures_remaining"] == 0
    assert attribution["compatibility_migration_failures_remaining"] == 0
    assert attribution["attribution_preserved_honestly"] is True


def test_m11_admits_only_semiconductor_deploy_com_002_and_preserves_watch():
    record = _record()
    admission = record["known_evidence_admission"]
    assert admission["admission_count"] == 1
    assert admission["admitted"] == {
        "subject": "semiconductor-intelligence",
        "revision": SEMICONDUCTOR_SHA,
        "standard": "STD-DEPLOY-COM-002",
        "state": "CONFORMS",
        "lifecycle": "CLOSED",
    }
    assert admission["deploy_com_001_admitted"] is False
    entries = json.loads(KNOWN.read_text(encoding="utf-8"))
    assert entries == build_known_evidence_index()
    semiconductor = [entry for entry in entries if entry["subject"] == "semiconductor-intelligence"]
    assert len(semiconductor) == 2  # COM-002 + COM-001 (Semiconductor joins COM-001 at M55,
    # audits/semiconductor-deployment-proof-m55-2026-09-05.md)
    com002 = [entry for entry in semiconductor if entry["standard"] == "STD-DEPLOY-COM-002"]
    assert len(com002) == 1 and SEMICONDUCTOR_SHA in com002[0]["summary"]
    assert any(
        entry["subject"] == "watch-clank" and entry["standard"] == "STD-DEPLOY-COM-001"
        for entry in entries
    )
    # M55 admitted the Semiconductor COM-001 live proof; COM-002 remains
    # the only other Semiconductor fact, unchanged in scope.
    assert sorted(e["standard"] for e in entries
                  if e["subject"] == "semiconductor-intelligence") == [
        "STD-DEPLOY-COM-001", "STD-DEPLOY-COM-002"
    ]
    assert admission["other_targets_inherited"] is False


def test_m11_prose_and_family_status_are_descriptive_and_safe():
    record = _record()
    family = record["family_status"]
    assert family["conclusion"] == "FIRST_VALIDATED_MEMBER_OF_ALEMBIC_MIGRATION_HEAD_DEPLOY_COM_002_FAMILY"
    assert family["descriptive_only"] is True
    assert family["evidence_inheritance"] is False
    assert family["other_target_conformance_inferred"] is False
    guards = record["guards"]
    assert guards["frozen_standard_files_changed"] is False
    assert guards["frozen_tags_changed_or_moved"] is False
    assert guards["semiconductor_modified_in_this_pass"] is False
    assert guards["host_deployment_live_or_production_db_actions"] is False
    text = AUDIT_MD.read_text(encoding="utf-8")
    for marker in (
        "CONFORMS / CLOSED",
        SEMICONDUCTOR_SHA,
        EXPECTED_HEAD,
        "create_all",
        "automatic `stamp head` fallback is removed",
        "full suite is therefore not green",
        "STD-DEPLOY-COM-001` remains unresolved",
        "first validated member of the Alembic migration-head",
        "No host",
        "Frozen Deployment standard files",
    ):
        assert marker in text
    assert "no overall Semiconductor conformance" in text


def test_m11_frozen_deployment_standards_and_tags_unchanged():
    for path in sorted((ROOT / "standards" / "deployment").glob("STD-DEPLOY-*.json")):
        tagged = subprocess.run(
            ["git", "show", f"deployment-standards-v1.0:{path.relative_to(ROOT).as_posix()}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            stdin=subprocess.DEVNULL,
            check=True,
        ).stdout
        assert path.read_text(encoding="utf-8") == tagged
    tag = subprocess.run(
        ["git", "rev-parse", "deployment-standards-v1.0^{commit}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        stdin=subprocess.DEVNULL,
        check=True,
    ).stdout.strip()
    assert tag == "33cc38849180716fd4d06b1356cf70c49d3d41d2"
