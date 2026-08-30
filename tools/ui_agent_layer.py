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
AUDITS_DIR = REPO_ROOT / "audits"

DECISION_REF_RE = re.compile(r"decisions/(\d{4}-[a-z0-9-]+\.md)")
AUDIT_JSON_BLOCK_RE = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)


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
    "STD-UI-COM-002": "A QC decision must be an atomic, provenance-bearing, append-only record, race-guarded against concurrent double-decisions, and the UI must not present it as committed unless the underlying write actually satisfies that contract. The decision contract applies to the operator decision path wherever it lives — GUI, CLI, or other operator tooling — not only where a GUI control exists (decisions/0005).",
    "STD-UI-COM-003": "A decided item must be excluded from the active queue on the very next render, via a read-side filter against the decision record — never by deleting or mutating the live row.",
    "STD-UI-COM-004": "If a GUI exposes a QC queue, it must also expose an operator-visible resolved/QC-history view sourced from the QC archive; a dedicated route or an inline section both satisfy this.",
    "STD-UI-COM-005": "Where a production/experimental maturity tier exists, promotion to production must be an explicit out-of-band config change — never a GUI button, never automatic from runtime metrics.",
    "STD-UI-COM-006": "A bulk 'run all collectors' control must exclude experimental/soak/non-promoted collectors by default; only the production/finalized list may run in bulk.",
    "STD-UI-COM-008": "Source operational health and coverage/output must be expressible as distinct, separately-labeled dimensions; a legitimately quiet source must not read as unhealthy purely from low output.",
    "STD-UI-COM-009": "Where the backend preserves materially distinct pipeline-phase outcomes for an individual run — a stage field, an ordered ledger, or per-run, phase-attributable outcome fields (fetch/parse failures, validation outcomes, regression notes) — the primary run surface must not erase that distinction, and must visibly indicate and directly link to the deeper detail. An ordered ledger is sufficient but not required; aggregate or windowed metrics alone do not trigger this.",
    "STD-UI-COM-010": "Every timestamp whose meaning could be ambiguous must have its semantic role labeled, and its timezone must be unambiguous — a per-value marker or one clearly stated page-level convention both satisfy this.",
    "STD-UI-COM-011": "Where a delivery mechanism records its own outcome, that outcome must be independently inspectable from discovery/review state; no dedicated delivery page is required, but collapsing distinct outcomes into one ambiguous boolean is not sufficient.",
    "STD-UI-NEWS-001": "A news-family Clank's QC vocabulary must use DUPLICATE as its fourth terminal action (not OUT_OF_STOCK); additional Clank-specific values beyond the fleet-standard four are allowed.",
    "STD-UI-NEWS-002": "A news-family Clank's live editorial intake/review queue must be reachable directly from the default landing surface, or via one obvious action — not buried in navigation.",
    "STD-UI-COM-007": "Manual collector controls must follow the Clank's lifecycle/authority policy: a collector in EXPERIMENTAL/SOAK state does not become runnable merely because a GUI control exists; if policy permits manual runs, the control must identify the collector as non-production and keep such runs out of production bulk actions; if policy forbids it, no individual control may be exposed.",
    "STD-UI-COM-012": "A primary operator surface must not present the Clank as healthy, normal, or operational solely from successful content activity when health is not actually represented there; where health is intentionally separated, an obvious path to current health should exist when operational judgement is part of the workflow.",
    "STD-UI-SKU-001": "Where availability is in scope for a SKU/product Clank's QC model, an availability-negative disposition ('exists, correctly identified, not currently available') must stay distinct from false-positive, duplicate, and not-useful — any queryable encoding satisfies this; a literal OUT_OF_STOCK label is not required.",
}

