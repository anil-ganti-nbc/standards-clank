from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "audits" / "watch-clank-cross-domain-2026-08-31-m2-remediation-plan.md"

def test_m2_plan_is_bounded_and_references_m1_exactly():
    text = PLAN.read_text()
    for marker in ("WC-M1-001", "fbf228f7ecccf2de4119fca29f8344aff9c49441", "STD-OPS-COM-003", "STD-DEPLOY-COM-001", "ENVIRONMENT_SETUP_ONLY"):
        assert marker in text
    assert text.count("**Preferred.") == 1
    assert "no Watch code, service, scheduler, database" in text

def test_m2_plan_has_two_options_and_no_known_evidence_admission():
    text = PLAN.read_text()
    assert "Hold an OS/kernel advisory file-lock handle" in text
    assert "database-session-scoped lock" in text
    assert "known-evidence admission" in text
