# Fleet Wiring M10 -- Persistent-State Compatibility Planning

```json
{"clank":"fleet-persistent-state-compatibility-planning","date":"2026-09-01","findings":[]}
```

Date: 2026-09-01  
Mode: read-only fleet classification and remediation design  
Controlling standard: `STD-DEPLOY-COM-002` v1  
Standards takeover: `043612756452fc9db871833425c2a641b68e00c3`

## Decision summary

All seven affected targets have durable structured state whose schema or
compatibility contract can evolve independently, so all seven are
`APPLIES`. None is promoted to conformance by this planning pass. The common
finding is not "no migrations": most targets have a migration or schema setup
routine, but normal work is not uniformly preceded by a trustworthy,
fail-closed compatibility decision with an auditable refusal reason.

The seven targets fall into five implementation families:

1. **Alembic migration head:** Semiconductor Intelligence.
2. **Current-schema bootstrap plus numbered SQLite history:** OEM Radar and
   Feature Phone.
3. **Ordered numbered SQLite history:** Korean Tech Wire and Tablet.
4. **Inline additive SQLite with a monotonic marker:** Smartwatch.
5. **Structural SQLAlchemy `create_all` plus ad hoc ALTER:** Chinese Tech Wire.

The safest order validates one target per family before a paired rollout:
Semiconductor, KTW, Feature Phone, Tablet, Smartwatch, OEM Radar, then CTW.
The order is deliberately not a mandate to copy storage code; it validates the
implementation-neutral barrier contract while preserving target-local
mechanics.

## Governing contract

The frozen standard says:

> A Clank whose trigger is met MUST prevent normal work from being admitted
> while the deployed code and required persistent-state contract are known to
> be incompatible. It MUST determine compatibility at a barrier that occurs
> before normal incompatible work is accepted, fail closed on known
> incompatibility, and preserve evidence sufficient to identify compatibility
> gating as the reason normal work was refused. The barrier may be deploy
> preflight, startup, first normal transaction, or another trustworthy gate;
> deployment ordering and mechanism are not prescribed.

Its trigger is persistent structured state with an independently evolving
schema or compatibility contract. Stateless, schema-less, and purely
ephemeral stores are trigger-unmet. The standard does not require Alembic,
numbered migrations, downgrade support, a particular rollout order, or a
destructive-state policy.

The planning contract is:

`identify intended software/state contract -> inspect persistent-state identity/version/shape -> establish compatibility before normal work -> fail closed on unknown/incompatible state -> migrate only through the canonical mechanism where allowed -> verify compatibility -> admit normal work`

Watch remains process precedent only. Its final evidence shows the desired
outcome; it does not inherit conformance to any other target.

## Takeover and scope

The Standards repository is on `master`, clean, and equals
`origin/master` at `043612756452fc9db871833425c2a641b68e00c3`.

| Target | Canonical branch | `HEAD = origin` | Tree |
|---|---|---|---|
| OEM Radar | `main` | `d720e0635894ddcc9a39f116e2aa4a1768090042` | CLEAN |
| Semiconductor Intelligence | `main` | `688b71a93b4988b5ce52ce85e46f09080b9a7948` | CLEAN |
| Chinese Tech Wire | `main` | `1a47220c69e6bb91f2899a0508508c42254c9d5b` | CLEAN |
| Korean Tech Wire | `main` | `2040af82136d8a8f181c464e7d62ce408dd2696d` | CLEAN |
| Feature Phone Clank | `main` | `4b7dce284f7c581395c5efe2b20ce1872e26897e` | CLEAN |
| Smartwatch Clank | `main` | `a631421e276b58ce3499787cc2bc72218648ce72` | CLEAN |
| Tablet Clank | `main` | `d9cb32ccee1b2bcaa4bc9d8af5ac1a7a7e7f6769` | CLEAN |

Smartphone Clank is intentionally out of scope. It was not flagged for this
gap by the canonical M1 sweep, and this pass found no bookkeeping evidence to
overturn that decision.

## Compatibility matrix

