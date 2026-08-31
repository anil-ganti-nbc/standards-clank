# Agent-facing Operations Constitution

This is the compact, implementation-facing layer over Standards Clank's
RATIFIED `STD-OPS-*` standards — mirroring
[docs/ui/constitution.md](../ui/constitution.md)'s and
[docs/data-ontology/constitution.md](../data-ontology/constitution.md)'s
design for the same reason: so an agent building or auditing a Clank's
scheduling/health/promotion/coordination layer doesn't have to read every
standard file individually. It is a summary, not a replacement. **Where
this document and a cited standard file disagree, the standard file
governs.** For the full `requirement`/`rationale`/`acceptance`/`evidence`
text behind any principle here, read `standards/operations/<ID>.json`
directly, or look it up in
[`ratified-index.json`](../../standards/operations/ratified-index.json).

**Authority rule for this document:** every normative statement below (a
MUST) is derived from, and cites inline, a RATIFIED `STD-OPS-*` standard.
Nothing here is invented. As of this writing, all four Operations
standards are RATIFIED — there is no "Pending" section of unratified
rules the way the UI constitution has one. Several **candidate** concerns
from the same evidence program were explicitly HELD, DEFERRED, or
REHOMED by Pass 0B and never became standards at all — see "Not a
standard" at the end. Do not treat any of those as a requirement; they
were never ratified, drafted, or reviewed as one.

**Trigger-scoping matters here, as in the Data/Ontology domain.** Every
principle below binds only Clanks with the specific architectural feature
it presupposes (triggered/scheduled execution, a health/alerting surface,
a soak/promotion lifecycle, a cross-context exclusivity marker). A Clank
that genuinely lacks the feature is out of scope by trigger, not in
violation — see each standard's own `trigger` field, and do not report a
finding against a Clank for a concept it doesn't have.

**Consequence, not algorithm.** None of these four standards choose a
scheduler technology, a run-table schema, a health-score formula, a
maturity state machine, a cycle count, or a locking mechanism — see
[decisions/0001](../../decisions/0001-standardise-contracts-not-implementation.md).
Do not propose "the fix" as a specific implementation; propose that the
*consequence* the standard requires (independent recording, axis
independence, evidence verifiability, validity-proof provenance) becomes
true, however the Clank already shapes its scheduling/coordination code.

**This domain has a governance relationship the UI and Data/Ontology
domains do not.** Three of the four standards below are explicit
**narrow complements** to `clank-architecture` Fleet Laws that are
already **ACTIVE** (not merely proposed) and CI-enforced in several fleet
repos. None of these standards restates, replaces, or activates that
governance — see "Relationship to `clank-architecture`" below for the
specific mapping. Do not cite a `STD-OPS-*` standard as if it were Fleet
Law text, and do not cite a Fleet Law as if Standards Clank had ratified
it.

---

## A. Execution invocation and outcome (`STD-OPS-COM-001`)

**A1.** Where a Clank fires collection or comparable scheduled work from
any trigger mechanism, it MUST record, in its own stored data, that an
invocation occurred and what outcome it produced — neither inferred from
scheduler-reported state ("enabled", "next run scheduled", "exit 0").
(`STD-OPS-COM-001`)

**A2.** A cycle that correctly performs no work because nothing was due
MUST be recorded as an explicit no-work outcome, not left as an absence
indistinguishable from a materialization failure. A process starting MUST
NOT, by itself, be treated as evidence that collection completed or
succeeded. (`STD-OPS-COM-001`)

**A3.** This does NOT apply to a Clank with no triggered/scheduled
execution at all. It does NOT mandate any scheduler technology, a single
run/invocation table, a specific stage vocabulary, or a specific health
metric — any representation under which invocation and outcome are both
independently recoverable conforms. (`STD-OPS-COM-001`)

## B. Health-honesty two-axis complement (`STD-OPS-COM-002`)

