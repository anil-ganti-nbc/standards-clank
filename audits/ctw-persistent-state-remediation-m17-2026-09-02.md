# Chinese Tech Wire — M17 persistent-state compatibility evidence

```json
{"clank":"chinese-tech-wire","date":"2026-09-02","findings":[{"standard":"STD-DEPLOY-COM-002","kind":"conformance","summary":"CONFORMS / CLOSED at canonical Chinese Tech Wire main revision c340a45ac8cfbab58d749dcbf78a7d703ca9cdb1: the new durable schema_meta v1 authority, corroborated by a deterministic 21-table required-column structural manifest, sits behind a read-only-first compatibility barrier — create_all is restricted to genuinely fresh bootstrap, structurally complete but marker-less databases are LEGACY_UNADOPTED and fail closed everywhere, promotion happens only through the explicit operator-only --adopt-current-schema action (structural proof before any write, re-verification after), and newer/partial/contradictory/corrupt state fails closed with evidence across CLI, session, dashboard, scheduled, and health surfaces."}]}
```

This Standards-only M17 record closes `STD-DEPLOY-COM-002` at
`c340a45ac8cfbab58d749dcbf78a7d703ca9cdb1`, source-level persistent-state
compatibility only. It does not imply deployed M17 state, real-database
adoption, production migration, or `STD-DEPLOY-COM-001` closure.
`STD-UI-COM-007`, `STD-UI-COM-011`, and `STD-DEPLOY-COM-001` remain
unresolved; `STD-OPS-COM-003` remains UNKNOWN; no overall CTW conformance
is claimed.

## Lineage and history

Standards takeover was `a78d2a4d2c55bc533d80770845aba65731ae3967`; CTW
parent was `1a47220c69e6bb91f2899a0508508c42254c9d5b`; the canonical
recorded revision is `c340a45ac8cfbab58d749dcbf78a7d703ca9cdb1` (pushed to
`origin/main` and verified before this pass). M1 recorded
`STD-DEPLOY-COM-002` as `INSUFFICIENT_EVIDENCE` — preserved. M16
classified the remediation family as
`CREATE_ALL_BOOTSTRAP_WITH_NEW_VERSION_AUTHORITY` after read-only recon;
M10 had recorded `APPLIES` / `STRUCTURAL_INFERENCE` / `UNGUARDED` skew /
risk `HIGH`.

## The original CTW defect (preserved)

Before M17, CTW had no durable schema or version authority of any kind.
`create_all` acted as implicit state admission on ordinary invocation —
including health and identity — silently filling missing tables in
existing databases; manual ALTER logic patched selected missing columns;
selected DDL failures were swallowed and execution continued; partial
marker-less state was repaired, masked, or tolerated; older code could
open newer state without any compatibility decision. This was not merely
"CTW lacked a version number": it was **mutation-as-admission without a
durable compatibility authority** — the act of opening state could erase
the evidence of incompatibility. M17 supersedes the defect for the
canonical SHA; the history is not erased.

## New primary authority

`schema_meta` — a single-row SQLite table recording the durable schema
version, expected **v1**, written only by canonical fresh bootstrap, the
explicit legacy-adoption action, or future marked migrations. It exists
precisely because the pre-M17 architecture offered no trustworthy durable
authority. The marker is never sufficient by itself: compatibility
requires the durable authority **plus** structural corroboration.
SQLAlchemy model metadata is not the durable authority; the expected
version is an explicit constant, never derived from package versions or
runtime model inspection.

## Structural corroboration and its honest limits

Verified: the required 21 application tables plus the authority itself,
and each table's required columns (the complete declarative column sets,
derived from the same models `create_all` bootstraps, so the manifest
cannot drift from a fresh bootstrap). Explicitly **not** claimed: SQL
type equality (SQLite type affinity makes it unreliable), index
equivalence (performance, not result correctness), and
nullability/constraint equivalence. The manifest corroborates the
marker — it does not replace it. A marker claiming v1 over missing
structure is PARTIAL.

## Compatibility model

