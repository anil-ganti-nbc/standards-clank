# Pass 3 evidence dossier — STD-UI-SKU-001

- **Standard ID:** STD-UI-SKU-001 ("SKU review systems must preserve a distinct availability-negative disposition")
- **Current proposed version/text:** v2. Requirement: "Where availability is in scope for a SKU/product-based Clank's QC model, that model MUST preserve a QC disposition meaning 'this product exists and was correctly identified, but is not currently available' — distinct from a product-invalid disposition (false positive), a not-novel disposition (duplicate), and a general not-useful disposition. A Clank MUST NOT fold an availability-negative case into false-positive or not-useful. Canonical presentation SHOULD use 'Out of Stock' as the operator-facing label where that phrase accurately describes the underlying source state, but this standard does not require a literal fourth enum value named OUT_OF_STOCK — any encoding that keeps the disposition distinctly queryable (a dedicated status, or an event-type-plus-reason-code pair) satisfies it."
- **Historical reason it remained proposed:** v1 (a literal OUT_OF_STOCK fourth enum value, written as the SKU mirror of NEWS-001's DUPLICATE rule) was returned by Operator Ratification Decision 001: the load-bearing invariant is ontological — availability-negative must not be misclassified as invalid/not-useful — not a specific label. v2 protects the ontology and explicitly allows oem-radar's event-type-plus-reason-code encoding; v2 itself has never been reviewed.

## Survey scope (re-verified at current HEADs)

| Repo | Availability in scope? | Availability encoding | Availability-negative vs false-positive/not-useful |
|---|---|---|---|
| watch-clank (fbf228f) | YES — availability change events (AVAILABILITY_CHANGE, PREORDER_STARTED, SHIPPING_STARTED, PRODUCT_REMOVED) | OUT_OF_STOCK as a terminal EventReview disposition (review.py:60) | DISTINCT — separate terminal verdict from FALSE_POSITIVE/NOT_USEFUL |
| smartwatch-clank (08a23f9) | YES — availability free-text on Observation + AVAILABILITY_CHANGE/PRODUCT_REMOVED/POSSIBLE_DISCONTINUATION events | OUT_OF_STOCK terminal disposition (qc_archive.py:43; no DUPLICATE) | DISTINCT |
| tablet-clank (41282f7) | PARTIAL — no availability data model; "still-listed vs withdrawn catalogue entry" exists only as a human verdict | OUT_OF_STOCK terminal disposition (qc_archive.py:44, rationale :40-43) | DISTINCT — explicitly not folded into FALSE_POSITIVE/NOT_USEFUL |
| feature-phone-clank (4051b64) | YES — availability field in change detection; automatic SPECS_BECAME_UNAVAILABLE / AVAILABILITY_CHANGED events | OUT_OF_STOCK terminal disposition (qc_store.py:49) + automatic availability-negative event types | DISTINCT at two layers (event type + human verdict) |
| oem-radar (9546465) | YES, deeply — Availability enum (IN_STOCK/PREORDER/SOLD_OUT/UNKNOWN) on per-SKU configurations, restock subsystem | **NO OUT_OF_STOCK disposition** — availability flip is a change_type (`AVAILABILITY_CHANGED`) plus first-class `ReasonCode.TEMPORARY_STOCK_CHANGE` (core/feedback.py:44, qc_archive.py:40-45) | DISTINCT by design — "an availability flip is not a separate verdict axis here"; NOISE/BUG map to not-useful/false-positive and never absorb stock blips |
| smartphone-clank (5684cf2) | **NO — availability deliberately out of scope** (release-state fixed "unknown", "not inferred from novelty") | none; no QC vocabulary exists | N/A by trigger |
| semiconductor-intelligence (8a356a3) | NO — signals, not stock; `CandidateReviewDisposition` docstring: OUT_OF_STOCK "has no honest equivalent here" so DUPLICATE takes its place (domain/enums.py:170-184) | none | N/A by trigger; independent semantic rationale recorded in code |
| korean-tech-wire (afb4aad) | NO — news only | QC_DECISIONS without OUT_OF_STOCK (qc_archive.py:46) | N/A by trigger |
| chinese-tech-wire (1a47220) | MARGINAL — a small JD.com documentary watchlist emits AVAILABILITY_CHANGED events (documentary_change.py:79-80); QC vocabulary is news-side (USEFUL/NOT_USEFUL/WRITTEN/DUPLICATE/FALSE_POSITIVE) | no availability disposition; no observed folding into false-positive | no counter-example observed |

## Evidence FOR

1. **The invariant holds in every implementation where the trigger applies** — five Clanks keep availability-negative distinct from false-positive/not-useful, through **three independent encodings**: a terminal OUT_OF_STOCK disposition (watch, smartwatch, tablet, feature-phone), an availability data-model + change_type + reason-code pair (oem-radar), and automatic availability-negative event types (feature-phone, smartwatch). v2's "any encoding that keeps the disposition distinctly queryable" clause was written for exactly this and is satisfied by all of them without a single code change.
2. **The strongest evidence is independent of the OUT_OF_STOCK lineage**: oem-radar's qc_archive docstring (qc_archive.py:40-45) documents, in its own words, why an availability flip must not become a verdict ("it is one of many change_types this queue reviews … 'this alert is just a routine/temporary stock blip, not real signal' is already a first-class REASON CODE") — the same invariant, derived independently, in a repo that deliberately does not use the watch vocabulary. And semiconductor-intelligence's enums docstring independently explains why OUT_OF_STOCK must be *absent* where availability is not in scope. Both are design-reasoning artifacts, not copied code.
3. **The negative half of the trigger also holds independently**: both news-family repos surveyed lack the disposition and neither shows any pressure to add it; smartphone-clank deliberately keeps availability out of scope and out of its (nonexistent) QC vocabulary. The rule, as triggered, never forces availability semantics onto a Clank that does not track them.

## Evidence AGAINST

1. **The terminal-OUT_OF_STOCK encoding is one lineage, not four votes**: watch's five-value contract is the documented ancestor of tablet's, feature-phone's, and smartwatch's QC sets (their qc_archive/qc_store docstrings credit watch and ktw/ctw ancestry). Raw implementation count therefore overstates support for that *encoding*.
2. **No conflation incident was found.** No repo documents an operator actually misfiling an availability-negative as false-positive/not-useful. The rule is supported by design reasoning and semantic distinctness, not by incident history.
3. **Domain question (handoff §8): is UI the right home?** Availability truth in oem-radar lives in the data model (Availability enum, restock subsystem) — arguably data/ontology territory. However, v2 is scoped to the *QC model's disposition vocabulary* — the operator-facing review axis — which is exactly the layer a UI standard governs (the same layer NEWS-001 governs). The data-model side (how availability is detected/stored) remains un-normated by this standard and free to vary.
4. oem-radar's conformance relies on the v2 encoding clause; under a hypothetical stricter literal-value wording it would fail — meaning the standard's value depends on v2's exact wording surviving ratification unchanged.

## Independent-lineage assessment

Terminal-OUT_OF_STOCK lineage: one (watch → smartwatch/tablet/feature-phone, documented ancestry). Independent confirmations of the *invariant*: oem-radar's reason-code design (independent taxonomy, independent derivation), semiconductor-intelligence's explicit absence rationale (independent), feature-phone's automatic event layer (semi-independent — same repo lineage as watch's QC but its event model is its own). Weighting independence and design reasoning over count: the invariant has at least two genuinely independent derivations plus zero counter-implementations across nine repos — sufficient for a trigger-scoped MUST, while the encoding preference (OUT_OF_STOCK label) rests on one lineage and is correctly only a SHOULD in v2.