| Target | Persistent state / authority | Version authority and migration | Current barrier / bypass | Unknown/newer state and failure risk | Planning classification | Family / risk |
|---|---|---|---|---|---|---|
| OEM Radar | `data/radar.db` SQLite; raw files are supporting artifacts | `schema_migrations` 1-7, `SCHEMA_VERSION=7`; in-app numbered migration plus current-schema bootstrap; no downgrade | `SqliteStore.__init__` calls `migrate()` before `run_all`, but compares only max version; CLI, timer, cron, dashboard all share this path; read-only dashboard is a safe non-work bypass | Missing state can be bootstrapped; newer max version proceeds; partial DDL has no durable not-ready state | `NO_COMPATIBILITY_BARRIER` | Current-schema bootstrap numbered SQLite / HIGH |
| Semiconductor | SQLAlchemy database (SQLite default; URL-configurable) | Alembic chain, current qualification head `c7d8e9f0a1b2`; downgrade scripts exist, but `create_all` remains available | Dashboard and explicit install/update use `upgrade_or_stamp_to_head`; ordinary Typer sessions and runtime bridge call `Base.metadata.create_all`; broad "already exists" exception fallback stamps head | Common create-all paths fail open on missing/newer metadata; stamp fallback can mask structure; Alembic transaction safety is not universal | `PARTIAL_MECHANISM` | Alembic migration head / HIGH |
| CTW | `data/ctw.db` SQLAlchemy SQLite plus separate `data/qc_archive.db` | `Base.metadata.create_all` and `migrate_schema` use PRAGMA/ALTER; QC archive has create-if-not-exists; no durable version head | `init_db` runs in main CLI and dashboard startup; direct `get_session`/library use can bypass; QC archive is separate and unversioned | Missing/newer/corrupt shape is treated structurally; selected migration/index errors are caught or skipped; no not-ready record | `NO_COMPATIBILITY_BARRIER` | Structural SQLAlchemy create-all additive / HIGH |
| KTW | Main SQLite plus separate unversioned QC SQLite | Ordered `MIGRATIONS` 1-5 and `schema_migrations`; auto-applied in `Database.migrate`; no downgrade | CLI context migrates before dispatch and soak reuses it; direct `Database` use and QC archive can bypass expected-head proof | Older state auto-migrates; newer rows are ignored; migration errors stop that process but no durable refusal/readiness fact | `PARTIAL_MECHANISM` | Ordered numbered SQLite / MEDIUM |
| Feature Phone | Production and separate experimental SQLite stores; JSONL continuity is evidence, not schema authority | `schema_migrations` 1-5, `SCHEMA_VERSION=5`; current-schema bootstrap plus numbered migrations | Store construction migrates before production/experimental runner, health, status, and backup; direct runner accepts caller-supplied store | Missing marker can be treated as fresh/current; newer max proceeds; failed migration can leave marker/shape disagreement | `PARTIAL_MECHANISM` | Current-schema bootstrap numbered SQLite / HIGH |
| Smartwatch | Main SQLite, separate QC SQLite, continuity JSONL, and cache JSON | `SQLiteStore.SCHEMA_VERSION=3` and `schema_version(id=1)`; inline guarded additive DDL; QC archive has no version | Writer construction calls `_migrate`; CLI, soak, local collection share it; read-only backup intentionally skips migration; no expected/max-supported check | Missing/corrupt/newer marker and partial DDL are not fail-closed; sidecar stores have independent schema policy | `PARTIAL_MECHANISM` | Inline additive SQLite schema version / HIGH |
| Tablet | Canonical SQLite, separate QC SQLite, isolated campaign SQLite/JSONL | `schema_migrations` 1-3; inline ordered migration, including qualification projection; no downgrade | Most CLI commands construct `Database` before dispatch; campaign preflight opens canonical read-only then isolated DB; no compatibility comparison | Newer/corrupt/partial state can proceed; auto-migration has no durable not-ready state; QC remains unversioned | `PARTIAL_MECHANISM` | Ordered numbered SQLite / HIGH |

### Per-target source observations

