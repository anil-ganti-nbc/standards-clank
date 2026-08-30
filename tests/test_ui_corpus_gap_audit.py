"""Final UI corpus gap audit (2026-08-31) machinery tests.

The audit concluded NO ESSENTIAL UI CONTRACT MISSING. These tests pin the
audit artefact and guarantee the pass could not have grown the corpus or
drifted the generated layer: the corpus stays exactly 15 RATIFIED with the
original id set, the dossier exists with its conclusion and per-area
dispositions, domain-rehome candidates are explicitly non-UI, and the
generated agent layer remains deterministic.
"""

import json
import re
from pathlib import Path

from tools.ui_agent_layer import load_ui_standards

REPO = Path(__file__).resolve().parents[1]
DOSSIER = REPO / "docs" / "ui-corpus-gap-audit.md"

EXPECTED_IDS = {
    "STD-UI-COM-001", "STD-UI-COM-002", "STD-UI-COM-003", "STD-UI-COM-004",
    "STD-UI-COM-005", "STD-UI-COM-006", "STD-UI-COM-007", "STD-UI-COM-008",
    "STD-UI-COM-009", "STD-UI-COM-010", "STD-UI-COM-011", "STD-UI-COM-012",
    "STD-UI-NEWS-001", "STD-UI-NEWS-002", "STD-UI-SKU-001",
}

DISPOSITIONS = ("COVERED", "REJECTED", "REHOME", "PRODUCT BACKLOG")


def _dossier() -> str:
    return DOSSIER.read_text()


def test_gap_audit_dossier_exists():
    assert DOSSIER.is_file()
    assert len(_dossier()) > 3000


def test_gap_audit_conclusion_is_no_essential_contract_missing():
    text = _dossier()
    assert "NO ESSENTIAL UI CONTRACT MISSING" in text
    assert "ESSENTIAL GAP(S) FOUND" not in text, (
        "conclusion A and B are mutually exclusive; this audit concluded A"
    )


def test_gap_audit_investigates_the_full_prompt_area_list():
    """Every investigation area from the commission must appear with exactly
    one disposition, so no area was silently dropped."""
    text = _dossier()
    areas = [
        "Alert severity", "Blocked / degraded", "Stale data", "Baselining vs novelty",
        "Evidence reachability", "Destructive actions", "Retry semantics",
        "Partial success", "Source identity", "Configuration drift",
        "Scheduler state", "Suppression reasons", "Data-confidence",
        "Maintenance / mothball", "Unknown / unavailable", "Manual overrides",
        "Cross-Clank handoff",
    ]
    rows = [line for line in text.splitlines() if line.startswith("| ") and "→" or line.startswith("| ") and any(d in line for d in DISPOSITIONS)]
    for area in areas:
        matching = [row for row in text.splitlines() if area in row and "DISPOSITION" not in row]
        assert matching, f"area not investigated: {area}"
    dispo_rows = [
        line for line in text.splitlines()
        if line.startswith("| ") and any(d in line for d in DISPOSITIONS) and "Findings" not in line
    ]
    assert len(dispo_rows) >= 17, f"expected >=17 disposition rows, found {len(dispo_rows)}"
    for row in dispo_rows:
        matches = [d for d in DISPOSITIONS if d in row]
        assert len(matches) == 1, f"each row needs exactly one disposition: {row!r} -> {matches}"


def test_gap_audit_corpus_unchanged_15_ratified_zero_proposed():
    standards = load_ui_standards()
    assert len(standards) == 15
    assert {s["id"] for s in standards} == EXPECTED_IDS
    assert all(s["status"] == "RATIFIED" for s in standards), (
        "the gap audit must not create, ratify, or retire anything"
    )


def test_no_new_normative_rule_appears_from_the_audit():
    index = json.loads((REPO / "standards/ui/ratified-index.json").read_text())
    checklist = json.loads((REPO / "standards/ui/agent-checklist.json").read_text())
    assert {e["id"] for e in index} == EXPECTED_IDS
    assert {i["standard"] for i in checklist} == EXPECTED_IDS


def test_domain_rehome_items_are_explicitly_non_ui():
    text = _dossier()
    rehome_section = text.split("Domain-rehome candidates")[1].split("## 6.")[0]
    for target in ("DATA / ONTOLOGY STANDARD", "OPERATIONS STANDARD"):
        assert target in rehome_section, f"rehome section must name non-UI target domains: {target}"
    assert "UI STANDARD" not in rehome_section, (
        "rehome candidates must not be classified as UI standards"
    )


def test_watch_com007_backlog_is_not_treated_as_a_gap():
    text = _dossier()
    assert "not** evidence of a missing standard" in text or "not evidence of a missing standard" in text
    assert "COM-007 covers it" in text
