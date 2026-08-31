"""Evidence-integrity tests for the Operations Pass 0A corpus
(docs/operations/pass0/). These are machinery tests — they check that the
evidence inventory is structurally sound (files exist, frontmatter is
well-formed, no normative standard was accidentally created, both frozen
baselines were not touched) — they do NOT encode any candidate invariant
from the clusters as normative truth. Pass 0A is evidence only.

Mirrors tests/test_pass0_evidence.py's design for the Data/Ontology
domain, adapted for Operations' own cluster-id/topic-number scheme
(descriptive kebab-case ids + a list of the 15 brief topic numbers each
cluster covers, rather than single letters A-G).
"""

import json
import re
import subprocess
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).parent.parent
PASS0_DIR = REPO_ROOT / "docs" / "operations" / "pass0"
CLUSTERS_DIR = PASS0_DIR / "clusters"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

VALID_CONFIDENCE = {"STRONG", "MODERATE", "WEAK"}
VALID_PRIORITY = {"HIGH", "MEDIUM", "LOW"}
VALID_TOPICS = set(range(1, 16))

CLUSTER_ID_RE = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")


def _cluster_files():
    return sorted(CLUSTERS_DIR.glob("*.md"))


def _parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    assert match, f"{path} has no YAML frontmatter block"
    return yaml.safe_load(match.group(1))


# -- required top-level files exist --

@pytest.mark.parametrize(
    "name",
    ["README.md", "evidence-log.md", "incident-ledger.md", "terminology-map.md", "handoff.md"],
)
def test_required_pass0_file_exists(name):
    path = PASS0_DIR / name
    assert path.is_file(), f"missing required Pass 0 file: {path}"
    assert len(path.read_text(encoding="utf-8")) > 200, f"{path} looks suspiciously empty"


def test_clusters_directory_has_fifteen_files():
    files = _cluster_files()
    assert len(files) == 15, f"expected 15 candidate-cluster files, found {len(files)}: {[f.name for f in files]}"


# -- frontmatter structure on every cluster file --

@pytest.mark.parametrize("path", _cluster_files(), ids=lambda p: p.stem)
def test_cluster_frontmatter_has_required_fields(path):
    fm = _parse_frontmatter(path)
    required = {"id", "domain", "topics", "confidence", "priority"}
    assert required <= fm.keys(), f"{path.name} missing frontmatter fields: {required - fm.keys()}"


@pytest.mark.parametrize("path", _cluster_files(), ids=lambda p: p.stem)
def test_cluster_id_matches_filename(path):
    fm = _parse_frontmatter(path)
    assert fm["id"] == path.stem, f"{path.name}: frontmatter id {fm['id']!r} does not match filename"
    assert CLUSTER_ID_RE.fullmatch(fm["id"]), f"{path.name}: id {fm['id']!r} is not kebab-case"


@pytest.mark.parametrize("path", _cluster_files(), ids=lambda p: p.stem)
def test_cluster_domain_is_operations(path):
    fm = _parse_frontmatter(path)
    assert fm["domain"] == "operations"


@pytest.mark.parametrize("path", _cluster_files(), ids=lambda p: p.stem)
def test_cluster_confidence_is_valid(path):
    fm = _parse_frontmatter(path)
    assert fm["confidence"] in VALID_CONFIDENCE, f"{path.name}: invalid confidence {fm['confidence']!r}"


@pytest.mark.parametrize("path", _cluster_files(), ids=lambda p: p.stem)
def test_cluster_priority_is_valid(path):
    fm = _parse_frontmatter(path)
    assert fm["priority"] in VALID_PRIORITY, f"{path.name}: invalid priority {fm['priority']!r}"


@pytest.mark.parametrize("path", _cluster_files(), ids=lambda p: p.stem)
def test_cluster_topics_are_valid(path):
    fm = _parse_frontmatter(path)
    topics = set(fm["topics"])
    assert topics, f"{path.name}: topics list is empty"
    assert topics <= VALID_TOPICS, f"{path.name}: invalid topic numbers {topics - VALID_TOPICS}"


