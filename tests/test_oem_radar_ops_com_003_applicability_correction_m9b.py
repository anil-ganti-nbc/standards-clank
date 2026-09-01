"""Guards for the OEM Radar M9B applicability correction."""

import hashlib
import json
import subprocess
from pathlib import Path

from tools.operations_agent_layer import build_known_evidence_index


ROOT = Path(__file__).resolve().parents[1]
AUDIT_MD = ROOT / "audits" / "oem-radar-ops-com-003-applicability-correction-m9b-2026-09-01.md"
AUDIT_JSON = ROOT / "audits" / "oem-radar-ops-com-003-applicability-correction-m9b-2026-09-01.json"
M1 = ROOT / "audits" / "fleet-blind-audit-sweep-m1-2026-09-01.json"
KNOWN = ROOT / "standards" / "operations" / "known-evidence-index.json"
REGISTRY = ROOT / "profiles" / "fleet-adoption.json"
OEM_SHA = "d720e0635894ddcc9a39f116e2aa4a1768090042"
STANDARDS_SHA = "421aab2a3e185a6ad6d72fef2ac5b3aa762e5be1"
M1_SHA256 = "1b6bfa718f2528db1655eb20f63d534e426440ed8b2e46e325c9bb020effedde"
# Recomputed at the M14 recording pass with LF-normalized hashing (the
# prior value was a raw CRLF working-copy hash, host-dependent); the
# operations index content itself is unchanged.
KNOWN_SHA256 = "b5673b0be4d85f430c0ef803b1b54a9ca77146146c9d0373405dc789e00299a1"


def _record():
    return json.loads(AUDIT_JSON.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    # LF-normalized so the pins are checkout-EOL independent (raw-byte
    # hashing made this guard fail on CRLF working copies for reasons
    # unrelated to content).
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def test_m9b_pins_target_and_current_not_applicable_state():
    record = _record()
    assert record["standards_clank_head"] == STANDARDS_SHA
    target = record["target"]
    assert target["head"] == OEM_SHA
    assert target["origin_main"] == OEM_SHA
    assert target["working_tree"] == "CLEAN"
    assert target["standard"] == "STD-OPS-COM-003"
    assert target["current_applicability"] == "NOT_APPLICABLE"
    assert record["correction"]["current_applicability"] == "NOT_APPLICABLE"
    assert record["correction"]["conformance_claim"] is False


def test_m9b_preserves_m1_history_and_changes_only_one_state():
    record = _record()
    assert _sha256(M1) == M1_SHA256
    history = record["history"]
    assert history["m1_rewritten"] is False
    assert history["m1_oem_radar_state"] == "INSUFFICIENT_EVIDENCE"
    assert history["chain"].startswith("M1 uncertainty")
    counts = record["counts"]
    assert counts["before_m1"] == {
        "APPLIES": 22,
        "NOT_APPLICABLE": 3,
        "CONFORMS": 18,
        "NON_CONFORMING": 0,
        "INSUFFICIENT_EVIDENCE": 4,
    }
    assert counts["after_m9b"] == {
        "APPLIES": 21,
        "NOT_APPLICABLE": 4,
        "CONFORMS": 18,
        "NON_CONFORMING": 0,
        "INSUFFICIENT_EVIDENCE": 3,
    }
    assert counts["changed_standard_ids"] == ["STD-OPS-COM-003"]
    assert counts["preserved_insufficiencies"] == [
        "STD-UI-COM-011",
        "STD-DEPLOY-COM-001",
        "STD-DEPLOY-COM-002",
    ]
    assert counts["unrelated_findings_changed"] is False


def test_m9b_leaves_resolver_fact_missing_and_unmodified():
    record = _record()
    facts = record["resolver_fact_boundary"]
    assert facts["mapped_fact"] == "has_promotion_soak"
    assert facts["registry_fact_value"] == "MISSING"
    assert facts["raw_resolver_disposition"] == "UNKNOWN"
    assert facts["fact_invented"] is False
    assert facts["resolver_mutated"] is False
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    entry = next(row for row in registry["clanks"] if row["id"] == "oem-radar")
    assert entry["facts"] == {}
    assert "has_promotion_soak" not in entry["facts"]


def test_m9b_does_not_admit_oem_conformance_evidence():
    record = _record()
    admission = record["known_evidence"]
    assert admission["conformance_admitted"] is False
    assert admission["non_conformance_admitted"] is False
    assert admission["applicability_finding_kind"] == "not_applicable"
    assert admission["oem_radar_ops_com_003_entry_created"] is False
    assert _sha256(KNOWN) == KNOWN_SHA256
    assert json.loads(KNOWN.read_text(encoding="utf-8")) == build_known_evidence_index()
    assert all(entry["subject"] != "oem-radar" for entry in build_known_evidence_index())
    block = AUDIT_MD.read_text(encoding="utf-8").split("```json", 1)[1].split("```", 1)[0]
    finding = json.loads(block)["findings"][0]
    assert finding["kind"] == "not_applicable"
    assert "NOT_APPLICABLE" in finding["summary"]


def test_m9b_frozen_standard_and_tags_remain_unchanged():
    path = ROOT / "standards" / "operations" / "STD-OPS-COM-003.json"
    tagged = subprocess.run(
        ["git", "show", f"operations-standards-v1.0:{path.relative_to(ROOT).as_posix()}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        stdin=subprocess.DEVNULL,
        check=True,
    ).stdout
    assert path.read_text(encoding="utf-8") == tagged
    expected_tags = {
        "ui-standards-v1.0": "d11320704aed69a3d8f854c9264b184e392ec80f",
        "data-ontology-standards-v1.0": "464a8057ea5dc26ef83248a20bafa0be5aa31148",
        "operations-standards-v1.0": "7100f294a83c30594f2ff9e953f7c9f77a95747f",
        "deployment-standards-v1.0": "33cc38849180716fd4d06b1356cf70c49d3d41d2",
    }
    for tag, expected in expected_tags.items():
        actual = subprocess.run(
            ["git", "rev-parse", f"{tag}^{{commit}}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            stdin=subprocess.DEVNULL,
            check=True,
        ).stdout.strip()
        assert actual == expected


def test_m9b_safety_and_validation_are_explicit():
    record = _record()
    safety = record["safety"]
    for key in (
        "target_modified",
        "host_access",
        "deployment_changed",
        "frozen_standard_changed",
        "tags_moved",
        "m1_history_rewritten",
        "resolver_or_trigger_facts_changed",
        "unrelated_standards_reaudited",
        "full_target_conformance_claim",
    ):
        assert safety[key] is False
    assert safety["target_tests_run"] is False
    assert safety["collectors_run"] is False
    validation = record["validation"]
    assert validation == {
        "command": "python -m pytest",
        "direct_unpiped": True,
        "passed": 840,
        "skipped": 0,
        "failed": 0,
        "exit_code": 0,
        "elapsed_seconds": 8.40,
    }
