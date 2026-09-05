"""M58 whole-project closure audit guards.

M58 independently determined that Standards Clank is complete under charter
section F, with non-blocking debt. It is a RECORDING artifact: it ratifies
nothing, admits no fact, and creates no obligation.

Deliberately NOT pinned: current external repo HEADs. Those are volatile
observations; pinning them would manufacture false debt the moment any fleet
repo legitimately moves, which is exactly the drift this closure classifies as
operational rather than normative.
"""

import json
import re
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
CLOSURE_MD = REPO / "audits" / "standards-clank-final-closure-m58-2026-09-05.md"
CLOSURE_JSON = REPO / "audits" / "standards-clank-final-closure-m58-2026-09-05.json"
CHARTER = REPO / "docs" / "charter.md"
DEPLOY_INDEX = REPO / "standards" / "deployment" / "known-evidence-index.json"
UI_FACTS = REPO / "standards" / "ui" / "evidence-facts.json"

FROZEN_TAGS = {
    "ui-standards-v1.0": "d11320704aed69a3d8f854c9264b184e392ec80f",
    "deployment-standards-v1.0": "33cc38849180716fd4d06b1356cf70c49d3d41d2",
    "operations-standards-v1.0": "7100f294a83c30594f2ff9e953f7c9f77a95747f",
    "data-ontology-standards-v1.0": "464a8057ea5dc26ef83248a20bafa0be5aa31148",
    "collector-ui-design-standards-v1.0": "f81f4ffa91e9a7af2f80195339d2762180a3154e",
}
FROZEN_DOMAINS = {"ui", "data-ontology", "operations", "deployment", "collector-ui-design"}


@pytest.fixture(scope="module")
def closure():
    return json.loads(CLOSURE_JSON.read_text(encoding="utf-8"))


def _git(*args):
    return subprocess.run(
        ["git", "-C", str(REPO), *args], capture_output=True, text=True,
        encoding="utf-8", stdin=subprocess.DEVNULL, check=True,
    ).stdout.strip()


# -- the artifact is a recording, not a standard --

def test_closure_artifacts_exist():
    assert CLOSURE_MD.is_file() and CLOSURE_JSON.is_file()
    assert len(CLOSURE_MD.read_text(encoding="utf-8")) > 5000


def test_closure_artifact_is_non_normative(closure):
    assert closure["artifact_kind"] == "RECORDING"
    assert closure["is_normative_standard"] is False
    assert closure["creates_obligation"] is False
    assert closure["admits_facts"] is False


def test_closure_findings_block_is_empty_so_no_index_changes():
    block = json.loads(re.search(r"```json\s*\n(.*?)\n```", CLOSURE_MD.read_text(encoding="utf-8"), re.DOTALL).group(1))
    for key in ("clank", "date", "findings"):
        assert key in block
    assert block["findings"] == []


def test_closure_creates_no_standard_file():
    assert not list((REPO / "standards").rglob("STD-M58*"))
    assert not list((REPO / "standards").rglob("*closure*"))


# -- exact frozen domain set, no PROPOSED anywhere --

def test_exact_frozen_domain_set(closure):
    declared = {d["domain"] for d in closure["frozen_domains"]}
    assert declared == FROZEN_DOMAINS
    populated = {
        p.name for p in (REPO / "standards").iterdir()
        if p.is_dir() and list(p.glob("STD-*.json"))
    }
    assert populated == FROZEN_DOMAINS


def test_no_proposed_standards_anywhere():
    statuses = []
    for p in (REPO / "standards").rglob("STD-*.json"):
        statuses.append(json.loads(p.read_text(encoding="utf-8"))["status"])
    assert len(statuses) == 26
    assert set(statuses) == {"RATIFIED"}, f"non-ratified normative standard present: {set(statuses)}"


def test_closure_totals_match_reality(closure):
    assert closure["totals"]["standards"] == 26
    assert closure["totals"]["ratified"] == 26
    assert closure["totals"]["proposed"] == 0


# -- frozen integrity --

@pytest.mark.parametrize("tag,expected", sorted(FROZEN_TAGS.items()))
def test_frozen_tag_unmoved(tag, expected):
    assert _git("rev-parse", f"{tag}^{{commit}}") == expected


def test_all_frozen_normative_files_byte_identical():
    domain_tag = {
        "ui": "ui-standards-v1.0",
        "data-ontology": "data-ontology-standards-v1.0",
        "operations": "operations-standards-v1.0",
        "deployment": "deployment-standards-v1.0",
        "collector-ui-design": "collector-ui-design-standards-v1.0",
    }
    checked = 0
    for domain, tag in domain_tag.items():
        for path in _git("ls-tree", "-r", "--name-only", tag, "--", f"standards/{domain}").splitlines():
            name = path.rsplit("/", 1)[-1]
            if not (name.startswith("STD-") and name.endswith(".json")):
                continue
            assert _git("rev-parse", f"{tag}:{path}") == _git("rev-parse", f"HEAD:{path}"), path
            checked += 1
    assert checked == 26


