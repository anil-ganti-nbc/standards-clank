# Deployment Pass 0B — Adversarial Adjudication

Adjudicates the six Deployment Pass 0A clusters. This document creates no
standard, ratifies nothing, and activates no ADR. Candidate cards in
[candidates/](candidates/) are candidate invariants for a future drafting pass,
not normative truth.

**Canon:** GitHub `anil-ganti-nbc/standards-clank`, HEAD
`02c74108e89bc99742aec5674e4632e19f822a12`. Frozen baselines
ui-standards-v1.0, data-ontology-standards-v1.0, operations-standards-v1.0 are
untouched; no tags moved; no target Clank and no clank-architecture file was
modified.

**Central evidence caveat (applied to every disposition):** all 10 ledger
incidents are reused from Operations Pass 0. Zero newly discovered
Deployment-specific incidents exist. No disposition below counts a reused
incident as a new independent vote. Distinctness was judged on whether the
proposed invariant differs from the ratified Operations/Data invariants — not
on incident novelty, because the same causal events may legitimately evidence
different contracts in different domains (Operations ratification itself drew
on this shared corpus).

---

## 1. Summary table

| Cluster | Structural disposition | Recommendation | Existing-standard overlap | Governance overlap |
|---|---|---|---|---|
| 01 materialisation-truth | KEEP DISTINCT | ADVANCE | COM-001/002/003 record what runs; none require intended-vs-running equality | Fleet Law 5/6 ACTIVE (complementary); ADR-0008 (non-competing) |
| 02 running-revision-identity | MERGE WITH 01 | REHOME (residual gap → clank-architecture Law 6/Law 9) | Identity parity retained as a facet of 01; mechanics already Law 6 | Fleet Law 6 ACTIVE, CI-backed; Law 9 DEFERRED |
| 03 schema-code-compatibility | KEEP DISTINCT | ADVANCE | Data COM-001–004 govern schema meaning/authority, not deploy-time gating; OPS standards are diagnostic, not preventive | GIC-14 (architecture); none conflicting |
| 04 partial-deployment-wiring | MERGE WITH 01 | ADVANCE (as facet of 01; no independent standard) | Wire-completeness is one facet of materialised state | Fleet Law 5 ACTIVE already owns scheduler authority exclusivity |
| 05 rollback-recovery-and-mutation | REHOME DOMAIN | REHOME (Architecture/Security-Recovery via ADR-0009) | None ratified; no Standards Clank gap proven | ADR-0009 PROPOSED — REVIEWED DRAFT (not ACTIVE); Law 5 shared |
| 06 target-environment-identity | MERGE WITH 01 | REJECT (as standalone; target-coverage facet retained by 01) | "Target-evidenced" requirement of 01 subsumes it | None beyond Law 6 |
| (charter DEP-C config/runtime congruence — no standalone 0A cluster) | MERGE WITH 01 | ADVANCE (as facet of 01) | Loaded-config parity is a facet of materialised state | Law 6 (identity mechanics); none conflicting |

Result: **2 ADVANCE candidates** (DEP-A materialisation truth; DEP-D
schema/code compatibility), four merges, one rehome, one standalone rejection.
Deployment survives as a distinct normative domain — but as a **small** one:
two contracts, not six standards.

---

## 2. Cluster adjudications

### 2.1 Cluster 01 — materialisation truth — KEEP DISTINCT / ADVANCE

**Adversarial test:** can a deployment be wrong while every operational
invocation/outcome record fully conforms to STD-OPS-COM-001? Yes — the
decisive case: an old deployed revision keeps running correctly, records
perfect invocation/outcome facts (COM-001), reports its health axes honestly
(COM-002), and carries valid promotion evidence (COM-003), while the intended
new state never materialised. Every ratified OPS standard governs the honesty
of records about *whatever is running*; none requires that the running state
equal the *intended* deployment. That equality is the Deployment contract.

**Distinctness proof (mandatory sentence):** An implementation can conform to
all existing ratified standards and still fail this invariant because
STD-OPS-COM-001/002/003 require records of invocations, outcomes, health
claims, and promotion evidence to be truthful about the running thing, and
COM-004 requires ownership validity — none of them requires the declared
intended deployment (revision, deploy-critical configuration, required
runtime wiring) to be verified as materially running in the stated target.

**Minimal Deployment-specific fact set (implementation-neutral):**
1. The intended deployed state is declared (intended revision/artifact,
   deploy-critical configuration, required runtime wiring components).
2. A deployment may be represented as complete only when target-evidenced
   checks confirm the declared state is what is materially running in a
   stated target.
No tool, mechanism, transport, or platform is prescribed.

