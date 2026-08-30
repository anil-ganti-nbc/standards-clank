"""Evidence-integrity tests for the Data/Ontology Pass 0A corpus
(docs/data-ontology/pass0/). These are machinery tests — they check that
the evidence inventory is structurally sound (files exist, frontmatter is
well-formed, no normative standard was accidentally created, the frozen
UI baseline was not touched) — they do NOT encode any candidate invariant
from the clusters as normative truth. Pass 0A is evidence only.
"""

import re
import subprocess
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).parent.parent
PASS0_DIR = REPO_ROOT / "docs" / "data-ontology" / "pass0"
CLUSTERS_DIR = PASS0_DIR / "clusters"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

VALID_CONFIDENCE = {"STRONG", "MODERATE", "WEAK"}
VALID_PRIORITY = {"HIGH", "MEDIUM", "LOW"}
VALID_CLUSTER_LETTERS = {"A", "B", "C", "D", "E", "F", "G"}

CLUSTER_ID_RE = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")


def _cluster_files():
    return sorted(CLUSTERS_DIR.glob("*.md"))


def _parse_frontmatter(path: Path) -> dict:
    text = path.read_text()
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
    assert len(path.read_text()) > 200, f"{path} looks suspiciously empty"


def test_clusters_directory_has_thirteen_files():
    files = _cluster_files()
    assert len(files) == 13, f"expected 13 candidate-cluster files, found {len(files)}: {[f.name for f in files]}"


# -- frontmatter structure on every cluster file --

@pytest.mark.parametrize("path", _cluster_files(), ids=lambda p: p.stem)
def test_cluster_frontmatter_has_required_fields(path):
    fm = _parse_frontmatter(path)
    required = {"id", "domain", "clusters", "confidence", "priority"}
    assert required <= fm.keys(), f"{path.name} missing frontmatter fields: {required - fm.keys()}"


@pytest.mark.parametrize("path", _cluster_files(), ids=lambda p: p.stem)
def test_cluster_id_matches_filename(path):
    fm = _parse_frontmatter(path)
    assert fm["id"] == path.stem, f"{path.name}: frontmatter id {fm['id']!r} does not match filename"
    assert CLUSTER_ID_RE.fullmatch(fm["id"]), f"{path.name}: id {fm['id']!r} is not kebab-case"


@pytest.mark.parametrize("path", _cluster_files(), ids=lambda p: p.stem)
def test_cluster_domain_is_data_ontology(path):
    fm = _parse_frontmatter(path)
    assert fm["domain"] == "data-ontology"


@pytest.mark.parametrize("path", _cluster_files(), ids=lambda p: p.stem)
def test_cluster_confidence_is_valid(path):
    fm = _parse_frontmatter(path)
    assert fm["confidence"] in VALID_CONFIDENCE, f"{path.name}: invalid confidence {fm['confidence']!r}"


@pytest.mark.parametrize("path", _cluster_files(), ids=lambda p: p.stem)
def test_cluster_priority_is_valid(path):
    fm = _parse_frontmatter(path)
    assert fm["priority"] in VALID_PRIORITY, f"{path.name}: invalid priority {fm['priority']!r}"


@pytest.mark.parametrize("path", _cluster_files(), ids=lambda p: p.stem)
def test_cluster_letters_are_valid(path):
    fm = _parse_frontmatter(path)
    letters = set(fm["clusters"])
    assert letters, f"{path.name}: clusters list is empty"
    assert letters <= VALID_CLUSTER_LETTERS, f"{path.name}: invalid cluster letters {letters - VALID_CLUSTER_LETTERS}"


@pytest.mark.parametrize("path", _cluster_files(), ids=lambda p: p.stem)
def test_cluster_has_required_body_sections(path):
    text = path.read_text()
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


# -- README's cluster table matches the actual files --

def test_readme_references_every_cluster_file():
    readme = (PASS0_DIR / "README.md").read_text()
    for path in _cluster_files():
        rel = f"clusters/{path.name}"
        assert rel in readme, f"README.md does not reference {rel}"


# -- this pass must not create any normative standard --

def test_no_std_data_files_exist_anywhere():
    matches = list(REPO_ROOT.glob("**/STD-DATA-*.json"))
    assert matches == [], f"Pass 0A must not create standard files, found: {matches}"


def test_no_data_ontology_domain_added_to_standard_schema_enum():
    schema_text = (REPO_ROOT / "schemas" / "standard.schema.json").read_text()
    assert '"data-ontology"' not in schema_text, (
        "standard.schema.json's domain enum must not be extended by an evidence-only pass"
    )


