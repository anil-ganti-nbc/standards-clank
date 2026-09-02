"""Narrow Standards guards for the CTW M17 Deployment evidence record."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.deployment_agent_layer import build_known_evidence_index


ROOT = Path(__file__).resolve().parents[1]
AUDIT_JSON = ROOT / "audits" / "ctw-persistent-state-remediation-m17-2026-09-02.json"
AUDIT_MD = ROOT / "audits" / "ctw-persistent-state-remediation-m17-2026-09-02.md"
KNOWN = ROOT / "standards" / "deployment" / "known-evidence-index.json"
MANIFEST = ROOT / "baselines" / "deployment-standards-v1.0.json"

STANDARDS_SHA = "a78d2a4d2c55bc533d80770845aba65731ae3967"
CTW_PARENT = "1a47220c69e6bb91f2899a0508508c42254c9d5b"
CTW_SHA = "c340a45ac8cfbab58d749dcbf78a7d703ca9cdb1"
FAMILY = "FIRST_VALIDATED_MEMBER_OF_CREATE_ALL_WITH_EXPLICIT_SCHEMA_AUTHORITY"


def _record() -> dict:
    return json.loads(AUDIT_JSON.read_text(encoding="utf-8"))


def test_m17_records_exact_lineage_and_narrow_verdict():
    record = _record()
    assert record["standards_clank_head"] == STANDARDS_SHA
    target = record["ctw"]
    assert target["head"] == CTW_SHA
    assert target["origin_main"] == CTW_SHA
    assert target["parent"] == CTW_PARENT
    assert target["standard"] == "STD-DEPLOY-COM-002"
    assert target["state"] == "CONFORMS"
    assert target["lifecycle"] == "CLOSED"
    assert target["scope"] == "source-level persistent-state compatibility only"
    assert record["verdict"]["revision"] == CTW_SHA
    for not_implied in (
        "implies_deployed_m17_state",
        "implies_real_db_adoption",
        "implies_production_migration",
        "implies_deploy_com_001_closure",
        "implies_full_target_conformance",
    ):
        assert record["verdict"][not_implied] is False


def test_m17_preserves_mutation_as_admission_defect_and_m1_lineage():
    record = _record()
    defect = record["original_defect"]
    assert defect["summary"] == (
        "mutation-as-admission without durable compatibility authority"
    )
    assert "even health/identity passed through mutating initialization" in defect["details"]
    assert record["source_lineage"]["m1_head"] == CTW_PARENT
    assert record["source_lineage"]["m1_deploy_com_002"] == "INSUFFICIENT_EVIDENCE"
    assert record["source_lineage"]["m1_preserved"] is True
    assert record["m16_recon"]["classification"] == (
        "CREATE_ALL_BOOTSTRAP_WITH_NEW_VERSION_AUTHORITY"
    )
    assert record["m10"]["risk"] == "HIGH"


def test_m17_authority_is_marker_plus_structure_never_metadata():
    record = _record()
    authority = record["primary_authority"]
    assert authority["table"] == "schema_meta"
    assert authority["expected_version"] == 1
    assert authority["model_metadata_is_not_the_authority"] is True
    assert authority["marker_alone_insufficient"] is True
    corr = record["structural_corroboration"]
    assert "required columns per table" in " ".join(corr["verified"])
    # the honest limits are recorded, not overclaimed
    assert "SQL type equality" in " ".join(corr["not_claimed"])
    assert "index equivalence" in " ".join(corr["not_claimed"])
    assert "nullability/constraint equivalence" in " ".join(corr["not_claimed"])


def test_m17_legacy_unadopted_is_first_class_and_distinct():
    record = _record()
    legacy = record["legacy_unadopted"]
    assert legacy["distinct_from_fresh"] is True
    assert legacy["distinct_from_migration_required"] is True
    assert legacy["distinct_from_compatible"] is True
    assert legacy["normal_operation"] == "fails closed everywhere"
    assert legacy["promotion_path"] == "explicit operator adoption only"
    assert legacy["real_ctw_db_state"] == "LEGACY_UNADOPTED"
    model = record["compatibility_model"]
    assert model["states"] == [
        "FRESH", "LEGACY_UNADOPTED", "MIGRATION_REQUIRED", "COMPATIBLE",
        "INCOMPATIBLE_NEWER", "UNKNOWN", "CORRUPT", "PARTIAL",
    ]
    assert "FRESH != LEGACY_UNADOPTED" in model["semantics"]
    assert "LEGACY_UNADOPTED != COMPATIBLE" in model["semantics"]


def test_m17_adoption_is_distinct_from_bootstrap_and_migration():
    record = _record()
    adoption = record["adoption"]
    assert adoption["command"] == "--adopt-current-schema"
    assert adoption["operator_only"] is True
    assert adoption["read_only_structural_proof_first"] is True
    assert adoption["no_repair_before_proof"] is True
    assert adoption["writes_after_proof"] is True
    assert adoption["reinspects_after_write"] is True
    assert adoption["distinct_from_bootstrap"] is True
    assert adoption["distinct_from_migration"] is True
    assert adoption["never_part_of_initialization"] is True
    assert adoption["re_adoption_of_adopted_store_refused"] is True
    for refused in (
        "missing tables", "missing required columns", "corrupt",
        "partial", "contradictory/unknown",
    ):
        assert refused in adoption["refuses"], refused
    # and the record never characterizes adoption as bootstrap or migration
    assert record["guards"]["adoption_represented_as_bootstrap_or_migration"] is False


def test_m17_real_db_scoped_and_never_adopted():
    record = _record()
    obs = record["real_db_observation"]
    assert obs["classification"] == "LEGACY_UNADOPTED"
    assert obs["marker"] == "absent"
    assert obs["byte_identical_through_m17"] is True
    assert obs["adopted"] is False and obs["migrated"] is False
    for not_claimed in (
        "deploy_com_001_proof", "production_adoption_proof",
        "production_migration_proof", "deployed_binary_is_m17_evidence",
    ):
        assert obs[not_claimed] is False
    assert record["guards"]["real_ctw_db_adopted_stamped_or_migrated"] is False


def test_m17_create_all_restriction_and_skew_recorded():
    record = _record()
    restriction = record["create_all_restriction"]
    assert restriction["single_call_site_inside_fresh_bootstrap"] is True
    assert "legacy adoption" in restriction["no_longer_acts_as"]
    assert "health initialization" in restriction["no_longer_acts_as"]
    skew = record["migration_and_skew"]
    assert skew["skew_contract"] == "FORWARD_ONLY_EXPLICIT"
    assert skew["fabricated_v0_lineage"] is False
    assert skew["legacy_adoption_is_not_normal_migration"] is True
    assert skew["ddl_failures_swallowed_before_normal_work"] is False
    assert skew["superseded_migrate_schema_path_deleted"] is True
    coverage = record["barrier_coverage"]
    assert coverage["unexplained_normal_bypass"] == "NONE"


def test_m17_health_identity_and_qc_recorded():
    record = _record()
    correction = record["health_identity_correction"]
    assert "mutating initialization" in correction["before"]
    assert correction["after_health"].startswith("read-only compatibility-aware")
    assert correction["status_names_normative"] is False
    qc = record["qc_archive_gate"]
    assert qc["fresh_bootstrap"] is True and qc["merged_into_primary_authority"] is False
    assert qc["invented_version_lineage"] is False
    orth = record["orthogonality"]
    assert orth["ops_com_003"] == "UNKNOWN (preserved)"
    assert orth["qualification_machinery_introduced"] is False


def test_m17_validation_green_without_attribution():
    record = _record()
    validation = record["validation"]
    assert validation["baseline_at_parent"]["passed"] == 369
    full = validation["full_suite_m17"]
    assert full["passed"] == 409 and full["failed"] == 0 and full["exit_code"] == 0
    assert validation["full_suite_green"] is True
    assert validation["new_m17_tests_passed"] == 40
    assert validation["baseline_attribution_required"] is False
    assert validation["focused_independently_rerun_this_pass"]["passed"] == 69
    assert validation["a_af_source_checks"] == {
        "verified": 32, "total": 32,
        "method": "mechanical read-only inspection of canonical source",
    }
    assert validation["counts_kept_separate"] is True


def test_m17_named_implementation_checks():
    checks = _record()["implementation_checks"]
    expected_yes = {
        "A_explicit_durable_primary_schema_authority_exists",
        "B_expected_version_explicit",
        "C_compatibility_inspection_read_only",
        "D_structural_corroboration_exists",
        "E_fresh_distinguishable_from_legacy_unadopted",
        "H_adoption_requires_explicit_operator_action",
        "I_adoption_verifies_full_structure_first",
        "J_current_compatible_state_performs_normal_work",
        "N_create_all_restricted_to_fresh_bootstrap",
        "O_successful_mutation_adoption_reverified",
        "R_every_normal_db_path_crosses_barrier",
    }
    assert len(checks) == 24
    yes = {k for k, v in checks.items() if v == "YES"}
    no = {k for k, v in checks.items() if v == "NO"}
    assert yes == expected_yes
    assert no == set(checks) - expected_yes
    # the counterfactual wording is what makes these NO: the named bad
    # outcomes did not and cannot happen
    for key in (
        "F_legacy_unadopted_silently_proceeds",
        "G_legacy_unadopted_silently_stamps_itself",
        "K_newer_state_performs_normal_work",
        "M_create_all_runs_during_normal_compatible_startup",
        "P_failed_migration_bootstrap_adoption_can_mark_ready",
        "Q_ddl_failure_silently_swallowed_and_normal_work_continues",
        "S_direct_normal_session_repository_bypass_exists",
        "T_health_mutates_schema",
        "U_identity_mutates_schema",
        "V_dashboard_silently_repairs_adopts_state",
        "W_real_local_db_mutated_by_m17",
        "X_ops_com_003_classification_changed",
    ):
        assert key in no, key


def test_m17_remaining_findings_and_ops_com_003_preserved():
    record = _record()
    assert record["remaining_findings"] == {
        "STD-UI-COM-007": "unresolved",
        "STD-UI-COM-011": "unresolved",
        "STD-DEPLOY-COM-001": "unresolved",
        "STD-OPS-COM-003": "UNKNOWN (preserved)",
    }
    orth = record["orthogonality"]
    assert orth["ops_com_003_closed_by_m17"] is False
    assert orth["ops_com_003_marked_not_applicable"] is False
    assert orth["compatibility_evidence_is_qualification_evidence"] is False


def test_m17_family_names_exactly_ctw_and_smartwatch_inherits_nothing():
    record = _record()
    family = record["family_status"]
    assert family["conclusion"] == FAMILY
    assert family["descriptive_only"] is True
    assert family["is_new_standard"] is False
    assert set(family["members"]) == {"chinese-tech-wire"}
    assert family["members"]["chinese-tech-wire"] == CTW_SHA
    assert family["not_merged_with"] == [
        "ALEMBIC_HEAD", "NUMBERED_SQLITE", "CURRENT_SCHEMA_BOOTSTRAP_SQLITE",
    ]
    for key in (
        "smartwatch_inherits_conformance", "smartwatch_inherits_evidence",
        "smartwatch_inherits_implementation_prescription",
        "smartwatch_needs_legacy_adoption_or_schema_meta_inferred",
    ):
        assert family[key] is False, key


def test_m17_admits_exactly_one_ctw_deployment_fact():
    record = _record()
    admission = record["known_evidence_admission"]
    assert admission["admission_count"] == 1
    assert admission["admitted"] == {
        "subject": "chinese-tech-wire", "revision": CTW_SHA,
        "standard": "STD-DEPLOY-COM-002", "state": "CONFORMS", "lifecycle": "CLOSED",
    }
    assert admission["historical_m1_preserved"] is True
    assert len(admission["prior_admissions_preserved"]) == 6
    for not_admitted in (
        "deploy_com_001_admitted", "ui_com_007_admitted",
        "ui_com_011_admitted", "ops_com_003_admitted",
    ):
        assert admission[not_admitted] is False
    entries = json.loads(KNOWN.read_text(encoding="utf-8"))
    assert entries == build_known_evidence_index()
    ctw = [e for e in entries if e["subject"] == "chinese-tech-wire"]
    assert len(ctw) == 1 and ctw[0]["standard"] == "STD-DEPLOY-COM-002"
    assert CTW_SHA in ctw[0]["summary"]
    assert {e["subject"] for e in entries} == {
        "chinese-tech-wire", "feature-phone-clank", "korean-tech-wire",
        "oem-radar", "semiconductor-intelligence", "tablet-clank", "watch-clank",
        "smartwatch-clank",  # joins at M18 (audits/smartwatch-persistent-state-remediation-m18-2026-09-02.md)
    }


def test_m17_prose_scope_and_no_action_declaration():
    text = " ".join(AUDIT_MD.read_text(encoding="utf-8").split())
    for marker in (
        "CONFORMS / CLOSED", CTW_SHA, CTW_PARENT, STANDARDS_SHA,
        "mutation-as-admission without a durable compatibility authority",
        "LEGACY_UNADOPTED", "byte-identical", FAMILY,
        "--adopt-current-schema", "not bootstrap and not migration",
        "NO CONFORMANCE INHERITANCE, NO EVIDENCE INHERITANCE, NO IMPLEMENTATION PRESCRIPTION",
        "remain unresolved", "UNKNOWN", "No host", "were not changed or moved",
    ):
        assert marker in text, marker
    assert "no overall CTW" in text and "conformance" in text


def test_m17_frozen_deployment_standards_unchanged():
    """Pure-read guard: the frozen standard files still match the
    deployment-standards-v1.0 manifest's LF-normalized hashes (tag-target
    immutability itself is guarded by tests/test_deployment_baseline_v1_0.py)."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["status"] == "FROZEN"
    assert manifest["immutable_tag"] == "deployment-standards-v1.0"
    for artifact in manifest["artifacts"]["standard_files"].values():
        raw = (ROOT / artifact["path"]).read_bytes().replace(b"\r\n", b"\n")
        assert hashlib.sha256(raw).hexdigest() == artifact["sha256_lf_normalized"]


def test_m17_guards_declare_no_target_or_host_action():
    record = _record()
    guards = record["guards"]
    for key in (
        "frozen_standard_files_changed", "frozen_tags_changed_or_moved",
        "ctw_modified_in_this_pass", "smartwatch_modified_in_this_pass",
        "real_ctw_db_adopted_stamped_or_migrated",
        "host_deployment_live_or_production_db_actions", "production_migration",
        "full_target_conformance_claim",
    ):
        assert guards[key] is False, key
