"""Process guards for the Deployment Pass 0B adjudication.

These checks validate process and traceability only. The candidate cards are
NOT normative truth; no standard was drafted, ratified, or activated here.
"""

import hashlib
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).parent.parent
PASS0 = REPO / "docs" / "deployment" / "pass0"
ADJUDICATION = PASS0 / "adjudication.md"
CANDIDATES = PASS0 / "candidates"

BASELINE_HASHES = {
    "baselines/ui-standards-v1.0.json": "097902304f4a2387efbb29cfc3517cff0e3913810081eb4002dd3226a14e8a18",
    "baselines/ui-standards-v1.0-release-notes.md": "51f6c5322de241dce8b60fe5deea7107f9ebb179bd911b1b850f08cd35f264f1",
    "baselines/data-ontology-standards-v1.0.json": "eb6ec348bf777365c414d86f2f3b81f41d2bee5b685285b60d809dc5b2281836",
    "baselines/data-ontology-standards-v1.0-release-notes.md": "9c1a27376c1900241b64c8df4087c5643e3d3d5733ca879977425855d28c6d9e",
    "baselines/operations-standards-v1.0.json": "bb244481df42d48d4b36126d4d2cf5ee6bfef5d1cc52e388f197e106b72c4c5e",
    "baselines/operations-standards-v1.0-release-notes.md": "67bb7e90374a49cdfbcaaa8596287a2f16fb04712326ef644acde9d4df3668bf",
}

PASS0A_RAW_HASHES = {
    "README.md": "10d19de743ef9f6d03f037c01e59f8ebff09f793de123900857da545efbf6379",
    "clusters/01-materialisation-truth.md": "a6fb2f8c353156bb3afb4c0cb8deb3d757d827d0f3baca9c41354364357249ba",
    "clusters/02-running-revision-identity.md": "973c90e69b15dc7ed9ed4dccb43b7ab341781a9759e27fc2863bf209ad9cadd1",
    "clusters/03-schema-code-compatibility.md": "06fb55f3284116627500e4aca19fab8333b9d29e5b5ef1b7d0875f08a02d45fc",
    "clusters/04-partial-deployment-wiring.md": "230b97caa3ab1516f13aa8a164e2e025d3bd1bdac49000482f7e1c1e7b8c04bc",
    "clusters/05-rollback-recovery-and-mutation.md": "a3f301b62eb9fd02ddb0e5ff52c68c820829bed077e470dd559a68dd52465c6f",
    "clusters/06-target-environment-identity.md": "b9788f3576e5dbb6ec82fededddde49afdbb736c15fe513b2b15bdd091eaec94",
    "evidence-log.md": "588b0f68f7af071e525fc3851d01b83f1643a4af9232bb95530318551d422d60",
    "handoff.md": "413ce857341ed10691cbe08a728b53304967b8653fc1b5365313a6fe5f2651f6",
    "incident-ledger.md": "808023ddff55f56a0a62ff004509619d86fcae9c1468f0b02b4a4465b99a81ec",
    "terminology-map.md": "5d2f7afe95865b342aa90eebb952464ea8f84c665073168b8c30898fd9d9b801",
}

CLUSTER_NAMES = [
    "01 materialisation-truth",
    "02 running-revision-identity",
    "03 schema-code-compatibility",
    "04 partial-deployment-wiring",
    "05 rollback-recovery-and-mutation",
    "06 target-environment-identity",
]

DISPOSITIONS = {
    "KEEP DISTINCT", "MERGE WITH 01", "SPLIT", "REHOME DOMAIN", "REJECT",
}
RECOMMENDATIONS = {"ADVANCE", "HOLD", "REHOME", "REJECT"}

FROZEN_TAGS = {
    "ui-standards-v1.0": "71e7ac427fd3c6dc11eea87d3eab528cd72ffd5f",
    "data-ontology-standards-v1.0": "f2f8a7626592f5f007377b1e0b04d2feb78d5cc2",
    "operations-standards-v1.0": "b36239d4b07b578822d62c8681046fa108e32d5c",
}


