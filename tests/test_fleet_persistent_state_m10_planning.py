"""Narrow structural guards for the read-only M10 planning artifact."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audits" / "fleet-persistent-state-compatibility-planning-m10-2026-09-01.json"
KNOWN = ROOT / "standards" / "deployment" / "known-evidence-index.json"
EXPECTED_STANDARDS = "043612756452fc9db871833425c2a641b68e00c3"
EXPECTED_TARGETS = {
    "oem-radar": "d720e0635894ddcc9a39f116e2aa4a1768090042",
    "semiconductor-intelligence": "688b71a93b4988b5ce52ce85e46f09080b9a7948",
    "chinese-tech-wire": "1a47220c69e6bb91f2899a0508508c42254c9d5b",
    "korean-tech-wire": "2040af82136d8a8f181c464e7d62ce408dd2696d",
    "feature-phone-clank": "4b7dce284f7c581395c5efe2b20ce1872e26897e",
    "smartwatch-clank": "a631421e276b58ce3499787cc2bc72218648ce72",
    "tablet-clank": "d9cb32ccee1b2bcaa4bc9d8af5ac1a7a7e7f6769",
}


def _record():
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    # LF-normalized so the pin is checkout-EOL independent (raw-byte hashing
    # made this guard fail on CRLF working copies for reasons unrelated to
    # content).
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def test_m10_scope_shas_and_clean_takeover_are_exact():
    record = _record()
    assert record["standards_clank_head"] == EXPECTED_STANDARDS
    assert set(record["scope"]["included_targets"]) == set(EXPECTED_TARGETS)
    assert record["scope"]["excluded_targets"] == ["smartphone-clank"]
    assert record["safety"]["smartphone_added"] is False
    assert set(record["takeover"]["targets"]) == set(EXPECTED_TARGETS)
    for target in record["targets"]:
        name = target["target"]
        assert target["sha"] == EXPECTED_TARGETS[name]
        assert target["sha"] == record["takeover"]["targets"][name]["origin_head"]
        assert record["takeover"]["targets"][name]["working_tree"] == "CLEAN"
        assert target["applicability"] == "APPLIES"


def test_m10_is_planning_only_and_marks_no_target_conformance():
    record = _record()
    assert record["standard"]["id"] == "STD-DEPLOY-COM-002"
    assert len(record["targets"]) == 7
    assert all(target["planning_classification"] != "SOURCE_MECHANISM_PRESENT" for target in record["targets"])
    assert all(target["planning_classification"] != "RE-AUDIT_ONLY" for target in record["targets"])
    assert record["current_m1_context"]["no_target_conformance_claim"] is True
    safety = record["safety"]
    for key in (
        "target_repositories_modified",
        "target_tests_or_collectors_run",
        "target_migrations_run",
        "databases_edited",
        "hosts_accessed",
        "deployments_or_restarts",
        "resolver_facts_modified",
        "known_evidence_admitted",
        "frozen_standards_modified",
        "tags_moved",
    ):
        assert safety[key] is False


def test_m10_families_order_and_recipe_are_deterministic():
    record = _record()
    assert len(record["families"]) == 5
    assert [item["rank"] for item in record["implementation_order"]] == list(range(1, 8))
    assert {item["target"] for item in record["implementation_order"]} == set(EXPECTED_TARGETS)
    assert len(record["reusable_regression_recipe"]) == 12
    assert "newer incompatible state fails closed with a compatibility-specific refusal" in record["reusable_regression_recipe"]
    assert record["safety"]["known_evidence_admitted"] is False


def test_m10_does_not_change_known_evidence_layer():
    # The planning artifact is not an admission. The index legitimately
    # gains one fact per recorded conformance (M11 Semiconductor, M12 KTW,
    # M13 Tablet, M14 Feature Phone, M15 OEM Radar, M17 CTW, M18
    # Smartwatch COM-002, M22 Smartwatch COM-001, M25 Feature Phone
    # COM-001, M28 Tablet COM-001 live proofs); this LF-normalized hash
    # still makes any other edit to the active evidence layer visible.
    # Recomputed at the M28 (live-proof admission) pass.
    assert _sha256(KNOWN) == "e70bcf18d7533a15327539aa710a579f7508bd5c3d048b77fc1cc2161db08ef5"
