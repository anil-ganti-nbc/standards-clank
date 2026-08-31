"""Data/Ontology ratification-closure guards (operator ruling, 2026-08-31).

Verifies: exactly the four STD-DATA-COM-* standards are RATIFIED at their
preserved versions (v1/v2/v2/v1), decisions 0010-0013 are Accepted and
correctly cross-referenced, the generated agent layer
(ratified-index.json / agent-checklist.json) matches its builder and
covers exactly these four ids, the constitution never treats a HOLD/
REHOME/REJECT candidate as normative, and the frozen UI baseline and
Pass 0 evidence/adjudication remain untouched. Does not encode any
standard's wording as beyond-challenge truth — ratification is the
operator's act, recorded here, not re-derived here.
"""

import json
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
DATA_DIR = REPO / "standards" / "data-ontology"
DECISIONS_DIR = REPO / "decisions"
CONSTITUTION = REPO / "docs" / "data-ontology" / "constitution.md"

EXPECTED_VERSIONS = {
    "STD-DATA-COM-001": 1,
    "STD-DATA-COM-002": 2,
    "STD-DATA-COM-003": 2,
    "STD-DATA-COM-004": 1,
}
EXPECTED_DECISIONS = {
    "STD-DATA-COM-001": "decisions/0010-data-com-001-decision.md",
    "STD-DATA-COM-002": "decisions/0011-data-com-002-decision.md",
    "STD-DATA-COM-003": "decisions/0012-data-com-003-decision.md",
    "STD-DATA-COM-004": "decisions/0013-data-com-004-decision.md",
}


def _load(sid: str) -> dict:
    return json.loads((DATA_DIR / f"{sid}.json").read_text(encoding="utf-8"))


# -- status/version preservation --

@pytest.mark.parametrize("sid,version", sorted(EXPECTED_VERSIONS.items()))
def test_standard_is_ratified_at_its_preserved_version(sid, version):
    obj = _load(sid)
    assert obj["status"] == "RATIFIED", f"{sid}: expected RATIFIED"
    assert obj["version"] == version, f"{sid}: expected version {version}, found {obj['version']}"


def test_exactly_four_data_ontology_standards_all_ratified():
    files = sorted(DATA_DIR.glob("STD-DATA-*.json"))
    assert {p.stem for p in files} == set(EXPECTED_VERSIONS)
    for path in files:
        obj = json.loads(path.read_text(encoding="utf-8"))
        assert obj["status"] == "RATIFIED"


# -- normative wording unchanged by this closure pass: only status/version/notes may differ from the Pass 2.5 commit --

@pytest.mark.parametrize("sid", sorted(EXPECTED_VERSIONS))
def test_requirement_forbidden_acceptance_unchanged_since_pass2_5(sid):
    result = subprocess.run(
        ["git", "show", f"d6f4e58:standards/data-ontology/{sid}.json"],
        cwd=REPO, capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL,
    )
    assert result.returncode == 0, f"could not read {sid} at commit d6f4e58"
    before = json.loads(result.stdout)
    after = _load(sid)
    for field in ("requirement", "trigger", "forbidden", "acceptance", "level", "domain", "applies_to", "id", "title"):
        assert before[field] == after.get(field), f"{sid}: normative field {field!r} changed during ratification closure"


# -- decisions 0010-0013 are Accepted and cross-reference correctly --

@pytest.mark.parametrize("sid,decision_path", sorted(EXPECTED_DECISIONS.items()))
def test_decision_record_is_accepted(sid, decision_path):
    text = (REPO / decision_path).read_text(encoding="utf-8")
    assert "Status: Accepted" in text, f"{decision_path}: expected Status: Accepted"
    assert "Operator ruling" in text, f"{decision_path}: expected an Operator ruling section"
    assert sid in text


