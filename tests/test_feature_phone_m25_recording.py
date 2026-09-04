"""Narrow Standards guards for the Feature Phone M25 DEPLOY-COM-001 admission."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.deployment_agent_layer import build_known_evidence_index


ROOT = Path(__file__).resolve().parents[1]
AUDIT_JSON = ROOT / "audits" / "feature-phone-deployment-proof-m25-2026-09-02.json"
AUDIT_MD = ROOT / "audits" / "feature-phone-deployment-proof-m25-2026-09-02.md"
KNOWN = ROOT / "standards" / "deployment" / "known-evidence-index.json"
MANIFEST = ROOT / "baselines" / "deployment-standards-v1.0.json"

STANDARDS_SHA = "760b2949acd0a6c742ca91e370d99647d4a8c200"
FP_SHA = "b60e881319b16d36625268d9ba2d66cb8ea8f818"
STALE_SHA = "303e42ff56c6929e603a85316023c16de039e6f9"
TARGET = "hetzner/ubuntu-4gb-hel1-1:cron-docker-compose-staging"
COLLECTORS = [
    "hmd-nokia", "punkt-ch", "doro-gb", "mudita-com", "sunbeam-f1-us",
    "tcl-alcatel-global",
]


def _record() -> dict:
    return json.loads(AUDIT_JSON.read_text(encoding="utf-8"))


def test_m25_records_exact_lineage_target_and_verdict():
    record = _record()
    assert record["standards_clank_head"] == STANDARDS_SHA
    fp = record["feature_phone"]
    assert fp["head"] == FP_SHA and fp["origin_main"] == FP_SHA
    assert fp["modified_in_this_pass"] is False
    assert fp["standard"] == "STD-DEPLOY-COM-001"
    assert fp["state"] == "LIVE_PROOF_CONFIRMED"
    assert fp["lifecycle"] == "CLOSED"
    assert fp["deployment_target"] == TARGET
    assert record["verdict"]["revision"] == FP_SHA
    assert record["verdict"]["deployment_target"] == TARGET
    assert record["verdict"]["generalizes_to_other_targets"] is False
    assert record["verdict"]["generalizes_to_future_revisions"] is False
    assert record["verdict"]["blesses_documented_windows_deployment"] is False


def test_m25_stale_v4_history_preserved_and_not_mislabelled():
    record = _record()
    stale = record["pre_m24_defect_history"]
    assert stale["live_selector_revision"] == STALE_SHA
    assert stale["stale_classification"] == "STALE_CONTENT_CONSISTENT"
    assert stale["mislabelled_claim_made"] is False
    assert stale["live_pair_coherently_v4"] is True
    assert stale["predecessor_predated"] == [
        "OPS-COM-003 remediation", "OPS-COM-004 remediation",
        "M14 COM-002 remediation",
    ]
    assert stale["tracked_docs_claimed_windows_task_scheduler_production"] is True
    assert stale["windows_task_disabled"] is True
    assert stale["windows_target_checkout_absent"] is True
    assert stale["actual_production_hetzner_cron_compose"] is True
    assert stale["actual_host_wrapper_untracked"] is True
    assert record["guards"]["old_artifact_described_as_mislabelled"] is False
    assert record["guards"]["historical_evidence_rewritten"] is False


def test_m25_canonical_deployment_and_persistent_state():
    record = _record()
    evidence = record["canonical_deployment_evidence"]
    assert evidence["deployed_source"] == FP_SHA
    assert evidence["production_scope_collectors"] == COLLECTORS
    assert evidence["production_scope_count_verified_against_tracked_config"] == 6
    assert evidence["experimental_sources_part_of_production_success"] is False
    state = record["persistent_state"]
    assert state["canonical_classification"] == "MIGRATION_REQUIRED"
    assert state["canonical_migration"] == (
        "v4 -> v5 via M14 read-only-first barrier and canonical path"
    )
    assert state["post_schema"] == 5
    assert state["post_state"] == "COMPATIBLE"
    assert state["integrity"] == "OK"
    assert state["com_002_re_ratified_here"] is False
    mechanism = record["deployment_mechanism"]
    assert mechanism["model"] == "Hetzner cron + Docker Compose one-shot"
    assert mechanism["host_wrapper_untracked"] is True
    assert mechanism["wrapper_tracked_source"] is None
    assert mechanism["natural_production_cron_fire_utc"] == "13:15Z"


def test_m25_ops_com_004_live_path_recorded_narrowly():
    record = _record()
    lock = record["ops_com_004_live_path"]
    assert lock["source_level_closure_preserved"] is True
    assert lock["re_admitted_here"] is False
    assert lock["deployment_relevant_fact"].startswith(
        "actual production execution path used the canonical grant-backed OS "
        "advisory lock path"
    )
    assert lock["lock_mechanism"].startswith("core/run_lock.py fcntl.flock")
    assert lock["pid_metadata_treated_as_authority"] is False


def test_m25_natural_scheduled_provenance_evidence():
    record = _record()
    proof = record["scheduler_provenance_proof"]
    assert proof["natural_cron_fire_utc"] == "13:15Z"
    assert proof["artifact_selected"] == FP_SHA
    assert proof["durable_source_revision"] == FP_SHA
    assert proof["execution_provenance"] == "SCHEDULED"
    assert proof["provenance_source"] == (
        "durable application record (not inferred from crontab presence)"
    )
    assert proof["collector_outcome"] == "all production collectors succeeded"


def test_m25_deployment_mechanism_gap_remains_open_debt():
    record = _record()
    gap = record["deployment_mechanism_gap"]
    assert gap["classification"] == "TRACKED_DEPLOYMENT_DESCRIPTION_STALE"
    assert gap["tracked_readme_still_describes_windows_lane_as_production"] is True
    assert gap["windows_task_still_disabled"] is True
    assert gap["windows_target_checkout_still_absent"] is True
    assert gap["host_wrapper_still_untracked"] is True
    assert gap["fixed_in_this_pass"] is False
    assert gap["feature_phone_docs_or_source_modified_in_this_pass"] is False
    assert gap["admission_does_not_bless"] == [
        "documented Windows deployment", "arbitrary host wrappers",
        "future revisions", "deployment documentation correctness",
    ]
    assert record["guards"]["deployment_doc_gap_claimed_fixed"] is False


def test_m25_all_material_evidence_obligations_supported():
    record = _record()
    review = record["evidence_review"]
    yes_keys = [k for k in review if k != "unsupported_material_obligations"]
    assert len(yes_keys) == 14
    assert all(review[k] is True for k in yes_keys)
    assert review["unsupported_material_obligations"] == []


def test_m25_remaining_findings_and_no_full_conformance():
    record = _record()
    remaining = record["remaining_feature_phone_findings"]
    assert remaining["STD-OPS-COM-003"] == "CLOSED (preserved)"
    assert remaining["STD-OPS-COM-004"] == "CLOSED (preserved)"
    assert remaining["STD-DEPLOY-COM-002"] == "CLOSED at M14 (preserved)"
    assert remaining["STD-UI-COM-011"] == "unresolved"
    assert remaining["fully_conforming_claimed_here"] is False
    non = record["non_inheritance"]
    assert non["no_other_target_inherits_this_proof"] is True
    assert non["feature_phone_com_002_fact_preserved"] is True
    assert non["smartwatch_com_001_and_com_002_facts_preserved"] is True
    assert non["watch_com_001_fact_preserved"] is True


def test_m25_admits_exactly_one_feature_phone_com001_fact():
    record = _record()
    admission = record["known_evidence_admission"]
    assert admission["admission_count"] == 1
    assert admission["admitted"] == {
        "subject": "feature-phone-clank", "revision": FP_SHA,
        "standard": "STD-DEPLOY-COM-001", "deployment_target": TARGET,
        "state": "LIVE_PROOF_CONFIRMED", "lifecycle": "CLOSED",
    }
    assert admission["deployment_facts_after_admission"] == 10
    entries = json.loads(KNOWN.read_text(encoding="utf-8"))
    assert entries == build_known_evidence_index()
    assert len(entries) == 12
    fp = [e for e in entries if e["subject"] == "feature-phone-clank"]
    assert len(fp) == 2
    by_standard = {e["standard"]: e for e in fp}
    assert by_standard["STD-DEPLOY-COM-002"]["source_reference"] == (
        "audits/feature-phone-persistent-state-remediation-m14-2026-09-02.md"
    )
    com001 = by_standard["STD-DEPLOY-COM-001"]
    assert com001["source_reference"] == (
        "audits/feature-phone-deployment-proof-m25-2026-09-02.md"
    )
    assert "LIVE_PROOF_CONFIRMED" in com001["summary"]
    assert FP_SHA in com001["summary"] and TARGET in com001["summary"]
    # prior live-proof facts remain: Watch COM-001 and Smartwatch COM-001
    for subject, sha in (
        ("watch-clank", "d03bc4b2f90289686331af0447d5ca4e8cf55822"),
        ("smartwatch-clank", "a93355480bb11e1bd16ae7837256ce9002fc2aa7"),
    ):
        fact = [e for e in entries
                if e["subject"] == subject and e["standard"] == "STD-DEPLOY-COM-001"]
        assert len(fact) == 1 and sha in fact[0]["summary"]


def test_m25_prose_preserves_history_gap_and_no_action_declaration():
    text = " ".join(AUDIT_MD.read_text(encoding="utf-8").split())
    for marker in (
        "LIVE_PROOF_CONFIRMED", FP_SHA, TARGET, STANDARDS_SHA, STALE_SHA,
        "STALE_CONTENT_CONSISTENT", "not a provenance lie", "staleness",
        "TRACKED_DEPLOYMENT_DESCRIPTION_STALE", "13:15Z", "SCHEDULED",
        "v4 -> v5", "COMPATIBLE", "os_advisory_lock",
        "untracked", "remains disabled", "operational debt",
        "STD-UI-COM-011", "No-action declaration", "were not changed or moved",
    ):
        assert marker in text, marker


def test_m25_frozen_deployment_standards_unchanged():
    """Pure-read guard: the frozen standard files still match the
    deployment-standards-v1.0 manifest's LF-normalized hashes (tag-target
    immutability itself is guarded by tests/test_deployment_baseline_v1_0.py)."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["status"] == "FROZEN"
    assert manifest["immutable_tag"] == "deployment-standards-v1.0"
    for artifact in manifest["artifacts"]["standard_files"].values():
        raw = (ROOT / artifact["path"]).read_bytes().replace(b"\r\n", b"\n")
        assert hashlib.sha256(raw).hexdigest() == artifact["sha256_lf_normalized"]


def test_m25_guards_declare_no_host_or_target_action():
    record = _record()
    guards = record["guards"]
    for key in (
        "frozen_standard_files_changed", "frozen_tags_changed_or_moved",
        "feature_phone_modified_in_this_pass", "host_access_or_mutation_in_this_pass",
        "deploy_restart_cron_wrapper_db_or_collector_action_in_this_pass",
        "historical_evidence_rewritten", "old_artifact_described_as_mislabelled",
        "deployment_doc_gap_claimed_fixed", "full_target_conformance_claim",
    ):
        assert guards[key] is False, key
