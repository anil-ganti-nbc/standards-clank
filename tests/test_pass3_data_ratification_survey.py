"""Data/Ontology Pass 3 (ratification survey) process guards.

At the time Pass 3 ran, its job was to leave all four DATA standards
PROPOSED at their exact versions, persist four awaiting-operator decision
records that did not self-ratify, and leave the frozen UI baseline, the
Pass 0/1/2 evidence, the Pass 0B adjudication, and the HOLD/REJECT
candidates untouched. A later, separately-authorized operator ruling
(decisions/0010-0013) has since ratified all four standards as written —
see tests/test_data_ontology_ratification_closure.py for the live
ratification/traceability guards. This file's remaining live job is
verifying Pass 3's own historical output (the survey dossier, the
originally-worded decision records, the frozen evidence hashes) wasn't
altered beyond the legitimate later status/notes changes ratification
made.
"""

import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATA_DIR = REPO / "standards" / "data-ontology"
PASS3 = REPO / "docs" / "data-ontology" / "pass3"
DECISIONS = REPO / "decisions"

EXPECTED_VERSIONS = {
    "STD-DATA-COM-001": 1,
    "STD-DATA-COM-002": 2,
    "STD-DATA-COM-003": 2,
    "STD-DATA-COM-004": 1,
}

DECISION_RECORDS = {
    "0010-data-com-001-decision.md": "STD-DATA-COM-001",
    "0011-data-com-002-decision.md": "STD-DATA-COM-002",
    "0012-data-com-003-decision.md": "STD-DATA-COM-003",
    "0013-data-com-004-decision.md": "STD-DATA-COM-004",
}

# (base commit where introduced, path, sha256 of CRLF-normalized content).
# Hash comparison is used instead of git subprocesses (git-spawn is
# unreliable on this host). These pin the surveyed evidence and the frozen
# UI baseline — none of which ratification touches or should touch.
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


def test_four_data_standards_ratified_at_the_surveyed_versions():
    """Pass 3 surveyed all four at these exact versions while PROPOSED.
    Ratification preserves version numbers exactly (operator instruction)
    and only changes status/notes — verified here as the live check."""
    files = sorted(DATA_DIR.glob("STD-DATA-*.json"))
    assert {p.stem for p in files} == set(EXPECTED_VERSIONS)
    for path in files:
        d = json.loads(path.read_text(encoding="utf-8"))
        assert d["status"] == "RATIFIED", f"{d['id']}: expected RATIFIED post-closure"
        assert d["version"] == EXPECTED_VERSIONS[d["id"]], f"{d['id']}: version drifted from the surveyed state"


def test_pass3_survey_dossier_exists_with_all_four_recommendations():
    text = (PASS3 / "ratification-survey.md").read_text(encoding="utf-8")
    for sid in EXPECTED_VERSIONS:
        assert sid in text
    rec_lines = [
        line for line in text.splitlines()
        if line.startswith("| STD-DATA-") and "RATIFY AS WRITTEN" in line
    ]
    assert len(rec_lines) == 4, f"expected 4 recommendation rows, found {len(rec_lines)}"


def test_decision_records_are_accepted_and_still_carry_the_survey_outcome():
    """Pass 3 left these as 'AWAITING OPERATOR DECISION' — a later,
    separately-authorized operator ruling flipped them to Accepted (with
    an added Operator ruling section; see
    tests/test_data_ontology_ratification_closure.py). This test's live
    job: the original survey outcome/recommendation/Option-A text Pass 3
    wrote must still be present, unedited, underneath the appended
    ruling — the ruling must not have overwritten history."""
    for name, sid in DECISION_RECORDS.items():
        text = (DECISIONS / name).read_text(encoding="utf-8")
        assert "Status: Accepted" in text, name
        assert sid in text
        assert "Option A" in text
        assert "MUST NOT ratify" in text, f"{name}: must still carry the no-self-ratification warning"
        assert "Operator ruling" in text, f"{name}: expected an appended Operator ruling section"


def test_no_new_data_candidate_standard_appeared():
    files = sorted(DATA_DIR.glob("STD-DATA-*.json"))
    assert {p.stem for p in files} == set(EXPECTED_VERSIONS)
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
