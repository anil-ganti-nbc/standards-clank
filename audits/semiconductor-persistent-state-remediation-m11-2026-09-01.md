# Semiconductor Intelligence - M11 persistent-state compatibility evidence

```json
{
  "clank": "semiconductor-intelligence",
  "date": "2026-09-01",
  "findings": [
    {
      "standard": "STD-DEPLOY-COM-002",
      "kind": "conformance",
      "summary": "CONFORMS / CLOSED at canonical Semiconductor Intelligence main revision 8085a1bbd1a4e133680702e8c1d916b71bb78a14: every supported normal entry point is behind a read-only exact Alembic-head compatibility barrier; unknown, missing, older, newer, divergent, or malformed state fails closed with an identifying reason, while create_all and automatic stamp fallback cannot admit compatibility."
    }
  ]
}
```

This Standards-only M11 record closes only `STD-DEPLOY-COM-002` for
Semiconductor Intelligence at canonical `main`/`origin/main` revision
`8085a1bbd1a4e133680702e8c1d916b71bb78a14`. It is source-level persistent-state
compatibility evidence, not proof that a live deployed database is compatible.
`STD-DEPLOY-COM-001` remains unresolved and no overall Semiconductor conformance
claim is made.

## Takeover and lineage

Standards was taken over at clean `HEAD` = `origin/master`
`5d1309fd4dff3d427aad095fadb26aedb2a7c5fd`. Semiconductor's canonical target
revision is `8085a1bbd1a4e133680702e8c1d916b71bb78a14`, and its remote resolves to
the same SHA. The M1 fleet audit recorded Semiconductor with 23 applicable
standards, 17 conformances, 0 non-conformances, and 6 insufficient findings:

- `STD-UI-COM-006`
- `STD-UI-COM-007`
- `STD-UI-COM-011`
- `STD-OPS-COM-003`
- `STD-DEPLOY-COM-001`
- `STD-DEPLOY-COM-002`

`STD-OPS-COM-003` was subsequently closed by the independent M6 Operations
record. This pass supersedes only the M1 `STD-DEPLOY-COM-002` insufficiency for
the Semiconductor revision above. The remaining four findings stay exactly
`INSUFFICIENT_EVIDENCE`.

M10 classified Semiconductor as `APPLIES`, family
`ALEMBIC_MIGRATION_HEAD`, `PARTIAL_MECHANISM`, with `HIGH` risk. The recorded
defect was that normal `_session` and runtime paths used `Base.metadata.create_all`
without a migration-head check and the explicit Alembic helper could stamp head
after broad "already exists" exceptions. Either path could therefore bless
unknown or incompatible state.

## Exact compatibility contract now present

The checked-in Alembic graph has one authoritative head,
`c7d8e9f0a1b2`. `semi_intel.schema_guard.authoritative_head()` reads that
head from the checked-in Alembic configuration and `inspect_schema()` performs a
read-only `MigrationContext` inspection. A state is ready only when its current
heads are exactly the one expected head. Missing databases, missing or empty
`alembic_version`, unknown/partial history, older heads, newer heads, divergent
heads, malformed configuration, and inspection errors are not inferred to be
compatible; they fail closed with an explicit compatibility reason.

`require_schema_head()` is the normal-work barrier. The CLI `_session` path,
operator status/doctor/update paths, dashboard startup and request dependency,
and runtime-bridge health/identity paths all use the guard before opening or
admitting normal state-touching work. Dashboard startup may perform the
explicit canonical Alembic upgrade operation, then requires the exact head;
ordinary request/session paths cannot fall back to structural creation.

`Base.metadata.create_all()` is not compatibility admission. It remains only
in explicitly exercised legacy/test comparison code and is not called by the
normal session, dashboard, operator, or runtime-health admission paths.
`upgrade_or_stamp_to_head()` now runs the canonical Alembic upgrade only; the
exception-string automatic `stamp head` fallback is removed. Explicit operator
`db stamp` remains an operator command and is not used as compatibility proof.
Failures expose `SchemaCompatibilityError`/CLI refusal text or truthful
runtime-health status reasons identifying the compatibility gate.

## Required source checks

