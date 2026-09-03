"""Freeze guards for the data-ontology-standards-v1.0 baseline.

These tests validate the frozen baseline as an immutable historical
snapshot AND (while HEAD's corpus still matches it) its agreement with
the live normative corpus. They deliberately do NOT forbid future
standards: if governance later legitimately adds, revises, supersedes, or
retires a Data/Ontology rule, the agreement tests below will (and should)
fail as a maintenance signal, resolved by recording a NEW baseline —
never by editing the v1.0 manifest or moving the tag. Do not read this
file as asserting the corpus stays four standards forever; it validates
the historical snapshot taken at freeze time.
"""

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

from tools.data_ontology_agent_layer import (
    load_data_ontology_standards,
    load_ratified_data_ontology_standards,
)

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "baselines" / "data-ontology-standards-v1.0.json"
RELEASE_NOTES = REPO / "baselines" / "data-ontology-standards-v1.0-release-notes.md"
HOLD_RESOLUTION = REPO / "docs" / "data-ontology" / "holds-disposition.md"

EXPECTED_VERSIONS = {
    "STD-DATA-COM-001": 1,
    "STD-DATA-COM-002": 2,
    "STD-DATA-COM-003": 2,
    "STD-DATA-COM-004": 1,
}

HELD_MARKERS = [
    "Honest-unknown / availability-honesty backing",
    "Cross-Clank entity identity",
    "Confidence-and-certainty semantics",
    "Canonical fact overwrite discipline",
    "Regional variant identity",
    "Timestamp-shaped values mistaken for chronological truth",
    "Source-disagreement representation",
]


@pytest.fixture(scope="module")
def manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_baseline_manifest_exists_and_is_frozen(manifest):
    assert manifest["baseline_id"] == "data-ontology-standards-v1.0"
    assert manifest["corpus"] == "data-ontology"
    assert manifest["status"] == "FROZEN"
    assert manifest["freeze_date"] == "2026-08-31"


def test_freeze_commit_resolves(manifest):
    sha = manifest["freeze_commit"]
    assert len(sha) == 40
    result = subprocess.run(
        ["git", "-C", str(REPO), "rev-parse", "--verify", "--quiet", f"{sha}^{{commit}}"],
        capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL,
    )
    assert result.returncode == 0, f"freeze commit {sha} does not resolve"


def test_baseline_records_exactly_the_four_ratified_standards(manifest):
    recorded = {s["id"]: (s["status"], s["version"]) for s in manifest["standards"]}
    assert set(recorded) == set(EXPECTED_VERSIONS)
    assert len(recorded) == 4
    for sid, version in EXPECTED_VERSIONS.items():
        assert recorded[sid] == ("RATIFIED", version), f"{sid}: expected (RATIFIED, {version}), found {recorded[sid]}"
    assert manifest["proposed"] == []


