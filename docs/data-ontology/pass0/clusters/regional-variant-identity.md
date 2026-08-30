---
id: regional-variant-identity
domain: data-ontology
clusters: [C]
confidence: MODERATE
priority: MEDIUM
---

# Regional Variant vs. Distinct Entity Is Genuinely Unresolved Fleet-Wide

## Concern

When the same physical product appears in multiple regions (possibly with
different SKUs, connectivity, or configuration per region), is a regional
appearance a new fact about an existing entity, or a new entity in its own
right? Every repo that has encountered this question has left it
explicitly open rather than answered it.

## Current terminology

`RegionalSighting` (smartphone-clank, schema exists, unwired), `NEW_REGION`
event type (watch-clank, added after an incident), region as part of the
identity key (tablet-clank, admitted provisional), `reconcile_samsung()`
region-keyed matching (smartwatch-clank).

## Repos surveyed

smartphone-clank, watch-clank, tablet-clank, smartwatch-clank.

## Independent evidence

- watch-clank: `NEW_REGION` transition type was added specifically after
  a real miss (Citizen regional-commercialisation incident, INC-05) — a
  known reference's first official observation in a new region is now a
  distinct, named event, with an explicit guard that no cross-currency
  pair can ever become a `PRICE_CHANGE`.
- smartphone-clank: HANDOFF.md §11.4 admits regional variants are
  "currently just multiple Evidence rows on one Device, not
  `RegionalSighting` rows — that table exists and would be the more
  correct fit but wasn't wired up this phase."
- tablet-clank: `IDENTITY_MODEL.md` states outright that region is
  currently *part of* the identity key (so two regions = two products by
  construction), and separately admits: "does not yet distinguish
  regional appearance from genuinely different hardware... real-world
  cross-region examples have not yet been audited."
- smartwatch-clank: `reconcile_samsung()` keys cross-source matching on
  `(region, regional_model_number)` for exact matches — a real, working
  mechanism, but Samsung-specific and ad hoc rather than a generalized
  regional-identity model.

## Inherited evidence

None found — each repo arrived at its own partial answer independently,
and none has fully resolved the question even for itself.

## Incidents

watch-clank's Citizen regional miss (INC-05) is the one confirmed,
concrete incident — a real product launch in a new region was invisible
because the system had no concept of "same reference, new region" at all
before the fix.

## Implementations

All partial. No repo has a complete, audited regional-identity model.

## Counterexamples

None — this is presented as an open question, not a disputed one; every
repo that has touched it agrees it's unresolved.

## Harm if violated

Confirmed once (watch-clank INC-05: a real launch missed entirely). The
risk in the other direction (treating two genuinely different regional
variants as one entity, losing a real distinction) is plausible but
unconfirmed by any incident in this pass.

## Likely domain

Data/ontology, core identity question — but explicitly flagged by every
repo that's touched it as needing more real-world evidence before a rule
could be written with confidence.

## Unresolved questions

1. This entire cluster *is* the unresolved question: is a regional
   appearance of a known reference (a) always the same entity with a new
   fact attached, (b) sometimes a distinct entity depending on
   configuration differences, or (c) something that can't be decided
   without more real-world audit? Every repo surveyed has left this open.
2. Should Pass 0B treat this as "not ready to adjudicate — needs a
   dedicated evidence-gathering pass across more regional examples" rather
   than attempting to resolve it now?

## Confidence: MODERATE
## Adjudication priority: MEDIUM
