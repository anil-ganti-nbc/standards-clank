# Feature Phone Clank — M14 persistent-state compatibility evidence

```json
{"clank":"feature-phone-clank","date":"2026-09-02","findings":[{"standard":"STD-DEPLOY-COM-002","kind":"conformance","summary":"CONFORMS / CLOSED at canonical Feature Phone main revision b60e881319b16d36625268d9ba2d66cb8ea8f818: SqliteStore and the QC archive each sit behind a read-only-first compatibility barrier that inspects through a mode=ro handle before any mutable setup, admits only genuinely fresh or known-older state through the canonical bootstrap/migration path with explicit re-verification, and leaves every refused file byte-identical — newer, unknown, corrupt, partial, and failed-migration state fails closed with compatibility evidence on CLI, dashboard, controller, and health surfaces."}]}
```

This Standards-only M14 record closes `STD-DEPLOY-COM-002` at
`b60e881319b16d36625268d9ba2d66cb8ea8f818`, source-level persistent-state
compatibility only. It is not live deployment proof, not a production
database migration, and not production-state convergence. `STD-DEPLOY-COM-001`
and `STD-UI-COM-011` remain unresolved; no overall Feature Phone conformance
is claimed.

## Lineage and history

Standards takeover was `ec83824d109263b1ae7ee92b02f2f271fea4fe0b`; Feature
Phone parent was `4b7dce284f7c581395c5efe2b20ce1872e26897e`; the canonical
recorded revision is `b60e881319b16d36625268d9ba2d66cb8ea8f818` (pushed to
`origin/main` and verified before this pass). M1 (`4051b64`) recorded
`STD-DEPLOY-COM-002` as `INSUFFICIENT_EVIDENCE`; that history is preserved.
M10 classified Feature Phone `APPLIES`, `PARTIAL_MECHANISM`, risk `HIGH`:
"the v5 marker proves only that the local migration routine recorded
progress; it does not prove current code/state compatibility or fail closed
on unknown/newer/partial state."

## The original architectural defect (preserved)

Before M14, `SqliteStore.__init__` itself invoked migration. Ordinary store
construction therefore could: mutate persistent state before any
compatibility was established; treat opening as migration admission;
silently upgrade older state; misclassify an existing database without
`schema_migrations` as fresh; and let a v6+ database proceed under v5
software because no migrations remained to run. Rollback/version-skew
behavior was unguarded. M14 supersedes this defect for the canonical Feature
Phone SHA; the history is not erased.

## Read-only-first barrier

The strongest property, recorded prominently: compatibility inspection
occurs through a `mode=ro` SQLite handle **before** the mutable read-write
connection, the WAL pragma, or any migration/bootstrap exists. A refusal is
raised before any read-write handle is created, and refusal tests establish
the refused file remains **byte-identical** — "inspection is logically
non-mutating" is weaker than "the refused persistent file remains
byte-identical", and Feature Phone proves the latter. Inspection itself
(quick_check, sqlite_master, table_info) contains no write statements.

## Compatibility state model (source-proven)

`FRESH`, `MIGRATION_REQUIRED`, `COMPATIBLE`, `INCOMPATIBLE_NEWER`,
`UNKNOWN`, `CORRUPT`, `PARTIAL`. Semantics: `FRESH != UNKNOWN` (a database
with tables but no version authority is UNKNOWN, never fresh);
`DB EXISTS != COMPATIBLE`; `DB OPENED != COMPATIBLE`; `TABLE EXISTS !=
COMPATIBLE` (a marker at the expected version is corroborated against the
full expected table set, else `PARTIAL`). Only genuinely fresh state
bootstraps canonically; existing state with missing, untrustworthy,
contradictory, or partial authority fails closed. Expected schema authority
is explicit v5 (`EXPECTED_SCHEMA_VERSION`, re-exported as `SCHEMA_VERSION`).

## Real local v4 observation — carefully scoped

A read-only observation recorded `data/feature_phone_clank.db` at schema v4
(`schema_migrations` 1–4, qualification tables absent, quick_check ok). The
file was **not** migrated and **not** modified during M14; this is **not**
production deployment proof and not a normal mutable open against the
original file. The valid inference only: under the canonical M14 source that
state classifies `MIGRATION_REQUIRED`, and the permitted path is
compatibility inspection → canonical migration to v5 → explicit
re-verification → normal work. The existing production-copy test exercised
the v4→v5 path on a **COPY**, preserving all 44 products — copy-based
evidence, not production migration.

## QC archive

The QC archive (`feature_phone_clank_qc.db`) has its own narrow, separate
compatibility gate: an exact-known-shape check against `table_info`. Known
pre-M14 archives are grandfathered only where the source can establish the
expected shape honestly; unknown, foreign-table, wrong-shape, and corrupt
archive state is refused with evidence. It is not a numbered-schema family
and no version metadata is invented for it.

## Migration and failure semantics

