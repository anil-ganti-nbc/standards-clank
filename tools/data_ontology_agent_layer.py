"""Builds the agent-facing Data/Ontology layer (ratified-index.json,
agent-checklist.json) from the authoritative standards/data-ontology/*.json
files, mirroring tools/ui_agent_layer.py's design exactly for the same
reasons documented there.

Every structural field (id, title, level, applies_to, version, status,
source_file, ratification_decision) is read directly from the standard
file — never hand-typed. Only two things are authored here, because they
require compression a machine can't do safely: `SUMMARIES` (a short
requirement summary) and `CHECKLIST_ITEMS` (a yes/no implementation
question + what failing it means). Both are keyed by standard id and
verified by tests/test_data_ontology_agent_layer.py to cover every
RATIFIED id and nothing else, so a summary can never silently go stale.

No known-evidence-index equivalent exists yet for this domain — there are
no audits/*.md findings against a RATIFIED Data/Ontology standard as of
this writing. If/when a Data/Ontology audit is performed, extend this
module the same way tools/ui_agent_layer.py's build_known_evidence_index()
does, reusing the same audits/*.md structured-block convention, rather
than inventing a new one.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
STANDARDS_DATA_ONTOLOGY_DIR = REPO_ROOT / "standards" / "data-ontology"
DECISIONS_DIR = REPO_ROOT / "decisions"

DECISION_REF_RE = re.compile(r"decisions/(\d{4}-[a-z0-9-]+\.md)")


def load_data_ontology_standards() -> list[dict]:
    return [json.loads(p.read_text()) for p in sorted(STANDARDS_DATA_ONTOLOGY_DIR.glob("STD-DATA-*.json"))]


def load_ratified_data_ontology_standards() -> list[dict]:
    return [s for s in load_data_ontology_standards() if s["status"] == "RATIFIED"]


def extract_ratification_decision(standard: dict) -> str:
    """Pull the decisions/*.md reference out of a standard's notes field —
    same convention tools/ui_agent_layer.py and
    tests/test_repository_contracts.py already enforce fleet-wide."""
    match = DECISION_REF_RE.search(standard.get("notes", ""))
    if not match:
        raise ValueError(f"{standard['id']}: no decisions/*.md reference found in notes")
    return f"decisions/{match.group(1)}"


# Short, human-authored requirement summaries. Must not weaken the MUST
# level or drop a stated trigger/scope-limit from the source standard.
SUMMARIES: dict[str, str] = {
    "STD-DATA-COM-001": "Where a Clank derives novelty/alerting/editorial state from its own local history, a continuity break (data loss, restore, re-baseline, collector replacement, region change) must be an explicit, queryable fact distinct from the records themselves, and baseline/bootstrap observations must be distinguishable at read time from ordinary post-continuity ones. No storage mechanism is prescribed.",
    "STD-DATA-COM-002": "Discovery/first-seen time alone never proves real-world novelty. Every default novelty-consuming path (alerts, new-item feeds, editorial queues) — including secondary or derived paths — must include or explicitly inherit a baseline-exclusion predicate as part of its own definition, verifiable by inspecting that definition; post-hoc external filtering or relying on today's clean output as proof does not conform. Editorial freshness, where modeled, stays a separate, optional, family-scoped judgement.",
    "STD-DATA-COM-003": "Default posture must prefer a missed merge to a false merge: insufficient evidence leaves records unresolved rather than forced together, and a candidate-surfacing key alone is never grounds for a committed merge. Any automatic merge must be evidence-gated (on a discriminator present in the records under consideration or the merged record, not world-knowledge), auditable (recording both the justifying evidence and which mechanism/decision-path performed it), and reversible or information-preserving. No identity algorithm is prescribed; cross-Clank identity is out of scope.",
    "STD-DATA-COM-004": "Where a Clank both ingests observations and derives canonical state, observation records, canonical fact/change records, and (where present) operator-decision records must stay distinguishable and separately consumable, never mixed. Every canonical fact/change must trace back to its supporting observations at explanatory granularity; every operator decision must trace to the state it was made against; an inferred value must never be presented as a direct source claim. No tier count, envelope shape, or retention duration is prescribed.",
}

# id -> (question, failure_means). One entry per RATIFIED standard.
CHECKLIST_ITEMS: dict[str, dict[str, str]] = {
    "STD-DATA-COM-001": {
        "question": "If this Clank derives novelty/alerting/editorial state from its own local history, is every continuity break (data loss, restore, re-baseline, collector replacement, region change) represented as an explicit, queryable fact, with baseline/bootstrap observations distinguishable from ordinary ones at read time?",
        "failure_means": "A continuity break leaves no durable trace a downstream reader can query, or relies solely on operator memory / a manually-invoked flag with no dataset-level record — a restore or re-baseline can then silently present as ordinary current history.",
    },
    "STD-DATA-COM-002": {
        "question": "Does every default novelty-asserting path — including secondary or derived ones — include or explicitly inherit a baseline-exclusion predicate as part of its own definition, verifiable by inspection rather than by today's output alone?",
        "failure_means": "A default novelty/alert/new-item view (or a secondary path with the same semantics) can return baseline-tagged records because the exclusion lives only in a caller's convention, a droppable post-hoc filter external to the path, or an assumption about what got written.",
    },
    "STD-DATA-COM-003": {
        "question": "When this Clank merges records from multiple sources into a canonical entity, does insufficient evidence leave them unresolved rather than forced together, and does every committed automatic merge record both its justifying evidence and which mechanism/decision-path performed it, with the pre-merge state reconstructable?",
        "failure_means": "A merge is committed solely on a coarse candidate-surfacing key while a stronger, present discriminator conflicts; an automatic merge has no recorded justification or performing mechanism; or the pre-merge per-source identities are irrecoverably lost after a merge.",
    },
    "STD-DATA-COM-004": {
        "question": "Are observation records, canonical fact/change records, and operator-decision records (where present) kept distinguishable and separately consumable, with every canonical fact traceable to its supporting observations and every inferred value distinguishable from a direct source claim?",
        "failure_means": "A reviewer, alerting system, or operator-facing queue receives unreviewed raw observations mixed into a canonical-change or decision stream, a canonical fact has no path back to supporting evidence, or an inferred/derived value is presented as though a source stated it directly.",
    },
}


def build_ratified_index() -> list[dict]:
    index = []
    for standard in load_ratified_data_ontology_standards():
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
                "source_file": f"standards/data-ontology/{sid}.json",
                "ratification_decision": extract_ratification_decision(standard),
            }
        )
    return index


def build_agent_checklist() -> list[dict]:
    checklist = []
    for standard in load_ratified_data_ontology_standards():
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
