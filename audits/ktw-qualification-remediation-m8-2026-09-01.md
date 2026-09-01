# Korean Tech Wire — M8 qualification provenance/reset evidence

```json
{
  "clank": "korean-tech-wire",
  "date": "2026-09-01",
  "findings": [
    {
      "standard": "STD-OPS-COM-003",
      "kind": "conformance",
      "summary": "CONFORMS / CLOSED at canonical Korean Tech Wire main revision 2040af82136d8a8f181c464e7d62ce408dd2696d: aggregate SQLite health-history execution establishes provenance, scope-aware material epochs, pre-gate reset lineage, independent terminal evidence, and fail-closed qualification gating."
    }
  ]
}
```

This Standards-only M8 record closes only `STD-OPS-COM-003` for Korean Tech
Wire at canonical `main`/`origin/main` revision
`2040af82136d8a8f181c464e7d62ce408dd2696d`, whose parent is
`afb4aada1d4fae09ada4658fe9fcf8dfa38eb23d`. It does not describe KTW as
fully conforming overall. No overall target conformance claim is made.

## Lineage and preserved M1 state

Standards was taken over at clean `HEAD` = `origin/master`:
`ea0549fa94aa4ffbda7deee00f13d71a3d203bdb`. The M1 fleet blind audit recorded
KTW with 23 applicable standards, 18 conformances, 0 non-conformances, and 5
insufficient findings:

- `STD-DATA-COM-001`
- `STD-UI-COM-011`
- `STD-OPS-COM-003`
- `STD-DEPLOY-COM-001`
- `STD-DEPLOY-COM-002`

Only `STD-OPS-COM-003` is superseded for the canonical KTW revision by this
record. The other four remain exactly `INSUFFICIENT_EVIDENCE`; this pass does
not re-audit them, infer applicability for OEM Radar, or admit any Deployment
evidence.

## KTW architecture and execution authority

M4 classified KTW as an **aggregate SQLite health-history architecture**. The
existing aggregate `runs` row and per-source `source_run_health` history remain
the operational history; the new qualification projection is separate from
content identity and health-history facts.

The target-local execution authority is the `run_collectors` boundary used by
the CLI, dashboard controller, and portable soak loop. The boundary creates the
aggregate run and then prepares qualification for each selected source before
collector work begins. `run_collectors` defaults to `MANUAL`; the due-aware
portable soak path supplies `SCHEDULED`, while tests can explicitly supply
`TEST`. KTW has no in-process deploy or recovery trigger, so no trusted value for
either was invented. Missing or invalid values normalize to `UNKNOWN`.

Qualification scope is explicit per source: `production:<source_id>` for
production sources and `experimental:<source_id>` otherwise. A multi-source
aggregate invocation therefore retains independently gated source scopes even
though the existing operational run remains aggregate.

## Qualification evidence mechanics

`qualification.py` computes a deterministic SHA-256 material identity from the
sorted, canonical qualification inputs: target, source identity/status/URL,
collector, request timeout, user agent, baked source revision, qualification
policy version, and schema version. Runtime timestamps and run identifiers are
not identity inputs.

Migration 5 is additive. It adds provenance and qualification columns to
`runs`, plus `qualification_scopes`, `qualification_epochs`,
`qualification_resets`, and `qualification_terminals` with the necessary
indexes and foreign keys. Existing runs retain the default `UNKNOWN`
provenance; no historical fact is backfilled or reclassified.

`prepare()` compares the current scope identity before any gate decision. A
material change creates a new epoch and an append-only reset row before the
changed run can consume evidence. The reset retains the prior identity when it
is known, the new identity, reason, provenance, source/run linkage, epoch, and
time. The first epoch has no fabricated prior identity. The gate reads only
current-scope/current-epoch terminal facts and fails closed for `UNKNOWN`, an
absent terminal, or an epoch/material mismatch.

