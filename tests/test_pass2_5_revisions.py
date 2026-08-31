"""Data/Ontology Pass 2.5 (apply Pass 2 review revisions) process guards.

Verifies exactly the two Pass 2 REVISE verdicts (STD-DATA-COM-002,
STD-DATA-COM-003) were applied, exactly as scoped: no touch to
STD-DATA-COM-001 or STD-DATA-COM-004, no new candidates, no promoted
HOLD/REHOME/REJECT cluster, no ratification, and the frozen UI baseline
and Pass 0 evidence remain untouched. Does not encode the revised wording
as ratified truth — these are structural/process guards only.
"""

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
DATA_DIR = REPO / "standards" / "data-ontology"
REVIEW = REPO / "docs" / "data-ontology" / "pass2" / "review.md"

DATA_IDS = {"STD-DATA-COM-001", "STD-DATA-COM-002", "STD-DATA-COM-003", "STD-DATA-COM-004"}
UNTOUCHED_IDS = {"STD-DATA-COM-001", "STD-DATA-COM-004"}
REVISED_IDS = {"STD-DATA-COM-002", "STD-DATA-COM-003"}


def _load(sid: str) -> dict:
    return json.loads((DATA_DIR / f"{sid}.json").read_text(encoding="utf-8"))


# -- untouched standards are byte-identical to their Pass 1 content --

def test_untouched_standards_had_no_git_diff_between_pass1_and_pass2_5():
    """Historical guard, pinned to the Pass 1 -> Pass 2.5 window only: at
    commit d6f4e58 (end of Pass 2.5), COM-001/004 were still byte-identical
    to their Pass 1 (1f66cf9) content — Pass 2.5 itself touched only
    COM-002/003. A later, separately-authorized ratification closure
    legitimately flips all four to RATIFIED, so this test compares two
    fixed historical commits, not the current working tree, and remains
    true regardless of what ratification did afterward."""
    import subprocess

    for sid in sorted(UNTOUCHED_IDS):
        result = subprocess.run(
            ["git", "-C", str(REPO), "diff", "--quiet", "1f66cf9", "d6f4e58", "--", f"standards/data-ontology/{sid}.json"],
            capture_output=True, text=True, stdin=subprocess.DEVNULL,
        )
        assert result.returncode == 0, f"{sid} changed between Pass 1 (1f66cf9) and Pass 2.5 (d6f4e58) — it should not have been touched by Pass 2.5"


# -- revised standards: version bumped, status stays PROPOSED --

@pytest.mark.parametrize("sid", sorted(REVISED_IDS))
def test_revised_standards_are_version_2(sid):
    """As of Pass 2.5, status was PROPOSED (verified then). A later,
    separately-authorized operator ruling (decisions/0011, 0012) has
    since ratified both — see test_data_ontology_ratification_closure.py
    for the live status/traceability guard. This test's remaining live
    job is the version number, which ratification explicitly preserved."""
    obj = _load(sid)
    assert obj["version"] == 2, f"{sid}: expected version 2 (operator-confirmed precedent: revision of a PROPOSED draft bumps version)"
    assert obj["status"] in ("PROPOSED", "REVIEWED", "RATIFIED")


@pytest.mark.parametrize("sid", sorted(UNTOUCHED_IDS))
def test_untouched_standards_remain_version_1(sid):
    obj = _load(sid)
    assert obj["version"] == 1
    assert obj["status"] in ("PROPOSED", "REVIEWED", "RATIFIED")


# -- COM-002: acceptance covers every default novelty-asserting path, including secondary/derived; explicit inheritance allowed; post-hoc/caller-only exclusion forbidden --

def test_com002_acceptance_covers_secondary_and_derived_novelty_paths():
    obj = _load("STD-DATA-COM-002")
    acceptance_text = " ".join(obj["acceptance"])
    assert "secondary or derived" in acceptance_text, "acceptance must explicitly bind secondary/derived novelty-asserting paths"
    assert "every default query, view, or api path" in acceptance_text.lower()


def test_com002_acceptance_allows_explicit_inheritance():
    obj = _load("STD-DATA-COM-002")
    acceptance_text = " ".join(obj["acceptance"])
    assert "explicitly inherit" in acceptance_text.lower(), "acceptance must allow an explicitly-inherited eligibility rule, not only an inline predicate"


