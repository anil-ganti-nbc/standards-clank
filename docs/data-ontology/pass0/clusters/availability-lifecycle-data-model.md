---
id: availability-lifecycle-data-model
domain: data-ontology
clusters: [G, B]
confidence: STRONG
priority: HIGH
---

# Availability/Lifecycle Facts Need an Honest Data Model Behind Any UI Guarantee

## Concern

Several Clanks make an explicit, UI-visible promise about availability or
release-state honesty ("release state defaults to unknown," "catalogue
absence is not discontinuation") — but the promise is not uniformly backed
by an actual data field or model. A promise implemented as decoration
rather than data cannot be relied on, tested, or extended.

## Current terminology

`release_state` (smartphone-clank — UI text only, no field), `availability_status`
(watch-clank, free text), `Availability` enum (oem-radar, closed type),
`Observation.availability` (smartwatch-clank, first-class), `availability`
(feature-phone-clank, dormant/unused field), absent entirely
(tablet-clank), `products.status` (semiconductor-intelligence's oem_radar
sub-system).

## Repos surveyed

All nine fleet Clanks.

## Independent evidence

- **smartphone-clank — the flagship finding of this entire pass**:
  `docs/KNOWN_LIMITATIONS.md:6` states "Release state defaults to
  unknown — novelty != upcoming" as design doctrine. There is **no
  `release_state` field anywhere in the schema** (grep-confirmed across
  `database/models.py` and `models/schemas.py`). The dossier UI literally
  hardcodes `&lt;span class="badge"&gt;unknown&lt;/span&gt;` — a string
  literal that renders identically for every device forever, bound to no
  data at all. The defensive *intent* is real and correct; the
  *implementation* is entirely absent.
- **smartwatch-clank — the positive counterexample**: the equivalent
  disclaimer ("catalogue evidence is a merchandising snapshot, not a
  discontinuation signal") **is** backed by real code — the
  `SamsungRelationship`/`CandidateState` enum set (9 combined states) has
  no member meaning "discontinued," so the model *structurally cannot*
  make the claim it disclaims against making.
- **oem-radar**: `ProductStatus` (ACTIVE/PRE_RELEASE/REMOVED/UNCERTAIN) is
  kept as a distinct field from `Availability` — "is this a going
  concern" vs. "can you buy it right now" are two different facts,
  explicitly.
- **feature-phone-clank**: `availability` exists as a raw per-observation
  string, populated by only 3 of several collectors, and confirmed
  (grep) **never read by the diff/event pipeline anywhere** — persisted
  evidence with zero semantic weight, explicitly listed as an out-of-scope
  backlog item.
- **tablet-clank**: no availability/stock/lifecycle column exists
  anywhere in the schema. The QC-layer `OUT_OF_STOCK` disposition's own
  docstring reasons about "a still-listed vs. withdrawn catalogue
  entry," but nothing stored backs that distinction — the reviewer's call
  is made from looking at the live page, not from any recorded fact.

## Inherited evidence

**A standing assumption is corrected by this pass**: prior UI-domain work
(standards-clank decisions/0009) assumed feature-phone-clank and
tablet-clank shared "one documented lineage" for the QC-layer
`OUT_OF_STOCK` disposition via watch-clank. This pass found two different
lineage paths instead: feature-phone-clank's QC vocabulary is explicitly
ported from **watch-clank**'s `EventReview`; tablet-clank's is explicitly
ported from **korean-tech-wire**'s `qc_archive.py` pattern (module
docstring names it directly; no reference to watch-clank exists anywhere
in tablet-clank). In **both** cases, the shared vocabulary was copied, but
the underlying availability *data model* was not — it is dormant-and-
unused in one repo and entirely absent in the other.

## Incidents

watch-clank's Citizen stale flood (INC-04) is a direct availability-data
quality incident: `availability_status` NULL for 47/47 items at discovery
time, because the cheap discovery path never carried real inventory data.
The `market_status` field (Current/DWS/Phase-Out/Promotion) was
deliberately *not* used as a filter after being proven unsafe (a
Phase-Out SKU had 7 units genuinely in stock) — a correctly-learned lesson
about not treating a lifecycle-stage label as a stock fact.

## Implementations

Genuinely bimodal: smartwatch-clank and oem-radar have real, structurally
honest availability/lifecycle data models with explicit non-conflation
enums. watch-clank has a working but loosely-typed (free-text) field.
feature-phone-clank, tablet-clank, and smartphone-clank have either a
dormant field, no field, or a UI-only promise.

## Counterexamples

None of the "absent" cases contradict the invariant — they simply haven't
built the data model yet, which is a legitimate scope choice (tablet-clank
and feature-phone-clank both track only feature/spec phones and tablets
where availability tracking may be lower priority). The concern is not
"every Clank must model availability" — it's "if a UI/operator-facing
promise is made about availability honesty, it must be backed by data."

## Harm if violated

Direct: an operator viewing smartphone-clank's dossier today receives a
guarantee ("release state: unknown, not inferred from novelty") that is
literally always true regardless of any actual evidence — this is
technically never a *false* statement, but it also can never become a
*true, informative* one; the field can never mature into something
useful without a data-model change no one may realize is needed.

## Likely domain

Data/ontology at its core (does the data model exist), with a UI-domain
edge (is the UI faithful to what the data model actually supports) already
partially covered by ratified `STD-UI-*` work — this cluster is
specifically about the data layer those UI standards deliberately left
un-normated.

## Unresolved questions

1. Should Standards Clank define a minimal fleet-wide availability/
   lifecycle vocabulary (even if optional/profile-scoped), given at least
   two Clanks (oem-radar, smartwatch-clank) have independently converged
   on similar shapes?
2. Is smartphone-clank's dossier badge a bug (should be removed or wired
   to real data) or an acceptable placeholder (labeled honestly enough as
   "unknown" that no harm results)? This pass takes no position — it's a
   finding, not a verdict.
3. Given the corrected lineage finding (two different OUT_OF_STOCK
   origins), should Standards Clank's own decision records
   (decisions/0009) be annotated with this correction? This is a
   UI-domain question outside this pass's authority to decide, flagged
   for the operator.

## Confidence: STRONG
## Adjudication priority: HIGH
