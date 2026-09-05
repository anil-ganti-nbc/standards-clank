"""M55: Semiconductor DEPLOY-COM-001 live-proof admission guards."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from tools.deployment_agent_layer import build_known_evidence_index

ROOT = Path(__file__).resolve().parents[1]
AUDIT_JSON = ROOT / "audits" / "semiconductor-deployment-proof-m55-2026-09-05.json"
AUDIT_MD = ROOT / "audits" / "semiconductor-deployment-proof-m55-2026-09-05.md"
KNOWN = ROOT / "standards" / "deployment" / "known-evidence-index.json"
MANIFEST = ROOT / "baselines" / "deployment-standards-v1.0.json"

SEMI_SHA = "53cb3f1f5358ad28a2d92ebd78efeab9534ddfa1"
PRE_SOURCE = "ece4b001c60dd156c2a05cb92cf0ea335e0532c6"
TARGET = "Hetzner:/home/deploy/staging/semiconductor-intelligence"
MECHANISM = ("cron 40 * * * * -> deploy_run.sh -> Docker Compose one-shot semi-intel "
             "-> semintel automation cycle (OperationalScheduler DB job lease)")
PRE_ALEMBIC = "a0b1c2d3e404"
CANON_HEAD = "c7d8e9f0a1b2"
MID_REVISION = "bf599f950d56"
CHAIN = [PRE_ALEMBIC, MID_REVISION, CANON_HEAD]
BACKUP_SHA = "e5f2ac6f49e020b87e9e70b34d0847273771f932a29c4adc2d34151a27be2944"
DEPLOY_SH_SHA = "385d7c4424fac0f0048181ed2d36544d4a208d438cae4469cac3b60714a082a2"
COMPOSE_SHA = "8b6e62d608ad24cce37cf1a6594f7d2def92a3bf9fe86250966b6a6f49e080c9"
LOCK_TOKEN = "23a4ac76f6c149f99e2b22da779b1645"
M11_SEMI_COM002_SHA = "8085a1bbd1a4e133680702e8c1d916b71bb78a14"


def _record() -> dict:
    return json.loads(AUDIT_JSON.read_text(encoding="utf-8"))


# -- A-D: exact subject, source SHA, target, verdict ---------------------------


def test_m55_records_exact_subject_source_target_and_verdict():
    record = _record()
    semi = record["semiconductor"]
    assert semi["target"] == "semiconductor-intelligence"
    assert semi["head"] == SEMI_SHA
    assert semi["origin_main"] == SEMI_SHA
    assert semi["standard"] == "STD-DEPLOY-COM-001"
    assert semi["state"] == "LIVE_PROOF_CONFIRMED"
    assert semi["lifecycle"] == "CLOSED"
    assert semi["deployment_target"] == TARGET
    assert semi["deployment_mechanism"] == MECHANISM
    assert "delivery OFF" in semi["scope"]


# -- E-F: pre-source and pre-Alembic --------------------------------------------


def test_m55_records_pre_deploy_state():
    pre = _record()["pre_deploy_state"]
    assert pre["live_source"] == PRE_SOURCE
    assert pre["classification"] == "BEHIND_CANON"
    assert pre["commits_behind"] == 4
    assert len(pre["intervening_commits"]) == 4
    assert pre["pre_live_image"] == "semi-intel:ece4b00"
    db = pre["db"]
    assert db["size_bytes"] == 10231808
    assert db["sha256"] == "fd4ce3e8edd72c82bd5876d54431055cffb74721378b6fd5240cf743f2e27ebb"
    assert db["quick_check"] == "ok"
    assert db["tables"] == 50
    assert db["alembic_revision"] == PRE_ALEMBIC
    assert db["self_consistent_with_ece4b00"] is True
    assert db["run_frontier"] == 344
    assert db["sources"] == 1


# -- G-H: canonical head + exact two-revision chain -------------------------------


def test_m55_canonical_head_and_migration_chain():
    pre = _record()["pre_deploy_state"]
    assert pre["canonical_head"] == CANON_HEAD
    assert pre["migration_required_before_canon"] is True
    assert pre["db"]["self_consistent_with_ece4b00"] is True
    scratch = _record()["scratch_migration"]
    assert scratch["chain"] == CHAIN
    assert _record()["live_migration"]["chain"] == CHAIN
    assert CHAIN[1] == MID_REVISION and len(CHAIN) == 3


# -- I: backup identity --------------------------------------------------------------


def test_m55_backup_identity():
    backup = _record()["backup"]
    assert backup["path_suffix"].endswith("semi-intel-backup-20260905T121316.967010Z.sqlite3")
    assert backup["size_bytes"] == 10231808
    assert backup["sha256"] == BACKUP_SHA
    assert backup["quick_check"] == "ok"
    assert backup["alembic_revision"] == PRE_ALEMBIC
    assert backup["runs"] == 344
    assert backup["manifest"].endswith(".manifest.json (507 bytes)")
    assert backup["prior_backups_untouched"] is True


# -- J: quiet-window / no-active-lease --------------------------------------------------


def test_m55_quiet_window_and_lease_gate():
    quiet = _record()["quiet_window"]
    assert quiet["running_jobs"] == 0
    assert quiet["active_leases"] == 0
    assert "between the 11:40 fire" in quiet["window_utc"]
    assert quiet["cron_unchanged"] == "40 * * * *"


# -- K: dependency diff empty --------------------------------------------------------------


def test_m55_dependency_gate():
    assert _record()["source_preparation"]["dependency_diff_lines"] == 0


# -- L: canonical image identity --------------------------------------------------------------


def test_m55_canonical_image_identity():
    prep = _record()["source_preparation"]
    assert prep["canonical_image"] == f"semi-intel:{SEMI_SHA}"
    assert prep["image_id"] == "e3d65d657eeb"
    assert prep["fast_forward"] == "ece4b00 -> 53cb3f1 confirmed via merge-base"
    assert "detached temp worktree" in prep["build_context"]


# -- M: runtime source_revision remains honestly unknown ------------------------------------------


def test_m55_identity_limitation_recorded_honestly():
    ident = _record()["identity_limitation"]
    assert ident["oci_revision_label"] == "absent"
    assert ident["identity_source_revision"] == "unknown"
    assert ident["recorded_honestly"] is True
    assert ident["unknown_converted_to_revision_claim"] is False
    proven = ident["identity_proven_through"]
    assert any(SEMI_SHA in p for p in proven)
    assert any(DEPLOY_SH_SHA in p for p in proven)
    assert any(COMPOSE_SHA in p for p in proven)
    assert any("qualification_provenance" in p for p in proven)


# -- N: scratch target proven -----------------------------------------------------------------------


def test_m55_scratch_targeting_proven():
    targeting = _record()["scratch_migration"]["targeting_proof"]
    assert targeting["classification"] == "SCRATCH_TARGET_PROVEN_BEFORE_MUTATION"
    assert targeting["marker"] == "m54-scratch-mount-marker read inside canonical container"
    assert targeting["live_db_excluded"] is True
    assert targeting["live_mis_target"] is False
    assert "e5f2ac6f" in targeting["source"]


# -- O-P: exact +3 tables and +3 nullable columns ------------------------------------------------------


def test_m55_exact_schema_delta():
    delta = _record()["scratch_migration"]["schema_delta"]
    assert delta["added_tables"] == ["candidate_reviews", "qualification_epochs", "qualification_events"]
    assert delta["added_nullable_columns_on_operational_job_runs"] == [
        "qualification_provenance", "qualification_material_identity", "qualification_epoch_id",
    ]
    assert delta["existing_row_transformation"] is False
    assert delta["destructive_schema_action"] is False
    assert delta["pre_existing_data_preserved"] is True
    detail = delta["candidate_reviews_detail"]
    assert "disposition Enum" in detail and "signal_candidates" in detail


# -- Q: backup_records artifact explained -----------------------------------------------------------------


def test_m55_backup_records_artifact_explained():
    artifact = _record()["scratch_migration"]["backup_records_artifact"]
    assert artifact["observed"] == "1 -> 0"
    assert artifact["classification"] == "COMPARISON_BASE_ARTIFACT"
    assert artifact["not_migration_data_loss"] is True
    assert artifact["verified_against"] == {"backup_file_rows": 0, "live_rows": 1}


# -- R: scratch health --------------------------------------------------------------------------------------


def test_m55_scratch_acceptance_qualified():
    acc = _record()["scratch_migration"]["acceptance"]
    assert acc["alembic_post"] == CANON_HEAD
    assert acc["quick_check"] == "ok"
    assert acc["tables"] == 53
    assert acc["expected_plus3_tables_present"] is True
    assert acc["expected_nullable_columns_present"] is True
    assert acc["pre_existing_rows_preserved"] is True
    assert acc["health"] == "healthy"
    assert acc["readiness"] is True
    assert acc["implicit_collection"] is False
    assert acc["qualification"] == "QUALIFIED"


# -- S: live migration matched scratch -----------------------------------------------------------------------


def test_m55_live_migration_matched_scratch():
    live = _record()["live_migration"]
    for gate in ("backup verified", "scratch targeting proven", "scratch migration PASS",
                 "scratch health PASS", "no live lease active", "canonical image built"):
        assert gate in live["gates_met"], gate
    assert live["result_matched_scratch"] is True
    assert live["chain"] == CHAIN
    assert live["post"]["tables"] == 53
    assert live["post"]["runs"] == 344
    assert live["post"]["schema_delta_matched_scratch"] is True


# -- T-U: pointer transition + unchanged wiring ----------------------------------------------------------------


def test_m55_pointer_transition_and_wiring_unchanged():
    pointer = _record()["pointer_transition"]
    assert pointer["from"] == "ece4b00"
    assert pointer["to"] == SEMI_SHA
    assert pointer["file"] == ".deployed-id"
    assert pointer["tracked_wiring_unchanged"] is True
    assert pointer["deploy_run_sh_sha256"] == DEPLOY_SH_SHA
    assert pointer["compose_sha256"] == COMPOSE_SHA


# -- V-X: cron, scope, delivery ---------------------------------------------------------------------------------


def test_m55_operational_contract_preserved():
    contract = _record()["operational_contract"]
    assert contract["cron"] == "40 * * * *"
    assert contract["command"] == ("deploy_run.sh -> docker compose run --rm semi-intel "
                                   "-> semintel automation cycle")
    assert contract["scope"] == "1 configured source"
    assert contract["source_name"] == "PCI ID Repository"
    assert contract["source_kind"] == "REGISTRY"
    assert contract["delivery"].startswith("OFF")
    assert contract["cadence_or_scope_change"] is False


# -- Y: dashboard N/A -----------------------------------------------------------------------------------------------


def test_m55_dashboard_not_applicable():
    assert _record()["operational_contract"]["dashboard"] == "NOT_DEPLOYED / NOT_APPLICABLE"


# -- Z: DB lease authority ---------------------------------------------------------------------------------------------


def test_m55_lease_authority():
    excl = _record()["exclusivity_authority"]
    assert excl["mechanism"] == "OperationalScheduler DB-level job lease"
    assert excl["table"] == "operational_job_leases"
    assert any("lock_token" in f for f in excl["fields"])
    assert any("expires_at" in f for f in excl["fields"])
    assert excl["host_flock_claimed"] is False


# -- AA-AC: run 345 authoritative, SCHEDULED, qualification_provenance --------------------------------------------------


def test_m55_run_345_authoritative_with_canon_era_provenance():
    run = _record()["natural_proof"]["authoritative_run"]
    assert run["run_id"] == 345
    assert run["job_type"] == "PIPELINE"
    assert run["trigger_type"] == "SCHEDULED"
    assert run["status"] == "SUCCESSFUL"
    assert run["started_utc"] == "2026-09-05T12:40:03.801568Z"
    assert run["finished_utc"] == "2026-09-05T12:42:06.589977Z"
    assert run["cron_fire_utc"] == "2026-09-05T12:40:01Z"
    assert run["attempt"] == 1
    assert run["owner_identity"] == "129eedf7cd50:1"
    assert run["lock_token"] == LOCK_TOKEN
    assert run["qualification_provenance"] == "scheduled"
    provenance = _record()["natural_proof"]["canon_era_durable_provenance"]
    assert provenance["field"] == "qualification_provenance"
    assert "not alone as a source-SHA proof" in provenance["interpretation"]


# -- AD: registry result -------------------------------------------------------------------------------------------------


def test_m55_registry_result_not_failure():
    registry = _record()["natural_proof"]["registry_result"]
    assert registry == {"new": 0, "duplicates": 21475, "errors": 0,
                        "classified": "established full-registry sweep behaviour, not failure"}


# -- AE-AF: continuity + barrier -------------------------------------------------------------------------------------------


def test_m55_continuity_and_barrier():
    proof = _record()["natural_proof"]
    cont = proof["continuity"]
    assert cont["operational_job_runs"] == "344 -> 345"
    assert cont["source_count"] == 1
    for flag in ("run_history_break", "identity_reset", "source_count_change",
                 "duplicate_explosion", "false_novelty", "lease_regression", "failed_transition"):
        assert cont[flag] is False, flag
    barrier = proof["barrier"]
    assert barrier["classification"] == "BARRIER_HELD"
    assert barrier["alembic_after_natural_run"] == CANON_HEAD
    assert barrier["hidden_bootstrap_or_downgrade"] is False


# -- AG: diagnostic-string test debt classified ------------------------------------------------------------------------------


def test_m55_red_test_debt_classified_not_laundered():
    debt = _record()["historical_test_debt"]
    assert debt["classification"] == "CURRENT_FAILURE_REPRODUCED_DEPLOYMENT_IRRELEVANT"
    assert "diagnostic-string" in debt["nature"]
    for prop in debt["substantive_property_holds"]:
        assert prop
    assert debt["m53_suite_was_not_green"]["failed"] == 12
    assert debt["source_suite_claimed_green"] is False
    assert debt["repaired_in_standards"] is False
    assert debt["com001_blocker"] is False


# -- AH-AI: rollback paired; no rollback ---------------------------------------------------------------------------------------


def test_m55_rollback_paired_rule_not_triggered():
    rollback = _record()["rollback"]
    assert rollback["triggered"] is False
    assert rollback["paired_rule_preserved"] is True
    assert "never one component alone" in rollback["rule"]
    assert rollback["old_image_retained"] == "semi-intel:ece4b00"


# -- AJ: exact scope / no inheritance -------------------------------------------------------------------------------------------


def test_m55_exact_scope_no_inheritance():
    record = _record()
    assert "delivery OFF" in record["semiconductor"]["scope"]
    guards = record["guards"]
    for key in ("frozen_standard_files_changed", "frozen_tags_changed_or_moved",
                "semiconductor_source_modified_in_this_pass",
                "hetzner_accessed_in_this_standards_pass", "com002_reclosed",
                "diagnostic_string_test_fixed", "generalization_to_future_shas",
                "generalization_to_other_targets", "full_target_conformance_claim"):
        assert guards[key] is False, key


# -- (§3) COM-002 closure preserved -----------------------------------------------------------------------------------------------


def test_m55_preserves_m11_com002_closure():
    record = _record()
    preserved = record["known_evidence_admission"]["com002_closure_preserved"]
    assert "CONFORMS/CLOSED" in preserved and M11_SEMI_COM002_SHA[:7] in preserved
    assert record["guards"]["com002_reclosed"] is False


# -- evidence-index admission -------------------------------------------------------------------------------------------------------


def test_m55_known_evidence_index_admits_semi_com001():
    committed = json.loads(KNOWN.read_text(encoding="utf-8"))
    assert committed == build_known_evidence_index(), "committed index is stale vs audits/*.md"
    # M57 resolved M56 debts D8/D9 by admitting Watch's and Smartphone's
    # already-concluded COM-002 facts, taking the index 16 -> 18. This
    # mission's own admission is unchanged; the global total is no longer
    # pinned here, since a later legitimate admission is not this test's
    # concern. What must still hold: this mission's fact is present once.
    assert len(committed) == 18
    semi = [e for e in committed if e["subject"] == "semiconductor-intelligence"]
    assert len(semi) == 2
    com001 = [e for e in semi if e["standard"] == "STD-DEPLOY-COM-001"]
    assert len(com001) == 1
    assert SEMI_SHA in com001[0]["summary"]
    assert TARGET in com001[0]["summary"]
    assert com001[0]["source_reference"] == "audits/semiconductor-deployment-proof-m55-2026-09-05.md"


def test_m55_prior_admissions_preserved_verbatim():
    committed = json.loads(KNOWN.read_text(encoding="utf-8"))
    pairs = {(e["subject"], e["standard"]) for e in committed}
    expected = {
        ("semiconductor-intelligence", "STD-DEPLOY-COM-001"),
        ("semiconductor-intelligence", "STD-DEPLOY-COM-002"),
        ("feature-phone-clank", "STD-DEPLOY-COM-001"),
        ("feature-phone-clank", "STD-DEPLOY-COM-002"),
        ("korean-tech-wire", "STD-DEPLOY-COM-001"),
        ("korean-tech-wire", "STD-DEPLOY-COM-002"),
        ("oem-radar", "STD-DEPLOY-COM-001"),
        ("oem-radar", "STD-DEPLOY-COM-002"),
        ("smartphone-clank", "STD-DEPLOY-COM-001"),
        ("smartwatch-clank", "STD-DEPLOY-COM-001"),
        ("smartwatch-clank", "STD-DEPLOY-COM-002"),
        ("tablet-clank", "STD-DEPLOY-COM-001"),
        ("tablet-clank", "STD-DEPLOY-COM-002"),
        ("watch-clank", "STD-DEPLOY-COM-001"),
        ("chinese-tech-wire", "STD-DEPLOY-COM-001"),
        ("chinese-tech-wire", "STD-DEPLOY-COM-002"),
    }
    # Subset, not equality: the intent is that no prior admission was
    # dropped or rewritten. M57 later admitted Watch and Smartphone
    # COM-002 (resolving M56 debts D8/D9) - a legitimate later
    # admission, not a regression of this mission.
    assert expected <= pairs
    com001_subjects = {s for s, st in pairs if st == "STD-DEPLOY-COM-001"}
    assert len(com001_subjects) == 9


def test_m55_audit_md_carries_parsable_json_block():
    text = AUDIT_MD.read_text(encoding="utf-8")
    start = text.index("```json")
    end = text.index("```", start + 7)
    block = json.loads(text[start + 7:end])
    assert block["clank"] == "semiconductor-intelligence"
    assert len(block["findings"]) == 1
    finding = block["findings"][0]
    assert finding["standard"] == "STD-DEPLOY-COM-001"
    assert "LIVE_PROOF_CONFIRMED" in finding["summary"]
    assert SEMI_SHA in finding["summary"]
    assert TARGET in finding["summary"]
    assert "BARRIER_HELD" in finding["summary"]
    assert "COMPARISON_BASE_ARTIFACT" in finding["summary"]


# -- AK: frozen standards/tags unchanged -----------------------------------------------------------------------------------------------


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


def test_m55_frozen_standards_unchanged():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["status"] == "FROZEN"
    pinned = _lf_pinned_artifacts(manifest)
    assert pinned
    for path, expected in pinned:
        raw = (ROOT / path).read_bytes().replace(b"\r\n", b"\n")
        assert hashlib.sha256(raw).hexdigest() == expected, f"frozen artifact drifted: {path}"


def test_m55_frozen_tags_have_not_moved():
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