@pytest.mark.parametrize("path", _cluster_files(), ids=lambda p: p.stem)
def test_cluster_has_required_body_sections(path):
    text = path.read_text(encoding="utf-8")
    required_headings = [
        "## Concern",
        "## Current terminology",
        "## Repos surveyed",
        "## Independent evidence",
        "## Inherited evidence",
        "## Incidents",
        "## Implementations",
        "## Counterexamples",
        "## Harm if violated",
        "## Likely domain",
        "## Unresolved questions",
    ]
    for heading in required_headings:
        assert heading in text, f"{path.name} missing required section: {heading!r}"


def test_no_duplicate_cluster_ids():
    ids = [_parse_frontmatter(p)["id"] for p in _cluster_files()]
    assert len(ids) == len(set(ids)), f"duplicate cluster ids: {ids}"


def test_every_topic_1_to_15_is_covered_by_at_least_one_cluster():
    covered = set()
    for p in _cluster_files():
        covered |= set(_parse_frontmatter(p)["topics"])
    assert covered == VALID_TOPICS, f"topics with no covering cluster: {VALID_TOPICS - covered}"


# -- README's cluster table matches the actual files --

def test_readme_references_every_cluster_file():
    readme = (PASS0_DIR / "README.md").read_text(encoding="utf-8")
    for path in _cluster_files():
        rel = f"clusters/{path.name}"
        assert rel in readme, f"README.md does not reference {rel}"


# -- this pass must not create any normative standard --

def test_no_std_operations_files_exist_anywhere():
    matches = list(REPO_ROOT.rglob("STD-OPERATIONS-*.json"))
    assert matches == [], f"Pass 0A must not create any STD-OPERATIONS file: {matches}"


def test_operations_domain_enum_extension_is_additive_only():
    """At Pass 0A's original writing, 'operations' was not yet in the
    domain enum — this test asserted its absence, since adding it is
    Pass 1's job. A later, separately-authorized Pass 1 legitimately
    added it (see tests/test_ops_pass1_drafting.py for the live drafting
    guards). This test's remaining live job: confirm that addition was
    purely additive — every domain present before Pass 1 is still
    present, nothing was removed or renamed."""
    schema = json.loads((REPO_ROOT / "schemas" / "standard.schema.json").read_text(encoding="utf-8"))
    domain_enum = set(schema["properties"]["domain"]["enum"])
    pre_pass1_domains = {
        "ui", "collectors", "sources", "classification", "events",
        "evidence", "health", "delivery", "soak", "security", "operator-workflow",
        "data-ontology",
    }
    assert pre_pass1_domains <= domain_enum, f"a pre-existing domain was removed: {pre_pass1_domains - domain_enum}"
    assert "operations" in domain_enum


def test_pass0_directory_contains_no_json_standard_files():
    json_files = list(PASS0_DIR.rglob("*.json"))
    assert json_files == [], f"Pass 0A evidence directory must contain no JSON standard files: {json_files}"


def test_no_target_clank_or_diagnostic_clank_directories_vendored():
    """This repo must never contain a copy of another Clank's source —
    evidence must be cited by file:line, not vendored in. The
    diagnostic-clank clone used for this survey lived in a scratch
    directory outside this repository, never here."""
    fleet_names = {
        "watch-clank", "smartwatch-clank", "smartphone-clank", "tablet-clank",
        "feature-phone-clank", "oem-radar", "chinese-tech-wire",
        "korean-tech-wire", "semiconductor-intelligence", "clank-architecture",
        "diagnostic-clank",
    }
    top_level = {p.name for p in REPO_ROOT.iterdir() if p.is_dir()}
    assert not (fleet_names & top_level), f"found vendored Clank directories: {fleet_names & top_level}"


