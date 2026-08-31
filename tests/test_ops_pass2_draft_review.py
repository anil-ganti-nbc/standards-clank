"""Operations Pass 2 (adversarial draft review) process guards.

The review must: give all four candidates exactly one verdict (three
APPROVE FOR RATIFICATION SURVEY, OPS-D DRAFT AS STD-OPS-COM-004), keep
every OPS standard PROPOSED (none ratified), create no fourth OPS
standard in this pass, and preserve the full Ops 0/1/1.5 evidence chain,
the frozen UI/DATA baselines, and the three PROPOSED OPS drafts
byte-for-byte (CRLF-normalized content hashes — no git subprocesses,
which are unreliable on this host).
"""

import hashlib
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REVIEW = REPO / "docs" / "operations" / "pass2" / "review.md"
OPS_DIR = REPO / "standards" / "operations"
RESOLUTION = REPO / "docs" / "operations" / "pass1" / "ops-d-resolution.md"

EXPECTED_OPS = {
    "STD-OPS-COM-001": ("PROPOSED", 1),
    "STD-OPS-COM-002": ("PROPOSED", 1),
    "STD-OPS-COM-003": ("PROPOSED", 1),
}

VERDICT_SECTIONS = [
    ("STD-OPS-COM-001", "APPROVE FOR RATIFICATION SURVEY"),
    ("STD-OPS-COM-002", "APPROVE FOR RATIFICATION SURVEY"),
    ("STD-OPS-COM-003", "APPROVE FOR RATIFICATION SURVEY"),
    ("OPS-D", "DRAFT AS STD-OPS-COM-004"),
]

# CRLF-normalized content hashes pinning the complete Operations evidence
# chain, the three PROPOSED OPS drafts, and both frozen baseline manifests
# exactly as verified during this review pass. Any post-review modification
# of any of these files fails these guards with a clear message.
FROZEN_HASHES = {
    "docs/operations/pass0/handoff.md":
        "6ed6a39a3205a25eeff07d1cc03f9fd38a7f9952ac33aeced9d04294f0afbb5d",
    "docs/operations/pass0/evidence-log.md":
        "8c73480a74a3ae39586ef6a4c0e59336a0be3ea6084314bc13977dab9eb07a35",
    "docs/operations/pass0/incident-ledger.md":
        "23110c1ed8c9394a19e04e5fc09629be58e2a180f30a96225a5b39d754539893",
    "docs/operations/pass0/clusters/pid-namespace-unsafe-stale-lock-reclaim.md":
        "88dafccc387b55638a6a47a0144adf6463f187b9a01c312884c49f55c57af9f2",
    "docs/operations/pass0/adjudication.md":
        "85365789e7a6358ba91be4db99ff0cd6d12a734717da56f27cc442d8fa022f40",
    "docs/operations/pass0/candidates/holds-rehomes-defers.md":
        "9472379209dc72f4be21219e1480cc2f8f699af8b2474fdad15e49591b3e92bd",
    "docs/operations/pass0/candidates/ops-a-execution-materialization-truth.md":
        "5dfe36833e60961a4059e9e66c254edfcc5c4283abf4a74074ed16d001705e3e",
    "docs/operations/pass0/candidates/ops-b-health-honesty-two-axis.md":
        "a9f8b02c0421b7be65cd1660950f5edaeb00f56464bfe76d1b90a3efdcfe5887",
    "docs/operations/pass0/candidates/ops-c-promotion-soak-evidence-integrity.md":
        "39d168374f5dca713152e22fbb015b599abeb11fd051f35ca3d39ba0490d469c",
    "docs/operations/pass0/candidates/ops-d-exclusivity-marker-soundness.md":
        "f9c07d2a2b7decda654f8c5243247863cfe9933aa9344ddbc289d9849df67454",
    "docs/operations/pass1/README.md":
        "f4eef42078354b98f044fb0ef44588871942471f9ebec29da960cabdd14a3080",
    "docs/operations/pass1/dossier-ops-a-execution-materialization-truth.md":
        "29ab711a1b8c864630ca492f0cef956187de03a09d13f6d3d5b5f02ac1b89d10",
    "docs/operations/pass1/dossier-ops-b-health-honesty-two-axis.md":
        "54aaefc9a10dd7a1085f8f3eb50d3c73d51e7bb6ea4389e57c55849f19d07b91",
    "docs/operations/pass1/dossier-ops-c-promotion-soak-evidence-integrity.md":
        "f6789552b5804d55374efe3981aeb34392710568bfbf34d4e8ac1d17c1476be8",
    "docs/operations/pass1/ops-d-resolution.md":
        "661b3fdc7c60365b2c7450f51792ad6514b05f2d5c46c8360b54688002130dc1",
    "docs/operations/pass2/review.md":
        "a689e9b13e574499fae64273949b9e60a655b36a964fbfbb84b7f53e38d646ac",
    "baselines/ui-standards-v1.0.json":
        "94eaaa1486bf18ed1b072c5f82ffa3d71d8a8c81bab6269dbdea567d61f3e0f9",
    "baselines/data-ontology-standards-v1.0.json":
        "eb6ec348bf777365c414d86f2f3b81f41d2bee5b685285b60d809dc5b2281836",
    "standards/operations/STD-OPS-COM-001.json":
        "8c1d09d0353e47f9389d9938436eefab0b313cd695a9b0f089799ce5667123aa",
    "standards/operations/STD-OPS-COM-002.json":
        "e256d73affab269e943bdd07d10f0248928a9e924033609967c0daa9931da9b6",
    "standards/operations/STD-OPS-COM-003.json":
        "5cfb26d4580645965e62ab0504485a0765ba460a09310d997f7a1919c9d24fab",
}