def test_closure_records_frozen_integrity(closure):
    fi = closure["frozen_integrity"]
    assert fi["tags_verified"] == 5
    assert fi["tags_moved"] == 0
    assert fi["normative_files_changed"] == 0
    assert fi["removals_from_frozen_dirs"] == 0
    assert fi["post_freeze_additions_are_evidence_layer_only"] is True


# -- deployment closure: 9 + 9 --

def test_nine_com_001_and_nine_com_002():
    idx = json.loads(DEPLOY_INDEX.read_text(encoding="utf-8"))
    c1 = [e for e in idx if e["standard"] == "STD-DEPLOY-COM-001"]
    c2 = [e for e in idx if e["standard"] == "STD-DEPLOY-COM-002"]
    assert len(c1) == 9
    assert len(c2) == 9
    assert len(idx) == 18
    assert {e["subject"] for e in c1} == {e["subject"] for e in c2}
    keys = [(e["standard"], e["subject"]) for e in idx]
    assert len(keys) == len(set(keys))


def test_closure_records_deployment_closure(closure):
    dc = closure["deployment_closure"]
    assert dc["com_001_applicable"] == dc["com_001_closed"] == 9
    assert dc["com_002_applicable"] == dc["com_002_closed"] == 9
    assert dc["total_facts"] == 18
    assert dc["current_canon_drift_distinguished_from_closure"] is True


# -- six CUD facts intact --

def test_six_cud_facts_conforms_and_source_verification():
    facts = json.loads(UI_FACTS.read_text(encoding="utf-8"))
    cud = [f for f in facts if f.get("standard_id") == "STD-CUD-001"]
    assert len(cud) == 6
    assert all(f["verdict"] == "CONFORMS" for f in cud)
    assert all(f["role"] == "CURRENT" for f in cud)
    assert all(f["provenance"]["kind"] == "source_verification" for f in cud)


def test_closure_does_not_claim_cud_is_live(closure):
    cud = closure["cud_integrity"]
    assert cud["source_conformance_implies_latest_live"] is False
    assert cud["any_live_proof_language"] is False


# -- M56 drift verdict preserved, not converted into Standards debt --

def test_m56_drift_verdict_preserved():
    m56 = json.loads((REPO / "audits" / "fleet-deploy-com-001-reconciliation-m56-2026-09-05.json").read_text(encoding="utf-8"))
    assert m56["fleet_verdict"] == "FLEET_DEPLOY_COM_001_CLOSED_HISTORICALLY_BUT_CURRENT_DRIFT_EXISTS"
    assert m56["deployment_fact_accounting"]["total_facts"] == 16, "M56 snapshot must not be retro-edited"


def test_drift_classified_operational_not_normative(closure):
    d = closure["current_canon_drift"]
    assert d["charter_requires_continuous_newest_canon_congruence"] is False
    assert d["classification"] == "OPERATIONAL_REVALIDATION"
    assert d["is_standards_blocker"] is False
    assert len(d["targets_behind_canon"]) == 5
    assert len(d["targets_congruent_at_m56"]) == 4


def test_no_current_canon_liveness_claim_invented(closure):
    flat = re.sub(r"\s+", " ", CLOSURE_MD.read_text(encoding="utf-8"))
    assert "LIVE_PROOF_CONFIRMED" not in flat, "a closure recording must not assert live proof"
    assert closure["actions_not_taken"], "actions-not-taken list must be present"
    joined = " ".join(closure["actions_not_taken"]).lower()
    assert "no current-canon liveness claim invented" in joined


# -- charter section F basis explicitly recorded --

def test_charter_f_basis_recorded_and_matches_the_charter(closure):
    basis = closure["charter_completion_basis"]
    assert basis["source"] == "docs/charter.md section F"
    assert basis["runtime_state_clause_present"] is False
    charter_flat = re.sub(r"\s+", " ", CHARTER.read_text(encoding="utf-8"))
    assert basis["rule"] in charter_flat, "recorded rule must be the charter's actual text"


def test_zero_unresolved_normative_concerns(closure):
    cls = closure["charter_f_concern_classification"]
    assert cls["UNRESOLVED"] == 0
    assert cls["STANDARDIZED"] == 26
    for bucket in ("REHOMED", "HELD_WITH_TRIGGER", "REJECTED"):
        assert cls[bucket], f"{bucket} must be explicitly enumerated"
    assert len(cls["corroborating_final_gap_conclusions"]) == 4


# -- debt register preserved, none blocking --

def test_debt_register_present_and_no_blocking_debt(closure):
    reg = closure["debt_register"]
    assert len(reg) >= 13
    assert closure["blocking_debts"] == 0
    assert not [d for d in reg if d["classification"] == "BLOCKING"]
    valid = {"BLOCKING", "NON_BLOCKING_HISTORICAL", "OPERATIONAL_REVALIDATION",
             "SOURCE_TEST_DEBT", "DOCUMENTATION_DEBT", "EVIDENCE_MODEL_DEBT", "RESOLVED"}
    assert all(d["classification"] in valid for d in reg)


