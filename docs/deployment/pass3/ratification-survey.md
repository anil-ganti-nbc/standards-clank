# Deployment Pass 3 — Ratification Survey (2026-08-31)

Advisory governance pass. Evaluates the two PROPOSED `STD-DEPLOY-*` standards
(v1) for operator ratification, from the stored Pass 0A evidence, Pass 0B
adjudication, Pass 1 dossiers, and Pass 2 adversarial review. **No fleet
recrawl was performed.** The only governance material read was the referenced
Fleet Law / ADR status passages in the local `clank-architecture` checkout at
`e9c4a2b` (the same SHA recorded in the Pass 0A evidence log); no
`clank-architecture` file was modified. **No standard was ratified and no
normative wording was changed**; both standards remain PROPOSED.

## State taken over

- Canonical HEAD: `f22b7815d0287e982be8239271602879bf6bf7aa` = origin/master,
  tree clean. Full suite green (726 passed, 1 environmental skip since
  repaired — the frozen-tag subprocess guard now runs).
- Standards under survey: exactly two — STD-DEPLOY-COM-001 v1 PROPOSED,
  STD-DEPLOY-COM-002 v1 PROPOSED.
- Pass 0A evidence intact; Pass 0B adjudication intact; Pass 1 dossiers
  intact; Pass 2 review intact with verdict **APPROVE FOR RATIFICATION
  SURVEY** for both standards.
- Frozen tags intact: `ui-standards-v1.0` (`71e7ac4`),
  `data-ontology-standards-v1.0` (`f2f8a76`),
  `operations-standards-v1.0` (`b36239d`).

## Evidence-reuse caveat (explicit, carried forward)

All 10 confirmed Deployment incidents are reused from Operations Pass 0;
newly discovered Deployment-specific incidents: **0**. This survey does not
treat reuse as new evidence, and does not hide it.

## Survey scope and inputs

Read: both standard JSONs, both Pass 1 dossiers, Pass 2 `review.md`, Pass 0B
`adjudication.md`, the Pass 0A evidence package, and the governance status
passages named above. No target Clank repository was read.

---

## STD-DEPLOY-COM-001 — completion/congruence truth

### Core invariant as written

A deployment may be represented as complete only when the declared intended
deployment state is verifiably congruent with what is materially running in
the stated target scope.

### Re-check of required properties

| Required property | Verdict in final text |
|---|---|
| Artifact/revision identity conditional and implementation-neutral | YES — trigger-conditional (applies where completion is represented); acceptance 2 explicitly permits package/build identity, digest, signed artifact identity, or equivalent "rather than Git" |
| Deploy-critical config conditional, not universal | YES — "Where correctness depends on independently variable deploy-critical configuration"; no universal config inventory or hashing |
| Required runtime wiring conditional | YES — "Where required runtime wiring is necessary"; no restart/reload/scheduler/container/transport prescription |
| Target scope part of the assertion, not a standalone law | YES — acceptance 1: the completion claim identifies the target/scope it is made against; no target-identity standard was created (Pass 0B cluster 06 remains rejected standalone) |
| Explicit partial/in-progress permitted | YES — requirement's final sentence and acceptance 5 |
| Git not required | YES — explicit |
| Immutable images not required | YES — mutable provenance conforms when it can establish actual running identity |
| Atomic deploy not required | YES — partial/in-progress representation replaces atomicity; no rollout-atomicity mandate anywhere |
| External/declarative systems conform | YES — no mechanism, transport, or platform prescribed; platform-native identity satisfies acceptance 2 |
| Deploy-command success alone insufficient | YES — requirement names command exit, repository state, copied files, image build, restart as non-evidence alone; forbidden clause 1 repeats it |
| Runtime state, not repository state, determines completion | YES — forbidden clause 2 |

### Strongest challenge: unbounded breadth?

Could "almost any deploy check" be claimed to satisfy it? No. The closure is
structural, not rhetorical: the requirement enumerates the classic
non-evidence (command exit, repo state, copied files, image build, restart
command alone), and forbidden clause 6 forbids "claiming intended-to-running
equality without evidence capable of comparing the two states." A check that
cannot compare the intended and running states — however elaborate — fails
the forbidden clause; a check that can compare them satisfies the acceptance
criteria regardless of mechanism. The breadth challenge is closed by the
comparability requirement itself, not by vagueness.