def _review() -> str:
    """Whitespace-normalized review text so markdown line wraps cannot
    break substring assertions."""
    return re.sub(r"\s+", " ", (REVIEW).read_text(encoding="utf-8"))


def test_review_dossier_exists():
    assert REVIEW.is_file()
    assert len(_review()) > 4000


def test_all_four_candidates_reviewed_with_exactly_one_verdict():
    text = _review()
    section_keys = {
        "STD-OPS-COM-001": "OPS-A",
        "STD-OPS-COM-002": "OPS-B",
        "STD-OPS-COM-003": "OPS-C",
        "OPS-D": "OPS-D",
    }
    for sid, verdict in VERDICT_SECTIONS:
        key = section_keys[sid]
        assert f"## {key}" in text, f"{sid} review section missing"
        sections = [
            block for block in text.split("## ")
            if block.startswith(key)
        ]
        assert sections, f"{sid} review section missing"
        verdicts = [
            v for v in (
                "APPROVE FOR RATIFICATION SURVEY", "REVISE", "HOLD",
                "DRAFT AS STD-OPS-COM-004", "REHOME", "REJECT",
            )
            if v in sections[0]
        ]
        assert len(verdicts) == 1, f"{sid}: verdicts found {verdicts}"
        assert verdicts[0] == verdict


def test_review_covers_all_required_adversarial_dimensions():
    text = _review()
    for marker in (
        "Trigger assessment", "Acceptance-criteria assessment",
        "Implementation-neutrality assessment", "Overlap assessment",
        "Strongest counterexample", "Strongest weakness",
        "Fleet Law / ADR reconciliation", "Domain-boundary confirmation",
        "Ratification-readiness summary",
    ):
        assert marker in text, f"review missing section/marker: {marker!r}"


def test_ops_d_drafting_constraints_specified_without_drafting():
    text = _review()
    assert "DRAFT AS STD-OPS-COM-004" in text
    for constraint in (
        "Proposed title", "Semantic invariant", "Trigger/applicability",
        "Minimum acceptance concepts", "Minimum forbidden concepts",
        "Implementation freedoms", "Fleet Law relationship",
        "Strongest counterexample survived",
    ):
        assert constraint in text, f"OPS-D drafting constraint missing: {constraint!r}"


def test_no_ops_standard_is_ratified():
    for path in sorted(OPS_DIR.glob("STD-OPS-*.json")):
        d = json.loads(path.read_text())
        assert d["status"] == "PROPOSED", f"{path.name}: review must not ratify"


def test_exactly_three_ops_standards_and_no_fourth_created():
    files = sorted(OPS_DIR.glob("STD-OPS-*.json"))
    assert {p.stem for p in files} == set(EXPECTED_OPS)
    assert len(files) == 3
    assert not list(REPO.rglob("STD-OPS-COM-004*")), (
        "OPS-D must not be drafted in this pass — that is Pass 2.5's task"
    )


def test_pass15_history_preserved():
    resolution = REPO / "docs" / "operations" / "pass1" / "ops-d-resolution.md"
    text = resolution.read_text(encoding="utf-8")
    assert "ADVANCE AS OPS-D" in text
    card = REPO / "docs" / "operations" / "pass0" / "candidates" / "ops-d-exclusivity-marker-soundness.md"
    assert card.is_file()


def test_evidence_chain_and_frozen_baselines_unchanged():
    for rel, expected in FROZEN_HASHES.items():
        actual = _normalized_sha256_file(REPO / rel)
        assert actual == expected, (
            f"{rel} diverged from its verified content — modified after this review pass"
        )


def _normalized_sha256_file(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def test_rehomed_and_deferred_concerns_stay_out_of_scope():
    text = _review()
    assert "future DEPLOYMENT domain" in text
    assert "future DELIVERY domain" in text
    assert "DEFER to ADR-0009" in text
    summary = text.split("Domain-boundary confirmation")[1].split("Ratification-readiness")[0]
    for marker in ("DEPLOYMENT", "DELIVERY", "ADR-0009", "HOLD"):
        assert marker in summary
