"""M52: CTW DEPLOY-COM-001 live-proof admission guards."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from tools.deployment_agent_layer import build_known_evidence_index

ROOT = Path(__file__).resolve().parents[1]
AUDIT_JSON = ROOT / "audits" / "ctw-deployment-proof-m52-2026-09-05.json"
AUDIT_MD = ROOT / "audits" / "ctw-deployment-proof-m52-2026-09-05.md"
KNOWN = ROOT / "standards" / "deployment" / "known-evidence-index.json"
MANIFEST = ROOT / "baselines" / "deployment-standards-v1.0.json"

CTW_SHA = "cfbd3158a5272aab6e67a2a9005be2c3a45544e6"
PRE_SOURCE = "552ffff"
PRE_SOURCE_FULL = "552ffff472689470820aecdec3d6dfa6faf478a8"
TARGET = "NAS:/volume2/clank/chinese-tech-wire"
MECHANISM = ("DSM Task Scheduler (hourly at :10 IST) -> host flock "
             "/tmp/ctw-nas-run.lock -> Docker one-shot chinese-tech-wire-nas-soak "
             "-> --full-once --scheduled")
BACKUP_SHA = "63cd4b78fc35347ba9598dbf76cc9b47830c818feacc1ab77bef1d03e9f184ac"
TARBALL_SHA = "e09fc9f081e6258e3f23c6f045e893cc39ae97d2701ed971f1fda738233e27a2"
LIVE_ADOPTED_SHA = "8c137bc4c2c43e0cd56ce5838a77be685b4707836e5c9ae6508ba272dd679826"
POST_RUN_SHA = "e39b65a34b2b799c497b24ed98bceeeea27d1b9b91010ff8a50ff7fba0d922d5"
INCIDENT_ID = "2a18c8ae-f887-4018-ae56-8b03b39141ee"
M17_CTW_COM002_SHA = "c340a45ac8cfbab58d749dcbf78a7d703ca9cdb1"


def _record() -> dict:
    return json.loads(AUDIT_JSON.read_text(encoding="utf-8"))


# -- A-C: exact target, source SHA, verdict -----------------------------------


def test_m52_records_exact_target_source_and_verdict():
    record = _record()
    ctw = record["ctw"]
    assert ctw["head"] == CTW_SHA
    assert ctw["origin_main"] == CTW_SHA
    assert ctw["standard"] == "STD-DEPLOY-COM-001"
    assert ctw["state"] == "LIVE_PROOF_CONFIRMED"
    assert ctw["lifecycle"] == "CLOSED"
    assert ctw["deployment_target"] == TARGET
    assert ctw["deployment_mechanism"] == MECHANISM
    assert "delivery OFF" in ctw["scope"]


# -- D-E: NAS current authority, Hetzner rollback-disabled ---------------------


def test_m52_preserves_authority_cutover_history():
    cut = _record()["authority_cutover_history"]
    assert cut["nas"]["role"] == "current authority since 2026-08-27 cutover"
    hetzner = cut["hetzner"]
    assert hetzner["staging_checkout"] == "9eec9f07f98425fdffd96433fd1748444a0a6dcf"
    assert hetzner["cron_disabled_utc"] == "2026-08-27T13:46:55Z"
    assert hetzner["role"] == "previous authority, disabled rollback"
    assert hetzner["last_run"] == {"id": 431, "status": "SUCCESS", "ended_utc": "2026-08-27T13:11:42Z"}
    assert cut["dual_host_divergence_aug19_27"].startswith("historical")
    assert cut["diagnostic_clank_incident"]["id_cited"] == INCIDENT_ID
    assert cut["diagnostic_clank_incident"]["record_retrieved"] is False


# -- F: pre-source 552ffff ------------------------------------------------------


def test_m52_records_pre_deploy_source():
    record = _record()
    pre = record["pre_deploy_state"]
    assert pre["live_source"] == PRE_SOURCE
    assert pre["live_source_full"] == PRE_SOURCE_FULL
    assert len(pre["identity_evidence"]) == 4
    assert pre["deployment_root"] == "/volume2/clank/chinese-tech-wire"


# -- G: LEGACY_UNADOPTED, not UNKNOWN -------------------------------------------


def test_m52_classifies_pre_state_legacy_unadopted_not_unknown():
    db = _record()["pre_deploy_state"]["db"]
    assert db["classification_under_canon"] == "LEGACY_UNADOPTED"
    assert db["not_unknown"] is True
    assert db["schema_meta"] == "absent"
    assert db["tables"] == 21
    assert db["size_bytes"] == 28147712
    assert db["sha256"] == BACKUP_SHA
    assert db["row_counts"] == {"articles": 12078, "source_runs": 7527, "ingestion_runs": 579}


# -- H: privilege-path correction -------------------------------------------------


def test_m52_privilege_path_correction_recorded():
    priv = _record()["privilege_path_correction"]
    assert priv["classification"] == "EARLIER_INFERENCE_SUPERSEDED_BY_STRONGER_EVIDENCE"
    assert priv["actual_path"] == "NOPASSWD: /usr/local/bin/docker (pre-existing operator rule)"
    assert priv["privilege_changes"] == "none"


# -- I: backup identity ------------------------------------------------------------


def test_m52_backup_identity():
    backup = _record()["backup"]
    assert backup["path"].endswith("ctw-pre-m51-20260905T011627Z.db")
    assert backup["size_bytes"] == 28147712
    assert backup["sha256"] == BACKUP_SHA
    assert backup["sha_identical_to_live"] is True
    assert backup["quick_check"] == "ok"
    assert backup["prior_backups_untouched"] is True


# -- J: pinned source verification ---------------------------------------------------


def test_m52_pinned_source_verification():
    art = _record()["source_artifact"]
    assert art["commit"] == CTW_SHA
    assert art["form"] == "GitHub pinned-commit source tarball (no git binary on NAS)"
    assert art["tarball_sha256"] == TARBALL_SHA
    assert "TREES-IDENTICAL" in art["canonical_tree_comparison"]
    assert "autocrlf" in art["canonical_tree_comparison"]
    assert art["git_checkout_on_nas_claimed"] is False
    assert art["stale_build_src_used"] is False


# -- K-L: mode-000 build incident; broken image never deployed ------------------------


def test_m52_build_incident_preserved_and_broken_image_never_deployed():
    incident = _record()["build_incident"]
    assert incident["classification"] == "PROCEDURAL_EVIDENCE_NOT_SOURCE_DEFECT"
    first = incident["first_build"]
    assert "NFSv4 ACLs" in first["context"]
    assert "mode-000" in first["result"]
    assert first["deployed"] is False
    second = incident["second_build"]
    assert second["context"] == "/tmp clean-modes extraction"
    assert second["correct_modes_verified"] is True
    assert second["result"].endswith("(id 5e7019a25f20)")


# -- (§10) dependency gate --------------------------------------------------------------


def test_m52_dependency_gate():
    dep = _record()["dependency_gate"]
    assert dep["classification"] == "DEPENDENCIES_COMPATIBLE"
    assert dep["requirements_txt_diff"] == "empty"
    assert "--require-hashes" in dep["lock_added"]
    assert dep["host_python_mutated"] is False


# -- M: scratch targeting proven before mutation ------------------------------------------


def test_m52_scratch_targeting_proven():
    targeting = _record()["scratch_adoption"]["targeting_proof"]
    assert targeting["classification"] == "SCRATCH_TARGET_PROVEN_BEFORE_MUTATION"
    assert "scratch-mount-marker-m51" in targeting["mount_marker"]
    assert targeting["resolved_url"].startswith("sqlite:////app/data/ctw.db")
    assert targeting["uid_ownership_aligned"].startswith("10001")
    assert targeting["live_db_excluded"] is True


# -- N-O-P: scratch adoption exact; only schema_meta added; all rows preserved --------------


def test_m52_scratch_adoption_exact_and_preserving():
    scratch = _record()["scratch_adoption"]
    assert scratch["pre_state"].startswith("LEGACY_UNADOPTED")
    result = scratch["adopt_result"]
    assert result == {"adopted": True, "state": "COMPATIBLE", "expected_schema_version": 1,
                      "verified_tables": 22, "exit": 0}
    added = scratch["added"]["schema_meta_row"]
    assert added[0] == 1 and added[2] == "legacy-adoption"
    preservation = scratch["preservation"]
    assert preservation["original_21_table_row_counts"] == "all unchanged"
    assert preservation["indexes"] == "41 -> 41"
    assert preservation["views_triggers"] == "0 -> 0"
    assert preservation["quick_check"] == "ok"
    assert preservation["unrelated_schema_mutation"] is False


# -- Q: scratch health ------------------------------------------------------------------------


def test_m52_scratch_health():
    health = _record()["scratch_adoption"]["scratch_health"]
    assert health["operational_state"] == "healthy"
    assert health["status_reasons"] == []
    assert health["total_runs"] == 579


# -- R: run 580 old-source checkpoint, not canonical proof -------------------------------------


def test_m52_run_580_is_old_source_checkpoint_only():
    checkpoint = _record()["final_old_source_checkpoint"]
    assert checkpoint["run_id"] == 580
    assert checkpoint["trigger"] == "SCHEDULED"
    assert checkpoint["source"] == PRE_SOURCE
    assert checkpoint["status"] == "SUCCESS"
    assert checkpoint["used_as_canonical_proof"] is False


# -- S: explicit live adoption ------------------------------------------------------------------


def test_m52_live_adoption_explicit_and_matching_scratch():
    live = _record()["live_adoption"]
    assert "explicit operator authorization" in live["authorization"]
    for pre in ("backup verified", "scratch PASS", "scratch health PASS",
                "canonical image built", "docker authority confirmed", "flock free"):
        assert pre in live["preconditions"]
    assert live["result"] == _record()["scratch_adoption"]["adopt_result"]
    assert live["matched_scratch"] is True
    assert live["schema_meta_row"][0] == 1 and live["schema_meta_row"][2] == "legacy-adoption"
    assert live["post_adoption"]["articles"] == 12091
    assert live["post_adoption"]["ingestion_runs"] == 580
    assert live["post_adoption"]["sha256"] == LIVE_ADOPTED_SHA
    assert live["post_adoption"]["automatic_migration"] is False


# -- T-U: pointer transition + identity surfaces -------------------------------------------------


def test_m52_pointer_transition_and_identity_surfaces():
    pointer = _record()["pointer_transition"]
    assert pointer["from"] == PRE_SOURCE
    assert pointer["to"] == CTW_SHA
    assert pointer["files_changed"] == [".deployed-id", ".env"]
    unchanged = pointer["files_unchanged"]
    assert len(unchanged) == 3
    for sha in unchanged.values():
        assert len(sha) == 64
    surfaces = pointer["identity_surfaces"]
    for surface in ("pinned_source_artifact", "oci_revision_label",
                    "ctw_source_revision_env", "identity_output"):
        assert surfaces[surface] == CTW_SHA, surface
    assert surfaces["git_head_on_nas_claimed"] is False


# -- V-X: scheduler/lock/delivery contract ---------------------------------------------------------


def test_m52_operational_contract_preserved():
    contract = _record()["operational_contract"]
    assert contract["scheduler"] == "DSM Task Scheduler, hourly at :10 IST"
    assert contract["command"] == "--full-once --scheduled"
    assert contract["host_lock"] == "flock -n /tmp/ctw-nas-run.lock"
    assert contract["release_channel"] == "nas-soak"
    assert contract["delivery"] == "OFF"
    assert contract["active_sources"] == 13
    assert contract["duplicate_schedule"] is False
    assert contract["hetzner_reenabled"] is False


# -- Y-Z: run 581 authoritative + SCHEDULED provenance -----------------------------------------------


def test_m52_run_581_is_authoritative_natural_proof():
    run = _record()["natural_proof"]["authoritative_run"]
    assert run["run_id"] == 581
    assert run["trigger"] == "SCHEDULED"
    assert run["status"] == "SUCCESS"
    assert run["started_utc"].startswith("2026-09-05T02:40:04")
    assert run["finished_utc"].startswith("2026-09-05T02:41:17")
    assert run["source"] == CTW_SHA
    assert run["duration_seconds"] == 73.94
    assert run["errors"] == 0 and run["warnings"] == 0


# -- AA-AC: 13-source scope, continuity, no false novelty ----------------------------------------------


def test_m52_source_scope_and_continuity():
    proof = _record()["natural_proof"]
    scope = proof["source_scope"]
    assert scope["count"] == 13 and len(scope["executed"]) == 13
    assert scope["ok"] == 9 and scope["soft_blocked"] == 4
    assert scope["canonically_disabled_absent"] == ["ptt", "geekbench"]
    assert scope["scope_match"] is True
    assert "not deployment failure" in scope["soft_blocks_classified"]
    cont = proof["continuity"]
    assert cont["articles"] == "12091 -> 12111"
    assert cont["community_threads"] == "258 -> 260"
    assert cont["source_runs"] == "7540 -> 7553"
    for flag in ("replay", "identity_reset", "false_novelty_flood",
                 "history_discontinuity", "scope_expansion", "hetzner_divergence_merged"):
        assert cont[flag] is False, flag


# -- AD: schema_meta barrier held ------------------------------------------------------------------------


def test_m52_barrier_held():
    barrier = _record()["natural_proof"]["compatibility_barrier"]
    assert barrier["classification"] == "BARRIER_HELD"
    assert barrier["schema_meta_after_run_581"] == [1, "2026-09-05 01:42:24", "legacy-adoption"]
    assert barrier["normal_operation_rewrote_authority"] is False


# -- AE-AF: dashboard N/A; no rollback ---------------------------------------------------------------------


def test_m52_dashboard_not_deployed_and_no_rollback():
    post = _record()["natural_proof"]["post_run"]
    assert _record()["natural_proof"]["dashboard"] == ("NOT_DEPLOYED / NOT_APPLICABLE "
                                                       "(no server-side CTW dashboard exists on this target)")
    assert post["quick_check"] == "ok"
    assert post["health"]["operational_state"] == "healthy"
    assert post["health"]["total_runs"] == 581
    assert post["delivery_still_off"] is True
    assert post["rollback_triggered"] is False
    assert post["old_image_retained"] == "chinese-tech-wire:552ffff"
    assert post["hetzner_still_disabled"] is True
    assert post["db_sha256"] == POST_RUN_SHA


# -- AG: exact scope / no inheritance ------------------------------------------------------------------------


def test_m52_exact_scope_no_inheritance():
    record = _record()
    assert "delivery OFF" in record["ctw"]["scope"]
    guards = record["guards"]
    for key in ("frozen_standard_files_changed", "frozen_tags_changed_or_moved",
                "ctw_source_modified_in_this_pass", "nas_accessed_in_this_standards_pass",
                "hetzner_reenabled", "generalization_to_future_shas",
                "generalization_to_other_targets", "com002_reclosed",
                "cutover_history_rewritten", "full_target_conformance_claim"):
        assert guards[key] is False, key


# -- (§3) COM-002 closure preserved, not re-closed --------------------------------------------------------------


def test_m52_preserves_m17_com002_closure():
    record = _record()
    preserved = record["known_evidence_admission"]["com002_closure_preserved"]
    assert "CONFORMS/CLOSED" in preserved and M17_CTW_COM002_SHA[:7] in preserved
    assert record["guards"]["com002_reclosed"] is False


# -- evidence-index admission ------------------------------------------------------------------------------------


def test_m52_known_evidence_index_admits_ctw_com001():
    committed = json.loads(KNOWN.read_text(encoding="utf-8"))
    assert committed == build_known_evidence_index(), "committed index is stale vs audits/*.md"
    # M57 resolved M56 debts D8/D9 by admitting Watch's and Smartphone's
    # already-concluded COM-002 facts, taking the index 16 -> 18. This
    # mission's own admission is unchanged; the global total is no longer
    # pinned here, since a later legitimate admission is not this test's
    # concern. What must still hold: this mission's fact is present once.
    assert len(committed) == 18
    ctw = [e for e in committed if e["subject"] == "chinese-tech-wire"]
    assert len(ctw) == 2
    com001 = [e for e in ctw if e["standard"] == "STD-DEPLOY-COM-001"]
    assert len(com001) == 1
    assert CTW_SHA in com001[0]["summary"]
    assert TARGET in com001[0]["summary"]
    assert com001[0]["source_reference"] == "audits/ctw-deployment-proof-m52-2026-09-05.md"


def test_m52_prior_admissions_preserved_verbatim():
    committed = json.loads(KNOWN.read_text(encoding="utf-8"))
    pairs = {(e["subject"], e["standard"]) for e in committed}
    # Subset, not equality: the intent is that no prior admission was dropped
    # or rewritten. M57 later added Watch and Smartphone COM-002 (M56 debts
    # D8/D9); that is a legitimate later admission, not an M52 regression.
    assert {
        ("chinese-tech-wire", "STD-DEPLOY-COM-001"),
        ("chinese-tech-wire", "STD-DEPLOY-COM-002"),
        ("feature-phone-clank", "STD-DEPLOY-COM-001"),
        ("feature-phone-clank", "STD-DEPLOY-COM-002"),
        ("korean-tech-wire", "STD-DEPLOY-COM-001"),
        ("korean-tech-wire", "STD-DEPLOY-COM-002"),
        ("oem-radar", "STD-DEPLOY-COM-001"),
        ("oem-radar", "STD-DEPLOY-COM-002"),
        ("semiconductor-intelligence", "STD-DEPLOY-COM-001"),
        ("semiconductor-intelligence", "STD-DEPLOY-COM-002"),
        ("smartphone-clank", "STD-DEPLOY-COM-001"),
        ("smartwatch-clank", "STD-DEPLOY-COM-001"),
        ("smartwatch-clank", "STD-DEPLOY-COM-002"),
        ("tablet-clank", "STD-DEPLOY-COM-001"),
        ("tablet-clank", "STD-DEPLOY-COM-002"),
        ("watch-clank", "STD-DEPLOY-COM-001"),
    } <= pairs


def test_m52_audit_md_carries_parsable_json_block():
    text = AUDIT_MD.read_text(encoding="utf-8")
    start = text.index("```json")
    end = text.index("```", start + 7)
    block = json.loads(text[start + 7:end])
    assert block["clank"] == "chinese-tech-wire"
    assert len(block["findings"]) == 1
    finding = block["findings"][0]
    assert finding["standard"] == "STD-DEPLOY-COM-001"
    assert "LIVE_PROOF_CONFIRMED" in finding["summary"]
    assert CTW_SHA in finding["summary"]
    assert TARGET in finding["summary"]
    assert "barrier HELD" in finding["summary"]


# -- AH: frozen standards/tags unchanged ---------------------------------------------------------------------------


def _lf_pinned_artifacts(manifest: dict):
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


def test_m52_frozen_standards_unchanged():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["status"] == "FROZEN"
    pinned = _lf_pinned_artifacts(manifest)
    assert pinned
    for path, expected in pinned:
        raw = (ROOT / path).read_bytes().replace(b"\r\n", b"\n")
        assert hashlib.sha256(raw).hexdigest() == expected, f"frozen artifact drifted: {path}"


def test_m52_frozen_tags_have_not_moved():
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
