"""M57 DEPLOY-COM-002 fleet completeness / evidence-model repair guards.

M57 resolved M56's debts D8 (Watch COM-002 in prose only) and D9 (Smartphone
COM-002 unadmitted) by tracing each to its underlying evidence, independently
re-verifying that evidence against the frozen standard at an exact source
revision, and admitting the two already-concluded facts. COM-002 goes 7 -> 9.

M57 made no host action, no deployment, no migration, no source modification,
altered no frozen standard, and re-scoped no COM-001 fact.
"""

import json
import re
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
DEPLOY_INDEX = REPO / "standards" / "deployment" / "known-evidence-index.json"
UI_FACTS = REPO / "standards" / "ui" / "evidence-facts.json"
MATRIX = REPO / "audits" / "deploy-com-002-fleet-completeness-m57-2026-09-05.md"
WATCH_ADMISSION = REPO / "audits" / "watch-deploy-com-002-m57-2026-09-05.md"
SMARTPHONE_ADMISSION = REPO / "audits" / "smartphone-deploy-com-002-m57-2026-09-05.md"
M56_RECON = REPO / "audits" / "fleet-deploy-com-001-reconciliation-m56-2026-09-05.json"

NAMED_TARGETS = {
    "watch-clank", "korean-tech-wire", "tablet-clank", "feature-phone-clank",
    "oem-radar", "smartwatch-clank", "smartphone-clank", "chinese-tech-wire",
    "semiconductor-intelligence",
}


@pytest.fixture(scope="module")
def index():
    return json.loads(DEPLOY_INDEX.read_text(encoding="utf-8"))


def _com(index, sid):
    return [e for e in index if e["standard"] == sid]


# -- COM-002 expected subject / applicability set --

def test_com_002_covers_all_nine_applicable_targets(index):
    """Applicability was determined from the frozen trigger plus each Clank's
    architecture, not from whether a fact already existed. All nine carry
    persistent structured state under an independently evolving contract, so
    the denominator is 9, not 7."""
    subjects = {e["subject"] for e in _com(index, "STD-DEPLOY-COM-002")}
    assert subjects == NAMED_TARGETS


def test_deployment_index_is_eighteen_facts(index):
    assert len(index) == 18
    assert len(_com(index, "STD-DEPLOY-COM-001")) == 9
    assert len(_com(index, "STD-DEPLOY-COM-002")) == 9


def test_no_duplicate_standard_subject_pair(index):
    keys = [(e["standard"], e["subject"]) for e in index]
    assert len(keys) == len(set(keys)), "no fact may shadow another"


def test_no_shadow_admission_outside_the_two_ratified_standards(index):
    assert {e["standard"] for e in index} == {"STD-DEPLOY-COM-001", "STD-DEPLOY-COM-002"}
    assert {e["kind"] for e in index} == {"known_conformance"}


# -- the two new admissions: exact classification, source and SHA --

def test_watch_com_002_admission_exists_and_is_exactly_scoped(index):
    watch = [e for e in _com(index, "STD-DEPLOY-COM-002") if e["subject"] == "watch-clank"]
    assert len(watch) == 1
    e = watch[0]
    assert e["source_reference"] == "audits/watch-deploy-com-002-m57-2026-09-05.md"
    assert "d03bc4b2f90289686331af0447d5ca4e8cf55822" in e["summary"]
    assert "CONFORMS / CLOSED" in e["summary"]
    assert "no current-canon claim" in e["summary"]


def test_watch_d8_classified_recording_defect():
    text = WATCH_ADMISSION.read_text(encoding="utf-8")
    assert "WATCH_COM002_RECORDING_DEFECT" in text
    # the real provenance must be named, not the misleading prose cite
    assert "watch-clank-cross-domain-2026-09-01-reaudit.json" in text
    assert "M4G is not the origin" in text or "M4G is not the origin." in text


def test_watch_admission_verified_against_frozen_criteria():
    text = WATCH_ADMISSION.read_text(encoding="utf-8")
    for element in ("schema_check.py", "run_pipeline.py", "EXIT_SCHEMA_MISMATCH",
                    "tests/test_schema_check.py"):
        assert element in text, f"missing verification element: {element}"


