"""Operations hold-resolution / final-gap disposition (2026-08-31) process
guards.

The operator-delegated review reconfirmed all four Pass 0B HOLD/DEFER/REHOME
dispositions and asked the final "is any essential Operations contract
still missing from v1" question. These guards pin the disposition
artefact, the per-concern reconfirmation, the topic-coverage table, and
the fact that this pass created no normative standard and touched no
ratified file.
"""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DISPOSITION = REPO / "docs" / "operations" / "holds-disposition.md"
OPS_DIR = REPO / "standards" / "operations"

CONCERNS = [
    "Lifecycle-state model: BLOCKED is prose, not code",
    "Destructive production-action authority",
    "Deployment truth + config drift",
    "Delivery retry/idempotency",
]
DISPOSITIONS = ("**HOLD**", "**DEFER**", "**REHOME**")


def test_disposition_document_exists():
    assert DISPOSITION.is_file()
    assert len(DISPOSITION.read_text(encoding="utf-8")) > 3000


def test_every_concern_reconfirmed_with_exactly_one_disposition():
    text = DISPOSITION.read_text(encoding="utf-8")
    rows = [line for line in text.splitlines() if line.startswith("| ") and "Still stands?" not in line]
    for concern in CONCERNS:
        rows_for = [row for row in rows if concern in row]
        assert len(rows_for) == 1, f"{concern}: {len(rows_for)} summary rows"
        matches = [d for d in DISPOSITIONS if d in rows_for[0]]
        assert len(matches) == 1, f"{concern}: needs exactly one disposition, got {matches}"
        assert "Yes" in rows_for[0], f"{concern}: must be explicitly reconfirmed as still standing"


def test_no_essential_operations_contract_missing_conclusion():
    text = DISPOSITION.read_text(encoding="utf-8")
    assert "NO ESSENTIAL OPERATIONS CONTRACT MISSING" in text


def test_all_fifteen_original_topics_covered_in_the_table():
    text = DISPOSITION.read_text(encoding="utf-8")
    table_section = text.split("### Topic-by-topic coverage")[1].split("### Incident cross-check")[0]
    rows = [line for line in table_section.splitlines() if line.startswith("| ") and line[2].isdigit()]
    assert len(rows) == 15, f"expected 15 topic rows, found {len(rows)}"


def test_disposition_created_no_normative_standard():
    files = sorted(OPS_DIR.glob("STD-OPS-*.json"))
    assert len(files) == 4, "this pass must not create or remove standards"
    for path in files:
        d = json.loads(path.read_text(encoding="utf-8"))
        assert d["status"] == "RATIFIED" and d["id"] in {
            "STD-OPS-COM-001", "STD-OPS-COM-002", "STD-OPS-COM-003", "STD-OPS-COM-004",
        }


def test_inc044_finding_recorded_as_evidence_gap_not_new_standard():
    """The one incident this pass found outside the cited-evidence trail
    (INC-044, concurrent Docker writers) must be recorded as
    corroborating evidence for the already-ratified COM-004, not framed
    as justifying a new or reopened standard."""
    text = DISPOSITION.read_text(encoding="utf-8")
    assert "INC-044" in text
    assert "not a missing standard" in text


def test_what_would_reopen_this_document_section_exists():
    text = DISPOSITION.read_text(encoding="utf-8")
    assert "## What would reopen this document" in text
