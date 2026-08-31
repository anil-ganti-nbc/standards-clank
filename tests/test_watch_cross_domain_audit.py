import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audits" / "watch-clank-cross-domain-2026-08-31.json"

def test_m1_audit_is_blind_pinned_and_complete():
    data = json.loads(AUDIT.read_text())
    assert data["mode"] == "BLIND_READ_ONLY"
    assert data["standards_clank_head"] == "23a07d29ae9fc87e349bbb75663930e1628dd7a6"
    assert data["target"]["head"] == "fbf228f7ecccf2de4119fca29f8344aff9c49441"
    assert set(data["baselines"].values()) == {"ui-standards-v1.0", "data-ontology-standards-v1.0", "operations-standards-v1.0", "deployment-standards-v1.0"}
    assert len(data["verdicts"]) == 25
    assert {x["state"] for x in data["verdicts"]} <= {"CONFORMS", "NON_CONFORMING", "INSUFFICIENT_EVIDENCE", "NOT_APPLICABLE", "UNKNOWN"}
    assert all(x["evidence"] for x in data["verdicts"])

def test_m1_has_no_target_change_and_finding_is_collapsed():
    data = json.loads(AUDIT.read_text())
    assert data["target"]["modified"] is False
    assert len(data["findings"]) == 1 and data["findings"][0]["severity"] == "MEDIUM"
    assert data["historical_comparison"]["after_blind_finalization"] is True
    assert "remediation is separate" in (ROOT / "audits" / "watch-clank-cross-domain-2026-08-31.md").read_text().lower()
