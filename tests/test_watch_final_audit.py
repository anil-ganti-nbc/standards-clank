"""Guards for the final Watch cross-domain audit and evidence admission."""

import json
from pathlib import Path

from tools.deployment_agent_layer import build_known_evidence_index
from tools.fleet_standards_resolver import frozen_standards

REPO = Path(__file__).resolve().parents[1]
AUDIT_JSON = REPO / "audits" / "watch-clank-cross-domain-2026-09-01-final.json"
AUDIT_MD = REPO / "audits" / "watch-clank-cross-domain-2026-09-01-final.md"
PRIOR_M4G = REPO / "audits" / "watch-clank-cross-domain-2026-09-01-reaudit-4.md"
CONFIRMED = REPO / "audits" / "watch-clank-deploy-live-proof-2026-09-01-confirmed.md"
FAILED = REPO / "audits" / "watch-clank-deploy-live-proof-2026-09-01.md"


def _audit():
    return json.loads(AUDIT_JSON.read_text(encoding="utf-8"))


def test_final_audit_has_exact_watch_and_standards_identity():
    audit = _audit()
    assert audit["standards_clank_head"] == "528b51c2e494890439abcaac87ce4e64e386d252"
    assert audit["target"]["head"] == "d03bc4b2f90289686331af0447d5ca4e8cf55822"
    assert audit["target"]["modified"] is False


def test_final_audit_matches_resolver_and_has_no_unresolved_verdict():
    audit = _audit()
    # M4G's controlling applicability ledger established all frozen ratified
    # standards as APPLIES.  The profile fact map is intentionally not edited
    # in this narrow conformance pass.
    applicable = {row["standard"]["id"] for row in frozen_standards()}
    verdicts = audit["verdicts"]
    assert {item["id"] for item in verdicts} == applicable
    assert len(verdicts) == 25
    assert {item["state"] for item in verdicts} == {"CONFORMS"}
    assert audit["final_counts"] == {
        "CONFORMS": 25,
        "NON_CONFORMING": 0,
        "INSUFFICIENT_EVIDENCE": 0,
        "NOT_APPLICABLE": 0,
        "UNKNOWN": 0,
    }


def test_deploy_closure_requires_confirmed_live_proof_fields():
    audit = _audit()["deployment_com_001"]
    assert audit["verdict"] == "CONFORMS"
    assert audit["lifecycle"] == "CLOSED"
    assert audit["live_proof"] == "LIVE_PROOF_CONFIRMED"
    assert audit["intended_revision"] == audit["observed_revision"] == "d03bc4b2f90289686331af0447d5ca4e8cf55822"
    assert audit["config_matches"] is True
    assert audit["wiring_matches"] is True
    assert audit["converged"] is True
    assert audit["comparator_state"] == "COMPLETE"
    assert audit["comparison_matches"] is True
    assert audit["comparator_exit"] == 0
    assert audit["evidence_artifact"] == "audits/watch-clank-deploy-live-proof-2026-09-01-confirmed.md"


def test_live_proof_history_and_supersession_are_preserved():
    assert "LIVE_PROOF_FAILED" in FAILED.read_text(encoding="utf-8")
    assert "LIVE_PROOF_CONFIRMED" in CONFIRMED.read_text(encoding="utf-8")
    assert '"superseded_by":"audits/watch-clank-cross-domain-2026-09-01-final.md"' in PRIOR_M4G.read_text(encoding="utf-8")
    assert "historical evidence" in AUDIT_MD.read_text(encoding="utf-8")


def test_deployment_known_evidence_is_admitted_deterministically():
    audit = _audit()["known_evidence_admission"]
    entries = build_known_evidence_index()
    assert entries == json.loads((REPO / "standards/deployment/known-evidence-index.json").read_text(encoding="utf-8"))
    # M11-M18 add independently guarded Semiconductor, KTW, Tablet,
    # Feature Phone, OEM Radar, CTW, and Smartwatch Deployment facts; M22,
    # M25, and M28 add the Smartwatch, Feature Phone, and Tablet COM-001
    # live-proof facts. The Watch admission remains unchanged and is still
    # present once.
    assert len(entries) == 11
    watch = [entry for entry in entries if entry["subject"] == "watch-clank"]
    assert len(watch) == audit["entries"] == 1
    assert watch[0]["standard"] == "STD-DEPLOY-COM-001"
    assert watch[0]["kind"] == "known_conformance"
    assert watch[0]["source_reference"] == "audits/watch-clank-cross-domain-2026-09-01-final.md"
    ktw = [entry for entry in entries if entry["subject"] == "korean-tech-wire"]
    assert len(ktw) == 1
    assert ktw[0]["standard"] == "STD-DEPLOY-COM-002"
    assert ktw[0]["source_reference"] == "audits/ktw-persistent-state-remediation-m12-2026-09-02.md"
    tablet = [entry for entry in entries if entry["subject"] == "tablet-clank"
              and entry["standard"] == "STD-DEPLOY-COM-002"]
    assert len(tablet) == 1
    assert tablet[0]["source_reference"] == "audits/tablet-persistent-state-remediation-m13-2026-09-02.md"


def test_reference_clank_claim_is_descriptive_and_scoped():
    audit = _audit()
    assert audit["reference_clank"] == {
        "clank": "watch-clank",
        "first_fully_wired_admitted_reference": True,
        "descriptive_only": True,
    }
    assert "not for future revisions" in audit["scope_caveat"]
