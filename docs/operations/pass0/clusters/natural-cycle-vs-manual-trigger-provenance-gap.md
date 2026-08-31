---
id: natural-cycle-vs-manual-trigger-provenance-gap
domain: operations
topics: [2]
confidence: STRONG
priority: HIGH
---

## Concern

Whether a given run was fired by the natural schedule or invoked
manually/by a deploy step is, in roughly half the fleet, either
unverifiable from stored data or verifiable only by a self-asserted flag
that nothing cross-checks against the actual scheduler. This matters
because promotion/soak evidence is routinely defined in terms of "clean
*natural* cycles" — if the trigger provenance can't be verified, neither
can the promotion evidence that depends on it.

## Current terminology

See [terminology-map.md](../terminology-map.md) first table — the
clearest illustration of fleet-wide inconsistency found in this survey:
three repos (smartphone-clank, chinese-tech-wire, semiconductor-intelligence)
store a trigger field; three (oem-radar, korean-tech-wire, tablet-clank)
store nothing verifiable; the rest fall in between.

## Repos surveyed

All nine fleet Clanks.

## Independent evidence

- smartphone-clank: `run_reason` field, explicit default
  `"production_scheduled"` vs `"field_test_manual"`, asserted and tested.
- chinese-tech-wire: `IngestionRun.trigger`, `"SCHEDULED"`/`"MANUAL"` —
  but **self-asserted only**, driven by a CLI flag nothing verifies
  against `schtasks.exe`'s own record, despite a separate module
  (`scheduler_status.py`) that *could* verify it and simply isn't
  cross-checked.
- semiconductor-intelligence: `OperationalTriggerType` enum persisted per
  job run, with the scheduled path *required* to route through
  `OperationalScheduler` so a direct pipeline invocation can't
  masquerade — the strongest implementation found.
- korean-tech-wire: **no schema field exists at all.** Promotion evidence
  is asserted only in a YAML comment ("2026-08-30 natural production
  proof: run_id 2708...") — unverifiable from the database itself, a
  real structural gap directly acknowledged in the survey.
- oem-radar: no trigger field; "Epoch" bookkeeping is documentation-only,
  not per-run.
- tablet-clank: no trigger-source field in the JSONL cycle schema at all.
- feature-phone-clank, watch-clank: no field; isolation-by-deployment
  (fully separate checkout/DB for experimental work) substitutes for
  per-run tagging.

## Inherited evidence

No repo cites another repo's specific trigger-tracking code — this
appears to be independent invention wherever it exists, not shared
lineage (contrast cluster B). `clank-architecture`'s ADR-0011
`materialization_policy` concept is adjacent but addresses a different
question (was a record expected at all, not who/what triggered the run).

## Incidents

No incident was found where a manual run was *actually* miscounted as
natural evidence and caused downstream harm — this is a documented
**structural gap with clear exploitability**, not yet a confirmed
incident. The closest adjacent incidents are INC-021 (korean-tech-wire's
due-gating AND-bug) and INC-032 (tablet-clank's manual soak-abort, whose
completed cycles were correctly, manually excluded from later evidence —
proving the exclusion currently depends on human diligence, not
mechanism).

## Implementations

Strong: semiconductor-intelligence (required routing through the
scheduler for the trigger to read `SCHEDULER`). Moderate: smartphone-clank
(stored but not cross-verified against an OS-level scheduler query).
Weak/self-asserted-only: chinese-tech-wire. Absent: oem-radar,
korean-tech-wire, tablet-clank, watch-clank, feature-phone-clank
(mitigated by isolation in the latter two, not by tagging).

## Counterexamples

None disputing the concern; the gap is universally implicit rather than
argued-for.

## Harm if violated

If a manual run's outcome is folded into "clean natural cycles" evidence
used for a promotion decision, that promotion rests on evidence weaker
than believed. No confirmed incident of this actually happening was
found, but the mechanism to prevent it is missing or weak in over half
the fleet, and the adjacent AND-gate incident (INC-021) shows how
quickly a due/trigger-accounting gap can produce real operational harm
once it's wrong.

## Likely domain

Operations.

## Unresolved questions

- Is this cluster's absence-of-a-confirmed-incident (as opposed to
  clusters A/B/C/G, which all have dated, harmful incidents) reason to
  rank it lower than HIGH? It's kept HIGH here because the *mechanism
  gap* is well-evidenced and directly undermines the evidentiary basis
  for promotion decisions across roughly half the fleet — but Pass 0B
  should weigh "structural gap, no incident yet" against "incident
  already occurred" explicitly when prioritizing.
- Should a standard require a stored, scheduler-cross-verified trigger
  field (SemInt's strength), or would requiring only "manual runs must be
  excluded, by mechanism not convention, from natural-cadence promotion
  evidence" (a narrower, easier-to-adopt consequence) be more
  appropriate given how differently each repo currently tracks this?