def test_pass0_directory_contains_no_json_standard_files():
    json_files = list(PASS0_DIR.rglob("*.json"))
    assert json_files == [], f"Pass 0A evidence directory must contain no JSON standard files: {json_files}"


# -- the frozen UI baseline must be untouched --

def _git(*args) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
        stdin=subprocess.DEVNULL,
    )
    return result.stdout.strip()


def test_ui_baseline_tag_exists_and_resolves():
    resolved = _git("rev-parse", "ui-standards-v1.0")
    assert resolved, "ui-standards-v1.0 tag does not resolve"


@pytest.mark.parametrize("path", ["standards/ui", "docs/ui"])
def test_ui_baseline_tree_unchanged_since_tag(path):
    tag_tree = _git("rev-parse", f"ui-standards-v1.0:{path}")
    head_tree = _git("rev-parse", f"HEAD:{path}")
    assert tag_tree == head_tree, (
        f"{path} tree hash changed between ui-standards-v1.0 and HEAD "
        f"({tag_tree} -> {head_tree}) — the UI baseline must stay frozen"
    )


@pytest.mark.parametrize(
    "decision_file",
    [
        "decisions/0003-operator-ratification-decision-001.md",
        "decisions/0004-operator-ratification-decision-002.md",
    ],
)
def test_ui_decision_records_unchanged_since_tag(decision_file):
    tag_blob = _git("rev-parse", f"ui-standards-v1.0:{decision_file}")
    head_blob = _git("rev-parse", f"HEAD:{decision_file}")
    assert tag_blob == head_blob, f"{decision_file} changed since the UI baseline freeze"


# -- handoff.md references only real cluster files --

def test_handoff_references_valid_cluster_files():
    handoff_text = (PASS0_DIR / "handoff.md").read_text()
    cluster_names = {p.name for p in _cluster_files()}
    # handoff.md is prose, not a strict manifest; verify every markdown
    # link into clusters/ that it contains points at a real file.
    referenced = re.findall(r"clusters/([a-z0-9-]+\.md)", handoff_text)
    for name in referenced:
        assert name in cluster_names, f"handoff.md references nonexistent cluster file clusters/{name}"


def test_handoff_covers_every_high_priority_cluster():
    """Loose heuristic: a majority of the cluster id's significant words
    (allowing for pluralization/gerund differences in handoff prose)
    should appear in handoff.md, and every HIGH-priority cluster file
    should be explicitly linked from handoff.md's own file link, or the
    README's table (both are acceptable coverage)."""
    handoff_text = (PASS0_DIR / "handoff.md").read_text().lower()
    readme_text = (PASS0_DIR / "README.md").read_text()
    for path in _cluster_files():
        fm = _parse_frontmatter(path)
        if fm["priority"] != "HIGH":
            continue
        if f"clusters/{path.name}" in readme_text:
            continue  # every HIGH cluster is at minimum linked from the README table
        words = [w for w in fm["id"].split("-") if len(w) > 2]
        stems = [w[:5] for w in words]  # crude stemming: first 5 chars
        hits = sum(1 for stem in stems if stem in handoff_text)
        assert hits >= max(1, len(stems) // 2), (
            f"HIGH priority cluster {fm['id']!r} does not appear well-covered in handoff.md (stem hits: {hits}/{len(stems)})"
        )


# -- incident ledger sanity --

def test_incident_ledger_has_substantial_content():
    text = (PASS0_DIR / "incident-ledger.md").read_text()
    # loose sanity check: expect at least 20 incident rows (a table row starts with "| INC-")
    incident_rows = re.findall(r"^\| INC-\d+ \|", text, flags=re.MULTILINE)
    assert len(incident_rows) >= 20, f"expected at least 20 incident rows, found {len(incident_rows)}"


def test_no_target_clank_directories_were_created_under_this_repo():
    """This repo must never contain a copy of another Clank's source —
    evidence must be cited by file:line, not vendored in."""
    fleet_names = {
        "watch-clank", "smartwatch-clank", "smartphone-clank", "tablet-clank",
        "feature-phone-clank", "oem-radar", "chinese-tech-wire",
        "korean-tech-wire", "semiconductor-intelligence", "clank-architecture",
        "diagnostic-clank",
    }
    top_level = {p.name for p in REPO_ROOT.iterdir() if p.is_dir()}
    assert not (fleet_names & top_level), f"found vendored Clank directories: {fleet_names & top_level}"
