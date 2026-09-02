"""Narrow Standards guards for the Feature Phone M14 Deployment evidence record."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.deployment_agent_layer import build_known_evidence_index


ROOT = Path(__file__).resolve().parents[1]
AUDIT_JSON = ROOT / "audits" / "feature-phone-persistent-state-remediation-m14-2026-09-02.json"
AUDIT_MD = ROOT / "audits" / "feature-phone-persistent-state-remediation-m14-2026-09-02.md"
KNOWN = ROOT / "standards" / "deployment" / "known-evidence-index.json"
MANIFEST = ROOT / "baselines" / "deployment-standards-v1.0.json"

STANDARDS_SHA = "ec83824d109263b1ae7ee92b02f2f271fea4fe0b"
FP_PARENT = "4b7dce284f7c581395c5efe2b20ce1872e26897e"
FP_SHA = "b60e881319b16d36625268d9ba2d66cb8ea8f818"
FAMILY = "FIRST_VALIDATED_MEMBER_OF_CURRENT_SCHEMA_BOOTSTRAP_SQLITE_COMPATIBILITY"


def _record() -> dict:
    return json.loads(AUDIT_JSON.read_text(encoding="utf-8"))


def test_m14_records_exact_lineage_and_narrow_verdict():
    record = _record()
    assert record["standards_clank_head"] == STANDARDS_SHA
    target = record["feature_phone"]
    assert target["head"] == FP_SHA
    assert target["origin_main"] == FP_SHA
    assert target["parent"] == FP_PARENT
    assert target["standard"] == "STD-DEPLOY-COM-002"
    assert target["state"] == "CONFORMS"
    assert target["lifecycle"] == "CLOSED"
    assert target["scope"] == "source-level persistent-state compatibility only"
    assert record["verdict"]["revision"] == FP_SHA
    for not_implied in (
        "implies_live_deployment_compatibility",
        "implies_production_db_migration",
        "implies_production_state_convergence",
        "implies_deploy_com_001_closure",
        "implies_full_target_conformance",
    ):
        assert record["verdict"][not_implied] is False


def test_m14_preserves_architectural_defect_history_and_m1_lineage():
    record = _record()
    defect = record["m10"]["original_defect"]
    assert "SqliteStore.__init__" in defect and "invoked migration" in defect
    assert record["source_lineage"]["m1_head"] == "4051b64fe7ba4dc188ec1e1a6920ce72b14f013d"
    assert record["source_lineage"]["m1_deploy_com_002"] == "INSUFFICIENT_EVIDENCE"
    assert record["source_lineage"]["m1_preserved"] is True
    assert record["source_lineage"]["m14_supersedes_defect_for_canonical_sha"] is True
    assert record["m10"]["classification"] == "PARTIAL_MECHANISM"
    assert record["m10"]["risk"] == "HIGH"


def test_m14_records_read_only_first_barrier_and_state_model():
    record = _record()
    barrier = record["read_only_first_barrier"]
    assert barrier["inspection_handle"].startswith("mode=ro")
    assert barrier["byte_neutral_refusals"] is True
    assert "refused persistent file remains byte-identical" in barrier["evidence_strength"]
    model = record["compatibility_model"]
    assert model["states"] == [
        "FRESH", "MIGRATION_REQUIRED", "COMPATIBLE", "INCOMPATIBLE_NEWER",
        "UNKNOWN", "CORRUPT", "PARTIAL",
    ]
    assert "UNKNOWN" in model["fresh_vs_unknown"] and "fail closed" in model["fresh_vs_unknown"]
    assert model["ready_state"] == "COMPATIBLE"
    assert record["authorities"]["main_store"]["expected_version"] == 5


def test_m14_v4_observation_is_scoped_to_inference_not_production_proof():
    record = _record()
    v4 = record["real_v4_observation"]
    assert v4["observed_state"].startswith("schema_migrations 1-4")
    assert v4["mutated_during_m14"] is False
    assert v4["production_deployment_proof"] is False
    assert v4["normal_mutable_open_exercised_against_original"] is False
    assert "MIGRATION_REQUIRED" in v4["valid_inference_only"]
    assert "COPY" in v4["copy_based_evidence"]


def test_m14_records_skew_failure_semantics_and_bypass_search():
    record = _record()
    skew = record["migration_and_skew"]
    assert skew["skew_contract"] == "FORWARD_ONLY_EXPLICIT"
    assert skew["rollback_claimed"] is False
    assert skew["production_migration_in_m14"] is False
    assert skew["failed_migration_marks_ready"] is False
    assert skew["incompatible_state"].startswith("preserved for diagnosis")
    coverage = record["barrier_coverage"]
    assert coverage["unexplained_normal_bypass"] == "NONE"
    for surface in ("cli", "dashboard", "controller_workers", "health", "direct_consumers"):
        assert coverage[surface]
    orth = record["orthogonality"]
    assert orth["held_run_lock_admits_incompatible_state"] is False
    assert orth["qualification_evidence_admits_incompatible_state"] is False
    assert orth["ops_com_003_closed"] is True and orth["ops_com_004_closed"] is True


def test_m14_validation_recorded_honestly_not_green():
    record = _record()
    validation = record["validation"]
    assert validation["focused"] == {
        "m14_compatibility": 34, "db_migrations": 2,
        "qualification_ops_com_003": 3, "run_lock_ops_com_004": 6,
        "scope_collector_dashboard": 26,
        "independently_rerun_during_this_pass": True,
    }
    assert validation["baseline_at_parent"] == {
        "head": FP_PARENT, "passed": 218, "skipped": 1, "failed": 4,
    }
    full = validation["full_suite_m14"]
    assert full["passed"] == 252 and full["failed"] == 4 and full["exit_code"] == 1
    assert validation["full_suite_green"] is False
    attribution = validation["baseline_attribution"]
    assert attribution["classification"] == "PRE_EXISTING / BASELINE_ATTRIBUTED"
    assert attribution["same_four_failures_unchanged"] is True
    assert attribution["no_new_full_suite_failure_introduced"] is True
    assert attribution["all_34_new_m14_tests_passed"] is True
    assert "clank_runtime/HealthPayload" in attribution["detail"]


def test_m14_named_implementation_checks():
    checks = _record()["implementation_checks"]
    expected_yes = {
        "A_expected_state_contract_explicit", "B_compatibility_inspection_read_only",
        "C_fresh_distinguishable_from_unknown",
        "I_canonical_migration_bootstrap_authoritative",
        "J_successful_migration_reverified",
        "L_every_operational_state_path_crosses_barrier",
        "Q_normal_v5_behavior_intact", "R_ops_com_003_remains_intact",
        "S_ops_com_004_remains_intact",
    }
    expected_no = set(checks) - expected_yes
    assert len(checks) == 19
    assert {k for k, v in checks.items() if v == "YES"} == expected_yes
    assert {k for k, v in checks.items() if v == "NO"} == expected_no


def test_m14_remaining_findings_and_prior_closures_preserved():
    record = _record()
    assert record["remaining_findings"] == {
        "STD-UI-COM-011": "unresolved", "STD-DEPLOY-COM-001": "unresolved",
    }
    assert set(record["prior_closed_after_m1"]) == {"STD-OPS-COM-003", "STD-OPS-COM-004"}


def test_m14_family_names_only_feature_phone_and_oem_radar_inherits_nothing():
    record = _record()
    family = record["family_status"]
    assert family["conclusion"] == FAMILY
    assert family["descriptive_only"] is True
    assert set(family["members"]) == {"feature-phone-clank"}
    assert family["members"]["feature-phone-clank"] == FP_SHA
    assert family["oem_radar_inherits_conformance"] is False
    assert family["oem_radar_inherits_evidence"] is False
    assert family["oem_radar_inherits_implementation_prescription"] is False
    assert family["smartwatch_or_ctw_inherit_anything"] is False


def test_m14_admits_exactly_one_feature_phone_deployment_fact():
    record = _record()
    admission = record["known_evidence_admission"]
    assert admission["performed"] is True
    assert admission["admission_count"] == 1
    assert admission["admitted"] == {
        "subject": "feature-phone-clank", "revision": FP_SHA,
        "standard": "STD-DEPLOY-COM-002", "state": "CONFORMS", "lifecycle": "CLOSED",
    }
    assert admission["historical_m1_preserved"] is True
    assert admission["deploy_com_001_admitted"] is False
    assert admission["ui_com_011_admitted"] is False
    assert admission["oem_radar_evidence_created"] is False
    entries = json.loads(KNOWN.read_text(encoding="utf-8"))
    assert entries == build_known_evidence_index()
    fp = [e for e in entries if e["subject"] == "feature-phone-clank"]
    assert len(fp) == 1 and fp[0]["standard"] == "STD-DEPLOY-COM-002"
    assert FP_SHA in fp[0]["summary"]
    # every prior admission preserved, none replaced
    subjects = {e["subject"] for e in entries}
    # oem-radar joins at M15; chinese-tech-wire joins at M17. The Feature
    # Phone admission itself is unchanged.
    assert subjects == {
        "feature-phone-clank", "korean-tech-wire", "oem-radar",
        "chinese-tech-wire", "semiconductor-intelligence", "tablet-clank",
        "watch-clank",
    }
    assert [e for e in entries if e["standard"] == "STD-DEPLOY-COM-001"] and \
        all(e["subject"] == "watch-clank" for e in entries if e["standard"] == "STD-DEPLOY-COM-001")


def test_m14_prose_scope_and_no_action_declaration():
    text = " ".join(AUDIT_MD.read_text(encoding="utf-8").split())
    for marker in (
        "CONFORMS / CLOSED", FP_SHA, FP_PARENT, STANDARDS_SHA,
        "byte-identical", FAMILY, "NOT green", "PRE_EXISTING / BASELINE_ATTRIBUTED",
        "copy-based evidence, not production migration",
        "NO CONFORMANCE, NO EVIDENCE, NO IMPLEMENTATION PRESCRIPTION",
        "remain unresolved", "`STD-DEPLOY-COM-001`", "`STD-UI-COM-011`",
        "No host", "were not changed or moved",
    ):
        assert marker in text, marker
    assert "no overall Feature Phone" in text and "conformance" in text


def test_m14_frozen_deployment_standards_unchanged():
    """Pure-read guard: the frozen standard files still match the
    deployment-standards-v1.0 manifest's LF-normalized hashes (tag-target
    immutability itself is guarded by tests/test_deployment_baseline_v1_0.py)."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["status"] == "FROZEN"
    assert manifest["immutable_tag"] == "deployment-standards-v1.0"
    for artifact in manifest["artifacts"]["standard_files"].values():
        raw = (ROOT / artifact["path"]).read_bytes().replace(b"\r\n", b"\n")
        assert hashlib.sha256(raw).hexdigest() == artifact["sha256_lf_normalized"]


def test_m14_guards_declare_no_target_or_host_action():
    record = _record()
    guards = record["guards"]
    for key in (
        "frozen_standard_files_changed", "frozen_tags_changed_or_moved",
        "feature_phone_modified_in_this_pass", "local_v4_production_db_modified",
        "host_deployment_live_or_production_db_actions", "production_migration",
        "full_target_conformance_claim", "other_target_evidence_inherited",
    ):
        assert guards[key] is False, key
