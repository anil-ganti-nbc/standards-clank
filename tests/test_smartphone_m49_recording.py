"""M49: Smartphone DEPLOY-COM-001 live-proof admission guards."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.deployment_agent_layer import build_known_evidence_index

ROOT = Path(__file__).resolve().parents[1]
AUDIT_JSON = ROOT / "audits" / "smartphone-deployment-proof-m49-2026-09-05.json"
AUDIT_MD = ROOT / "audits" / "smartphone-deployment-proof-m49-2026-09-05.md"
KNOWN = ROOT / "standards" / "deployment" / "known-evidence-index.json"
MANIFEST = ROOT / "baselines" / "deployment-standards-v1.0.json"

STANDARDS_SHA = "dee8805defc06b32dd0dc250bd68e3232121405f"
SM_PARENT = "90a1ad4736a871fb48eb4afe5f539d9a9097ed95"
SM_SHA = "e514c45dca4cf966441c27799d98761096dc8c40"
TARGET = "hetzner:/opt/smartphone-clank"
BACKUP_SHA = "a578cfadc0f8478c1f22924c4c0a4210bfc144f8ab323c2be5f3c9a8facdb673"
FAMILY = "FIRST_VALIDATED_MEMBER_OF_SYSTEMD_SOURCE_TIMER_COMPATIBILITY"
RUN_ID = "2c9b9ede-cefb-429c-a53b-c2ca4bddc460"


def _record() -> dict:
    return json.loads(AUDIT_JSON.read_text(encoding="utf-8"))


# -- A-C: exact target, source SHA, verdict -----------------------------------


def test_m49_records_exact_target_source_and_verdict():
    record = _record()
    target = record["smartphone"]
    assert target["head"] == SM_SHA
    assert target["origin_main"] == SM_SHA
    assert target["standard"] == "STD-DEPLOY-COM-001"
    assert target["state"] == "LIVE_PROOF_CONFIRMED"
    assert target["lifecycle"] == "CLOSED"
    assert target["deployment_target"] == TARGET
    assert target["deployment_mechanism"] == "systemd source-specific timers + dashboard service"


# -- D: pre-deploy SHA preserved -----------------------------------------------


def test_m49_preserves_pre_deploy_sha():
    record = _record()
    assert record["pre_deploy_state"]["live_sha"] == SM_PARENT
    assert record["pre_deploy_state"]["classification"] == "BEHIND_CANON"
    assert record["pre_deploy_state"]["distance"] == 10
    assert record["pre_deploy_state"]["dependency_diff"] == "empty"


# -- E: backup identity ---------------------------------------------------------


def test_m49_backup_evidence_recorded():
    record = _record()
    backup = record["backup"]
    assert backup["path"] == "/opt/smartphone-clank/backups/clank-pre-m48-e514c45.db"
    assert backup["size_bytes"] == 5902336
    assert backup["sha256"] == BACKUP_SHA
    assert backup["quick_check"] == "ok"


# -- F-G: Alembic 0007→0008 with procedural deviation --------------------------


def test_m49_alembic_procedural_deviation_preserved_honestly():
    record = _record()
    dev = record["alembic_procedural_deviation"]
    assert dev["live_transition"]["from"] == "0007_wave1_baseline_state"
    assert dev["live_transition"]["to"] == "0008_analyst_action_integrity"
    assert dev["classification"] == "LIVE_MIGRATION_SUCCEEDED_WITH_PROCEDURAL_DEVIATION"
    assert "alembic/env.py" in dev["actual"]
    assert "scratch" in dev["intended"].lower()
    assert dev["no_data_loss"] is True


def test_m49_no_false_scratch_first_claim():
    text = " ".join(AUDIT_MD.read_text(encoding="utf-8").split()).lower()
    assert "procedural deviation" in text
    # The MD must not present the live migration as if the scratch-first plan
    # executed: any mention of scratch-first must be framed as intent, not fact.
    if "scratch-first" in text:
        assert "intended" in text
    assert "live" in text and "production db" in text or "live db" in text


# -- I: canonical index identity ------------------------------------------------


def test_m49_canonical_index_identity_recorded():
    record = _record()
    dev = record["alembic_procedural_deviation"]
    assert "uq_analyst_action_terminal" in dev["migration_effect"]


# -- J: analyst_actions 0→0 ------------------------------------------------------


def test_m49_analyst_actions_zero_to_zero():
    record = _record()
    dev = record["alembic_procedural_deviation"]
    assert dev["analyst_actions_rows_before"] == 0
    assert dev["analyst_actions_rows_after"] == 0
    assert dev["no_data_loss"] is True


# -- K: DB size change -----------------------------------------------------------


def test_m49_db_size_change_recorded():
    record = _record()
    assert record["alembic_procedural_deviation"]["db_size_change"] == "5902336 → 5906432"


# -- L: systemd/venv identity chain -----------------------------------------------


def test_m49_identity_chain_native_systemd_venv():
    record = _record()
    identity = record["runtime_identity"]
    assert identity["native_systemd_venv"] is True
    assert identity["oci_demanded"] is False
    assert "systemd unit" in identity["chain"][0]
    assert "checkout SHA e514c45" in identity["chain"][-1]


# -- M: stale dashboard process recorded ------------------------------------------


def test_m49_stale_dashboard_recorded():
    record = _record()
    dash = record["dashboard"]
    assert dash["pre_restart"]["http_status"] == 500
    assert dash["pre_restart"]["code_era"] == "pre-deploy"
    assert dash["pre_restart"]["pid"] == 1606365
    assert dash["post_restart"]["http_status"] == 200
    assert dash["post_restart"]["pid"] == 1738142
    assert dash["no_collection_on_load"] is True


# -- N-O: PID restart + HTTP recovery ---------------------------------------------


def test_m49_pid_restart_and_http_recovery():
    record = _record()
    dash = record["dashboard"]
    assert dash["pre_restart"]["pid"] == 1606365
    assert dash["post_restart"]["pid"] == 1738142
    assert dash["pre_restart"]["http_status"] == 500
    assert dash["post_restart"]["http_status"] == 200


# -- P: /proc/fd/ same-state-path proof -------------------------------------------


def test_m49_same_state_path_runtime_proof():
    record = _record()
    ssp = record["same_state_path"]
    assert "clank.db" in ssp["dashboard_fd_proof"]
    assert ssp["path_equality_proven"] is True
    assert ssp["alembic_version_both"] == "0008_analyst_action_integrity"
    assert ssp["shared_counts"]["devices"] == 270


# -- Q: 270 devices / 350 runs visibility ------------------------------------------


def test_m49_shared_production_state_counts():
    record = _record()
    ssp = record["same_state_path"]["shared_counts"]
    assert ssp["devices"] == 270
    assert ssp["collector_runs"] == 350


# -- R: dashboard load no collection -----------------------------------------------


def test_m49_dashboard_no_collection_on_load():
    record = _record()
    assert record["dashboard"]["no_collection_on_load"] is True


# -- S-T: 20:18 no-material vs 21:46 authoritative --------------------------------


def test_m49_two_fires_correctly_classified():
    record = _record()
    proof = record["natural_proof"]
    first = proof["earlier_no_material_fire"]
    auth = proof["authoritative_run"]
    # Only the 21:46 run carries proof weight; the 20:18 fire is explicitly
    # declassified as no-material-collection.
    assert first["classification"] == "NATURAL_EXECUTION_NO_MATERIAL_COLLECTION"
    assert first["is_collection_proof"] is False
    assert auth["started_at_utc"] > first["started_at_utc"]
    assert auth["run_reason"] == "production_scheduled"
    assert auth["run_id"] != first.get("run_id")


# -- U-W: production_scheduled provenance + run ID + new_devices -------------------


def test_m49_natural_run_provenance_and_results():
    record = _record()
    auth = record["natural_proof"]["authoritative_run"]
    assert auth["run_reason"] == "production_scheduled"
    assert auth["run_id"] == RUN_ID
    assert auth["new_devices"] == 0
    assert auth["success"] == 1
    assert auth["collector"] == "samsung_us_support_sitemap"


# -- X: collector_runs 349→350 ------------------------------------------------------


def test_m49_collector_runs_increment():
    record = _record()
    integrity = record["post_run_integrity"]
    assert integrity["collector_runs_delta"] == "349 → 350"
    assert integrity["rollback_required"] is False


# -- Y: no rollback -----------------------------------------------------------------


def test_m49_no_rollback():
    record = _record()
    assert record["post_run_integrity"]["rollback_required"] is False


# -- Z: exact scope / no inheritance ------------------------------------------------


def test_m49_exact_scope_no_inheritance():
    record = _record()
    target = record["smartphone"]
    assert "this exact source SHA" in target["scope"]
    assert record["guards"]["generalization_to_future_shas"] is False
    assert record["guards"]["generalization_to_other_targets"] is False


# -- AA: frozen standards/tags unchanged ---------------------------------------------


def _lf_pinned_artifacts(manifest: dict):
    """Yield (path, expected_lf_sha) for every LF-normalized pin in a freeze
    manifest, handling both direct entries and nested per-standard groups."""
    pinned = []

    def walk(node):
        if not isinstance(node, dict):
            return
        if "sha256_lf_normalized" in node and "path" in node:
            pinned.append((node["path"], node["sha256_lf_normalized"]))
            return
        for value in node.values():
            walk(value)

    walk(manifest.get("artifacts", {}))
    return pinned


def test_m49_frozen_standards_unchanged():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["status"] == "FROZEN"
    pinned = _lf_pinned_artifacts(manifest)
    assert pinned, "no LF-normalized pins found in deployment manifest"
    for path, expected in pinned:
        raw = (ROOT / path).read_bytes().replace(b"\r\n", b"\n")
        assert hashlib.sha256(raw).hexdigest() == expected, (
            f"frozen artifact drifted: {path}"
        )


# -- family + guards ------------------------------------------------------------------


def test_m49_family_names_exactly_smartphone():
    record = _record()
    family = record["family_status"]
    assert family["conclusion"] == FAMILY
    assert family["descriptive_only"] is True
    assert family["is_new_standard"] is False
    assert set(family["members"]) == {"smartphone-clank"}
    assert family["members"]["smartphone-clank"] == SM_SHA


def test_m49_guards_declare_no_target_or_host_action():
    record = _record()
    guards = record["guards"]
    for key in (
        "frozen_standard_files_changed", "frozen_tags_changed_or_moved",
        "smartphone_modified_in_this_pass",
        "host_deployment_live_or_production_db_actions_in_this_pass",
        "generalization_to_future_shas", "generalization_to_other_targets",
        "com002_reclosed", "full_target_conformance_claim",
    ):
        assert guards[key] is False, key


# -- evidence-index admission ---------------------------------------------------


def test_m49_known_evidence_index_admits_smartphone_com001():
    committed = json.loads(KNOWN.read_text(encoding="utf-8"))
    regenerated = build_known_evidence_index()
    assert committed == regenerated, "committed index is stale vs audits/*.md"
    assert len(committed) == 15
    sm = [
        e for e in committed
        if e["subject"] == "smartphone-clank" and e["standard"] == "STD-DEPLOY-COM-001"
    ]
    assert len(sm) == 1
    assert SM_SHA in sm[0]["summary"]
    assert TARGET in sm[0]["summary"]
    assert sm[0]["source_reference"] == "audits/smartphone-deployment-proof-m49-2026-09-05.md"


def test_m49_prior_admissions_preserved_verbatim():
    """The pre-M49 pairs plus the M52 CTW COM-001 admission must all be present."""
    committed = json.loads(KNOWN.read_text(encoding="utf-8"))
    pairs = {(e["subject"], e["standard"]) for e in committed}
    expected_prior = {
        ("chinese-tech-wire", "STD-DEPLOY-COM-001"),
        ("chinese-tech-wire", "STD-DEPLOY-COM-002"),
        ("feature-phone-clank", "STD-DEPLOY-COM-001"),
        ("feature-phone-clank", "STD-DEPLOY-COM-002"),
        ("korean-tech-wire", "STD-DEPLOY-COM-001"),
        ("korean-tech-wire", "STD-DEPLOY-COM-002"),
        ("oem-radar", "STD-DEPLOY-COM-001"),
        ("oem-radar", "STD-DEPLOY-COM-002"),
        ("semiconductor-intelligence", "STD-DEPLOY-COM-002"),
        ("smartphone-clank", "STD-DEPLOY-COM-001"),
        ("smartwatch-clank", "STD-DEPLOY-COM-001"),
        ("smartwatch-clank", "STD-DEPLOY-COM-002"),
        ("tablet-clank", "STD-DEPLOY-COM-001"),
        ("tablet-clank", "STD-DEPLOY-COM-002"),
        ("watch-clank", "STD-DEPLOY-COM-001"),
    }
    assert pairs == expected_prior


def test_m49_audit_md_carries_parsable_json_block():
    text = AUDIT_MD.read_text(encoding="utf-8")
    start = text.index("```json")
    end = text.index("```", start + 7)
    block = json.loads(text[start + 7:end])
    # layer-tool findings format: {"clank": ..., "findings": [...]}
    assert block["clank"] == "smartphone-clank"
    assert len(block["findings"]) == 1
    finding = block["findings"][0]
    assert finding["standard"] == "STD-DEPLOY-COM-001"
    assert "LIVE_PROOF_CONFIRMED" in finding["summary"]
    assert SM_SHA in finding["summary"]


# -- AA (continued): frozen tags have not moved -----------------------------------


def test_m49_frozen_tags_have_not_moved():
    import subprocess

    expected = {
        "ui-standards-v1.0": "d11320704aed69a3d8f854c9264b184e392ec80f",
        "deployment-standards-v1.0": "33cc38849180716fd4d06b1356cf70c49d3d41d2",
        "operations-standards-v1.0": "7100f294a83c30594f2ff9e953f7c9f77a95747f",
        "data-ontology-standards-v1.0": "464a8057ea5dc26ef83248a20bafa0be5aa31148",
        "collector-ui-design-standards-v1.0": "f81f4ffa91e9a7af2f80195339d2762180a3154e",
    }
    for tag, expected_commit in expected.items():
        result = subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", f"{tag}^{{commit}}"],
            capture_output=True, text=True, encoding="utf-8",
            stdin=subprocess.DEVNULL, check=True,
        )
        assert result.stdout.strip() == expected_commit, f"tag {tag} has moved"
