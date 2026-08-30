# smartphone-clank — fresh-agent blind validation audit (second validation), 2026-08-30

```json
{
  "clank": "smartphone-clank",
  "date": "2026-08-30",
  "findings": [
    { "standard": "STD-UI-COM-001", "kind": "conformance", "summary": "All GET routes are pure reads; the only run-triggering POST hard-returns 403 read-only (dashboard/app.py:127-132) without invoking the controller; collection is driven by systemd timers outside the GUI process; the field-test launcher scrubs inherited webhook credentials." },
    { "standard": "STD-UI-COM-002", "kind": "violation", "summary": "The only operator QC decision path is the CLI qc-action command (main.py:1227-1268), which writes a raw INSERT into analyst_actions (main.py:1251-1259) with no uniqueness constraint on (target_type, target_id) and no concurrent-decision handling (alembic/versions/0004_v032.py:15-29); provenance columns exist but before_state/after_state/related_evidence are written as NULL, so 'on what evidence' is not reconstructable. GUI-invisible, but the underlying decision contract governs the write itself (decisions/0005)." },
    { "standard": "STD-UI-COM-003", "kind": "not_applicable", "summary": "No active operator QC/review queue surface exists for a decided item to leave; the page titled 'Device queue' (dashboard/templates/devices.html:4) is a canonical catalogue — its query (dashboard/app.py:135-163) selects all devices by recency with no decision-state semantics. Refined from the pass-1 'violation' classification per decisions/0005; the root write-path gap remains recorded under STD-UI-COM-002." },
    { "standard": "STD-UI-COM-004", "kind": "not_applicable", "summary": "The standard's explicit 'if, and only if, a Clank's GUI exposes an operator QC queue' trigger is unmet: the GUI exposes no QC queue (the QC surface is CLI). Refined from the pass-1 'violation' classification per decisions/0005." },
    { "standard": "STD-UI-COM-005", "kind": "conformance", "summary": "Production membership is a compile-time fail-closed frozenset (alerts/source_maturity.py:31-50); promotion requires an explicit reviewed code edit ('never a config-only flip', alerts/source_maturity.py:11-13); no GUI route mutates it and no runtime metric can (single reference in the codebase)." },
    { "standard": "STD-UI-COM-006", "kind": "not_applicable", "summary": "The GUI exposes no bulk 'run all' control at all — the only mutation route hard-returns 403 (dashboard/app.py:127-132) and LocalCollectionController.start() (dashboard/local_collection.py:52-65) is GUI-unreachable at HEAD; bulk execution lives in systemd timers outside the GUI. (Note: native/windows/launcher.py:5-9 docstring still claims per-source triggering — stale vs app.py, recorded as a maintainer note, not a standards failure.)" },
    { "standard": "STD-UI-COM-008", "kind": "conformance", "summary": "Health is a 0-100 score whose every deduction is a named, rendered factor (observability/metrics.py:293-401; factor cards dashboard/templates/metrics.html:73-89); output volume lives in separate labeled columns (metrics.html:24-39). Sustained zero-output-vs-baseline is a health signal by explicit design (zero_discovery_with_healthy_fetch threshold, unexpected_zero status, labeled candidate_count_low factor) — the standard's stated carve-out, satisfied as a distinctly labeled dimension, not a silent blend." },
    { "standard": "STD-UI-COM-009", "kind": "unresolved", "summary": "Aggregate fetch-vs-parse distinction is visible inline (parser-fail and HTTP-fail columns, metrics.html:33-34,60-61; last-run status granularity flows into named health factors), but there is no per-run surface: individual run records — including the regression notes the metrics subtitle (metrics.html:5) advertises — are reachable from no route. CollectorRunRecord (observability/metrics.py:34-68) is a flat per-run record with phase-attributable counters and a status enum but no stage field/ledger. Whether that is an 'equivalent structured record' under COM-009 is an open interpretation: PARTIAL pending decisions/0006; under the proposed reading it would be FAIL (indicated but unreachable), under a strict reading N/A (trigger unmet). Do not resolve without the operator." },
    { "standard": "STD-UI-COM-010", "kind": "violation", "summary": "Naive-UTC datetimes (database/models.py:46-47,127,368-370) are rendered raw with no zone marker and no stated page-level convention on four of five content surfaces: devices.html:12,20; dossier.html:18-19,79,96,99; metrics.html:28,55; discord.html:11,16-17,32. The only zoned value in the GUI is home.html:45 ('Generated ... UTC'). dossier.html:79 'When' sits on occurred_at while the backend also tracks recorded_at (database/models.py:212-213) and shows neither label nor the other value, so observed-vs-recorded is not determinable." },
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
| STD-UI-COM-009 | PARTIAL — unresolved, pending decisions/0006 |
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

### STD-UI-COM-009 — PARTIAL / unresolved

See the structured finding above. The aggregate surface does not collapse
the fetch-vs-parse distinction the backend tracks (separate labeled
24h-failure columns, `metrics.html:33-34,60-61`; last-run status
granularity surfaces as named, delta-labeled health factors,
`observability/metrics.py:327-341` + `metrics.html:73-89`). But no route
exposes per-run records at all — including the regression notes that
`metrics.html:5` explicitly advertises — so acceptance criterion 1's
"direct, discoverable path" is unmet *if* the trigger applies. Whether a
flat per-run record with phase-attributable counters and a status enum is
an "equivalent structured record of what point execution reached" is the
open question in
[decisions/0006-com009-equivalent-structured-record.md](../decisions/0006-com009-equivalent-structured-record.md):
under the proposed reading the verdict would become FAIL; under a strict
reading, N/A. Left unresolved for the operator.

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
  structured record" trigger needs the interpretation proposal in
  decisions/0006; the workflow's pass-1 worked example required updating
  to the refined classification.

## Proposed exceptions

None. The COM-002 gap is a pre-existing implementation debt against
ratified semantics, not a case where compliance is genuinely
inappropriate.

## Unresolved questions for the operator

1. COM-009 "equivalent structured record" interpretation (decisions/0006).
2. Whether the absence of any operator QC *GUI* in smartphone-clank
   should be tracked as product backlog (the COM-002 write-contract
   failure stands either way).
