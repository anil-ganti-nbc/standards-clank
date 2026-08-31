"""Process guards for the Deployment Pass 3 ratification survey.

This pass is advisory only: recommendations are not ratification, statuses
remain PROPOSED, and no normative wording was changed.
"""

import hashlib
import json
from pathlib import Path

REPO = Path(__file__).parent.parent
DEPLOY = REPO / "standards" / "deployment"
PASS0 = REPO / "docs" / "deployment" / "pass0"
PASS1 = REPO / "docs" / "deployment" / "pass1"
PASS2 = REPO / "docs" / "deployment" / "pass2"
PASS3 = REPO / "docs" / "deployment" / "pass3"
DECISIONS = REPO / "decisions"
SURVEY = PASS3 / "ratification-survey.md"

STD_HASHES = {
    "STD-DEPLOY-COM-001.json": "6f07d90cf4ba8046dbf2fa50e2b6b35f2313985dc3c1b10aa48f7aaca5df32b8",
    "STD-DEPLOY-COM-002.json": "f7f52bd05eb19f8ecce2d97467b5ed2ee38ea418fb2d7dc43599c16f0bf78ce7",
}
PASS1_HASHES = {
    "README.md": "a78bca4a3e6a82f2592e1f98c8b3a90f4c3238ae6888cf014ab36fb40597d29b",
    "dossier-dep-a-materialisation-truth.md": "e34aa93d852ac39d61662ed198ed056b524bef438b1f4f4aaf70a46a387dd493",
    "dossier-dep-d-schema-code-compatibility.md": "17b9e3f1d8a050eadba139d135bbb61b22a9e3591bedd97cdda1af57021bb0c9",
}
PASS2_HASHES = {
    "review.md": "33d3701daedc6dd99a45bf10e53103d3c560907eeb9f173373685d729717cb0d",
}

VALID_RECOMMENDATIONS = {"RATIFY AS WRITTEN", "REVISE BEFORE RATIFICATION", "HOLD", "REJECT"}


def _hash(path):
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def survey_text():
    return SURVEY.read_text(encoding="utf-8")


def test_exactly_two_deployment_standards_surveyed():
    records = {path.stem: json.loads(path.read_text(encoding="utf-8")) for path in DEPLOY.glob("STD-DEPLOY-*.json")}
    assert set(records) == {"STD-DEPLOY-COM-001", "STD-DEPLOY-COM-002"}
    text = survey_text()
    assert text.count("STD-DEPLOY-COM-") >= 2
    assert "STD-DEPLOY-COM-003" not in text


def test_exactly_one_recommendation_per_standard_from_valid_set():
    text = survey_text()
    table = text.split("## Recommendations (advisory — one per standard)")[1]
    for standard in ("STD-DEPLOY-COM-001", "STD-DEPLOY-COM-002"):
        rows = [line for line in table.splitlines() if line.startswith(f"| {standard} ")]
        assert len(rows) == 1, standard
        recommendation = rows[0].split("|")[2].strip()
        assert recommendation in VALID_RECOMMENDATIONS, recommendation


def test_both_standards_remain_proposed_v1():
    for name in STD_HASHES:
        record = json.loads((DEPLOY / name).read_text(encoding="utf-8"))
        assert record["status"] == "PROPOSED", name
        assert record["version"] == 1, name


def test_normative_wording_unchanged():
    for name, expected in STD_HASHES.items():
        assert _hash(DEPLOY / name) == expected, name


def test_decision_records_exist_pending_and_forbid_self_ratification():
    records = {
        "0018": DECISIONS / "0018-deploy-com-001-decision.md",
        "0019": DECISIONS / "0019-deploy-com-002-decision.md",
    }
    for number, path in records.items():
        text = path.read_text(encoding="utf-8")
        assert path.is_file(), number
        assert "Status: PENDING" in text, number
        assert "**PENDING**" in text, number
        assert "0002-no-agent-self-ratification.md" in text, number
        assert "RATIFIED" not in text.split("## Operator decision")[0].split("## Recommendation")[1], number
    assert not list(DECISIONS.glob("0020-*")), "no additional decision records expected"


def test_no_self_ratification_of_deployment_standards():
    for name in STD_HASHES:
        record = json.loads((DEPLOY / name).read_text(encoding="utf-8"))
        assert record["status"] == "PROPOSED"
        assert "RATIFIED" != record["status"]
    survey = survey_text()
    assert "No standard was ratified and no" in survey
    assert "decisions/0002-no-agent-self-ratification.md" in survey


def test_pass0_evidence_pass0b_adjudication_and_pass2_review_unchanged():
    assert _hash(PASS0 / "adjudication.md") == "3af86d4ca28fdc1574e55cf7f85733132a83c1d5e060ba064fd9c55221d375f8"
    assert _hash(PASS0 / "README.md") == "95e29cdb4f0ad02acb2636b6db5162f156029974a189afc64c81c7b070818d77"
    for relative, expected in PASS1_HASHES.items():
        assert _hash(PASS1 / relative) == expected, relative
    for relative, expected in PASS2_HASHES.items():
        assert _hash(PASS2 / relative) == expected, relative


def test_pass2_verdicts_are_approve_for_ratification_survey():
    review = (PASS2 / "review.md").read_text(encoding="utf-8")
    for standard in ("STD-DEPLOY-COM-001", "STD-DEPLOY-COM-002"):
        assert f"| {standard} | **APPROVE FOR RATIFICATION SURVEY** | None |" in review


def test_evidence_reuse_caveat_remains_explicit():
    text = survey_text()
    assert "reused from Operations Pass 0" in text
    assert "**0**" in text
    assert "SUFFICIENT" in text
    for dossier in PASS1.glob("dossier-*.md"):
        assert "REUSED FROM OPERATIONS PASS 0" in dossier.read_text(encoding="utf-8")


def test_governance_statuses_recorded_without_activation():
    text = survey_text()
    assert "Fleet Law 5 | ACTIVE" in text
    assert "Fleet Law 6 | ACTIVE" in text
    assert "Law 9 | DEFERRED" in text
    assert "PROPOSED – REVIEWED DRAFT (not ACTIVE)" in text
    assert "not activated" in text or "neither activated" in text


def test_frozen_baselines_and_tags_untouched_and_no_outside_modification():
    import subprocess

    for tag in ("ui-standards-v1.0", "data-ontology-standards-v1.0", "operations-standards-v1.0"):
        try:
            sha = subprocess.run(
                ["git", "rev-parse", tag], cwd=REPO, capture_output=True, text=True,
                check=True, stdin=subprocess.DEVNULL,
            ).stdout.strip()
        except (OSError, subprocess.CalledProcessError) as exc:
            raise AssertionError(f"frozen tag unreadable: {tag}: {exc}")
        assert len(sha) == 40, tag
    assert not (REPO / "clank-architecture").exists()
    survey = survey_text()
    assert "no\n`clank-architecture` file was modified" in survey
    assert "No target Clank repository was read." in survey
