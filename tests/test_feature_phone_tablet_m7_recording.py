"""Narrow guards for the Feature Phone + Tablet M7 Operations record."""

import json
from pathlib import Path

from tools.operations_agent_layer import build_known_evidence_index


ROOT = Path(__file__).resolve().parents[1]
AUDIT_JSON = ROOT / "audits" / "feature-phone-tablet-qualification-remediation-m7-2026-09-01.json"
FEATURE_MD = ROOT / "audits" / "feature-phone-clank-qualification-remediation-m7-2026-09-01.md"
TABLET_MD = ROOT / "audits" / "tablet-clank-qualification-remediation-m7-2026-09-01.md"
KNOWN = ROOT / "standards" / "operations" / "known-evidence-index.json"
FEATURE_SHA = "4b7dce284f7c581395c5efe2b20ce1872e26897e"
TABLET_SHA = "d9cb32ccee1b2bcaa4bc9d8af5ac1a7a7e7f6769"
STANDARDS_SHA = "2a1fd3465872f38333031422bd623dbb4add04b0"


def _record():
    return json.loads(AUDIT_JSON.read_text(encoding="utf-8"))


def test_m7_records_two_narrow_closed_verdicts_at_canonical_revisions():
    record = _record()
    assert record["standards_clank_head"] == STANDARDS_SHA
    for subject, sha in (("feature-phone-clank", FEATURE_SHA), ("tablet-clank", TABLET_SHA)):
        target = record["targets"][subject]
        assert target["head"] == sha
        assert target["origin_main"] == sha
        assert target["standard"] == "STD-OPS-COM-003"
        assert target["state"] == "CONFORMS"
        assert target["lifecycle"] == "CLOSED"
        assert target["scope"] == "source-level qualification provenance/reset remediation only"


def test_m7_preserves_three_insufficiencies_and_prior_lock_closure():
    record = _record()
    expected_remaining = {
        "STD-UI-COM-011": "INSUFFICIENT_EVIDENCE",
        "STD-DEPLOY-COM-001": "INSUFFICIENT_EVIDENCE",
        "STD-DEPLOY-COM-002": "INSUFFICIENT_EVIDENCE",
    }
    for target in record["targets"].values():
        assert target["remaining_m1_insufficiencies"] == expected_remaining
        assert target["m3_lock_authority"]["state"] == "CONFORMS"
        assert target["m3_lock_authority"]["lifecycle"] == "CLOSED"
        assert target["m3_lock_authority"]["remains_intact"] is True
        assert target["m3_lock_authority"]["new_lock_evidence_admitted"] is False
    assert record["guards"]["full_target_conformance_claim"] is False


def test_m7_records_scope_isolation_and_validation_honestly():
    targets = _record()["targets"]
    feature = targets["feature-phone-clank"]
    assert feature["focused_qualification"] == {
        "command": "python -m pytest tests/test_qualification_m7.py",
        "passed": 3,
        "failed": 0,
    }
    assert feature["full_suite"]["baseline"]["failed"] == 4
    assert feature["full_suite"]["final"]["failed"] == 4
    assert feature["full_suite"]["final"]["passed"] == 217
    assert feature["full_suite"]["baseline_attribution"]["same_four_failures"] is True
    assert feature["full_suite"]["baseline_attribution"]["new_failures_introduced"] is False
    assert feature["full_suite"]["baseline_attribution"]["full_suite_claim"] == "not green"

    tablet = targets["tablet-clank"]
    assert tablet["focused_qualification"]["passed"] == 3
    assert tablet["full_suite"]["final"] == {
        "revision": TABLET_SHA,
        "passed": 121,
        "skipped": 0,
        "failed": 0,
        "exit_code": 0,
    }
    assert "source scope" in tablet["scope_model"]


def test_m7_family_result_is_descriptive_and_independent():
    family = _record()["family_status"]
    assert family["conclusion"] == "SQLITE_OPERATIONAL_SCOPE_RECIPE_VALIDATED"
    assert family["descriptive_only"] is True
    assert family["members"] == {"feature-phone-clank": FEATURE_SHA, "tablet-clank": TABLET_SHA}
    assert family["shared_contract_closed_independently"] is True
    assert family["evidence_inheritance"] is False
    assert family["other_target_conformance_inferred"] is False


def test_m7_known_evidence_admits_only_two_ops_facts():
    record = _record()
    admission = record["known_evidence_admission"]
    assert admission["performed"] is True
    assert admission["deployment_evidence_admitted"] is False
    assert admission["unrelated_standards_admitted"] is False
    assert len(admission["admitted"]) == 2
    entries = json.loads(KNOWN.read_text(encoding="utf-8"))
    assert entries == build_known_evidence_index()
    m7 = [
        entry for entry in entries
        if entry["source_reference"] in {
            "audits/feature-phone-clank-qualification-remediation-m7-2026-09-01.md",
            "audits/tablet-clank-qualification-remediation-m7-2026-09-01.md",
        }
    ]
    assert {(entry["subject"], entry["standard"]) for entry in m7} == {
        ("feature-phone-clank", "STD-OPS-COM-003"),
        ("tablet-clank", "STD-OPS-COM-003"),
    }
    assert all(entry["kind"] == "known_conformance" for entry in m7)
    assert all("CONFORMS / CLOSED" in entry["summary"] for entry in m7)


def test_m7_prose_keeps_scope_and_safety_boundaries():
    for path, markers in (
        (FEATURE_MD, (FEATURE_SHA, "SQLITE_OPERATIONAL_SCOPE_RECIPE_VALIDATED", "PRE_EXISTING / BASELINE_ATTRIBUTED", "STD-DEPLOY-COM-001")),
        (TABLET_MD, (TABLET_SHA, "SQLITE_OPERATIONAL_SCOPE_RECIPE_VALIDATED", "121 passed", "STD-DEPLOY-COM-002")),
    ):
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            assert marker in text
        assert "No Deployment evidence" in text
        assert "No overall target conformance claim" in text
        assert "No host" in text
