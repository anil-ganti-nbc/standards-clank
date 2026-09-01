import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audits" / "watch-clank-cross-domain-2026-09-01-reaudit-2.json"


def test_m4c_is_read_only_and_complete():
    data = json.loads(AUDIT.read_text())
    assert data["standards_clank_head"] == "aa9b58c53e94a0d5db6dc009f0ac4ada53566cdb"
    assert data["target"]["head"] == "f78575a903d64c75bcee62cb81cbe9e70f3f9db7"
    assert data["target"]["modified"] is False
    assert len(data["verdicts"]) == 25
    assert {item["applicability"] for item in data["verdicts"]} == {"APPLIES"}
    assert data["no_remediation_declaration"] is True
    assert data["no_known_evidence_admission"] is True
    assert data["no_frozen_standard_changes"] is True


def test_m4c_preserves_live_pending_and_records_residual_ops_gap():
    data = json.loads(AUDIT.read_text())
    states = {item["id"]: item["state"] for item in data["verdicts"]}
    assert states["STD-OPS-COM-003"] == "NON_CONFORMING"
    assert states["STD-DEPLOY-COM-001"] == "INSUFFICIENT_EVIDENCE"
    assert data["implementation_check"]["G"] == "YES"
    assert data["known_evidence_admission"].startswith("DO NOT ADMIT")
