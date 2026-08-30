# watch-clank — fresh-agent validation audit, 2026-08-30

```json
{
  "clank": "watch-clank",
  "date": "2026-08-30",
  "findings": [
    { "standard": "STD-UI-COM-001", "kind": "conformance", "summary": "All GET routes are read-only; collection is reachable only from gated POST routes; lifespan() only logs." },
    { "standard": "STD-UI-COM-002", "kind": "conformance", "summary": "Unique constraint on event_id/lead_id; IntegrityError caught and reapplied as a correction; response only returns ok after commit. Cited as this standard's own reference implementation." },
    { "standard": "STD-UI-COM-003", "kind": "conformance", "summary": "Active-queue queries outer-join the review table and filter on review id is null; no live-row mutation for QC purposes." },
    { "standard": "STD-UI-COM-004", "kind": "conformance", "summary": "/qc/history and its API routes read from the review tables via dedicated history-fetch functions, nav-linked, never reconstructed from the live table." },
    { "standard": "STD-UI-COM-005", "kind": "conformance", "summary": "No route mutates EXPERIMENTAL_MATURITY_COLLECTORS; no promote button/route found." },
    { "standard": "STD-UI-COM-006", "kind": "conformance", "summary": "SAFE_COLLECTOR_IDS excludes experimental collectors from the bulk run-all route by default; override requires an out-of-band env var." },
    { "standard": "STD-UI-COM-008", "kind": "conformance", "summary": "SourceHealth.acquisition_state and .yield_state are distinct fields, rendered as separately-labeled columns. Cited as this standard's own reference implementation." },
    { "standard": "STD-UI-COM-009", "kind": "conformance", "summary": "REMEDIATED (watch-clank 13f842a) and verified PASS 2026-08-31. Original violation: PipelineLedger tracks real stage data with an explicit stage_order, but the primary Runs page shows only a terminal status badge with no link or indication that stage/correlation detail exists; even the per-watch drill-down doesn't hyperlink the correlation id. Fix: /runs/{run_id} run-detail surface linked from every run row, stage-ordered ledger grouped per correlation id with links into /correlation/{id}; hyperlinked drill-down short-ids." },
    { "standard": "STD-UI-COM-010", "kind": "conformance", "summary": "REMEDIATED (watch-clank 13f842a) and verified PASS 2026-08-31. Original violation: the SpecialistLead table's 'Published / observed' column collapses two distinct timestamp semantics into one with no per-row indication of which is shown; watch_detail.html and correlation.html render raw timestamps skipping the app's documented always-labeled-with-zone convention. Fix: all four surfaces via humantime; neutral 'Timing' header with explicit per-cell published/discovered role labels on both render paths. Separate low-severity observation (not a reopened failure): scheduler.html renders windows schtasks next_run/last_run strings without zone labels." },
    { "standard": "STD-UI-COM-011", "kind": "violation", "summary": "PARTIALLY REMEDIATED (watch-clank 13f842a, verified 2026-08-31): the primary notification paths now record and surface per-item sent/failed/gated/ineligible outcomes (events extra['delivery']; leads delivery_state + migration 012; Delivery column on Recent Intelligence, server and JS rows). REMAINING GAPS: (1) notify_correlation — the CONFIRMED/FAMILY_MATCH follow-up send — records no delivery outcome, so a correlation-alerted lead can read as 'not delivered'; (2) _record_watch_event with notify=False records nothing, where the control flow could state gated/notify_disabled. Original violation: Event.extra['alerted'] and SpecialistLead.notified_at were persisted delivery outcomes no template ever read; only aggregate Discord config state was shown." },
    { "standard": "STD-UI-NEWS-001", "kind": "conformance", "summary": "SpecialistLeadReview vocabulary uses DUPLICATE, not OUT_OF_STOCK, confirming the two-vocabulary hybrid design." },
    { "standard": "STD-UI-NEWS-002", "kind": "unresolved", "summary": "The intelligence/review queue is one click from the stats-first landing page via a low-visual-weight link; whether that satisfies 'reachable directly or via one obvious action' for a hybrid Clank is a genuine applicability question the rule's news-only evidence base doesn't resolve." }
  ]
}
```

This block is machine-read by `tools/ui_agent_layer.py` to build
[`standards/ui/known-evidence-index.json`](../standards/ui/known-evidence-index.json) —
kept structurally separate from the normative ratified-index/checklist so
a blind conformance audit isn't told in advance what it's expected to
find. See that file's own note, and
[`docs/ui/agent-implementation-workflow.md`](../docs/ui/agent-implementation-workflow.md)'s
re-verification clause.

## Post-remediation verification (2026-08-31) — REMEDIATION_PARTIAL

The three violations found below were remediated in watch-clank commit
`13f842a` under an informed remediation plan, then independently
re-verified against that HEAD (not against the remediation report). The
historical violation findings above and the violation sections below are
preserved unmodified as the original record; the structured block now
carries the current assessment.

