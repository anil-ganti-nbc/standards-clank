---
id: evidence-provenance-granularity
domain: data-ontology
clusters: [E]
confidence: STRONG
priority: HIGH
---

# Evidence/Provenance Must Be Traceable at Fact, Change, and Decision Granularity

## Concern

An operator (or another system) needs to be able to answer "why does this
Clank believe X?" at several distinct levels: what raw evidence produced
this fact, what changed and when, and what a human decided about it and
on what basis. Collapsing these into one tier loses the ability to audit
or correct any one layer independently of the others.

## Current terminology

`SnapshotFetch`/`SnapshotBlob`/`SourceObservation`/`PipelineLedger`/
`EventReview` (watch-clank, deepest storage-layer stack); `EvidenceItem`/
`snapshots.raw_ref`/`ChangeEvent.meta`/`alert_review_history` (oem-radar);
`DecisionExplanation`/`TimelineEvent`/`MaterialChange` (chinese-tech-wire's
`EXPLAINABILITY_CONTRACT.md` — the single richest artifact found);
`SignalItem`/`Evidence`/`ClaimEvidenceLink`/`ClaimEvent`/
`ClaimLinkSuggestion` (semiconductor-intelligence, four-to-five tiers);
`EventEnvelope` draft (clank-architecture/diagnostic-clank, unwritten).

## Repos surveyed

watch-clank, oem-radar, chinese-tech-wire, korean-tech-wire,
feature-phone-clank, tablet-clank, smartwatch-clank, smartphone-clank,
semiconductor-intelligence, diagnostic-clank.

## Independent evidence

Every repo surveyed except korean-tech-wire (pre-scoring-maturity, no
alerting layer to explain yet) independently built at least a three-tier
provenance stack: raw/fact-level, change-level, and (where a QC/review
layer exists) operator-decision-level. The richest independent examples:

- **chinese-tech-wire's `EXPLAINABILITY_CONTRACT.md`**: a formal, versioned
  (`explanation_version: v1`) contract with `Contribution`
  (component/raw/weight/contribution/facts), `ThresholdCheck`,
  `TimelineEvent` (with an explicit `inferred` boolean flag distinguishing
  reconstructed from directly-observed chronology), and `MaterialChange`.
  Rule 1: "Never invent facts not present in stored records or
  configuration."
- **semiconductor-intelligence's four-tier trust ladder**: `SignalItem`
  (raw) → `Evidence` (immutable, canonical) → `Claim` (falsifiable
  assertion, synthesized from possibly-disagreeing evidence via
  `ClaimEvidenceLink.stance`) → `ClaimEvent` (append-only audit trail).
- **watch-clank's storage-layer depth**: separate content-addressed
  `SnapshotBlob` beneath the parsed `SourceObservation` — deeper at the
  raw-fetch layer than any other repo surveyed.
- **oem-radar's method-as-provenance**: `evidence_links.method` records
  *how* a fact was linked (exact_sku/alias/normalized_model/none), not
  just the outcome — the linking method is itself first-class provenance.

## Inherited evidence

No repo cites another repo's specific evidence-model code. The three-tier
shape (fact/change/decision) recurs so consistently that it reads as
convergent good design under a shared house philosophy rather than
copying — the same assessment reached independently for several other
clusters in this pass.

## Incidents

- oem-radar's Stage 11→11.1 (evidence observations polluting the
  canonical change-event stream, 44.6% of all "alerts") is the clearest
  incident of *collapsing* provenance tiers that should have stayed
  separate.
- clank-architecture's RISK_REGISTER R-001 ("repository head mistaken for
  deployed artifact") and P4-G5 ("BACKUP-NO-HASH") are both
  provenance-granularity incidents at the infrastructure level, cited as
  evidence, not verified against a specific Clank in this pass.
- diagnostic-clank's Law 6 (Provenance) specimen names a live, specific
  cross-Clank incident: "SemInt d43481f claim-vs-ledger contradiction" —
  not independently verified in this pass, flagged for follow-up.

## Implementations

Genuinely mature and varied — this is the cluster with the widest
independent implementation base in the entire survey. No repo is missing
this concept entirely; the variance is in depth (how many tiers, how much
raw-payload retention) not in whether the concept exists.

## Counterexamples

None found that argue against the concept. korean-tech-wire simply hasn't
reached the maturity stage where a decision-explanation tier is needed
yet (no scoring/alerting layer exists) — an absence of need, not a
counterexample.

## Harm if violated

Directly measured in oem-radar's Stage 11 incident (44.6% of the
canonical alert stream was non-canonical evidence, burying real signal
and corrupting downstream metrics).

## Likely domain

Data/ontology, core case — this is arguably the cluster closest to
"ready to adjudicate," given how mature and convergent the independent
implementations already are.

## Unresolved questions

1. Is diagnostic-clank's draft `EventEnvelope` contract (occurred_at vs
   observed_at, `correction_of` as an explicit supersession pointer,
   multi-dimensional confidence explicitly forbidden from collapsing to a
   scalar) worth adopting or adapting as a fleet-wide shape, given it is
   already a near-complete synthesis of what every repo independently
   built pieces of?
2. Should raw-payload retention depth (full HTML/JSON vs. hash-only) be
   standardized, or is this legitimately an implementation/cost tradeoff
   each Clank should own?

## Confidence: STRONG
## Adjudication priority: HIGH
