"""Operations Pass 1 (candidate drafting) process guards.

Pass 1 must draft exactly the three Pass 0B ADVANCE candidates with full
candidate cards (OPS-A, OPS-B, OPS-C) as PROPOSED standards, change no
existing normative status, create no candidates beyond those three, leave
held/deferred/rehomed Pass 0B dispositions unpromoted, leave both frozen
baselines and the Pass 0 evidence/adjudication corpus untouched, and
never self-ratify. Proposed wording is NOT encoded as ratified truth.
"""

import json
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
OPS_DIR = REPO / "standards" / "operations"
PASS0_DIR = REPO / "docs" / "operations" / "pass0"
PASS1_DIR = REPO / "docs" / "operations" / "pass1"

EXPECTED_IDS = {"STD-OPS-COM-001", "STD-OPS-COM-002", "STD-OPS-COM-003"}


def _load(sid: str) -> dict:
    return json.loads((OPS_DIR / f"{sid}.json").read_text(encoding="utf-8"))


def _git(*args) -> str:
    result = subprocess.run(
        ["git", "-C", str(REPO), *args],
        capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL, check=True,
    )
    return result.stdout.strip()


# -- exactly three standards, all PROPOSED, all v1 --

def test_exactly_three_std_ops_standards_exist():
    files = sorted(OPS_DIR.glob("STD-OPS-*.json"))
    assert {p.stem for p in files} == EXPECTED_IDS, f"expected exactly {EXPECTED_IDS}, found {[p.stem for p in files]}"
    assert len(files) == 3


@pytest.mark.parametrize("sid", sorted(EXPECTED_IDS))
def test_standard_is_proposed_at_version_1(sid):
    obj = _load(sid)
    assert obj["status"] == "PROPOSED", f"{sid}: expected PROPOSED, found {obj['status']}"
    assert obj["version"] == 1, f"{sid}: expected version 1, found {obj['version']}"
    assert obj["domain"] == "operations"


def test_no_fourth_operations_standard_and_no_ops_d():
    """The mission explicitly forbade a fourth standard; Pass 0B's
    adjudication table marked a fourth cluster (2, pid-namespace-unsafe
    locking) ADVANCE but never produced a full candidate card for it —
    confirm no ops-d file exists anywhere, drafted or as a card."""
    assert not list(REPO.rglob("STD-OPS-COM-004*"))
    assert not list(REPO.rglob("ops-d-*"))


# -- no self-ratification --

@pytest.mark.parametrize("sid", sorted(EXPECTED_IDS))
def test_no_ratification_decision_referenced_yet(sid):
    obj = _load(sid)
    notes = obj.get("notes", "")
    assert "not yet ratified" in notes
    assert "not self-ratified" in notes
    assert "decisions/" not in notes, f"{sid}: PROPOSED standard must not cite a ratification decision record yet"


# -- required structural content per draft --

@pytest.mark.parametrize("sid", sorted(EXPECTED_IDS))
def test_each_draft_has_trigger_and_applicability(sid):
    obj = _load(sid)
    assert obj.get("trigger"), f"{sid}: missing trigger/applicability text"
    assert "applies_to" in obj


@pytest.mark.parametrize("sid", sorted(EXPECTED_IDS))
def test_each_draft_has_acceptance_criteria(sid):
    obj = _load(sid)
    assert obj.get("acceptance"), f"{sid}: missing acceptance criteria"
    assert len(obj["acceptance"]) >= 3


@pytest.mark.parametrize("sid", sorted(EXPECTED_IDS))
def test_each_draft_has_forbidden_behavior(sid):
    obj = _load(sid)
    assert obj.get("forbidden"), f"{sid}: missing forbidden behavior list"
    assert len(obj["forbidden"]) >= 3


@pytest.mark.parametrize("sid", sorted(EXPECTED_IDS))
def test_each_draft_cites_its_governance_overlap(sid):
    obj = _load(sid)
    notes = obj.get("notes", "")
    assert "clank-architecture" in notes
    assert ("Fleet Law" in notes) or ("ADR-" in notes), f"{sid}: notes must cite the specific Fleet Law/ADR overlap"
    assert "Standards Clank defines the semantic invariant" in notes
    assert "separate authority" in notes


@pytest.mark.parametrize("sid", sorted(EXPECTED_IDS))
def test_each_draft_has_evidence_citations(sid):
    obj = _load(sid)
    assert obj.get("evidence"), f"{sid}: missing evidence array"
    assert len(obj["evidence"]) >= 3


