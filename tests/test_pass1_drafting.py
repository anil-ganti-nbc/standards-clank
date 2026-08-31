"""Data/Ontology Pass 1 drafting guards.

Verifies exactly the four Pass 0B ADVANCE candidates (C1/C2/C3/C5) were
drafted as PROPOSED standards, none were self-ratified, none of the
HOLD/REHOME/REJECT candidates were promoted, the frozen UI baseline is
untouched, and every draft is properly schema-valid, evidence-backed, and
cross-referenced back to its Pass 0 origin. Does not encode any draft's
wording as ratified truth — these are structural/process guards only.
"""

import json
import re
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
DATA_ONTOLOGY_DIR = REPO / "standards" / "data-ontology"
PASS0_DIR = REPO / "docs" / "data-ontology" / "pass0"
PASS1_DIR = REPO / "docs" / "data-ontology" / "pass1"
UI_BASELINE_MANIFEST = REPO / "baselines" / "ui-standards-v1.0.json"

EXPECTED_IDS = {"STD-DATA-COM-001", "STD-DATA-COM-002", "STD-DATA-COM-003", "STD-DATA-COM-004"}

HOLD_REHOME_REJECT_CLUSTER_IDS = {
    "cross-clank-fleet-identity",  # C7, HOLD/DEFER
    "availability-lifecycle-data-model",  # C4, SPLIT/HOLD
    "timestamp-shaped-values",  # C6, REHOME
    "confidence-and-certainty-semantics",  # HOLD
    "canonical-fact-overwrite-discipline",  # HOLD
    "regional-variant-identity",  # HOLD
    "unknown-absent-vs-false",  # folded into HOLD
    "editorial-freshness-vs-novelty",  # folded into C2, not its own standard
    "source-disagreement-representation",  # REJECT
}


def _standard_files():
    return sorted(DATA_ONTOLOGY_DIR.glob("STD-DATA-*.json"))


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


# -- exactly four new standards exist, all PROPOSED --

def test_exactly_four_data_ontology_standards_exist():
    files = _standard_files()
    found_ids = {p.stem for p in files}
    assert found_ids == EXPECTED_IDS, f"expected {EXPECTED_IDS}, found {found_ids}"


@pytest.mark.parametrize("path", _standard_files(), ids=lambda p: p.stem)
def test_standard_status_is_known_and_not_self_ratified(path):
    """As drafted in Pass 1, all four were PROPOSED. An explicit operator
    ruling (decisions/0010-0013) has since ratified all four — that is a
    legitimate status progression, not self-ratification. Actual
    self-ratification (RATIFIED/REVIEWED with no traceable operator
    decision) is enforced globally by
    tests/test_repository_contracts.py::test_every_ratified_standard_traces_to_a_decision_record."""
    obj = _load(path)
    assert obj["status"] in ("PROPOSED", "REVIEWED", "RATIFIED"), f"{path.name}: unexpected status {obj['status']!r}"


@pytest.mark.parametrize("path", _standard_files(), ids=lambda p: p.stem)
def test_standard_version_is_at_least_one(path):
    """As drafted in Pass 1, all four were version 1. STD-DATA-COM-002 and
    -003 were later bumped to version 2 by Pass 2.5's revision cycle
    (operator-confirmed precedent: a REVISE verdict on a still-PROPOSED
    draft bumps version, same as the UI domain's COM-007/SKU-001) — see
    tests/test_pass2_5_revisions.py for the precise per-standard version
    assertions and the diff-from-Pass-1 guard on the other two."""
    obj = _load(path)
    assert obj["version"] >= 1


@pytest.mark.parametrize("path", _standard_files(), ids=lambda p: p.stem)
def test_standard_domain_is_data_ontology(path):
    obj = _load(path)
    assert obj["domain"] == "data-ontology"


@pytest.mark.parametrize("path", _standard_files(), ids=lambda p: p.stem)
def test_standard_id_matches_filename(path):
    obj = _load(path)
    assert obj["id"] == path.stem


# -- required content per the task's drafting-principles section --

@pytest.mark.parametrize("path", _standard_files(), ids=lambda p: p.stem)
def test_standard_has_acceptance_and_forbidden(path):
    obj = _load(path)
    assert obj.get("acceptance"), f"{path.name}: missing acceptance criteria"
    assert obj.get("forbidden"), f"{path.name}: missing forbidden-behavior examples"


@pytest.mark.parametrize("path", _standard_files(), ids=lambda p: p.stem)
def test_standard_has_trigger_applicability_clause(path):
    obj = _load(path)
    assert obj.get("trigger"), f"{path.name}: missing trigger/applicability clause"
    assert len(obj["trigger"]) > 30, f"{path.name}: trigger clause looks too thin to be meaningful"


@pytest.mark.parametrize("path", _standard_files(), ids=lambda p: p.stem)
def test_standard_has_required_base_fields(path):
    obj = _load(path)
    required = {
        "id", "title", "domain", "level", "status", "version",
        "requirement", "rationale", "acceptance", "forbidden",
        "evidence", "origin", "introduced", "notes",
    }
    assert required <= obj.keys(), f"{path.name}: missing {required - obj.keys()}"