## Overlap analysis

- **NEWS-001**: DISTINCT and complementary — NEWS-001 fixes the news-family fourth action (DUPLICATE); SKU-001 fixes the availability-negative disposition for SKU families whose fourth axis is stock state, not novelty. Both were born in Pass 1 from the same mirror-structure question; neither subsumes the other.
- **COM-005/006/007/008/009/010/011**: DISTINCT — no interaction with promotion, run controls, health implication, run stages, timestamps, or delivery.

## Applicability analysis

The trigger clause ("Where availability is in scope for a SKU/product-based Clank's QC model") cleanly excludes all news-family Clanks, smartphone-clank (availability deliberately out of scope), and any future Clank that does not track availability — verified against all nine surveyed repos. No implementation is forced to add availability semantics it does not have.

## Testability analysis

Objectively testable: if availability is tracked, enumerate the QC disposition vocabulary and the availability encodings; verify availability-negative outcomes remain queryable as such (dedicated disposition, or event-type-plus-reason-code) and cannot be expressed only as false-positive/not-useful. The survey applied exactly this test to nine repos.

## Recommendation

**RATIFY AS WRITTEN.** v2 already contains the narrowing Pass 1 demanded (ontology over label); the trigger clause is verified clean against nine implementations; the invariant is independently derived in at least two lineages; the one live counter-consideration (UI-domain fit) is resolved by v2's scoping to the QC disposition layer. The standard freezes behavior the fleet already exhibits everywhere it applies.

## Exact narrowed wording

Not applicable — no narrowing recommended.

## Remaining uncertainty

No conflation incident exists yet; the MUST is justified by semantic analysis and design doctrine rather than operator harm. If the operator weights incident evidence strictly, HOLD is the honest alternative — but the only evidence that would resolve it is a future conflation failure, which is not a concrete fetchable source, and the cost of ratifying (zero changes required anywhere) is negligible.

## Operator decision required

See decisions/0009-pass3-sku-001-decision.md.
