# Agent-facing Deployment Constitution

This is the compact, implementation-facing layer over Standards Clank's
RATIFIED `STD-DEPLOY-*` standards — mirroring
[docs/operations/constitution.md](../operations/constitution.md)'s design
(which itself mirrors the UI and Data/Ontology constitutions) for the same
reason: so an agent building or auditing a Clank's deployment behavior
doesn't have to read every standard file individually. It is a summary, not
a replacement. **Where this document and a cited standard file disagree,
the standard file governs.** For the full
`requirement`/`rationale`/`acceptance`/`evidence` text behind any principle
here, read `standards/deployment/<ID>.json` directly, or look it up in
[`ratified-index.json`](../../standards/deployment/ratified-index.json).

**Authority rule for this document:** every normative statement below (a
MUST) is derived from, and cites inline, a RATIFIED `STD-DEPLOY-*`
standard. Nothing here is invented. Both Deployment standards are RATIFIED
— there is no "Pending" section. Several **candidate** concerns from the
same evidence program were explicitly MERGED, REHOMED, or REJECTED by Pass
0B and never became standards at all — see "Not a standard" at the end. Do
not treat any of those as a requirement; they were never ratified, drafted,
or reviewed as one.

**Trigger-scoping matters here, as in every other domain.** Each principle
below binds only Clanks with the specific architectural feature it
presupposes (a represented deployment transition; code depending on a
persistent structured-state contract with an independently evolvable
compatibility boundary). A Clank that genuinely lacks the feature is out of
scope by trigger, not in violation — see each standard's own `trigger`
field, and do not report a finding against a Clank for a concept it doesn't
have.

**Consequence, not algorithm.** Neither standard chooses a deployment tool,
transport, topology, migration framework, or rollout order — see
[decisions/0001](../../decisions/0001-standardise-contracts-not-implementation.md).
Do not propose "the fix" as a specific implementation; propose that the
*consequence* the standard requires (verified intended-vs-running
congruence before completion claims; fail-closed compatibility gating
before normal work) becomes true, however the Clank already shapes its
deployment and startup code.

**This domain has a governance relationship with `clank-architecture`**
like Operations does. Neither standard restates, replaces, or activates
any Fleet Law or ADR — see "Relationship to `clank-architecture`" below.

---

## A. Deployment completion congruence (`STD-DEPLOY-COM-001`)

**A1.** Where a Clank represents a transition from a declared intended
deployment state into a target runtime/environment as complete, it MUST
represent that completion only when evidence appropriate to the stated
target scope verifies that the declared intended state is materially
running. A deploy command exit, repository state, copied files, an image
build, or a restart command alone is NOT completion evidence.
(`STD-DEPLOY-COM-001`)

**A2.** The intended state MUST identify an artifact or revision by
trustworthy provenance capable of comparison with the running artifact or
revision — a build/package identity, digest, signed artifact identity, or
revision identifier all conform; Git is NOT required. Where correctness
depends on independently variable deploy-critical configuration or
required runtime wiring, that configuration or wiring MUST be included in
the verification. (`STD-DEPLOY-COM-001`)

**A3.** Where a deployment spans multiple targets or components, a
non-converged subset MUST be represented as partial or in-progress rather
than complete. Target environment identity is a facet of the completion
claim (the claim states the target scope it is made against), NOT a
standalone standard. (`STD-DEPLOY-COM-001`)

**A4.** This does NOT apply to a purely local tool with no meaningful
deployment transition. It does NOT require Git, a repository checkout, a
host, a container, immutable images, an atomic rollout, configuration
hashing of every file, or any particular transport, platform, or topology.
External/declarative deployment systems conform via their own
identity/parity evidence. (`STD-DEPLOY-COM-001`)

## B. Persistent-state compatibility gate (`STD-DEPLOY-COM-002`)

**B1.** Where deployed code depends on persistent structured state whose
schema or compatibility contract can evolve independently, the Clank MUST
determine compatibility at a barrier occurring before normal incompatible
work is accepted, and MUST fail closed on known incompatibility — normal
work MUST NOT be admitted while the deployed code and required
persistent-state contract are known to be incompatible.
(`STD-DEPLOY-COM-002`)

**B2.** The refusal MUST leave evidence identifying compatibility gating
as the reason normal work was refused — without prescribing a general
observability system. (`STD-DEPLOY-COM-002`)

**B3.** Process start, database connectivity, database existence, table
existence, `create_all` completion, or deployment-command success are
never, by themselves, compatibility proof. A backwards-compatible staged
rollout, code-first bridge, DB-first rollout, startup preflight, lazy
first-work barrier, capability check, or platform-enforced compatibility
all conform when they prevent normal incompatible work.
(`STD-DEPLOY-COM-002`)

