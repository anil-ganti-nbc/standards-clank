---
id: schema-deploy-fail-closed-gating
domain: operations
topics: [8]
confidence: MODERATE
priority: MEDIUM
---

## Concern

Whether a deploy checks schema compatibility *before* serving traffic
(fail closed: refuse to start rather than silently run against a
mismatched schema) or only discovers a mismatch after the fact.

## Current terminology

"Schema guard," "schema_check," "EXPECTED_HEAD" — different names, same
shape, in the repos that have it at all.

## Repos surveyed

watch-clank, smartphone-clank, semiconductor-intelligence,
korean-tech-wire, oem-radar, chinese-tech-wire, tablet-clank,
feature-phone-clank.

## Independent evidence

- watch-clank: `app/db/schema_check.py`, a startup check that refuses
  (exit 3) on any Alembic-head mismatch, built in direct response to a
  real production outage (INC-007-adjacent — every scheduled run failing
  with a missing-table error after a skipped manual migration step).
- smartphone-clank: three separate runtime entrypoints (daemon, `main.py
  run`/`init`, cloud one-shot runner) all refuse to start rather than
  silently `create_all()` if schema is behind — but this is a
  *repeated-incident* pattern (INC-016 occurred at least twice before
  the fix held).
- semiconductor-intelligence: a health check compares live
  `alembic_version` against a hardcoded expected head — but this is a
  post-hoc health signal, not a pre-traffic-switch gate, and the intended
  rollback procedure for a schema mismatch was explicitly untested
  ("no schema changes were made this phase, so there is no
  schema-incompatibility scenario to plan around yet").
- oem-radar: three-way SHA/identity cross-check before trusting a
  deployment (overlaps cluster I) functions as an indirect schema-readiness
  proxy but isn't itself a schema check.
- korean-tech-wire: manual, sequential, human-run checklist
  (`pytest`, `health`, integrity check) rather than an automated
  pre-traffic gate.
- chinese-tech-wire, tablet-clank, feature-phone-clank: no fail-closed
  schema-version check found; chinese-tech-wire self-flags "two
  overlapping schema-migration mechanisms... pre-existing and untouched."

## Inherited evidence

`clank-architecture/GOLDEN_INCIDENT_CORPUS.md` GIC-14 ("schema drift /
unsupported schema") and `DATA_SURVIVABILITY.md` R4 ("bad migration")
register this as a known risk class with an executable CI fixture, but
no incident narrative (root cause/date) beyond the individual-Clank
evidence above was found at the governance layer.

## Incidents

INC-007 (watch-clank's original outage that motivated the fix), INC-016
(smartphone-clank, recurred at least twice before holding).

## Implementations

Strong: watch-clank, smartphone-clank (both fail-closed, both built in
direct response to a real incident). Weak/absent: chinese-tech-wire,
tablet-clank, feature-phone-clank, korean-tech-wire (manual checklist
only).

## Counterexamples

None disputing the concern; absence in several repos looks like "hasn't
been bitten yet" rather than a considered decision against it.

## Harm if violated

INC-007: every scheduled run failing in production after a skipped
manual migration step. INC-016: a table with zero rows repeatedly
appearing in production, confirmed reproducing at least twice.

## Likely domain

Operations.

## Unresolved questions

- Is there enough independent-incident evidence (2 confirmed: watch-clank,
  smartphone-clank) to justify HIGH rather than MEDIUM priority, or does
  the fact that over half the surveyed repos have no equivalent mechanism
  at all (and no incident either) suggest this is lower-urgency until
  more evidence accumulates? Kept MEDIUM here pending Pass 0B's judgment.
- Should a standard require the *fail-closed* behavior specifically, or
  only that *some* schema-compatibility check exists before traffic is
  served (leaving fail-open-with-alert as a conforming alternative)?
