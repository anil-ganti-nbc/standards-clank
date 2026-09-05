"""Narrow Standards guards for the Tablet M28 DEPLOY-COM-001 admission."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.deployment_agent_layer import build_known_evidence_index


ROOT = Path(__file__).resolve().parents[1]
AUDIT_JSON = ROOT / "audits" / "tablet-deployment-proof-m28-2026-09-03.json"
AUDIT_MD = ROOT / "audits" / "tablet-deployment-proof-m28-2026-09-03.md"
KNOWN = ROOT / "standards" / "deployment" / "known-evidence-index.json"
MANIFEST = ROOT / "baselines" / "deployment-standards-v1.0.json"

STANDARDS_SHA = "9f784326b4ec5bfd4327fc4c162d0165f6d73ee7"
TAB_SHA = "b3088ebc716227b99e1d8aa66942c8a6e87bbfcb"
STALE_SHA = "2bd8929459cb44ac840dc0cabcfb7ed91383cf45"
TARGET = "hetzner/ubuntu-4gb-hel1-1:systemd-timer-experimental-dir"
LIVE_PATH = "/home/deploy/experimental/tablet-clank"
BACKUP_SHA = "e3a5c1972925ad5a44889cb2117f507d69060905c06ab6a0ed9915a94381634b"
CANONICAL_FOUR = [
    "honor_cn_tablets_catalogue", "honor_cn_tablets_comparison",
    "tcl_global_tablets", "honor_uk_tablets",
]


def _record() -> dict:
    return json.loads(AUDIT_JSON.read_text(encoding="utf-8"))


def test_m28_records_exact_lineage_target_and_verdict():
    record = _record()
    assert record["standards_clank_head"] == STANDARDS_SHA
    tab = record["tablet"]
    assert tab["head"] == TAB_SHA and tab["origin_main"] == TAB_SHA
    assert tab["modified_in_this_pass"] is False
    assert tab["standard"] == "STD-DEPLOY-COM-001"
    assert tab["state"] == "LIVE_PROOF_CONFIRMED"
    assert tab["lifecycle"] == "CLOSED"
    assert tab["deployment_target"] == TARGET
    assert record["verdict"]["revision"] == TAB_SHA
    assert record["verdict"]["deployment_target"] == TARGET
    for not_implied in (
        "generalizes_to_other_targets", "generalizes_to_future_revisions",
        "implies_all_tablet_deployments_conform", "implies_opt_examples_correct",
        "implies_immutable_artifact_identity",
        "implies_revision_env_meaningful_on_this_lane",
        "implies_ui_com_011_closed", "implies_full_target_conformance",
    ):
        assert record["verdict"][not_implied] is False


def test_m28_stale_v1_history_preserved_and_not_mislabelled():
    record = _record()
    stale = record["pre_m27_stale_history"]
    assert stale["live_source"] == STALE_SHA
    assert stale["commits_behind_canonical"] == 10
    assert stale["schema"] == "v1"
    assert stale["historical_runs"] == 159
    assert stale["qualification_tables"] is False
    assert stale["provenance_column"] is False
    assert stale["production_scope_sources"] == 3
    assert stale["honor_uk_tablets_absent"] is True
    assert stale["predated"] == [
        "OPS-COM-003 remediation", "OPS-COM-004 remediation",
        "M13 COM-002 remediation",
    ]
    assert stale["code_state_pair"] == "internally coherent"
    assert stale["classification"] == "STALE_CONTENT_CONSISTENT"
    assert stale["mislabelled_claim_made"] is False
    assert record["guards"]["old_deployment_described_as_mislabelled"] is False
    assert record["guards"]["historical_evidence_rewritten"] is False


def test_m28_identity_model_is_venv_chain_without_revision_env():
    record = _record()
    identity = record["identity_model"]
    assert identity["oci_container_chain"] is False
    assert identity["immutable_artifact_identity_claimed"] is False
    assert identity["identity_chain"][0] == f"canonical Git checkout SHA {TAB_SHA}"
    assert identity["identity_chain"][-1] == "natural production execution"
    assert identity["revision_env_used"] is False
    assert identity["revision_env_deliberately_not_added"] is True
    assert identity["limitation_recorded_honestly"] is True
    assert LIVE_PATH in " ".join(identity["identity_chain"])
    probes = record["canonical_content_probes"]
    assert probes["schema_version_v3"] is True
    assert probes["production_allowlist_count"] == 4
    assert probes["honor_uk_tablets_included"] is True
    assert probes["canonical_production_cli_path"] is True


def test_m28_backup_migration_and_compatibility():
    record = _record()
    state = record["persistent_state"]
    assert state["backup_sha256"] == BACKUP_SHA
    assert state["backup_size_bytes"] == 11071488
    assert state["canonical_classification"] == "MIGRATION_REQUIRED"
    assert state["canonical_migration"] == "v1 -> v3 using Database()"
    assert state["post_migrations"] == [1, 2, 3]
    assert state["post_state"] == "COMPATIBLE"
    assert state["integrity"] == "OK"
    assert state["historical_data_preserved"] is True
    assert state["old_v1_rows"] == "left UNKNOWN, not rewritten"
    assert state["com_002_re_ratified_here"] is False


def test_m28_systemd_mechanism_and_natural_execution():
    record = _record()
    mechanism = record["deployment_mechanism"]
    assert mechanism["model"] == "systemd timer + oneshot venv execution (non-Docker)"
    assert mechanism["timer"] == "tablet-clank-production.timer (enabled)"
    assert mechanism["on_calendar_utc"] == ["06:20", "18:20"]
    assert mechanism["randomized_delay_sec"] == 90
    assert mechanism["exec_start"].startswith(f"{LIVE_PATH}/.venv/bin/python")
    assert mechanism["resident_service_required"] is False
    proof = record["natural_timer_proof"]
    assert proof["fired_at_utc"] == "2026-09-02T18:20:54Z"
    assert proof["naturally_timer_fired"] is True
    assert proof["manual_test_run"] is False
    assert proof["exit_code"] == 0 and proof["result"] == "success"
    assert proof["pid"] == 1557855
    assert proof["runs"] == "160-163"


def test_m28_durable_scheduled_provenance_and_lock_chain():
    record = _record()
    provenance = record["durable_provenance"]
    assert provenance["runs"] == ["160", "161", "162", "163"]
    assert provenance["execution_provenance"] == "SCHEDULED"
    assert provenance["authority"].startswith("durable DB record")
    assert provenance["historical_v1_rows"] == "remain UNKNOWN, not rewritten"
    lock = record["ops_com_004_live_path"]
    assert lock["source_level_closure_preserved"] is True
    assert lock["re_admitted_here"] is False
    assert lock["chain"] == [
        "systemd ExecStart", "canonical Tablet production CLI", "SoakLock",
        "OS advisory lock acquisition",
    ]
    assert lock["natural_service_pid"] == 1557855
    assert lock["lock_authority"] == "os_advisory_lock"
    assert lock["post_run_lock_inspect"] == "stale (diagnostic only)"
    assert lock["pid_is_authority"] is False
    assert lock["kernel_tracing_claimed"] is False
    assert record["guards"]["kernel_tracing_claimed"] is False


def test_m28_dep_inc_009_scope_drift_closed_by_live_execution():
    record = _record()
    drift = record["dep_inc_009_scope_drift_closure"]
    assert drift["m26_live_scope_sources"] == 3
    assert drift["canonical_intended_sources"] == 4
    assert drift["canonical_four"] == CANONICAL_FOUR
    assert drift["m27_natural_cycle_executed_all_four"] is True
    assert drift["classification"] == "PRODUCTION_ALLOWLIST_DRIFT_CLOSED"
    assert drift["closure_evidence"].startswith("live natural execution")
    assert drift["honor_uk_evidence"] == {
        "run": 162, "status": "SUCCESS", "accepted": 25, "new": 2,
    }


def test_m28_qualification_recorded_without_overstatement():
    record = _record()
    qual = record["qualification_evidence"]
    assert qual["new_canonical_scopes_epochs_terminals"] == 4
    assert qual["provenance"] == "SCHEDULED"
    assert qual["first_canonical_scheduled_epochs"] == (
        "expected NOT_QUALIFIED state where applicable"
    )
    assert qual["historical_v1_evidence_rewritten"] is False
    assert qual["qualification_status_overstated"] is False
    ops = record["operational_result"]
    assert ops["cycle_result"] == "SUCCESS"
    assert ops["db"] == "v3 / COMPATIBLE"
    assert ops["timer_still_enabled"] is True
    assert ops["checkout_still_exact"] == TAB_SHA
    assert ops["production_sources_executed"] == 4
    assert ops["rollback_observed"] is False


def test_m28_path_debt_remains_open():
    record = _record()
    debt = record["path_debt"]
    assert debt["classification"] == "TRACKED_DEPLOYMENT_PATH_DESCRIPTION_STALE"
    assert debt["tracked_examples_path"] == "/opt/tablet-clank"
    assert debt["live_production_path"] == LIVE_PATH
    assert debt["m27_classification"] == "NON_MATERIAL_PATH_VARIANCE"
    assert debt["examples_claimed_correct"] is False
    assert debt["modified_in_this_pass"] is False
    assert debt["admission_does_not_bless"] == [
        "arbitrary paths", "example currency", "future revisions/targets",
    ]


def test_m28_all_material_evidence_obligations_supported():
    record = _record()
    review = record["evidence_review"]
    yes_keys = [k for k in review if k != "unsupported_material_obligations"]
    assert len(yes_keys) == 16
    assert all(review[k] is True for k in yes_keys)
    assert review["unsupported_material_obligations"] == []


def test_m28_remaining_findings_and_no_full_conformance():
    record = _record()
    remaining = record["remaining_tablet_findings"]
    assert remaining["STD-OPS-COM-003"] == "CLOSED (preserved)"
    assert remaining["STD-OPS-COM-004"] == "CLOSED (preserved)"
    assert remaining["STD-DEPLOY-COM-002"] == "CLOSED at M13 (preserved)"
    assert remaining["STD-UI-COM-011"] == "unresolved"
    assert remaining["fully_conforming_claimed_here"] is False
    non = record["non_inheritance"]
    assert non["no_other_target_inherits_this_proof"] is True
    assert non["tablet_com_002_fact_preserved"] is True
    assert non["watch_smartwatch_feature_phone_com_001_facts_preserved"] is True


def test_m28_admits_exactly_one_tablet_com001_fact():
    record = _record()
    admission = record["known_evidence_admission"]
    assert admission["admission_count"] == 1
    assert admission["admitted"] == {
        "subject": "tablet-clank", "revision": TAB_SHA,
        "standard": "STD-DEPLOY-COM-001", "deployment_target": TARGET,
        "state": "LIVE_PROOF_CONFIRMED", "lifecycle": "CLOSED",
    }
    assert admission["deployment_facts_after_admission"] == 11
    entries = json.loads(KNOWN.read_text(encoding="utf-8"))
    assert entries == build_known_evidence_index()
    assert len(entries) == 14
    tab = [e for e in entries if e["subject"] == "tablet-clank"]
    assert len(tab) == 2
    by_standard = {e["standard"]: e for e in tab}
    assert by_standard["STD-DEPLOY-COM-002"]["source_reference"] == (
        "audits/tablet-persistent-state-remediation-m13-2026-09-02.md"
    )
    com001 = by_standard["STD-DEPLOY-COM-001"]
    assert com001["source_reference"] == (
        "audits/tablet-deployment-proof-m28-2026-09-03.md"
    )
    assert "LIVE_PROOF_CONFIRMED" in com001["summary"]
    assert TAB_SHA in com001["summary"] and TARGET in com001["summary"]
    # prior live-proof facts remain exactly once each
    for subject, sha in (
        ("watch-clank", "d03bc4b2f90289686331af0447d5ca4e8cf55822"),
        ("smartwatch-clank", "a93355480bb11e1bd16ae7837256ce9002fc2aa7"),
        ("feature-phone-clank", "b60e881319b16d36625268d9ba2d66cb8ea8f818"),
    ):
        fact = [e for e in entries
                if e["subject"] == subject and e["standard"] == "STD-DEPLOY-COM-001"]
        assert len(fact) == 1 and sha in fact[0]["summary"]


def test_m28_prose_preserves_history_debt_and_no_action_declaration():
    text = " ".join(AUDIT_MD.read_text(encoding="utf-8").split())
    for marker in (
        "LIVE_PROOF_CONFIRMED", TAB_SHA, TARGET, STANDARDS_SHA, STALE_SHA,
        "STALE_CONTENT_CONSISTENT", "not", "described as mislabelled",
        "10 commits behind", "159 historical runs", BACKUP_SHA,
        "v1 → v3", "COMPATIBLE", "NON_MATERIAL_PATH_VARIANCE",
        "TRACKED_DEPLOYMENT_PATH_DESCRIPTION_STALE", "/opt/tablet-clank",
        LIVE_PATH, "os_advisory_lock", "1557855", "2026-09-02 18:20:54 UTC",
        "160–163", "SCHEDULED", "PRODUCTION_ALLOWLIST_DRIFT_CLOSED",
        "run 162", "NOT_QUALIFIED", "STD-UI-COM-011",
        "No-action declaration", "were not changed or moved",
    ):
        assert marker in text, marker


def test_m28_frozen_deployment_standards_unchanged():
    """Pure-read guard: the frozen standard files still match the
    deployment-standards-v1.0 manifest's LF-normalized hashes (tag-target
    immutability itself is guarded by tests/test_deployment_baseline_v1_0.py)."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["status"] == "FROZEN"
    assert manifest["immutable_tag"] == "deployment-standards-v1.0"
    for artifact in manifest["artifacts"]["standard_files"].values():
        raw = (ROOT / artifact["path"]).read_bytes().replace(b"\r\n", b"\n")
        assert hashlib.sha256(raw).hexdigest() == artifact["sha256_lf_normalized"]


def test_m28_guards_declare_no_host_or_target_action():
    record = _record()
    guards = record["guards"]
    for key in (
        "frozen_standard_files_changed", "frozen_tags_changed_or_moved",
        "tablet_modified_in_this_pass", "host_access_or_mutation_in_this_pass",
        "deploy_restart_unit_timer_db_or_collector_action_in_this_pass",
        "historical_evidence_rewritten", "old_deployment_described_as_mislabelled",
        "kernel_tracing_claimed", "full_target_conformance_claim",
    ):
        assert guards[key] is False, key
