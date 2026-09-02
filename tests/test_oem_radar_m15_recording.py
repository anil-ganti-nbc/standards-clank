"""Narrow Standards guards for the OEM Radar M15 Deployment evidence record."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.deployment_agent_layer import build_known_evidence_index


ROOT = Path(__file__).resolve().parents[1]
AUDIT_JSON = ROOT / "audits" / "oem-radar-persistent-state-remediation-m15-2026-09-02.json"
AUDIT_MD = ROOT / "audits" / "oem-radar-persistent-state-remediation-m15-2026-09-02.md"
KNOWN = ROOT / "standards" / "deployment" / "known-evidence-index.json"
MANIFEST = ROOT / "baselines" / "deployment-standards-v1.0.json"

STANDARDS_SHA = "f3eef513ce89cf2fcb96dad0a60b9bd77ba62baa"
OEM_PARENT = "d720e0635894ddcc9a39f116e2aa4a1768090042"
OEM_SHA = "79fbee63ee3a43badad085671ba5bf6837b627f7"
FP_SHA = "b60e881319b16d36625268d9ba2d66cb8ea8f818"
RECIPE = "CURRENT_SCHEMA_BOOTSTRAP_SQLITE_COMPATIBILITY_RECIPE_VALIDATED"


def _record() -> dict:
    return json.loads(AUDIT_JSON.read_text(encoding="utf-8"))


def test_m15_records_exact_lineage_and_narrow_verdict():
    record = _record()
    assert record["standards_clank_head"] == STANDARDS_SHA
    target = record["oem_radar"]
    assert target["head"] == OEM_SHA
    assert target["origin_main"] == OEM_SHA
    assert target["parent"] == OEM_PARENT
    assert record["family_first_member"]["revision"] == FP_SHA
    assert target["standard"] == "STD-DEPLOY-COM-002"
    assert target["state"] == "CONFORMS"
    assert target["lifecycle"] == "CLOSED"
    assert target["scope"] == "source-level persistent-state compatibility only"
    assert record["verdict"]["revision"] == OEM_SHA
    for not_implied in (
        "implies_live_deployment_state",
        "implies_production_migration",
        "implies_deploy_com_001_closure",
        "implies_full_target_conformance",
    ):
        assert record["verdict"][not_implied] is False


def test_m15_preserves_laundering_defect_history_and_m1_lineage():
    record = _record()
    defect = record["m10"]["original_defect"]
    assert "layered the current schema" in defect and "swallowed duplicate-column" in defect
    assert "admission-ordering defect" in defect  # not merely a missing version check
    assert record["source_lineage"]["m1_head"] == OEM_PARENT
    assert record["source_lineage"]["m1_deploy_com_002"] == "INSUFFICIENT_EVIDENCE"
    assert record["source_lineage"]["m1_preserved"] is True
    assert record["source_lineage"]["m15_supersedes_defect_for_canonical_sha"] is True
    assert record["m10"]["classification"] == "NO_COMPATIBILITY_BARRIER"
    assert record["m10"]["risk"] == "HIGH"
    assert record["source_lineage"]["m9b_ops_com_003"] == "NOT_APPLICABLE"


def test_m15_orphan_qc_not_declared_active_and_inventory_scoped():
    record = _record()
    inventory = record["persistent_state_inventory"]
    orphan = inventory["orphan_artifact"]
    assert orphan["verdict"].startswith("NOT active schema authority")
    assert "zero source references" in orphan["verdict"]
    assert record["guards"]["orphan_qc_declared_active_authority"] is False
    assert inventory["canonical_evolving_store"]["authority"].startswith("schema_migrations v7")


def test_m15_real_db_observation_scoped_to_compatibility_only():
    record = _record()
    obs = record["real_radar_db_observation"]
    assert obs["mutated_during_m15"] is False and obs["byte_identical"] is True
    for not_claimed in (
        "deployment_proof", "production_migration_proof",
        "live_crawler_proof", "deploy_com_001_evidence",
    ):
        assert obs[not_claimed] is False
    assert obs["evidentiary_scope"].endswith("nothing more")


def test_m15_records_read_only_first_barrier_byte_neutral_and_model():
    record = _record()
    barrier = record["read_only_first_barrier"]
    assert barrier["inspection_handle"].startswith("mode=ro")
    assert barrier["byte_neutral_refusals"] is True
    assert barrier["independently_verified_from_source_ordering"] is True
    model = record["compatibility_model"]
    assert model["states"] == [
        "FRESH", "MIGRATION_REQUIRED", "COMPATIBLE", "INCOMPATIBLE_NEWER",
        "UNKNOWN", "CORRUPT", "PARTIAL",
    ]
    assert len(model["semantics"]) == 5
    assert "corroborated against the expected 20-table structure" in model["distinguishing_feature"]
    assert model["vocabulary_normative_fleet_wide"] is False


def test_m15_legacy_fixture_correction_recorded_as_stronger():
    record = _record()
    fix = record["historical_fixture_correction"]
    assert "marker-only pseudo-databases" in fix["before"]
    assert "error swallowing" in fix["before"]
    assert "canonical migration DDL" in fix["after"]
    assert fix["character"].startswith("STRONGER evidence, not relaxed")
    assert record["guards"]["legacy_fixtures_characterized_as_relaxed"] is False


def test_m15_one_shot_model_and_skew_recorded():
    record = _record()
    one_shot = record["one_shot_execution_model"]
    assert one_shot["ephemeral_lifetime_bypasses_authority"] is False
    assert one_shot["crawler_runs_id_is_compatibility_authority"] is False
    assert one_shot["event_persistence_before_admission"] is False
    assert one_shot["refused_crawl_writes_nothing"] is True
    skew = record["migration_and_skew"]
    assert skew["skew_contract"] == "FORWARD_ONLY_EXPLICIT"
    assert skew["rollback_claimed"] is False
    assert skew["duplicate_column_errors_swallowed"] is False
    assert skew["no_production_migration_in_m15"] is True
    assert record["barrier_coverage"]["unexplained_normal_bypass"] == "NONE"


def test_m15_validation_green_without_attribution():
    record = _record()
    validation = record["validation"]
    assert validation["baseline_at_parent"]["passed"] == 545
    assert validation["baseline_at_parent"]["failed"] == 0
    full = validation["full_suite_m15"]
    assert full["passed"] == 572 and full["failed"] == 0 and full["exit_code"] == 0
    assert validation["full_suite_green"] is True
    assert validation["new_m15_tests_passed"] == 27
    assert validation["baseline_attribution_needed"] is False
    assert validation["focused_independently_rerun_this_pass"]["passed"] == 82
    assert validation["a_ad_source_checks"] == {"verified": 31, "total": 31,
                                                "method": "mechanical read-only inspection of canonical source"}


def test_m15_named_implementation_checks():
    checks = _record()["implementation_checks"]
    expected_yes = {
        "A_expected_state_contract_explicit", "B_inspection_read_only",
        "C_fresh_distinguishable_from_unknown",
        "I_canonical_migration_authoritative", "J_migration_reverified",
        "L_every_operational_state_path_guarded", "Q_normal_v7_behavior_intact",
        "R_ops_com_003_applicability_decision_intact",
    }
    assert len(checks) == 18
    assert {k for k, v in checks.items() if v == "YES"} == expected_yes
    assert {k for k, v in checks.items() if v == "NO"} == set(checks) - expected_yes


def test_m15_remaining_findings_and_ops_com_003_preserved():
    record = _record()
    assert record["remaining_findings"]["STD-UI-COM-011"] == "unresolved"
    assert record["remaining_findings"]["STD-DEPLOY-COM-001"] == "unresolved"
    assert record["remaining_findings"]["STD-OPS-COM-003"] == "NOT_APPLICABLE (preserved)"
    orth = record["orthogonality"]
    assert orth["ops_com_003_not_applicable"] is True
    assert orth["qualification_gate_added"] is False
    assert orth["qualification_epochs_added"] is False
    assert orth["crawler_runs_id_is_telemetry_only"] is True
    assert orth["migration_set_unchanged"] == "2..7"


def test_m15_family_names_exactly_two_members_and_others_inherit_nothing():
    record = _record()
    family = record["family_status"]
    assert family["conclusion"] == RECIPE
    assert family["descriptive_only"] is True
    assert family["is_new_standard"] is False
    assert set(family["members"]) == {"feature-phone-clank", "oem-radar"}
    assert family["members"] == {"feature-phone-clank": FP_SHA, "oem-radar": OEM_SHA}
    assert family["contradictory_exception_required"] is False
    for key in (
        "ctw_inherits_conformance", "ctw_inherits_evidence",
        "ctw_inherits_implementation_prescription",
        "smartwatch_inherits_conformance", "smartwatch_inherits_evidence",
        "smartwatch_inherits_implementation_prescription",
    ):
        assert family[key] is False, key
    differences = family["recorded_differences"]
    assert "v5" in differences["feature_phone"] and "v7" in differences["oem_radar"]


def test_m15_admits_exactly_one_oem_deployment_fact():
    record = _record()
    admission = record["known_evidence_admission"]
    assert admission["admission_count"] == 1
    assert admission["admitted"] == {
        "subject": "oem-radar", "revision": OEM_SHA,
        "standard": "STD-DEPLOY-COM-002", "state": "CONFORMS", "lifecycle": "CLOSED",
    }
    assert admission["historical_m1_preserved"] is True
    assert admission["deploy_com_001_admitted"] is False
    assert admission["ui_com_011_admitted"] is False
    assert admission["ops_com_003_conformance_admitted"] is False
    assert len(admission["prior_admissions_preserved"]) == 5
    entries = json.loads(KNOWN.read_text(encoding="utf-8"))
    assert entries == build_known_evidence_index()
    oem = [e for e in entries if e["subject"] == "oem-radar"]
    assert len(oem) == 1 and oem[0]["standard"] == "STD-DEPLOY-COM-002"
    assert OEM_SHA in oem[0]["summary"]
    subjects = {e["subject"] for e in entries}
    assert subjects == {
        "feature-phone-clank", "korean-tech-wire", "oem-radar",
        "semiconductor-intelligence", "tablet-clank", "watch-clank",
    }
    # the Feature Phone family fact remains exactly as M14 admitted it
    fp = [e for e in entries if e["subject"] == "feature-phone-clank"]
    assert len(fp) == 1 and FP_SHA in fp[0]["summary"]


def test_m15_prose_scope_and_no_action_declaration():
    text = " ".join(AUDIT_MD.read_text(encoding="utf-8").split())
    for marker in (
        "CONFORMS / CLOSED", OEM_SHA, OEM_PARENT, STANDARDS_SHA, FP_SHA,
        "byte-identical", RECIPE, "admission-ordering defect",
        "evidence, not relaxed coverage", "FORWARD_ONLY_EXPLICIT",
        "NOT_APPLICABLE", "No host", "were not changed or moved",
        "NO CONFORMANCE INHERITANCE, NO EVIDENCE INHERITANCE, NO IMPLEMENTATION PRESCRIPTION",
    ):
        assert marker in text, marker
    assert "no overall OEM Radar" in text and "conformance" in text


def test_m15_frozen_deployment_standards_unchanged():
    """Pure-read guard: the frozen standard files still match the
    deployment-standards-v1.0 manifest's LF-normalized hashes (tag-target
    immutability itself is guarded by tests/test_deployment_baseline_v1_0.py)."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["status"] == "FROZEN"
    assert manifest["immutable_tag"] == "deployment-standards-v1.0"
    for artifact in manifest["artifacts"]["standard_files"].values():
        raw = (ROOT / artifact["path"]).read_bytes().replace(b"\r\n", b"\n")
        assert hashlib.sha256(raw).hexdigest() == artifact["sha256_lf_normalized"]


def test_m15_guards_declare_no_target_or_host_action():
    record = _record()
    guards = record["guards"]
    for key in (
        "frozen_standard_files_changed", "frozen_tags_changed_or_moved",
        "oem_radar_modified_in_this_pass", "feature_phone_modified_in_this_pass",
        "host_deployment_live_or_production_db_actions", "production_migration",
        "full_target_conformance_claim", "orphan_qc_declared_active_authority",
        "real_db_observation_overstated", "legacy_fixtures_characterized_as_relaxed",
    ):
        assert guards[key] is False, key