**B4.** Stateless Clanks, schema-less Clanks, and ephemeral stores with no
evolving compatibility boundary are explicitly trigger-unmet (N/A), not
non-conforming. The standard does NOT mandate a SQL engine, Alembic, a
migrations table, migration ordering, downtime, or a rollback
implementation, and does NOT require predicting unknown defects — "known"
bounds the duty to state that has been determined at a real barrier.
(`STD-DEPLOY-COM-002`)

---

## Relationship to ratified UI, Data/Ontology, and Operations standards

Neither A nor B restates or weakens a `STD-UI-*`, `STD-DATA-*`, or
`STD-OPS-*` standard — see each standard's own `notes` field for the
specific overlap analysis:

- `STD-DEPLOY-COM-001` (A) is DISTINCT from `STD-OPS-COM-001`:
  Operations asks whether an execution that ran materialised and what
  outcome it produced; A asks whether the state materially running is the
  intended deployment state. A stale but healthy old revision can satisfy
  every Operations standard while failing A.
- `STD-DEPLOY-COM-002` (B) is DISTINCT from `STD-OPS-COM-001/002`:
  Operations honestly records failures after work is admitted; B prevents
  admission of known incompatible work in the first place. B is also
  DISTINCT from the `STD-DATA-*` corpus, which governs meaning, identity,
  provenance, and record structure — not the deployment-transition duty.

## Relationship to `clank-architecture`

Neither standard restates, replaces, or activates `clank-architecture`
governance:

- **`STD-DEPLOY-COM-001` (A)** defers to **Fleet Law 6** (ACTIVE) for
  host-evidenced SHA/digest identity mechanics — A requires comparable
  intended/running provenance without restating Law 6's evidence
  mechanics; per-repo Law 6 adoption coverage remains
  clank-architecture's concern. A is COMPLEMENTARY to **Fleet Law 5**
  (ACTIVE), which owns scheduler/notification authority exclusivity, and
  to ADR-0008 (execution liveness/materialisation overlap, not
  intended-vs-running completion truth). Law 9 (DEFERRED) remains
  clank-architecture's separate unactivated proposal; A does not
  resurrect or pre-empt it.
- **`STD-DEPLOY-COM-002` (B)** is COMPLEMENTARY to architecture **GIC-14**
  (schema-drift risk identification); B supplies the narrow admission
  gate. No ACTIVE Fleet Law owns deploy-time compatibility gating. B is
  DISTINCT from ADR-0009: it creates no destructive-state obligation.

**Do not read any of the above as Standards Clank having activated,
migrated, or superseded a Fleet Law or ADR.** ADR-0009 remains
PROPOSED — REVIEWED DRAFT (not ACTIVE); nothing in this domain activates
it. `clank-architecture` is a separate authority; these standards bind
narrowly and reference, they do not incorporate by reference or restate.

## Not a standard (MERGED / REHOMED / REJECTED — never ratified, do not enforce)

These candidates came from the same Pass 0 evidence program but were
merged, rehomed, or rejected by Pass 0B's adjudication and never became
standards. An implementation agent MUST NOT treat any of these as a
requirement, cite them in a conformance report as if ratified, or use
them to justify a code change:

- **Running revision identity (cluster 02)** — MERGED into A as the
  identity facet; the identity-evidence *mechanics* gap was REHOMED to
  `clank-architecture` (Fleet Law 6 adoption / deferred Law 9).
- **Partial deployment wiring (cluster 04)** — MERGED into A as the
  required-runtime-wiring facet; scheduler authority duplication is
  already owned by ACTIVE Fleet Law 5.
- **Target environment identity (cluster 06)** — REJECTED as a standalone
  standard (no confirmed wrong-host deployment in the corpus); retained
  only as the stated-target-scope facet of A.
- **Destructive state mutation / rollback & recovery (cluster 05)** —
  REHOMED to `clank-architecture` ADR-0009 (PROPOSED — REVIEWED DRAFT,
  not ACTIVE) via the ADR-0009 activation path. This is the one
  catastrophic incident family in the corpus; Standards Clank declined to
  compete with the existing, incident-authored governing contract.

Full detail:
[docs/deployment/pass0/adjudication.md](pass0/adjudication.md).

## Status of this domain

**2 RATIFIED, 0 PROPOSED** (2026-08-31, by operator acceptance of
[decisions/0018](../../decisions/0018-deploy-com-001-decision.md) and
[decisions/0019](../../decisions/0019-deploy-com-002-decision.md), following
the [Pass 3 ratification survey](pass3/ratification-survey.md)). The domain
is NOT yet frozen/tagged: no hold-resolution/final-gap pass has been
performed and no `deployment-standards-v1.0` baseline exists yet. No
Deployment conformance audit has been performed against any Clank, so no
known-evidence-index exists (same reasoning as Operations and
Data/Ontology at their agent-layer build time).
