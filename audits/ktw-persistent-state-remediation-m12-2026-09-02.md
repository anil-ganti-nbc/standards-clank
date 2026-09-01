# Korean Tech Wire — M12 persistent-state compatibility evidence

```json
{
  "clank": "korean-tech-wire",
  "date": "2026-09-02",
  "findings": [
    {
      "standard": "STD-DEPLOY-COM-002",
      "kind": "conformance",
      "summary": "CONFORMS / CLOSED at canonical Korean Tech Wire main revision 354cb7aed0b174923393a0c71e7c4c6230cda28c: main SQLite v5 and the independent QC archive v1 each use read-only compatibility inspection and fail-closed normal-access barriers; valid older main-store prefixes migrate only through the canonical path and every other unknown, corrupt, partial, or newer state is refused."
    }
  ]
}
```

This Standards-only M12 record closes `STD-DEPLOY-COM-002` only for Korean Tech
Wire at canonical `main` / `origin/main` revision
`354cb7aed0b174923393a0c71e7c4c6230cda28c`. It admits source-level
persistent-state compatibility evidence, not live deployment or production
database evidence. `STD-DEPLOY-COM-001` remains unresolved; no overall KTW
conformance is claimed.

## Takeover, lineage, and original gap

Standards was clean at `HEAD` = `origin/master` =
`30c573eb151013a4174a22f62bb284fbcfcc5ed2`. KTW's parent revision was
`2040af82136d8a8f181c464e7d62ce408dd2696d`; canonical remote `main` now
resolves to `354cb7aed0b174923393a0c71e7c4c6230cda28c`.

M1 recorded KTW with 23 applicable standards, 18 conformances, no
non-conformances, and five insufficient findings: `STD-DATA-COM-001`,
`STD-UI-COM-011`, `STD-OPS-COM-003`, `STD-DEPLOY-COM-001`, and
`STD-DEPLOY-COM-002`. Operations M8 subsequently closed `STD-OPS-COM-003`.
This record supersedes only the M1 Deployment compatibility insufficiency.

M10 classified KTW as `APPLIES`, `PARTIAL_MECHANISM`, `MEDIUM` risk, and a
member of the ordered numbered-SQLite family. The main collector DB had
numbered SQLite migrations but no explicit expected-head barrier before normal
work; the separately persisted QC archive had no version authority. Version
skew and rollback behavior were therefore unguarded.

## Two state authorities and compatible-state model

KTW has two relevant, independent persistent-state contracts:

- The main collector database has ordered SQLite `schema_migrations` through
  explicit expected version **v5**.
- The QC archive has separate `qc_schema_migrations` through independent
  expected version **v1**.

The source exposes the descriptive compatibility vocabulary `FRESH`,
`MIGRATION_REQUIRED`, `COMPATIBLE`, `INCOMPATIBLE_NEWER`, `UNKNOWN`,
`CORRUPT`, and `PARTIAL`. Inspection is read-only: it opens existing SQLite
state read-only and checks integrity, durable version markers, ordered history,
and required structure. `FRESH` is not `UNKNOWN`: a missing or empty store may
use the canonical bootstrap, while any non-empty store without trustworthy
version authority is refused rather than recreated, stamped, or blessed.

## Barrier and migration semantics

`Database.connect()` and `QCArchive.connect()` require compatibility before
normal access. CLI context and dashboard startup are the canonical migration
boundaries; each migrates only the allowed state, then explicitly calls the
compatibility check again before state use. This covers CLI commands including
status and health, portable soak/scheduler due and retry work, dashboard/manual
and QC paths, and direct normal state consumers.

Only a valid older contiguous prefix of the main v5 history may take the
canonical ordered migration path. Normal work remains blocked until the
post-migration check proves the expected durable contract. Unknown, missing,
corrupt, contradictory/partial, or newer state fails closed without deletion,
reconstruction, or table-existence inference. A failed migration cannot make
the store ready because readiness is re-inspected from the durable marker and
structure. An older KTW binary refuses v6+ state. No rollback compatibility or
transactional recovery guarantee is claimed.

## Named implementation checks

| Check | Result |
|---|---|
| Explicit expected schema version | YES |
| Compatibility inspection is read-only | YES |
| Unknown state silently counts as compatible | NO |
| Older unmigrated state can perform normal work | NO |
| Newer state can perform normal work | NO |
| Non-empty missing-marker state silently bootstraps | NO |
| Corrupt or partial state can perform normal work | NO |
| Canonical migration remains authoritative | YES |
| Post-migration version is reverified | YES |
| Failed migration can mark state ready | NO |
| Every operational entry point crosses the barrier | YES |
| Alternate normal DB opening can bypass the barrier | NO |
| Current-version behavior remains intact | YES |
| Existing `STD-OPS-COM-003` behavior remains intact | YES |

## Validation

The canonical source evidence records these direct, non-live commands:

```text
python -m pytest -q tests/test_deploy_com_002_m12.py
7 passed in 1.87s, exit 0

python -m pytest -q tests/test_deploy_com_002_m12.py tests/test_storage.py tests/test_qc_archive.py tests/test_qualification_m8.py tests/test_health_soak.py tests/test_scheduling.py tests/test_field_test_dashboard.py
57 passed in 22.01s, exit 0

python -m pytest -q
99 passed in 22.25s, exit 0
```

The full non-live suite is green; no baseline attribution is needed.

## Narrow verdict and admission

`STD-DEPLOY-COM-002 = CONFORMS / CLOSED` for KTW at
`354cb7aed0b174923393a0c71e7c4c6230cda28c`, only for source-level
persistent-state compatibility. Exactly one new Deployment known-evidence fact
is admitted for that target, revision, and standard. Existing Watch
`STD-DEPLOY-COM-001`, Semiconductor `STD-DEPLOY-COM-002`, and historical KTW
M1 evidence remain preserved.

The unresolved KTW findings remain `STD-DATA-COM-001`, `STD-UI-COM-011`, and
`STD-DEPLOY-COM-001`, all `INSUFFICIENT_EVIDENCE`. `STD-OPS-COM-003` remains
previously closed. No unrelated KTW standard is admitted.

## Family status and safety

KTW is the **first validated member of the numbered-SQLite compatibility
family**: explicit version authority, read-only inspection, a fail-closed
barrier, canonical migration, and post-migration verification are source-proven
once. This is descriptive process evidence only. Tablet inherits nothing and
remains independently unproven; no target must copy KTW's schema design.

KTW was not modified in this Standards pass. No host, deployment, live target,
collector, production database, production migration, restart, or rollback
action occurred. Frozen Deployment standard files and immutable v1.0 tags were
not changed or moved.
