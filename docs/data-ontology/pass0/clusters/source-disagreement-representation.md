---
id: source-disagreement-representation
domain: data-ontology
clusters: [D]
confidence: WEAK
priority: LOW
---

# Conflicting Facts From Different Sources Are Rarely Represented as Disagreement

## Concern

When two sources report different values for what should be the same
fact (e.g. two retail listings disagreeing on price, two publishers
disagreeing on a detail), does the system represent this as an explicit
disagreement, or does one value silently win?

## Current terminology

`ClaimEvidenceLink.stance` (SUPPORTS/WEAKENS/CONTRADICTS —
semiconductor-intelligence, the one rich implementation), implicit
last-observed-wins (chinese-tech-wire, korean-tech-wire, most others),
dual independent confidence dimensions (oem-radar, a partial answer).

## Repos surveyed

semiconductor-intelligence, chinese-tech-wire, korean-tech-wire, oem-radar.

## Independent evidence

semiconductor-intelligence's `Claim`/`ClaimEvidenceLink` model is the
**only** fleet implementation found that explicitly represents
disagreement as a first-class fact: a claim's truth-state is a synthesis
over possibly-contradicting evidence stances, not a single overwritten
field, and a `ContradictionCheck` records what a rules engine found
without ever changing confidence/status by itself. oem-radar's dual
confidence dimensions (parse quality + identity certainty) are a partial,
narrower answer — they keep two *kinds* of uncertainty separate, but do
not represent "source A says X, source B says Y" as its own state.

## Inherited evidence

None — semiconductor-intelligence's model is explicitly original
engineering (per its own lineage notes), not shared with or copied from
any other repo.

## Incidents

None found. This is the weakest-evidenced cluster in the entire pass —
no repo other than semiconductor-intelligence has needed to solve this
problem yet (either because disagreement is rare in their source mix, or
because it happens and is silently resolved without anyone noticing).

## Implementations

One (semiconductor-intelligence). Every other repo surveyed either
explicitly admits no disagreement-representation exists (chinese-tech-wire's
own evidence-log entry states this directly: "no explicit mechanism found
for representing *conflicting* facts... later-observed values silently
become 'the' value") or the concern doesn't yet arise in their
architecture.

## Counterexamples

The near-universal silence on this concern across 8 of 9 Clanks could
mean either "this genuinely doesn't matter for most Clanks' source mix"
or "this is a real, unmeasured gap nobody has hit yet." This pass cannot
distinguish between those two readings from the evidence available.

## Harm if violated

No incident evidence — purely theoretical risk (a silently-resolved
disagreement could produce a wrong canonical fact with no trace of the
alternative).

## Likely domain

Data/ontology, but the thinnest-evidenced cluster in this pass —
appropriately LOW priority. Not "wrong to consider," just not yet
supported by enough evidence to justify expensive adjudication now.

## Unresolved questions

1. Is this genuinely a non-issue for 8 of 9 Clanks (single-source-of-truth
   architectures where disagreement structurally can't arise), or an
   unmeasured gap? Would need targeted evidence-gathering (deliberately
   looking for cases where two sources actually disagreed) before this
   cluster could move up in priority.
2. Is semiconductor-intelligence's `Claim`/stance model worth studying as
   a template *if* this becomes a live concern elsewhere, or is it
   over-engineered for the claims/evidence-journalism domain it was built
   for and not transferable to SKU tracking?

## Confidence: WEAK
## Adjudication priority: LOW