**OEM Radar.** The persistent operational authority is the SQLite product,
source, snapshot, event, notification, and run state in
`src/oem_radar/providers/sqlite/schema.sql`. `SqliteStore.migrate()` executes
the current schema and then applies numbered statements based on the maximum
`schema_migrations.version`. No code contract is compared to that number.
`execute_crawl`, the one-shot timer/cron entry points, and
`CrawlController` all arrive at the same store constructor, which is useful
coverage but not a compatibility barrier. Newer state is not rejected and
there is no migration refusal record.

**Semiconductor Intelligence.** The Alembic chain is a real durable authority
and the latest checked-in head is `c7d8e9f0a1b2`. However, `_session()` and the
runtime bridge use `Base.metadata.create_all`, while `upgrade_or_stamp_to_head`
stamps the head whenever an exception contains "already exists". The dashboard
uses the Alembic-aware path at startup, but request/session and ordinary CLI
paths still make compatibility dependent on which function was reached first.
This is the clearest example of "migration framework" not equaling "pre-work
compatibility gate".

**Chinese Tech Wire.** `database/db.py` creates ORM tables and then applies
best-effort column/index patches. The separate QC archive has its own
create-if-not-exists schema and no version marker. Main CLI and dashboard
startup call `init_db`, but direct session/library callers can bypass it. The
source explicitly catches missing-table and index problems in migration helpers,
so a partial state can be silently treated as usable.

**Korean Tech Wire.** `Database.migrate()` has explicit numbered migrations
through version 5, including qualification tables. CLI `context()` calls it
before command dispatch, and soak uses the same runner. The QC archive is a
separate unversioned SQLite file. The main store has no expected-head or
maximum-supported comparison: applied rows are enough to proceed, so a newer
state can be opened by older code.

**Feature Phone.** The production and experimental stores use the same
`SqliteStore` with schema versions through 5. Version 5 adds qualification
state/epoch/event tables. The normal CLI opens a store before its runner, and
the explicit experimental path uses a separate DB, but the migration routine
does not establish a supported version range or durable failed/readiness state.
Continuity JSONL remains a separate evidence ledger and must not become schema
compatibility authority.

**Smartwatch.** `SQLiteStore` records a monotonic schema version 3 and uses
guarded additive DDL for main observations, qualification, and evidence state.
The QC archive and continuity/cache files evolve separately. All writers use
the store, but `_migrate()` updates the marker rather than comparing an
expected compatibility contract; a newer marker is left alone and accepted.
The read-only backup path intentionally skips migration, which is safe for
copying but cannot be treated as readiness evidence.

**Tablet.** `Database.migrate()` writes versions 1-3 and adds the qualification
projection. The regular CLI constructs the database before dispatch, while
`soak-campaign` preflights the canonical DB read-only and writes an isolated
campaign DB. That isolation is a strong state-safety measure, not a proof that
the campaign DB or canonical production DB is code-compatible. QC is a
separate, unversioned SQLite schema.

## Migration versus compatibility

The reusable remediation must preserve this distinction:

- **Migration framework:** changes or bootstraps persistent state and records
  some progress.
- **Compatibility barrier:** before normal work, proves the running software's
  required state contract is supported, refuses known/unknown incompatible
  state, and leaves an identifying refusal fact.

An excellent migration framework without a uniform fail-closed barrier remains
insufficient. Conversely, a target may conform with a simpler capability
contract if it can prove compatibility without elaborate migrations. No target
is currently marked `SOURCE_MECHANISM_PRESENT` or `RE-AUDIT_ONLY`; each needs a
barrier-focused implementation and independent proof.

## Family ledger

