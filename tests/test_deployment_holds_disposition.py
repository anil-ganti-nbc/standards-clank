"""Guards for Deployment Pass 4 final-gap disposition.

The audit resolves parked residuals without drafting a third standard or
turning its conclusion into a baseline/tag.
"""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
AUDIT = REPO / "docs" / "deployment" / "holds-disposition.md"
DEPLOY = REPO / "standards" / "deployment"
RESIDUALS = (
    "Target-environment identity", "Fleet Law 6 identity mechanics",
    "Deferred Fleet Law 9 provenance", "Destructive state / rollback / recovery",
    "Config congruence", "Partial runtime wiring", "Schema migration mechanics",
)


def test_final_gap_audit_exists_and_reaches_explicit_conclusion():
    text = AUDIT.read_text(encoding="utf-8")
    assert "NO ESSENTIAL DEPLOYMENT CONTRACT MISSING" in text
    assert "READY TO FREEZE DEPLOYMENT STANDARDS V1.0" in text
    assert "No fleet recrawl was performed" in text


def test_every_parked_residual_is_resolved_without_new_standard():
    text = AUDIT.read_text(encoding="utf-8")
    for residual in RESIDUALS:
        rows = [line for line in text.splitlines() if line.startswith("| ") and residual in line]
        assert len(rows) == 1, residual
        assert "Yes" in rows[0], residual
    standards = {path.stem: json.loads(path.read_text(encoding="utf-8")) for path in DEPLOY.glob("STD-DEPLOY-*.json")}
    assert set(standards) == {"STD-DEPLOY-COM-001", "STD-DEPLOY-COM-002"}
    assert all(record["status"] == "RATIFIED" and record["version"] == 1 for record in standards.values())


def test_audit_preserves_rehomes_without_reopening_them():
    text = AUDIT.read_text(encoding="utf-8")
    assert "PROPOSED — REVIEWED DRAFT" in text and "ADR-0009" in text
    assert "Fleet Law 6 is ACTIVE" in text and "Law 9 is DEFERRED" in text
    assert "What would reopen this document" in text
