"""Process guards for the Deployment operator ratification closure.

The closure applied the operator's Option A rulings on decisions 0018/0019:
both standards moved PROPOSED -> RATIFIED with normative wording preserved.
No freeze/tag, no third standard, no governance activation.
"""

import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).parent.parent
DEPLOY = REPO / "standards" / "deployment"
PASS1 = REPO / "docs" / "deployment" / "pass1"
PASS3 = REPO / "docs" / "deployment" / "pass3"
DECISIONS = REPO / "decisions"


def _hash(path):
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _standards():
    return {path.stem: json.loads(path.read_text(encoding="utf-8")) for path in DEPLOY.glob("STD-DEPLOY-*.json")}


def test_exactly_two_deployment_standards_all_ratified_v1():
    records = _standards()
    assert set(records) == {"STD-DEPLOY-COM-001", "STD-DEPLOY-COM-002"}
    assert all(record["status"] == "RATIFIED" and record["version"] == 1 for record in records.values())


def test_zero_deployment_standards_remain_proposed():
    assert [record for record in _standards().values() if record["status"] == "PROPOSED"] == []


def test_deployment_readme_reports_closed_domain_state():
    text = (DEPLOY / "README.md").read_text(encoding="utf-8")
    assert "2 `RATIFIED`, 0 `PROPOSED`" in text
    # Pass 4 later concluded no essential contract is missing; the future
    # mechanical freeze remains intentionally separate from ratification.
    assert "READY TO FREEZE DEPLOYMENT STANDARDS V1.0" in text
    assert "not frozen yet" in text


def test_decisions_0018_and_0019_are_accepted_option_a():
    for number, sid in (("0018", "STD-DEPLOY-COM-001"), ("0019", "STD-DEPLOY-COM-002")):
        path = next(DECISIONS.glob(f"{number}-*.md"))
        text = path.read_text(encoding="utf-8")
        assert "Status: Accepted" in text, number
        assert "Option A: RATIFY AS WRITTEN" in text, number
        assert sid in text, number
        # History preserved: declined alternatives remain on record.
        assert "Strongest objection" in text and "Option B" in text, number


def test_ratified_notes_carry_traceability_and_preserve_reused_evidence_disclosure():
    for record in _standards().values():
        assert "RATIFIED 2026-08-31 by operator acceptance of decisions/00" in record["notes"]
        assert "Version 1 text unchanged" in record["notes"]
    reuse_disclosures = 0
    for record in _standards().values():
        for item in record["evidence"]:
            if "REUSED FROM OPERATIONS PASS 0" in item["summary"]:
                reuse_disclosures += 1
    assert reuse_disclosures >= 5, "per-incident reuse disclosure must survive ratification"


def test_pass3_survey_history_intact():
    assert _hash(PASS3 / "ratification-survey.md") == "1835bda7b150839b13e0fe3e6692aac2ed81ea08da1a83ae0cd23924948ca72f"
    text = (PASS3 / "ratification-survey.md").read_text(encoding="utf-8")
    # The survey's own advisory content (recommendations, objections, options) is unchanged.
    for marker in ("RATIFY AS WRITTEN", "Option B", "SUFFICIENT", "reused from Operations Pass 0"):
        assert marker in text
    for path in sorted(PASS1.glob("dossier-*.md")):
        assert "REUSED FROM OPERATIONS PASS 0" in path.read_text(encoding="utf-8")


def test_destructive_state_concern_remains_rehomed():
    text = (PASS1 / "README.md").read_text(encoding="utf-8")
    assert "ADR-0009" in text and "rehomed" in text
    constitution = (REPO / "docs" / "deployment" / "constitution.md").read_text(encoding="utf-8")
    assert "REHOMED" in constitution
    assert "PROPOSED — REVIEWED DRAFT" in constitution
    for record in _standards().values():
        assert record["id"] != "STD-DEPLOY-COM-003"


def test_no_target_or_architecture_modification():
    assert not (REPO / "clank-architecture").exists()
    try:
        result = subprocess.run(
            ["git", "-C", str(REPO), "status", "--porcelain"],
            capture_output=True, text=True, encoding="utf-8", check=True, stdin=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        return  # git unavailable; other guards cover the repo state
    tracked = [line[3:] for line in result.stdout.splitlines() if line.strip()]
    # standards/ui/evidence-*.json are the M36 non-normative UI evidence
    # layer (facts ledger + generated index); the frozen STD-UI-*.json
    # standard files themselves remain outside this allowlist on purpose.
    allowed = (
        "standards/deployment/", "standards/operations/",
        "standards/ui/evidence-facts.json", "standards/ui/evidence-index.json",
        "docs/deployment/", "docs/fleet-wiring.md",
        "docs/project-completion-audit.md", "baselines/deployment-standards-v1.0",
        "audits/", "decisions/", "tests/", "tools/", "scripts/", "profiles/",
    )
    for relative in tracked:
        assert relative.startswith(allowed), relative