# -- both frozen baselines must be untouched --

def _git(*args) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
        stdin=subprocess.DEVNULL,
    )
    return result.stdout.strip()


def test_ui_baseline_tag_exists_and_resolves():
    resolved = _git("rev-parse", "ui-standards-v1.0^{commit}")
    assert resolved == "d11320704aed69a3d8f854c9264b184e392ec80f"


def test_data_ontology_baseline_tag_exists_and_resolves():
    resolved = _git("rev-parse", "data-ontology-standards-v1.0^{commit}")
    assert resolved == "464a8057ea5dc26ef83248a20bafa0be5aa31148"


@pytest.mark.parametrize("path", [
    "standards/ui", "docs/ui",
    "baselines/ui-standards-v1.0.json", "baselines/ui-standards-v1.0-release-notes.md",
])
def test_ui_baseline_paths_unchanged_since_freeze(path):
    tag_tree = _git("rev-parse", f"ui-standards-v1.0:{path}")
    head_tree = _git("rev-parse", f"HEAD:{path}")
    assert tag_tree == head_tree, f"{path} changed since the ui-standards-v1.0 freeze"


@pytest.mark.parametrize("path", [
    "standards/data-ontology", "docs/data-ontology",
    "baselines/data-ontology-standards-v1.0.json",
    "baselines/data-ontology-standards-v1.0-release-notes.md",
])
def test_data_ontology_baseline_paths_unchanged_since_freeze(path):
    tag_tree = _git("rev-parse", f"data-ontology-standards-v1.0:{path}")
    head_tree = _git("rev-parse", f"HEAD:{path}")
    assert tag_tree == head_tree, f"{path} changed since the data-ontology-standards-v1.0 freeze"


# -- handoff.md references only real cluster files, covers every HIGH cluster --

def test_handoff_references_valid_cluster_files():
    handoff_text = (PASS0_DIR / "handoff.md").read_text(encoding="utf-8")
    cluster_names = {p.name for p in _cluster_files()}
    referenced = re.findall(r"clusters/([a-z0-9-]+\.md)", handoff_text)
    for name in referenced:
        assert name in cluster_names, f"handoff.md references nonexistent cluster file clusters/{name}"


def test_handoff_covers_every_high_priority_cluster():
    handoff_text = (PASS0_DIR / "handoff.md").read_text(encoding="utf-8")
    readme_text = (PASS0_DIR / "README.md").read_text(encoding="utf-8")
    for path in _cluster_files():
        fm = _parse_frontmatter(path)
        if fm["priority"] != "HIGH":
            continue
        assert f"clusters/{path.name}" in readme_text, (
            f"HIGH priority cluster {fm['id']!r} not linked from README's table"
        )


def test_handoff_flags_the_fleet_law_reconciliation_question():
    """The operations domain's defining difference from data-ontology's
    Pass 0A: several clusters overlap ACTIVE (not proposed) governance in
    clank-architecture/FLEET_LAWS.md. This must be surfaced to Pass 0B,
    not silently absorbed."""
    handoff_text = (PASS0_DIR / "handoff.md").read_text(encoding="utf-8")
    assert "Fleet Law" in handoff_text
    assert "ACTIVE" in handoff_text


# -- incident ledger sanity --

def test_incident_ledger_has_substantial_content():
    text = (PASS0_DIR / "incident-ledger.md").read_text(encoding="utf-8")
    incident_rows = re.findall(r"^\| INC-\d+ \|", text, flags=re.MULTILINE)
    assert len(incident_rows) >= 20, f"expected at least 20 incident rows, found {len(incident_rows)}"


def test_incident_ids_are_unique():
    text = (PASS0_DIR / "incident-ledger.md").read_text(encoding="utf-8")
    ids = re.findall(r"^\| (INC-\d+) \|", text, flags=re.MULTILINE)
    assert len(ids) == len(set(ids)), "duplicate INC-* ids in incident-ledger.md"
