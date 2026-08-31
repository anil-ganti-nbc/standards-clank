"""Structural guards for the Deployment Pass 0A evidence inventory.

These checks deliberately validate process and traceability only. They do not
turn an evidence cluster into a normative deployment requirement.
"""

import hashlib
import re
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).parent.parent
PASS0 = REPO / "docs" / "deployment" / "pass0"
CLUSTERS = PASS0 / "clusters"
FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
PRIORITIES = {"HIGH", "MEDIUM", "LOW"}
REQUIRED = {
    "cluster", "likely_domain", "priority", "evidence_strength",
}
BASELINE_HASHES = {
    "baselines/ui-standards-v1.0.json": "097902304f4a2387efbb29cfc3517cff0e3913810081eb4002dd3226a14e8a18",
    "baselines/ui-standards-v1.0-release-notes.md": "51f6c5322de241dce8b60fe5deea7107f9ebb179bd911b1b850f08cd35f264f1",
    "baselines/data-ontology-standards-v1.0.json": "eb6ec348bf777365c414d86f2f3b81f41d2bee5b685285b60d809dc5b2281836",
    "baselines/data-ontology-standards-v1.0-release-notes.md": "9c1a27376c1900241b64c8df4087c5643e3d3d5733ca879977425855d28c6d9e",
    "baselines/operations-standards-v1.0.json": "bb244481df42d48d4b36126d4d2cf5ee6bfef5d1cc52e388f197e106b72c4c5e",
    "baselines/operations-standards-v1.0-release-notes.md": "67bb7e90374a49cdfbcaaa8596287a2f16fb04712326ef644acde9d4df3668bf",
}


def cluster_files():
    return sorted(CLUSTERS.glob("*.md"))


def metadata(path):
    match = FRONTMATTER.match(path.read_text(encoding="utf-8"))
    assert match, f"missing YAML metadata: {path}"
    return yaml.safe_load(match.group(1))


@pytest.mark.parametrize("name", ["README.md", "evidence-log.md", "incident-ledger.md", "terminology-map.md", "handoff.md"])
def test_required_artifacts_exist(name):
    assert (PASS0 / name).is_file()


def test_clusters_have_required_metadata_and_unique_names():
    files = cluster_files()
    assert len(files) >= 1
    names = []
    for path in files:
        record = metadata(path)
        assert REQUIRED <= record.keys()
        assert record["priority"] in PRIORITIES
        assert path.name[:2].isdigit(), f"cluster lacks NN filename prefix: {path.name}"
        names.append(record["cluster"])
    assert len(names) == len(set(names))


def test_cluster_references_resolve_and_high_clusters_are_cited():
    ledger = (PASS0 / "incident-ledger.md").read_text(encoding="utf-8")
    readme = (PASS0 / "README.md").read_text(encoding="utf-8")
    ids = set(re.findall(r"\| (DEP-INC-\d+) \|", ledger))
    assert len(ids) == 10
    assert len(ids) == len(re.findall(r"\| DEP-INC-\d+ \|", ledger))
    for path in cluster_files():
        body = path.read_text(encoding="utf-8")
        for incident in re.findall(r"DEP-INC-\d+", body):
            assert incident in ids, f"{path.name} cites unknown {incident}"
        if metadata(path)["priority"] == "HIGH":
            assert f"clusters/{path.name}" in readme
            assert "DEP-INC-" in body


def test_reused_operations_incidents_and_lineage_are_explicit():
    ledger = (PASS0 / "incident-ledger.md").read_text(encoding="utf-8")
    assert ledger.count("REUSED FROM OPERATIONS PASS 0") == 10
    for name in ("INDEPENDENT INCIDENT", "INCIDENT INHERITANCE", "SHARED GOVERNANCE"):
        assert name in ledger


def test_governance_statuses_are_recorded_without_activation():
    evidence = (PASS0 / "evidence-log.md").read_text(encoding="utf-8")
    assert "Fleet Law 6, **ACTIVE**" in evidence
    assert "Law 9, **DEFERRED" in evidence
    assert "ADR-0009, **PROPOSED — REVIEWED DRAFT**" in evidence


def test_no_normative_deployment_artifacts_exist():
    assert not list(REPO.rglob("STD-DEPLOY-*.json"))
    assert not (REPO / "standards" / "deployment").exists()
    assert not list(PASS0.rglob("*.json"))


def test_no_target_clank_or_architecture_is_vendored_or_modified_here():
    forbidden = {"watch-clank", "oem-radar", "chinese-tech-wire", "korean-tech-wire", "feature-phone-clank", "smartphone-clank", "smartwatch-clank", "tablet-clank", "semiconductor-intelligence", "diagnostic-clank", "clank-architecture"}
    assert not (forbidden & {path.name for path in REPO.iterdir() if path.is_dir()})


def test_frozen_baseline_artifacts_remain_byte_identical():
    for relative, expected in BASELINE_HASHES.items():
        actual = hashlib.sha256((REPO / relative).read_bytes()).hexdigest()
        assert actual == expected, f"frozen baseline changed: {relative}"


def test_handoff_forbids_fleet_recrawl():
    handoff = (PASS0 / "handoff.md").read_text(encoding="utf-8")
    assert "DO NOT RECRAWL THE FLEET" in handoff
