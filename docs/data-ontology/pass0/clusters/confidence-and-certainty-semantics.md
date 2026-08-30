---
id: confidence-and-certainty-semantics
domain: data-ontology
clusters: [D, E]
confidence: MODERATE
priority: MEDIUM
---

# Confidence Must Be Multi-Dimensional and Never Conflated With Editorial Value

## Concern

Confidence/certainty (how sure are we this fact is true) is a different
axis from editorial value (how much does this fact matter). Collapsing
multiple independent confidence signals into one scalar early loses
information about *why* something is uncertain; conflating confidence
with editorial importance can suppress genuinely important
low-confidence leads or inflate unimportant high-confidence ones.

## Current terminology

`confidence_dimensions` (diagnostic-clank draft, explicit "never collapse
to a single scalar"), dual confidence (oem-radar — parse quality + identity
certainty, kept separate), six-component confidence architecturally
forbidden from feeding editorial_value (semiconductor-intelligence),
`ConfidenceLedgerEntry` per-contribution ledger (smartphone-clank),
`novelty_score` (chinese-tech-wire — the one identified scalar-collapse
point in an otherwise well-separated system).

## Repos surveyed

oem-radar, semiconductor-intelligence, smartphone-clank, chinese-tech-wire,
smartwatch-clank, watch-clank, diagnostic-clank.

## Independent evidence

- semiconductor-intelligence: confidence's six weighted components are
  **test-enforced** to never feed `editorial_value` — "a candidate can be
  low-confidence and high editorial value simultaneously." The strongest,
  most architecturally rigorous example in the fleet.
- oem-radar: confidence is carried on *both* the product (parse quality)
  and the resolution link (identity certainty) — "both feed the
  notification" but are never merged into one score.
- smartphone-clank: `ConfidenceLedgerEntry` is a genuine per-contribution,
  additive audit ledger, with a single AST-scan-enforced legal writer.

## Inherited evidence

None found — independently converged designs.

## Incidents

**smartphone-clank's dossier "drift" badge bug** is the standout finding:
`ConfidenceLedger.summary()` sets `ledger.confidence = device.confidence`
directly (the same value, not an independent recomputation), so the
dossier's `device.confidence == ledger.confidence` drift-comparison can
structurally never evaluate false. The real drift-detection logic exists
(`ConfidenceService.recalculate()`) but is reachable only from a demo
script and a test — never from any UI or documented CLI path. This is a
genuine "the honest computation exists, but the thing labeled as showing
it doesn't" bug, distinct from (but related to) the availability-lifecycle
cluster's "UI promise with no backing data" pattern.

chinese-tech-wire's `novelty_score` combining first-in-cluster
(structural signal) and new-spec-content (informational signal) into one
scalar is the one identified case in the fleet of a confidence-adjacent
value being prematurely collapsed, in a codebase that is otherwise very
careful about this exact distinction elsewhere (see
`EXPLAINABILITY_CONTRACT.md`).

## Implementations

Uneven maturity — semiconductor-intelligence and oem-radar are the most
architecturally deliberate; feature-phone-clank, tablet-clank, and
korean-tech-wire have no formal confidence score at all (append-only
observation count serves as an informal substitute).

## Counterexamples

None found arguing against multi-dimensionality — the variance is in how
far along each repo is, not disagreement about the principle.

## Harm if violated

smartphone-clank's badge bug is real but low-severity (a cosmetic
non-function, not a false-positive harm) — no confirmed operator-facing
incident traces to a confidence/editorial-value conflation in this pass.

## Likely domain

Data/ontology, moderate strength — genuinely useful evidence but thinner
incident backing than the HIGH-priority clusters.

## Unresolved questions

1. Should "confidence must never be a direct input to editorial/novelty
   scoring" be generalized as a fleet-wide principle, given
   semiconductor-intelligence enforces it with an actual test?
2. Is the smartphone-clank badge bug worth a standalone remediation
   ticket (out of scope for this pass) independent of any broader
   standard?

## Confidence: MODERATE
## Adjudication priority: MEDIUM
