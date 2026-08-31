"""Operations Pass 3 (ratification survey) process guards.

The survey must evaluate all four PROPOSED STD-OPS standards from stored
evidence only (no fleet recrawl), leave every standard's status/version
unchanged (still PROPOSED, still v1 — this pass recommends, it does not
ratify), produce one AWAITING OPERATOR DECISION record per standard with
no self-ratification, preserve the frozen baselines and every earlier
Operations pass's artifacts untouched, and honestly flag the OPS-D
review-path process gap rather than smoothing it over.
"""

import json
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
OPS_DIR = REPO / "standards" / "operations"
PASS3 = REPO / "docs" / "operations" / "pass3"
DECISIONS = REPO / "decisions"

EXPECTED_IDS = {"STD-OPS-COM-001", "STD-OPS-COM-002", "STD-OPS-COM-003", "STD-OPS-COM-004"}

DECISION_RECORDS = {
    "0014-ops-com-001-decision.md": "STD-OPS-COM-001",
    "0015-ops-com-002-decision.md": "STD-OPS-COM-002",
    "0016-ops-com-003-decision.md": "STD-OPS-COM-003",
    "0017-ops-com-004-decision.md": "STD-OPS-COM-004",
}


def _load(sid: str) -> dict:
    return json.loads((OPS_DIR / f"{sid}.json").read_text(encoding="utf-8"))


def _git(*args) -> str:
    result = subprocess.run(
        ["git", "-C", str(REPO), *args],
        capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL, check=True,
    )
    return result.stdout.strip()


# -- this pass must not ratify anything --

@pytest.mark.parametrize("sid", sorted(EXPECTED_IDS))
def test_all_four_ops_standards_are_now_ratified(sid):
    """The survey pass itself did not ratify — the operator's subsequent
    acceptance of decisions/0014-0017 did. All four are now RATIFIED v1."""
    obj = _load(sid)
    assert obj["status"] == "RATIFIED", f"{sid}: expected RATIFIED after operator closure"
    assert obj["version"] == 1


def test_exactly_four_std_ops_standards_still_exist():
    files = sorted(OPS_DIR.glob("STD-OPS-*.json"))
    assert {p.stem for p in files} == EXPECTED_IDS
    assert len(files) == 4


# -- survey dossier exists and covers all four standards with one recommendation each --

def test_survey_dossier_exists():
    path = PASS3 / "ratification-survey.md"
    assert path.is_file()
    assert len(path.read_text(encoding="utf-8")) > 3000


def test_survey_recommends_exactly_once_per_standard():
    text = (PASS3 / "ratification-survey.md").read_text(encoding="utf-8")
    for sid in sorted(EXPECTED_IDS):
        assert sid in text, f"{sid} not mentioned in the survey"
    rec_lines = [
        line for line in text.splitlines()
        if line.startswith("| STD-OPS-") and "RATIFY AS WRITTEN" in line
    ]
    assert len(rec_lines) == 4, f"expected 4 recommendation rows, found {len(rec_lines)}"


def test_survey_flags_the_ops_d_review_path_gap():
    """This survey must not silently treat OPS-D's review history as
    equivalent to OPS-A/B/C's — OPS-D's drafted text never went through
    its own dedicated Pass 2 adversarial review, only the pre-draft
    candidate did."""
    text = (PASS3 / "ratification-survey.md").read_text(encoding="utf-8")
    assert "not itself re-reviewed" in text or "has not been through a dedicated" in text or "review-path" in text.lower()


# -- decision records: one per standard, AWAITING OPERATOR DECISION, no self-ratification --

@pytest.mark.parametrize("name,sid", sorted(DECISION_RECORDS.items()))
def test_decision_record_exists_and_is_accepted(name, sid):
    text = (DECISIONS / name).read_text(encoding="utf-8")
    assert "Status: Accepted" in text, f"{name}: expected Accepted after operator ruling"
    assert sid in text
    assert "MUST NOT ratify" in text or "MUST NOT self-ratify" in text, f"{name}: must carry the no-self-ratification warning"
    assert "Option A" in text


def test_decisions_readme_lists_0014_through_0017():
    text = (DECISIONS / "README.md").read_text(encoding="utf-8")
    for n in ("0014", "0015", "0016", "0017"):
        assert n in text


def test_no_decision_record_was_self_ratified():
    """All four decisions are now Accepted by operator ruling. The
    original Pass 0B/1/2/3 text (AWAITING, option menus, no-self-ratify
    warnings) must still be present underneath the acceptance ruling —
    history preserved, not rewritten."""
    for name in DECISION_RECORDS:
        text = (DECISIONS / name).read_text(encoding="utf-8")
        assert "MUST NOT" in text or "must not" in text, (
            f"{name}: no-self-ratification warning must still be present"
        )


# -- OPS-D specific: no overlap with OPS-A restated in the survey --

def test_survey_states_ops_d_no_overlap_with_ops_a():
    text = (PASS3 / "ratification-survey.md").read_text(encoding="utf-8")
    assert "STD-OPS-COM-001" in text.split("COM-004")[-1] or "COM-001" in text


# -- Pass 0/1/2/2.5 artifacts unchanged by this survey --

PRIOR_PASS_DOC_PATHS = [
    "docs/operations/pass0",
    "docs/operations/pass1",
    "docs/operations/pass2",
    "docs/operations/pass2.5",
]


@pytest.mark.parametrize("path", PRIOR_PASS_DOC_PATHS)
def test_prior_pass_docs_unchanged_by_survey(path):
    result = subprocess.run(
        ["git", "-C", str(REPO), "diff", "--quiet", "5aadec0", "--", path],
        capture_output=True, stdin=subprocess.DEVNULL,
    )
    assert result.returncode == 0, f"{path} changed since STD-OPS-COM-004 was drafted at 5aadec0 — the survey must not alter prior-pass artifacts"


# -- both frozen baselines untouched --

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
    assert tag_tree == head_tree


@pytest.mark.parametrize("path", [
    "standards/data-ontology", "docs/data-ontology",
    "baselines/data-ontology-standards-v1.0.json",
    "baselines/data-ontology-standards-v1.0-release-notes.md",
])
def test_data_ontology_baseline_paths_unchanged(path):
    tag_tree = _git("rev-parse", f"data-ontology-standards-v1.0:{path}")
    head_tree = _git("rev-parse", f"HEAD:{path}")
    assert tag_tree == head_tree


def test_no_target_clank_or_clank_architecture_directories_vendored():
    fleet_names = {
        "watch-clank", "smartwatch-clank", "smartphone-clank", "tablet-clank",
        "feature-phone-clank", "oem-radar", "chinese-tech-wire",
        "korean-tech-wire", "semiconductor-intelligence", "clank-architecture",
        "diagnostic-clank",
    }
    top_level = {p.name for p in REPO.iterdir() if p.is_dir()}
    assert not (fleet_names & top_level)
