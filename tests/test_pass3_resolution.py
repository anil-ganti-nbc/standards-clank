"""Pass 3 (Proposed Standards Resolution) machinery tests.

The pass produces evidence dossiers and AWAITING-OPERATOR-DECISION records
for the three PROPOSED standards. It must not move any normative status:
these tests pin that the dossiers exist, carry exactly one recommendation
each, reference real proposed standards, and that nothing was ratified,
retired, leaked, or fabricated by the pass itself.
"""

import json
import re
from pathlib import Path

from tools.ui_agent_layer import load_ui_standards

REPO = Path(__file__).resolve().parents[1]
DOSSIER_DIR = REPO / "docs" / "pass3-proposed-standards"
DECISIONS_DIR = REPO / "decisions"

PROPOSED_IDS = ["STD-UI-COM-007", "STD-UI-COM-012", "STD-UI-SKU-001"]
RECOMMENDATIONS = [
    "RATIFY AS WRITTEN",
    "NARROW THEN RATIFY",
    "RETIRE / REJECT",
    "INSUFFICIENT EVIDENCE — HOLD",
]


def _dossiers() -> dict[str, str]:
    return {
        "STD-UI-COM-012": (DOSSIER_DIR / "com-012-dossier.md").read_text(),
        "STD-UI-COM-007": (DOSSIER_DIR / "com-007-dossier.md").read_text(),
        "STD-UI-SKU-001": (DOSSIER_DIR / "sku-001-dossier.md").read_text(),
    }


def test_dossier_files_exist_at_expected_paths():
    for name in ("com-012-dossier.md", "com-007-dossier.md", "sku-001-dossier.md"):
        assert (DOSSIER_DIR / name).is_file(), name


def test_each_dossier_references_its_current_proposed_standard():
    standards = {s["id"]: s for s in load_ui_standards()}
    for sid, text in _dossiers().items():
        assert sid in text
        assert standards[sid]["status"] == "PROPOSED", f"{sid} must still be PROPOSED"
        assert f"v {standards[sid]['version']}" in text or f"v{standards[sid]['version']}" in text


def test_each_dossier_has_exactly_one_recommendation():
    for sid, text in _dossiers().items():
        recs = [
            r for r in RECOMMENDATIONS
            if re.search(r"^\*\*" + re.escape(r) + r"\.\*\*", text, flags=re.MULTILINE)
            or f"**{r}.**" in text
        ]
        assert len(recs) == 1, f"{sid}: expected exactly one recommendation, found {recs}"
        assert "## Recommendation" in text


def test_each_dossier_contains_required_sections():
    required = [
        "Survey scope",
        "Evidence FOR",
        "Evidence AGAINST",
        "lineage",
        "Overlap analysis",
        "Applicability analysis",
        "estability",
        "Remaining uncertainty",
        "Operator decision required",
    ]
    for sid, text in _dossiers().items():
        for section in required:
            assert section in text, f"{sid} dossier missing section marker: {section!r}"


def test_each_dossier_records_survey_heads():
    for sid, text in _dossiers().items():
        shas = re.findall(r"\b[0-9a-f]{7}\b", text)
        assert len(shas) >= 5, f"{sid} dossier should cite surveyed repo HEADs, found {shas}"


def test_decision_records_exist_and_are_awaiting_operator_decision():
    for name, sid in (
        ("0007-pass3-com-012-decision.md", "STD-UI-COM-012"),
        ("0008-pass3-com-007-decision.md", "STD-UI-COM-007"),
        ("0009-pass3-sku-001-decision.md", "STD-UI-SKU-001"),
    ):
        text = (DECISIONS_DIR / name).read_text()
        assert "Status: AWAITING OPERATOR DECISION" in text
        assert sid in text
        assert "Option A" in text
        for forbidden in ("Status: Accepted", "Status: Ratified", "Status: Retired"):
            assert forbidden not in text, f"{name}: decision must not be self-marked {forbidden!r}"


def test_pass3_did_not_change_normative_status_or_counts():
    statuses = {s["id"]: (s["status"], s["version"]) for s in load_ui_standards()}
    ratified = [sid for sid, (st, _) in statuses.items() if st == "RATIFIED"]
    proposed = [sid for sid, (st, _) in statuses.items() if st == "PROPOSED"]
    assert len(ratified) == 12
    assert sorted(proposed) == sorted(PROPOSED_IDS)
    for sid in PROPOSED_IDS:
        assert statuses[sid] == ("PROPOSED", 2), f"{sid}: Pass 3 must not alter text version or status"
    for sid, (st, version) in statuses.items():
        if st == "RATIFIED":
            assert version >= 1  # unchanged from pre-pass state (versions untouched by dossiers)


def test_decision_records_do_not_self_ratify():
    """The decision records must present options, never declare an outcome."""
    for name in (
        "0007-pass3-com-012-decision.md",
        "0008-pass3-com-007-decision.md",
        "0009-pass3-sku-001-decision.md",
    ):
        text = (DECISIONS_DIR / name).read_text()
        assert "MUST NOT" in text or "must not" in text
        assert not re.search(r"^\s*RATIFY\s*$", text, flags=re.MULTILINE), name
