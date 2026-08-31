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
    "baselines/ui-standards-v1.0.json": "94eaaa1486bf18ed1b072c5f82ffa3d71d8a8c81bab6269dbdea567d61f3e0f9",
    "baselines/ui-standards-v1.0-release-notes.md": "51f6c5322de241dce8b60fe5deea7107f9ebb179bd911b1b850f08cd35f264f1",
    "baselines/data-ontology-standards-v1.0.json": "eb6ec348bf777365c414d86f2f3b81f41d2bee5b685285b60d809dc5b2281836",
    "baselines/data-ontology-standards-v1.0-release-notes.md": "9c1a27376c1900241b64c8df4087c5643e3d3d5733ca879977425855d28c6d9e",
    "baselines/operations-standards-v1.0.json": "bb244481df42d48d4b36126d4d2cf5ee6bfef5d1cc52e388f197e106b72c4c5e",
    "baselines/operations-standards-v1.0-release-notes.md": "67bb7e90374a49cdfbcaaa8596287a2f16fb04712326ef644acde9d4df3668bf",
}

PASS0A_RAW_HASHES = {
    "README.md": "95e29cdb4f0ad02acb2636b6db5162f156029974a189afc64c81c7b070818d77",
    "clusters/01-materialisation-truth.md": "0a533669639e7606a283946e4aa1eb50f9632bb3575345c5a49fe76f79a065c6",
    "clusters/02-running-revision-identity.md": "bbfffc58cf9ebeb022bcfa567e9baa518e83af2583dfeb5a6eb614f3e8165f5e",
    "clusters/03-schema-code-compatibility.md": "61cf5283e5233a0cbb39b2b8dc875b52e0be0173100c735f0de30b6459d01092",
    "clusters/04-partial-deployment-wiring.md": "be78e64300204fa3acc6f6ad4d9568c69b3d485238e4fad0330562b013f6237d",
    "clusters/05-rollback-recovery-and-mutation.md": "d68f3466cd5bbc2d6a42ccce9e8ccc1c85fbfbcd4400a17140e5a47e889e4ef3",
    "clusters/06-target-environment-identity.md": "94344a17a7be6d05c06b148a1c05522fc2c678d0efa047f0c3afe15e442d2d5b",
    "evidence-log.md": "5ea28e1f4cd93b7710149f9f70058e0887b1c01aa241466630f02f6daddcb550",
    "handoff.md": "6f13e6494a1abeec1a403d4a63163f6b85abd550d287e3ac07e08cd9bbcbb587",
    "incident-ledger.md": "ae9003405a69980ed9774d643d62aedcda532cfb810bdda4ea05d4b7016335d6",
    "terminology-map.md": "6de6b70e85cdf9afe98ef0e6fe0e06f71c33cb837300c25df97035e5f5bed881",
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


def _canonical_content_hash(path):
    """Hash committed text independently of Windows LF-to-CRLF checkout conversion."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


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


def test_pass0b_created_no_standard_files_and_no_ratification():
    """Pass 1 later drafts exactly two proposals; Pass 0B remains unchanged."""
    assert not list(PASS0.rglob("*.json"))


def test_frozen_baseline_artifacts_remain_byte_identical():
    for relative, expected in BASELINE_HASHES.items():
        actual = _canonical_content_hash(REPO / relative)
        assert actual == expected, f"frozen baseline changed: {relative}"


def test_pass0a_raw_evidence_unchanged():
    for relative, expected in PASS0A_RAW_HASHES.items():
        actual = _canonical_content_hash(PASS0 / relative)
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
