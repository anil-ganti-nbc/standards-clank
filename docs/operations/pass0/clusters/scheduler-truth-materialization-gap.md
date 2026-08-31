---
id: scheduler-truth-materialization-gap
domain: operations
topics: [1, 13]
confidence: STRONG
priority: HIGH
---

## Concern

"The scheduler fired" (or "the scheduler shows enabled/next-run") is
routinely, silently non-equivalent to "the collection actually happened
and was recorded." The gap can occur at any of several distinct stages
between schedule definition and outcome record, and multiple fleet
members have independently built (or are still missing) mechanisms to
catch it.

## Current terminology

See [terminology-map.md](../terminology-map.md) "Was this a scheduled or
manual run?" table. No two repos use the same vocabulary; `clank-architecture`
ADR-0008/0011 is the only place a shared vocabulary has been proposed
(`SCHEDULE_EXPECTED → SCHEDULER_FIRED → PROCESS_STARTED →
APPLICATION_EXECUTED → RUN_MATERIALIZED → RUN_COMPLETED →
OUTCOME_RECORDED`), and it is not yet adopted by any individual Clank's
own code.

## Repos surveyed

All nine fleet Clanks, plus `clank-architecture` and `diagnostic-clank`
(both repo and live NAS incident log).

## Independent evidence

- watch-clank: `scheduled` flag was a pure log label with zero behavioral
  effect (INC-002-adjacent finding).
- oem-radar: explicit "an hourly OS trigger does not mean hourly crawls"
  distinction, verified by manual probe.
- chinese-tech-wire: dedicated read-only `scheduler_status.py` querying
  `schtasks.exe`, deliberately kept separate from DB-recorded execution
  state, but the two are never cross-validated against each other.
- korean-tech-wire: due-ness computed entirely from persisted run
  history, explicitly avoiding any dependency on asking the scheduler
  anything — yet this design still suffered INC-021 (see Incidents).
- smartphone-clank: `is_due()` computed from DB history rather than
  scheduler state, built specifically in response to INC-012.
- semiconductor-intelligence: `last_scheduler_invocation` and
  `last_successful_job_commit` persisted as two distinct fields — cited
  by `clank-architecture` as "the reference semantic" for the fleet.
- tablet-clank: no scheduler exists in-repo at all (scheduling lives
  entirely in deploy-time systemd artifacts, untracked by the app).

## Inherited evidence

`clank-architecture` ADR-0008/0011's six/seven-stage model is explicitly
a *generalization written after* INC-027 (the fleet-wide git-stash
outage) and INC-028 (oem-radar's false-positive materialization-gap
inference) — i.e. the shared vocabulary was derived from real incidents,
not proposed speculatively. `semiconductor-intelligence`'s
invocation-vs-commit pattern is cited by name in `FLEET_LAWS.md` (Law 3)
and `adr/0002` as the reference implementation other Clanks should match,
though the audit trail shows even SemInt's own live deployment was found
violating it (`clank-architecture` fleet archaeology report).

## Incidents

INC-002, INC-009 (materialization aspect), INC-012, INC-021, INC-027
(the canonical, most severe example — three Clanks simultaneously, ~36h
silent), INC-028 (the inverse failure: a monitor over-inferring a gap
from a legitimately empty cycle), INC-030, INC-037, INC-045. See
[incident-ledger.md](../incident-ledger.md).

## Implementations

Strongest: semiconductor-intelligence's invocation/commit split (already
fleet-cited as reference), chinese-tech-wire's separate scheduler-status
query, korean-tech-wire's pure DB-derived due-check, smartphone-clank's
`is_due()`. Weakest/absent: tablet-clank (no in-repo scheduler concept at
all — entirely deploy-artifact-based), korean-tech-wire's own design
still missed INC-021 because per-item due state was correct but
aggregated with an AND-gate (see cluster E's overlap note).

## Counterexamples

None found disputing the *concern* itself — every repo that has thought
about this at all agrees scheduler-fired and outcome-recorded are
different facts. The disagreement, where it exists, is only about
mechanism (DB-history-derived vs. OS-query-derived vs. both).

## Harm if violated

Ranges from "silent zero-output cycles nobody notices" (INC-002,
INC-037) to "three Clanks simultaneously silent for ~36 hours"
(INC-027) to "~4x intended request rate against a real third-party host
for over a week" (INC-021, which is really this concern plus cluster E's
AND-gate problem compounding). This is the highest-severity,
highest-recurrence cluster in the corpus.

## Likely domain

Operations — core scheduling/execution-truth concern, squarely inside
the domain's charter.

## Unresolved questions

- Should a Standards Clank rule adopt `clank-architecture`'s six/seven-stage
  vocabulary directly, or define its own coarser two-fact contract
  (invocation timestamp + outcome timestamp, as SemInt already does) and
  let the finer-grained stage model stay `clank-architecture`'s own
  concern?
- Is `clank-architecture`'s Golden Incident Corpus (already CI-enforced
  in several fleet repos) something Standards Clank should reference
  rather than duplicate, given it already encodes fixtures for
  `PRE-EXEC-MATERIALIZATION-GAP`?
- INC-028 shows a rule requiring "every scheduled invocation must
  materialize a record" would itself be *wrong* — any rule here must
  accommodate a legitimate zero-work cycle. How should a standard state
  the requirement so it doesn't reproduce that false-positive shape?