@pytest.mark.parametrize("path", _standard_files(), ids=lambda p: p.stem)
def test_standard_evidence_entries_are_well_formed(path):
    obj = _load(path)
    for entry in obj["evidence"]:
        assert entry.get("class"), f"{path.name}: evidence entry missing class"
        assert entry.get("source"), f"{path.name}: evidence entry missing source"
        assert entry.get("summary"), f"{path.name}: evidence entry missing summary"


# -- deterministic schema validation --

@pytest.mark.parametrize("path", _standard_files(), ids=lambda p: p.stem)
def test_standard_id_pattern_is_valid(path):
    obj = _load(path)
    assert re.fullmatch(r"STD-[A-Z0-9]+(-[A-Z0-9]+)*-[0-9]{3}", obj["id"])


@pytest.mark.parametrize("path", _standard_files(), ids=lambda p: p.stem)
def test_standard_level_and_origin_are_valid_enums(path):
    obj = _load(path)
    assert obj["level"] in {"MUST", "SHOULD", "MAY"}
    assert obj["origin"] in {
        "OPERATOR_REQUIREMENT", "DIAGNOSTIC_INCIDENT", "CROSS_CLANK_BEST_PRACTICE",
        "ARCHITECTURAL_INVARIANT", "REGRESSION", "EXPERIMENTAL_FINDING",
    }


def test_standard_schema_domain_enum_accepts_data_ontology():
    schema = json.loads((REPO / "schemas" / "standard.schema.json").read_text(encoding="utf-8"))
    assert "data-ontology" in schema["properties"]["domain"]["enum"]


def test_standard_schema_defines_trigger_field():
    schema = json.loads((REPO / "schemas" / "standard.schema.json").read_text(encoding="utf-8"))
    assert "trigger" in schema["properties"], "schema must define the new optional trigger field"


# -- each standard references its Pass 0 evidence/adjudication origin --

@pytest.mark.parametrize("path", _standard_files(), ids=lambda p: p.stem)
def test_standard_notes_reference_pass0_origin(path):
    obj = _load(path)
    notes = obj["notes"]
    assert "docs/data-ontology/pass0/candidates/" in notes, f"{path.name}: notes must cite its Pass 0B candidate card"
    assert "docs/data-ontology/pass0/clusters/" in notes, f"{path.name}: notes must cite its Pass 0A cluster"
    assert "docs/data-ontology/pass1/dossier-" in notes, f"{path.name}: notes must cite its Pass 1 dossier"


@pytest.mark.parametrize("path", _standard_files(), ids=lambda p: p.stem)
def test_standard_notes_referenced_files_exist(path):
    obj = _load(path)
    notes = obj["notes"]
    for ref in re.findall(r"docs/data-ontology/pass[01]/[\w./-]+\.md", notes):
        assert (REPO / ref).is_file(), f"{path.name}: notes references nonexistent file {ref}"


@pytest.mark.parametrize("path", _standard_files(), ids=lambda p: p.stem)
def test_standard_notes_document_their_ratification_status_honestly(path):
    """At Pass 1 drafting time, every draft's notes said 'not ratified' /
    'may not self-ratify'. All four have since been ratified by explicit
    operator ruling — their notes now say RATIFIED and cite the deciding
    decisions/00xx record instead, which is the honest updated statement,
    not a regression of this guard's intent (no undocumented status
    change)."""
    obj = _load(path)
    notes = obj["notes"]
    if obj["status"] == "RATIFIED":
        assert "RATIFIED" in notes
        assert "decisions/" in notes
    else:
        assert "not ratified" in notes.lower()
        assert "self-ratify" in notes.lower() or "self ratify" in notes.lower()


# -- no HOLD/REHOME/REJECT candidate was promoted --

def test_no_hold_rehome_reject_cluster_was_promoted_to_a_standard():
    """A HOLD/REHOME/REJECT cluster may be mentioned in prose as an
    explicit disclaimer (e.g. 'this standard does not cover X, see the
    still-held cluster') — that's a deliberate scope boundary, not a
    promotion. What must never happen is one being cited as an *evidence
    source* the way an ADVANCE cluster is (see
    test_standard_notes_reference_pass0_origin), which would mean its
    content was actually drafted into a standard."""
    for path in _standard_files():
        obj = _load(path)
        evidence_sources = " ".join(e.get("source", "") for e in obj["evidence"])
        for cluster_id in HOLD_REHOME_REJECT_CLUSTER_IDS:
            assert f"clusters/{cluster_id}.md" not in evidence_sources, (
                f"{path.name}: cites HOLD/REHOME/REJECT cluster {cluster_id!r} as an evidence source"
            )


def test_no_fifth_or_sixth_pass0b_candidate_was_drafted():
    """Only C1, C2, C3, C5 may exist as dossiers or standards — not C4, C6, C7."""
    dossier_names = {p.stem for p in PASS1_DIR.glob("dossier-*.md")}
    assert dossier_names == {
        "dossier-c1-continuity-explicitness",
        "dossier-c2-novelty-read-side-exclusion",
        "dossier-c3-identity-conservatism",
        "dossier-c5-provenance-tier-separation",
    }


