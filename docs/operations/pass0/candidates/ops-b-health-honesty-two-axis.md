# Candidate card OPS-B — Health-honesty two-axis complement

- **Candidate name:** Health-honesty two-axis complement (clusters 3 + 4)
- **Plain-language invariant:** Scheduler-liveness/trigger provenance and outcome health are separate axes that must never be conflated in either direction; and within health, acquisition success (reachable, exit 0, parsed) and yield/output (new items, useful content) are separate axes — "ran successfully and produced nothing" is its own state, never silent health.
- **Exact semantic distinction:** Fleet Law 3 (ACTIVE) already owns the principle ("a job can exit 0 while producing nothing useful"). This candidate standardizes the slice Law 3 leaves open: the axis vocabulary and the conflation-forbidden semantics across the fleet's nine different names for the same two axes.
- **Trigger/applicability:** any Clank with scheduled collection whose health or alerting depends on distinguishing liveness from output.
- **Strongest evidence:** 7 of 9 surveyed Clanks independently built a two-axis split (the most convergently-adopted pattern in the entire Operations survey), several citing Fleet Law 3 by name in source comments; INC-006 (ZERO_ITEMS counted HEALTHY, masking 20 consecutive empty runs); INC-022 (korean-tech-wire's found-vs-new distinction correctly caught an 8.5-day zero-new block); diagnostic-clank's ADR-0007 HealthPayload contract built from a green-dashboard/missing-delivery incident; chinese-tech-wire/korean-tech-wire found-vs-new zero-streak pair built with zero shared code.
- **Strongest contrary evidence:** tablet-clank explicitly does not implement disappearance detection — an accepted scope gap (legitimate, scoped; noted, not a dispute).
- **Independent lineages:** convergent, not copied — nine different names, structurally different implementations; the ctw/ktw pair is independently convergent; shared-law citation is governance lineage, not code lineage.
- **Incidents:** INC-006, INC-022, INC-043/ADR-0007.
- **Fleet-Law/ADR relationship:** NARROW COMPLEMENT to ACTIVE Fleet Law 3 — the principle is Law 3's; the SC-ratifiable slice is the two-axis semantics + vocabulary. Health-state display itself remains UI COM-008/012 territory (operator-facing), this card binds the data/operations semantics beneath it.
- **Governance reconciliation disposition:** NARROW COMPLEMENT + reference Law 3.
- **Strongest counterexample:** "a Clank with genuinely no scheduler and no external sources (pure analysis over imported data) — neither axis exists."
- **Why it survives:** trigger-unmet for a pure analysis tool; every Clank with scheduled collection has both axes in some form.
- **Likely implementation freedom:** axis names, health computation, storage shape, display integration (display remains UI COM-008's).
- **Live finding flagged to operator:** smartphone-clank's `health_score()` is a documented, unfixed gap against this exact pattern (an otherwise fleet-wide-adopted pattern with one named exception).
- **Evidence strength:** STRONG. **Fleet impact:** HIGH. **Standardization risk:** MED (governance overlap with ACTIVE Law 3 — the wording must complement, never restate).
- **Recommendation: ADVANCE** (as narrow complement).

## Counterexample test

**Strongest plausible counterexample:** "A Clank with genuinely no
scheduler and no external sources (pure analysis over imported data) —
neither axis exists."

**Does it survive?** YES — trigger-unmet for a pure analysis tool; every
Clank with scheduled collection has both axes in some form. A second:
"health display is already COM-008's territory." COM-008 governs the
display semantics; OPS-B binds the data/operations-layer axis distinction
the display must not conflate. Survives as a narrow complement.
