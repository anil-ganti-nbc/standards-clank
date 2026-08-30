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


def test_each_dossier_references_its_standard_and_ratifying_decision():
    """Post-ratification: each dossier documents the standard whose v2 text
    was ratified (version preserved), and each standard's notes trace to
    its Pass 3 decision."""
    standards = {s["id"]: s for s in load_ui_standards()}
    decision_for = {
        "STD-UI-COM-012": "0007-pass3-com-012-decision.md",
        "STD-UI-COM-007": "0008-pass3-com-007-decision.md",
        "STD-UI-SKU-001": "0009-pass3-sku-001-decision.md",
    }
    for sid, text in _dossiers().items():
        assert sid in text
        status, version = standards[sid]["status"], standards[sid]["version"]
        assert status == "RATIFIED" and version == 2, f"{sid}: {status} v{version}"
        assert "decisions/" + decision_for[sid] in standards[sid]["notes"], (
            f"{sid}: notes must trace to its ratifying decision"
        )


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


def test_decision_records_carry_the_operator_acceptance():
    """Pre-ratification these records had to be un-marked; the operator has
    since accepted all three (Option A). The coherent post-closure state is:
    Accepted status, the operator ruling recorded, and the corresponding
    standard RATIFIED at v2."""
    standards = {s["id"]: (s["status"], s["version"]) for s in load_ui_standards()}
    for name, sid in (
        ("0007-pass3-com-012-decision.md", "STD-UI-COM-012"),
        ("0008-pass3-com-007-decision.md", "STD-UI-COM-007"),
        ("0009-pass3-sku-001-decision.md", "STD-UI-SKU-001"),
    ):
        text = (DECISIONS_DIR / name).read_text()
        assert "Status: Accepted (operator ruling, 2026-08-31)" in text, name
        assert "Option A" in text and "Operator ruling" in text, name
        assert standards[sid] == ("RATIFIED", 2), (
            f"{sid} must be RATIFIED v2 to be consistent with an accepted decision"
        )


def test_ratification_closure_state_is_15_ratified_zero_proposed():
    standards = load_ui_standards()
    ratified = sorted(s["id"] for s in standards if s["status"] == "RATIFIED")
    proposed = [s["id"] for s in standards if s["status"] == "PROPOSED"]
    assert len(ratified) == 15 and not proposed
    for sid in ("STD-UI-COM-007", "STD-UI-COM-012", "STD-UI-SKU-001"):
        entry = next(s for s in standards if s["id"] == sid)
        assert entry["version"] == 2, f"{sid}: text/version must be preserved exactly"


def test_pass3_preserves_text_and_closes_the_proposed_set():
    """The survey itself changed no text; the only post-survey mutation was
    the operator's ratification of all three at their v2 text, which closes
    the proposed set entirely."""
    statuses = {s["id"]: (s["status"], s["version"]) for s in load_ui_standards()}
    assert not [sid for sid, (st, _) in statuses.items() if st == "PROPOSED"]
    for sid in PROPOSED_IDS:
        assert statuses[sid] == ("RATIFIED", 2), f"{sid}: ratified at v2, text preserved"


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


def test_new_ratified_rules_present_in_generated_layer_with_pass3_traceability():
    """The regenerated ratified-index/checklist must carry the three rules,
    each tracing to its own Pass 3 decision record."""
    import json

    index = {e["id"]: e for e in json.loads((REPO / "standards/ui/ratified-index.json").read_text())}
    checklist = {i["standard"] for i in json.loads((REPO / "standards/ui/agent-checklist.json").read_text())}
    expected_decision = {
        "STD-UI-COM-007": "decisions/0008-pass3-com-007-decision.md",
        "STD-UI-COM-012": "decisions/0007-pass3-com-012-decision.md",
        "STD-UI-SKU-001": "decisions/0009-pass3-sku-001-decision.md",
    }
    for sid, decision in expected_decision.items():
        assert sid in index, f"{sid} missing from regenerated ratified-index"
        assert index[sid]["ratification_decision"] == decision
        assert sid in checklist, f"{sid} missing from regenerated agent-checklist"