# -- forbidden vocabulary: cycle counts / stage vocab / scheduler tech must not be mandated --

def _normative_text(obj: dict) -> str:
    """Only the binding fields — requirement, forbidden, acceptance,
    trigger — not rationale/evidence, which legitimately cite real fleet
    technology (systemd, cron, APScheduler) as incident context without
    mandating it."""
    parts = [obj["requirement"], obj["trigger"], *obj["forbidden"], *obj["acceptance"]]
    return " ".join(parts)


def test_ops_a_does_not_mandate_scheduler_technology_or_one_run_table():
    text = _normative_text(_load("STD-OPS-COM-001"))
    for banned in ("systemd", "cron", "APScheduler"):
        assert banned not in text, f"STD-OPS-COM-001's normative text must not mandate {banned}"


def test_ops_b_does_not_prescribe_a_score_formula():
    """The trigger text explicitly disclaims prescribing a score formula
    ('does not require... a score formula') — that disclaiming mention is
    expected; the check is that no concrete formula/threshold syntax
    (e.g. an equation or a numeric score cutoff) appears normatively."""
    text = _normative_text(_load("STD-OPS-COM-002")).lower()
    assert "does not require" in text and "formula" in text
    assert not any(ch.isdigit() for ch in text), "normative text must not embed a numeric threshold/formula"


def test_ops_c_does_not_prescribe_cycle_counts_or_durations():
    text = _normative_text(_load("STD-OPS-COM-003"))
    for banned in ("12 cycles", "20 cycles", " hours", " days"):
        assert banned not in text
    assert "policy parameter" in text.lower()


# -- held/deferred/rehomed clusters remain unpromoted --

def test_held_deferred_rehomed_concerns_have_no_std_ops_file():
    """Cluster 14 (HOLD), cluster 10 (DEFER to ADR-0009), clusters 8/9/12
    (REHOME to a future DEPLOYMENT domain), and cluster 15 (REHOME to a
    future DELIVERY domain) must not have been promoted into a drafted
    standard by this pass."""
    all_text = " ".join(p.read_text(encoding="utf-8") for p in OPS_DIR.glob("STD-OPS-*.json"))
    for forbidden_topic in (
        "destructive", "backup", "deployment revision", "remote host truth",
        "schema deployment", "notification retry", "blocked/mothballed",
    ):
        assert forbidden_topic.lower() not in all_text.lower(), (
            f"a held/deferred/rehomed concern ({forbidden_topic!r}) leaked into a drafted standard"
        )


def test_holds_rehomes_defers_card_unchanged_since_pass0b():
    result = subprocess.run(
        ["git", "-C", str(REPO), "diff", "--quiet", "53480ec", "--",
         "docs/operations/pass0/candidates/holds-rehomes-defers.md"],
        capture_output=True, stdin=subprocess.DEVNULL,
    )
    assert result.returncode == 0, "holds-rehomes-defers.md changed since Pass 0B — held/deferred/rehomed dispositions must stay exactly where Pass 0B put them"


# -- Pass 0 evidence and Pass 0B adjudication untouched --

PASS0_UNCHANGED_SINCE_21f0885 = [
    "docs/operations/pass0/evidence-log.md",
    "docs/operations/pass0/incident-ledger.md",
    "docs/operations/pass0/terminology-map.md",
    "docs/operations/pass0/README.md",
    "docs/operations/pass0/handoff.md",
]


@pytest.mark.parametrize("path", PASS0_UNCHANGED_SINCE_21f0885)
def test_pass0a_evidence_files_unchanged_since_introduction(path):
    result = subprocess.run(
        ["git", "-C", str(REPO), "diff", "--quiet", "21f0885", "--", path],
        capture_output=True, stdin=subprocess.DEVNULL,
    )
    assert result.returncode == 0, f"{path} changed since Pass 0A introduced it"


def test_pass0a_clusters_directory_unchanged_since_introduction():
    result = subprocess.run(
        ["git", "-C", str(REPO), "diff", "--quiet", "21f0885", "--", "docs/operations/pass0/clusters"],
        capture_output=True, stdin=subprocess.DEVNULL,
    )
    assert result.returncode == 0, "docs/operations/pass0/clusters/ changed since Pass 0A introduced it"


PASS0B_UNCHANGED_SINCE_53480ec = [
    "docs/operations/pass0/adjudication.md",
    "docs/operations/pass0/candidates/ops-a-execution-materialization-truth.md",
    "docs/operations/pass0/candidates/ops-b-health-honesty-two-axis.md",
    "docs/operations/pass0/candidates/ops-c-promotion-soak-evidence-integrity.md",
]