def test_smartphone_com_002_admission_exists_and_is_exactly_scoped(index):
    sp = [e for e in _com(index, "STD-DEPLOY-COM-002") if e["subject"] == "smartphone-clank"]
    assert len(sp) == 1
    e = sp[0]
    assert e["source_reference"] == "audits/smartphone-deploy-com-002-m57-2026-09-05.md"
    assert "e514c45dca4cf966441c27799d98761096dc8c40" in e["summary"]
    assert "CONFORMS / CLOSED" in e["summary"]


def test_smartphone_d9_classified_recording_defect():
    text = SMARTPHONE_ADMISSION.read_text(encoding="utf-8")
    assert "SMARTPHONE_COM002_RECORDING_DEFECT" in text


def test_smartphone_admission_does_not_rest_on_the_live_migration():
    """The accidental live 0007->0008 transition must be corroboration only.
    M57 §14 forbids using it as the COM-002 proof basis."""
    text = SMARTPHONE_ADMISSION.read_text(encoding="utf-8")
    index_entry = json.loads(re.search(r"```json\s*\n(.*?)\n```", text, re.DOTALL).group(1))
    summary = index_entry["findings"][0]["summary"]
    assert "NOT the proof basis" in summary or "not used as COM-002 proof" in summary
    assert "expressly not used as COM-002 proof" in summary or "expressly not" in summary
    # the procedural deviation must still be preserved in the artifact
    assert "procedural deviation" in text
    assert "scratch" in text


def test_smartphone_admission_names_the_source_level_barrier():
    text = SMARTPHONE_ADMISSION.read_text(encoding="utf-8")
    for element in ("ensure_schema_or_refuse", "runtime/run_once.py",
                    "init_fresh_database", "test_schema_authority.py"):
        assert element in text, f"missing verification element: {element}"


# -- completeness matrix --

def test_completeness_matrix_covers_nine_targets_and_states_the_denominator():
    text = MATRIX.read_text(encoding="utf-8")
    for target in NAMED_TARGETS:
        assert target in text, f"{target} missing from the completeness matrix"
    flat = re.sub(r"\s+", " ", text)
    assert "9 applicable / 9 closed / 0 N/A" in flat
    assert "DEPLOY_COM_002_FLEET_COMPLETE" in text


def test_matrix_records_why_the_count_was_seven():
    """The structural explanation must be preserved: the 7 were the M10
    remediation cohort, not the applicable set."""
    flat = re.sub(r"\s+", " ", MATRIX.read_text(encoding="utf-8"))
    assert "remediation cohort" in flat
    assert "positive exception" in flat
    assert "fleet-persistent-state-compatibility-planning-m10" in flat


def test_matrix_states_source_level_proof_suffices_for_com_002():
    """The decision rule that distinguishes COM-002 from COM-001 must be
    explicit, since it is what licenses source-level closure."""
    flat = re.sub(r"\s+", " ", MATRIX.read_text(encoding="utf-8"))
    assert "materially running" in flat
    assert "source-level proof close it" in flat or "source-level" in flat


# -- no false current-canon claims anywhere in the new artifacts --

@pytest.mark.parametrize("path", [WATCH_ADMISSION, SMARTPHONE_ADMISSION, MATRIX])
def test_new_artifacts_make_no_current_canon_liveness_claim(path):
    flat = re.sub(r"\s+", " ", path.read_text(encoding="utf-8"))
    assert "LIVE_PROOF_CONFIRMED" not in flat, (
        "a COM-002 admission must not borrow COM-001's live-proof vocabulary"
    )


# -- COM-001 non-interference --

def test_com_001_untouched_nine_subjects_and_verdicts(index):
    com1 = _com(index, "STD-DEPLOY-COM-001")
    assert len(com1) == 9
    assert {e["subject"] for e in com1} == NAMED_TARGETS
    assert all("LIVE_PROOF_CONFIRMED" in e["summary"] for e in com1)
    assert all(e["kind"] == "known_conformance" for e in com1)


