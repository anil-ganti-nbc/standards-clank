---
id: entity-identity-coarse-key-merge
domain: data-ontology
clusters: [C]
confidence: STRONG
priority: HIGH
---

# Coarse Identity Keys Falsely Merging Distinct Entities

## Concern

A key built for *candidate surfacing* (a rough match to narrow down
possibilities) gets used as if it were a *confident identity match*,
causing two genuinely different real-world entities (SKUs, variants,
listings) to be silently treated as one — producing phantom
change/novelty events, or losing a genuine distinction.

## Current terminology

`model_key` coarse fallback (oem-radar), `IDENTITY_ANOMALY` (feature-phone-clank),
`identity_correction` (tablet-clank), single-shared-entity clustering
(semiconductor-intelligence/Signal Radar), `DEDUPE_FAILURE`/
`IDENTITY_FAILURE` (diagnostic-clank shared enum vocabulary).

## Repos surveyed

oem-radar, feature-phone-clank, tablet-clank, semiconductor-intelligence,
watch-clank (conservative-by-policy counterexample), chinese-tech-wire
(admitted risk, not yet incident), diagnostic-clank (shared vocabulary).

## Independent evidence

- oem-radar: `resolve_identity()`'s six-way cascade explicitly ranks match
  methods (exact SKU > alias > full config signature > variant-only >
  platform-change), each recording method+confidence — built specifically
  to prevent this failure mode.
- feature-phone-clank: `products.model_number` set once at creation,
  never touched again; a later SKU mismatch is flagged for review, never
  auto-resolved.
- tablet-clank: `IDENTITY_MODEL.md` explicitly documents its own fallback
  as "intentionally conservative and may merge products when a source
  exposes no stable identifier; those cases require audit before
  production use" — an honest, pre-declared risk acknowledgment, not a
  discovered-after-the-fact one.
- watch-clank: brand-by-brand conservative allowlist policy — "a brand
  only gets suffix-stripping rules once real evidence shows which
  suffixes are safe to collapse... until then its normalizer must be a
  conservative pass-through" — a deliberate, evidence-gated anti-merge
  policy, and the strongest *preventive* counterexample in the fleet.

## Inherited evidence

No cross-repo citation found for this specific mechanism. oem-radar's
identity cascade and semiconductor-intelligence's proposal-layer +
independence-grouping redesign are structurally similar in spirit
(never trust a single weak signal; require corroboration) but were built
independently for different domains (hardware SKUs vs. entity mentions in
text) with no shared code.

## Incidents

Four confirmed, independent, real incidents of exactly this shape:

1. oem-radar — Samsung/Lenovo tier-word merge (Galaxy Book6 Ultra 64GB vs
   32GB treated as one product), **recurred a second time** in different
   code (Evidence Fusion identity-linking) months later.
2. feature-phone-clank — `IDENTITY_ANOMALY` duplicate-notification bug
   (a narrower variant: not a merge, but a stale-comparison-baseline bug
   with the same "which value counts as the anchor" root shape).
3. tablet-clank — Apple Store carrier/unlocked URL duplication, 48 false
   `new_product` events from one un-deduplicated regional partNumber.
4. semiconductor-intelligence — Signal Radar's single-shared-entity
   clustering flaw (the "Jensen Huang becomes a story" incident) — the
   most severe instance in the fleet, motivating a full architectural
   rebuild rather than a patch.

Four independent, real, dated recurrences of the same failure family —
this is the strongest incident-density cluster in the entire pass.

## Implementations

Range from "no cross-source merging attempted at all" (korean-tech-wire,
feature-phone-clank — by explicit policy) to "rich, ranked, confidence-
scored cascade" (oem-radar) to "conservative allowlist, evidence-gated"
(watch-clank) to "exact-only, human-resolved, no fuzzy matching ever"
(semiconductor-intelligence, post-redesign).

## Counterexamples

Chinese-tech-wire's fuzzy title-similarity clustering has not (yet)
produced a documented false-merge incident, despite being the most
aggressive fuzzy-matching implementation surveyed — its own docs admit
the risk ("brand overlap can soft-match different model numbers") but no
incident confirms it has happened. Worth noting as a live, unresolved
risk rather than a counterexample against the invariant.

## Harm if violated

Phantom change/spec/price events (oem-radar, tablet-clank), false
"top story" rankings built on a merged-entity artifact
(semiconductor-intelligence — the single most severe real-world harm
example: a nonsense "story" became the highest-scored item in the
database), duplicate operator-facing notifications (feature-phone-clank).

## Likely domain

Data/ontology, core case.

## Unresolved questions

1. Is there a generalizable acceptance criterion here (e.g. "an identity
   match below some confidence tier MUST surface as a candidate/review
   item, never auto-merge") that would fit every repo's actual
   architecture, or is match-confidence tiering too implementation-
   specific to standardize?
2. Should "false merges are worse than missed merges" (chinese-tech-wire's
   explicit stated philosophy) be adopted as a fleet-wide default
   posture, given how consistently repos that violated it were burned?

## Confidence: STRONG
## Adjudication priority: HIGH