| Check | Result | Evidence |
|---|---|---|
| A. Authoritative identity is the expected Alembic head | YES | `authoritative_head()` resolves the checked-in single head `c7d8e9f0a1b2`. |
| B. Compatibility inspection is read-only | YES | `inspect_schema()` uses a connection and `MigrationContext.get_current_heads()` only. |
| C. Missing/unknown state is not silently compatible | YES | Missing SQLite state and empty/unknown heads return not-ready with an explicit reason. |
| D. Older/divergent state cannot proceed because tables exist | YES | Exact tuple comparison rejects older, empty, and divergent heads before `_session`. |
| E. Newer/incompatible state fails closed | YES | A newer or any non-exact current head produces `SchemaCompatibilityError`. |
| F. `create_all()` is not compatibility admission | YES | Normal session/runtime/dashboard paths use the guard; create-all comparison is not readiness. |
| G. Automatic stamp fallback is not admission | YES | The compatibility helper performs explicit Alembic upgrade only; broad exception stamping is gone. |
| H. CLI paths cross the barrier | YES | `_session` requires the exact head before normal commands obtain a session. |
| I. Dashboard paths cross the barrier | YES | Explicit startup reconciliation is followed by exact-head checking; each request dependency checks again. |
| J. Runtime-health/startup paths cross the barrier | YES | Runtime bridge uses the guard and reports false readiness/reasons on incompatibility. |
| K. No normal state-touching path bypasses preparation | YES | CLI, operator, dashboard, and runtime entry points converge on the guard before work. |
| L. Failure exposes an explicit reason | YES | Guard exceptions, CLI refusal output, and health `status_reasons` identify schema incompatibility. |
| M. Success depends on exact head, not structural inference | YES | Readiness is true only for `current_heads == (expected_head,)`. |

## Migration is distinct from compatibility

M11 added no migration and did not migrate production state. The existing
canonical Alembic history remains the only schema-changing mechanism. A fresh
or older development database may be reconciled only by an explicit Alembic
upgrade operation; that operation is separate from the read-only compatibility
decision. Migration-framework presence, connectivity, table existence, or
`create_all` completion is not evidence of compatibility. The conformance fact
is that normal work cannot proceed unless the persistent state is proven to have
the exact expected migration head.

## Validation evidence

Focused M11 and adjacent compatibility regression coverage on the canonical
target commit passed:

```text
python -m pytest -q tests/test_deploy_com_002_m11.py tests/test_legacy_import_interfaces.py tests/test_lifecycle_persistence.py tests/test_web_notifications.py tests/test_cli_db.py
21 passed, 0 failed, exit 0
```

The final targeted startup/operator regression also passed (8 passed, exit 0),
and `python -m compileall -q semi_intel` completed successfully.

The direct full target suite was recorded as:

```text
python -m pytest -q
894 passed, 1 skipped, 11 failed, 38254 warnings in 1622.52s (0:27:02), exit 1
```

The 11 failures are preserved honestly as environmental/baseline-unrelated
to M11: ten Windows `WinError 50` subprocess-launch failures and one Node
dashboard parse failure. No M11 implementation failure and no
compatibility/migration test failure remained. The full suite is therefore not green
and is not represented as green by this record.

## Narrow verdict and Deployment admission

`STD-DEPLOY-COM-002 = CONFORMS / CLOSED` for Semiconductor Intelligence is
admitted only at `8085a1bbd1a4e133680702e8c1d916b71bb78a14` and only for the
source-level persistent-state compatibility barrier. The four unresolved M1
findings remain:

- `STD-UI-COM-006` - `INSUFFICIENT_EVIDENCE`
- `STD-UI-COM-007` - `INSUFFICIENT_EVIDENCE`
- `STD-UI-COM-011` - `INSUFFICIENT_EVIDENCE`
- `STD-DEPLOY-COM-001` - `INSUFFICIENT_EVIDENCE`

Exactly one narrow Deployment known-evidence fact is admitted for
Semiconductor + this SHA + `STD-DEPLOY-COM-002`. The existing Watch
`STD-DEPLOY-COM-001` evidence remains intact. No `STD-DEPLOY-COM-001` fact is
admitted here, and no evidence is inherited by another target.

## Family status

Semiconductor is the **first validated member of the Alembic migration-head
DEPLOY-COM-002 family**. This is descriptive process evidence only: one
Alembic target now demonstrates the exact-head recipe. It does not infer
conformance for KTW, Feature Phone, Tablet, Smartwatch, OEM Radar, CTW, or any
other target, and it does not require identical storage or runtime mechanics
elsewhere.

## Safety and freeze declarations

Semiconductor was not modified during this Standards pass. No host,
deployment, scheduler, live database, production migration, or restart action
occurred. Frozen Deployment standard files and immutable v1.0 tags were not
changed or moved. No KTW M12 work was begun.