`FRESH`, `LEGACY_UNADOPTED`, `MIGRATION_REQUIRED`, `COMPATIBLE`,
`INCOMPATIBLE_NEWER`, `UNKNOWN`, `CORRUPT`, `PARTIAL`. Pinned semantics:
`FRESH != LEGACY_UNADOPTED`; `LEGACY_UNADOPTED != MIGRATION_REQUIRED`;
`LEGACY_UNADOPTED != COMPATIBLE`; `DB_OPEN_SUCCESS != COMPATIBLE`;
`MARKER_EXISTS != COMPATIBLE`; `STRUCTURE_EXISTS != COMPATIBLE`;
`MIGRATION_CAN_RUN != COMPATIBLE`.

## LEGACY_UNADOPTED — first-class evidence

LEGACY_UNADOPTED means: existing, marker-less, structurally complete
enough to match the pre-M17 current schema, and not yet authorized under
the new durable authority. It is neither fresh bootstrap nor ordinary
migration. Normal operation — startup, sessions, health, dashboard,
scheduled collection — fails closed against it, and no ordinary code path
can promote it. It becomes COMPATIBLE only through explicit operator
adoption. The real local `ctw.db` sits in exactly this state, preserved.

## Explicit legacy adoption — a distinct authority transition

The operator action is `--adopt-current-schema` (exact source name). It
must be explicitly invoked; operates only on existing marker-less state
of the expected complete shape; performs the read-only structural proof
first (the LEGACY_UNADOPTED classification *is* the proof); performs no
repair before proof; refuses missing tables, missing required columns,
corrupt, partial, and contradictory/unknown state untouched; writes
`schema_meta` v1 only after proof; re-inspects afterwards; and reports
durable success/failure evidence. Adoption is a distinct authority
transition — it is not bootstrap and not migration, and it is never part
of ordinary initialization. An already-adopted store refuses re-adoption.

## Real ctw.db observation — strictly scoped

Observed read-only during M16/M17: structurally complete pre-M17 shape
(21 tables), no `schema_meta`, quick_check ok, with retained read-only
inventory counts (1,504 articles, 1,008 leads, 221 source_runs,
17 ingestion_runs) preserved as inventory only. The file remained
marker-less, LEGACY_UNADOPTED, and **byte-identical** — never adopted,
migrated, or initialized through a mutating path. This is **not**
DEPLOY-COM-001 proof, production adoption/migration proof, or evidence
that any deployed CTW binary runs M17.

## create_all restriction

`create_all` is permitted only for genuinely fresh primary bootstrap (and
isolated disposable test setup). It no longer acts as ordinary startup
repair, current-state admission, legacy adoption, migration, health
initialization, identity initialization, or dashboard repair — the source
contains exactly one call site, inside the fresh-bootstrap path behind
the genuine-fresh guard. This inversion is central to the family
evidence.

## Migration and failure semantics

No fabricated v0 lineage exists: v1 is the first marked version, and the
architecture for future marked migrations is established (known marked
older state → explicit canonical migration → authority advancement →
structural re-verification → compatible). Legacy marker-less adoption is
separate from that mechanism. Failed fresh bootstrap cannot mark ready
(it surfaces as an admission failure with evidence; the interrupted state
becomes LEGACY_UNADOPTED, recoverable only by adoption); failed adoption
cannot mark ready; DDL failures can no longer be silently swallowed
before normal work — the superseded `migrate_schema` path (with both
DANGEROUS_ADMISSION_MASKING sites) is deleted from the codebase;
contradictory state remains preserved for diagnosis.

## Health and identity — corrected

Before M17 both passed through mutating initialization. After M17:
`--identity` performs no state mutation merely to identify the service;
health is read-only and compatibility-aware — it reports
`persistent_state:` reasons and degraded/not-ready for LEGACY_UNADOPTED
(including explicit `--adopt-current-schema` guidance), INCOMPATIBLE_NEWER,
PARTIAL, UNKNOWN, and CORRUPT, and never creates, alters, stamps, adopts,
or repairs. Status names are CTW-local, not normative fleet requirements.

## Entry points and bypass result

Independently verified: scheduler and manual cycles (via `run_full_cycle`'s
gated initialization), CLI collection, dashboard startup (`run_gui`
surfaces an evidence-bearing refusal and exits; `create_app` propagates),
direct `get_session` consumers (session-level gate refuses unadmittable
state without mutating), source-health operations, health and identity
(read-only/untouched), the QC archive (own gate), and the adoption action
(ADOPTION_ONLY). `create_all`: BOOTSTRAP_ONLY. Read-only connections:
READ_ONLY_INSPECTION. **NO UNEXPLAINED NORMAL_BYPASS.**

## QC archive

