# Smartwatch Clank — M18 persistent-state compatibility evidence

```json
{"clank":"smartwatch-clank","date":"2026-09-02","findings":[{"standard":"STD-DEPLOY-COM-002","kind":"conformance","summary":"CONFORMS / CLOSED at canonical Smartwatch main revision a93355480bb11e1bd16ae7837256ce9002fc2aa7: the retained durable monotonic schema_version v3 marker (single row, id=1), structurally corroborated against the expected 17-table contract plus the complete runs column set, sits behind a read-only-first compatibility barrier — read-write construction inspects through a mode=ro handle before any mutating open, compatible state opens with zero schema writes (hash-proven byte-identical), only genuinely fresh or source-proven historical pre-marker (v1/v2 runs-only) state may enter the canonical additive _migrate() and is re-verified read-only afterwards, arbitrary marker-less state is UNKNOWN and fails closed, and newer/partial/contradictory/malformed/corrupt/failed-migration state fails closed with evidence across CLI run, read-only inspection commands, scheduler, dashboard, local collection, and the independent QC archive gate."}]}
```

This Standards-only M18 record closes `STD-DEPLOY-COM-002` at
`a93355480bb11e1bd16ae7837256ce9002fc2aa7`, source-level persistent-state
compatibility only. It does not imply deployed M18 state, production
database compatibility, any live deployment action, or
`STD-DEPLOY-COM-001` closure. `STD-UI-COM-011` and `STD-DEPLOY-COM-001`
remain unresolved; `STD-OPS-COM-003` remains independently closed at M5
and was not re-ratified here; no overall Smartwatch conformance is
claimed.

## Lineage and history

Standards takeover was `40ed95c44f1402a88be66260402d1b2c53475394`
(origin/master, clean); the Smartwatch parent was
`a631421e276b58ce3499787cc2bc72218648ce72` (the M5 OPS-COM-003
qualification-closure revision); the canonical recorded revision is
`a93355480bb11e1bd16ae7837256ce9002fc2aa7` (pushed to `origin/main` and
verified before this pass). M1 recorded `STD-DEPLOY-COM-002` as
`INSUFFICIENT_EVIDENCE` — preserved. M10 had classified the target
`APPLIES` / `PARTIAL_MECHANISM` with an inline additive SQLite
schema-version mechanism, monotonic marker, no explicit compatibility
comparison or barrier, `UNGUARDED` rollback posture, and risk `HIGH`.

## The original Smartwatch defect (preserved)

Before M18, Smartwatch **did** have a schema marker. The defect was
**marker-without-admission-barrier plus mutation-before-compatibility**,
not "no marker":

- `schema_version` (single row, `id = 1`) existed as a durable, monotonic
  authority, advanced only upward.
- `_migrate()` ran unconditionally on every read-write construction:
  the full current-schema `executescript`, guarded additive `ALTER TABLE`
  logic, and the marker stamp could all execute before any compatibility
  classification existed.
- Because the marker was monotonic and never compared against a maximum
  supported version, older code encountering newer state simply left the
  newer marker untouched and proceeded — the monotonic stamp silently
  declined to move and nothing failed.
- Missing-marker existing state could be treated like fresh/upgradeable
  state and laundered toward "current" by ordinary construction.
- There was no explicit fail-closed version comparison anywhere.

M18 supersedes the defect for the canonical SHA; the history is not
erased.

## Schema authority

`schema_version` — a single-row SQLite table (`id = 1`), durable and
monotonic, expected **v3** (`EXPECTED_SCHEMA_VERSION = 3` in
`core/schema_state.py`, re-exported by `SQLiteStore.SCHEMA_VERSION` so
the schema, the migration stamp, and the compatibility gate cannot
drift). The existing mechanism was **retained, not replaced**: M18's fix
turns the pre-existing marker into an actual compatibility authority by
placing read-only admission before mutation and corroborating the marker
against structure. The marker alone is not sufficient and is not
described as sufficient.

## Structural corroboration and its honest limits

Verified (source-proven): every expected table of the v3 contract — the
**17-table contract** including `runs`, the qualification tables, and
the `schema_version` authority itself — plus the **complete expected
`runs` column set** (original v1 columns plus every guarded
`ADD COLUMN` the store has shipped). `runs` is checked because it is the
only table the additive migration mechanism has ever `ALTER`ed, so it is
exactly where historical additive evolution can contradict the marker. A
marker claiming v3 over missing structure is PARTIAL.

