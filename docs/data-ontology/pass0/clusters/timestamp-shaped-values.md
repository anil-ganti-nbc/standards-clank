---
id: timestamp-shaped-values
domain: data-ontology
clusters: [A, D]
confidence: MODERATE
priority: HIGH
---

# Timestamp/Ordering-Shaped Values Mistaken for Chronological or Causal Truth

## Concern

A value that looks like or behaves like a temporal/ordering signal (a
publisher's "updated at" field, a database row's insertion-order ID, a
single successful scheduler firing) gets used as if it were validated
chronological or causal truth, without first checking that it actually
carries that meaning.

## Current terminology

No single fleet-wide term — this is a recurring *incident shape*, named
independently in each occurrence: firmware-version-as-timestamp
(smartwatch-clank), origin-selection-by-id (semiconductor-intelligence),
UUID-lexical-ordering (diagnostic-clank/clank-fleet adapter), single-fire
cadence-proof (diagnostic-clank/oem-radar NAS canary).

## Repos surveyed

smartwatch-clank, semiconductor-intelligence, diagnostic-clank
(clank-fleet adapters, oem-radar NAS canary incident).

## Independent evidence

Four structurally distinct but same-shaped bugs, found independently, in
four different codebases, with no cross-citation between any of them:

1. **smartwatch-clank**: a collector wrote a Zendesk *editorial*
   `updated_at` into the *hardware-semantic* `firmware_version` field;
   because that field participates in change-detection, a single
   site-wide editorial touch produced 23 simultaneous false
   `FIRMWARE_RELEASED` events sharing one timestamp.
2. **semiconductor-intelligence**: independence-group "origin" selection
   used row-insertion order (`id`) instead of `posted_at`, silently
   mispicking origin whenever collection order and publish order
   diverged — found and fixed with a named regression test.
3. **diagnostic-clank / clank-fleet (smartphone-clank adapter)**:
   `last_run()` ordered candidate rows by row `id` (a UUID, sorts
   lexicographically, not chronologically) instead of `finished_at`,
   risking a false-STALE or false-HEALTHY read of "the latest run."
4. **diagnostic-clank / oem-radar NAS canary**: a single successful
   scheduler firing was treated by an agent as proof of a recurring
   hourly cadence; the owner later established the task was actually
   once-daily.

## Inherited evidence

None — the four occurrences are in four unrelated codebases/contexts with
no shared code and no citation. This is presented as a **recurring
anti-pattern class**, not a single lineage.

## Incidents

All four items above are themselves the incidents (see incident-ledger.md
INC-20, INC-23, INC-31, INC-26). Three of the four were found and fixed;
one (smartwatch-clank's) has a documented remediation that is **not yet
implemented** — the source remains BLOCKED from production specifically
because of this bug.

## Implementations

Not applicable in the usual sense — there is no positive "implementation"
of a general defense against this pattern anywhere in the fleet. Each
fix was point-specific (compare `posted_at` not `id`; compare
`finished_at` not the UUID; require multi-interval scheduler observation).
No repo has a generic invariant or test ("no field that participates in
temporal/precedence logic may be populated from an unvalidated
timestamp-shaped or ordering-shaped source") that would catch a *future*
instance of this bug class before it ships.

## Counterexamples

watch-clank's `_humantime()`/temporal-labeling discipline (see the
ratified UI standard `STD-UI-COM-010`, a different but related concern)
and its `publication_timestamp_is_usable()` clock-skew/future-dating
rejection are the closest thing to a *general* defense found in this
pass — but it's scoped to display-layer timezone/semantic-role labeling,
not to precedence/change-detection logic using the wrong field.

## Harm if violated

Directly measured: 23 false hardware-release alerts (smartwatch-clank,
contained only because the source was still experimental); a silently
wrong "origin" attribution in an editorial-independence calculation
(semiconductor-intelligence); a risk of dashboards reporting the wrong run
as authoritative (diagnostic-clank adapter bug, caught before shipping via
adversarial testing); a week of 4x over-collection from a
cadence-verification gap (a related but distinct variant, see
[baseline-epoch-continuity.md](baseline-epoch-continuity.md) — the
korean-tech-wire due-gating incident shares the "insufficiently-verified
signal treated as proven" root shape but is really an aggregation bug, not
a timestamp-mistaken-for-truth bug; listed there instead).

## Likely domain

Data/ontology (which field means what, and what a valid derivation of
"latest"/"origin"/"proven-recurring" looks like) with a testing-discipline
edge (adversarial fixtures like `uuid_trap_db` are how this class of bug
gets caught before shipping).

## Unresolved questions

1. Is this a coherent, standardizable concern at all, or is it too
   diffuse (four genuinely different bugs) to write one acceptance
   criterion for? This cluster is flagged HIGH priority specifically
   because the *recurrence* across independent codebases is itself the
   interesting finding — Pass 0B should judge whether a general principle
   ("never derive precedence/origin/recency from a field whose semantic
   meaning hasn't been validated to actually track time") is extractable,
   or whether this is better handled as a testing-practice recommendation
   (adversarial fixtures) rather than a data-ontology standard.
2. Should Standards Clank recommend fleet-wide adoption of an
   adversarial-fixture pattern (like `uuid_trap_db`) as a conformance
   practice for any code deriving "latest"/"origin" from a sortable field?

## Confidence: MODERATE
## Adjudication priority: HIGH
