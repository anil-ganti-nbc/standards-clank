# smartphone-clank — fresh-agent blind validation audit (second validation), 2026-08-30

```json
{
  "clank": "smartphone-clank",
  "date": "2026-08-30",
  "findings": [
    { "standard": "STD-UI-COM-001", "kind": "conformance", "summary": "All GET routes are pure reads; the only run-triggering POST hard-returns 403 read-only (dashboard/app.py:127-132) without invoking the controller; collection is driven by systemd timers outside the GUI process; the field-test launcher scrubs inherited webhook credentials." },
    { "standard": "STD-UI-COM-002", "kind": "conformance", "summary": "REMEDIATED (smartphone-clank 5684cf2) and verified PASS 2026-08-31. Original violation: the CLI qc-action command wrote a raw INSERT into analyst_actions with no uniqueness constraint on (target_type, target_id), no concurrent-decision handling, and NULL provenance snapshot columns. Fix (operator Option A): partial unique index uq_analyst_action_terminal (ORM for fresh databases, migration 0008 for existing) enforcing one authoritative terminal decision per target with 'note' exempt as a non-terminal append-only channel; fail-closed explicit vocabulary; collisions resolved as explicit rejection with distinct CLI message and non-zero exit; provenance snapshot populated in the same transaction." },
    { "standard": "STD-UI-COM-003", "kind": "not_applicable", "summary": "No active operator QC/review queue surface exists for a decided item to leave; the page titled 'Device queue' (dashboard/templates/devices.html:4) is a canonical catalogue — its query (dashboard/app.py:135-163) selects all devices by recency with no decision-state semantics. Refined from the pass-1 'violation' classification per decisions/0005; the root write-path gap remains recorded under STD-UI-COM-002." },
    { "standard": "STD-UI-COM-004", "kind": "not_applicable", "summary": "The standard's explicit 'if, and only if, a Clank's GUI exposes an operator QC queue' trigger is unmet: the GUI exposes no QC queue (the QC surface is CLI). Refined from the pass-1 'violation' classification per decisions/0005." },
    { "standard": "STD-UI-COM-005", "kind": "conformance", "summary": "Production membership is a compile-time fail-closed frozenset (alerts/source_maturity.py:31-50); promotion requires an explicit reviewed code edit ('never a config-only flip', alerts/source_maturity.py:11-13); no GUI route mutates it and no runtime metric can (single reference in the codebase)." },
    { "standard": "STD-UI-COM-006", "kind": "not_applicable", "summary": "The GUI exposes no bulk 'run all' control at all — the only mutation route hard-returns 403 (dashboard/app.py:127-132) and LocalCollectionController.start() (dashboard/local_collection.py:52-65) is GUI-unreachable at HEAD; bulk execution lives in systemd timers outside the GUI. (Note: native/windows/launcher.py:5-9 docstring still claims per-source triggering — stale vs app.py, recorded as a maintainer note, not a standards failure.)" },
    { "standard": "STD-UI-COM-008", "kind": "conformance", "summary": "Health is a 0-100 score whose every deduction is a named, rendered factor (observability/metrics.py:293-401; factor cards dashboard/templates/metrics.html:73-89); output volume lives in separate labeled columns (metrics.html:24-39). Sustained zero-output-vs-baseline is a health signal by explicit design (zero_discovery_with_healthy_fetch threshold, unexpected_zero status, labeled candidate_count_low factor) — the standard's stated carve-out, satisfied as a distinctly labeled dimension, not a silent blend." },
    { "standard": "STD-UI-COM-009", "kind": "conformance", "summary": "REMEDIATED (smartphone-clank 5684cf2) and verified PASS 2026-08-31, under the operator-accepted decisions/0006 boundary (CollectorRunRecord is a per-run, phase-attributable 'equivalent structured record'). Original violation: /metrics indicated that per-run detail existed (the subtitle advertised 'regression notes in run records') but no route exposed any run record. Fix: new /metrics/runs/{run_id} detail surface (status, phase-attributable counters, regression notes, run_reason) plus a Recent runs table linking every run; aggregate metrics unchanged." },
    { "standard": "STD-UI-COM-010", "kind": "conformance", "summary": "REMEDIATED (smartphone-clank 5684cf2) and verified PASS 2026-08-31. Original violation: naive-UTC datetimes rendered raw with no zone marker and no stated page-level convention across devices/dossier/metrics/discord, and a dossier Timeline 'When' column ambiguous between occurred_at and recorded_at. Fix: one stated 'All times UTC' convention in the shared base layout (explicitly sufficient under the ratified wording), covering every surface; the ambiguous column relabeled to 'Observed'." },
    { "standard": "STD-UI-COM-011", "kind": "conformance", "summary": "Per-channel delivery accounting with five distinct outcomes (eligible/attempted/delivered/suppressed/failed) plus a failures table with reason/HTTP status/error (dashboard/app.py:243-292; dashboard/templates/discord.html:11-38; alerts/delivery.py:181-201), backed by a delivery record that persists suppressed sends with evidence (alerts/source_maturity.py:15-18). Failed and suppressed are visibly distinct from never-eligible." },
    { "standard": "STD-UI-NEWS-001", "kind": "not_applicable", "summary": "smartphone-clank is sku-based (devices/SKUs/evidence/snapshots from OEM support pages and sitemaps; no story/lead entities; no review vocabulary anywhere) — the standard is scoped to applies_to: [news-based]. The 'Newsroom' branding (dashboard/app.py:2, home.html:4, the 'newsroom' Discord channel) is naming for a device-discovery intelligence channel, not an editorial-lead workflow." },
    { "standard": "STD-UI-NEWS-002", "kind": "not_applicable", "summary": "sku-based family (see STD-UI-NEWS-001 entry); no live editorial intake/review queue concept exists to expose. No review vocabularies of any kind were found, so the Clank is not a watch-clank-style hybrid." }
  ]
}
```

