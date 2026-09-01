"""Guards for the read-only OEM Radar OPS-COM-003 checkpoint."""

import json
import subprocess
from pathlib import Path

from tools.operations_agent_layer import build_known_evidence_index


ROOT = Path(__file__).resolve().parents[1]
AUDIT_MD = ROOT / "audits" / "oem-radar-ops-com-003-applicability-m9-2026-09-01.md"
AUDIT_JSON = ROOT / "audits" / "oem-radar-ops-com-003-applicability-m9-2026-09-01.json"
KNOWN = ROOT / "standards" / "operations" / "known-evidence-index.json"
OEM_SHA = "d720e0635894ddcc9a39f116e2aa4a1768090042"
STANDARDS_SHA = "d65e67a5fa4e48f788220596408ee867ffa52f36"


def _record():
    return json.loads(AUDIT_JSON.read_text(encoding="utf-8"))


def test_m9_pins_takeover_target_and_not_applicable_verdict():
    record = _record()
    assert record["standards_clank_head"] == STANDARDS_SHA
    target = record["target"]
    assert target["head"] == OEM_SHA
    assert target["origin_main"] == OEM_SHA
    assert target["working_tree"] == "CLEAN"
    assert target["standard"] == "STD-OPS-COM-003"
    assert target["applicability"] == "NOT_APPLICABLE"
    assert record["decision"]["verdict"] == "NOT_APPLICABLE"
    assert record["decision"]["remediation_warranted"] is False


def test_m9_proves_telemetry_without_qualification_semantics():
    record = _record()
    model = record["execution_model"]
    assert model["runtime_shape"] == "STATELESS_ONE_SHOT"
    assert model["durable_run_identity"]["present"] is True
    assert model["provenance"]["recorded"] is False
    assert model["persistence"]["qualification_evidence"] is False
    assert model["qualification_gate"]["present"] is False
    assert model["material_change"]["qualification_material_identity"] is False
    assert model["epoch_reset"]["qualification_epoch"] is False
    criteria = record["applicability_test"]
    assert criteria["evidence_persists_across_executions"] is True
    assert criteria["persisted_state_is_qualification_evidence"] is False
    assert criteria["evidence_affects_qualification_or_maturity_gate"] is False
    assert criteria["all_ops_com_003_conditions_satisfied"] is False


def test_m9_resolver_gap_is_recorded_without_mutating_governance():
    record = _record()
    facts = record["resolver_trigger_fact_analysis"]
    assert facts["mapped_fact"] == "has_promotion_soak"
    assert facts["registry_value"] == "MISSING"
    assert facts["finding"] == "TARGET_TRIGGER_FACT_INCOMPLETE"
    assert record["safety_guards"]["resolver_changed"] is False
    assert record["known_evidence"]["conformance_admitted"] is False
    assert record["known_evidence"]["non_conformance_admitted"] is False


def test_m9_not_applicable_finding_does_not_admit_known_evidence():
    record = _record()
    entries = json.loads(KNOWN.read_text(encoding="utf-8"))
    assert entries == build_known_evidence_index()
    assert all(entry["subject"] != "oem-radar" for entry in entries)
    block = AUDIT_MD.read_text(encoding="utf-8").split("```json", 1)[1].split("```", 1)[0]
    finding = json.loads(block)["findings"][0]
    assert finding["kind"] == "not_applicable"
    assert "NOT_APPLICABLE" in finding["summary"]


def test_m9_frozen_operations_standard_is_unchanged():
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


def test_m9_safety_and_validation_boundaries_are_explicit():
    record = _record()
    safety = record["safety_guards"]
    assert all(safety[key] is False for key in (
        "target_mutated",
        "host_access",
        "deployment_changed",
        "database_changed",
        "scheduler_changed",
        "frozen_standards_changed",
        "tags_moved",
        "resolver_changed",
        "known_evidence_admitted",
        "full_target_conformance_claim",
    ))
    assert safety["no_qualification_remediation"] is True
    validation = record["validation"]
    assert validation["target_tests_run"] is False
    assert validation["collectors_run"] is False
    assert validation["standards_suite"]["command"] == "python -m pytest"
    assert validation["standards_suite"]["direct_unpiped"] is True
    assert validation["standards_suite"]["status"] == "PASS"
    assert validation["standards_suite"]["passed"] == 834
    assert validation["standards_suite"]["failed"] == 0
    assert validation["standards_suite"]["skipped"] == 0
    assert validation["standards_suite"]["exit_code"] == 0
