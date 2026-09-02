"""Narrow Standards guards for the Smartwatch M18 Deployment evidence record."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.deployment_agent_layer import build_known_evidence_index


ROOT = Path(__file__).resolve().parents[1]
AUDIT_JSON = ROOT / "audits" / "smartwatch-persistent-state-remediation-m18-2026-09-02.json"
AUDIT_MD = ROOT / "audits" / "smartwatch-persistent-state-remediation-m18-2026-09-02.md"
KNOWN = ROOT / "standards" / "deployment" / "known-evidence-index.json"
MANIFEST = ROOT / "baselines" / "deployment-standards-v1.0.json"

STANDARDS_SHA = "40ed95c44f1402a88be66260402d1b2c53475394"
SW_PARENT = "a631421e276b58ce3499787cc2bc72218648ce72"
SW_SHA = "a93355480bb11e1bd16ae7837256ce9002fc2aa7"
FAMILY = "FIRST_VALIDATED_MEMBER_OF_ADDITIVE_SCHEMA_MARKER_COMPATIBILITY"


def _record() -> dict:
    return json.loads(AUDIT_JSON.read_text(encoding="utf-8"))


def test_m18_records_exact_lineage_and_narrow_verdict():
    record = _record()
    assert record["standards_clank_head"] == STANDARDS_SHA
    target = record["smartwatch"]
    assert target["head"] == SW_SHA
    assert target["origin_main"] == SW_SHA
    assert target["parent"] == SW_PARENT
    assert target["standard"] == "STD-DEPLOY-COM-002"
    assert target["state"] == "CONFORMS"
    assert target["lifecycle"] == "CLOSED"
    assert target["scope"] == "source-level persistent-state compatibility only"
    assert record["verdict"]["revision"] == SW_SHA
    for not_implied in (
        "implies_live_deployed_compatibility",
        "implies_production_db_compatibility",
        "implies_deploy_com_001_closure",
        "implies_full_target_conformance",
    ):
        assert record["verdict"][not_implied] is False


def test_m18_preserves_marker_without_barrier_defect_and_m1_lineage():
    record = _record()
    defect = record["original_defect"]
    assert defect["summary"] == (
        "marker-without-admission-barrier + mutation-before-compatibility"
    )
    # the defect must NOT be reduced to "Smartwatch had no marker"
    assert defect["not_reduced_to"] == "Smartwatch had no schema marker"
    assert defect["details"] == [
        "schema_version existed as a durable monotonic authority",
        "_migrate() ran unconditionally on read-write construction",
        "full schema executescript/additive ALTER logic could mutate before "
        "compatibility classification",
        "schema_version was monotonic and only advanced upward",
        "older code encountering newer state left the newer marker untouched "
        "and proceeded",
        "missing-marker state could be treated like fresh/upgradeable state",
        "no explicit fail-closed version comparison existed",
    ]
    assert record["source_lineage"]["m1_head"] == SW_PARENT
    assert record["source_lineage"]["m1_deploy_com_002"] == "INSUFFICIENT_EVIDENCE"
    assert record["source_lineage"]["m1_preserved"] is True
    assert record["source_lineage"]["m5_ops_com_003_closed_at_parent"] is True
    assert record["m10"]["classification"] == "PARTIAL_MECHANISM"
    assert record["m10"]["risk"] == "HIGH"
    assert record["m10"]["applicability"] == "APPLIES"
    assert record["m10"]["explicit_version_comparison"] is False


def test_m18_authority_is_retained_marker_plus_structure():
    record = _record()
    authority = record["schema_authority"]
    assert authority["marker"] == "schema_version"
    assert authority["expected_version"] == 3
    assert authority["durable"] is True and authority["monotonic"] is True
    assert authority["existing_mechanism_retained_not_replaced"] is True
    assert authority["marker_alone_insufficient"] is True
    corr = record["structural_corroboration"]
    assert "17-table expected contract" in " ".join(corr["verified"])
    assert "complete expected runs column set" in " ".join(corr["verified"])
    # honest limits: nothing the source does not check is claimed
    for not_claimed in (
        "column type equivalence", "nullability/constraint equivalence",
        "index equivalence", "byte-for-byte DDL fingerprint",
    ):
        assert not_claimed in " ".join(corr["not_claimed"])


def test_m18_historical_pre_marker_is_narrow_and_distinct_from_unknown():
    record = _record()
    hist = record["historical_pre_marker_generation"]
    assert hist["source_proven"] is True
    assert hist["classification"] == "MIGRATION_REQUIRED"
    assert hist["not"] == ["FRESH", "UNKNOWN", "COMPATIBLE"]
    assert hist["recognition"].startswith("structural and narrow")
    assert hist["arbitrary_marker_less_db"].startswith("does NOT qualify")
    assert hist["migration_path"] == "canonical additive _migrate() only"
    assert hist["reverification_after_migration"] is True
    assert hist["not_silent_grandfathering"] is True
    assert hist["not_generic_marker_less_adoption"] is True
    assert hist["not_ctw_legacy_unadopted_terminology"] is True
    fresh = record["fresh_vs_unknown"]
    assert fresh["distinct_states_preserved"] is True
    assert fresh["UNKNOWN"].startswith("existing marker-less state")
    model = record["compatibility_model"]
    assert model["states"] == [
        "FRESH", "MIGRATION_REQUIRED", "COMPATIBLE", "INCOMPATIBLE_NEWER",
        "UNKNOWN", "CORRUPT", "PARTIAL",
    ]
    assert "FRESH != UNKNOWN" in model["semantics"]
    assert "MARKER_PRESENT != COMPATIBLE" in model["semantics"]
    assert "DB_OPENED != COMPATIBLE" in model["semantics"]
    assert model["state_names_fleet_normative"] is False


def test_m18_ordering_migration_and_skew_recorded():
    record = _record()
    ro = record["read_only_first_ordering"]
    assert ro["inspection_before_read_write_open"] is True
    assert ro["compatible_open_zero_schema_writes"] is True
    assert set(ro["mutating_operations_after_inspection"]) == {
        "executescript", "CREATE TABLE", "ALTER TABLE", "marker writes",
        "migrations",
    }
    assert ro["filesystem_guarantee_overclaim"] is False
    migration = record["migration_semantics"]
    assert migration["canonical_migrate_authoritative"] is True
    assert migration["may_enter"] == ["FRESH", "recognized MIGRATION_REQUIRED"]
    assert migration["never_runs_on"] == [
        "COMPATIBLE", "UNKNOWN", "INCOMPATIBLE_NEWER", "CORRUPT", "PARTIAL",
    ]
    assert migration["reverified_after"] is True
    assert migration["failed_migration_marks_ready"] is False
    assert migration["fabricated_lineage"] is False
    skew = record["version_skew"]
    assert skew["posture"] == "FORWARD_ONLY_EXPLICIT"
    assert skew["downgrade_claimed"] is False
    assert skew["sqlite_orm_tolerance_is_not_compatibility"] is True
    coverage = record["barrier_coverage"]
    assert coverage["unexplained_normal_bypass"] == "NONE"


def test_m18_entry_points_classified_and_qc_narrow():
    record = _record()
    coverage = record["barrier_coverage"]
    assert "store barrier" in coverage["cli_run"]
    assert coverage["scheduler_and_soak_runner"].endswith("same CLI barrier")
    assert coverage["backup"].startswith("read-only mode=ro construction")
    assert coverage["direct_store_constructors"].endswith(
        "no writable path bypasses _admit_compatibility"
    )
    health = record["health_status"]
    assert health["read_only"] is True and health["cannot_migrate"] is True
    assert health["cannot_repair"] is True
    qc = record["qc_archive"]
    assert qc["fresh_bootstrap_canonical"] is True
    assert qc["invented_version_lineage"] is False
    assert qc["numbered_migration_lineage"] is False
    assert qc["shared_schema_version_authority"] is False
    orth = record["qualification_orthogonality"]
    assert orth["ops_com_003"].startswith("CONFORMS / CLOSED at M5")
    assert orth["qualification_provenance_proves_compatibility"] is False
    assert orth["qualification_epoch_or_gate_can_bypass_admission"] is False
    assert orth["provenance_semantics_intact"] == ["SCHEDULED", "MANUAL", "UNKNOWN"]


def test_m18_validation_non_green_with_baseline_attribution():
    record = _record()
    validation = record["validation"]
    reported = validation["reported_by_m18_remediation_pass"]
    assert reported["baseline_at_parent"]["total"] == 251
    assert reported["baseline_at_parent"]["passed"] == 248
    assert reported["full_suite_m18"]["total"] == 276
    assert reported["full_suite_m18"]["passed"] == 273
    assert reported["full_suite_m18"]["exit_code"] == 1
    rerun = validation["independent_rerun_this_pass"]
    assert rerun["baseline_at_parent"]["collected"] == 246
    assert rerun["full_suite_m18"]["collected"] == 268
    assert rerun["full_suite_m18"]["exit_code"] == 1
    assert rerun["new_m18_tests_passed"] == 22
    assert validation["same_two_failures_at_baseline_and_m18"] is True
    assert validation["failing_tests"] == [
        "tests/test_specialist_collectors.py::test_tier_and_name",
        "tests/test_specialist_collectors.py::"
        "test_specialist_joins_experimental_scope_not_production",
    ]
    assert validation["classification"] == "PRE_EXISTING / BASELINE_ATTRIBUTED"
    assert validation["full_suite_green"] is False
    assert validation["full_suite_claim"] == (
        "NON_GREEN_FULL_SUITE; collected totals must never be read as all passed"
    )
    assert validation["new_m18_regression_introduced"] is False
    assert validation["counts_kept_separate"] is True
    assert "total_count_discrepancy" in validation


def test_m18_named_implementation_checks():
    checks = _record()["implementation_checks"]
    expected_yes = {
        "A_expected_schema_version_explicit",
        "B_compatibility_inspection_read_only",
        "C_fresh_distinguishable_from_unknown",
        "I_marker_sufficiently_corroborated_against_structure",
        "J_canonical_migration_authoritative",
        "K_migration_reverified",
        "M_every_normal_db_path_guarded",
        "R_normal_v3_behavior_intact",
        "S_ops_com_003_remains_intact",
    }
    assert len(checks) == 19
    yes = {k for k, v in checks.items() if v == "YES"}
    no = {k for k, v in checks.items() if v == "NO"}
    assert yes == expected_yes
    assert no == set(checks) - expected_yes
    for key in (
        "D_unknown_silently_proceeds",
        "E_old_unmigrated_state_performs_normal_work",
        "F_newer_incompatible_state_performs_normal_work",
        "G_missing_authority_existing_state_silently_bootstraps",
        "H_corrupt_partial_state_performs_normal_work",
        "L_failed_migration_can_mark_ready",
        "N_direct_normal_consumer_bypass_exists",
        "O_qualification_can_bypass_compatibility",
        "P_health_dashboard_silently_repair_incompatible_state",
        "Q_old_software_silently_accepts_newer_state",
    ):
        assert key in no, key


def test_m18_remaining_findings_and_no_full_conformance():
    record = _record()
    assert record["remaining_findings"] == {
        "STD-UI-COM-011": "unresolved",
        "STD-DEPLOY-COM-001": "unresolved",
        "STD-OPS-COM-003": "CONFORMS / CLOSED at M5 (preserved, not re-ratified)",
    }
    assert record["verdict"]["implies_full_target_conformance"] is False


def test_m18_family_names_exactly_smartwatch_and_no_inheritance():
    record = _record()
    family = record["family_status"]
    assert family["conclusion"] == FAMILY
    assert family["descriptive_only"] is True
    assert family["is_new_standard"] is False
    assert set(family["members"]) == {"smartwatch-clank"}
    assert family["members"]["smartwatch-clank"] == SW_SHA
    assert family["not_merged_with"] == [
        "ALEMBIC_HEAD", "NUMBERED_SQLITE", "CURRENT_SCHEMA_BOOTSTRAP",
        "CREATE_ALL_WITH_EXPLICIT_AUTHORITY",
    ]
    non_inheritance = record["non_inheritance"]
    for target in ("watch-clank", "oem-radar", "chinese-tech-wire"):
        assert non_inheritance[target] == {
            "com_002_evidence_inheritance": False,
            "implementation_inheritance": False,
        }
    assert non_inheritance["other_targets_inherit_smartwatch_conformance"] is False


def test_m18_admits_exactly_one_smartwatch_deployment_fact():
    record = _record()
    admission = record["known_evidence_admission"]
    assert admission["admission_count"] == 1
    assert admission["admitted"] == {
        "subject": "smartwatch-clank", "revision": SW_SHA,
        "standard": "STD-DEPLOY-COM-002", "state": "CONFORMS", "lifecycle": "CLOSED",
    }
    assert admission["deployment_facts_after_admission"] == 8
    assert admission["historical_m1_preserved"] is True
    assert len(admission["prior_admissions_preserved"]) == 7
    for not_admitted in (
        "deploy_com_001_admitted", "ui_com_011_admitted",
        "additional_ops_com_003_fact_admitted",
    ):
        assert admission[not_admitted] is False
    entries = json.loads(KNOWN.read_text(encoding="utf-8"))
    assert entries == build_known_evidence_index()
    sw = [e for e in entries if e["subject"] == "smartwatch-clank"
          and e["standard"] == "STD-DEPLOY-COM-002"]
    assert len(sw) == 1
    assert SW_SHA in sw[0]["summary"]
    assert {e["subject"] for e in entries} == {
        "smartwatch-clank", "chinese-tech-wire", "feature-phone-clank",
        "korean-tech-wire", "oem-radar", "semiconductor-intelligence",
        "tablet-clank", "watch-clank",
    }
    # smartwatch-clank (M22/M18), feature-phone-clank (M25/M14), and
    # tablet-clank (M28/M13) each carry two Deployment facts
    assert len(entries) == 11


def test_m18_prose_scope_and_no_action_declaration():
    text = " ".join(AUDIT_MD.read_text(encoding="utf-8").split())
    for marker in (
        "CONFORMS / CLOSED", SW_SHA, SW_PARENT, STANDARDS_SHA,
        "marker-without-admission-barrier plus mutation-before-compatibility",
        "MIGRATION_REQUIRED", "UNKNOWN", FAMILY,
        "FORWARD_ONLY_EXPLICIT", "17-table contract", "byte-identical",
        "NO SMARTWATCH COM-002 EVIDENCE INHERITANCE, NO IMPLEMENTATION",
        "NOT green", "PRE_EXISTING / BASELINE_ATTRIBUTED",
        "remain unresolved", "No host", "were not changed or moved",
        "not re-ratified", "NON_GREEN_FULL_SUITE",
    ):
        assert marker in text, marker
    assert "no overall Smartwatch" in text and "conformance" in text


def test_m18_frozen_deployment_standards_unchanged():
    """Pure-read guard: the frozen standard files still match the
    deployment-standards-v1.0 manifest's LF-normalized hashes (tag-target
    immutability itself is guarded by tests/test_deployment_baseline_v1_0.py)."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["status"] == "FROZEN"
    assert manifest["immutable_tag"] == "deployment-standards-v1.0"
    for artifact in manifest["artifacts"]["standard_files"].values():
        raw = (ROOT / artifact["path"]).read_bytes().replace(b"\r\n", b"\n")
        assert hashlib.sha256(raw).hexdigest() == artifact["sha256_lf_normalized"]


def test_m18_guards_declare_no_target_or_host_action():
    record = _record()
    guards = record["guards"]
    for key in (
        "frozen_standard_files_changed", "frozen_tags_changed_or_moved",
        "smartwatch_modified_in_this_pass",
        "host_deployment_live_or_production_db_actions", "production_migration",
        "full_target_conformance_claim",
    ):
        assert guards[key] is False, key
    assert guards["historical_pre_marker_represented_distinctly_from_unknown"] is True