def test_d8_d9_recorded_resolved_without_retro_editing_m56(closure):
    reg = {d["id"]: d for d in closure["debt_register"]}
    assert reg["D8"]["classification"] == "RESOLVED"
    assert reg["D9"]["classification"] == "RESOLVED"
    assert closure["m56_register_retro_edited"] is False
    m56 = json.loads((REPO / "audits" / "fleet-deploy-com-001-reconciliation-m56-2026-09-05.json").read_text(encoding="utf-8"))
    m56_reg = {d["id"]: d for d in m56["historical_evidence_debt_register"]}
    assert m56_reg["D8"]["resolved"] is False, "the M56 snapshot keeps its own wording"
    assert m56_reg["D9"]["resolved"] is False


def test_source_test_debt_not_laundered(closure):
    assert closure["final_state_answers"]["H_source_test_debt_laundered_as_standards_success"] is False
    reg = {d["id"]: d for d in closure["debt_register"]}
    assert reg["D4"]["classification"] == "SOURCE_TEST_DEBT"


# -- verdict shape --

def test_verdict_is_one_of_the_five_permitted_values(closure):
    assert closure["final_verdict"] in {
        "STANDARDS_CLANK_COMPLETE",
        "STANDARDS_CLANK_COMPLETE_WITH_NON_BLOCKING_DEBT",
        "STANDARDS_CLANK_NOT_COMPLETE_BLOCKING_GAPS",
        "STANDARDS_CLANK_EVIDENCE_CONFLICT",
        "STANDARDS_CLANK_CHARTER_AMBIGUOUS",
    }


def test_verdict_consistent_with_debt_and_concerns(closure):
    """A complete verdict requires zero unresolved normative concerns; a
    with-debt verdict requires debt actually to exist."""
    if closure["final_verdict"].startswith("STANDARDS_CLANK_COMPLETE"):
        assert closure["charter_f_concern_classification"]["UNRESOLVED"] == 0
        assert closure["blocking_debts"] == 0
    if closure["final_verdict"] == "STANDARDS_CLANK_COMPLETE_WITH_NON_BLOCKING_DEBT":
        live = [d for d in closure["debt_register"] if d["classification"] != "RESOLVED"]
        assert live, "with-non-blocking-debt requires at least one live debt"


def test_domain_verdicts_cover_all_five_domains(closure):
    dv = closure["domain_verdicts"]
    assert set(dv) == {"UI", "DATA_ONTOLOGY", "OPERATIONS", "DEPLOYMENT", "COLLECTOR_UI_DESIGN"}
    valid = {"COMPLETE", "COMPLETE_WITH_NON_BLOCKING_DEBT", "NOT_COMPLETE", "CONFLICT"}
    assert set(dv.values()) <= valid
    assert "NOT_COMPLETE" not in dv.values()
    assert "CONFLICT" not in dv.values()


def test_final_state_answers_complete_and_consistent(closure):
    a = closure["final_state_answers"]
    assert set(a) == {
        "A_all_frozen_standards_intact", "B_proposed_standards_awaiting_ratification",
        "C_all_charter_required_normative_concerns_resolved", "D_all_nine_com_001_targets_closed",
        "E_all_nine_com_002_targets_closed", "F_m56_drift_is_a_standards_blocker",
        "G_historical_debts_block_completion", "H_source_test_debt_laundered_as_standards_success",
        "I_host_or_source_work_required_before_completion", "J_can_be_archived_as_complete",
    }
    assert a["A_all_frozen_standards_intact"] is True
    assert a["B_proposed_standards_awaiting_ratification"] is False
    assert a["C_all_charter_required_normative_concerns_resolved"] is True
    assert a["D_all_nine_com_001_targets_closed"] is True
    assert a["E_all_nine_com_002_targets_closed"] is True
    assert a["I_host_or_source_work_required_before_completion"] is False
    assert a["J_can_be_archived_as_complete"] is True


def test_publication_note_recorded_honestly(closure):
    """M57 was unpushed at audit time; the closure must say so rather than
    silently assess against an assumed-pushed canon."""
    assert "publication_note" in closure
    assert closure["origin_master_at_audit"] != closure["audited_head"]
    assert any("push" in w.lower() for w in closure["remaining_required_work"])


def test_no_self_ratification_violation_recorded(closure):
    sr = closure["self_ratification_audit"]
    assert sr["violations_found"] == 0
    for key in ("implementation_treated_as_law", "source_fix_used_to_self_ratify",
                "historical_unknown_laundered_into_conforms",
                "tests_pass_used_as_sole_normative_proof"):
        assert sr[key] is False
    assert sr["standards_traced_to_accepted_operator_decisions"] == 26
