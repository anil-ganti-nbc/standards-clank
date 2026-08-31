import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audits" / "watch-clank-cross-domain-2026-09-01-reaudit.json"


def test_m4a_reaudit_is_complete_and_read_only():
    data = json.loads(AUDIT.read_text())
    assert data["target"]["head"] == "89d159dff59f242de176498444a20abf98a3df7f"
    assert data["target"]["modified"] is False
    assert len(data["verdicts"]) == 25
    assert all(item["applicability"] == "APPLIES" and item["state"] in {"CONFORMS", "NON_CONFORMING", "INSUFFICIENT_EVIDENCE"} for item in data["verdicts"])
    assert data["no_remediation_declaration"] is True
    assert data["no_known_evidence_admission"] is True
    assert data["no_frozen_standard_changes"] is True


def test_m4a_tracks_frozen_tags_and_finding_lifecycle():
    data = json.loads(AUDIT.read_text())
    assert data["frozen_tags"] == {
        "ui-standards-v1.0": "71e7ac427fd3c6dc11eea87d3eab528cd72ffd5f",
        "data-ontology-standards-v1.0": "f2f8a7626592f5f007377b1e0b04d2feb78d5cc2",
        "operations-standards-v1.0": "b36239d4b07b578822d62c8681046fa108e32d5c",
        "deployment-standards-v1.0": "6c00706b6a9469d17996978b01af91a1f46d62a9",
    }
    lifecycle = {item["finding_id"]: item["state"] for item in data["prior_finding_lifecycle"]}
    assert lifecycle["WC-M1-001"] == "CLOSED"
    assert "kernel-observed" in next(item for item in data["prior_finding_lifecycle"] if item["finding_id"] == "WC-M1-001")["basis"]
    assert lifecycle["STD-DEPLOY-COM-001-insufficiency"] == "LIVE_PROOF_PENDING"
    assert next(item for item in data["verdicts"] if item["id"] == "STD-DEPLOY-COM-001")["state"] == "INSUFFICIENT_EVIDENCE"
