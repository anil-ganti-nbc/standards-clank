"""M40: Collector UI Design System v1 proposal + fleet gap audit guards."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STD_FILE = ROOT / "standards" / "collector-ui-design" / "STD-CUD-001.json"
EVIDENCE_MD = ROOT / "audits" / "collector-ui-design-evidence-m40-2026-09-04.md"
EVIDENCE_JSON = ROOT / "audits" / "collector-ui-design-evidence-m40-2026-09-04.json"
MANIFEST = ROOT / "baselines" / "ui-standards-v1.0.json"

PROPOSED_SHA_HASH = "aaa38c123d3e3e96d3bb3f1f21adf8487ce1723defdcf8f424af6bc7258e"

EXPECTED_SIX = {
    "smartphone-clank", "smartwatch-clank", "feature-phone-clank",
    "tablet-clank", "watch-clank", "oem-radar",
}
EXPECTED_NON_COLLECTOR = {"chinese-tech-wire", "korean-tech-wire", "semiconductor-intelligence"}


def _std() -> dict:
    return json.loads(STD_FILE.read_text(encoding="utf-8"))


def test_std_cud_001_is_proposed_not_ratified():
    std = _std()
    assert std["status"] == "PROPOSED"
    assert std["version"] == 1
    assert std["domain"] == "collector-ui-design"
    assert std["id"] == "STD-CUD-001"
    assert std["level"] == "MUST"


def test_std_cud_001_applies_to_exactly_six_collector_clanks():
    std = _std()
    # applies_to is empty (profiles don't distinguish collector vs non-collector);
    # the trigger text scopes the standard to the six collector-family Clanks
    assert std["applies_to"] == []
    for clank in EXPECTED_SIX:
        assert clank in std["trigger"] or "collector" in std["trigger"].lower()


def test_std_cud_001_does_not_apply_to_non_collector_clanks():
    std = _std()
    for clank in EXPECTED_NON_COLLECTOR:
        assert clank not in std["applies_to"], (
            f"{clank} must not automatically be in scope"
        )


def test_std_cud_001_covers_required_design_areas():
    std = _std()
    req = std["requirement"].lower()
    for area in (
        "byte-identically", "design_system_version", "text label",
        "clank identity", "empty state", "accent",
        "navigation grammar", "desktop-first", "1080p",
    ):
        assert area in req, f"requirement missing: {area}"


def test_std_cud_001_forbidden_list_covers_anti_patterns():
    std = _std()
    forbidden = [f.lower() for f in std["forbidden"]]
    joined = " ".join(forbidden)
    for anti in (
        "phase-0 scaffold", "generic", "colour alone",
        "empty", "dead-space",
    ):
        assert anti in joined, f"anti-pattern missing: {anti}"


def test_std_cud_001_notes_separate_from_semantic_ui():
    std = _std()
    assert "semantic" in std["notes"].lower()
    assert "not normative" in std["notes"].lower() or "not" in std["notes"].lower()
    # explicitly does not duplicate frozen UI standards
    assert "STD-UI-COM" in std["notes"]


def test_evidence_artifact_records_all_six():
    evidence = json.loads(EVIDENCE_JSON.read_text(encoding="utf-8"))
    targets = evidence["collector_family_evidence"]["targets"]
    assert set(targets) == EXPECTED_SIX
    assert evidence["collector_family_evidence"]["byte_identical"] is True
    assert evidence["collector_family_evidence"]["sha256"].startswith("aaa38c12")


def test_evidence_records_com001_matrix():
    evidence = json.loads(EVIDENCE_JSON.read_text(encoding="utf-8"))
    matrix = evidence["deployment_com_001_matrix"]
    assert set(matrix["confirmed"]) == {
        "watch-clank", "smartwatch-clank", "feature-phone-clank",
        "tablet-clank", "korean-tech-wire",
    }
    assert set(matrix["unresolved"]) == {
        "oem-radar", "semiconductor-intelligence", "chinese-tech-wire",
        "smartphone-clank",
    }


def test_evidence_records_source_drift():
    evidence = json.loads(EVIDENCE_JSON.read_text(encoding="utf-8"))
    drift = evidence["source_drift"]
    assert set(drift["moved_since_m36"]) == EXPECTED_SIX
    assert set(drift["unchanged_since_m36"]) == EXPECTED_NON_COLLECTOR
    assert drift["com002_facts_invalidated"] is False
    assert drift["superseding_pass_required"] is True


def test_evidence_records_remaining_unresolved():
    evidence = json.loads(EVIDENCE_JSON.read_text(encoding="utf-8"))
    remaining = evidence["remaining_unresolved"]
    assert set(remaining["deploy_com_001"]) == {
        "oem-radar", "semiconductor-intelligence", "chinese-tech-wire",
        "smartphone-clank",
    }
    assert "smartphone-clank" in " ".join(remaining["ui_com_011"])
    assert "chinese-tech-wire" in " ".join(remaining["ops_com_003"])


def test_proposal_evidence_md_records_shared_module_hash():
    text = EVIDENCE_MD.read_text(encoding="utf-8")
    assert "aaa38c12" in text
    assert "byte-identical" in text
    assert "collector-ui-v1" in text


def test_proposal_evidence_md_records_gap_audit():
    text = " ".join(EVIDENCE_MD.read_text(encoding="utf-8").split())
    for marker in (
        "LIVE_PROOF_CONFIRMED", "UNRESOLVED", "MOVED", "UNCHANGED",
        "NON-UI", "red-CI", "dcrainmaker",
    ):
        assert marker in text, marker


def test_frozen_ui_tag_unchanged():
    import subprocess
    tag = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "--verify", "--quiet",
         "ui-standards-v1.0^{commit}"],
        capture_output=True, text=True, encoding="utf-8",
        stdin=subprocess.DEVNULL, check=True,
    ).stdout.strip()
    assert tag == "d11320704aed69a3d8f854c9264b184e392ec80f"


def test_frozen_ui_manifest_unchanged():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["status"] == "FROZEN"
    assert manifest["baseline_id"] == "ui-standards-v1.0"
