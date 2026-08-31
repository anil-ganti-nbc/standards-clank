"""Operations Pass 1.5 (OPS-D scope-omission resolution) process guards.

The resolution must: give OPS-D an explicit final Pass-1 disposition
(ADVANCE AS OPS-D) with a full candidate card, leave Pass 0B history and
the Pass 0A evidence intact, leave the three existing PROPOSED OPS
standards unchanged, create no fourth standard, and leave the frozen
baselines untouched.
"""

import hashlib
import json
import re
import subprocess
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OPS_DIR = REPO / "standards" / "operations"
PASS0 = REPO / "docs" / "operations" / "pass0"
PASS1 = REPO / "docs" / "operations" / "pass1"
RESOLUTION = PASS1 / "ops-d-resolution.md"
CARD = PASS0 / "candidates" / "ops-d-exclusivity-marker-soundness.md"

EXPECTED_OPS = {
    "STD-OPS-COM-001": ("PROPOSED", 1),
    "STD-OPS-COM-002": ("PROPOSED", 1),
    "STD-OPS-COM-003": ("PROPOSED", 1),
}

DECISION_RECORDS = {
    "0010-data-com-001-decision.md": "STD-DATA-COM-001",
    "0011-data-com-002-decision.md": "STD-DATA-COM-002",
    "0012-data-com-003-decision.md": "STD-DATA-COM-003",
    "0013-data-com-004-decision.md": "STD-DATA-COM-004",
}

# (introduction commit, path, sha256 of CRLF-normalized content at that
# commit). Hash comparison is used instead of git subprocesses (git-spawn
# is unreliable on this host).
FROZEN_HASHES = {
    "21f0885/docs/operations/pass0/handoff.md":
        "6ed6a39a3205a25eeff07d1cc03f9fd38a7f9952ac33aeced9d04294f0afbb5d",
    "21f0885/docs/operations/pass0/evidence-log.md":
        "8c73480a74a3ae39586ef6a4c0e59336a0be3ea6084314bc13977dab9eb07a35",
    "21f0885/docs/operations/pass0/incident-ledger.md":
        "23110c1ed8c9394a19e04e5fc09629be58e2a180f30a96225a5b39d754539893",
    "21f0885/docs/operations/pass0/clusters/pid-namespace-unsafe-stale-lock-reclaim.md":
        "88dafccc387b55638a6a47a0144adf6463f187b9a01c312884c49f55c57af9f2",
    "21f0885/docs/data-ontology/pass0/adjudication.md":
        "2143093f6524c4fa8dd1796f77dd44d5568d373d7368f403f02fd2cc6ab16246",
    # holds-and-rejects.md pinned at its post-pointer state: the additive
    # disposition pointer was itself commissioned (cd4384b), so the
    # current content — pointer + all seven original cards — is the
    # protected baseline.
    "cd4384b/docs/data-ontology/pass0/candidates/holds-and-rejects.md":
        "1b13f64597953576d26aedb0653a2d77f8b19e6db387b167fba2475c66630e42",
    "d113207/baselines/ui-standards-v1.0.json":
        "94eaaa1486bf18ed1b072c5f82ffa3d71d8a8c81bab6269dbdea567d61f3e0f9",
    "4407654/baselines/data-ontology-standards-v1.0.json":
        "eb6ec348bf777365c414d86f2f3b81f41d2bee5b685285b60d809dc5b2281836",
}


def _normalized_sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def _normalized_sha256_file(path: Path) -> str:
    return _normalized_sha256_bytes(path.read_bytes())


def test_resolution_document_exists_with_disposition_a():
    text = RESOLUTION.read_text(encoding="utf-8")
    assert "ADVANCE AS OPS-D" in text
    assert "Pass 0B" in text and "Pass 1" in text and "Pass 1.5" in text
    assert "omission" in text.lower()
    assert "STD-OPS-COM-004" in text  # explicitly records that no draft was created


def test_opsd_candidate_card_exists_with_counterexample_and_fleet_laws():
    text = CARD.read_text(encoding="utf-8")
    assert "Exclusivity-marker soundness" in text
    assert text.count("**Recommendation:") == 1
    assert "**Recommendation: ADVANCE AS OPS-D**" in text
    assert "Counterexample test" in text
    assert "Fleet Law 5" in text and "Fleet Law 7" in text
    assert "DB session" in text  # implementation freedom demonstrated


def test_opsd_card_invariant_is_mechanism_neutral():
    """The invariant must constrain validity semantics (liveness/ownership
    provable by the granting authority), never mandate lockfiles, PIDs,
    namespaces, or a particular locking system."""
    text = CARD.read_text(encoding="utf-8")
    assert "structurally observable by the authority that grants it" in text
    assert "context-ambiguous identifier" in text


def test_adjudication_correction_note_is_additive():
    """Pass 0B's original cluster-2 verdict text must remain, with the
    Pass 1.5 resolution note appended alongside it."""
    text = (PASS0 / "adjudication.md").read_text(encoding="utf-8")
    assert "OPS-D Lock reclaim soundness" in text  # original table verdict
    assert (
        "PID-namespace-unsafe stale-lock reclaim — KEEP DISTINCT, ADVANCE (OPS-D)"
        in text
    )
    assert "Pass 1.5 resolution (2026-08-31)" in text
    assert "candidates/ops-d-exclusivity-marker-soundness.md" in text


def test_exactly_three_ops_standards_and_no_fourth():
    files = sorted(OPS_DIR.glob("STD-OPS-*.json"))
    assert {p.stem for p in files} == set(EXPECTED_OPS)
    for path in files:
        d = json.loads(path.read_text())
        assert (d["status"], d["version"]) == EXPECTED_OPS[d["id"]]
        assert "exclusivity" not in d["title"].lower(), (
            "no fourth OPS standard (OPS-D draft) may exist unless separately commissioned"
        )


def test_frozen_artifacts_unchanged():
    for key, expected in FROZEN_HASHES.items():
        base, rel = key.split("/", 1)
        path = REPO / rel
        assert path.is_file(), f"{rel} missing"
        digest = _normalized_sha256_file(path)
        assert digest == expected, (
            f"{rel} no longer matches its {base} content — modified after introduction"
        )


def test_held_pass0b_cards_untouched():
    holds = PASS0 / "candidates" / "holds-rehomes-defers.md"
    text = holds.read_text(encoding="utf-8")
    assert "Recommendation: HOLD" in text
    assert "Recommendation: ADVANCE" not in text
    assert "DEFER BEYOND V1" not in text  # holds-and-rejects predates the disposition doc