@pytest.mark.parametrize("path", PASS0B_UNCHANGED_SINCE_53480ec)
def test_pass0b_adjudication_files_unchanged_since_introduction(path):
    result = subprocess.run(
        ["git", "-C", str(REPO), "diff", "--quiet", "53480ec", "--", path],
        capture_output=True, stdin=subprocess.DEVNULL,
    )
    assert result.returncode == 0, f"{path} changed since Pass 0B introduced it"


# -- neither frozen baseline manifest lists an OPS standard, both tags intact --

def test_neither_frozen_baseline_manifest_lists_an_ops_standard():
    for manifest_path in ("baselines/ui-standards-v1.0.json", "baselines/data-ontology-standards-v1.0.json"):
        manifest = json.loads((REPO / manifest_path).read_text(encoding="utf-8"))
        ids = {s["id"] for s in manifest["standards"]}
        assert not any(i.startswith("STD-OPS-") for i in ids), f"{manifest_path} must never list an OPS standard"


def test_both_baseline_tags_resolve_to_their_frozen_commits():
    assert _git("rev-parse", "ui-standards-v1.0^{commit}") == "d11320704aed69a3d8f854c9264b184e392ec80f"
    assert _git("rev-parse", "data-ontology-standards-v1.0^{commit}") == "464a8057ea5dc26ef83248a20bafa0be5aa31148"


@pytest.mark.parametrize("path", [
    "standards/ui", "docs/ui",
    "baselines/ui-standards-v1.0.json", "baselines/ui-standards-v1.0-release-notes.md",
])
def test_ui_baseline_paths_unchanged(path):
    tag_tree = _git("rev-parse", f"ui-standards-v1.0:{path}")
    head_tree = _git("rev-parse", f"HEAD:{path}")
    assert tag_tree == head_tree, f"{path} changed since the ui-standards-v1.0 freeze"


@pytest.mark.parametrize("path", [
    "standards/data-ontology", "docs/data-ontology",
    "baselines/data-ontology-standards-v1.0.json",
    "baselines/data-ontology-standards-v1.0-release-notes.md",
])
def test_data_ontology_baseline_paths_unchanged(path):
    tag_tree = _git("rev-parse", f"data-ontology-standards-v1.0:{path}")
    head_tree = _git("rev-parse", f"HEAD:{path}")
    assert tag_tree == head_tree, f"{path} changed since the data-ontology-standards-v1.0 freeze"


# -- no target Clank / clank-architecture vendored or modified --

def test_no_target_clank_or_clank_architecture_directories_vendored():
    fleet_names = {
        "watch-clank", "smartwatch-clank", "smartphone-clank", "tablet-clank",
        "feature-phone-clank", "oem-radar", "chinese-tech-wire",
        "korean-tech-wire", "semiconductor-intelligence", "clank-architecture",
        "diagnostic-clank",
    }
    top_level = {p.name for p in REPO.iterdir() if p.is_dir()}
    assert not (fleet_names & top_level), f"found vendored Clank directories: {fleet_names & top_level}"


# -- dossiers exist --

def test_pass1_dossier_exists_for_each_draft():
    for name in (
        "dossier-ops-a-execution-materialization-truth.md",
        "dossier-ops-b-health-honesty-two-axis.md",
        "dossier-ops-c-promotion-soak-evidence-integrity.md",
    ):
        path = PASS1_DIR / name
        assert path.is_file(), f"missing dossier: {name}"
        text = path.read_text(encoding="utf-8")
        for heading in (
            "## Candidate", "## Source clusters", "## Pass 0B disposition",
            "## Evidence strength", "## Strongest incidents", "## Lineage assessment",
            "## Fleet Law / ADR relationship", "## Strongest counterexample",
            "## Unresolved wording questions", "## Recommendation",
        ):
            assert heading in text, f"{name} missing section {heading!r}"


def test_every_dossier_recommendation_is_a_valid_value():
    valid = ("READY FOR REVIEW", "NEEDS NARROWING", "HOLD")
    for name in (
        "dossier-ops-a-execution-materialization-truth.md",
        "dossier-ops-b-health-honesty-two-axis.md",
        "dossier-ops-c-promotion-soak-evidence-integrity.md",
    ):
        text = (PASS1_DIR / name).read_text(encoding="utf-8")
        section = text.split("## Recommendation")[1]
        assert any(v in section for v in valid), f"{name}: no valid recommendation value found"
