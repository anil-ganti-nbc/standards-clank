"""M40: Collector UI Design System v1 proposal + fleet gap audit guards.

Tests are split into:
- NORMATIVE CONTRACT TESTS: assert what STD-CUD-001 actually requires
- REFERENCE IMPLEMENTATION CONSISTENCY TESTS: assert properties of the
  six current implementations (evidence, not requirements)
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
STD_FILE = ROOT / "standards" / "collector-ui-design" / "STD-CUD-001.json"
EVIDENCE_MD = ROOT / "audits" / "collector-ui-design-evidence-m40-2026-09-04.md"
EVIDENCE_JSON = ROOT / "audits" / "collector-ui-design-evidence-m40-2026-09-04.json"
MANIFEST = ROOT / "baselines" / "ui-standards-v1.0.json"

CURRENT_SIX = {
    "smartphone-clank", "smartwatch-clank", "feature-phone-clank",
    "tablet-clank", "watch-clank", "oem-radar",
}
CURRENT_NON_COLLECTOR = {"chinese-tech-wire", "korean-tech-wire", "semiconductor-intelligence"}


def _std() -> dict:
    return json.loads(STD_FILE.read_text(encoding="utf-8"))


# =====================================================================
# NORMATIVE CONTRACT TESTS
# These assert what STD-CUD-001 requires of any conforming implementation.
# =====================================================================


class TestNormativeContract:
    def test_status_is_ratified(self):
        std = _std()
        assert std["status"] == "RATIFIED"
        assert std["version"] == 1
        assert std["domain"] == "collector-ui-design"
        assert std["id"] == "STD-CUD-001"
        assert std["level"] == "MUST"

    def test_applies_to_six_collector_clanks_via_trigger(self):
        std = _std()
        assert std["applies_to"] == []
        for clank in CURRENT_SIX:
            assert "collector" in std["trigger"].lower()
        for clank in CURRENT_NON_COLLECTOR:
            assert clank not in std["trigger"]

    def test_requirement_conforms_to_design_system_profile(self):
        req = _std()["requirement"].lower()
        assert "design system profile" in req
        assert "design-system version" in req

    def test_requirement_does_not_demand_byte_identity(self):
        req = _std()["requirement"].lower()
        assert "byte-identically" not in req
        assert "byte-identical" not in req

    def test_requirement_does_not_demand_accent_only_override(self):
        req = _std()["requirement"].lower()
        assert "only visual token" not in req
        assert "only css custom property divergence" not in req

    def test_requirement_permits_domain_specific_adaptations(self):
        req = _std()["requirement"].lower()
        assert "domain-specific visual adaptations" in req
        for preserved in (
            "family recognisability", "navigation grammar",
            "status semantics", "accessibility",
        ):
            assert preserved in req

    def test_requirement_guarantees_status_text_carrying(self):
        req = _std()["requirement"].lower()
        assert "text label" in req
        assert "colour is supplementary" in req

    def test_requirement_guarantees_full_clank_identity(self):
        req = _std()["requirement"].lower()
        assert "full clank identity" in req

    def test_requirement_guarantees_meaningful_empty_states(self):
        req = _std()["requirement"].lower()
        assert "meaningful empty states" in req

    def test_requirement_guarantees_navigation_grammar(self):
        req = _std()["requirement"].lower()
        assert "navigation grammar" in req

    def test_requirement_guarantees_desktop_layout(self):
        req = _std()["requirement"].lower()
        assert "1080p" in req and "1440p" in req

    def test_requirement_guarantees_gui_load_side_effect_free(self):
        req = _std()["requirement"].lower()
        assert "gui load must remain side-effect free" in req

    def test_requirement_requires_explicit_intent_for_collection(self):
        req = _std()["requirement"].lower()
        assert "explicit operator intent" in req
        assert "canonical execution/locking/state path" in req

    def test_requirement_permits_readonly_gui(self):
        req = _std()["requirement"].lower()
        assert "read-only gui is acceptable" in req

    def test_requirement_prohibits_readonly_scaffold_masquerade(self):
        req = _std()["requirement"].lower()
        assert "must not masquerade as a finished interactive operator ui" in req

    def test_forbidden_covers_anti_patterns(self):
        std = _std()
        forbidden = " ".join(f.lower() for f in std["forbidden"])
        for anti in (
            "phase-0 scaffold", "generic", "colour alone",
            "empty", "dead-space", "side effect of gui load",
            "read-only scaffold",
        ):
            assert anti in forbidden, f"anti-pattern missing: {anti}"

    def test_forbidden_does_not_prohibit_domain_adaptations(self):
        forbidden = " ".join(f.lower() for f in _std()["forbidden"])
        assert "accent" not in forbidden
        assert "byte-identical" not in forbidden
        assert "domain-specific" not in forbidden

    def test_acceptance_preserves_operator_workflow_clarity(self):
        std = _std()
        acceptance = " ".join(a.lower() for a in std["acceptance"])
        assert "explicit operator intent" in acceptance
        assert "canonical execution/locking/state path" in acceptance
        assert "side effect" in acceptance

    def test_acceptance_preserves_domain_adaptation_permission(self):
        acceptance = " ".join(a.lower() for a in _std()["acceptance"])
        assert "domain-specific visual adaptations" in acceptance


# =====================================================================
# REFERENCE IMPLEMENTATION CONSISTENCY TESTS
# These assert properties of the six current implementations.
# They are EVIDENCE for the proposal, not requirements of STD-CUD-001.
# =====================================================================


class TestReferenceImplementationConsistency:
    def test_all_six_current_shas_recorded_in_evidence(self):
        evidence = json.loads(EVIDENCE_JSON.read_text(encoding="utf-8"))
        targets = evidence["collector_family_evidence"]["targets"]
        assert set(targets) == CURRENT_SIX

    def test_current_implementations_are_byte_identical(self):
        """REFERENCE EVIDENCE: the six current implementations happen to be
        byte-identical. This is a property of the current implementation
        wave, not a requirement of STD-CUD-001. Future implementations may
        use different architectures."""
        evidence = json.loads(EVIDENCE_JSON.read_text(encoding="utf-8"))
        assert evidence["collector_family_evidence"]["byte_identical"] is True
        assert evidence["collector_family_evidence"]["sha256"].startswith("aaa38c12")

    def test_current_implementations_use_accent_only_override(self):
        """REFERENCE EVIDENCE: the current implementations override only the
        accent tokens. Future implementations may adapt other tokens where
        domain-specific visual adaptations preserve the family invariants."""
        evidence = json.loads(EVIDENCE_JSON.read_text(encoding="utf-8"))
        assert evidence["collector_family_evidence"]["per_clank_accent_only_override"] is True

    def test_current_implementations_report_collector_ui_v1(self):
        evidence = json.loads(EVIDENCE_JSON.read_text(encoding="utf-8"))
        assert evidence["collector_family_evidence"]["design_system_version"] == "collector-ui-v1"


# =====================================================================
# FROZEN INTEGRITY
# =====================================================================


class TestFrozenIntegrity:
    def test_frozen_ui_tag_unchanged(self):
        tag = subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", "--verify", "--quiet",
             "ui-standards-v1.0^{commit}"],
            capture_output=True, text=True, encoding="utf-8",
            stdin=subprocess.DEVNULL, check=True,
        ).stdout.strip()
        assert tag == "d11320704aed69a3d8f854c9264b184e392ec80f"

    def test_frozen_ui_manifest_unchanged(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        assert manifest["status"] == "FROZEN"
        assert manifest["baseline_id"] == "ui-standards-v1.0"


# =====================================================================
# FLEET GAP AUDIT EVIDENCE
# =====================================================================


class TestFleetGapAudit:
    def test_evidence_records_com001_matrix(self):
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

    def test_evidence_records_source_drift(self):
        evidence = json.loads(EVIDENCE_JSON.read_text(encoding="utf-8"))
        drift = evidence["source_drift"]
        assert set(drift["moved_since_m36"]) == CURRENT_SIX
        assert set(drift["unchanged_since_m36"]) == CURRENT_NON_COLLECTOR
        assert drift["com002_facts_invalidated"] is False
        assert drift["superseding_pass_required"] is True

    def test_evidence_records_remaining_unresolved(self):
        evidence = json.loads(EVIDENCE_JSON.read_text(encoding="utf-8"))
        remaining = evidence["remaining_unresolved"]
        assert set(remaining["deploy_com_001"]) == {
            "oem-radar", "semiconductor-intelligence", "chinese-tech-wire",
            "smartphone-clank",
        }
        assert "smartphone-clank" in " ".join(remaining["ui_com_011"])
        assert "chinese-tech-wire" in " ".join(remaining["ops_com_003"])

    def test_proposal_evidence_md_records_shared_module_hash(self):
        text = EVIDENCE_MD.read_text(encoding="utf-8")
        assert "aaa38c12" in text
        assert "byte-identical" in text
        assert "collector-ui-v1" in text

    def test_proposal_evidence_md_records_gap_audit(self):
        text = " ".join(EVIDENCE_MD.read_text(encoding="utf-8").split())
        for marker in (
            "LIVE_PROOF_CONFIRMED", "UNRESOLVED", "MOVED", "UNCHANGED",
            "NON-UI", "red-CI", "dcrainmaker",
        ):
            assert marker in text, marker
