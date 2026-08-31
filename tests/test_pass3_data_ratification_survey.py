"""Data/Ontology Pass 3 (ratification survey) process guards.

The survey must leave all four DATA standards PROPOSED at their exact
versions, persist four awaiting-operator decision records that do not
self-ratify, and leave the frozen UI baseline, the Pass 0/1/2 evidence,
the Pass 0B adjudication, and the HOLD/REJECT candidates untouched. No
new DATA candidate standard may appear, and no recommendation is encoded
as normative truth.
"""

import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATA_DIR = REPO / "standards" / "data-ontology"
PASS3 = REPO / "docs" / "data-ontology" / "pass3"
DECISIONS = REPO / "decisions"

EXPECTED = {
    "STD-DATA-COM-001": ("PROPOSED", 1),
    "STD-DATA-COM-002": ("PROPOSED", 2),
    "STD-DATA-COM-003": ("PROPOSED", 2),
    "STD-DATA-COM-004": ("PROPOSED", 1),
}

DECISION_RECORDS = {
    "0010-data-com-001-decision.md": "STD-DATA-COM-001",
    "0011-data-com-002-decision.md": "STD-DATA-COM-002",
    "0012-data-com-003-decision.md": "STD-DATA-COM-003",
    "0013-data-com-004-decision.md": "STD-DATA-COM-004",
}

# (base commit where introduced, path, sha256 of CRLF-normalized content).
# Hash comparison is used instead of git subprocesses (git-spawn is
# unreliable on this host). These pin the surveyed evidence, the frozen UI
# baseline, and the two v1 drafts that Pass 2.5 did not touch.
FROZEN_HASHES = {
    "d113207/baselines/ui-standards-v1.0.json":
        "94eaaa1486bf18ed1b072c5f82ffa3d71d8a8c81bab6269dbdea567d61f3e0f9",
    "d113207/baselines/ui-standards-v1.0-release-notes.md":
        "51f6c5322de241dce8b60fe5deea7107f9ebb179bd911b1b850f08cd35f264f1",
    "3ce1c2c/docs/data-ontology/pass0/evidence-log.md":
        "1c27cf60f8fb19ed39ba9c7ff9afb457628903f443a19c5c86d63cde2b85ac16",
    "3ce1c2c/docs/data-ontology/pass0/incident-ledger.md":
        "6a97e04ffdc64a94ecf74bd0c92d49d31a42f29fd29b9bf0cf7eeb08321c7c88",
    "3ce1c2c/docs/data-ontology/pass0/handoff.md":
        "1861e61cfa1fc8aacf05c08be9ad7f05223b1efc6987f3aa674a728bb955c043",
    "0166aeb/docs/data-ontology/pass0/adjudication.md":
        "2143093f6524c4fa8dd1796f77dd44d5568d373d7368f403f02fd2cc6ab16246",
    "0166aeb/docs/data-ontology/pass0/candidates/holds-and-rejects.md":
        "6905cd72b8733672ca91b86bec58c2e2347b8bbbd616695427e362752a8259cc",
}


def _normalized_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def test_exactly_four_data_standards_remain_proposed_at_expected_versions():
    files = sorted(DATA_DIR.glob("STD-DATA-*.json"))
    assert {p.stem for p in files} == set(EXPECTED)
    for path in files:
        d = json.loads(path.read_text())
        assert d["status"] == "PROPOSED", f"{d['id']}: survey must not ratify"
        assert (d["status"], d["version"]) == EXPECTED[d["id"]], (
            f"{d['id']}: version/status drifted from the surveyed state"
        )


def test_no_data_standard_is_ratified():
    ratified = [
        p.name for p in sorted(DATA_DIR.glob("STD-DATA-*.json"))
        if json.loads(p.read_text())["status"] == "RATIFIED"
    ]
    assert not ratified, f"survey must not ratify: {ratified}"


def test_pass3_survey_dossier_exists_with_all_four_recommendations():
    text = (PASS3 / "ratification-survey.md").read_text()
    for sid in EXPECTED:
        assert sid in text
    rec_lines = [
        line for line in text.splitlines()
        if line.startswith("| STD-DATA-") and "RATIFY AS WRITTEN" in line
    ]
    assert len(rec_lines) == 4, f"expected 4 recommendation rows, found {len(rec_lines)}"


def test_decision_records_exist_awaiting_operator_decision():
    for name, sid in DECISION_RECORDS.items():
        text = (DECISIONS / name).read_text()
        assert "Status: AWAITING OPERATOR DECISION" in text, name
        assert sid in text
        assert "Option A" in text
        assert "MUST NOT" in text, f"{name}: must carry the no-self-ratification warning"


def test_no_self_ratification_occurred():
    for name in DECISION_RECORDS:
        text = (DECISIONS / name).read_text()
        assert "Status: Accepted" not in text
        assert "Status: Ratified" not in text
    for path in sorted(DATA_DIR.glob("STD-DATA-*.json")):
        d = json.loads(path.read_text())
        assert d["status"] == "PROPOSED"


def test_no_new_data_candidate_standard_appeared():
    files = sorted(DATA_DIR.glob("STD-DATA-*.json"))
    assert {p.stem for p in files} == set(EXPECTED)
    assert len(files) == 4


def test_frozen_artifacts_unchanged():
    for key, expected in FROZEN_HASHES.items():
        base, rel = key.split("/", 1)
        path = REPO / rel
        assert path.is_file(), f"{rel} missing"
        digest = _normalized_sha256(path)
        assert digest == expected, (
            f"{rel} diverged from its {base} content — modified after introduction"
        )
