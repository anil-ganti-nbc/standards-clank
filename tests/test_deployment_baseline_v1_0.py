"""Freeze guards for the immutable Deployment Standards v1.0 baseline."""

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "baselines" / "deployment-standards-v1.0.json"
RELEASE_NOTES = REPO / "baselines" / "deployment-standards-v1.0-release-notes.md"
AUDIT = REPO / "docs" / "deployment" / "holds-disposition.md"
DEPLOY = REPO / "standards" / "deployment"
FREEZE_CORPUS_COMMIT = "8f7f78bb3be351d66ed1f314576e0762e1211d9e"
TAG = "deployment-standards-v1.0"
PREVIOUS_TAGS = {
    "ui-standards-v1.0": "d11320704aed69a3d8f854c9264b184e392ec80f",
    "data-ontology-standards-v1.0": "464a8057ea5dc26ef83248a20bafa0be5aa31148",
    "operations-standards-v1.0": "7100f294a83c30594f2ff9e953f7c9f77a95747f",
}


def _hash(path):
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


@pytest.fixture(scope="module")
def manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_manifest_and_release_notes_identify_the_frozen_baseline(manifest):
    assert RELEASE_NOTES.is_file()
    assert manifest["baseline_id"] == TAG
    assert manifest["corpus"] == "deployment"
    assert manifest["status"] == "FROZEN"
    assert manifest["version"] == "1.0"
    assert manifest["freeze_commit"] == FREEZE_CORPUS_COMMIT
    assert manifest["immutable_tag"] == TAG
    notes = RELEASE_NOTES.read_text(encoding="utf-8")
    for marker in ("2 RATIFIED / 0 PROPOSED", "NO ESSENTIAL DEPLOYMENT CONTRACT MISSING", "10 confirmed Deployment incidents were reused", "0 newly discovered Deployment-specific incidents"):
        assert marker in notes


def test_exact_frozen_standard_set_and_contents_match_manifest(manifest):
    expected = {"STD-DEPLOY-COM-001", "STD-DEPLOY-COM-002"}
    records = {item["id"]: item for item in manifest["standards"]}
    assert set(records) == expected and manifest["proposed"] == []
    files = sorted(DEPLOY.glob("STD-DEPLOY-*.json"))
    assert {path.stem for path in files} == expected
    for sid, record in records.items():
        assert record["version"] == 1 and record["status"] == "RATIFIED"
        obj = json.loads((DEPLOY / f"{sid}.json").read_text(encoding="utf-8"))
        assert obj["version"] == 1 and obj["status"] == "RATIFIED"
        artifact = manifest["artifacts"]["standard_files"][sid]
        assert _hash(REPO / artifact["path"]) == artifact["sha256_lf_normalized"]


def test_agent_layer_decisions_and_final_gap_provenance_are_current(manifest):
    from tools.deployment_agent_layer import build_agent_checklist, build_ratified_index

    assert json.loads((DEPLOY / "ratified-index.json").read_text(encoding="utf-8")) == build_ratified_index()
    assert json.loads((DEPLOY / "agent-checklist.json").read_text(encoding="utf-8")) == build_agent_checklist()
    for key in ("ratified_index", "agent_checklist"):
        artifact = manifest["artifacts"][key]
        assert _hash(REPO / artifact["path"]) == artifact["sha256_lf_normalized"]
    for decision in ("0018-deploy-com-001-decision.md", "0019-deploy-com-002-decision.md"):
        assert "Status: Accepted" in (REPO / "decisions" / decision).read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")
    assert "NO ESSENTIAL DEPLOYMENT CONTRACT MISSING" in audit
    assert "READY TO FREEZE DEPLOYMENT STANDARDS V1.0" in audit
    # The frozen normative baseline remains unchanged; the post-freeze
    # Deployment known-evidence layer is generated from the final audit.
    assert (DEPLOY / "known-evidence-index.json").is_file()
    assert manifest["artifacts"]["conformance_audit"] is None


def test_residuals_and_prior_baselines_are_preserved(manifest):
    residuals = manifest["residual_dispositions"]
    assert "ACTIVE" in residuals["identity_mechanics"]
    assert "DEFERRED" in residuals["law_9"]
    assert "PROPOSED — REVIEWED DRAFT" in residuals["destructive_state"]
    assert "COM-001 facet" in residuals["config_congruence"]
    for tag, expected in PREVIOUS_TAGS.items():
        actual = subprocess.run(["git", "rev-parse", f"{tag}^{{}}"], cwd=REPO, capture_output=True, text=True, check=True, stdin=subprocess.DEVNULL).stdout.strip()
        assert actual == expected


def test_deployment_tag_is_annotated_and_targets_freeze_commit_after_creation():
    result = subprocess.run(["git", "rev-parse", "--verify", "--quiet", f"refs/tags/{TAG}"], cwd=REPO, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    if result.returncode:
        pytest.skip("tag is created after the pre-tag validation suite")
    tag_type = subprocess.run(["git", "cat-file", "-t", TAG], cwd=REPO, capture_output=True, text=True, check=True, stdin=subprocess.DEVNULL).stdout.strip()
    assert tag_type == "tag"
    tag_commit = subprocess.run(["git", "rev-parse", f"{TAG}^{{}}"], cwd=REPO, capture_output=True, text=True, check=True, stdin=subprocess.DEVNULL).stdout.strip()
    # Forward-only tooling/audit commits legitimately follow the frozen baseline.
    # The tag must stay attached to the recorded freeze commit, not mutable HEAD.
    assert tag_commit == "33cc38849180716fd4d06b1356cf70c49d3d41d2"
