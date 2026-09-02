# OEM Radar Clank — M15 persistent-state compatibility evidence

```json
{"clank":"oem-radar","date":"2026-09-02","findings":[{"standard":"STD-DEPLOY-COM-002","kind":"conformance","summary":"CONFORMS / CLOSED at canonical OEM Radar main revision 79fbee63ee3a43badad085671ba5bf6837b627f7: schema_migrations v7 authority corroborated against the expected 20-table structure sits behind a read-only-first compatibility barrier that inspects through a mode=ro handle before any mutable setup, admits only genuinely fresh or known-older state through the canonical bootstrap/migration path with explicit re-verification, leaves refused files byte-identical, and no longer swallows duplicate-column migration errors — newer, unknown, corrupt, partial, and marker-behind-structure state fails closed across scheduler, CLI, dashboard, one-shot crawl, and health surfaces."}]}
```

This Standards-only M15 record closes `STD-DEPLOY-COM-002` at
`79fbee63ee3a43badad085671ba5bf6837b627f7`, source-level persistent-state
compatibility only. It is not live deployment proof, not a production
database migration, and not `STD-DEPLOY-COM-001` closure. `STD-UI-COM-011`
and `STD-DEPLOY-COM-001` remain unresolved; no overall OEM Radar
conformance is claimed.

## Lineage and history

Standards takeover was `f3eef513ce89cf2fcb96dad0a60b9bd77ba62baa`; OEM Radar
parent was `d720e0635894ddcc9a39f116e2aa4a1768090042`; the canonical
recorded revision is `79fbee63ee3a43badad085671ba5bf6837b627f7` (pushed to
`origin/main` and verified before this pass). M1 recorded
`STD-DEPLOY-COM-002` as `INSUFFICIENT_EVIDENCE` at this same parent SHA —
that history is preserved. M9b recorded `STD-OPS-COM-003 = NOT_APPLICABLE`
for OEM Radar; M10 classified it `APPLIES`, `NO_COMPATIBILITY_BARRIER`,
risk `HIGH`.

## The original OEM defect (preserved)

Before M15, `SqliteStore` construction invoked `migrate()` automatically,
and `migrate()` **layered the current `schema.sql` over the database before
honestly classifying it**, then stamped the marker, then swallowed
duplicate-column migration errors. Consequently construction could: turn
unknown structure into apparently current state; let marker/schema
contradictions proceed; let a newer v8+ database proceed because no
migrations remained to run; and erase the very evidence of incompatibility
as a side effect of opening. This was not merely "missing a version check"
— it was an **admission-ordering defect** in which mutation itself could
destroy incompatibility evidence. M15 supersedes the defect for the
canonical OEM Radar SHA; the history is not erased.

## Persistent-state inventory

Canonical evolving SQLite state: `radar.db`, plus equivalent experimental
database paths served by the same `SqliteStore` class. Authority:
`schema_migrations` v7 corroborated against the expected 20-table
structure. `data/oem_radar_qc.db` is **not** active schema authority:
independent source inspection confirms zero source references at the
canonical SHA — an orphaned pre-M4 artifact, not part of the normal
persistent-state contract. Non-schema content stores (`http_cache`,
`data/raw`, logs) have no evolving compatibility contract and are not
forced under DEPLOY-COM-002.

## Real radar.db observation — carefully scoped

Observed read-only during M15: v7 marker (1–7), all 20 expected tables,
`quick_check` ok, 85 crawler runs, 1,042 change events, and the file
remained byte-identical through the mission. This evidences that the real
store was current/compatible. It is **not** deployment proof, production
migration proof, live crawler proof, or DEPLOY-COM-001 evidence.

## Read-only-first barrier

Compatibility inspection occurs through a `mode=ro` handle **before** the
read-write connection, the WAL pragma, schema creation, migration, or any
marker write exists; a refusal is raised before any read-write handle is
created. Rejected state is test-proven **byte-identical**. Verified
directly from canonical source ordering in this pass.

## Compatibility model

`FRESH`, `MIGRATION_REQUIRED`, `COMPATIBLE`, `INCOMPATIBLE_NEWER`,
`UNKNOWN`, `CORRUPT`, `PARTIAL`. Semantics recorded: `FRESH != UNKNOWN`;
`DB_OPEN_SUCCESS != COMPATIBLE`; `MIGRATION_CAN_RUN != COMPATIBLE`;
`MARKER_EXISTS != COMPATIBLE`; `STRUCTURE_EXISTS != COMPATIBLE`. OEM
Radar's distinguishing feature: the marker authority is corroborated
against the expected structure — a marker claiming v7 with any expected
table missing is `PARTIAL`. The exact seven-state vocabulary is a family
observation, not a fleet-wide norm.

## Historical migration fixture correction (stronger, not relaxed)

