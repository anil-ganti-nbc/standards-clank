"""Builds the agent-facing Deployment layer (ratified-index.json,
agent-checklist.json) from the authoritative standards/deployment/*.json
files, mirroring tools/operations_agent_layer.py's design (which itself
mirrors tools/ui_agent_layer.py's and tools/data_ontology_agent_layer.py's)
for the same reasons documented there.

Every structural field (id, title, level, applies_to, version, status,
source_file, ratification_decision) is read directly from the standard
file — never hand-typed. Only two things are authored here, because they
require compression a machine can't do safely: `SUMMARIES` (a short
requirement summary) and `CHECKLIST_ITEMS` (a yes/no implementation
question + what failing it means). Both are keyed by standard id and
verified by tests/test_deployment_agent_layer.py to cover every RATIFIED
id and nothing else, so a summary can never silently go stale.

No known-evidence-index equivalent exists for this domain — there are no
audits/*.md findings against a RATIFIED Deployment standard as of this
writing (no Deployment conformance audit has been performed against any
Clank). If/when a Deployment audit is performed, extend this module the
same way tools/ui_agent_layer.py's build_known_evidence_index() does,
reusing the same audits/*.md structured-block convention, rather than
inventing a new one.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
STANDARDS_DEPLOYMENT_DIR = REPO_ROOT / "standards" / "deployment"
DECISIONS_DIR = REPO_ROOT / "decisions"

DECISION_REF_RE = re.compile(r"decisions/(\d{4}-[a-z0-9-]+\.md)")


def load_deployment_standards() -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(STANDARDS_DEPLOYMENT_DIR.glob("STD-DEPLOY-*.json"))]


def load_ratified_deployment_standards() -> list[dict]:
    return [s for s in load_deployment_standards() if s["status"] == "RATIFIED"]


def extract_ratification_decision(standard: dict) -> str:
    """Pull the decisions/*.md reference out of a standard's notes field —
    same convention tools/ui_agent_layer.py, tools/data_ontology_agent_layer.py,
    and tools/operations_agent_layer.py already enforce fleet-wide."""
    match = DECISION_REF_RE.search(standard.get("notes", ""))
    if not match:
        raise ValueError(f"{standard['id']}: no decisions/*.md reference found in notes")
    return f"decisions/{match.group(1)}"


# Short, human-authored requirement summaries. Must not weaken the MUST
# level or drop a stated trigger/scope-limit from the source standard.
SUMMARIES: dict[str, str] = {
    "STD-DEPLOY-COM-001": "A deployment may be represented as complete only when evidence appropriate to the stated target scope verifies that the declared intended deployment state — artifact/revision by comparable trustworthy provenance, plus deploy-critical configuration and required runtime wiring where correctness depends on them — is materially running. A deploy command exit, repository state, copied files, image build, or restart command alone is not completion evidence, and a non-converged multi-target subset must be represented as partial/in-progress. No Git, immutable images, atomic rollout, or particular transport/tooling is prescribed.",
    "STD-DEPLOY-COM-002": "Where deployed code depends on persistent structured state whose schema/compatibility contract can evolve independently, the Clank must determine compatibility at a barrier before normal incompatible work is accepted, fail closed on known incompatibility, and leave evidence identifying compatibility gating as the refusal reason. Preflight, startup, lazy first-transaction, or platform-enforced barriers all conform; no SQL engine, Alembic, migrations table, rollout order, downtime, or rollback implementation is prescribed, and stateless/schema-less Clanks are trigger-unmet (N/A).",
}

# id -> (question, failure_means). One entry per RATIFIED standard.
CHECKLIST_ITEMS: dict[str, dict[str, str]] = {
    "STD-DEPLOY-COM-001": {
        "question": "When this Clank represents a deployment as complete, can it show evidence — appropriate to the stated target scope — that the intended artifact/revision (and, where correctness depends on them, the deploy-critical configuration and required runtime wiring) is what is materially running, rather than resting on the deploy command's exit, repository state, copied files, an image build, or a restart alone?",
        "failure_means": "A deployment is declared complete because the deploy/build/restart command succeeded or the repository carries the intended state; a partially converged multi-target rollout is represented as complete; or no evidence exists that is capable of comparing the intended and actually running states.",
    },
    "STD-DEPLOY-COM-002": {
        "question": "Where this Clank's code depends on persistent structured state with an independently evolvable compatibility contract, does a barrier before normal work determine code/state compatibility, refuse normal work fail-closed on known incompatibility, and leave evidence identifying compatibility gating as the reason — with process start, database connectivity, or table existence never treated as compatibility proof by itself?",
        "failure_means": "Normal work is admitted while the deployed code and required persistent-state contract are known to be incompatible; connectivity/table existence/create_all completion is treated as compatibility proof; or an incompatible-state refusal happens silently with no evidence identifying the gate as the cause.",
    },
}


def build_ratified_index() -> list[dict]:
    index = []
    for standard in load_ratified_deployment_standards():
        sid = standard["id"]
        if sid not in SUMMARIES:
            raise ValueError(f"{sid}: missing entry in SUMMARIES")
        index.append(
            {
                "id": sid,
                "title": standard["title"],
                "level": standard["level"],
                "applies_to": standard["applies_to"],
                "version": standard["version"],
                "requirement_summary": SUMMARIES[sid],
                "source_file": f"standards/deployment/{sid}.json",
                "ratification_decision": extract_ratification_decision(standard),
            }
        )
    return index


def build_agent_checklist() -> list[dict]:
    checklist = []
    for standard in load_ratified_deployment_standards():
        sid = standard["id"]
        if sid not in CHECKLIST_ITEMS:
            raise ValueError(f"{sid}: missing entry in CHECKLIST_ITEMS")
        item = CHECKLIST_ITEMS[sid]
        checklist.append(
            {
                "standard": sid,
                "question": item["question"],
                "failure_means": item["failure_means"],
            }
        )
    return checklist
