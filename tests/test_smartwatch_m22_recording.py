"""Narrow Standards guards for the Smartwatch M22 DEPLOY-COM-001 admission."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.deployment_agent_layer import build_known_evidence_index


ROOT = Path(__file__).resolve().parents[1]
AUDIT_JSON = ROOT / "audits" / "smartwatch-deployment-proof-m22-2026-09-02.json"
AUDIT_MD = ROOT / "audits" / "smartwatch-deployment-proof-m22-2026-09-02.md"
KNOWN = ROOT / "standards" / "deployment" / "known-evidence-index.json"
MANIFEST = ROOT / "baselines" / "deployment-standards-v1.0.json"

STANDARDS_SHA = "8cea2e5f4d95a40be5119bc0f1da2612bc83f11f"
SW_SHA = "a93355480bb11e1bd16ae7837256ce9002fc2aa7"
TARGET = "hetzner/ubuntu-4gb-hel1-1:cron-docker-compose-staging"
IMAGE_ID = "sha256:8fdace0a3847c346aa4bd989f7429be7de2cacb45d71af853017770bacab83b5"
CYCLE = "61d54662fbf344fca9888df3f5f870a3"
FINGERPRINT = "f24e97c47e741913"


def _record() -> dict:
    return json.loads(AUDIT_JSON.read_text(encoding="utf-8"))


def test_m22_records_exact_lineage_target_and_verdict():
    record = _record()
    assert record["standards_clank_head"] == STANDARDS_SHA
    sw = record["smartwatch"]
    assert sw["head"] == SW_SHA and sw["origin_main"] == SW_SHA
    assert sw["modified_in_this_pass"] is False
    assert sw["standard"] == "STD-DEPLOY-COM-001"
    assert sw["state"] == "LIVE_PROOF_CONFIRMED"
    assert sw["lifecycle"] == "CLOSED"
    assert sw["deployment_target"] == TARGET
    assert record["verdict"]["revision"] == SW_SHA
    assert record["verdict"]["deployment_target"] == TARGET
    assert record["verdict"]["generalizes_to_other_targets"] is False
    assert record["verdict"]["generalizes_to_future_revisions"] is False
    # closure rests on the corrected live wiring, not the artifact revision
    assert record["verdict"]["closure_depends_on_corrected_live_wiring_evidence"] is True
    assert record["verdict"]["closure_depends_only_on_artifact_revision"] is False


def test_m22_identity_chain_image_id_and_stale_history_preserved():
    record = _record()
    chain = record["identity_chain"]
    for facet in ("intended_source_sha", "host_source_head", "oci_revision",
                  "runtime_run_revision"):
        assert chain[facet] == SW_SHA
    assert chain["four_way_equal"] is True
    assert chain["deployed_artifact"] == "smartwatch-clank:a933554"
    assert chain["image_id"] == IMAGE_ID
    assert chain["deployed_id_selector_alone_is_not_artifact_proof"] is True
    stale = record["initial_live_state"]
    assert stale["deployed_selector"] == "smartwatch-clank:08a23f9"
    assert stale["classification"] == "STALE_CONTENT_CONSISTENT"
    assert stale["provenance_lie_proven"] is False
    assert stale["material_mismatch"].endswith("closure refused")


def test_m22_wiring_defect_and_correction_are_both_preserved():
    record = _record()
    defect = record["material_wiring_defect"]
    assert defect["first_natural_tick"] == "03:50Z"
    assert defect["exposed"] == "MATERIAL_WIRING_DRIFT"
    assert defect["detail"] == "host wrapper omitted --trigger SCHEDULED"
    assert defect["recorded_provenance_at_first_tick"] == "MANUAL"
    assert defect["blocked_deploy_com_001"] is True
    assert defect["historical_manual_evidence_preserved_not_rewritten"] is True
    fix = record["host_wrapper_remediation"]
    assert fix["changed"] == "exactly one exec line"
    for key in ("no_crontab_change", "no_image_rebuild", "no_source_commit"):
        assert fix[key] is True
    assert fix["result"].startswith("host wrapper content-identical")
    closing = record["closing_evidence"]
    assert closing["second_natural_tick_utc"] == "2026-09-02T05:50:02Z"
    assert closing["cycle_id"] == CYCLE
    assert closing["execution_provenance"] == "SCHEDULED for all 13 new runs"
    assert closing["schema_version_at_run"] == 3
    assert closing["config_fingerprint"] == FINGERPRINT


def test_m22_state_migration_and_outcome():
    record = _record()
    state = record["persistent_state"]
    assert state["pre_deploy_schema"] == 2
    assert state["canonical_migration"] == (
        "v2 -> v3 via M18 compatibility barrier and canonical additive _migrate()"
    )
    assert state["post_schema"] == 3 and state["expected"] == 3
    assert state["state"] == "COMPATIBLE" and state["integrity_check"] == "ok"
    assert state["migration_during_m21c_observation"] is False
    closing = record["closing_evidence"]
    assert (closing["attempted"], closing["healthy"], closing["failed"]) == (13, 13, 0)
    assert closing["runs"] == "1583-1595"
    assert closing["production_allowlist_count_verified_against_tracked_config"] == 13
    mechanism = record["deployment_mechanism"]
    assert mechanism["model"] == "cron + docker compose one-shot execution"
    assert mechanism["resident_service_required"] is False
    assert "run --mode production --trigger SCHEDULED" in mechanism["exec_line"]


def test_m22_qualification_and_garmin_recorded_narrowly():
    record = _record()
    qual = record["qualification_provenance"]
    assert qual["historical_0350_manual_epoch_openings"].startswith(
        "valid history, untouched"
    )
    at = qual["at_0550"]
    assert at["same_material_identity"] is True and at["epoch_reset"] is False
    assert at["terminal_provenance"] == "SCHEDULED" and at["terminal_outcome"] == "HEALTHY"
    assert qual["epoch_not_recreated_as_scheduled"] is True
    assert qual["latest_terminal_evidence_represents_scheduled_path"] is True
    garmin = record["experimental_garmin"]
    assert garmin["collectors"] == ["garmin_catalogue", "garmin_official_news"]
    assert garmin["state"] == "unhealthy in soak"
    assert garmin["in_production_allowlist_tick"] is False
    assert garmin["orthogonal_to_com_001_proof"] is True
    assert garmin["claimed_healthy"] is False


def test_m22_all_material_evidence_obligations_supported():
    record = _record()
    review = record["evidence_review"]
    yes_keys = [k for k in review if k != "unsupported_material_obligations"]
    assert all(review[k] is True for k in yes_keys)
    assert review["unsupported_material_obligations"] == []


def test_m22_remaining_state_and_no_full_conformance():
    record = _record()
    remaining = record["remaining_smartwatch_findings"]
    assert remaining["STD-OPS-COM-003"].startswith("CLOSED at M5")
    assert remaining["STD-DEPLOY-COM-002"].startswith("CLOSED at M18")
    assert remaining["STD-UI-COM-011"] == "unresolved"
    assert remaining["fully_conforming_claimed_here"] is False
    non = record["non_inheritance"]
    assert non["no_other_target_inherits_this_proof"] is True
    assert non["watch_com_001_fact_preserved"] is True
    assert non["smartwatch_com_002_fact_preserved"] is True


def test_m22_admits_exactly_one_smartwatch_com001_fact():
    record = _record()
    admission = record["known_evidence_admission"]
    assert admission["admission_count"] == 1
    assert admission["admitted"] == {
        "subject": "smartwatch-clank", "revision": SW_SHA,
        "standard": "STD-DEPLOY-COM-001", "deployment_target": TARGET,
        "state": "LIVE_PROOF_CONFIRMED", "lifecycle": "CLOSED",
    }
    assert admission["deployment_facts_after_admission"] == 9
    entries = json.loads(KNOWN.read_text(encoding="utf-8"))
    assert entries == build_known_evidence_index()
    assert len(entries) == 16
    sw = [e for e in entries if e["subject"] == "smartwatch-clank"]
    assert len(sw) == 2
    by_standard = {e["standard"]: e for e in sw}
    assert by_standard["STD-DEPLOY-COM-002"]["source_reference"] == (
        "audits/smartwatch-persistent-state-remediation-m18-2026-09-02.md"
    )
    com001 = by_standard["STD-DEPLOY-COM-001"]
    assert com001["source_reference"] == (
        "audits/smartwatch-deployment-proof-m22-2026-09-02.md"
    )
    assert "LIVE_PROOF_CONFIRMED" in com001["summary"]
    assert SW_SHA in com001["summary"] and TARGET in com001["summary"]
    # exactly one Watch COM-001 fact remains, and the watch fact is untouched
    watch = [e for e in entries
             if e["subject"] == "watch-clank" and e["standard"] == "STD-DEPLOY-COM-001"]
    assert len(watch) == 1
    assert "d03bc4b2f90289686331af0447d5ca4e8cf55822" in watch[0]["summary"]


def test_m22_prose_preserves_defect_history_and_no_action_declaration():
    text = " ".join(AUDIT_MD.read_text(encoding="utf-8").split())
    for marker in (
        "LIVE_PROOF_CONFIRMED", SW_SHA, TARGET, STANDARDS_SHA, IMAGE_ID, CYCLE,
        "STALE_CONTENT_CONSISTENT", "MATERIAL_WIRING_DRIFT", "MANUAL",
        "SCHEDULED", "2026-09-02T05:50:02Z", "1583", FINGERPRINT,
        "content-identical", "not rewritten", "unhealthy in soak",
        "STD-UI-COM-011", "No-action declaration", "were not changed or moved",
    ):
        assert marker in text, marker


def test_m22_frozen_deployment_standards_unchanged():
    """Pure-read guard: the frozen standard files still match the
    deployment-standards-v1.0 manifest's LF-normalized hashes (tag-target
    immutability itself is guarded by tests/test_deployment_baseline_v1_0.py)."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["status"] == "FROZEN"
    assert manifest["immutable_tag"] == "deployment-standards-v1.0"
    for artifact in manifest["artifacts"]["standard_files"].values():
        raw = (ROOT / artifact["path"]).read_bytes().replace(b"\r\n", b"\n")
        assert hashlib.sha256(raw).hexdigest() == artifact["sha256_lf_normalized"]


def test_m22_guards_declare_no_host_or_target_action():
    record = _record()
    guards = record["guards"]
    for key in (
        "frozen_standard_files_changed", "frozen_tags_changed_or_moved",
        "smartwatch_modified_in_this_pass", "host_access_or_mutation_in_this_pass",
        "deploy_restart_cron_wrapper_db_or_collector_action_in_this_pass",
        "historical_manual_evidence_rewritten", "experimental_garmin_claimed_healthy",
        "full_target_conformance_claim",
    ):
        assert guards[key] is False, key