**B1.** Where a Clank's health or alerting model depends on distinguishing
whether scheduled collection is running from whether it is producing
useful results, execution/liveness health and output/yield health MUST
remain independently representable — success on one MUST NOT be
presented, directly or by omission, as success on the other.
(`STD-OPS-COM-002`)

**B2.** Where source-level output is meaningful, a source producing zero
new observations MUST be classifiable as healthy, anomalous, or unknown
according to that source's own expected behavior — never silently
collapsed into a single undifferentiated "healthy" status merely because
the triggering/execution path succeeded. (`STD-OPS-COM-002`)

**B3.** This does NOT apply to a Clank with no scheduler and no external
sources (neither axis exists). It does NOT require exactly two fields,
one naming convention, or one score formula. (`STD-OPS-COM-002`)

## C. Promotion/soak qualification evidence integrity (`STD-OPS-COM-003`)

**C1.** Where a Clank qualifies a collector or source for production via
soak/natural-cycle evidence, that evidence MUST be structurally
verifiable from the Clank's own stored data, not merely asserted in
documentation or an operator's memory. (`STD-OPS-COM-003`)

**C2.** Wherever the natural/manual/deploy-verification/recovery
distinction affects qualification, the execution path itself MUST record
enough provenance to make that distinction after the fact. A material
change MUST start/reset the qualification window with the reset decision
recorded (what changed, why). An operational incident, host migration, or
manual recovery action MUST NOT itself reset accumulated qualification
evidence or be silently counted as ordinary natural-cycle evidence unless
the Clank's own policy explicitly permits that class of evidence.
(`STD-OPS-COM-003`)

**C3.** Where more than one gate governs promotion/production
eligibility, divergence between those gates MUST be detectable, and MUST
fail closed (treated as not-yet-eligible) rather than silently promoting
through whichever gate was updated. An operator intervention performed
during a qualification window MUST be distinguishable from a natural
qualification cycle — interventions are never required to be forbidden,
only distinguishable and non-qualifying unless policy explicitly says
otherwise. (`STD-OPS-COM-003`)

**C4.** This does NOT apply to a Clank with no promotion lifecycle
(everything production-immediately). It does NOT mandate any specific
cycle count, duration, maturity state machine, or single-gate
architecture — multiple gates are permitted provided divergence is
detectable and fails closed. (`STD-OPS-COM-003`)

## D. Exclusivity/ownership marker soundness (`STD-OPS-COM-004`)

**D1.** Where a Clank uses an exclusivity/ownership marker (a run lock,
lease, or ownership record) to coordinate execution across process or
execution-context boundaries, that marker's validity MUST be determinable
from state the granting authority itself observes, never inferred by the
validating context from a reusable or context-ambiguous identifier.
(`STD-OPS-COM-004`)

**D2.** Reclaiming a marker MUST rest on grantor-observable proof of the
owner's death or expiry. Honoring a marker as currently held, and any
action taken on the strength of it (including terminating the process it
identifies), MUST rest on that same standard of proof. (`STD-OPS-COM-004`)

**D3.** This does NOT apply to purely in-process locking (the marker
cannot outlive the context that validated it) or to a Clank with no
exclusivity/ownership marker at all. It does NOT mandate a specific
mechanism — OS advisory locks, database session-scoped locks, lease
services, kernel handles, and fencing tokens all conform; even a
PID+hostname+start-time tuple conforms if the start-time genuinely proves
identity. (`STD-OPS-COM-004`)

---

## Relationship to ratified UI and Data/Ontology standards

None of A-D restate or weaken a `STD-UI-*` or `STD-DATA-*` standard — see
each standard's own `notes` field for the specific overlap analysis:

- `STD-OPS-COM-002` (B) binds the **underlying data/operations-layer
  state model** that `STD-UI-COM-008`/`STD-UI-COM-012` (operator-facing
  display of health/coverage semantics) must not misrepresent —
  COMPLEMENTARY, not duplicative; B governs the truth beneath the
  display, not the display itself.
- No Operations standard touches `STD-DATA-*` — the domains are DISTINCT
  (execution/scheduling truth vs. data-representation truth).

