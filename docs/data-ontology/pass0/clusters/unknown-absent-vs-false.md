---
id: unknown-absent-vs-false
domain: data-ontology
clusters: [B]
confidence: STRONG
priority: MEDIUM
---

# Unknown/Absent Must Never Be Silently Upgraded to a Definite Negative Fact

## Concern

A missing value, a failed fetch, or an unclassified state must not be
treated as equivalent to a confirmed negative fact (e.g. "zero items"
meaning "catalogue collapsed" vs. "genuinely nothing new"; a failed run
counted as a healthy empty result).

## Current terminology

Tri-state fields (`Component.known: bool|None`, oem-radar;
`Snapshot.meaningful: Optional[bool]`, smartphone-clank),
`FailureClass.CATALOGUE_COLLAPSE`/`CHALLENGE_PAGE_AS_ZERO` (diagnostic-clank
shared enum), `blocked_zero_result` (feature-phone-clank),
`unexpected_zero_is_failure` (smartwatch-clank), `record_status:
legacy_unverified` (korean-tech-wire), `certainty: confirmed/probable/unknown`
(chinese-tech-wire).

## Repos surveyed

All nine fleet Clanks, plus diagnostic-clank (strongest fleet-wide
incident evidence).

## Independent evidence

Nearly universal discipline, independently stated as a first-principles
rule in most repos' own architecture docs: watch-clank's `editorial.py`
("never infer SOLD_OUT from source failure"), oem-radar's `Component.known`
tri-state and "never emit a transition *to* UNKNOWN", chinese-tech-wire's
`missed_stories.py` ("never invents new certainty"), feature-phone-clank/
tablet-clank's identical "unknown stays None, never fabricate" docstrings,
semiconductor-intelligence's `SignalMentionStatus` proposal-layer design.

## Inherited evidence

Independent convergence — near-identical phrasing appears in unrelated
repos' docstrings with no cross-citation, suggesting either a shared
house style or (more likely, per this pass's overall pattern) the fleet
having independently learned the same lesson repeatedly.

## Incidents

diagnostic-clank's INC-27/INC-28 (zero/catalogue-collapse counted as
healthy success, fleet-wide pattern spanning oem-radar, feature-phone-clank,
smartwatch-clank), korean-tech-wire's Samsung Newsroom missing-filter
incident (INC-12, absence of a code branch indistinguishable at runtime
from "no low-value content exists"), semiconductor-intelligence's
`stale_run_threshold_minutes` dead-config incident (INC-24).

## Implementations

Broad and mature — this is one of the best-defended concerns in the
fleet, likely because the underlying failure mode (mistaking "we don't
know" for "the answer is no") is intuitive and has been independently
rediscovered many times.

## Counterexamples

smartphone-clank's "release state" (see
[availability-lifecycle-data-model.md](availability-lifecycle-data-model.md))
is the fleet's one clear failure to back this discipline with real data —
though notably the *symptom* is the opposite of the usual failure (a
permanent, un-upgradeable "unknown" rather than a false negative), so it's
not a counterexample to the invariant itself, just an implementation gap.

## Harm if violated

Confirmed fleet-wide via diagnostic-clank's shared `FailureClass` enum
existing specifically because this happened more than once; korean-tech-wire's
19,344-reference over-acceptance incident is a concrete, dated, measured
example.

## Likely domain

Data/ontology, well-established.

## Unresolved questions

1. Given how consistently this is already honored, is there anything left
   to standardize beyond documentation/naming consistency? This may be a
   case where the fleet has already largely solved the problem
   independently, and a standard would mostly be capturing existing good
   practice rather than fixing a live gap.

## Confidence: STRONG
## Adjudication priority: MEDIUM