| Standard | Initial (2026-08-30) | After 13f842a (verified 2026-08-31) |
|---|---|---|
| STD-UI-COM-009 | FAIL | REMEDIATED — PASS |
| STD-UI-COM-010 | FAIL | REMEDIATED — PASS |
| STD-UI-COM-011 | FAIL | PARTIALLY REMEDIATED |

Full suite at verification time: 485 passed, 2 skipped. No new
ratified-standard regressions; all specialist-surface regression checks
clean. Remaining COM-011 scope (both are delivery write paths the
remediation did not instrument, exactly the class acceptance criterion 2
targets):

1. `notify_correlation` — the CONFIRMED/FAMILY_MATCH follow-up send —
   records no delivery outcome, so a correlation-alerted lead can read as
   "not delivered".
2. `_record_watch_event` with `notify=False` records nothing, where the
   control flow could state `gated/notify_disabled`.

Separate non-remediation note: `scheduler.html` renders Windows
`schtasks` `next_run`/`last_run` strings without zone labels — a new,
low-severity COM-010 observation, explicitly **not** a reopening of the
remediated COM-010 finding.

## Context

This is the first fresh-agent validation of Standards Clank's agent-facing
UI layer (`docs/ui/constitution.md` +
`docs/ui/agent-implementation-workflow.md` +
`standards/ui/ratified-index.json` + `standards/ui/agent-checklist.json`):
an agent with no memory of how that layer was built, given only the repo
itself and told to follow the workflow literally against watch-clank's
current code, read-only, stopping before any implementation (workflow
steps 1-8 only).

## Clank family

Hybrid (`sku-based` and `news-based`), confirmed independently in code —
not just from the profile files. `watch-clank/app/models/review.py:60`
(`EventReview`, includes `OUT_OF_STOCK`) and
`watch-clank/app/models/specialist_lead_review.py:44`
(`SpecialistLeadReview`, uses `DUPLICATE` instead) are two structurally
separate review tables with two different vocabularies.

## Applicable RATIFIED standards

Fleet-wide: `STD-UI-COM-001`, `002`, `003`, `004`, `005`, `006`, `008`,
`009`, `010`, `011`. Family-scoped (news-based): `STD-UI-NEWS-001`,
`STD-UI-NEWS-002`.

## Conformances

`STD-UI-COM-001`, `002`, `003`, `004`, `005`, `006`, `008`, `STD-UI-NEWS-001`
— see the structured findings above for the specific code evidence per
rule. `STD-UI-COM-002` and `STD-UI-COM-008` are independently cited by
those standards' own files as watch-clank being their reference
implementation.

## Violations

- **`STD-UI-COM-009`** — confirmed and reproduces what the standard's own
  `notes` field already flagged at ratification time
  (`standards/ui/STD-UI-COM-009.json`): watch-clank's Runs page collapses
  tracked pipeline-stage detail with no visible indication or link to it.
- **`STD-UI-COM-011`** — confirmed the known `Event.extra['alerted']` gap
  cited in `standards/ui/STD-UI-COM-011.json`'s evidence, **and
  independently found a second, previously-uncited instance**:
  `SpecialistLead.notified_at` has the identical never-surfaced pattern.
- **`STD-UI-COM-010`** — confirmed the known "Published / observed"
  ambiguous-column regression cited in `standards/ui/STD-UI-COM-010.json`,
  plus two further raw/unlabeled timestamps not previously cited
  (`watch_detail.html:37`, `correlation.html:13`).

## N/A

None — every applicable standard's underlying concept genuinely exists in
watch-clank's architecture.

## Specialist surfaces to preserve

The two separate QC vocabularies/tables (this *is* the hybrid
architecture, not a bug); the `reviewed_today_breakdown` audit-trail
extension; the `qc_memory_context`/`human_qc_deprioritized` annotation
mechanism; the `acquisition_state`/`yield_state` two-dimensional health
model (this *is* the STD-UI-COM-008 conformance mechanism); the IST
secondary-timezone reading in `_humantime`; the local-collection
field-test controller's lock semantics.

## Files expected to change (not authorized, not touched)

`app/templates/runs.html`, `app/main.py` (`run_history`),
`app/templates/watch_detail.html`, `app/templates/correlation.html`,
`app/templates/intelligence.html`, plus the QC-dict helper functions in
`app/main.py` and their templates for the delivery-outcome fix. See the
full agent report (this audit's originating task) for line-level detail.

## Proposed exceptions

None. All three violations look like ordinary remediation-backlog items —
nothing about watch-clank's architecture makes compliance genuinely
inappropriate.

## Unresolved semantic questions

`STD-UI-NEWS-002`'s applicability to a *hybrid* Clank's landing page is a
genuine open question (see the finding above) — left unresolved by
operator instruction pending a future profile/applicability rule for
hybrids, rather than an ad hoc decision against watch-clank specifically.

## What this audit does NOT do

It does not authorize or schedule remediation work. No code in
watch-clank was touched to produce or as a result of this audit — the
originating task was explicitly read-only (workflow steps 1-8 only).