def test_m56_verdict_and_snapshot_unchanged():
    recon = json.loads(M56_RECON.read_text(encoding="utf-8"))
    assert recon["fleet_verdict"] == "FLEET_DEPLOY_COM_001_CLOSED_HISTORICALLY_BUT_CURRENT_DRIFT_EXISTS"
    # M56's own snapshot numbers are historical and must not be retro-edited
    assert recon["deployment_fact_accounting"]["total_facts"] == 16
    assert recon["deployment_fact_accounting"]["com_002_facts"] == 7
    assert recon["current_canon_observation"]["exact_current"] == 4
    assert recon["current_canon_observation"]["behind_current"] == 5


def test_m56_debt_register_chronology_preserved():
    """D8/D9 must remain in the M56 register as originally recorded. M57
    resolves them in its own artifacts; it does not erase history."""
    recon = json.loads(M56_RECON.read_text(encoding="utf-8"))
    reg = {d["id"]: d for d in recon["historical_evidence_debt_register"]}
    assert "D8" in reg and "D9" in reg
    assert reg["D8"]["subject"] == "watch-clank"
    assert reg["D9"]["subject"] == "smartphone-clank"
    assert reg["D8"]["resolved"] is False, "the M56 record is a snapshot; it stays as written"
    assert reg["D9"]["resolved"] is False


def test_m57_records_the_resolution_of_d8_and_d9():
    for path in (WATCH_ADMISSION, SMARTPHONE_ADMISSION):
        text = path.read_text(encoding="utf-8")
        assert re.search(r"Resolves M56 debt D[89]", text), f"{path.name}: no debt resolution recorded"


# -- CUD non-interference --

def test_six_cud_facts_intact_and_still_source_verification():
    facts = json.loads(UI_FACTS.read_text(encoding="utf-8"))
    cud = [f for f in facts if f.get("standard_id") == "STD-CUD-001"]
    assert len(cud) == 6
    assert all(f["verdict"] == "CONFORMS" for f in cud)
    assert all(f["role"] == "CURRENT" for f in cud)
    assert all(f["provenance"]["kind"] == "source_verification" for f in cud), (
        "CUD facts must never be retyped into deployment proof"
    )


# -- frozen integrity --

def _git(*args):
    return subprocess.run(
        ["git", "-C", str(REPO), *args], capture_output=True, text=True,
        encoding="utf-8", stdin=subprocess.DEVNULL, check=True,
    ).stdout.strip()


@pytest.mark.parametrize("tag,expected", [
    ("ui-standards-v1.0", "d11320704aed69a3d8f854c9264b184e392ec80f"),
    ("deployment-standards-v1.0", "33cc38849180716fd4d06b1356cf70c49d3d41d2"),
    ("operations-standards-v1.0", "7100f294a83c30594f2ff9e953f7c9f77a95747f"),
    ("data-ontology-standards-v1.0", "464a8057ea5dc26ef83248a20bafa0be5aa31148"),
    ("collector-ui-design-standards-v1.0", "f81f4ffa91e9a7af2f80195339d2762180a3154e"),
])
def test_five_frozen_tags_unmoved(tag, expected):
    assert _git("rev-parse", f"{tag}^{{commit}}") == expected


def test_twenty_six_frozen_normative_files_unchanged():
    tags = {
        "ui": "ui-standards-v1.0",
        "data-ontology": "data-ontology-standards-v1.0",
        "operations": "operations-standards-v1.0",
        "deployment": "deployment-standards-v1.0",
        "collector-ui-design": "collector-ui-design-standards-v1.0",
    }
    checked = 0
    for domain, tag in tags.items():
        for path in _git("ls-tree", "-r", "--name-only", tag, "--", f"standards/{domain}").splitlines():
            name = path.rsplit("/", 1)[-1]
            if not (name.startswith("STD-") and name.endswith(".json")):
                continue
            assert _git("rev-parse", f"{tag}:{path}") == _git("rev-parse", f"HEAD:{path}"), (
                f"frozen normative file changed: {path}"
            )
            checked += 1
    assert checked == 26
