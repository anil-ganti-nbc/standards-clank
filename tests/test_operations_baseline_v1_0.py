"""Freeze guards for the operations-standards-v1.0 baseline.

These tests validate the frozen baseline as an immutable historical
snapshot AND (while HEAD's corpus still matches it) its agreement with
the live normative corpus. They deliberately do NOT forbid future
standards: if governance later legitimately adds, revises, supersedes, or
retires an Operations rule, the agreement tests below will (and should)
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

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "baselines" / "operations-standards-v1.0.json"
RELEASE_NOTES = REPO / "baselines" / "operations-standards-v1.0-release-notes.md"
HOLD_RESOLUTION = REPO / "docs" / "operations" / "holds-disposition.md"

EXPECTED_VERSIONS = {
    "STD-OPS-COM-001": 1,
    "STD-OPS-COM-002": 1,
    "STD-OPS-COM-003": 1,
    "STD-OPS-COM-004": 1,
}

HELD_MARKERS = [
    "Lifecycle-state model: BLOCKED is prose, not code",
    "Destructive production-action authority",
    "Config drift",
    "schema/deploy",
    "Delivery retry/idempotency",
]


@pytest.fixture(scope="module")
def manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_baseline_manifest_exists_and_is_frozen(manifest):
    assert manifest["baseline_id"] == "operations-standards-v1.0"
    assert manifest["corpus"] == "operations"
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
    freeze. If governance later legitimately revises/adds/retires an
    Operations rule, this test is expected to fail — resolve it by
    recording a new baseline, never by editing the v1.0 manifest."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    recorded = {s["id"]: (s["status"], s["version"]) for s in manifest["standards"]}
    live = {}
    for sid in EXPECTED_VERSIONS:
        obj = json.loads((REPO / "standards" / "operations" / f"{sid}.json").read_text(encoding="utf-8"))
        live[sid] = (obj["status"], obj["version"])
    assert live == recorded, "corpus has diverged from operations-standards-v1.0 — record a new baseline"


def test_zero_proposed_operations_standards_at_freeze():
    files = sorted((REPO / "standards" / "operations").glob("STD-OPS-*.json"))
    assert {p.stem for p in files} == set(EXPECTED_VERSIONS)
    for path in files:
        obj = json.loads(path.read_text(encoding="utf-8"))
        assert obj["status"] == "RATIFIED", f"{obj['id']}: expected RATIFIED at freeze"


def test_manifest_referenced_standard_files_exist_and_hashes_match(manifest):
    """Artifact hashes are the frozen v1.0 state; while HEAD matches the
    freeze they also match the working tree (same agreement semantics as
    the version test)."""
    for sid, artifact in manifest["artifacts"]["standard_files"].items():
        path = REPO / artifact["path"]
        assert path.is_file(), artifact["path"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == artifact["sha256"], (
            f"{artifact['path']} diverged from the frozen v1.0 state — record a new baseline"
        )


def test_manifest_now_records_the_built_agent_layer(manifest):
    """At freeze time this test asserted no agent-facing layer existed
    yet for Operations (unlike ui-standards-v1.0 and
    data-ontology-standards-v1.0). A later, separately-authorized
    housekeeping task legitimately built one, mirroring the UI/Data-Ontology
    pattern. The frozen tag (commit 7100f29) still correctly records
    'no agent layer' as true at that point in history; this test's
    remaining live job is the forward state — confirm the manifest's
    artifacts fields and the actual files now agree."""
    assert manifest["artifacts"]["ratified_index"]["path"] == "standards/operations/ratified-index.json"
    assert manifest["artifacts"]["agent_checklist"]["path"] == "standards/operations/agent-checklist.json"
    assert manifest["artifacts"]["constitution"]["path"] == "docs/operations/constitution.md"
    assert "artifacts_note" in manifest
    assert (REPO / "tools" / "operations_agent_layer.py").is_file()
    assert (REPO / "standards" / "operations" / "ratified-index.json").is_file()
    assert (REPO / "docs" / "operations" / "constitution.md").is_file()
    for artifact_key in ("ratified_index", "agent_checklist"):
        artifact = manifest["artifacts"][artifact_key]
        digest = hashlib.sha256((REPO / artifact["path"]).read_bytes()).hexdigest()
        assert digest == artifact["sha256"], f"{artifact['path']} diverged from the manifest's recorded hash"


def test_decision_chain_resolves(manifest):
    for ref in manifest["ratification_chain"]:
        assert (REPO / ref).is_file(), ref


def test_hold_resolution_reference_resolves_and_conclusion_is_recorded(manifest):
    ref = manifest["artifacts"]["hold_resolution_audit"]
    path = REPO / ref["path"]
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert ref["conclusion"] in text
    assert "NO ESSENTIAL OPERATIONS CONTRACT MISSING" in text


def test_held_deferred_rehomed_items_not_in_frozen_corpus(manifest):
    recorded_ids = {s["id"] for s in manifest["standards"]}
    assert len(recorded_ids) == 4
    held = manifest["held_set_excluded_from_v1"]
    assert len(held["hold"]) == 1
    assert len(held["defer"]) == 1
    assert len(held["rehome_deployment_domain"]) == 3
    assert len(held["rehome_delivery_domain"]) == 1


def test_ops_com_004_provenance_note_present_and_corrected(manifest):
    """At freeze time (tag operations-standards-v1.0, commit 7100f29),
    this test asserted a 'known_review_path_note' claiming STD-OPS-COM-004
    never received a dedicated post-draft adversarial review. That was
    stale by the time of ratification closure: a dedicated closure-time
    review of the finished text had already run and returned APPROVE FOR
    RATIFICATION before the operator ratified. The tag is left exactly
    where it is (the immutable historical record of what was believed at
    freeze time); this test's remaining live job is the forward
    correction — confirm the manifest now carries the accurate
    provenance chain, not the stale claim."""
    assert "ops_com_004_provenance_note" in manifest
    note = manifest["ops_com_004_provenance_note"]
    assert "STD-OPS-COM-004" in note
    assert "APPROVE FOR RATIFICATION" in note
    assert "Forward correction" in note
    assert "known_review_path_note" not in manifest


def test_release_notes_state_the_freeze_terms():
    text = RELEASE_NOTES.read_text(encoding="utf-8")
    assert "4 RATIFIED / 0 PROPOSED" in text
    assert "NO ESSENTIAL OPERATIONS CONTRACT MISSING" in text
    for term in (
        "Future Operations standards are not forbidden",
        "may be revised or superseded through governance",
        "not automatically conformant forever",
        "does not prescribe a scheduler technology",
        "independent and unchanged",
        "immutable historical records",
        "Post-freeze forward update",
    ):
        assert term in text, f"release notes missing freeze term: {term!r}"
    for marker in HELD_MARKERS:
        assert marker in text, f"release notes must preserve held/deferred/rehomed concern name: {marker!r}"


def test_release_notes_carry_the_corrected_ops_com_004_provenance():
    """At freeze time this test checked for the (then-current, later
    found stale) 'different review path' claim. Superseded: the release
    notes now carry the forward-corrected provenance chain ending in a
    dedicated closure-time review that returned APPROVE FOR RATIFICATION."""
    text = RELEASE_NOTES.read_text(encoding="utf-8")
    assert "forward correction" in text.lower()
    assert "APPROVE FOR RATIFICATION" in text
    assert "STD-OPS-COM-004" in text


def test_manifest_generation_is_deterministic():
    """Re-deriving the manifest's standards list from the normative files
    must reproduce exactly what was frozen."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    derived = []
    for path in sorted((REPO / "standards" / "operations").glob("STD-OPS-*.json")):
        obj = json.loads(path.read_text(encoding="utf-8"))
        derived.append({"id": obj["id"], "version": obj["version"], "status": obj["status"], "title": obj["title"]})
    assert manifest["standards"] == derived