### Distinctness test

YES — a stale, healthy, correctly-wired old revision can conform to
STD-OPS-COM-001 (truthful invocation/outcome records), COM-002 (honest
health), COM-003 (valid promotion evidence), COM-004 (valid ownership), and
all Data/UI standards, while violating COM-001 because the intended
deployment never materialised. The sentence completes convincingly; the
converse (Ops-recorded failure of the new code on a correct deployment) shows
the two contracts are not relabellings.

### Evidence sufficiency

**SUFFICIENT.** Reuse is acceptable here because the standard encodes a
distinct causal contract — intended-vs-running congruence — that no ratified
Operations standard owns; the same causal events evidence different failure
shapes in different domains, which is how the ratified Operations corpus
itself was built. It is not relabelling: Operations ratified record-honesty
about whatever runs; COM-001 gates the completion representation against the
intended state, a duty those records structurally cannot express (three
independent incident lineages: DEP-INC-001, 004, 009 — all reused, honestly
labelled; plus independent five-way/three-way verification convergence).

### Governance overlap

| Governance | Verified status | Relationship |
|---|---|---|
| Fleet Law 5 | ACTIVE | COMPLEMENTARY — owns scheduler/notification authority exclusivity; COM-001 owns completion congruence |
| Fleet Law 6 | ACTIVE | DEFER TO EXISTING AUTHORITY — owns host-evidenced SHA/digest mechanics; COM-001 requires comparable parity without restating mechanics |
| Law 9 | DEFERRED | DISTINCT — unactivated proposal; not resurrected or pre-empted |
| ADR-0009 | PROPOSED – REVIEWED DRAFT (not ACTIVE) | DISTINCT — destructive-mutation safety is outside COM-001's scope; not activated, not restated |

No PROBLEMATIC DUPLICATION.

### Strongest objection

That "trustworthy provenance capable of comparison" delegates the real
standard to implementer discretion: an operator could nominate a weak
provenance (e.g., a mutable tag) and claim congruence. Answer: the forbidden
clauses and acceptance 2 do not ban mutable labels categorically but require
the evidence to establish *actual running identity*; a mutable tag that
cannot do so fails the comparison-capability requirement. Residual judgement
is a proportionality feature of a mechanism-neutral MUST, the same
construction the ratified Operations standards use. Objection noted; not
disqualifying.

### Option B (genuine alternative)

Narrow COM-001 to artifact/revision identity parity only and leave
config/wiring congruence to a future standard. This is a real alternative —
but it would have left the Garmin wrapper divergence (DEP-INC-004, the
strongest single incident) unguarded until an unscheduled future pass, and
Pass 0B's merges (clusters 04, 06, charter DEP-C) would need re-opening.
Recommended against, recorded for the operator.

**Recommendation: RATIFY AS WRITTEN.**

---

## STD-DEPLOY-COM-002 — persistent-state compatibility gate

### Core invariant as written

Where normal operation depends on persistent-state compatibility, known
incompatibility must gate normal work fail-closed.

### Re-check of required properties

| Required property | Verdict in final text |
|---|---|
| Stateless/schema-less N/A | YES — trigger excludes them; acceptance 5 makes them trigger-unmet, not non-conforming |
| No migration framework mandated | YES — no Alembic/SQL/migrations-table requirement anywhere |
| No migration ordering mandated | YES — code-first, DB-first, expand-contract all named as conforming in acceptance 4 |
| Preflight/startup/lazy barriers conform | YES — requirement names deploy preflight, startup, first normal transaction, or another trustworthy gate |
| Backwards-compatible staged rollout conforms | YES — acceptance 4 |
| DB-first or code-first conform | YES — acceptance 4 |
| Connectivity/table existence/process start insufficient | YES — forbidden clause 2 names each explicitly, including `create_all` completion |
| Ordinary work must not proceed under known incompatible state | YES — requirement's MUST plus forbidden clauses 1, 3, 4 |
| Failure evidence narrow, not a general observability rule | YES — acceptance 3 requires attributable refusal evidence "without prescribing a general observability system" |

### Strongest challenge: the "known incompatibility" never-check loophole?