# -- ADR references resolve where used --

def test_adr_references_cite_only_existing_pass0_evidence_of_them():
    """ADR-0006/ADR-0014 are clank-architecture documents this repo never
    vendors — verify any ADR citation in a drafted standard is corroborated
    by the Pass 0A evidence log (i.e. the citation isn't invented fresh in
    Pass 1, but traces back to material already gathered and preserved)."""
    evidence_log = (PASS0_DIR / "evidence-log.md").read_text()
    for path in _standard_files():
        obj = _load(path)
        text = json.dumps(obj)
        for adr in re.findall(r"ADR-\d{4}", text):
            assert adr in evidence_log, f"{path.name} cites {adr}, which does not appear in Pass 0A's evidence log"


# -- ADVANCE dossiers have the required structure and an explicit recommendation --

@pytest.mark.parametrize(
    "dossier_name",
    [
        "dossier-c1-continuity-explicitness.md",
        "dossier-c2-novelty-read-side-exclusion.md",
        "dossier-c3-identity-conservatism.md",
        "dossier-c5-provenance-tier-separation.md",
    ],
)
def test_dossier_has_required_sections_and_recommendation(dossier_name):
    text = (PASS1_DIR / dossier_name).read_text()
    for heading in [
        "**Candidate ID**", "**Source Pass 0 cluster(s)**", "**Adjudication result**",
        "## Strongest evidence", "## Strongest counterexample", "## Exact semantic boundary",
        "## Overlap analysis", "## Draft rationale", "## Unresolved wording questions",
        "## Recommendation:",
    ]:
        assert heading in text, f"{dossier_name} missing {heading!r}"
    assert re.search(r"## Recommendation: (READY FOR REVIEW|NEEDS NARROWING|HOLD)\s*$", text.strip()), (
        f"{dossier_name}: recommendation must be exactly one of the three allowed values"
    )
    assert "RATIFIED" not in text and "Accepted" not in text, (
        f"{dossier_name}: must not mark anything as ratified/accepted"
    )


# -- no decision record was created marking anything Accepted --

def test_any_accepted_decision_for_these_candidates_is_a_real_operator_ruling():
    """At Pass 1 drafting time, no decision record existed for these four
    at all — this test's original job (no Pass-1-authored Accepted
    record) is now superseded by an explicit, later operator ruling
    (decisions/0010-0013). The live guard: any decision record that DOES
    mark a Data/Ontology draft Accepted must carry a dated 'Operator
    ruling' section, not just a bare status flip."""
    decisions_dir = REPO / "decisions"
    for path in decisions_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        if "STD-DATA-COM" in text and "Status: Accepted" in text:
            assert "Operator ruling" in text, f"{path.name}: marked Accepted with no Operator ruling section"


# -- the frozen UI baseline and manifest are untouched --

def _git(*args) -> str:
    result = subprocess.run(
        ["git", *args], cwd=REPO, capture_output=True, text=True, check=True, stdin=subprocess.DEVNULL,
    )
    return result.stdout.strip()


def test_ui_baseline_manifest_lists_no_data_ontology_standard():
    manifest = json.loads(UI_BASELINE_MANIFEST.read_text(encoding="utf-8"))
    manifest_ids = {s["id"] for s in manifest["standards"]}
    assert manifest_ids.isdisjoint(EXPECTED_IDS), "the UI baseline manifest must never list a Data/Ontology standard"
    assert manifest["corpus"] == "ui"


@pytest.mark.parametrize("path", [
    "standards/ui", "docs/ui",
    "baselines/ui-standards-v1.0.json", "baselines/ui-standards-v1.0-release-notes.md",
])
def test_ui_baseline_paths_unchanged_since_freeze(path):
    """baselines/ is no longer a UI-only directory (it also holds the
    data-ontology-standards-v1.0 freeze) — this checks the UI baseline's
    own files by path, not the whole directory tree, which now
    legitimately has a sibling."""
    tag_tree = _git("rev-parse", f"ui-standards-v1.0:{path}")
    head_tree = _git("rev-parse", f"HEAD:{path}")
    assert tag_tree == head_tree, f"{path} changed since the ui-standards-v1.0 freeze"


def test_ui_standards_tag_still_resolves_to_the_expected_commit():
    # ui-standards-v1.0 is an annotated tag; rev-parse alone returns the
    # tag object's own SHA, not the commit — dereference with ^{commit}.
    resolved = _git("rev-parse", "ui-standards-v1.0^{commit}")
    assert resolved == "d11320704aed69a3d8f854c9264b184e392ec80f"


def test_no_ui_standard_file_was_touched_by_this_pass():
    ui_dir = REPO / "standards" / "ui"
    for path in ui_dir.glob("STD-UI-*.json"):
        tag_blob = _git("rev-parse", f"ui-standards-v1.0:standards/ui/{path.name}")
        head_blob = _git("rev-parse", f"HEAD:standards/ui/{path.name}")
        assert tag_blob == head_blob, f"{path.name} changed since the UI freeze"