## Relationship to `clank-architecture`

Three of the four standards above are explicit **narrow complements** to
`clank-architecture` governance that is already **ACTIVE** and
CI-enforced in several fleet repos — a materially different situation
from the UI and Data/Ontology domains, whose closest prior art was itself
only PROPOSED:

- **`STD-OPS-COM-002` (B)** is a narrow complement to **Fleet Law 3**
  (ACTIVE — "scheduler invocation is not job success"). Law 3 owns the
  health-honesty principle itself; B ratifies only the axis-vocabulary
  and conflation-forbidden semantics Law 3 leaves open across nine
  differently-named fleet implementations.
- **`STD-OPS-COM-003` (C)** is a narrow complement to **Fleet Law 8**
  (ACTIVE — promotion-gate integrity, three named historical violators).
  Law 8 owns promotion-gate authority; C owns evidence verifiability,
  reset-traceability, and drift-detectability.
- **`STD-OPS-COM-001` (A)** defers to **Fleet Law 5** (ACTIVE —
  single-scheduler authority) for which scheduler should be authoritative;
  A only makes duplicate/zombie automation *detectable*. A also
  complements `clank-architecture` ADR-0008/ADR-0011 (both PROPOSED, not
  ACTIVE) — their finer stage/no-work vocabulary stays clank-architecture's
  own; A ratifies only the coarser two-fact minimum.
- **`STD-OPS-COM-004` (D)** is a narrow complement to **Fleet Law 7**
  (ACTIVE — writer coordination) and **Fleet Law 5** (ACTIVE). Neither Law
  addresses the validity-proof soundness of the coordination primitive
  itself; D does. D is DISTINCT from `clank-architecture` ADR-0009
  (destructive production-action authority, also PROPOSED) — related in
  spirit (both forbid acting on unproven identity), unrelated in scope.

**Do not read any of the above as Standards Clank having activated,
migrated, or superseded a Fleet Law or ADR.** `clank-architecture` is a
separate authority; these standards bind narrowly and reference, they do
not incorporate by reference or restate.

## Not a standard (HOLD / DEFER / REHOME — never ratified, do not enforce)

These candidates came from the same Pass 0 evidence program but were
never advanced past Pass 0B's adjudication, or were advanced and then
explicitly parked pending a future domain. An implementation agent MUST
NOT treat any of these as a requirement, cite them in a conformance
report as if ratified, or use them to justify a code change:

- **Lifecycle-state model: BLOCKED is prose, not code** (cluster 14) —
  HOLD. Real mechanism gap (a "blocked from production" determination
  often lives only in a ticket, never an enforced code-level state), zero
  confirmed harmful mispromotion found.
- **Destructive production-action authority** (cluster 10) — DEFERRED to
  `clank-architecture` ADR-0009 (PROPOSED — REVIEWED DRAFT), the complete,
  incident-authored governing contract for this concern. The most severe
  concern found in the entire Operations survey; Standards Clank declined
  to compete with an existing, sufficient contract.
- **Config drift, remote-host deployment truth, schema/deploy fail-closed
  gating** (clusters 8+9+12) — REHOMED to a future, not-yet-started
  DEPLOYMENT domain.
- **Retry/restart notification idempotency** (cluster 15) — REHOMED to a
  future, not-yet-started DELIVERY domain.

Full detail:
[docs/operations/holds-disposition.md](holds-disposition.md) and
[docs/operations/pass0/candidates/holds-rehomes-defers.md](pass0/candidates/holds-rehomes-defers.md).

## Status of this domain

**FROZEN as `operations-standards-v1.0`** (2026-08-31, tag at commit
`7100f29`), after a hold-resolution / final-gap pass
([docs/operations/holds-disposition.md](holds-disposition.md)) concluded
**NO ESSENTIAL OPERATIONS CONTRACT MISSING**. See
[baselines/operations-standards-v1.0.json](../../baselines/operations-standards-v1.0.json).
