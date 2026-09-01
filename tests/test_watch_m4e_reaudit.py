import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audits" / "watch-clank-cross-domain-2026-09-01-reaudit-3.json"


def test_m4e_ledger_is_complete_read_only_and_pins_watch():
    data = json.loads(AUDIT.read_text())
    assert data["target"]["head"] == "c192e799babf687eb98708a5bfd900b4f7c9aac2"
    assert data["target"]["modified"] is False
    assert len(data["verdicts"]) == 25
    assert {item["applicability"] for item in data["verdicts"]} == {"APPLIES"}
    assert data["no_remediation_declaration"] is True
    assert data["no_known_evidence_admission"] is True
    assert data["no_frozen_standard_changes"] is True


def test_m4e_requires_both_m4c_fixes_and_distinguishes_live_proof():
    data = json.loads(AUDIT.read_text())
    ops = data["ops_com_003_assessment"]
    assert ops["m4c_no_fabricated_provenance"] is True
    assert ops["m4c_reset_lineage"] is True
    assert ops["terminal_evidence_after_changed_reset"] is False
    states = {item["id"]: item["state"] for item in data["verdicts"]}
    assert states["STD-OPS-COM-003"] == "NON_CONFORMING"
    assert states["STD-DEPLOY-COM-001"] == "INSUFFICIENT_EVIDENCE"
    assert data["known_evidence_recommendation"].startswith("DO NOT ADMIT")