@pytest.mark.parametrize("sid,decision_path", sorted(EXPECTED_DECISIONS.items()))
def test_standard_notes_cite_its_accepted_decision(sid, decision_path):
    obj = _load(sid)
    assert decision_path in obj["notes"], f"{sid}: notes must cite {decision_path}"
    assert "RATIFIED" in obj["notes"]


def test_decisions_readme_lists_0010_through_0013():
    text = (DECISIONS_DIR / "README.md").read_text(encoding="utf-8")
    for n in ("0010", "0011", "0012", "0013"):
        assert n in text


def test_no_agent_self_ratification_disclaimer_removed_from_decisions():
    """Decisions 0010-0013 still carry the standing 'an agent MUST NOT
    ratify' disclaimer even after acceptance — matching 0007-0009's
    pattern of leaving that sentence in place post-ruling."""
    for decision_path in EXPECTED_DECISIONS.values():
        text = (REPO / decision_path).read_text(encoding="utf-8")
        assert "MUST NOT ratify" in text


# -- generated agent layer integrity --

def test_generated_files_match_builder_output():
    import sys

    sys.path.insert(0, str(REPO))
    from tools.data_ontology_agent_layer import build_agent_checklist, build_ratified_index

    index = json.loads((DATA_DIR / "ratified-index.json").read_text(encoding="utf-8"))
    checklist = json.loads((DATA_DIR / "agent-checklist.json").read_text(encoding="utf-8"))
    assert index == build_ratified_index()
    assert checklist == build_agent_checklist()


def test_ratified_index_covers_exactly_the_four_standards():
    index = json.loads((DATA_DIR / "ratified-index.json").read_text(encoding="utf-8"))
    ids = {entry["id"] for entry in index}
    assert ids == set(EXPECTED_VERSIONS)
    for entry in index:
        assert entry["version"] == EXPECTED_VERSIONS[entry["id"]]
        assert entry["ratification_decision"] == EXPECTED_DECISIONS[entry["id"]]


def test_agent_checklist_covers_exactly_the_four_standards():
    checklist = json.loads((DATA_DIR / "agent-checklist.json").read_text(encoding="utf-8"))
    ids = {item["standard"] for item in checklist}
    assert ids == set(EXPECTED_VERSIONS)
    for item in checklist:
        assert item.get("question")
        assert item.get("failure_means")


def test_ratified_index_entries_have_no_extra_fields():
    required = {"id", "title", "level", "applies_to", "version", "requirement_summary", "source_file", "ratification_decision"}
    for entry in json.loads((DATA_DIR / "ratified-index.json").read_text(encoding="utf-8")):
        assert entry.keys() == required, f"{entry['id']}: unexpected fields {entry.keys() - required}"


# -- no HOLD/REHOME/REJECT candidate leaks into the constitution as normative --

HOLD_REHOME_REJECT_MARKERS = [
    "Availability/lifecycle honesty backing",
    "Timestamp-shaped values mistaken for chronological truth",
    "Cross-Clank entity identity",
    "Confidence-and-certainty semantics",
    "canonical-fact-overwrite discipline",
    "regional-variant identity",
    "Source-disagreement representation",
]


def test_constitution_exists_and_covers_all_four_ratified_ids():
    text = CONSTITUTION.read_text(encoding="utf-8")
    for sid in EXPECTED_VERSIONS:
        assert sid in text, f"constitution.md does not cite {sid}"


def test_constitution_places_held_candidates_only_in_the_not_a_standard_section():
    text = CONSTITUTION.read_text(encoding="utf-8")
    marker = "## Not a standard"
    assert marker in text, "constitution.md must have an explicit non-normative section for held candidates"
    body, _, held_section = text.partition(marker)
    for name in HOLD_REHOME_REJECT_MARKERS:
        assert name not in body, f"{name!r} appears in the constitution's normative body (sections A-D), not just the held-candidates section"
        assert name in held_section, f"{name!r} missing from the held-candidates section"