Could a system simply never check compatibility and therefore never face
"known" incompatibility? No. The requirement is not "refrain from admitting
work you know to be incompatible"; it is a positive duty: the Clank "MUST
determine compatibility at a barrier that occurs before normal incompatible
work is accepted." Acceptance 1 requires the running application to be able
to distinguish compatible from known-incompatible required persistent state
before normal incompatible work is admitted. A system that never checks
cannot perform that determination and cannot conform — the loophole is
closed by the determination duty, with "known" honestly bounding only the
impossible prediction of unknown defects. The Pass 2 review reached the same
conclusion; this survey independently confirms it from the text.

### Distinctness test

YES — a Clank can conform to every ratified standard and still violate
COM-002: it can honestly record invocation failures (COM-001), report health
axes truthfully (COM-002 Ops), hold valid promotion and ownership evidence,
and govern schema meaning under the Data standards, while still admitting
normal work against a known-incompatible persistent contract, because no
ratified standard imposes a preventive admission gate at the deploy/runtime
boundary. The sentence completes convincingly.

### Evidence sufficiency

**SUFFICIENT.** Two independent incident/remediation lineages (DEP-INC-002
smartphone recurrence; DEP-INC-001 stale-image compatibility risk — both
reused and labelled) plus two independently built fail-closed safeguards
(watch's mismatch-refusing schema check; smartphone's Alembic-sole-authority
fail-closed entrypoints). The reused events evidence a preventive duty
distinct from anything ratified: Operations standards record the damage
honestly after work is admitted; COM-002 prevents admission. Not relabelling.

### Governance overlap

| Governance | Verified status | Relationship |
|---|---|---|
| Fleet Law 5 | ACTIVE | DISTINCT — authority exclusivity is not compatibility gating |
| Fleet Law 6 | ACTIVE | DISTINCT — provenance evidence is not admission gating |
| Law 9 | DEFERRED | DISTINCT — convergence proposal does not own compatibility gating |
| ADR-0009 | PROPOSED – REVIEWED DRAFT (not ACTIVE) | DISTINCT — non-destructive compatibility barrier; no destructive-state obligation created; ADR-0009 neither activated nor restated |
| GIC-14 (architecture) | architecture risk governance | COMPLEMENTARY — flags the risk class; COM-002 supplies the narrow gate |

No PROBLEMATIC DUPLICATION.

### Strongest objection

That "normal work" versus the compatibility barrier's own work is a fuzzy
boundary a misbehaving implementation could drive a truck through (admitting
real work while calling it a probe). Answer: the boundary is stated in the
requirement ("before normal incompatible work is accepted") and the Pass 2
review's reading stands — a narrowly necessary compatibility probe is not
ordinary work; anything serving user/collector/production function is. The
wording is as tight as a mechanism-neutral gate can be, and the forbidden
clauses catch the driven truck. Objection noted; not disqualifying.

### Option B (genuine alternative)

HOLD COM-002 until a second independent schema-compatibility incident
appears. This is a real, defensible alternative for an operator who weights
incident novelty over invariant distinctness and implementation convergence —
but it would leave the known, recurring production failure shape
(DEP-INC-002 recurred) unstandardised while two fleets have already
converged on the gate. Recommended against, recorded for the operator.

**Recommendation: RATIFY AS WRITTEN.**

---

## Recommendations (advisory — one per standard)

| Standard | Recommendation |
|---|---|
| STD-DEPLOY-COM-001 | RATIFY AS WRITTEN |
| STD-DEPLOY-COM-002 | RATIFY AS WRITTEN |

Both meet the survey bar: implementation-neutral wording, correctly scoped
triggers, testable acceptance criteria, meaningful forbidden behavior, no
surviving legitimate counterexample, no problematic duplication of ACTIVE
governance, convincing distinctness against the ratified corpus, and
sufficient (disclosed-reuse) evidence. **This is a recommendation only.**
Ratification is the operator's decision, per
[decisions/0002-no-agent-self-ratification.md](../../../decisions/0002-no-agent-self-ratification.md);
both standards remain PROPOSED and no normative status was changed here.

## Operator decisions now required

1. `decisions/0018` — STD-DEPLOY-COM-001 v1: Option A (ratify as written,
   recommended) or Option B (narrow to artifact-identity parity and defer
   config/wiring facets). Status: PENDING.
2. `decisions/0019` — STD-DEPLOY-COM-002 v1: Option A (ratify as written,
   recommended) or Option B (hold until a second independent compatibility
   incident). Status: PENDING.
