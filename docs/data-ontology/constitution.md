# Agent-facing Data/Ontology Constitution

This is the compact, implementation-facing layer over Standards Clank's
RATIFIED `STD-DATA-*` standards — mirroring
[docs/ui/constitution.md](../ui/constitution.md)'s design for the same
reason: so an agent building or auditing a Clank's data/truth-representation
layer doesn't have to read every standard file individually. It is a
summary, not a replacement. **Where this document and a cited standard
file disagree, the standard file governs.** For the full
`requirement`/`rationale`/`acceptance`/`evidence` text behind any
principle here, read `standards/data-ontology/<ID>.json` directly, or look
it up in
[`ratified-index.json`](../../standards/data-ontology/ratified-index.json).

**Authority rule for this document:** every normative statement below (a
MUST) is derived from, and cites inline, a RATIFIED `STD-DATA-*` standard.
Nothing here is invented. As of this writing, all four Data/Ontology
standards are RATIFIED — there is no "Pending" section of unratified
rules the way the UI constitution has one. Several **candidate** concerns
from the same evidence program were explicitly HELD, REHOMED, or
REJECTED by Pass 0B and never became standards at all — see "Not a
standard" at the end. Do not treat any of those as a requirement; they
were never ratified, drafted, or reviewed as one.

**Trigger-scoping matters more here than in the UI domain.** Every
principle below binds only Clanks with the specific architectural feature
it presupposes (local-history novelty derivation, cross-source merging,
both observations and derived canonical state). A Clank that genuinely
lacks the feature is out of scope by trigger, not in violation — see each
standard's own `trigger` field, and do not report a finding against a
Clank for a concept it doesn't have.

**Consequence, not algorithm.** None of these four standards choose a
storage shape, an identity algorithm, an event-envelope format, or a
confidence-scoring scheme — see
[decisions/0001](../../decisions/0001-standardise-contracts-not-implementation.md).
Do not propose "the fix" as a specific schema; propose that the
*consequence* the standard requires (traceability, exclusion,
reversibility, explicit continuity) becomes true, however the Clank
already shapes its data.

---

## A. Continuity and epoch state

**A1.** Where a Clank derives novelty, alerting, or editorial state from
comparison against its own prior local history, a discontinuity in that
history (data loss, restore from an older backup, a re-baseline, a
collector/source replacement that breaks continuity, a region change that
invalidates prior comparisons) MUST be represented as an explicit,
queryable fact about the dataset's timeline — distinct from the records
themselves and from any novelty judgement made using them.
(`STD-DATA-COM-001`)

**A2.** Baseline/bootstrap observations MUST be distinguishable, at read
time, from ordinary post-continuity observations, without the reader
needing out-of-band knowledge. (`STD-DATA-COM-001`)

**A3.** This does NOT apply to a Clank with no local-history-derived
novelty/alerting/editorial logic — a stateless collector has nothing for
this standard to bind. It does NOT mandate an epoch table, a specific
event-type vocabulary, or any particular storage mechanism — an epoch
marker, a gap record, a baseline flag, or an equivalent all conform.
(`STD-DATA-COM-001`)

## B. Novelty and the read-side exclusion contract

**B1.** A record's first appearance in a Clank's own database MUST NOT,
by itself, be treated as evidence that the thing it represents is new in
the real world. (`STD-DATA-COM-002`)

**B2.** Every default query, view, or API path whose semantics assert
novelty — including secondary or derived such paths — MUST exclude
baseline/continuity-tagged records by including, or explicitly
inheriting, a baseline-exclusion predicate (or an equivalent eligibility
rule) as part of that path's own definition. This MUST be verifiable by
inspecting the path's definition or its inherited eligibility rule.
Post-hoc filtering external to the path, and treating today's clean
output as proof, do NOT satisfy this. (`STD-DATA-COM-002`)

**B3.** An explicit override or history/baseline-inspection view MAY
surface baseline-era records, provided doing so does not relabel them as
novel. Where a Clank models editorial freshness as a concept distinct
from discovery-novelty (typically news/lead-oriented Clanks), it MUST
stay a separate judgement — never implied by discovery time or novelty
status. No catalogue/SKU Clank is required to build editorial freshness.
(`STD-DATA-COM-002`)

## C. Entity-identity conservatism

**C1.** Where a Clank merges records from more than one source, sighting,
or observation into a canonical entity, the default posture MUST prefer a
missed merge over a false merge: insufficient evidence of sameness MUST
leave two records unresolved/separate rather than forced together. A
key or signal used only to surface or propose a candidate match MUST NOT,
by itself, be treated as sufficient grounds to commit that match as
canonical identity. (`STD-DATA-COM-003`)

