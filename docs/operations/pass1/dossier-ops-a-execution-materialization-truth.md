# Pass 1 Dossier — OPS-A: Execution materialization truth

**Drafted as:** [STD-OPS-COM-001](../../../standards/operations/STD-OPS-COM-001.json)

## Candidate

Execution invocation and outcome must be independently recorded, never
inferred from scheduler-claimed state. A Clank that fires collection must
record two facts in its own store — that an invocation happened, and what
outcome it produced — and a legitimately empty cycle is a recorded
no-work outcome, never a materialization gap.

## Source clusters

Pass 0A clusters `scheduler-truth-materialization-gap` (topics 1, 13) and
`stale-duplicate-automation-surviving-migration` (topic 9), merged by
Pass 0B into candidate card
[ops-a-execution-materialization-truth.md](../pass0/candidates/ops-a-execution-materialization-truth.md).

## Pass 0B disposition

`ADVANCE`. Both source clusters were `KEEP DISTINCT` at HIGH priority in
Pass 0A; Pass 0B merged them on the basis that zombie/duplicate
automation becomes *detectable* once the two-fact contract exists (two
independent invocation streams become visible in records), while single-scheduler
*authority* itself stays Fleet Law 5's separate concern.

## Evidence strength

STRONG. Five Clanks (watch-clank, oem-radar, chinese-tech-wire,
korean-tech-wire, semiconductor-intelligence) built distinct mechanisms
independently; the fleet's most severe operational incident anchors it.

## Strongest incidents

- INC-027 — a 2026-08-22 root-privileged redeploy silently broke cron
  across **three Clanks simultaneously** for ~36 hours; scheduler
  invocations existed, zero application runs materialized, no failure
  record was written. The corpus's most severe operational incident.
- INC-002 — a stale pre-migration cron launcher fired invisibly alongside
  a new scheduler architecture for days.
- INC-021 — a whole-fleet AND-gated due-check produced ~4x the intended
  request rate for over a week despite each per-source due-check being
  individually correct.
- INC-012 — a single-worker scheduler silently dropped 165 due
  executions under its own misfire grace window.
- INC-028 — the counter-evidence: a monitoring tool inferred a false
  materialization gap from three legitimately empty, correctly-due-gated
  cycles. Directly shapes the standard's acceptance criteria (a no-work
  cycle must be a recorded outcome, never an inferred absence).

## Lineage assessment

Independent invention in five repos, not copied code. `clank-architecture`
ADR-0008's six-stage vocabulary was derived *after* and *in direct
response to* INC-027/INC-028 — governance following incidents, not
preceding them. semiconductor-intelligence's invocation-vs-commit split
is cited fleet-wide (Fleet Law 3, ADR-0002) as "the reference semantic,"
making it the strongest single implementation precedent, though still
one Clank's own code, not a shared library.

## Fleet Law / ADR relationship

COMPLEMENT to ADR-0008 (PROPOSED — REVIEWED DRAFT, not ACTIVE at
drafting time) — this standard ratifies only the coarser two-fact
minimum; ADR-0008's finer six-stage vocabulary stays clank-architecture's
own. REFERENCES, does not restate, ADR-0011's no-work-outcome semantics
(also PROPOSED). DEFERS to Fleet Law 5 (ACTIVE) for single-scheduler
authority — this standard makes duplication *detectable*, Law 5 governs
which scheduler *should* be authoritative.

## Strongest counterexample

"A Clank scheduled entirely by an external platform has no invocation
record of its own to expose."

**Why the wording survives:** the requirement binds the Clank's own
recorded evidence of what happened *after* a trigger fired, not who or
what fired it — "scheduler technology and its location... are out of
scope" is stated explicitly in the `trigger` field. A Clank fully
externally scheduled still receives a triggered invocation and still
produces an outcome; it must still record both.

## Unresolved wording questions

- Should "invocation" require a specific minimum granularity (e.g. must
  distinguish which specific trigger source fired), or is "an invocation
  occurred, from *a* trigger" sufficient for v1? Left at the coarser bar
  deliberately, per the mission's "smallest invariant supported by the
  evidence" instruction — flagged for Pass 2 to test.
- The forbidden-list's fourth item ("silently allowing a second, forgotten,
  or duplicate trigger source... without that duplication being
  detectable") is the mechanism carrying cluster 11's merge — worth Pass
  2 checking whether this reads as in-scope for a materialization-truth
  standard or oversteps into Law 5's single-authority territory.

## Recommendation

**READY FOR REVIEW.**