# id -> (question, failure_means). One entry per RATIFIED standard.
CHECKLIST_ITEMS: dict[str, dict[str, str]] = {
    "STD-UI-COM-001": {
        "question": "Does opening or launching the GUI avoid starting any collector run by itself?",
        "failure_means": "A GET route, app-startup hook, or lifespan event triggers collection with no explicit operator action.",
    },
    "STD-UI-COM-002": {
        "question": "Is every operator QC decision — whether recorded through the GUI, a CLI command, or other operator tooling — written as an atomic, provenance-bearing, race-guarded record, with any success indicator driven by confirmation of that write?",
        "failure_means": "A QC action can appear successful (toast, checkmark, queue removal, a CLI 'recorded' message) before or without a confirmed atomic/race-safe write; a concurrent double-decision can silently duplicate, crash, or lose data; or a GUI-less decision path (CLI command, service method, action store) was never inventoried and so never checked.",
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
        "question": "If the backend preserves materially distinct pipeline-phase outcomes for an individual run — per-run, phase-attributable fields such as fetch/parse failures, validation outcomes, or regression notes, not just window aggregates — can an operator reach that run's phase detail directly and discoverably from the primary run surface?",
        "failure_means": "Stage-level detail exists in per-run structured state or on some page, but the primary run surface gives no visible indication it exists and no direct link to it; or aggregate/window health metrics alone were mistaken for per-run stage data (without per-run, phase-attributable state this standard is not triggered).",
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
    "STD-UI-COM-007": {
        "question": "Where manual collector controls exist, do they follow the Clank's lifecycle policy — non-production collectors identified as non-production at the control, such runs isolated from bulk actions, and no control at all where policy forbids manual runs?",
        "failure_means": "A manual control runs an experimental/soak collector with no non-production indication at the control, such a run is reachable via or counted in a production run-all, or a control is exposed for a collector whose policy forbids manual execution.",
    },
    "STD-UI-COM-012": {
        "question": "Does the primary workflow surface avoid presenting the Clank as healthy or operational solely from content activity when health is not actually represented there — and where health is separated, is an obvious path to current health provided when operational judgement is part of the workflow?",
        "failure_means": "A landing/primary page presents activity, counts, or queue movement in a way that reads as health with no measured health behind it, or health is separated with no obvious path to it where the operator needs it for judgement.",
    },
    "STD-UI-SKU-001": {
        "question": "Where availability is in scope for the QC model, is an availability-negative outcome kept distinct from false-positive, duplicate, and not-useful — via any queryable encoding — rather than folded into them?",
        "failure_means": "An availability-negative case can only be expressed as false-positive or not-useful, or availability semantics are forced onto a QC model whose Clank does not track availability.",
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


def load_audit_findings() -> list[tuple[Path, dict]]:
    """Parse the leading fenced ```json block out of every audits/*.md
    file. Returns (path, parsed_block) pairs. Fails closed (raises) if an
    audit file has no such block, or the block is malformed — a silent
    skip would mean a real finding quietly never reaches the index.

    A block may carry "superseded_by": "<audits/… path>" when a later
    audit for the same Clank replaces its assessment (see
    audits/smartphone-clank-2026-08-30-pass1.md). The file and its
    findings stay in the repository as historical evidence, but
    build_known_evidence_index() excludes superseded blocks so the index
    reflects the current assessment only."""
    results = []
    for path in sorted(AUDITS_DIR.glob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text()
        match = AUDIT_JSON_BLOCK_RE.search(text)
        if not match:
            raise ValueError(f"{path}: no leading ```json findings block found")
        block = json.loads(match.group(1))
        for key in ("clank", "date", "findings"):
            if key not in block:
                raise ValueError(f"{path}: findings block missing required key {key!r}")
        results.append((path, block))
    return results


def _active_audit_findings() -> list[tuple[Path, dict]]:
    """load_audit_findings() with superseded blocks removed and every
    superseded_by reference validated (must point at an existing,
    non-superseded audit file) — a supersession marker pointing at a
    missing or itself-superseded file must fail closed, not drift."""
    all_blocks = load_audit_findings()
    superseded = {path for path, block in all_blocks if block.get("superseded_by")}
    active = []
    for path, block in all_blocks:
        ref = block.get("superseded_by")
        if not ref:
            active.append((path, block))
            continue
        if f"audits/{path.name}" == ref:
            raise ValueError(f"{path}: superseded_by points at itself")
        target = REPO_ROOT / ref
        if not target.is_file():
            raise ValueError(f"{path}: superseded_by target {ref!r} does not exist")
        if target in superseded:
            raise ValueError(f"{path}: superseded_by target {ref!r} is itself superseded")
    return active


def build_known_evidence_index() -> list[dict]:
    """Prior findings (from audits/*.md) about specific Clanks, kept
    entirely separate from build_ratified_index()/build_agent_checklist().

    This is deliberate, not an oversight: a BLIND conformance audit should
    load only the constitution + ratified-index + checklist, so it
    reproduces findings independently rather than being told in advance
    what it's expected to find. An INFORMED remediation task may
    additionally load this file. See
    docs/ui/agent-implementation-workflow.md's re-verification clause —
    every entry here is a hypothesis from a prior pass, not current-state
    truth, and MUST be re-verified against the target's current
    implementation before being reported as a present non-conformance.

    Only `kind: "violation"` findings are included — conformances,
    not-applicable classifications, and unresolved questions aren't
    "evidence of a gap" and don't belong in a prior-nonconformance index.
    Superseded audit blocks (see `_active_audit_findings`) are excluded so
    the index always reflects the current assessment of a Clank.
    """
    ratified_ids = {s["id"] for s in load_ratified_ui_standards()}
    index = []
    for path, block in _active_audit_findings():
        for finding in block["findings"]:
            if finding.get("kind") != "violation":
                continue
            std_id = finding["standard"]
            if std_id not in ratified_ids:
                raise ValueError(
                    f"{path}: finding cites {std_id!r}, which is not a RATIFIED standard id"
                )
            index.append(
                {
                    "standard": std_id,
                    "subject": block["clank"],
                    "kind": "known_nonconformance",
                    "source": "audit",
                    "summary": finding["summary"],
                    "source_reference": f"audits/{path.name}",
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
