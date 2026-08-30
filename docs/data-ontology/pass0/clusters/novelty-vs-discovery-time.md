---
id: novelty-vs-discovery-time
domain: data-ontology
clusters: [A, F]
confidence: STRONG
priority: HIGH
---

# "New to Us" (FIRST_SEEN_BY_CLANK) vs. "New in the World" (NEW_REFERENCE)

## Concern

A row appearing in a Clank's database for the first time is not, by
itself, evidence that the thing it represents is new in the real world —
it may simply be the first time *this Clank* observed something that has
existed for a while (a baseline sweep, a re-crawl, a newly-added
collector). Conflating the two produces false novelty.

## Current terminology

`FIRST_SEEN_BY_CLANK` vs `NEW_REFERENCE` (watch-clank, the fleet's most
explicit named pair); `is_baseline` / baseline `meta` tag (oem-radar);
`FIRST_SEEN_BY_CLANK != NEW_TO_MARKET` (diagnostic-clank "knowledge law");
`GIC-01`/`FLEET_LAWS.md Law 2` (clank-architecture, "Observation !=
novelty").

## Repos surveyed

All nine fleet Clanks; strongest evidence in watch-clank, oem-radar,
korean-tech-wire; also clank-architecture and diagnostic-clank.

## Independent evidence

- watch-clank: `editorial.py:70-92` — "A reference that is merely absent
  from this database until today is not, by itself, evidence the
  manufacturer launched it today." Alerts visibly mark
  `FIRST_SEEN_BY_CLANK` events as "novelty UNCONFIRMED" in the alert body
  itself, not buried in a reason field.
- oem-radar: `BASELINE_META_KEY`, stamped only from an explicit
  `baseline: bool` passed at call time, "never inferred from a timestamp."
- korean-tech-wire: `baseline_has_content()` — a source's first-ever
  successful non-zero run establishes the baseline; only after that does a
  zero-reference run become an anomaly, not before.
- semiconductor-intelligence: `SignalCandidate.first_observed_at`-scoped
  novelty computation, three explicit outcomes (`first_appearance`/
  `repeated`/`updated`), never silently merged.

## Inherited evidence

feature-phone-clank's baseline gating (`is_baseline = previous_count is
None`, gating *every* event type) and its catastrophic-zero guard are
explicitly "learned from Smartphone Clank's incident history" — a named,
cross-Clank inherited lesson (`core/scope.py:1-9`, `core/runner.py:1-16`).
This is the clearest confirmed lineage line in the entire pass for this
concern.

## Incidents

Six incidents directly on this axis: watch-clank INC-01/02/03/06,
oem-radar INC-07, semiconductor-intelligence's Signal Radar predecessor
(INC-22, identity-adjacent but the same false-novelty root shape),
diagnostic-clank's DB-002 (oem-radar, cross-cited). Two of these
(watch-clank INC-07-analog and oem-radar INC-07) are the **same failure
shape independently discovered in two repos with zero cross-citation** —
a correctly-created baseline flag existed in both, and in both cases the
*display/aggregation layer* simply never consulted it. This independent
convergence on both the failure mode and a structurally similar fix
(a shared SQL/query-level exclusion predicate) is unusually strong
evidence that this is a real, recurring class of bug, not a one-off.

## Implementations

Every fleet Clank that has any concept of "new" implements *some* form of
this distinction. Maturity varies widely: watch-clank and oem-radar have
the richest, most incident-hardened implementations; korean-tech-wire's is
narrow but correct; chinese-tech-wire's is present but has one identified
conflation point (`novelty_score` blends two signals into one scalar, see
[editorial-freshness-vs-novelty.md](editorial-freshness-vs-novelty.md)).

## Counterexamples

None found — no repo asserts the opposite position (that discovery-time
alone is sufficient evidence of real-world novelty). The variance is in
implementation maturity and completeness, not in disagreement about the
principle.

## Harm if violated

Directly measured: watch-clank's ~1045-event burst, oem-radar's 1,875
baseline records "in front of the first genuine alert," korean-tech-wire's
4x sustained request-rate flood (a related but distinct due-gating
variant of the same aggregation-conflation family).

## Likely domain

Data/ontology, core case — arguably the single best-evidenced invariant
in this entire pass.

## Unresolved questions

1. Should the fleet standardize on watch-clank's explicit two-value naming
   (`FIRST_SEEN_BY_CLANK`/`NEW_REFERENCE`), or is this purely a data-model
   concern (any implementation shape acceptable, similar to how UI
   standards avoided mandating implementation)?
2. Given the confirmed independent-convergence pattern (flag exists,
   display layer doesn't check it), is there a generalizable *query-level*
   contract worth standardizing (e.g. "the active/default view query MUST
   exclude baseline-tagged records by construction, not by caller
   discipline")?

## Confidence: STRONG
## Adjudication priority: HIGH