This block is machine-read by `tools/ui_agent_layer.py` to build
[`standards/ui/known-evidence-index.json`](../standards/ui/known-evidence-index.json) —
kept structurally separate from the normative ratified-index/checklist so
a blind conformance audit isn't told in advance what it's expected to
find. It is now also the *current* smartphone-clank assessment: it
supersedes
[smartphone-clank-2026-08-30-pass1.md](smartphone-clank-2026-08-30-pass1.md)
(GUI Ratification Pass 1 note), whose COM-003/004 "violation"
classifications were refined to N/A under the ratified conditional
wording by
[decisions/0005-qc-applicability-refinement.md](../decisions/0005-qc-applicability-refinement.md).
The pass-1 file's factual observations stand; only its classification
changed.

## Post-remediation verification (2026-08-31) — REMEDIATION_VERIFIED

The three violations found below were remediated in smartphone-clank
commit `5684cf2` under an informed remediation plan (operator-approved,
including the Option A terminal-decision uniqueness ruling), then
independently re-verified against that HEAD (not against the remediation
report). The original violation findings and the remediation/interpretation
history above are preserved unmodified; the structured block now carries
the current assessment.

| Standard | Initial (2026-08-30/31) | After 5684cf2 (verified 2026-08-31) |
|---|---|---|
| STD-UI-COM-002 | FAIL | REMEDIATED — PASS |
| STD-UI-COM-009 | FAIL | REMEDIATED — PASS |
| STD-UI-COM-010 | FAIL | REMEDIATED — PASS |

Full suite at verification time: 252 passed, 1 skipped. No new
ratified-standard regressions; read-only dashboard posture, COM-003/004
N/A standing, and all specialist surfaces preserved.

Operational/deploy note (not a standards violation): existing production
databases receive the COM-002 integrity contract via migration 0008 at
the next normal `alembic upgrade head`; until then an unmigrated database
enforces no uniqueness. Optional hardening/backlog (explicitly not a
blocker to this closure): the qc-action CLI could fail closed on a stale
schema, mirroring the dashboard's schema_guard refusal.

The QC GUI absence remains non-normative product/remediation backlog only;
`STD-UI-COM-003`/`STD-UI-COM-004` remain N/A per their ratified triggers
(decisions/0005). COM-003/004 were not reclassified by this closure.

## Context

Second fresh-agent validation of the compact agent layer
(`docs/ui/constitution.md` + `docs/ui/agent-implementation-workflow.md` +
`standards/ui/ratified-index.json` + `standards/ui/agent-checklist.json`),
against **smartphone-clank HEAD `09923e7`** (2026-08-30, verified equal to
its GitHub `origin/main`), read-only, stopping before any implementation.

Blindness disclosure: a perfectly blind audit of this target was not
possible — the prior pass-1 assessment was already cited inside the agent
layer itself (workflow worked example). All verdicts below were derived
from current smartphone-clank code; one inventory gap (the CLI-only
`analyst_actions` write path, created in a migration rather than the
models module) was caught during the post-freeze comparison step and then
independently re-verified against HEAD before being adopted.

