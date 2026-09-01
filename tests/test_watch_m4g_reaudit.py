import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audits" / "watch-clank-cross-domain-2026-09-01-reaudit-4.json"


def test_m4g_closure_ledger_is_complete_and_read_only():
    data = json.loads(AUDIT.read_text())
    assert data["target"]["head"] == "d03bc4b2f90289686331af0447d5ca4e8cf55822"
    assert data["target"]["modified"] is False
    assert len(data["verdicts"]) == 25
    assert {item["applicability"] for item in data["verdicts"]} == {"APPLIES"}
    assert data["no_remediation_declaration"] is True
    assert data["no_known_evidence_admission"] is True
    assert data["no_frozen_standard_changes"] is True


def test_m4g_ops_closure_requires_reset_and_terminal_facts():
    data = json.loads(AUDIT.read_text())
    closure = data["ops_com_003_closure"]
    assert all(closure[key] is True for key in (
        "structural_provenance", "pre_event_reset", "reset_lineage",
        "reset_terminal_coexistence", "terminal_dedup_ignores_reset", "terminal_idempotence",
    ))
    states = {item["id"]: item["state"] for item in data["verdicts"]}
    assert states["STD-OPS-COM-003"] == "CONFORMS"
    assert states["STD-DEPLOY-COM-001"] == "INSUFFICIENT_EVIDENCE"
    assert data["known_evidence_recommendation"] == "ADMIT AFTER LIVE PROOF"
