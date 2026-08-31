---
id: health-state-vs-scheduler-enabled-conflation
domain: operations
topics: [11]
confidence: STRONG
priority: HIGH
---

## Concern

"The scheduler shows this job as enabled" (or "the last invocation
exited 0") must not be read as "this job is actually healthy." A job can
be enabled, invoked on schedule, and exit successfully while producing
nothing useful (zero items, a broken delivery path, a persistent 403) —
and several fleet members have shipped code that conflated the two before
correcting it.

## Current terminology

See [terminology-map.md](../terminology-map.md) "Health vs.
scheduler-enabled" section — this is the single most convergently-adopted
pattern in the entire survey, though under nine different names.

## Repos surveyed

All nine fleet Clanks, plus `clank-architecture` (which already has an
**ACTIVE**, not proposed, governing law for this specific concern — see
Inherited evidence).

## Independent evidence

- watch-clank: `acquisition_state` (can it reach/interpret the source)
  split from `yield_state` (what has it produced), explicitly because "a
  persistent 403 that exits 0 is BLOCKED, never healthy."
- oem-radar: `operational_state: degraded-until-first-run` — a fresh
  volume with no run history reports degraded, not healthy, by design.
- smartphone-clank: `health_score()` starts at 100 and does **not**
  check enablement, validation status, or candidate realism — a
  documented, still-open gap (INC-013-adjacent finding, not yet fixed as
  of survey).
- feature-phone-clank: `delivery_health` is a distinct axis from
  `source_health` by construction — `get_health()` has no dependency on
  the notifications table at all.
- chinese-tech-wire: `runtime_snapshot()` returns OS-level scheduler
  state and DB-level run state as unmerged siblings; a fresh container
  with zero runs explicitly reports `"unknown"`, never `"healthy"`.
- korean-tech-wire: five-state `health_state` (`HEALTHY`/`STALE`/
  `BLOCKED`/`FAILED`/`UNKNOWN`), explicitly citing "Fleet Law 3 (health
  honesty)" in its own source comment.
- semiconductor-intelligence: ten-condition `effective_automation_state`
  layering (`disabled`/`task_status_unavailable`/.../`running_normally`)
  — "enabled" is explicitly only one of ~10 checked conditions.

## Inherited evidence

`clank-architecture/FLEET_LAWS.md` Law 3 ("Health honesty": "Scheduler
invocation ≠ successful work; a failing scheduled unit must be observable
in one query") is marked **ACTIVE** — the only ACTIVE document found in
`clank-architecture` besides the promotion freeze. It names specific
historical violators across multiple Clanks (KTW dashboard
HEALTHY-iff-ever-succeeded; FGT 200+0=ok; smartphone dormant
maintenance-alerting; smartwatch failing timer lane fired hourly with
zero observability). `diagnostic-clank`'s ADR-0007 independently derives
the same principle from the Watch-Clank-class incident (a fleet reporting
green while the Discord delivery path was missing), and its
`HealthPayload` contract encodes `observed_count`/`expected_range` fields
directly citing that incident.

## Incidents

INC-006 (ZERO_ITEMS-as-healthy), INC-013 (smartphone-clank's still-open
health-score gap), INC-021 (korean-tech-wire — a `health_state` model
existed but the *scheduling* gate that caused the incident was separate,
see cluster A/E), INC-043 (Helldivers2/FGT — collection succeeded,
delivery silently failed, motivated ADR-0007 directly).

## Implementations

Strong, working examples: watch-clank, feature-phone-clank,
korean-tech-wire, chinese-tech-wire, semiconductor-intelligence — all
independently split health into at least two axes. Weak/gap: smartphone-clank's
`health_score()` is a documented, currently-unfixed exception to an
otherwise fleet-wide-adopted pattern.

## Counterexamples

None found arguing scheduler-enabled should be treated as health —
every repo that addressed the question at all agrees they must be
separate. smartphone-clank's gap is a shipped-but-unfixed defect, not a
disagreement with the principle.

## Harm if violated

INC-043 (a real news item silently never delivered while collection
reported healthy) is the clearest illustration — "green dashboard, no
actual output" is exactly the failure mode `FLEET_LAWS.md` Law 3 and ADR-0007
both name as their motivating incident.

## Likely domain

Operations.

## Unresolved questions

- `clank-architecture`'s Fleet Law 3 is already ACTIVE fleet-wide
  governance (with CI enforcement in several repos via the shared
  `conformance` suite). Should a Standards Clank Operations standard on
  this topic *adopt/restate* Law 3, defer to it entirely and not
  duplicate, or standardize only the parts Law 3 doesn't cover (e.g. the
  specific axis names/vocabulary, which vary a lot per repo)? This is
  the single most important governance-reconciliation question this pass
  surfaces — see [README.md](../README.md)'s "Relationship to existing
  Fleet Laws" note.
- smartphone-clank's known, unfixed `health_score()` gap — is flagging
  it here (as evidence, not as a violation finding) appropriate, or does
  it require a real audit before any characterization beyond "gap noted
  in the repo's own docs"?