def test_baseline_versions_match_normative_files():
    """Agreement test: holds while HEAD's corpus is unchanged since the
    freeze. If governance later legitimately revises/adds/retires a
    Data/Ontology rule, this test is expected to fail — resolve it by
    recording a new baseline, never by editing the v1.0 manifest."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    recorded = {s["id"]: (s["status"], s["version"]) for s in manifest["standards"]}
    live = {s["id"]: (s["status"], s["version"]) for s in load_data_ontology_standards()}
    assert live == recorded, "corpus has diverged from data-ontology-standards-v1.0 — record a new baseline"


def test_zero_proposed_data_ontology_standards_at_freeze():
    live = load_data_ontology_standards()
    proposed = [s["id"] for s in live if s["status"] == "PROPOSED"]
    assert proposed == [], f"unexpected PROPOSED standards at freeze: {proposed}"
    assert {s["id"] for s in load_ratified_data_ontology_standards()} == set(EXPECTED_VERSIONS)


def test_generated_layer_agrees_with_baseline(manifest):
    index = json.loads((REPO / "standards/data-ontology/ratified-index.json").read_text(encoding="utf-8"))
    checklist = json.loads((REPO / "standards/data-ontology/agent-checklist.json").read_text(encoding="utf-8"))
    recorded_ids = {s["id"] for s in manifest["standards"]}
    recorded_versions = {s["id"]: s["version"] for s in manifest["standards"]}
    assert {e["id"] for e in index} == recorded_ids
    assert {e["id"]: e["version"] for e in index} == recorded_versions
    assert {i["standard"] for i in checklist} == recorded_ids


def test_manifest_referenced_artifacts_exist_and_hashes_match(manifest):
    """Artifact hashes are the frozen v1.0 state; while HEAD matches the
    freeze they also match the working tree (same agreement semantics as
    the version test)."""
    for artifact in manifest["artifacts"].values():
        path = REPO / artifact["path"]
        assert path.is_file(), artifact["path"]
        if "sha256" in artifact:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            assert digest == artifact["sha256"], (
                f"{artifact['path']} diverged from the frozen v1.0 state — record a new baseline"
            )


def test_decision_chain_resolves(manifest):
    for ref in manifest["ratification_chain"]:
        assert (REPO / ref).is_file(), ref


def test_hold_resolution_reference_resolves_and_conclusion_is_recorded(manifest):
    ref = manifest["artifacts"]["hold_resolution_audit"]
    path = REPO / ref["path"]
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert ref["conclusion"] in text
    assert "Zero concerns advance into a DATA v1 baseline." in text


def test_held_defer_reject_items_not_in_frozen_corpus(manifest):
    """DEFER/REHOME/REJECT candidates must never appear as frozen
    standards, and must be named in the manifest's excluded set."""
    recorded_ids = {s["id"] for s in manifest["standards"]}
    assert not any(sid.startswith("STD-DATA-C4") or sid.startswith("STD-DATA-C6") or sid.startswith("STD-DATA-C7") for sid in recorded_ids)
    held = manifest["held_set_excluded_from_v1"]
    assert len(held["defer_beyond_v1"]) == 5
    assert len(held["rehome"]) == 1
    assert len(held["reject"]) == 1


def test_release_notes_state_the_freeze_terms_and_reopening_triggers():
    text = RELEASE_NOTES.read_text(encoding="utf-8")
    assert "4 RATIFIED / 0 PROPOSED" in text
    assert "Zero concerns advance into a DATA v1 baseline" in text or "no additional held concern advances" in text
    for term in (
        "Future Data/Ontology standards are not forbidden",
        "may be revised or superseded through governance",
        "not automatically conformant forever",
        "does not prescribe a schema",
        "independent and unchanged",
        "immutable historical records",
    ):
        assert term in text, f"release notes missing freeze term: {term!r}"
    for marker in HELD_MARKERS:
        assert marker in text, f"release notes must preserve held-candidate name: {marker!r}"
    for trigger_fragment in (
        "a second independent instance, an incident, or disposition of the smartphone backlog",
        "adjudication of clank-architecture's ADR-0014, or a concrete cross-Clank collision incident",
        "an operator misreading confidence across Clanks, or a second QC-vocabulary harmonization pass",
        "a documented overwrite-induced provenance loss",
    ):
        assert trigger_fragment in text, f"release notes must preserve reopening trigger: {trigger_fragment!r}"


def test_manifest_generation_is_deterministic():
    """Re-deriving the manifest's standards list from the normative files
    must reproduce exactly what was frozen."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    derived = [
        {"id": s["id"], "version": s["version"], "status": s["status"], "title": s["title"]}
        for s in sorted(load_ratified_data_ontology_standards(), key=lambda x: x["id"])
    ]
    assert manifest["standards"] == derived


def test_ui_baseline_untouched_by_this_freeze():
    """Domain-scoped freeze guard: this pass must not touch the UI
    baseline tag/tree, and must not create a repo-wide 'Standards Clank
    v1.0' tag. Does not assert the data-ontology-standards-v1.0 tag
    itself exists — the freeze guards must be green BEFORE that tag is
    created (tests gate the commit; the tag is created after), so tag
    creation is verified operationally (git ls-remote) after push, not by
    this suite."""
    result = subprocess.run(
        ["git", "-C", str(REPO), "tag", "-l"],
        capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL, check=True,
    )
    tags = set(result.stdout.split())
    assert "ui-standards-v1.0" in tags
    assert not any(t.lower().replace(" ", "-").startswith("standards-clank-v1") for t in tags)

    from tools.ui_agent_layer import assert_ui_frozen_tree_intact
    
    assert_ui_frozen_tree_intact('ui-standards-v1.0', 'standards/ui')