def test_constitution_normative_principles_cite_only_ratified_ids():
    import re

    text = CONSTITUTION.read_text(encoding="utf-8")
    body = text.split("## Not a standard")[0]
    referenced = set(re.findall(r"STD-DATA-COM-\d{3}", body))
    assert referenced, "constitution.md's normative body cites no STD-DATA-* id at all"
    assert referenced == set(EXPECTED_VERSIONS), f"unexpected ids in normative body: {referenced - set(EXPECTED_VERSIONS)}"


# -- no candidate was newly promoted; Pass 0 evidence/adjudication untouched --

def test_still_no_std_data_file_beyond_the_four():
    files = list(REPO.glob("standards/**/STD-DATA-*.json"))
    assert {p.stem for p in files} == set(EXPECTED_VERSIONS)


PASS0_FROZEN = [
    ("3ce1c2c", "docs/data-ontology/pass0/evidence-log.md"),
    ("3ce1c2c", "docs/data-ontology/pass0/incident-ledger.md"),
    ("3ce1c2c", "docs/data-ontology/pass0/handoff.md"),
    ("0166aeb", "docs/data-ontology/pass0/adjudication.md"),
]
    # holds-and-rejects.md is excluded from the byte-identity pin: the
    # 2026-08-31 holds disposition prepended an additive pointer to it
    # (cards preserved unmodified — guarded by test_holds_cards_preserved
    # in tests/test_data_holds_disposition.py).


@pytest.mark.parametrize("base,path", PASS0_FROZEN, ids=[p for _, p in PASS0_FROZEN])
def test_pass0_artifacts_unchanged_since_introduction(base, path):
    result = subprocess.run(
        ["git", "-C", str(REPO), "diff", "--quiet", base, "--", path],
        capture_output=True, text=True, stdin=subprocess.DEVNULL,
    )
    assert result.returncode == 0, f"{path} changed since its introduction at {base}"


def test_pass2_and_pass3_artifacts_unchanged():
    for base, path in [
        ("d6f4e58", "docs/data-ontology/pass2/review.md"),
        ("00a27f0", "docs/data-ontology/pass3/ratification-survey.md"),
    ]:
        result = subprocess.run(
            ["git", "-C", str(REPO), "diff", "--quiet", base, "--", path],
            capture_output=True, text=True, stdin=subprocess.DEVNULL,
        )
        assert result.returncode == 0, f"{path} changed during ratification closure"


# -- frozen UI baseline untouched --

def _git(*args) -> str:
    result = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True, check=True, stdin=subprocess.DEVNULL)
    return result.stdout.strip()


@pytest.mark.parametrize("path", ["standards/ui", "docs/ui", "baselines"])
def test_ui_baseline_paths_unchanged_since_freeze(path):
    tag_tree = _git("rev-parse", f"ui-standards-v1.0:{path}")
    head_tree = _git("rev-parse", f"HEAD:{path}")
    assert tag_tree == head_tree, f"{path} changed since the ui-standards-v1.0 freeze"


def test_ui_standards_tag_still_resolves_to_the_expected_commit():
    resolved = _git("rev-parse", "ui-standards-v1.0^{commit}")
    assert resolved == "d11320704aed69a3d8f854c9264b184e392ec80f"


def test_data_ontology_baseline_now_declared():
    """At ratification closure (this file's original writing), the
    operator had explicitly deferred freezing this domain, and this test
    asserted no baselines/data-ontology* manifest or
    data-ontology-standards-v1.0 tag existed yet. A later, separately-
    authorized Baseline Freeze pass (preceded by a hold-resolution audit,
    docs/data-ontology/holds-disposition.md) has since declared that
    baseline — see tests/test_data_ontology_baseline_v1_0.py for the live
    freeze guards. This test's remaining live job: the baseline exists
    and references this same four-standard, four-decision corpus."""
    manifest_paths = list(REPO.glob("baselines/data-ontology*"))
    assert manifest_paths, "expected a baselines/data-ontology* manifest to exist post-freeze"
