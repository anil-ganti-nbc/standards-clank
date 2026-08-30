"""Freeze guards for the ui-standards-v1.0 baseline.

These tests validate the frozen baseline as an immutable historical
snapshot AND (while HEAD still matches it) its agreement with the live
normative corpus. They deliberately do NOT forbid future standards: if
governance later legitimately adds, revises, supersedes, or retires UI
rules, the agreement tests below will (and should) fail as a maintenance
signal, resolved by recording a new baseline — never by editing the
v1.0 manifest or moving the tag.
"""

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

from tools.ui_agent_layer import load_ui_standards, load_ratified_ui_standards

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "baselines" / "ui-standards-v1.0.json"
RELEASE_NOTES = REPO / "baselines" / "ui-standards-v1.0-release-notes.md"
EXPECTED_IDS = {
    "STD-UI-COM-001", "STD-UI-COM-002", "STD-UI-COM-003", "STD-UI-COM-004",
    "STD-UI-COM-005", "STD-UI-COM-006", "STD-UI-COM-007", "STD-UI-COM-008",
    "STD-UI-COM-009", "STD-UI-COM-010", "STD-UI-COM-011", "STD-UI-COM-012",
    "STD-UI-NEWS-001", "STD-UI-NEWS-002", "STD-UI-SKU-001",
}


@pytest.fixture(scope="module")
def manifest():
    return json.loads(MANIFEST.read_text())


def test_baseline_manifest_exists_and_is_frozen(manifest):
    assert manifest["baseline_id"] == "ui-standards-v1.0"
    assert manifest["corpus"] == "ui"
    assert manifest["status"] == "FROZEN"
    assert manifest["freeze_date"] == "2026-08-31"


def test_freeze_commit_resolves(manifest):
    sha = manifest["freeze_commit"]
    assert len(sha) == 40
    result = subprocess.run(
        ["git", "-C", str(REPO), "rev-parse", "--verify", "--quiet", f"{sha}^{{commit}}"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, f"freeze commit {sha} does not resolve"


def test_baseline_records_exactly_the_frozen_corpus(manifest):
    recorded = {s["id"]: (s["status"], s["version"]) for s in manifest["standards"]}
    assert set(recorded) == EXPECTED_IDS
    assert len(recorded) == 15
    assert all(status == "RATIFIED" for status, _ in recorded.values())
    assert manifest["proposed"] == []


def test_baseline_versions_match_normative_files():
    """Agreement test: holds while HEAD's corpus is unchanged since the
    freeze. If governance later legitimately revises/adds/retires a UI
    rule, this test is expected to fail — resolve it by recording a new
    baseline, never by editing the v1.0 manifest."""
    manifest = json.loads(MANIFEST.read_text())
    recorded = {s["id"]: (s["status"], s["version"]) for s in manifest["standards"]}
    live = {s["id"]: (s["status"], s["version"]) for s in load_ui_standards()}
    assert live == recorded, "corpus has diverged from ui-standards-v1.0 — record a new baseline"


def test_generated_layer_agrees_with_baseline():
    manifest = json.loads(MANIFEST.read_text())
    index = json.loads((REPO / "standards/ui/ratified-index.json").read_text())
    checklist = json.loads((REPO / "standards/ui/agent-checklist.json").read_text())
    recorded_ids = {s["id"] for s in manifest["standards"]}
    assert {e["id"] for e in index} == recorded_ids
    assert {i["standard"] for i in checklist} == recorded_ids


def test_manifest_referenced_artifacts_exist_and_hashes_match():
    """Artifact hashes are the frozen v1.0 state; while HEAD matches the
    freeze they also match the working tree (same agreement semantics as
    the version test)."""
    manifest = json.loads(MANIFEST.read_text())
    for artifact in manifest["artifacts"].values():
        path = REPO / artifact["path"]
        assert path.is_file(), artifact["path"]
        if "sha256" in artifact:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            assert digest == artifact["sha256"], (
                f"{artifact['path']} diverged from the frozen v1.0 state — record a new baseline"
            )


def test_gap_audit_reference_and_conclusion_present(manifest):
    gap = manifest["artifacts"]["final_gap_audit"]
    assert gap["conclusion"] == "NO ESSENTIAL UI CONTRACT MISSING"
    assert "NO ESSENTIAL UI CONTRACT MISSING" in (REPO / gap["path"]).read_text()


def test_remediation_verifications_exist_and_say_verified(manifest):
    for entry in manifest["remediation_verifications"]:
        audit = REPO / entry["audit"]
        assert audit.is_file()
        assert "REMEDIATION_VERIFIED" in audit.read_text(), entry["clank"]


def test_baseline_decision_chain_resolves(manifest):
    for chain in ("ratification_chain", "interpretation_and_governance_chain"):
        for ref in manifest[chain]:
            assert (REPO / ref).is_file(), ref


def test_release_notes_state_the_freeze_terms():
    text = RELEASE_NOTES.read_text()
    assert "15 RATIFIED / 0 PROPOSED" in text
    assert "NO ESSENTIAL UI CONTRACT MISSING" in text
    for term in (
        "Future UI standards are not forbidden",
        "Standards may be superseded through governance",
        "not automatically conformant forever",
        "covers the UI corpus only",
        "remediation backlog",
        "immutable historical records",
    ):
        assert term in text, f"release notes missing freeze term: {term!r}"


def test_manifest_generation_is_deterministic():
    """Re-deriving the manifest's standards list from the normative files
    must reproduce exactly what was frozen."""
    manifest = json.loads(MANIFEST.read_text())
    derived = [
        {"id": s["id"], "version": s["version"], "status": s["status"], "title": s["title"]}
        for s in sorted(load_ui_standards(), key=lambda x: x["id"])
    ]
    assert manifest["standards"] == derived