**Merges absorbed here (explicit):**
- **02 running revision identity** — intended-vs-running equality is
  meaningless without identity comparison, so identity parity is a required
  facet of this invariant. However, the *mechanics* of identity evidence are
  already owned by **Fleet Law 6 (ACTIVE, CI-backed)**: exact SHA/digest
  evidenced on host. Restating Law 6 as a Standards Clank standard would be a
  PROBLEMATIC DUPLICATION; the residual gap is **adoption coverage in target
  repos** (architecture conformance suite is confirmed; per-repo adoption is
  not), which is an enforcement concern for clank-architecture — rehomed
  there (Law 6 adoption / deferred Law 9 trigger). Minimum identity evidence
  where no OCI image exists is a Law 6 refinement question, not a new
  standards-clank contract.
- **Charter DEP-C config/runtime congruence** (no standalone 0A cluster —
  correctly pre-merged by 0A): independently mutable configuration is a real
  distinct risk (Garmin wrapper divergence, DEP-INC-004), but stale loaded
  config is simply one facet of "declared state is not materially running."
  A declarative platform with immutable config makes the facet trivially
  satisfied, which is exactly how a merged facet should behave.
- **04 partial wiring** — see 2.3.
- **06 target-environment identity** — see 2.5.

**Counterexample test (strongest legitimate architectures):**
- *Serverless / managed platform*: the declared revision/alias vs the served
  revision is precisely the parity this invariant demands; verification is
  platform-native. Survives.
- *Git-less packaged deployment*: identity via package version, artifact
  digest, or build metadata — the invariant requires attribution, not Git.
  Survives.
- *Immutable container images*: config baked into the image collapses the
  config facet; the parity duty remains for wiring. Survives.
- *Blue/green, rolling multi-host*: legitimate as long as completeness claims
  are lane/host-scoped and each claimed-complete unit satisfies parity.
  Survives.
- *Single-host local Clank*: duty is trivial but not vacuous. Survives.
- *Intentional dev/experimental divergence*: legitimate when explicit and
  isolated (feature-phone lane topology); the invariant forbids *undeclared*
  divergence, not deliberate lanes. Survives.

**Evidence scoring:** EVIDENCE: STRONG (4 incidents; 3 independent causal
lineages: DEP-INC-001 stale-tag compose start, DEP-INC-004 wrapper drift,
DEP-INC-009 unresolved host/repo drift; independent positive convergence in
feature-phone, smartwatch five-way check, Diagnostic phase0). FLEET IMPACT:
HIGH. STANDARDISATION RISK: MEDIUM (must not prescribe tooling and must not
duplicate Laws 5/6 — mitigated by the implementation-neutral fact set and the
explicit deference above). INDEPENDENT LINEAGES: 3. REUSED INCIDENTS: 4
(DEP-INC-001, 004, 006, 009). NEW DEPLOYMENT-SPECIFIC INCIDENTS: 0.

Recommendation: ADVANCE → candidate card
[candidates/dep-a-deployment-materialisation-truth.md](candidates/dep-a-deployment-materialisation-truth.md).

### 2.2 Cluster 02 — running revision identity — MERGE WITH 01 / REHOME

**Attack:** the cluster's own file concedes the risk: a standard here would
"directly restate ACTIVE Law 6." Law 6 already requires host-evidenced exact
SHA/digest and is CI-backed. A Standards Clank standard adding nothing but
vocabulary is a PROBLEMATIC DUPLICATION. The genuine residual item —
per-repo adoption of Law 6 evidence, and the minimum-identity question for
non-OCI artifacts — is architecture-governance work, not a new normative
contract here.

**Disposition:** identity parity is retained as a mandatory facet of the
ADVANCE candidate from cluster 01 (so nothing evidential is lost); the
standardisation gap is **REHOME**d to clank-architecture (Law 6 adoption
coverage; Law 9 DEFERRED as the natural home if deployment convergence is
ever promoted). Reopening trigger: if clank-architecture declines the rehome
and a materialisation incident recurs that parity evidence would have caught.

### 2.3 Cluster 03 — schema/code compatibility — KEEP DISTINCT / ADVANCE

**Attack:** is this Data/Ontology? No — checked against the ratified data
standards by title and scope: STD-DATA-COM-001 (continuity/epoch), COM-002
(novelty views), COM-003 (entity merges), COM-004 (record separability). They
govern meaning, provenance, and record discipline; none imposes a
deployment-transition duty. Is it already Operations? No — COM-001 records
failing invocations honestly *after* they happen; COM-002 keeps health claims
honest while a process can be honestly healthy before its first query; the
smartphone recurrence (DEP-INC-002) shows the failure class recurs inside
operations that were otherwise well-evidenced. Is `create_all` normative? No
— implementation detail; Alembic, `create_all`, or any mechanism conforms if
compatibility is guaranteed and mismatch fails closed.

