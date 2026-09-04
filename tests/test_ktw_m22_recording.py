"""Narrow Standards guards for the KTW M22 DEPLOY-COM-001 evidence record."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.deployment_agent_layer import build_known_evidence_index


ROOT = Path(__file__).resolve().parents[1]
AUDIT_JSON = ROOT / "audits" / "ktw-deployment-proof-m22-2026-09-04.json"
AUDIT_MD = ROOT / "audits" / "ktw-deployment-proof-m22-2026-09-04.md"
KNOWN = ROOT / "standards" / "deployment" / "known-evidence-index.json"
MANIFEST = ROOT / "baselines" / "deployment-standards-v1.0.json"

STANDARDS_SHA = "e379ea59abd472cc5d86899a8e7935ec21845d95"
KTW_PARENT = "afb4aada1d4fae09ada4658fe9fcf8dfa38eb23d"
KTW_SHA = "f49bd02eb214b650a146e9c0f6f348d526285a91"
TARGET = "hetzner/ubuntu-4gb-hel1-1:systemd-venv-soak"
BACKUP_SHA = "80dcb1927598d8d22a3cf1039e05f882f467ff9a9e3d3fa95dad123974bc0407"
FAMILY = "FIRST_VALIDATED_MEMBER_OF_SYSTEMD_VENV_SOAK_COMPATIBILITY"


def _record() -> dict:
    return json.loads(AUDIT_JSON.read_text(encoding="utf-8"))


def test_m22_records_exact_lineage_and_narrow_verdict():
    record = _record()
    assert record["standards_clank_head"] == STANDARDS_SHA
    target = record["ktw"]
    assert target["head"] == KTW_SHA
    assert target["origin_main"] == KTW_SHA
    assert target["parent"] == KTW_PARENT
    assert target["standard"] == "STD-DEPLOY-COM-001"
    assert target["state"] == "LIVE_PROOF_CONFIRMED"
    assert target["lifecycle"] == "CLOSED"
    assert target["deployment_target"] == TARGET
    assert target["scope"].startswith("this exact source SHA + target")


def test_m22_preserves_stale_pre_state_and_marker_correction():
    record = _record()
    pre = record["pre_deploy_state"]
    assert pre["live_sha"] == KTW_PARENT
    assert pre["classification"] == "STALE_DEPLOYMENT"
    assert pre["m20_recon_observed_marker"] == 2
    assert pre["marker_at_deploy_time"] == 4
    assert pre["earlier_recon_preserved"] is True
    assert pre["articles"] == 917
    assert pre["quick_check"] == "ok"


def test_m22_backup_evidence_recorded():
    record = _record()
    backup = record["backup"]
    assert backup["path"] == "/opt/korean-tech-wire/backups/kbw-pre-m21-f49bd02.db"
    assert backup["size_bytes"] == 11120640
    assert backup["sha256"] == BACKUP_SHA
    assert backup["size_matched_live_db"] is True
    assert backup["overwrite_refusal_corroborated"] is True
    assert backup["full_byte_identity_claimed"] is False  # honest: size/hash only


def test_m22_transport_is_credential_free_bundle():
    record = _record()
    transport = record["transport"]
    assert transport["method"] == "credential-free git bundle"
    assert transport["weakness_in_runtime_identity"] is False


def test_m22_identity_chain_proven_non_container():
    record = _record()
    identity = record["runtime_identity"]
    assert identity["classification"] == "IDENTITY_PROVEN"
    assert "systemd unit" in identity["chain"][0]
    assert "f49bd02" in identity["chain"][-2]
    assert identity["oci_demanded"] is False


def test_m22_persistent_state_transition_recorded():
    record = _record()
    transition = record["persistent_state_transition"]
    assert transition["pre_marker"] == 4
    assert transition["post_marker"] == 5
    assert transition["articles_preserved"] == 917
    assert transition["quick_check"] == "ok"
    assert transition["compatibility"] == "COMPATIBLE"
    assert transition["qualification_tables_present"] is True
    assert transition["qc_archive_at_proof_time"] == "absent"


def test_m22_two_natural_fires_correctly_classified():
    record = _record()
    fires = record["natural_fires"]
    first = fires["first_post_deploy"]
    assert first["classification"] == "NATURAL_DUE_CHECK_ONLY"
    assert first["run_rows_created"] == 0
    assert first["is_collection_proof"] is False
    second = fires["second_post_deploy"]
    assert second["is_authoritative_collection_proof"] is True
    assert second["result"] == "exit 0 / systemd SUCCESS"


def test_m22_natural_collection_evidence_recorded():
    record = _record()
    evidence = record["natural_collection_evidence"]
    assert set(evidence["production_sources"]) == {
        "the_elec", "lg_display_newsroom", "etnews_hardware"
    }
    assert evidence["all_success"] is True
    assert evidence["provenance"] == "SCHEDULED"
    assert evidence["qualification_epochs_created"] == 6
    assert evidence["qualification_terminals_created"] == 6
    assert evidence["counts_for_qualification"] == 1


def test_m17_qualification_notqualified_orthogonal_to_deployment():
    record = _record()
    orth = record["orthogonality"]
    assert orth["deployment_proof"] == "CONFIRMED"
    assert orth["qualification_maturity"] == "NOT_YET_QUALIFIED"
    assert orth["ops_com_003_reclosed"] is False
    assert orth["ops_com_003_reclassified"] is False
    assert orth["promotion_readiness_claimed"] is False
    evidence = record["natural_collection_evidence"]
    assert evidence["gate_status"] == "NOT_QUALIFIED"
    assert "repeated scheduled successes" in evidence["gate_status_expected"]


def test_m22_family_names_exactly_ktw():
    record = _record()
    family = record["family_status"]
    assert family["conclusion"] == FAMILY
    assert family["descriptive_only"] is True
    assert family["is_new_standard"] is False
    assert set(family["members"]) == {"korean-tech-wire"}
    assert family["members"]["korean-tech-wire"] == KTW_SHA
    for existing in (
        "ALEMBIC_HEAD", "NUMBERED_SQLITE", "CURRENT_SCHEMA_BOOTSTRAP_SQLITE",
        "CREATE_ALL_WITH_EXPLICIT_SCHEMA_AUTHORITY",
        "ADDITIVE_SCHEMA_MARKER_COMPATIBILITY",
    ):
        assert existing in family["not_merged_with"]
    assert family["all_other_clanks_inherit"] is False


def test_m22_admits_exactly_one_ktw_deploy_com_001_fact():
    record = _record()
    admission = record["known_evidence_admission"]
    assert admission["admission_count"] == 1
    assert admission["admitted"] == {
        "subject": "korean-tech-wire", "revision": KTW_SHA,
        "standard": "STD-DEPLOY-COM-001",
        "state": "LIVE_PROOF_CONFIRMED", "lifecycle": "CLOSED",
    }
    assert admission["historical_m1_preserved"] is True
    assert admission["prior_admissions_preserved"] == 11
    entries = json.loads(KNOWN.read_text(encoding="utf-8"))
    assert entries == build_known_evidence_index()
    ktw = [e for e in entries if e["subject"] == "korean-tech-wire"]
    assert len(ktw) == 2  # COM-002 + COM-001
    com001 = [e for e in ktw if e["standard"] == "STD-DEPLOY-COM-001"]
    assert len(com001) == 1 and KTW_SHA in com001[0]["summary"]
    # every prior admission preserved
    assert {e["subject"] for e in entries} == {
        "chinese-tech-wire", "feature-phone-clank", "korean-tech-wire",
        "oem-radar", "semiconductor-intelligence", "smartwatch-clank",
        "tablet-clank", "watch-clank",
    }


def test_m22_prose_scope_and_no_action_declaration():
    text = " ".join(AUDIT_MD.read_text(encoding="utf-8").split())
    for marker in (
        "LIVE_PROOF_CONFIRMED", KTW_SHA, KTW_PARENT, STANDARDS_SHA, TARGET,
        "NATURAL_DUE_CHECK_ONLY", BACKUP_SHA, FAMILY,
        "NOT_QUALIFIED", "orthogonal", "No host", "were not changed or moved",
        "credential-free",
    ):
        assert marker in text, marker
    assert "no overall" not in text or "Korean Tech Wire" in text
    # scope statements
    assert "this exact source SHA" in text


def test_m22_frozen_deployment_standards_unchanged():
    """Verify frozen STD-*.json files match their pinned hashes."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["status"] == "FROZEN"
    standard_files = manifest["artifacts"]["standard_files"]
    for sid, artifact in standard_files.items():
        raw = (ROOT / artifact["path"]).read_bytes().replace(b"\r\n", b"\n")
        assert hashlib.sha256(raw).hexdigest() == artifact["sha256_lf_normalized"], (
            f"{artifact['path']} drifted from the frozen state"
        )
def test_m22_guards_declare_no_target_or_host_action():
    record = _record()
    guards = record["guards"]
    for key in (
        "frozen_standard_files_changed", "frozen_tags_changed_or_moved",
        "ktw_modified_in_this_pass",
        "host_deployment_live_or_production_db_actions_in_this_pass",
        "production_migration_in_this_pass", "full_target_conformance_claim",
        "generalization_to_future_shas", "generalization_to_other_targets",
        "qualification_notqualified_reinterpreted_as_deployment_failure",
    ):
        assert guards[key] is False, key
