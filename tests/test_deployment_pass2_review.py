"""Process guards for the Deployment Pass 2 adversarial review.

Review approval is not ratification and does not make proposed text normative.
"""

import hashlib
import json
from pathlib import Path

REPO = Path(__file__).parent.parent
PASS0 = REPO / "docs" / "deployment" / "pass0"
REVIEW = REPO / "docs" / "deployment" / "pass2" / "review.md"
DEPLOY = REPO / "standards" / "deployment"
RAW_HASHES = {
    "README.md": "95e29cdb4f0ad02acb2636b6db5162f156029974a189afc64c81c7b070818d77",
    "adjudication.md": "3af86d4ca28fdc1574e55cf7f85733132a83c1d5e060ba064fd9c55221d375f8",
}


def _hash(path):
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def test_review_has_exactly_one_approval_verdict_per_draft():
    text = REVIEW.read_text(encoding="utf-8")
    for standard in ("STD-DEPLOY-COM-001", "STD-DEPLOY-COM-002"):
        assert f"| {standard} | **APPROVE FOR RATIFICATION SURVEY** | None |" in text
    assert text.count("| STD-DEPLOY-COM-") == 2


def test_review_preserves_proposal_state_and_exact_standard_set():
    files = sorted(DEPLOY.glob("STD-DEPLOY-*.json"))
    assert [path.stem for path in files] == ["STD-DEPLOY-COM-001", "STD-DEPLOY-COM-002"]
    assert all(json.loads(path.read_text(encoding="utf-8"))["status"] == "PROPOSED" for path in files)


def test_review_preserves_evidence_adjudication_and_governance_boundaries():
    for relative, expected in RAW_HASHES.items():
        assert _hash(PASS0 / relative) == expected
    text = REVIEW.read_text(encoding="utf-8")
    assert "10 Deployment Pass 0 incidents were" in text
    assert "**0**" in text and "ADR-0009" in text
    assert "PROPOSED — REVIEWED DRAFT" in text


def test_normalized_hash_guard_remains_strict_against_content_changes():
    sample = b"same\r\ncontent\r\n"
    assert hashlib.sha256(sample.replace(b"\r\n", b"\n")).hexdigest() == hashlib.sha256(b"same\ncontent\n").hexdigest()
    assert _hash(PASS0 / "README.md") != hashlib.sha256(b"changed\n").hexdigest()
