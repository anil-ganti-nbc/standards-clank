# Tablet Clank — M13 persistent-state compatibility evidence

```json
{"clank":"tablet-clank","date":"2026-09-02","findings":[{"standard":"STD-DEPLOY-COM-002","kind":"conformance","summary":"CONFORMS / CLOSED at canonical Tablet main revision b3088ebc716227b99e1d8aa66942c8a6e87bbfcb: main/campaign SQLite v3 and independent QC archive v1 each have read-only compatibility inspection and fail-closed normal-access barriers; campaign preflight proves canonical compatibility before its read-only SQLite access."}]}
```

This Standards-only M13 record closes `STD-DEPLOY-COM-002` at
`b3088ebc716227b99e1d8aa66942c8a6e87bbfcb`, source-level only. It is not live
deployment or production database proof. `STD-DEPLOY-COM-001` and
`STD-UI-COM-011` remain unresolved; no overall Tablet conformance is claimed.

Standards takeover was `e698bee3f09c861a1d7ca3be080a33f37ac7cd3c`; Tablet
parent was `d9cb32ccee1b2bcaa4bc9d8af5ac1a7a7e7f6769`. M10's HIGH-risk
`PARTIAL_MECHANISM` defect was auto-migration as compatibility admission, an
unversioned QC archive, and campaign preflight directly reading canonical state.

Tablet now has separate main/campaign `schema_migrations` v3 and QC
`qc_schema_migrations` v1 authorities. It exposes `FRESH`,
`MIGRATION_REQUIRED`, `COMPATIBLE`, `INCOMPATIBLE_NEWER`, `UNKNOWN`, `CORRUPT`,
and `PARTIAL`. Read-only inspection distinguishes fresh from unknown existing
state; only valid older prefixes can migrate canonically, followed by explicit
re-verification. Unknown, corrupt, partial, or newer state fails closed; v4+
is refused by older code and no rollback compatibility is claimed.

Database and QCArchive guard their respective normal access. CLI, scheduler,
manual, status/health, direct consumers, and campaign execution cross these
barriers. Campaign preflight proves compatibility before canonical read-only
SQLite access; lock ownership and qualification remain separate downstream
authorities and cannot bless compatibility.

Focused compatibility/qualification/QC/campaign/preflight/lock/soak/CLI
coverage was `87 passed in 11.14s, exit 0`; direct full suite was `124 passed
in 18.77s, exit 0`. Named A–R checks match the required fail-closed contract.
OPS-COM-003 and OPS-COM-004 remain closed.

Exactly one narrow Tablet Deployment fact is admitted; Watch, Semiconductor,
and KTW facts remain preserved. No host, deployment, collector, production DB,
production migration, restart, or Tablet modification occurred. Frozen
Deployment standard files and immutable tags were not changed or moved.

## Family result

`NUMBERED_SQLITE_COMPATIBILITY_RECIPE_VALIDATED` is descriptive process
evidence across exactly KTW `354cb7aed0b174923393a0c71e7c4c6230cda28c` and
Tablet `b3088ebc716227b99e1d8aa66942c8a6e87bbfcb`: explicit numbered authority
→ read-only inspection → fail closed → canonical old-prefix migration →
post-migration verification → normal work. Tablet's campaign/preflight model
needed no exception. Feature Phone, Smartwatch, OEM Radar, CTW, and all other
targets inherit nothing.