**C2.** Any merge committed automatically (without a human decision) MUST
be evidence-gated on a discriminator present in the records under
consideration or in the merged record (not a world-knowledge threshold),
auditable (recording both the justifying evidence and which
mechanism/decision-path performed the merge), and reversible or otherwise
information-preserving — the pre-merge per-source identities MUST remain
reconstructable even if the canonical view no longer displays them
separately. (`STD-DATA-COM-003`)

**C3.** This constrains the *consequence* of an identity decision, never
the matching algorithm or a confidence threshold — model number, source
IDs, region+model, fingerprints, aliases, compound keys, and manual
resolution are all equally permitted mechanisms. It binds within-Clank
merges only; the same real-world entity discovered by two *different*
Clanks is an explicitly separate, still-HELD concern (see "Not a
standard"). (`STD-DATA-COM-003`)

## D. Provenance tier separation and traceability

**D1.** Where a Clank both ingests raw observations and derives canonical
state from them, observation records, canonical fact/change records, and
(where an operator-decision layer exists) operator-decision records MUST
remain distinguishable and separately consumable — a consumer reading
"canonical changes" or "operator decisions" MUST NOT receive unreviewed
raw observations mixed into that stream. (`STD-DATA-COM-004`)

**D2.** Every canonical fact or change MUST remain traceable back to the
observation(s) that support it, at a granularity sufficient to explain
why the Clank believes it — a URL plus a content hash plus an extraction
record, a source-observation ID, or an equivalent reconstructable
reference all satisfy this; unlimited raw-payload retention is NOT
required unless a Clank's own retention needs call for it. Every operator
decision MUST remain traceable to the state it was made against.
(`STD-DATA-COM-004`)

**D3.** A value inferred or derived by the Clank itself MUST remain
distinguishable from a value explicitly stated by a source — an inferred
value MUST NOT be serialized or presented as if a source directly claimed
it. (`STD-DATA-COM-004`)

**D4.** "Separable" is satisfied by separate tables, a discriminator
column on one table, or an equivalent means — no tier count (3-5 observed
fleet-wide, all conformant), envelope shape, or retention *duration* is
prescribed; retention duration is per-Clank operations policy.
(`STD-DATA-COM-004`)

---

## Relationship to ratified UI standards

None of A-D restate or weaken a `STD-UI-*` standard — see each standard's
own `notes` field for the specific overlap analysis, confirmed by Pass 2's
adversarial review:

- `STD-DATA-COM-002` (B) is a **data-layer mirror** of `STD-UI-COM-003`'s
  read-side-exclusion shape — COMPLEMENTARY, not duplicative. COM-003
  governs decided-QC-item visibility; B governs novelty correctness
  beneath any surface.
- `STD-DATA-COM-004` (D)'s decision-tier clause is the **general case**
  `STD-UI-COM-002` is the stricter, UI-specific instance of (atomicity,
  race-guard, UI truthfulness) — COMPLEMENTARY, neither restates the
  other.
- No Data/Ontology standard touches `STD-UI-COM-008/009/010/011` (display-
  layer semantics) or `STD-UI-SKU-001` (QC-vocabulary availability
  disposition) — DISTINCT, checked explicitly during drafting and review.

## Not a standard (HOLD / REHOME / REJECT — never ratified, do not enforce)

These candidates came from the same Pass 0 evidence program but were
never advanced past Pass 0B's adjudication. An implementation agent MUST
NOT treat any of these as a requirement, cite them in a conformance
report as if ratified, or use them to justify a code change:

- **Availability/lifecycle honesty backing** (Pass 0B candidate C4) —
  SPLIT/HOLD. The general "a UI-visible semantic guarantee must be backed
  by queryable state" invariant remains unratified.
- **Timestamp-shaped values mistaken for chronological truth** (candidate
  C6) — REJECTED as a standard, REHOMED to diagnostic/testing practice
  (an adversarial-fixture pattern, not a fleet rule).
- **Cross-Clank entity identity** (candidate C7) — HOLD/DEFER, blocked by
  clank-architecture's own adopted ADR-0002 (`DO_NOT_STANDARDISE`)
  position and an unadjudicated prerequisite (ADR-0014).
- Confidence-and-certainty semantics, canonical-fact-overwrite discipline,
  regional-variant identity — all HOLD, insufficient evidence or an
  unresolved domain-boundary question as of this writing.
- Source-disagreement representation — REJECTED (one implementation,
  zero incidents).

Full detail: [docs/data-ontology/pass0/adjudication.md](pass0/adjudication.md).

## Status of this domain

**FROZEN as `data-ontology-standards-v1.0`** (2026-08-31), after a
dedicated hold-resolution audit on the HELD/REHOME/REJECT candidates
above concluded none of them advance into v1 — see
[docs/data-ontology/holds-disposition.md](holds-disposition.md) and
[baselines/data-ontology-standards-v1.0.json](../../baselines/data-ontology-standards-v1.0.json).
