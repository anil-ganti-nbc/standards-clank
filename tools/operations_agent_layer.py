"""Builds the agent-facing Operations layer (ratified-index.json,
agent-checklist.json) from the authoritative standards/operations/*.json
files, mirroring tools/ui_agent_layer.py's and
tools/data_ontology_agent_layer.py's design exactly for the same reasons
documented there.

Every structural field (id, title, level, applies_to, version, status,
source_file, ratification_decision) is read directly from the standard
file — never hand-typed. Only two things are authored here, because they
require compression a machine can't do safely: `SUMMARIES` (a short
requirement summary) and `CHECKLIST_ITEMS` (a yes/no implementation
question + what failing it means). Both are keyed by standard id and
verified by tests/test_operations_agent_layer.py to cover every RATIFIED
id and nothing else, so a summary can never silently go stale.

No known-evidence-index equivalent exists yet for this domain — there are
no audits/*.md findings against a RATIFIED Operations standard as of this
writing (no Operations conformance audit has been performed against any
Clank). If/when an Operations audit is performed, extend this module the
same way tools/ui_agent_layer.py's build_known_evidence_index() does,
reusing the same audits/*.md structured-block convention, rather than
inventing a new one.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
STANDARDS_OPERATIONS_DIR = REPO_ROOT / "standards" / "operations"
DECISIONS_DIR = REPO_ROOT / "decisions"

DECISION_REF_RE = re.compile(r"decisions/(\d{4}-[a-z0-9-]+\.md)")


def load_operations_standards() -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(STANDARDS_OPERATIONS_DIR.glob("STD-OPS-*.json"))]


def load_ratified_operations_standards() -> list[dict]:
    return [s for s in load_operations_standards() if s["status"] == "RATIFIED"]


def extract_ratification_decision(standard: dict) -> str:
    """Pull the decisions/*.md reference out of a standard's notes field —
    same convention tools/ui_agent_layer.py and
    tools/data_ontology_agent_layer.py already enforce fleet-wide."""
    match = DECISION_REF_RE.search(standard.get("notes", ""))
    if not match:
        raise ValueError(f"{standard['id']}: no decisions/*.md reference found in notes")
    return f"decisions/{match.group(1)}"


# Short, human-authored requirement summaries. Must not weaken the MUST
# level or drop a stated trigger/scope-limit from the source standard.
SUMMARIES: dict[str, str] = {
    "STD-OPS-COM-001": "Where a Clank fires collection from any trigger mechanism, it must record in its own store that an invocation occurred and what outcome it produced — neither inferred from scheduler-reported state ('enabled', 'next run', 'exit 0'). A legitimately empty due-gated cycle must be an explicit recorded no-work outcome, never an absence indistinguishable from a materialization failure. No scheduler technology, run-table schema, or stage vocabulary is prescribed.",
    "STD-OPS-COM-002": "Execution/trigger-liveness health and output/yield health must remain independently representable — a job exiting successfully while producing nothing useful is its own state, never silently read as ordinary healthy. Where a source's output is meaningful, zero output must be classifiable as healthy, anomalous, or unknown according to that source's own expected behavior, never silently collapsed into undifferentiated health. No field count, naming convention, or score formula is prescribed.",
    "STD-OPS-COM-003": "Promotion/soak qualification evidence must be structurally verifiable from a Clank's own stored data: trigger provenance (natural/manual/deploy/recovery) where it affects qualification; material-change soak-clock resets recorded with identity and reason; incidents/host moves/manual recovery never silently resetting or silently counting as clean evidence; and multi-gate promotion divergence detectable and failing closed. Cycle counts, retention durations, and maturity-state-machine shape are explicitly per-Clank policy.",
    "STD-OPS-COM-004": "An exclusivity/ownership marker's validity must be determinable from state the granting authority itself observes, never inferred from a reusable or context-ambiguous identifier (PID, hostname). Reclaiming, honoring, or acting on a marker must rest on grantor-observable proof of death/expiry — never bare-identifier inference. OS advisory locks, database session locks, leases, kernel handles, and fencing tokens all conform; only bare-identifier reclaim is forbidden.",
}

# id -> (question, failure_means). One entry per RATIFIED standard.
CHECKLIST_ITEMS: dict[str, dict[str, str]] = {
    "STD-OPS-COM-001": {
        "question": "For any trigger firing, can a downstream reader determine — from this Clank's own stored data, independent of the scheduler — that an invocation occurred and what outcome it produced, with a legitimately empty due-gated cycle recorded as an explicit no-work outcome rather than left as an absence?",
        "failure_means": "Scheduler-reported state ('enabled', 'next run', 'exit 0') is presented as proof a cycle ran or succeeded; a legitimately empty cycle is indistinguishable from a materialization failure; or a second, forgotten trigger source can fire against the same work with no independently-visible invocation record to catch it.",
    },
    "STD-OPS-COM-002": {
        "question": "Are execution/trigger-liveness health and output/yield health kept independently representable, such that a run that executed successfully but produced nothing is distinguishable from ordinary healthy operation, and zero output is classified according to that source's own expected behavior rather than collapsed into a single undifferentiated status?",
        "failure_means": "A successful scheduler invocation or process exit code is presented as proof of output/yield health; a source silently producing nothing reads as healthy with no distinguishing signal; or an unexpected zero-output drop is not classifiable as a health concern distinct from ordinary operation.",
    },
    "STD-OPS-COM-003": {
        "question": "Wherever this Clank's promotion/soak decisions depend on trigger provenance, material-change resets, incident history, or multi-gate agreement, is that evidence recoverable from stored data rather than asserted in documentation or memory, with interventions distinguishable-but-not-forbidden and gate divergence detectable and failing closed?",
        "failure_means": "A manual or deploy-verification run is indistinguishable from natural-cadence qualification evidence; a soak-clock reset happens with no recorded identity/reason; an incident or manual recovery silently resets or silently counts as clean evidence; or a source is promoted through one gate while a second, independently-maintained gate silently disagrees.",
    },
    "STD-OPS-COM-004": {
        "question": "Where this Clank uses an exclusivity/ownership marker capable of outliving or being interpreted across process/execution-context boundaries, is its validity determined from state the granting authority itself observes, rather than inferred from a reusable identifier such as a bare PID or hostname?",
        "failure_means": "A marker is reclaimed as stale, honored as live, or acted upon (including terminating the process it identifies) based solely on a PID, hostname, or similarly ambiguous identifier whose liveness/ownership the validating context cannot structurally prove.",
    },
}


def build_ratified_index() -> list[dict]:
    index = []
    for standard in load_ratified_operations_standards():
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
                "source_file": f"standards/operations/{sid}.json",
                "ratification_decision": extract_ratification_decision(standard),
            }
        )
    return index


def build_agent_checklist() -> list[dict]:
    checklist = []
    for standard in load_ratified_operations_standards():
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