## Clank family

`sku-based`, verified against content: units are devices/SKUs, evidence,
snapshots, download assets, and per-URL fetch ledgers from OEM support
pages, sitemaps, and store categories. No story/lead entities, no review
vocabularies of any kind — **not** a watch-clank-style hybrid. The
"Newsroom" naming (app module docstring, home page title, `newsroom`
Discord channel) is branding over a device-discovery intelligence
channel; it is a family-classification hazard worth remembering, not a
family fact.

## Verdict table

| Standard | Verdict |
|---|---|
| STD-UI-COM-001 | PASS |
| STD-UI-COM-002 | FAIL |
| STD-UI-COM-003 | N/A |
| STD-UI-COM-004 | N/A |
| STD-UI-COM-005 | PASS |
| STD-UI-COM-006 | N/A |
| STD-UI-COM-008 | PASS |
| STD-UI-COM-009 | FAIL (under the operator-accepted decisions/0006 boundary; previously PARTIAL/unresolved) |
| STD-UI-COM-010 | FAIL |
| STD-UI-COM-011 | PASS |
| STD-UI-NEWS-001 | N/A (family) |
| STD-UI-NEWS-002 | N/A (family) |

## Violations (current evidence, exact file:line)

### STD-UI-COM-002 — FAIL

The only operator QC decision path is the CLI `qc-action` command
(`main.py:1227-1268`). It performs a raw
`INSERT INTO analyst_actions ...` (`main.py:1251-1259`). The table
(`alembic/versions/0004_v032.py:15-29`) has a primary key but **no
uniqueness constraint on `(target_type, target_id)`** and no concurrent
-second-decision handling: two simultaneous decisions on the same target
both commit as indistinguishable rows, each acknowledged with
`[green]recorded[/green]` (`main.py:1264`). Acceptance criteria 2 and 3
fail verbatim. Criterion 1 is met with a weakness: `analyst_actions` *is*
distinct from the live device/evidence rows and append-only in practice
(nothing in this repo reads or updates it — consumption is external via
Motherclank, per the command docstring), and it carries provenance
columns, but the CLI writes `None` into `before_state`, `after_state`,
and `related_evidence`, so "on what evidence" is not reconstructable from
the record. Operator experience: duplicate silent success. Smallest
semantic remediation: a uniqueness constraint plus defined collision
handling, and population of the provenance snapshot columns. The GUI
truthfulness clause is trivially satisfied today — there is no GUI QC
surface to lie — the failure is purely the write contract, which governs
the decision path wherever it lives (decisions/0005).

### STD-UI-COM-010 — FAIL

All timestamps are naive-UTC `DateTime` (`database/models.py:46-47`,
`:127`, `:368-370`) rendered raw with no per-value zone marker, and no
content surface states a page-level convention: `devices.html:12,20`;
`dossier.html:18-19,79,96,99`; `metrics.html:28,55`;
`discord.html:11,16-17,32`. The only zoned value in the entire GUI is
`home.html:45` ("Generated … UTC") — the convention is known but not
stated where timestamps are actually shown, which is exactly what
acceptance criterion 2 requires. One genuine semantic-role ambiguity: the
dossier Timeline column "When" (`dossier.html:79`) renders `occurred_at`
while the backend separately tracks `recorded_at`
(`database/models.py:212-213`) and the UI shows neither a distinguishing
label nor the other value. Operator experience: bare values like
`2026-08-30 14:22:01` with no stated zone. Smallest semantic remediation:
one "All times UTC" caption per surface (or in `base.html`); relabel
"When".

### STD-UI-COM-009 — FAIL

`CollectorRunRecord` (`observability/metrics.py:34-68`) preserves
materially distinct pipeline-phase outcomes at the level of an individual
run: immutable per-run rows with phase-attributable counters
(`http_failures` = fetch stage, `parser_failures` = parse stage), a
per-run status enum (success / partial / degraded / unexpected_zero /
failed / blocked), and per-run regression notes. Under the operator-accepted
interpretation ([decisions/0006](../decisions/0006-com009-equivalent-structured-record.md),
accepted 2026-08-30), this is an "equivalent structured record": a flat
record that preserves fetch-vs-parse-vs-overall distinctions for a
specific run carries the same pipeline truth as a formal ordered stage
ledger: applicability follows the granularity of preserved evidence, not
the shape of the schema.