Independent of the primary authority: one `qc_archive` table, no evolving
history, no invented `schema_meta` lineage. Fresh archives bootstrap
canonically; the exact known existing shape proceeds (the real local
archive grandfathers); wrong-shape, foreign-table, and corrupt state
fails closed with evidence.

## Version-skew contract

`FORWARD_ONLY_EXPLICIT`: `schema_meta` version > 1 fails closed under v1
software; SQLAlchemy's ORM tolerance for extra columns is explicitly not
compatibility; no downgrade path exists or is claimed. Target-local, not
fleet-normative.

## Validation evidence

Baseline at parent `1a47220c`: **369 passed, 0 failed, exit 0**. M17 at
`c340a45`: **409 passed, 0 failed, exit 0** — the full suite is GREEN,
no baseline attribution required. New M17 tests: **40 passed**. This
recording pass independently re-ran the focused suites (compatibility,
scheduler, runtime bridge, source health: **69 passed**) and verified all
A–AF source claims mechanically (**32/32**) against the canonical SHA.
Counts are kept separate; nothing was merged or rewritten.

## Implementation checks (named)

A explicit durable primary schema authority exists: YES. B expected
version explicit: YES. C compatibility inspection read-only: YES.
D structural corroboration exists: YES. E fresh distinguishable from
legacy-unadopted: YES. F legacy-unadopted silently proceeds: NO.
G legacy-unadopted silently stamps itself: NO. H adoption requires
explicit operator action: YES. I adoption verifies full structure first:
YES. J current compatible state performs normal work: YES. K newer state
performs normal work: NO. L partial/contradictory state performs normal
work: NO. M create_all runs during normal compatible startup: NO.
N create_all restricted to fresh bootstrap: YES. O successful
mutation/adoption reverified: YES. P failed migration/bootstrap/adoption
can mark ready: NO. Q DDL failure silently swallowed and normal work
continues: NO. R every normal DB path crosses barrier: YES. S direct
normal session/repository bypass exists: NO. T --health mutates schema:
NO. U --identity mutates schema: NO. V dashboard silently repairs/adopts
state: NO. W real local DB mutated by M17: NO. X OPS-COM-003
classification changed: NO.

## Verdict

`STD-DEPLOY-COM-002` = **CONFORMS / CLOSED** at
`c340a45ac8cfbab58d749dcbf78a7d703ca9cdb1`, scope: source-level
persistent-state compatibility only. This does not imply deployed M17
state, real-DB adoption, production migration, `STD-DEPLOY-COM-001`
closure, or full CTW conformance. `STD-UI-COM-007`, `STD-UI-COM-011`, and
`STD-DEPLOY-COM-001` remain unresolved; `STD-OPS-COM-003` remains UNKNOWN
(resolver/evidence state, not altered by M17; no qualification machinery
introduced; compatibility evidence is not qualification evidence).

## Family status

`FIRST_VALIDATED_MEMBER_OF_CREATE_ALL_WITH_EXPLICIT_SCHEMA_AUTHORITY` is
descriptive process evidence naming exactly one member: CTW
`c340a45ac8cfbab58d749dcbf78a7d703ca9cdb1`. Family-defining
characteristics: create_all previously functioned as implicit authority; a
durable schema authority was introduced explicitly; structural
corroboration remains independent; create_all is restricted to genuinely
fresh bootstrap; marker-less legacy state becomes LEGACY_UNADOPTED;
adoption is explicit and separate from bootstrap/migration; the read-only
barrier precedes normal work; newer/partial/unknown state fails closed.
This is not a new standard and is not merged with ALEMBIC_HEAD,
NUMBERED_SQLITE, or CURRENT_SCHEMA_BOOTSTRAP_SQLITE.

Smartwatch: **NO CONFORMANCE INHERITANCE, NO EVIDENCE INHERITANCE, NO
IMPLEMENTATION PRESCRIPTION.** Smartwatch remains an independent future
target; nothing here infers that its schema architecture needs legacy
adoption or `schema_meta`.

Exactly one narrow CTW Deployment fact is admitted; the Watch,
Semiconductor, KTW, Tablet, Feature Phone, and OEM Radar admissions remain
preserved, as does CTW's M1 insufficiency history. No host, deployment,
collector, production-DB, adoption, migration, restart, or target
modification occurred in this pass. Frozen Deployment standard files and
immutable tags were not changed or moved.