| Family | Members | Shared remediation shape | Target-local mechanics / risk |
|---|---|---|---|
| `ALEMBIC_MIGRATION_HEAD` | Semiconductor | Strict expected-head/capability gate; remove create-all bypass and broad stamping; persist refusal | ORM/Alembic URL and downgrade scripts remain local; stamp fallback is the key risk |
| `CURRENT_SCHEMA_BOOTSTRAP_NUMBERED_SQLITE` | OEM Radar, Feature Phone | Bound current-schema bootstrap with a maximum-supported contract, explicit ready/refused outcome, and tests for unmarked/newer/partial stores | OEM snapshot pipeline versus Feature production/experimental qualification scopes |
| `ORDERED_NUMBERED_SQLITE` | KTW, Tablet | Expected-head check, transactional/readiness result, and per-store refusal evidence | KTW main+QC versus Tablet canonical+campaign+QC; campaign isolation must remain independent |
| `INLINE_ADDITIVE_SQLITE_SCHEMA_VERSION` | Smartwatch | Validate supported version range and required capabilities before writer work; define sidecar policy | Main DB, QC archive, continuity, and read-only backup have different roles |
| `STRUCTURAL_SQLALCHEMY_CREATE_ALL_ADDITIVE` | CTW | Introduce explicit durable authority for operational and QC stores; stop swallowing compatibility failures | Dual store, direct-session bypass, and source-health pipeline create highest ambiguity |

## Ranked implementation order

1. **Semiconductor** -- strongest existing durable authority; validate a strict
   migration-head gate while removing the dangerous `create_all`/stamp bypass.
2. **Korean Tech Wire** -- clear ordered SQLite model and contained primary
   store; validate expected-head and refusal semantics.
3. **Feature Phone** -- validate the bootstrap family while preserving separate
   production/experimental scope and qualification history.
4. **Tablet** -- apply the ordered family independently across canonical,
   campaign, and QC stores; do not inherit KTW evidence.
5. **Smartwatch** -- adapt the contract to inline DDL, schema marker, QC, and
   continuity sidecars after the numbered families are proven.
6. **OEM Radar** -- reuse the bootstrap family after Feature Phone; one-shot
   scheduling lowers concurrency but not version-skew risk.
7. **Chinese Tech Wire** -- defer the highest-ambiguity dual-store design until
   explicit authority and failure semantics are validated elsewhere.

## Implementation-neutral regression recipe

Every later target implementation should prove all twelve cases:

1. Expected state version/capabilities permit startup and normal work.
2. Older migratable state cannot admit normal work before canonical migration
   and the barrier.
3. Newer incompatible state fails closed with a compatibility-specific refusal.
4. Missing version fails closed unless an explicit safe empty-state bootstrap is
   documented.
5. Corrupt or partial migration state fails closed.
6. Every operational entry point crosses the same compatibility barrier.
7. Compatibility inspection is non-destructive.
8. Migration runs only through the canonical mechanism.
9. Post-migration version/capabilities are verified before normal work.
10. Failed migration never records or infers `READY`.
11. Rollback/version-skew behavior matches the declared contract.
12. Fresh empty state/bootstrap works where explicitly supported.

## Applicability and safety disposition

| Target | `STD-DEPLOY-COM-002` planning applicability |
|---|---|
| OEM Radar | `APPLIES` |
| Semiconductor Intelligence | `APPLIES` |
| Chinese Tech Wire | `APPLIES` |
| Korean Tech Wire | `APPLIES` |
| Feature Phone Clank | `APPLIES` |
| Smartwatch Clank | `APPLIES` |
| Tablet Clank | `APPLIES` |

No applicability correction is warranted. No target is marked conforming by
planning alone. The Smartphone row is not added.

This pass is read-only. No target code, target database, resolver fact,
deployment, host, migration, collector, known-evidence index, frozen standard,
or tag was modified. No target tests or collectors were run. The paired JSON
artifact is the machine-readable source for the matrix and guard assertions.

## Standards validation and handoff

The paired files are the only planned Standards artifacts:

- `audits/fleet-persistent-state-compatibility-planning-m10-2026-09-01.md`
- `audits/fleet-persistent-state-compatibility-planning-m10-2026-09-01.json`

The full Standards suite was run directly and unpiped after the artifact and
guard work: **844 passed, 0 failed, 0 skipped, exit 0 (8.03s)**. A clean local
commit is required; no push is authorized by this planning prompt. The next
action after that clean commit is a separately authorized push of the exact
Standards commit, followed by a target-local M11 implementation mission
beginning with Semiconductor.