def test_com002_forbids_post_hoc_and_output_inspection_only_exclusion():
    obj = _load("STD-DATA-COM-002")
    forbidden_text = " ".join(obj["forbidden"]).lower()
    assert "external to" in forbidden_text, "forbidden must name post-hoc/external-to-the-path filtering"
    assert "output" in forbidden_text and "conformance" in forbidden_text, (
        "forbidden must name relying on output inspection alone as proof of conformance"
    )


def test_com002_does_not_prescribe_one_sql_shape_or_field_name():
    obj = _load("STD-DATA-COM-002")
    text = json.dumps(obj).lower()
    for banned in ["select * from", "where is_baseline =", "create table"]:
        assert banned not in text


def test_com002_still_permits_explicit_history_inspection_views():
    obj = _load("STD-DATA-COM-002")
    acceptance_text = " ".join(obj["acceptance"])
    assert "may surface them" in acceptance_text.lower() or "may" in acceptance_text.lower()


def test_com002_editorial_freshness_remains_optional_corollary_only():
    obj = _load("STD-DATA-COM-002")
    trigger = obj["trigger"].lower()
    assert "not required to build editorial freshness" in trigger or "typically news" in trigger


# -- COM-003: discriminator scope local to considered/merged records; merge audit includes mechanism --

def test_com003_discriminator_scope_is_local_not_world_knowledge():
    obj = _load("STD-DATA-COM-003")
    forbidden_text = " ".join(obj["forbidden"])
    assert "present in the records under consideration" in forbidden_text, (
        "FORBIDDEN 1 must scope 'available' discriminators to the records under consideration or the merged record"
    )
    assert "available and conflicts" not in forbidden_text, "the old world-knowledge-shaped 'available and conflicts' phrasing must be gone"


def test_com003_automatic_merge_audit_records_mechanism():
    obj = _load("STD-DATA-COM-003")
    acceptance_text = " ".join(obj["acceptance"])
    assert "mechanism" in acceptance_text.lower() and "decision-path" in acceptance_text.lower(), (
        "acceptance must require the merge audit record which mechanism/decision-path performed the merge"
    )


def test_com003_does_not_define_universal_confidence_threshold_or_key_hierarchy():
    """Checks only the normative clauses (requirement/forbidden/acceptance),
    not notes/rationale, which legitimately discuss in prose what was
    deliberately NOT added — that disclaiming language would otherwise
    trip a naive substring search."""
    obj = _load("STD-DATA-COM-003")
    normative_text = json.dumps(
        {"requirement": obj["requirement"], "forbidden": obj["forbidden"], "acceptance": obj["acceptance"]}
    ).lower()
    for banned in ["confidence >=", "confidence threshold", "key hierarchy", "priority order: model number"]:
        assert banned not in normative_text


def test_com003_core_posture_unchanged():
    obj = _load("STD-DATA-COM-003")
    requirement = obj["requirement"]
    assert "prefer a missed merge over a false merge" in requirement
    assert "evidence-gated" in requirement
    assert "auditable" in requirement
    assert "reversible or otherwise information-preserving" in requirement


def test_com003_still_excludes_cross_clank_identity():
    obj = _load("STD-DATA-COM-003")
    assert "C7" in obj["notes"] and "DO_NOT_STANDARDISE" in obj["notes"]


# -- both revised standards reference the Pass 2 review as their revision origin --

@pytest.mark.parametrize("sid", sorted(REVISED_IDS))
def test_revised_standard_notes_cite_pass2_review(sid):
    obj = _load(sid)
    assert "pass2/review.md" in obj["notes"]
    assert "REVISE" in obj["notes"]


# -- no new candidates, no promoted HOLD/REHOME/REJECT --

def test_still_exactly_four_data_standards():
    files = sorted(DATA_DIR.glob("STD-DATA-*.json"))
    assert {p.stem for p in files} == DATA_IDS
    assert len(files) == 4