Against that trigger, the surface obligations bite, and the current GUI
does not meet them. The primary run surface (`/metrics`) indicates that
per-run detail exists — its subtitle explicitly advertises "regression
notes in run records" (`metrics.html:5`) — but **no route exposes any run
record**: individual run statuses, per-run failure counters, and the
advertised regression notes are reachable only by querying the database
directly. That is acceptance criterion 1 failed on its second half:
indicated, but with no direct, discoverable path. The aggregate
fetch-vs-parse columns (`metrics.html:33-34,60-61`) and factor-labeled
health scores show the backend's distinctions at window granularity,
which has real operational value but does not substitute for per-run
reachability — a single run's `partial` status and its specific failure
phase are exactly what the operator cannot get to.

Operator experience: `/metrics` says deeper per-run information exists,
and then offers no way to see any of it.

Verdict history: recorded as **PARTIAL/unresolved** in the original
blind validation while the trigger question was open
(decisions/0006 was then a proposal); the operator accepted the
interpretation on 2026-08-30, which resolved the applicability question
in favor of the trigger applying. The reachability gap was never in
dispute — only whether the standard was triggered — so the FAIL rests on
the same evidence, under settled semantics.

## Specialist surfaces to preserve

Read-only Phase 0 posture with the hard-403 mutation block
(`dashboard/app.py:127-132`); explainable factor-level health scores with
per-collector score-factor cards; suppression-with-evidence delivery
ledger (`WebhookDelivery` rows for policy-suppressed sends,
`alerts/source_maturity.py:15-18`); confidence-ledger stored-vs-derived
drift check on the dossier (`dossier.html:26-34`); fail-closed eligibility
reason sets (`alerts/eligibility.py`); soak-suppression notification
policy (`alerts/source_maturity.py`). A future remediation must not
normalize any of these into generic CRUD.

## Target-maintainer notes (not standards findings)

- `native/windows/launcher.py:5-9` docstring claims the eight field-test
  sources "remain individually triggerable via
  LocalCollectionController.start(source_id)", but the current GUI POST
  route hard-returns 403 without ever calling it (`dashboard/app.py:127-132`)
  — a docs/code divergence inside smartphone-clank. No ratified standard
  is violated by a stale docstring; recorded here only for the target's
  maintainers. smartphone-clank was not modified by this audit.

## Agent-layer assessment

- The compact layer was sufficient for 10 of 12 standards without opening
  full normative files. Two traps were exposed and are now addressed in
  the workflow: a GUI-first inventory can miss CLI/migration-level
  operator decision paths (COM-002), and surface names can mislead
  applicability analysis (the "Device queue" catalogue). See
  decisions/0005 for the methodology corrections.
- Checklist/constitution ambiguities fed back: COM-009's "equivalent
  structured record" trigger question was resolved by operator acceptance
  of decisions/0006, with the boundary folded into the standard as v3
  (per-run, phase-attributable structured outcomes qualify; window
  aggregates alone do not); the workflow's pass-1 worked example was
  updated to the refined classification.

## Proposed exceptions

None. The COM-002 gap is a pre-existing implementation debt against
ratified semantics, not a case where compliance is genuinely
inappropriate.

## Product/remediation backlog (non-normative)

Per the operator ruling of 2026-08-30 (recorded in
[decisions/0006](../decisions/0006-com009-equivalent-structured-record.md)):

- **The absent operator QC GUI is tracked as product/remediation
  backlog.** This is an explicit classification, not a softening of a
  violation: `STD-UI-COM-003` and `STD-UI-COM-004` **remain N/A** under
  their ratified conditional triggers (decisions/0005), because no QC
  queue surface exists for them to govern. "Standards-compliant" does
  not mean "feature-complete" — Standards Clank must not distort
  conditional standards to express that a better operator workflow would
  be welcome. The backlog item says: a future operator QC/review surface
  for smartphone-clank would be valuable, and when one is built it must
  satisfy COM-002's decision contract from day one.
- The COM-009 reachability gap (no per-run detail surface) is a
  standards **violation** (FAIL above), distinct from the backlog item
  above: the per-run evidence already exists, so this is current
  non-conformance, not a missing feature.
- Neither item authorizes remediation work; no exception has been filed
  or proposed for either.

## Operator decisions log

1. ~~COM-009 "equivalent structured record" interpretation~~ — resolved
   2026-08-30: accepted (decisions/0006); verdict FAIL as recorded above.
2. ~~Whether the absent QC GUI is backlog or violation~~ — resolved
   2026-08-30: backlog, explicitly not a COM-003/004 violation (see
   Product/remediation backlog above).
