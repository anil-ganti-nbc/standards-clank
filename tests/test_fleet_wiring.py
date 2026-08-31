import json
import subprocess
from pathlib import Path

from tools.fleet_standards_resolver import DOMAINS, audit_plan, load_registry, resolve

ROOT = Path(__file__).resolve().parents[1]

def test_registry_is_unique_and_profiles_are_real():
    registry = load_registry(); clanks = registry["clanks"]
    assert len(clanks) == 9
    assert len({x["id"] for x in clanks}) == len(clanks)
    assert len({x["repository"] for x in clanks}) == len(clanks)
    profiles = {p.stem for p in (ROOT / "profiles").glob("*-based.json")}
    assert {x["primary_profile"] for x in clanks} <= profiles
    assert registry["fact_value_vocabulary"] == ["TRUE", "FALSE", "UNKNOWN"]

def test_resolution_is_frozen_complete_and_unknown_is_not_na():
    result = resolve("watch-clank")
    assert result["baselines"] == DOMAINS
    assert {x["domain"] for x in result["standards"]} == set(DOMAINS)
    assert {x["applicability"] for x in result["standards"]} <= {"APPLIES", "NOT_APPLICABLE", "UNKNOWN"}
    assert next(x for x in result["standards"] if x["id"] == "STD-DEPLOY-COM-001")["applicability"] == "APPLIES"
    assert next(x for x in result["standards"] if x["id"] == "STD-DEPLOY-COM-002")["applicability"] == "APPLIES"
    other = resolve("oem-radar")
    assert next(x for x in other["standards"] if x["id"] == "STD-DEPLOY-COM-002")["applicability"] == "UNKNOWN"
    assert next(x for x in other["standards"] if x["id"] == "STD-UI-NEWS-001")["applicability"] == "NOT_APPLICABLE"

def test_tags_are_present_and_plan_is_deterministic_and_blind():
    expected = {"ui-standards-v1.0": "d11320704aed69a3d8f854c9264b184e392ec80f", "data-ontology-standards-v1.0": "464a8057ea5dc26ef83248a20bafa0be5aa31148", "operations-standards-v1.0": "7100f294a83c30594f2ff9e953f7c9f77a95747f", "deployment-standards-v1.0": "33cc38849180716fd4d06b1356cf70c49d3d41d2"}
    for tag in DOMAINS.values():
        actual = subprocess.run(["git", "rev-parse", f"{tag}^{{}}"], cwd=ROOT, text=True, capture_output=True, check=True, stdin=subprocess.DEVNULL).stdout.strip()
        assert actual == expected[tag]
    first, second = audit_plan("watch-clank"), audit_plan("watch-clank")
    assert first == second and first["items"]
    rendered = json.dumps(first).upper()
    assert "PASS" not in rendered and '"FAIL"' not in rendered and "COMPLIANT" not in rendered
    # Normative text may discuss historical records; the plan must not import
    # historical audit files or target remediation advice.
    assert "AUDITS/" not in rendered and "REMEDIATION BACKLOG" not in rendered
