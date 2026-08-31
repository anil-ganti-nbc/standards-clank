---
id: retry-restart-authority-and-idempotency
domain: operations
topics: [10]
confidence: MODERATE
priority: MEDIUM
---

## Concern

Distinct from cluster B (the specific PID-namespace-unsafe locking bug):
who or what is authorized to retry a failed run or restart a stuck job,
and does a retry/restart guarantee idempotency (no duplicate side
effects — no double notification, no double write) rather than merely
preventing *concurrent* execution.

## Current terminology

No shared vocabulary.

## Repos surveyed

feature-phone-clank, smartphone-clank, semiconductor-intelligence,
korean-tech-wire, chinese-tech-wire, watch-clank, `diagnostic-clank`.

## Independent evidence

- feature-phone-clank: explicit retry-safety model for the notification
  layer — bounded attempts (`MAX_ATTEMPTS=5`), `UNIQUE dedup_key` with
  `INSERT OR IGNORE` guaranteeing "a rerun, restart, or double-invocation
  cannot create a second row for the same event," verified directly
  (`FEATURE_PHONE_CLANK_DEFINITION_OF_DONE.md`). Also INC-019, a real
  duplicate-notification bug from a stale comparison baseline, distinct
  from the retry mechanism itself but in the same functional area.
- smartphone-clank: no special retry — a failed attempt simply remains
  subject to the same interval as a successful run; idempotency-under-retry
  is regression-tested (a retried run that reprocesses an
  already-delivered discovery never re-attempts the alert).
- semiconductor-intelligence: both automatic (`next_retry_at`, declared
  but no consuming code path found in this pass) and manual/operator
  retry (`OperationalScheduler.retry`, creates a new job run linked via
  `parent_retry_id`) exist; lease-based mutual exclusion prevents
  duplicate concurrent execution (a concurrent attempt is `SKIPPED`, not
  double-run).
- korean-tech-wire: fully automatic exponential backoff (no manual retry
  pathway found) — 2 failures at normal cadence, then doubling per
  failure up to a 24h ceiling; explicitly tested to survive a simulated
  process restart.
- chinese-tech-wire: no automatic retry at the application level;
  restart/duplicate-execution protection is external only (`flock`
  wrapping the cron invocation) plus a stale-running-row ignore
  threshold that is not obviously kept in sync with the OS-level
  execution-timeout setting (two independently-configured 2-hour
  ceilings in two different layers).
- watch-clank: stale-run recovery can itself manufacture concurrency —
  `stale_run_threshold_minutes` shorter than a legitimate long-running
  force-baseline sweep means a second entrant's recovery logic could mark
  a live run FAILED and start a concurrent writer (flagged as a real,
  undocumented, unenforced single-writer-assumption risk, not yet a
  confirmed incident).

## Inherited evidence

`diagnostic-clank`'s Stage-0.5 explicitly implements **no** operational
retry/restart capability at all yet (`operations.py`'s `RESTART`/`RUN_NOW`
are contract stubs returning `STAGE0_NOT_IMPLEMENTED`); ADR-0005
(fencing) requires a valid ownership token and confirmed-offline status
before any fallback local execution is even attempted — i.e. the
fleet-supervisory layer treats retry/restart authority as a
not-yet-built, deliberately gated capability, consistent with individual
Clanks currently handling this entirely on their own.

## Incidents

INC-019 (feature-phone-clank's duplicate notification from a stale
comparison baseline — related to but not directly caused by the retry
mechanism itself). No incident of an actual double-execution side effect
from a retry/restart race was confirmed in this survey (watch-clank's
risk is flagged as real but unconfirmed).

## Implementations

Strongest: feature-phone-clank's dedup-key idempotency guarantee,
korean-tech-wire's tested exponential backoff. Weakest/unconfirmed-risk:
watch-clank's stale-run-threshold-vs-execution-timeout mismatch.

## Counterexamples

None disputing the concern.

## Harm if violated

Confirmed harm is limited to INC-019 (one duplicate Discord notification
for one real event) — comparatively low severity relative to other
HIGH-priority clusters in this corpus, which is the main reason this is
scored MEDIUM rather than HIGH despite reasonably broad evidence.

## Likely domain

Operations.

## Unresolved questions

- Should this cluster be merged into cluster B (locking), since in
  practice the lock IS the primary retry/restart-authority mechanism in
  most repos, or kept separate because the *idempotency-under-retry*
  question (does a retry avoid duplicate side effects) is logically
  distinct from *concurrent-execution prevention* (does a lock prevent
  two runs happening at once)?
- watch-clank's stale-run-threshold-vs-execution-timeout mismatch is a
  real, flagged, but unconfirmed risk — is it strong enough evidence to
  cite in a standard, or does it need an actual incident first?