@pytest.fixture(scope="module")
def adjudication_text():
    assert ADJUDICATION.is_file(), "adjudication.md missing"
    return ADJUDICATION.read_text(encoding="utf-8")


def test_all_six_clusters_have_exactly_one_disposition(adjudication_text):
    table = adjudication_text.split("## 1. Summary table")[1].split("## 2.")[0]
    for name in CLUSTER_NAMES:
        rows = [line for line in table.splitlines() if line.startswith(f"| {name} ")]
        assert len(rows) == 1, f"cluster '{name}' must appear exactly once"
        cells = [cell.strip() for cell in rows[0].split("|")[1:-1]]
        disposition = cells[1].split(" (")[0]
        recommendation = cells[2].split(" (")[0]
        assert disposition in DISPOSITIONS, f"cluster '{name}' disposition ambiguous: {cells[1]}"
        assert recommendation in RECOMMENDATIONS, f"cluster '{name}' recommendation ambiguous: {cells[2]}"


def test_advance_candidates_exist_as_cards_with_required_sections():
    cards = sorted(CANDIDATES.glob("*.md"))
    assert len(cards) == 2, "expected exactly two ADVANCE candidate cards"
    for card in cards:
        text = card.read_text(encoding="utf-8")
        assert "## Strongest counterexample" in text, card.name
        assert "## Why it survives" in text, card.name
        assert "## Existing-standard distinctness proof" in text, card.name
        assert "## Fleet Law / ADR relationship" in text, card.name
        assert "## Recommendation" in text, card.name


def test_reused_incidents_not_claimed_as_new_evidence(adjudication_text):
    assert "Newly discovered Deployment-specific incidents: **0.**" in adjudication_text
    assert "Reused from Operations Pass 0: **10 (all).**" in adjudication_text
    for card in CANDIDATES.glob("*.md"):
        assert "Newly discovered deployment-specific incidents: 0." in card.read_text(encoding="utf-8"), card.name


def test_adr_0009_status_correctly_recorded_not_active(adjudication_text):
    assert "PROPOSED — REVIEWED DRAFT" in adjudication_text
    assert "NOT ACTIVE" in adjudication_text
    assert "**ACTIVE**" not in adjudication_text.split("ADR-0009")[1].split("\n")[0]


def test_no_std_deploy_files_and_no_ratified_deployment_standards():
    assert not list(REPO.rglob("STD-DEPLOY-*.json"))
    assert not list(REPO.rglob("STD-DEPLOY-*.md"))
    assert not (REPO / "standards" / "deployment").exists()
    assert not list(PASS0.rglob("*.json"))


def test_frozen_baseline_artifacts_remain_byte_identical():
    for relative, expected in BASELINE_HASHES.items():
        actual = hashlib.sha256((REPO / relative).read_bytes()).hexdigest()
        assert actual == expected, f"frozen baseline changed: {relative}"


def test_pass0a_raw_evidence_unchanged():
    for relative, expected in PASS0A_RAW_HASHES.items():
        actual = hashlib.sha256((PASS0 / relative).read_bytes()).hexdigest()
        assert actual == expected, f"Pass 0A raw evidence changed: {relative}"


def test_frozen_tags_untouched():
    for tag, expected in FROZEN_TAGS.items():
        try:
            actual = subprocess.run(
                ["git", "rev-parse", tag], cwd=REPO, capture_output=True, text=True, check=True
            ).stdout.strip()
        except (OSError, subprocess.CalledProcessError) as exc:
            pytest.skip(f"git unavailable or tag unreadable: {exc}")
        assert actual == expected, f"frozen tag moved: {tag}"


def test_adjudication_claims_no_target_repo_modification(adjudication_text):
    assert "no target Clank and no clank-architecture" in adjudication_text