Compatibility inspection precedes migration; canonical `_MIGRATIONS` remain
authoritative; bootstrap is restricted to genuinely fresh state; valid older
state migrates in one transaction (BEGIN IMMEDIATE, rollback on failure);
successful migration and bootstrap are re-inspected before the store is
handed back; failure cannot mark state ready (`admission_failure` evidence,
version authority not advanced, retry re-crosses inspection); incompatible
state is preserved for diagnosis, never deleted or reconstructed. No
production migration occurred in M14.

## Version-skew contract

`FORWARD_ONLY_EXPLICIT`: older Feature Phone software does not silently
accept newer incompatible persistent state (v6+ fails closed for software
expecting v5); no downgrade or rollback compatibility is claimed or
invented. This is a target-local contract, not translated into a fleet-wide
requirement.

## Entry points and bypass search

Independent repository-wide search confirms every normal operational path is
guarded behind the compatibility barrier: nine state-touching CLI commands
(exit 3 with a machine-readable evidence record), dashboard render and QC
POST (503 with evidence page/JSON), local-collection controller workers
(blocked state + evidence), qualification-facing store access, direct normal
`SqliteStore` construction, the QC archive gate, and runtime health reporting
(`persistent_state:` reason plus degraded for unadmittable states).
Read-only inspection paths (`connect_readonly`, the health probe) remain
read-only inspection paths; migration/bootstrap internals remain
migration/bootstrap-only; test-only `:memory:` paths are not production
bypasses. **NO UNEXPLAINED NORMAL_BYPASS.**

## Lock / qualification orthogonality

`STD-OPS-COM-003` and `STD-OPS-COM-004` remain closed; their regressions
were re-run and pass. A held authoritative run lock cannot admit
incompatible persistent state, and qualification evidence cannot admit
incompatible persistent state: compatibility is an independent prerequisite
(dedicated tests prove both directions).

## Validation evidence (honest)

Focused, re-run independently during this recording pass: M14 compatibility
34 passed; DB migrations 2; qualification 3; run lock 6;
scope/collector/dashboard operational checks 26. Full suite at parent
`4b7dce2`: **218 passed, 1 skipped, 4 failed**. Full suite at M14
`b60e881`: **252 passed, 1 skipped, 4 failed, exit 1**. The full suite is
**NOT green** and is not recorded as green. The same four failures existed
at baseline and remained unchanged — 3 shared `clank_runtime`/`HealthPayload`
Pydantic contract-drift failures and 1 Windows Python 3.14 subprocess-handle
flake — classified `PRE_EXISTING / BASELINE_ATTRIBUTED`. No new full-suite
failure was introduced by M14; all 34 new M14 tests passed.

## Implementation checks (named)

A expected state contract explicit: YES. B compatibility inspection
read-only: YES. C fresh distinguishable from unknown: YES. D unknown silently
compatible: NO. E old unmigrated normal work: NO. F newer incompatible
normal work: NO. G missing authority existing state silently bootstraps: NO.
H corrupt/partial state normal work: NO. I canonical migration/bootstrap
authoritative: YES. J successful migration reverified: YES. K failed
migration can mark ready: NO. L every operational state path crosses
barrier: YES. M direct normal DB consumer can bypass: NO. N lock ownership
can bypass compatibility: NO. O qualification can bypass compatibility: NO.
P old software silently accepts newer state: NO. Q normal v5 behavior
intact: YES. R OPS-COM-003 remains intact: YES. S OPS-COM-004 remains
intact: YES.

## Verdict

`STD-DEPLOY-COM-002` = **CONFORMS / CLOSED** at
`b60e881319b16d36625268d9ba2d66cb8ea8f818`, scope: source-level
persistent-state compatibility only. This implies no live deployment
compatibility, no production database migration, no production-state
convergence, no `STD-DEPLOY-COM-001` closure, and no full Feature Phone
conformance. `STD-UI-COM-011` and `STD-DEPLOY-COM-001` remain unresolved.

## Family result

`FIRST_VALIDATED_MEMBER_OF_CURRENT_SCHEMA_BOOTSTRAP_SQLITE_COMPATIBILITY` is
descriptive and names exactly one member: Feature Phone
`b60e881319b16d36625268d9ba2d66cb8ea8f818`. Meaning: the
current-schema/bootstrap SQLite compatibility contract has been demonstrated
once — compatibility inspection and migration/bootstrap are separated,
unknown existing state is no longer laundered into current state, and
explicit fail-closed version-skew handling exists. OEM Radar inherits **NO
CONFORMANCE, NO EVIDENCE, NO IMPLEMENTATION PRESCRIPTION** and remains an
independent future target. Smartwatch and CTW inherit nothing.

Exactly one narrow Feature Phone Deployment fact is admitted; the KTW,
Semiconductor, Tablet, and Watch admissions remain preserved. No host,
deployment, collector, production-DB, production-migration, restart, or
Feature Phone modification occurred in this pass. Frozen Deployment standard
files and immutable tags were not changed or moved.
