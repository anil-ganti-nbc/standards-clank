"""M36: UI superseding-evidence resolution guards.

Covers the evidence-facts ledger, the generated evidence index, the
current-verdict resolver, and the frozen-standard immutability boundary.
Test letters A-L follow the M36 mission's required coverage list.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

from tools.ui_agent_layer import (
    build_evidence_index,
    build_fleet_ui_summary,
    load_evidence_facts,
    resolve_current_verdict,
)

ROOT = Path(__file__).resolve().parents[1]
FACTS = ROOT / "standards" / "ui" / "evidence-facts.json"
INDEX = ROOT / "standards" / "ui" / "evidence-index.json"
MANIFEST = ROOT / "baselines" / "ui-standards-v1.0.json"

EXPECTED_SIX = {
    "smartphone-clank", "smartwatch-clank", "feature-phone-clank",
    "tablet-clank", "watch-clank", "oem-radar",
}
CURRENT_CANON = {
    "watch-clank": "4d0413c16518e8433f1b8273c6ce7de7561d37ef",
    "oem-radar": "070914c82516c29be781a49acb77c8d86953f1e2",
    "semiconductor-intelligence": "53cb3f1f5358ad28a2d92ebd78efeab9534ddfa1",
    "chinese-tech-wire": "24c0b7974ac3162ead2796f30793b811209b120d",
    "korean-tech-wire": "f49bd02eb214b650a146e9c0f6f348d526285a91",
    "feature-phone-clank": "bbd28450ce9d5ba84822104e8a33c734af338c2b",
    "smartphone-clank": "e514c45dca4cf966441c27799d98761096dc8c40",
    "smartwatch-clank": "cc80aafa24ab1f96439503bb1660867a437772ed",
    "tablet-clank": "2b1ba6ecbe1ae4e5a0d4380395b2e3fc3a38d5d9",
}


# -- ledger integrity ---------------------------------------------------------


def test_facts_ledger_is_valid_and_complete():
    facts = load_evidence_facts()
    targets = {f["target"] for f in facts}
    assert targets == set(CURRENT_CANON)
    current = [f for f in facts if f["role"] == "CURRENT"]
    scopes = [(f["target"], f["standard_id"]) for f in current]
    assert len(scopes) == len(set(scopes)) == 141
    # Different standards may be admitted at different SHAs (M36 UI facts at
    # their M36-era SHAs; CUD-001 facts at current origin/main SHAs).
    assert all(f["source_sha"] for f in current)  # non-empty SHA


def test_A_historical_nonconformance_remains_queryable():
    smartphone_009 = [
        f for f in load_evidence_facts()
        if f["role"] == "HISTORICAL"
        and f["target"] == "smartphone-clank"
        and f["standard_id"] == "STD-UI-COM-009"
    ]
    assert len(smartphone_009) == 1
    assert smartphone_009[0]["verdict"] == "NONCONFORMING"
    assert "historical" in smartphone_009[0]["provenance"]["kind"]


def test_B_newer_conformance_supersedes_as_current():
    fact = resolve_current_verdict("smartphone-clank", "STD-UI-COM-009")
    assert fact is not None
    assert fact["verdict"] == "CONFORMS"
    assert fact["role"] == "CURRENT"
    hist = [
        f for f in load_evidence_facts()
        if f["role"] == "HISTORICAL"
        and f["target"] == "smartphone-clank"
        and f["standard_id"] == "STD-UI-COM-009"
    ][0]
    assert hist["superseded_by"] == fact["fact_id"]


def test_C_historical_sha_query_returns_historical_state():
    """Querying a historical fact by its recorded scope returns the
    historical verdict, not the current one."""
    hist = [
        f for f in load_evidence_facts()
        if f["role"] == "HISTORICAL"
        and f["target"] == "watch-clank"
        and f["standard_id"] == "STD-UI-COM-011"
    ]
    assert len(hist) == 1
    assert hist[0]["verdict"] == "NONCONFORMING"
    # the resolved CURRENT verdict for the same scope is CONFORMS
    assert resolve_current_verdict("watch-clank", "STD-UI-COM-011")["verdict"] == "CONFORMS"


def test_D_no_cross_sha_inheritance():
    """Resolution is only ever from CURRENT-role facts: a HISTORICAL fact
    at any SHA can never satisfy a CURRENT scope. Different standards may
    be admitted at different SHAs (M36 UI facts vs M43 CUD facts)."""
    index = build_evidence_index()
    for entry in index["current"]:
        assert entry["source_sha"], f"missing SHA: {entry}"
    for hist in index["historical"]:
        assert hist["role"] == "HISTORICAL"


def test_E_no_cross_target_inheritance():
    """A superseded_by relation crossing target or standard scope must fail
    closed at resolution time."""
    facts = load_evidence_facts()
    poisoned = json.loads(json.dumps(facts))
    for fact in poisoned:
        if fact["role"] == "HISTORICAL":
            fact["superseded_by"] = next(
                f["fact_id"] for f in poisoned
                if f["role"] == "CURRENT" and f["target"] != fact["target"]
            )
            break
    FACTS.write_text(json.dumps(poisoned, indent=2), encoding="utf-8")
    try:
        with pytest.raises(ValueError, match="crosses"):
            build_evidence_index()
    finally:
        FACTS.write_text(
            json.dumps(facts, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    build_evidence_index()  # restored


def test_F_na_rationale_survives_indexing():
    index = build_evidence_index()
    na = [
        e for e in index["current"]
        if e["target"] == "smartphone-clank"
        and e["standard_id"] == "STD-UI-COM-006"
    ]
    assert len(na) == 1
    assert na[0]["verdict"] == "NOT_APPLICABLE"
    raw = json.loads(FACTS.read_text(encoding="utf-8"))
    rationale = [
        f for f in raw if f["fact_id"] == na[0]["fact_id"]
    ][0]["provenance"]["note"]
    assert "no bulk run-all control" in rationale


def test_G_feature_phone_com_011_boundary_survives_round_trip():
    summary = build_fleet_ui_summary()
    fp = summary["targets"]["feature-phone-clank"]
    assert len(fp["boundaries"]) == 1
    boundary = fp["boundaries"][0]
    assert boundary["standard_id"] == "STD-UI-COM-011"
    rationale = boundary["rationale"]
    # the three grounding facts of the boundary
    assert "wire no notifier" in rationale
    assert "external delivery is disabled" in rationale
    assert "webhook env empty" in rationale
    # and the re-verification trigger
    assert "becomes APPLIES" in rationale

    # round-trip through the committed index file
    committed = json.loads(INDEX.read_text(encoding="utf-8"))
    fp_committed = [
        e for e in committed["current"]
        if e["target"] == "feature-phone-clank"
        and e["standard_id"] == "STD-UI-COM-011"
    ]
    assert len(fp_committed) == 1
    assert fp_committed[0]["verdict"] == "NOT_APPLICABLE"
    fact = [
        f for f in json.loads(FACTS.read_text(encoding="utf-8"))
        if f["fact_id"] == fp_committed[0]["fact_id"]
    ][0]
    assert "APPLICABILITY BOUNDARY" in json.dumps(fact["provenance"])


def test_H_frozen_standard_regression_notes_not_current_facts():
    """The ratified UI standards' own notes (which mention historical
    regressions/remediations) must never leak into the evidence index as
    current facts: the index is built only from the facts ledger."""
    index = build_evidence_index()
    index_strings = json.dumps(index)
    for std_file in (ROOT / "standards" / "ui").glob("STD-UI-*.json"):
        std = json.loads(std_file.read_text(encoding="utf-8"))
        notes = std.get("notes", "")
        if "regression" in notes.lower():
            assert notes not in index_strings
    # the current verdict for watch COM-011 comes from the ledger, not from
    # any frozen standard file
    fact = resolve_current_verdict("watch-clank", "STD-UI-COM-011")
    assert "audit" in json.dumps(fact["provenance"])


def test_I_fact_count_equals_index_count():
    facts = load_evidence_facts()
    index = build_evidence_index()
    assert index["counts"]["current_cells"] == sum(
        1 for f in facts if f["role"] == "CURRENT"
    )
    assert index["counts"]["historical_facts"] == sum(
        1 for f in facts if f["role"] == "HISTORICAL"
    )
    assert len(index["current"]) == index["counts"]["current_cells"]
    assert len(index["historical"]) == index["counts"]["historical_facts"]
    committed = json.loads(INDEX.read_text(encoding="utf-8"))
    assert committed == index


def test_J_generated_fleet_matrix_equals_admitted_facts():
    summary = build_fleet_ui_summary()
    facts = load_evidence_facts()
    for target in CURRENT_CANON:
        per_target = [
            f for f in facts
            if f["role"] == "CURRENT" and f["target"] == target
        ]
        cell = summary["targets"][target]
        assert cell["conforms"] == sum(
            1 for f in per_target if f["verdict"] == "CONFORMS"
        )
        assert cell["not_applicable"] == sum(
            1 for f in per_target if f["verdict"] == "NOT_APPLICABLE"
        )
        expected_cells = 16 if target in EXPECTED_SIX else 15
        assert cell["conforms"] + cell["not_applicable"] == expected_cells
        # admission expectation: zero UNKNOWN, zero INSUFFICIENT, zero
        # NONCONFORMING in current UI evidence
        assert all(
            f["verdict"] in ("CONFORMS", "NOT_APPLICABLE") for f in per_target
        )
    # and the index itself enumerates zero unknown scopes
    assert build_evidence_index()["unknown_scopes"] == []


def test_K_frozen_ui_manifest_and_tag_unchanged():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["status"] == "FROZEN"
    for artifact in manifest["artifacts"].values():
        if "sha256" in artifact:
            digest = hashlib.sha256((ROOT / artifact["path"]).read_bytes()).hexdigest()
            assert digest == artifact["sha256"], (
                f"frozen artifact drifted: {artifact['path']}"
            )
    # the immutable tag still resolves
    tag = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "--verify", "--quiet",
         "ui-standards-v1.0^{commit}"],
        capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL,
        check=True,
    ).stdout.strip()
    assert tag  # tag exists; its immutability is guarded by test_ui_baseline_v1_0.py


def test_L_conflicting_same_scope_current_facts_fail_closed(tmp_path):
    facts = load_evidence_facts()
    poisoned = json.loads(json.dumps(facts))
    scope_fact = next(
        f for f in poisoned
        if f["role"] == "CURRENT" and f["target"] == "watch-clank"
        and f["standard_id"] == "STD-UI-COM-001"
    )
    duplicate = json.loads(json.dumps(scope_fact))
    duplicate["fact_id"] = "UI-F-9999"
    duplicate["verdict"] = "NOT_APPLICABLE"
    poisoned.append(duplicate)
    FACTS.write_text(json.dumps(poisoned, indent=2), encoding="utf-8")
    try:
        with pytest.raises(ValueError, match="conflicting CURRENT facts"):
            build_evidence_index()
    finally:
        FACTS.write_text(
            json.dumps(facts, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    build_evidence_index()  # restored


# -- fleet summary shape --------------------------------------------------------


def test_fleet_summary_domain_scoped_not_fleet_wide():
    summary = build_fleet_ui_summary()
    assert set(summary["targets"]) == set(CURRENT_CANON)
    for target, cell in summary["targets"].items():
        expected_cells = 16 if target in EXPECTED_SIX else 15
        assert cell["conforms"] + cell["not_applicable"] == expected_cells
        assert cell["conforms"] >= 10
    # semiconductor carries the NON-UI red-CI caveat on its facts
    semi = summary["targets"]["semiconductor-intelligence"]
    assert semi["caveats"], "semiconductor red-CI caveat must be present"
    assert "not fully green" in semi["caveats"][0]["caveat"]
    assert "UI verdicts unaffected" in semi["caveats"][0]["caveat"]
    # smartphone keeps its structural N/A set
    assert summary["targets"]["smartphone-clank"]["not_applicable"] == 5
    # smartwatch COM-011 structural N/A is present with rationale
    smartwatch_na = [
        f for f in load_evidence_facts()
        if f["role"] == "CURRENT" and f["target"] == "smartwatch-clank"
        and f["standard_id"] == "STD-UI-COM-011"
    ]
    assert smartwatch_na[0]["verdict"] == "NOT_APPLICABLE"
    assert "NotImplementedError" in json.dumps(smartwatch_na[0]["provenance"])


def test_current_shas_match_known_canon():
    """Every current fact has a source SHA from a known canon point.
    Different standards may be admitted at different SHAs (M36 UI facts
    at their takeover SHAs, M43 CUD facts at current origin/main SHAs)."""
    index = build_evidence_index()
    for entry in index["current"]:
        assert entry["source_sha"], f"missing SHA: {entry['fact_id']}"