Explicitly **not** claimed: column type equivalence, nullability or
constraint equivalence, index equivalence, or any byte-for-byte DDL
fingerprint — the source performs no such checks and none are asserted.
The structural check corroborates the marker; it does not replace it.

## Historical pre-marker generation — the Smartwatch-specific nuance

Smartwatch genuinely had a source-proven pre-marker generation: the
`schema_version` table was introduced during the Expansion Stage, and
existing source/tests preserve the honest historical `runs`-only shape
at the historical v1 and v2 column sets (`LEGACY_GENERATIONS` in
`core/schema_state.py`). M18 recognizes **only that source-proven
historical shape** as `MIGRATION_REQUIRED`:

- recognition is structural and narrow — the database must contain
  exactly the `runs` table at one recognized historical generation's
  exact column set; nothing else qualifies;
- an arbitrary marker-less existing database does **not** qualify and is
  `UNKNOWN`, failing closed;
- recognized historical state routes through the canonical additive
  `_migrate()` only, and is re-verified read-only afterwards.

This is a legacy-generation compatibility rule. It is **not** silent
grandfathering, not generic marker-less adoption, and **not** CTW's
operator `LEGACY_UNADOPTED` adoption — that terminology is CTW-local and
is deliberately not used for Smartwatch.

## FRESH != UNKNOWN != MIGRATION_REQUIRED

Three states are preserved distinctly:

- **FRESH**: zero user tables (or a missing database file) — canonical
  bootstrap may create the store through `_migrate()`.
- **UNKNOWN**: an existing database with tables but no `schema_version`
  authority that does not match a recognized historical generation — it
  is not fresh, must not be bootstrapped, must not be stamped, and fails
  closed everywhere.
- **MIGRATION_REQUIRED**: older marked state (v1/v2) or recognized
  historical pre-marker state — admissible only through the canonical
  migration path with explicit re-verification.

## Compatibility model

Exact source names (`SchemaState` in `core/schema_state.py`): `FRESH`,
`MIGRATION_REQUIRED`, `COMPATIBLE`, `INCOMPATIBLE_NEWER`, `UNKNOWN`,
`CORRUPT`, `PARTIAL`. Pinned semantics from the source docstring:
`FRESH != UNKNOWN`; `MARKER_PRESENT != COMPATIBLE`; `DB_OPENED !=
COMPATIBLE`; `MIGRATION_CAN_RUN != COMPATIBLE`; `STRUCTURE_EXISTS !=
COMPATIBLE`. State names are Smartwatch-local and are not normative
across the fleet. The independent QC archive gate uses its own narrower
internal strings (`FRESH`/`COMPATIBLE`/`CORRUPT`/`UNKNOWN_OR_WRONG_SHAPE`
mapped onto UNKNOWN/CORRUPT verdicts) and introduces no version lineage.

## Read-only-first ordering

Compatibility inspection occurs **before** the read-write connection
that can run `executescript`, `CREATE TABLE`, `ALTER TABLE`, marker
writes, or migrations: `SQLiteStore.__init__` calls
`_admit_compatibility()`, which opens the existing file through a
`mode=ro` URI handle and adjudicates it with `inspect_schema` (strictly
read-only: quick_check, table inventory, `PRAGMA table_info`) before any
writable connection is created. A compatible v3 store opens with zero
schema writes — hash-proven byte-identical by tests (`test_5`,
`test_23b`), as is the refusal of incompatible state (hash-proven for
newer, missing-marker, and CLI refusal paths). The CLI's inspection
commands gate with `inspect_store` before their read-only opens.
Byte-identity is claimed only where tests prove it; no broader
filesystem guarantee is asserted.

## Migration and failure semantics

The canonical additive `_migrate()` remains authoritative. Only FRESH or
recognized MIGRATION_REQUIRED state may enter it; migration never runs
on current COMPATIBLE state and never runs on UNKNOWN, newer, corrupt,
or partial state. Successful migration/bootstrap is re-inspected
read-only and must observe COMPATIBLE before the store is admitted.
Failed migration raises with the failure preserved as evidence and the
store never marked ready (test-proven: a sabotaged migration leaves the
file at its prior MIGRATION_REQUIRED state, unadmitted). Marker
advancement occurs only through the canonical migration's monotonic
stamp logic. No version lineage is fabricated beyond the source-proven
v1/v2/v3 history.

