"""Data/Ontology holds-disposition (2026-08-31) process guards.

The operator-delegated triage ruled on every Pass 0B HOLD/REHOME/REJECT
concern: five DEFER BEYOND V1, one REHOME (confirmed), one REJECT
(stands). These guards pin the disposition artefact, the per-concern
coverage, and the fact that triage created no normative standards and
touched no ratified file.
"""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DISPOSITION = REPO / "docs" / "data-ontology" / "holds-disposition.md"
DATA_DIR = REPO / "standards" / "data-ontology"

CONCERNS = [
    "Honest-unknown / availability-honesty backing",
    "Cross-Clank entity identity",
    "Confidence-and-certainty semantics",
    "Canonical fact overwrite discipline",
    "Regional variant identity",
    "Timestamp-shaped values",
    "Source-disagreement representation",
]
DISPOSITIONS = ("ADVANCE FOR V1", "DEFER BEYOND V1", "REHOME", "REJECT")


def test_disposition_document_exists():
    assert DISPOSITION.is_file()
    assert len(DISPOSITION.read_text()) > 3000


def test_every_concern_has_exactly_one_disposition():
    text = DISPOSITION.read_text()
    rows = [line for line in text.splitlines() if line.startswith("| ") and "DEFER BEYOND V1" in line or (
        line.startswith("| ") and any(d in line for d in ("REHOME", "REJECT"))
    )]
    covered = [c for c in CONCERNS if c in text]
    assert covered == CONCERNS, f"missing concerns: {set(CONCERNS) - set(covered)}"
    for concern in CONCERNS:
        rows_for = [row for row in rows if concern in row]
        assert len(rows_for) == 1, f"{concern}: {len(rows_for)} summary rows"
        matches = [d for d in DISPOSITIONS if d in rows_for[0]]
        assert len(matches) == 1, f"{concern}: needs exactly one disposition, got {matches}"


def test_zero_concerns_advance_into_v1():
    text = DISPOSITION.read_text()
    summary = text.split("Per-concern rulings")[0]
    assert "Zero concerns advance into a DATA v1 baseline" in summary
    assert "ADVANCE FOR V1" not in summary


def test_triage_created_no_normative_standard():
    files = sorted(DATA_DIR.glob("STD-DATA-*.json"))
    assert len(files) == 4, "triage must not create standards"
    for path in files:
        d = json.loads(path.read_text())
        assert d["status"] == "RATIFIED" and d["id"] in {
            "STD-DATA-COM-001", "STD-DATA-COM-002", "STD-DATA-COM-003", "STD-DATA-COM-004",
        }


def test_promotion_triggers_recorded_for_each_defer():
    text = DISPOSITION.read_text()
    assert text.count("Promotion trigger:") >= 4, (
        "each DEFER must state what would reopen it"
    )


def test_rehome_target_is_non_ui():
    text = DISPOSITION.read_text()
    assert "diagnostic/testing practice" in text