**Distinctness proof (mandatory sentence):** An implementation can conform to
all existing ratified standards and still fail this invariant because no
ratified standard requires a deployment to verify compatibility between
running code and the persisted schema/state contract *before normal work is
accepted and to fail closed on incompatibility*: Data standards govern
schema meaning/authority, and OPS standards are honest-recording duties that
observe the damage rather than gate the transition.

**Trigger/applicability:** applies only to Clanks whose code depends on a
persistent schema/state contract; schema-less and stateless Clanks are
trigger-unmet (N/A). No migration machinery is required; code-first and
DB-first sequencing both conform if compatibility is guaranteed before work
acceptance. Verification may be eager or lazy at startup, provided
incompatible state cannot silently receive normal work.

**Counterexample test:** *stateless Clank* → N/A by trigger. *Managed
database with compatibility enforcement* → satisfies the gate by platform
mechanism. *Blue/green with schema dual-writing* → conforms: compatibility
holds for both revisions during transition. *Schema-less JSON store with no
contract* → N/A. The invariant survives all of them because it demands
compatibility, not any mechanism.

**Evidence scoring:** EVIDENCE: STRONG (2 independent incident lineages,
DEP-INC-001 and DEP-INC-002, plus independent fail-closed implementations in
watch-clank and smartphone-clank — two fleets arrived at the same gate
without coordination). FLEET IMPACT: MEDIUM-HIGH (every schema-bearing
Clank). STANDARDISATION RISK: LOW-MEDIUM (machinery-neutrality is the only
trap, and the trigger scoping avoids it). INDEPENDENT LINEAGES: 2. REUSED
INCIDENTS: 2 (DEP-INC-001, 002). NEW DEPLOYMENT-SPECIFIC INCIDENTS: 0.

Recommendation: ADVANCE → candidate card
[candidates/dep-d-schema-code-compatibility-gate.md](candidates/dep-d-schema-code-compatibility-gate.md).

### 2.4 Cluster 04 — partial deployment wiring — MERGE WITH 01 / ADVANCE (facet)

**Attack:** the attempted separate invariant — "all deployment-required
runtime components must reach a mutually compatible target state before
deployment is represented as complete" — is not a different invariant from
materialisation truth; it is the same equality check with the state
decomposed into components. The wiring facet (DEP-INC-004 wrapper drift,
DEP-INC-007 coexisting schedules) is fully covered by the cluster-01 fact
set's "required runtime wiring" element. Scheduler-authority duplication is
already owned by **Fleet Law 5 (ACTIVE, CI-backed)**; adding a topology
standard here risks competing authority with an active law.

**Disposition:** MERGE WITH 01. No independent standard. Recommendation
ADVANCE solely in the sense that the facet is carried by the advanced
cluster-01 candidate. Reopening trigger: none needed; facet is retained.

### 2.5 Cluster 06 — target environment identity — MERGE WITH 01 / REJECT