Terminal facts are persisted independently of reset facts. They use
`INSERT OR IGNORE` uniqueness on `(run_id, scope_key)`, so recording a terminal
fact is idempotent and a reset and terminal can coexist for the same execution.
Only a successful `SCHEDULED` terminal counts toward reusable qualification;
manual and test outcomes remain auditable without silently becoming scheduled
evidence. No downstream writer upgrades absent provenance or fabricates a
trusted provenance value.

## Required invariant checks

| Invariant | Result | Source-derived basis |
|---|---|---|
| A. Trusted provenance originates at execution authority | YES | CLI/dashboard/soak call the `run_collectors` boundary, which binds the run and per-source preparation. |
| B. Missing provenance stays `UNKNOWN` | YES | `normalize_provenance()` maps missing/invalid values to `UNKNOWN`; legacy runs default to it. |
| C. Downstream code cannot invent trusted provenance | YES | Qualification terminal rows use the authority-bound context; no downstream upgrade path exists. |
| D. Qualification scope is explicit and appropriate | YES | Production and experimental source scopes are distinct, source-keyed, and independently gated. |
| E. Material identity is deterministic and qualification-relevant | YES | Canonical sorted-input SHA-256 excludes timestamps and run IDs. |
| F. Material change invalidates reusable prior evidence | YES | A changed identity creates a new epoch before evidence lookup. |
| G. Reset precedes stale-evidence consumption | YES | `prepare()` persists the epoch/reset before `_gate()` evaluates the run. |
| H. Old evidence cannot qualify the first changed execution | YES | Gates query the new epoch, which has no prior terminal fact. |
| I. Reset lineage keeps prior/new identity where known | YES | Reset rows retain both identities, reason, provenance, and execution linkage; first epoch remains null prior. |
| J. Historical unknowns remain honest | YES | Legacy rows are preserved with `UNKNOWN`; no backfill occurs. |
| K. Reset and terminal evidence coexist | YES | Separate reset and terminal tables permit both facts for one run. |
| L. Terminal evidence is idempotent | YES | Terminal uniqueness plus `INSERT OR IGNORE` makes repeated recording harmless. |
| M. Gate fails closed on absent/stale/divergent/untrusted evidence | YES | Unknown provenance, missing current terminal evidence, and material divergence are ineligible. |
| N. Alternate execution paths cannot bypass preparation | YES | CLI, dashboard, soak, direct runner, and test paths converge on `run_collectors`; preparation is inside the shared loop before collector work. |

## Validation evidence

The canonical KTW remediation evidence records the direct full-suite command as
`python -m pytest`: **92 passed**, **0 skipped**, **0 failed**, exit code 0.
Focused qualification, health/soak, and storage coverage was also green:
`python -m pytest tests/test_qualification_m8.py tests/test_health_soak.py
tests/test_storage.py` — **17 passed**.

No collector, live target, host, deployment, or production database was used in
this recording pass.

## Narrow verdict and Operations admission

`STD-OPS-COM-003 = CONFORMS / CLOSED` for KTW is admitted only at
`2040af82136d8a8f181c464e7d62ce408dd2696d` and only for source-level
qualification provenance/reset conformance. The original M1 insufficiency is
retained as historical evidence; the four remaining KTW findings stay
unresolved. The Operations known-evidence index gains exactly this one
KTW/revision/standard fact. No Deployment evidence is admitted. No unrelated
KTW standard or target fact is admitted.

## Architectural pattern conclusion

KTW is an independently implemented third architectural shape under the same
`STD-OPS-COM-003` contract: aggregate SQLite invocation and per-source health
history with a separate qualification projection. This is descriptive process
evidence only. It does not place KTW in the rich ORM/job or per-source SQLite
operational-scope families, copy their schema, or transfer evidence to another
target. OEM Radar remains unresolved and no OEM applicability or conformance is
inferred.

## Safety and freeze declarations

KTW was not modified during this Standards pass. No host, deployment, live
collector, scheduler, or production-database action occurred. Frozen standard
files and immutable v1.0 tags were not changed or moved.
