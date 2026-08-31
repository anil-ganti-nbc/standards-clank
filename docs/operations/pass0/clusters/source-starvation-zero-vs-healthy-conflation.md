---
id: source-starvation-zero-vs-healthy-conflation
domain: operations
topics: [6]
confidence: STRONG
priority: HIGH
---

## Concern

A source that silently stops producing observations (or drops to zero
new items) must be distinguishable, at the detection layer, from a source
that is legitimately quiet (nothing new exists right now). Multiple fleet
members independently built a "found > 0, new == 0 is normal; found == 0
is suspicious" distinction — and multiple members shipped a version that
initially failed to catch a real starvation event.

## Current terminology

No shared vocabulary; each repo names its own found-vs-new / zero-streak
concept independently. See individual repo evidence below.

## Repos surveyed

All nine fleet Clanks, plus `diagnostic-clank` (contract layer +
motivating incident).

## Independent evidence

- watch-clank: `ZERO_ITEMS` was counted as a *success* status by
  `health.py`, so 20 consecutive zero-item runs read `HEALTHY` (INC-006)
  until an explicit `zero_item_warning_streak` setting was added.
- oem-radar: `CollectorHealthConfig` with
  `minimum_fraction_of_previous_catalog`/`unexpected_zero_is_failure`
  thresholds classifies a shrinking or zero catalog as
  `degraded`/`failed`.
- smartphone-clank: a `SourceHealth` table exists in schema
  specifically for this purpose but "nothing writes to it yet" — a
  genuine, self-flagged gap; a separate `zero_discovery_with_healthy_fetch`
  metric does exist and caught a real Google collector redirect-wall
  event correctly.
- feature-phone-clank: `blocked_zero_result` is a distinct classification
  from a removal event; requires three consecutive healthy absences
  before treating a source as genuinely gone.
- chinese-tech-wire: explicit "QUIET" (found>0, new==0 — normal) vs
  "DEGRADED" (found==0 despite success — real signal) split, plus a
  `found_zero_streak` counter distinct from `new_zero_streak`.
- korean-tech-wire: identical found-vs-new principle
  (`docs/promotion-policy.md`), independently worded, and directly tested
  against a real incident (SK hynix, INC-022 — zero new articles for the
  entire 8.5-day soak, correctly caught and surfaced via the health
  command).
- smartwatch-clank: `assess_catalogue()` raises on unexpected zero and on
  a collapse ratio below a configurable threshold.
- tablet-clank: **explicitly does not implement this** — "disappearance
  detection is not implemented," documented as a known, accepted gap
  under the current bounded-source-guard design.

## Inherited evidence

`diagnostic-clank`'s `HealthPayload` contract
(`observed_count`/`previous_observed_count`/`expected_range_min/max`)
directly cites "Watch Clank product-catalogue ZERO_ITEMS must not be
reported as overall healthy" as its motivating incident — i.e. the
fleet-level contract layer was written *in response to* watch-clank's
real defect (INC-006), after the fact. No repo was found citing another
repo's *code* for this specific mechanism (unlike the lock cluster) —
implementations read as convergent, not copied.

## Incidents

INC-006 (watch-clank, the archetypal case), INC-022 (korean-tech-wire,
detection *working correctly*), INC-037 (FGT/NAS, a scheduler-level
silent-stop that this kind of detection would also have caught had it
been checked against DSM's own "next trigger" claim).

## Implementations

Strong: chinese-tech-wire and korean-tech-wire's found-vs-new distinction
is the cleanest independently-converged pair in the corpus — nearly
identical concept, structurally different code, no shared lineage.
Strong: smartwatch-clank, oem-radar. Gap, self-flagged: smartphone-clank
(dead table). Gap, accepted-by-design: tablet-clank.

## Counterexamples

None disputing the concern — tablet-clank's gap is an acknowledged
scope limitation ("safe enough for bounded experimental soak because...")
not a disagreement that starvation detection matters.

## Harm if violated

INC-006 is a clean before/after: 20 consecutive zero-item runs read
`HEALTHY` until fixed — a source could be completely dead for an
arbitrary period with the dashboard showing green the whole time. This
overlaps heavily with cluster C (health-vs-scheduler) but is narrow and
well-evidenced enough to warrant its own entry, mirroring how the
Data/Ontology domain kept closely-related concerns (novelty-vs-discovery,
editorial-freshness-vs-novelty) as separate clusters.

## Likely domain

Operations.

## Unresolved questions

- Given how convergently this pattern has already been built (found-vs-new
  as the near-universal shape), is there anything left to standardize
  beyond naming the consequence ("a health/status view must not report a
  silently-zero source as healthy")? Or would a Standards Clank rule here
  be largely redundant with what the fleet has already independently
  converged on — worth Pass 0B explicitly asking whether ratification
  adds value versus documenting existing best practice.
- tablet-clank's explicit, accepted gap — is "not yet needed for
  experimental soak scope" a legitimate scope-based exception, or does
  any production-eligible source need this regardless of current
  maturity?