**Attack:** aggressive, as instructed. There is **one** missed-host incident
(DEP-INC-008) and **no confirmed wrong-host deployment anywhere in the
corpus**. The scary framing ("deployment authority must know which
environment it is mutating") is generic host-inventory/security vocabulary
with a single data point. What the evidence actually shows is narrower: a
verification sweep asserted a fleet-wide negative without stating its target
coverage. That failure mode — verification claims must state what target they
actually covered — is precisely the "stated target" element of the
cluster-01 fact set (target-evidenced checks *in a stated target*).

**Disposition:** MERGE WITH 01 as the target-coverage facet; **REJECT** as a
standalone concern/standard. Reopening trigger: any confirmed wrong-host
deployment incident (none exists today).

### 2.6 Cluster 05 — rollback, recovery, and deploy-time state mutation — REHOME DOMAIN / REHOME

**Attack:** the entire evidence base is **one incident family**
(DEP-INC-005, explicitly INCIDENT INHERITANCE — feature-phone total volume
loss and smartwatch partial loss are one lineage, not two independent
votes). That lineage already produced **ADR-0009, verified
PROPOSED — REVIEWED DRAFT (not ACTIVE)**, whose mechanically checkable
pieces already live in architecture conformance. A Standards Clank deployment
standard here would create **competing authority** with a drafted ADR awaiting
activation, with zero incremental evidence. One catastrophic incident
justifies a safety invariant — and that invariant already exists, in the
governance layer that owns it.

**Disposition:** REHOME DOMAIN → clank-architecture / Security-Recovery,
via the ADR-0009 activation path. Standards Clank claims no ownership.
Reopening triggers: (a) ADR-0009 activation stalls or is abandoned;
(b) a destructive state-mutation incident recurs after ADR-0009 activation,
demonstrating the ADR contract is insufficient; (c) a fleet-wide backup /
recoverability evidence gap is independently evidenced as a future Recovery
domain. ADR-0009 status is recorded here exactly as: **PROPOSED — REVIEWED
DRAFT, not active, not activated by this pass.**

### 2.7 Charter DEP-C — config/runtime congruence (no standalone cluster)

Pass 0A did not raise config congruence as its own cluster; the charter
asked whether it should become one. Adjudicated: **MERGE WITH 01 / ADVANCE
as facet.** Independently mutable config is a genuine risk (DEP-INC-004), but
mirroring artifact categories (code vs config vs wiring) as separate
standards is taxonomy, not evidence; each is a facet of one declared-vs-
materialised equality. Immutable-config platforms trivially satisfy the
facet, which is the correct behaviour for a facet rather than a standalone
contract.

---

## 3. Fleet Law / ADR reconciliation

| Governance | Status (verified) | Relationship to surviving candidates |
|---|---|---|
| Fleet Law 5 (single scheduler/notification authority) | ACTIVE, CI-backed | COMPLEMENTARY with DEP-A: Law 5 owns authority exclusivity; DEP-A owns materialised parity. No duplication. |
| Fleet Law 6 (host-evidenced SHA/digest) | ACTIVE, CI-backed | DEFER TO EXISTING AUTHORITY for identity mechanics; DEP-A requires parity but does not restate Law 6's evidence mechanics. Residual per-repo adoption gap rehomed to architecture. |
| Fleet Law 9 (deployment convergence) | DEFERRED | Natural home for the rehomed cluster-02 residual; no conflict. |
| ADR-0008 | ADR governance (execution liveness/materialisation overlap) | COMPLEMENTARY; no competing authority created. |
| ADR-0009 (state separation, destructive-operation safety) | **PROPOSED — REVIEWED DRAFT (NOT ACTIVE)** | Cluster 05 DEFERS TO this existing authority; not activated, not duplicated. |
| GIC-14 (architecture) | architecture governance | Overlaps cluster 03; COMPLEMENTARY — architecture flags the risk class, the candidate standard owns the deployment-transition duty. |

---

## 4. Cross-domain test — mandatory sentences

**DEP-A (materialisation truth):** an implementation can conform to
STD-OPS-COM-001, COM-002, COM-003, COM-004 and every Data/Ontology standard
and still fail this invariant because all of those standards govern the
truthfulness and discipline of records about whatever happens to be running
— invocation facts, health axes, promotion evidence, ownership validity,
record separability — and none requires the declared intended deployment to
be verified as materially running in a stated target; a stale old revision
satisfying every record-honesty duty is the canonical conforming failure.

**DEP-D (schema/code compatibility gate):** an implementation can conform to
all ratified standards and still fail this invariant because STD-DATA-COM-001
through 004 govern schema meaning, novelty, merge discipline, and record
separability — not the deployment transition — while STD-OPS-COM-001/002
record and expose incompatibility damage only *after* work has been accepted
against incompatible state; no ratified standard imposes the preventive
fail-closed duty at the deploy boundary.

Both sentences complete convincingly; both candidates are therefore
distinctness-proven against the ratified corpus.

---

## 5. Evidence accounting (undisguised)

- Total confirmed incidents in the Deployment ledger: 10.
- Reused from Operations Pass 0: **10 (all).**
- Newly discovered Deployment-specific incidents: **0.**
- Independent causal lineages across the ledger: materialisation parity (3:
  INC-007, INC-016/017 shapes, INC-004-wrapper, INC-030/031-host-drift
  family), destructive mutation (1 family: INC-041/036), plus shared-
  governance records (INC-014, INC-040). Nothing in this pass adds a vote.
- Both ADVANCE candidates rest on reused incidents whose *deployment-specific
  failure shape* differs from the shape Operations ratified against. That is
  the sole justification for advancing; it is recorded so no future reader
  mistakes reuse for fresh evidence.

---

## 6. Held / rehomed / rejected — consolidated record

- **HOLD:** none. No cluster carried an unresolved factual ambiguity of the
  kind that requires holding; weak clusters were decidable by merge/reject.
- **REHOME:** cluster 02 residual (identity-evidence mechanics/adoption →
  clank-architecture Law 6 / deferred Law 9); cluster 05 (destructive state
  mutation & recovery → ADR-0009 activation path, Architecture/
  Security-Recovery).
- **REJECT:** cluster 06 as a standalone concern (absorbed as the
  target-coverage facet of DEP-A); any future proposal to restate Fleet
  Law 5 or Law 6 as STD-DEPLOY standards (PROBLEMATIC DUPLICATION).

## 7. Process assertions

- All six 0A clusters adjudicated; each received exactly one structural
  disposition and one recommendation.
- Every ADVANCE candidate has a counterexample record and an
  existing-standard distinctness proof (cards in candidates/).
- No STD-DEPLOY-* files exist; nothing was ratified; frozen baselines,
  tags, and Pass 0A raw evidence are unchanged; no target Clank and no
  clank-architecture content was modified.
- Deployment Pass 1 does **not** begin here.