Before M15, three existing legacy-migration tests built marker-only
pseudo-databases — a version stamp plus nothing. They passed only because
the pre-M15 migration path overlaid the current schema, tolerated
contradictory structure, and swallowed migration errors. M15 rebuilt them
on genuine historical schema shapes (`tests/legacy_db.py` replays the
project's own canonical migration DDL), so historical data survival is now
tested against realistic old structures, migrations must genuinely
transform them, and the Stage-11 evidence-move assertions are preserved.
The tests no longer depend on the defect being remediated — this is
**stronger** evidence, not relaxed coverage.

## Migration and failure semantics

Compatibility inspection occurs first; FRESH enters canonical bootstrap
only; valid historical prefixes enter canonical migration only, in
canonical order, transactionally (`BEGIN IMMEDIATE` with rollback proved
by the sabotage and duplicate-column tests); migrated state is re-inspected
before the store is handed back; unknown/partial/contradictory state fails
closed; duplicate-column failures are no longer silently accepted; failure
cannot advance the version marker or mark state ready; retry re-enters
inspection. No production migration occurred in M15. No stronger
transactional guarantee than the source proves is claimed.

## One-shot execution model

OEM Radar is one-shot oriented, and that is precisely why the barrier is
at store construction: the hourly scheduled task, a manual `oem-radar run`,
and the dashboard's crawl trigger all converge through
`execute_crawl` → compatibility-protected store construction. Verified:
ephemeral process lifetime does not bypass persistent-state authority (a
refused one-shot crawl writes nothing — no `crawler_runs` row, byte-identical
file); `crawler_runs.id` remains execution telemetry and is not
compatibility authority; event persistence cannot begin before state
admission; no daemon-specific assumption is required.

## Health / refusal evidence

Source-proven refusal behavior: CLI exits 3 printing a machine-readable
`state_incompatible` record; the dashboard's read-write handlers and
read-only data APIs return 503 with the same evidence; health appends a
`persistent_state:` reason and degrades for unadmittable states; the
launcher and `sync_registry_before_serve` surfaces name the compatibility
gate instead of masking the refusal as a generic "sync skipped"; a
dashboard-triggered crawl records the refusal as its failure outcome with
the evidence attached. Exit codes and state names are target-local facts,
not normative fleet requirements.

## Version-skew contract

`FORWARD_ONLY_EXPLICIT`: v8+ state fails closed under v7 software; additive
migrations are not treated as backward-compatibility proof; no downgrade or
rollback compatibility is claimed. Target-local, not fleet-normative.

## OPS-COM-003 non-applicability preserved

`STD-OPS-COM-003 = NOT_APPLICABLE` (M9b) is preserved untouched. The
compatibility barrier adds no qualification gate, no qualification epochs,
and no maturity machinery — asserted by a dedicated test that pins the
migration set at 2..7 and the schema free of qualification concepts.
`crawler_runs.id` remains telemetry/execution identity only.

## Validation evidence

Baseline at parent `d720e063`: **545 passed, 2 skipped, 0 failed, exit 0**.
M15 at `79fbee63`: **572 passed, 2 skipped, 0 failed, exit 0** — the full
suite is GREEN with no baseline attribution needed. New M15 tests:
27 passed. This recording pass independently re-ran the focused suites
(compatibility, db lifecycle, run lock, crawl trigger: 82 passed) and
verified all A–AD source claims mechanically (31/31) against the canonical
SHA.

## Implementation checks (named)

A expected state contract explicit: YES. B inspection read-only: YES.
C fresh distinguishable from unknown: YES. D unknown silently compatible:
NO. E old unmigrated state normal work: NO. F newer incompatible state
normal work: NO. G missing authority existing state can bootstrap: NO.
H corrupt/partial normal work: NO. I canonical migration authoritative:
YES. J migration reverified: YES. K failed migration can mark ready: NO.
L every operational state path guarded: YES. M direct normal consumer can
bypass: NO. N one-shot execution can bypass due to ephemerality: NO.
O event persistence before compatibility: NO. P old software silently
accepts newer state: NO. Q normal v7 behavior intact: YES. R OPS-COM-003
applicability decision intact: YES.

## Verdict

`STD-DEPLOY-COM-002` = **CONFORMS / CLOSED** at
`79fbee63ee3a43badad085671ba5bf6837b627f7`, scope: source-level
persistent-state compatibility only. This implies no live deployment
state, no production migration, no `STD-DEPLOY-COM-001` closure, and no
full OEM Radar conformance. `STD-UI-COM-011` and `STD-DEPLOY-COM-001`
remain unresolved; `STD-OPS-COM-003` remains NOT_APPLICABLE.

## Family comparison and result

Shared contract, satisfied independently by both members: read-only-first
inspection → fresh-vs-unknown distinction → fail closed on
unknown/incompatible state → canonical bootstrap/migration for known-safe
state only → post-migration verification → normal work only after
compatibility proof → explicit version-skew posture → evidence-bearing
refusal → complete operational-path coverage.

Meaningful differences (recorded, neither exceptional nor contradictory):
Feature Phone v5 with qualification tables sharing the main store, a
separate exact-shape QC-archive gate, longer-lived operator surfaces, and
existing OPS-COM-003/004 closures; OEM Radar v7 with marker-vs-structure
corroboration, no active second versioned store, a one-shot crawl
architecture, a more severe pre-existing defect (schema overlay plus
error swallowing), and OPS-COM-003 NOT_APPLICABLE.

`CURRENT_SCHEMA_BOOTSTRAP_SQLITE_COMPATIBILITY_RECIPE_VALIDATED` is
descriptive process evidence across exactly two members: Feature Phone
`b60e881319b16d36625268d9ba2d66cb8ea8f818` and OEM Radar
`79fbee63ee3a43badad085671ba5bf6837b627f7`. This is not a new standard.
CTW: NO CONFORMANCE INHERITANCE, NO EVIDENCE INHERITANCE, NO IMPLEMENTATION
PRESCRIPTION. Smartwatch: NO CONFORMANCE INHERITANCE, NO EVIDENCE
INHERITANCE, NO IMPLEMENTATION PRESCRIPTION. Nothing is generalized
further.

Exactly one narrow OEM Radar Deployment fact is admitted; the Watch,
Semiconductor, KTW, Tablet, and Feature Phone admissions remain preserved,
as does OEM Radar's M1 insufficiency history. No host, deployment,
collector, production-DB, production-migration, restart, or target
modification occurred in this pass. Frozen Deployment standard files and
immutable tags were not changed or moved.