## Version-skew contract

`FORWARD_ONLY_EXPLICIT`: v3 software encountering a v4+ marker fails
closed as `INCOMPATIBLE_NEWER` (test-proven at v4 and v5, byte-identical
refusal). Additive migrations do not prove backward compatibility;
SQLite's tolerance for extra columns is explicitly not compatibility; no
downgrade path exists or is claimed. Target-local, not fleet-normative.

## Entry points and bypass result

Independently verified against the canonical source:

- **CLI `run`** (the scheduler's command): barrier inside the store
  constructor; `SchemaStateError` is caught and emitted as structured
  JSON evidence (`gate: persistent_state_compatibility`, full report) with
  exit code 3, file untouched.
- **Portable soak runner / scheduler**: invokes `python -m
  smartwatch_clank.cli run --trigger SCHEDULED` — guarded by the same CLI
  barrier; no separate store path exists.
- **CLI inspection commands** (`health`, `discoveries`, `candidates`,
  `reconciliation`, `soak`): explicit `inspect_store` gate first; refuses
  unadmittable state *and* MIGRATION_REQUIRED (read-only surfaces cannot
  migrate) with exit 3 and evidence; then opens `read_only=True`
  (mode=ro, never migrates). Health on a genuinely fresh database
  reports "not initialized" rather than fabricating status.
- **`backup`**: read-only store construction (mode=ro URI); inspection-
  class — it never migrates and never gates, and copies whatever schema
  the source already has. It admits no normal work; every real writer
  was already gated by its own non-read-only construction.
- **Dashboard render**: `render_dashboard` constructs the store through
  the same barrier — incompatible state raises and the request fails
  rather than serving state as fact. The QC-decision endpoint catches
  `SchemaStateError` and returns a structured 503 evidence payload; the
  run endpoints surface the gate refusal as a 500 error payload.
- **Local collection controller**: catches `SchemaStateError` before any
  collection runs and records the refusal as the controller's outcome
  (failed state + evidence).
- **`run_finalized`** (dashboard "Run All"/per-collector): guarded by the
  store constructor barrier.
- **Direct store constructors** (any normal consumer): the barrier is in
  `__init__` itself — there is no writable store path that does not pass
  through `_admit_compatibility`.
- **`identity` / `scope` / `collectors`**: do not touch the SQLite
  store; the continuity registry is a hash-chained JSONL sidecar outside
  the relational store and is not a schema authority.

**NO UNEXPLAINED NORMAL_BYPASS.** Read-only inspection paths are
classified as inspection, not as mutating normal paths.

## Qualification orthogonality (OPS-COM-003 preserved)

`STD-OPS-COM-003` was closed at M5 on the parent revision
`a631421e276b58ce3499787cc2bc72218648ce72` and remains closed; it was
not re-audited or re-ratified here beyond regression preservation.
Compatibility is established independently of qualification: the
compatibility barrier is the store construction itself, so qualification
provenance, epochs, and gates all live **inside** an already-admitted
store and cannot bypass state admission (test-proven). The M5
SCHEDULED/MANUAL/UNKNOWN provenance semantics remain intact, and the
focused qualification/provenance suites pass on the canonical SHA
(20 passed).

## QC archive

Independent of the primary authority: one `qc_decisions` table, exactly
one schema shape, **no** version history, **no** invented `schema_version`
lineage, no numbered migrations, and no shared `schema_version` authority.
Read-only inspection first; a fresh file bootstraps canonically and is
re-inspected after bootstrap; the exact known `qc_decisions` shape
proceeds unchanged; wrong-shape, foreign-table, and corrupt state is
refused with evidence instead of being silently patched by
`CREATE TABLE IF NOT EXISTS`.

## Validation evidence

As reported by the M18 remediation pass: baseline at parent
`a631421e` — **251 total, 248 passed, 1 skipped, 2 failed, exit 1**;
post-M18 at `a9335548` — **276 total, 273 passed, 1 skipped, 2 failed,
exit 1**; **25 new M18 tests** reported passed.

This recording pass independently re-ran both ends in its own
environment (Windows, `python -m pytest`): baseline parent — **246
collected, 243 passed, 1 skipped, 2 failed, exit 1**; canonical M18 —
**268 collected, 265 passed, 1 skipped, 2 failed, exit 1**; and a
collect-only diff proving **exactly 22 new tests, all in
`tests/test_m18_schema_state.py`**, with no other collection change.
The absolute totals differ between the M18 report and this pass's
environment (a collection-environment difference, recorded honestly
rather than reconciled by assumption); **every material invariant holds
in both**: the same two `dcrainmaker_specialist` failures
(`test_tier_and_name`,
`test_specialist_joins_experimental_scope_not_production`) are present
at baseline and unchanged after M18; M18 introduced **no new
full-suite failures**; all new M18 tests pass; focused rerun of the M18
plus qualification/provenance/QC suites this pass: **42 passed**.

Classification: **NON_GREEN_FULL_SUITE** with **PRE_EXISTING /
BASELINE_ATTRIBUTED** failures. The full suite is **NOT green** and is
not claimed green; 268/276 collected totals must never be read as "all
passed".

## Implementation checks (named)

A expected schema version explicit (v3, single authority constant):
YES. B compatibility inspection read-only (mode=ro adjudication before
any writable open): YES. C fresh distinguishable from unknown: YES.
D unknown silently proceeds: NO. E old unmigrated state performs normal
work: NO. F newer incompatible state performs normal work: NO.
G missing-authority existing state silently bootstraps: NO.
H corrupt/partial state performs normal work: NO.
I marker sufficiently corroborated against structure: YES.
J canonical migration authoritative: YES. K migration reverified: YES.
L failed migration can mark ready: NO.
M every normal DB path guarded: YES.
N direct normal consumer bypass exists: NO.
O qualification can bypass compatibility: NO.
P health/dashboard silently repair incompatible state: NO.
Q old software silently accepts newer state: NO.
R normal v3 behavior intact: YES.
S OPS-COM-003 remains intact: YES.

## Verdict

`STD-DEPLOY-COM-002` = **CONFORMS / CLOSED** at
`a93355480bb11e1bd16ae7837256ce9002fc2aa7`, scope: source-level
persistent-state compatibility only. This does not imply live deployed
compatibility, production database compatibility proof,
`STD-DEPLOY-COM-001` closure, or full Smartwatch conformance.

## Remaining Smartwatch findings

Preserved unresolved: **STD-UI-COM-011** and **STD-DEPLOY-COM-001**.
Preserved closed: **STD-OPS-COM-003** (M5, parent revision). Smartwatch
is not called fully conforming.

## Family status

`FIRST_VALIDATED_MEMBER_OF_ADDITIVE_SCHEMA_MARKER_COMPATIBILITY` is
descriptive process evidence naming exactly one member: Smartwatch
`a93355480bb11e1bd16ae7837256ce9002fc2aa7`. Family-defining
characteristics: a durable monotonic marker pre-existed; the marker
lacked fail-closed admission semantics; a read-only comparison was added
before mutation; the marker is structurally corroborated; historical
source-proven pre-marker generations are recognized narrowly; canonical
additive migration is retained; arbitrary marker-less state fails
closed; newer state fails closed. This is not a new standard and is not
merged with `ALEMBIC_HEAD`, `NUMBERED_SQLITE`,
`CURRENT_SCHEMA_BOOTSTRAP`, or `CREATE_ALL_WITH_EXPLICIT_AUTHORITY`.

## Non-inheritance

**Watch: NO SMARTWATCH COM-002 EVIDENCE INHERITANCE, NO IMPLEMENTATION
INHERITANCE. OEM Radar: NO SMARTWATCH COM-002 EVIDENCE INHERITANCE, NO
IMPLEMENTATION INHERITANCE. CTW: NO SMARTWATCH COM-002 EVIDENCE
INHERITANCE, NO IMPLEMENTATION INHERITANCE.** No other target inherits
Smartwatch conformance, evidence, or implementation.

Exactly one narrow Smartwatch Deployment fact is admitted (Smartwatch +
`a93355480bb11e1bd16ae7837256ce9002fc2aa7` + `STD-DEPLOY-COM-002` +
CONFORMS/CLOSED), bringing the Deployment known-evidence index to 8
facts; all prior admissions are preserved, as is Smartwatch's M1
insufficiency history. No `DEPLOY-COM-001`, `UI-COM-011`, or additional
`OPS-COM-003` fact was admitted. No host, deployment, collector,
production-DB, migration, restart, or target modification occurred in
this pass; Smartwatch was not modified. Frozen Deployment standard files
and immutable tags were not changed or moved.
