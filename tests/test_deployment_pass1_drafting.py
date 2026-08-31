"""Process and scope guards for Deployment Pass 1 proposals.

The assertions confirm what was drafted and its reviewability; PROPOSED text is
not thereby treated as ratified truth.
"""

import hashlib
import json
from pathlib import Path

REPO = Path(__file__).parent.parent
DEPLOY = REPO / "standards" / "deployment"
PASS0 = REPO / "docs" / "deployment" / "pass0"
PASS1 = REPO / "docs" / "deployment" / "pass1"
IDS = {"STD-DEPLOY-COM-001", "STD-DEPLOY-COM-002"}
PASS0_RAW_HASHES = {
    "README.md": "95e29cdb4f0ad02acb2636b6db5162f156029974a189afc64c81c7b070818d77",
    "adjudication.md": "3af86d4ca28fdc1574e55cf7f85733132a83c1d5e060ba064fd9c55221d375f8",
}


def _hash(path):
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def standards():
    return {path.stem: json.loads(path.read_text(encoding="utf-8")) for path in DEPLOY.glob("STD-DEPLOY-*.json")}


def test_exactly_two_version_one_proposals_exist():
    records = standards()
    assert set(records) == IDS
    assert all(record["status"] == "PROPOSED" and record["version"] == 1 for record in records.values())
    assert not list(DEPLOY.glob("STD-DEPLOY-*.md"))


def test_com001_is_applicable_and_implementation_neutral():
    record = standards()["STD-DEPLOY-COM-001"]
    text = record["trigger"] + record["requirement"] + " ".join(record["acceptance"])
    assert "target" in text.lower() and "materially running" in text.lower()
    assert "deploy-critical configuration" in text and "runtime wiring" in text
    assert "partial or in-progress" in text
    for forbidden_requirement in ("MUST use Git", "MUST use systemd", "MUST use Docker", "MUST use SSH"):
        assert forbidden_requirement not in text


def test_com002_is_persistent_compatibility_gate_not_tooling_rule():
    record = standards()["STD-DEPLOY-COM-002"]
    text = record["trigger"] + record["requirement"] + " ".join(record["forbidden"] + record["acceptance"])
    assert "persistent" in text.lower() and "stateless" in text.lower() and "N/A" in text
    assert "fail closed" in text.lower() and "normal work" in text.lower()
    assert "Data/Ontology" in record["notes"] and "Operations" in record["notes"]
    for prescription in ("MUST use Alembic", "MUST use SQL", "MUST migrate before deploy"):
        assert prescription not in text


def test_rehomes_and_rejections_remain_out_of_the_standard_set():
    text = (PASS1 / "README.md").read_text(encoding="utf-8")
    assert "ADR-0009" in text and "rehomed" in text
    assert "target-environment identity" in text
    assert "STD-DEPLOY-COM-003" not in text


def test_pass0_evidence_and_adjudication_are_unchanged():
    for relative, expected in PASS0_RAW_HASHES.items():
        assert _hash(PASS0 / relative) == expected, relative


def test_dossiers_and_index_disclose_proposal_status_and_reused_evidence():
    readme = (DEPLOY / "README.md").read_text(encoding="utf-8")
    assert "2 `PROPOSED`, 0 `RATIFIED`" in readme
    for dossier in PASS1.glob("dossier-*.md"):
        text = dossier.read_text(encoding="utf-8")
        assert "REUSED FROM OPERATIONS PASS 0" in text
        assert "0 newly discovered Deployment-specific incidents" in text
        assert "READY FOR REVIEW" in text