HOLD_REHOME_REJECT_CLUSTER_IDS = {
    "cross-clank-fleet-identity", "availability-lifecycle-data-model",
    "timestamp-shaped-values", "confidence-and-certainty-semantics",
    "canonical-fact-overwrite-discipline", "regional-variant-identity",
    "unknown-absent-vs-false", "editorial-freshness-vs-novelty",
    "source-disagreement-representation",
}


def test_no_hold_rehome_reject_cluster_cited_as_evidence_source():
    for path in sorted(DATA_DIR.glob("STD-DATA-*.json")):
        obj = json.loads(path.read_text(encoding="utf-8"))
        evidence_sources = " ".join(e.get("source", "") for e in obj["evidence"])
        for cluster_id in HOLD_REHOME_REJECT_CLUSTER_IDS:
            assert f"clusters/{cluster_id}.md" not in evidence_sources, (
                f"{path.name}: cites HOLD/REHOME/REJECT cluster {cluster_id!r} as an evidence source"
            )


# -- no ratification occurred anywhere in this pass --

def test_data_standard_status_is_a_known_value():
    """At Pass 2.5 time, none were ratified — verified true then. Status
    has since legitimately progressed via an explicit, separately-
    authorized operator ruling; see test_data_ontology_ratification_closure.py
    for the live ratification/traceability guards."""
    for path in sorted(DATA_DIR.glob("STD-DATA-*.json")):
        obj = json.loads(path.read_text(encoding="utf-8"))
        assert obj["status"] in ("PROPOSED", "REVIEWED", "RATIFIED")


def test_any_decision_record_accepting_com_002_or_003_has_an_operator_ruling_section():
    """At Pass 2.5 time, no decision record existed for these two at all.
    A later operator ruling (decisions/0011, 0012) legitimately marks them
    Accepted; the live guard is that any such acceptance carries a real,
    dated Operator ruling section, not a bare status flip."""
    decisions_dir = REPO / "decisions"
    for path in decisions_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        if ("STD-DATA-COM-002" in text or "STD-DATA-COM-003" in text) and "Status: Accepted" in text:
            assert "Operator ruling" in text, f"{path.name}: marked Accepted with no Operator ruling section"


# -- Pass 0 evidence and Pass 0B adjudication remain untouched --

PASS0_FROZEN = [
    ("3ce1c2c", "docs/data-ontology/pass0/evidence-log.md"),
    ("3ce1c2c", "docs/data-ontology/pass0/incident-ledger.md"),
    ("3ce1c2c", "docs/data-ontology/pass0/handoff.md"),
    ("0166aeb", "docs/data-ontology/pass0/adjudication.md"),
    # holds-and-rejects.md excluded from the byte-identity pin: the
    # 2026-08-31 holds disposition prepended an additive pointer to it
    # (cards preserved unmodified — guarded by test_holds_cards_preserved
    # in tests/test_data_holds_disposition.py).
    ("0166aeb", "docs/data-ontology/pass0/candidates/c1-continuity-explicitness.md"),
    ("0166aeb", "docs/data-ontology/pass0/candidates/c2-novelty-read-side-exclusion.md"),
    ("0166aeb", "docs/data-ontology/pass0/candidates/c3-identity-conservatism.md"),
    ("0166aeb", "docs/data-ontology/pass0/candidates/c5-provenance-tier-separation.md"),
]


@pytest.mark.parametrize("base,path", PASS0_FROZEN, ids=[p for _, p in PASS0_FROZEN])
def test_pass0_artifacts_unchanged_since_introduction(base, path):
    import subprocess

    result = subprocess.run(
        ["git", "-C", str(REPO), "diff", "--quiet", base, "--", path],
        capture_output=True, text=True, stdin=subprocess.DEVNULL,
    )
    assert result.returncode == 0, f"{path} changed since its introduction at {base}"


def test_pass2_review_unchanged_since_pass2():
    import subprocess

    result = subprocess.run(
        ["git", "-C", str(REPO), "diff", "--quiet", "7b33a71", "--", "docs/data-ontology/pass2/review.md"],
        capture_output=True, text=True, stdin=subprocess.DEVNULL,
    )
    assert result.returncode == 0, "Pass 2 review.md must not be modified by Pass 2.5"


# -- frozen UI baseline untouched --

def _git(*args) -> str:
    import subprocess

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