def test_deployment_and_delivery_rehomes_remain_out_of_operations_baseline(manifest):
    """The later-authorized Deployment Pass 1 proposals are outside this
    frozen Operations corpus; this guard protects the historical manifest,
    not the future absence of another domain's proposals."""
    ids = {s["id"] for s in manifest["standards"]}
    assert not any(i.startswith("STD-DEPLOYMENT-") or i.startswith("STD-DELIVERY-") for i in ids)
    assert not list(REPO.glob("standards/delivery/STD-*.json"))


def test_ui_and_data_ontology_baselines_untouched_by_this_freeze():
    """Domain-scoped freeze guard: this pass must not touch the UI or
    Data/Ontology baseline tags/trees, and must not create a repo-wide
    'Standards Clank v1.0' tag."""
    result = subprocess.run(
        ["git", "-C", str(REPO), "tag", "-l"],
        capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL, check=True,
    )
    tags = set(result.stdout.split())
    assert "ui-standards-v1.0" in tags
    assert "data-ontology-standards-v1.0" in tags
    assert not any(t.lower().replace(" ", "-").startswith("standards-clank-v1") for t in tags)

    for tag, path in (
        ("ui-standards-v1.0", "standards/ui"),
        ("data-ontology-standards-v1.0", "standards/data-ontology"),
    ):
        tag_tree = subprocess.run(
            ["git", "-C", str(REPO), "rev-parse", f"{tag}:{path}"],
            capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL, check=True,
        ).stdout.strip()
        head_tree = subprocess.run(
            ["git", "-C", str(REPO), "rev-parse", f"HEAD:{path}"],
            capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL, check=True,
        ).stdout.strip()
        assert tag_tree == head_tree, f"{path} changed by the operations freeze"
