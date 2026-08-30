"""Builds the agent-facing UI layer (ratified-index.json, agent-checklist.json)
from the authoritative standards/ui/*.json files.

Every structural field (id, title, level, applies_to, version, status,
source_file, ratification_decision) is read directly from the standard
file — never hand-typed. Only two things are authored here, because they
require compression a machine can't do safely without risking exactly the
kind of weakening docs/ui/constitution.md warns against: `SUMMARIES` (a
short requirement summary) and `CHECKLIST_ITEMS` (a yes/no implementation
question + what failing it means). Both are keyed by standard id and
verified by tests/test_ui_agent_layer.py to cover every RATIFIED id and
nothing else, so a summary can never silently go stale if a standard is
added, revised, or reworded without updating this file — the test suite
will fail closed, not pass silently.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
STANDARDS_UI_DIR = REPO_ROOT / "standards" / "ui"
DECISIONS_DIR = REPO_ROOT / "decisions"

DECISION_REF_RE = re.compile(r"decisions/(\d{4}-[a-z0-9-]+\.md)")


def load_ui_standards() -> list[dict]:
    return [json.loads(p.read_text()) for p in sorted(STANDARDS_UI_DIR.glob("STD-UI-*.json"))]


def load_ratified_ui_standards() -> list[dict]:
    return [s for s in load_ui_standards() if s["status"] == "RATIFIED"]


def extract_ratification_decision(standard: dict) -> str:
    """Pull the decisions/*.md reference out of a standard's notes field.
    Reuses the same convention tests/test_repository_contracts.py already
    enforces (every RATIFIED standard's notes must cite a real decision file)."""
    match = DECISION_REF_RE.search(standard.get("notes", ""))
    if not match:
        raise ValueError(f"{standard['id']}: no decisions/*.md reference found in notes")
    return f"decisions/{match.group(1)}"


# Short, human-authored requirement summaries. Must not weaken the MUST/
# SHOULD/MAY level or drop a stated exception/scope-limit from the source
# standard — see docs/ui/constitution.md's own warning against collapsing
# backend requirements into cosmetic UI advice.
SUMMARIES: dict[str, str] = {
    "STD-UI-COM-001": "Loading or launching the GUI must never itself start a collector run; collection requires an explicit operator action, or a mechanism entirely outside the GUI process.",
    "STD-UI-COM-002": "A QC decision must be an atomic, provenance-bearing, append-only record, race-guarded against concurrent double-decisions, and the UI must not present it as committed unless the underlying write actually satisfies that contract.",
    "STD-UI-COM-003": "A decided item must be excluded from the active queue on the very next render, via a read-side filter against the decision record — never by deleting or mutating the live row.",
    "STD-UI-COM-004": "If a GUI exposes a QC queue, it must also expose an operator-visible resolved/QC-history view sourced from the QC archive; a dedicated route or an inline section both satisfy this.",
    "STD-UI-COM-005": "Where a production/experimental maturity tier exists, promotion to production must be an explicit out-of-band config change — never a GUI button, never automatic from runtime metrics.",
    "STD-UI-COM-006": "A bulk 'run all collectors' control must exclude experimental/soak/non-promoted collectors by default; only the production/finalized list may run in bulk.",
    "STD-UI-COM-008": "Source operational health and coverage/output must be expressible as distinct, separately-labeled dimensions; a legitimately quiet source must not read as unhealthy purely from low output.",
    "STD-UI-COM-009": "Where the backend already tracks distinct pipeline stages for a run, the primary run surface must not erase a materially significant stage distinction, and must visibly indicate and directly link to the deeper detail when it exists.",
    "STD-UI-COM-010": "Every timestamp whose meaning could be ambiguous must have its semantic role labeled, and its timezone must be unambiguous — a per-value marker or one clearly stated page-level convention both satisfy this.",
    "STD-UI-COM-011": "Where a delivery mechanism records its own outcome, that outcome must be independently inspectable from discovery/review state; no dedicated delivery page is required, but collapsing distinct outcomes into one ambiguous boolean is not sufficient.",
    "STD-UI-NEWS-001": "A news-family Clank's QC vocabulary must use DUPLICATE as its fourth terminal action (not OUT_OF_STOCK); additional Clank-specific values beyond the fleet-standard four are allowed.",
    "STD-UI-NEWS-002": "A news-family Clank's live editorial intake/review queue must be reachable directly from the default landing surface, or via one obvious action — not buried in navigation.",
}

# id -> (question, failure_means). One entry per RATIFIED standard.
CHECKLIST_ITEMS: dict[str, dict[str, str]] = {
    "STD-UI-COM-001": {
        "question": "Does opening or launching the GUI avoid starting any collector run by itself?",
        "failure_means": "A GET route, app-startup hook, or lifespan event triggers collection with no explicit operator action.",
    },
    "STD-UI-COM-002": {
        "question": "Is every QC decision written as an atomic, provenance-bearing, race-guarded record, and does the UI only show it as committed once that write is confirmed?",
        "failure_means": "A QC action can appear successful (toast, checkmark, queue removal) before or without a confirmed atomic/race-safe write, or a concurrent double-decision can silently duplicate, crash, or lose data.",
    },
    "STD-UI-COM-003": {
        "question": "Does a just-decided item disappear from the active queue on the very next render, via a read-side filter rather than deleting or mutating the live row?",
        "failure_means": "A decided item still appears in the active queue, or its removal depends on deleting/flagging the live record instead of a read-side exclusion against the decision record.",
    },
    "STD-UI-COM-004": {
        "question": "If this Clank has a QC queue, is there a way to review recently-made QC decisions, sourced from the QC archive rather than reconstructed from the live table?",
        "failure_means": "A QC queue exists with no way to see recently-decided items short of querying the database directly.",
    },
    "STD-UI-COM-005": {
        "question": "If this Clank has a production/experimental maturity tier, is promotion an explicit config-file change rather than a GUI action or an automatic metric-driven promotion?",
        "failure_means": "A 'promote to production' control exists in the GUI, or a collector auto-promotes after N successful runs with no human action.",
    },
    "STD-UI-COM-006": {
        "question": "Does the bulk 'run all' control exclude experimental/non-production collectors by default?",
        "failure_means": "Clicking 'run all' also runs an experimental/soak/non-promoted collector with no explicit override.",
    },
    "STD-UI-COM-008": {
        "question": "Can an operator read a source's operational health as a distinct, separately-labeled value from its coverage/output, without a legitimately quiet source misreading as unhealthy?",
        "failure_means": "Health and coverage are blended into one score/badge with no way to tell which drove the result, or a source with zero new items renders identically to a failing one.",
    },
    "STD-UI-COM-009": {
        "question": "If the backend tracks distinct pipeline stages for a run, can an operator reach that detail directly and discoverably from the primary run surface?",
        "failure_means": "Stage-level detail exists in the backend or on some page, but the primary run surface gives no visible indication it exists and no direct link to it.",
    },
    "STD-UI-COM-010": {
        "question": "Is every displayed timestamp's semantic role labeled, and is its timezone unambiguous (a per-value marker or one stated page-wide convention)?",
        "failure_means": "A timestamp's meaning (published vs. discovered vs. decided, etc.) can't be determined from the UI, or its timezone is silently browser-local/unstated with no convention declared.",
    },
    "STD-UI-COM-011": {
        "question": "If this Clank delivers to an external channel, can an operator see the distinct delivery outcome (sent/failed/pending/suppressed) independently from discovery/review state?",
        "failure_means": "Delivery outcomes are computed/persisted but never shown in the GUI, or collapsed into a single boolean that can't distinguish failed/suppressed from never-attempted.",
    },
    "STD-UI-NEWS-001": {
        "question": "For a news-family Clank, does the QC vocabulary include DUPLICATE as its fourth terminal action, not OUT_OF_STOCK?",
        "failure_means": "A news-family Clank's QC vocabulary uses OUT_OF_STOCK, or has no way to mark a lead as not-novel/already-covered.",
    },
    "STD-UI-NEWS-002": {
        "question": "For a news-family Clank, is the live intake/review queue exposed directly on the default landing surface, or reachable via one single obvious action?",
        "failure_means": "The default landing view is a stats/health page and reaching the review queue requires searching through navigation.",
    },
}


def build_ratified_index() -> list[dict]:
    index = []
    for standard in load_ratified_ui_standards():
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
                "source_file": f"standards/ui/{sid}.json",
                "ratification_decision": extract_ratification_decision(standard),
            }
        )
    return index


def build_agent_checklist() -> list[dict]:
    checklist = []
    for standard in load_ratified_ui_standards():
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
