# Candidate Card — DEP-D: Schema/Code Compatibility Gate

Status: CANDIDATE (Pass 0B adjudication). Not drafted, not ratified, not
normative.

## Candidate name
Schema/Code Compatibility Gate (from Pass 0A cluster 03).

## Plain-language invariant
If a Clank's running code depends on a persistent schema/state contract, a
deployment must verify compatibility between that code and the persisted
schema/state before normal work is accepted, and must fail closed on
incompatibility.

## Trigger / applicability
Applies only to Clanks whose code depends on a persistent schema or state
contract. Schema-less and stateless Clanks are trigger-unmet (N/A). Code-first
and DB-first deployment sequencing both conform if compatibility is
guaranteed. Verification may be eager or lazy (e.g., at startup) provided
incompatible state cannot silently receive normal work.

## Strongest evidence
Smartphone recurrence (DEP-INC-002): an implementation-shaped migration
action (`create_all()` as schema authority) was not a safe compatibility
gate and incorrect production state recurred — proving the duty is
compatibility, not migration machinery. Watch-clank independently ships a
fail-on-mismatch schema check; smartphone independently makes its migration
authority sole and fails entrypoints closed — two fleets converging on the
same gate without coordination.

## Incident references
DEP-INC-001, DEP-INC-002 (both reused from Operations Pass 0 — see
accounting in adjudication.md §5).

## Independent lineage count
2 (DEP-INC-001 watch-clank; DEP-INC-002 smartphone-clank), reinforced by
two independent positive implementations.

## Reused incident count
2. Newly discovered deployment-specific incidents: 0.

## Existing-standard distinctness proof
STD-DATA-COM-001–004 govern schema meaning/continuity, novelty, merge
discipline, and record separability — not the deployment transition.
STD-OPS-COM-001/002 are honest-recording duties that expose incompatibility
only after work has been accepted against incompatible state. An
implementation can conform to all ratified standards and still fail this
invariant because no ratified standard imposes the preventive fail-closed
duty at the deploy boundary.

## Fleet Law / ADR relationship
GIC-14 (architecture): COMPLEMENTARY — architecture flags the risk class;
this candidate owns the deployment-transition duty. No active Fleet Law
governs deploy-time compatibility gating; no conflict.

## Strongest counterexample
Stateless Clank with no persistent schema.

## Why it survives
The counterexample is trigger-unmet: the invariant's applicability is scoped
to persistent-schema dependence, so a stateless Clank is N/A rather than
non-conforming. Other counterexamples conform by construction: managed
databases enforcing compatibility satisfy the gate via platform mechanism;
blue/green with schema dual-writing holds compatibility for both revisions
during transition; schema-less stores with no contract are N/A. The
invariant demands compatibility, not any mechanism (`create_all`, Alembic,
or otherwise are equally conformant if the gate holds).

## Implementation freedoms
Any migration tool or none; code-first or DB-first; eager or lazy (startup)
verification; platform-enforced compatibility counts. No specific framework,
ORM, or migration machinery is required.

## Evidence strength
STRONG (two independent lineages plus two independent implementations).

## Fleet impact
MEDIUM-HIGH (every schema-bearing Clank).

## Standardisation risk
LOW-MEDIUM — the only trap is machinery prescription, avoided by the
compatibility-not-mechanics formulation and N/A scoping.

## Recommendation
ADVANCE (to drafting in a later pass, only if the operator schedules one).
