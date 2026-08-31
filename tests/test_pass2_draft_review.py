"""Data/Ontology Pass 2 (adversarial draft review) process guards.

The review pass must: review all four PROPOSED DATA drafts with exactly
one verdict each, change no normative status, create no new DATA
candidates or standards, leave the frozen UI baseline, the Pass 0
evidence, and the Pass 0B adjudication untouched, and reference only
valid standard IDs. Proposed wording is NOT encoded as ratified truth.
"""

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REVIEW = REPO / "docs" / "data-ontology" / "pass2" / "review.md"
DATA_DIR = REPO / "standards" / "data-ontology"
DATA_IDS = {
    "STD-DATA-COM-001", "STD-DATA-COM-002", "STD-DATA-COM-003", "STD-DATA-COM-004",
}
VERDICTS = ("APPROVE FOR RATIFICATION SURVEY", "REVISE", "HOLD")


def _review() -> str:
    return REVIEW.read_text(encoding="utf-8")


def test_review_dossier_exists():
    assert REVIEW.is_file()
    assert len(_review()) > 4000


def test_all_four_drafts_reviewed_with_exactly_one_verdict():
    text = _review()
    for sid in sorted(DATA_IDS):
        sections = [
            block for block in text.split("\n## ")
            if block.startswith(f"STD-DATA-{sid[-3:]}" ) or sid in block.split("\n")[0]
        ]
        assert sections, f"{sid} not reviewed"
        block = sections[0]
        verdict_lines = [
            line for line in block.splitlines()
            if line.startswith("- **Verdict:") or line.startswith("**Verdict")
        ]
        verdicts_found = [v for v in VERDICTS if any(v in vl for vl in verdict_lines)]
        assert len(verdicts_found) == 1, f"{sid}: verdicts found {verdicts_found}"


def test_each_draft_reviewed_section_names_the_standard_id():
    text = _review()
    for sid in sorted(DATA_IDS):
        assert f"## {sid} —" in text, f"review section header missing for {sid}"


def test_review_pass_itself_did_not_ratify_anything():
    """Live re-check of the historical claim: at the Pass 2 commit
    (7b33a71), no Data/Ontology standard was RATIFIED. A later,
    separately-authorized operator ruling has since ratified all four —
    that is not this pass's doing, verified by diffing the standards
    directory against the Pass 2 commit and confirming its own tree
    contained no RATIFIED status."""
    import subprocess

    result = subprocess.run(
        ["git", "-C", str(REPO), "show", "7b33a71:standards/data-ontology"],
        capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL,
    )
    assert result.returncode == 0
    for path in sorted(DATA_DIR.glob("STD-DATA-*.json")):
        blob = subprocess.run(
            ["git", "-C", str(REPO), "show", f"7b33a71:standards/data-ontology/{path.name}"],
            capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL,
        )
        assert blob.returncode == 0, f"{path.name} did not exist at the Pass 2 commit"
        assert json.loads(blob.stdout)["status"] == "PROPOSED", f"{path.name}: Pass 2 commit itself must not have ratified anything"


def test_exactly_four_data_standards_and_no_new_candidates():
    files = sorted(DATA_DIR.glob("STD-DATA-*.json"))
    assert {p.stem for p in files} == DATA_IDS
    assert len(files) == 4


# (base commit where the artifact was introduced, path, sha256 of the blob
# as stored at that commit). Guards compare working-tree bytes to the
# frozen base-commit content directly — no git subprocess, which is
# unreliable on this host (intermittent WinError 6 on rapid spawns).
FROZEN_ARTIFACTS = [
    ("0166aeb", "docs/data-ontology/pass0/candidates/holds-and-rejects.md",
     "1b13f64597953576d26aedb0653a2d77f8b19e6db387b167fba2475c66630e42"),
    ("d113207", "baselines/ui-standards-v1.0.json",
     "94eaaa1486bf18ed1b072c5f82ffa3d71d8a8c81bab6269dbdea567d61f3e0f9"),
    ("d113207", "baselines/ui-standards-v1.0-release-notes.md",
     "51f6c5322de241dce8b60fe5deea7107f9ebb179bd911b1b850f08cd35f264f1"),
    ("3ce1c2c", "docs/data-ontology/pass0/evidence-log.md",
     "1c27cf60f8fb19ed39ba9c7ff9afb457628903f443a19c5c86d63cde2b85ac16"),
    ("3ce1c2c", "docs/data-ontology/pass0/incident-ledger.md",
     "6a97e04ffdc64a94ecf74bd0c92d49d31a42f29fd29b9bf0cf7eeb08321c7c88"),
    ("3ce1c2c", "docs/data-ontology/pass0/handoff.md",
     "1861e61cfa1fc8aacf05c08be9ad7f05223b1efc6987f3aa674a728bb955c043"),
    ("0166aeb", "docs/data-ontology/pass0/adjudication.md",
     "2143093f6524c4fa8dd1796f77dd44d5568d373d7368f403f02fd2cc6ab16246"),
]


def test_frozen_artifacts_remain_byte_identical_to_their_base_commits():
    import hashlib

    for base, path, expected in FROZEN_ARTIFACTS:
        raw = (REPO / path).read_bytes()
        normalized = raw.replace(b"\r\n", b"\n")
        digest = hashlib.sha256(normalized).hexdigest()
        assert digest == expected, (
            f"{path} no longer matches its {base} content — modified after introduction"
        )


def test_review_references_valid_standard_ids():
    text = _review()
    referenced = set(re.findall(r"STD-DATA-(?:COM-\d+)", text))
    assert referenced <= DATA_IDS, f"review references unknown DATA ids: {referenced - DATA_IDS}"
    assert referenced == DATA_IDS, f"review must reference all four drafts, missing: {DATA_IDS - referenced}"
