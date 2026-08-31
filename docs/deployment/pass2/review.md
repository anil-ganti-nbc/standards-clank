# Deployment Pass 2 — Adversarial Draft Review

Scope: review of the two Pass 1 `PROPOSED` texts only, against the Pass 0B
adjudication and cited governance. No fleet repository was recrawled, no
standard was drafted or ratified, and no ADR was activated.

## Verdicts

| Standard | Verdict | Exact revision required |
|---|---|---|
| STD-DEPLOY-COM-001 | **APPROVE FOR RATIFICATION SURVEY** | None |
| STD-DEPLOY-COM-002 | **APPROVE FOR RATIFICATION SURVEY** | None |

## COM-001 — deployment materialisation truth

### Coherence and counterexample attack

The invariant remains one coherent equality: declared intended deployment state
must be verifiably congruent with materially running state before completion is
claimed. Artifact/revision identity, deploy-critical configuration, required
wiring, and target scope are conditional facets: the text says “where
correctness depends” for configuration and wiring, and permits comparable
provenance rather than a universal field set.

The strongest counterexample survives unchanged: a signed-package,
externally-configured, Git-less deployment rolls over three hosts in ten
minutes. Package/build identity can compare intended and running artifacts;
external configuration is checked only when it is deploy-critical; each host
or declared rollout unit can remain explicitly partial/in-progress until that
declared scope converges. This does not require a Git checkout, SSH, Docker,
systemd, immutable images, or configuration hashes. A single-process local
deployment also conforms through a proportionate stated target and equivalent
identity evidence.

### Weakness attack and conclusion

The strongest wording risk is that “comparable trustworthy provenance” could be
misread as demanding a durable central deployment ledger. The acceptance text
correctly avoids that: it requires evidence capable of comparison, not a
particular record system. Mutable tags and symbolic labels are not categorically
banned; they fail only when they cannot establish actual running identity.

It does not duplicate OPS-COM-001. OPS-COM-001 asks whether an execution that
actually ran materialised and what outcome it produced; COM-001 asks whether
the thing running is the declared intended deployment. A stale but healthy old
revision can satisfy OPS-COM-001 and fail COM-001. Completion, not ordinary
runtime health, is the gated representation.

**Verdict: APPROVE FOR RATIFICATION SURVEY.** No exact revision is required.

## COM-002 — persistent-state compatibility gate

### Coherence and counterexample attack

The trigger is correctly limited to code whose persistent structured-state
contract can evolve independently. Stateless and schema-less Clanks are
explicitly N/A. The text permits deploy preflight, startup, first normal
transaction, or another trustworthy barrier; it permits code-first bridges,
DB-first changes, staged/expand-contract rollouts, and platform enforcement.
It mandates no schema-number encoding, SQL engine, migration framework, or
rollout order.

The strongest counterexample survives: compatibility-bridging code deploys
first, accepts work compatible with both old and new state, and migrates later.
Compatibility exists throughout, so no known incompatible normal work is
admitted. This is conforming. Process start, connectivity, table existence, or
`create_all` success remain insufficient by themselves when the persistent
contract requires more.

### Weakness attack and conclusion

“Known incompatibility” is correctly bounded: the rule does not pretend that a
Clank must predict unknown defects, but it forbids ordinary work continuing
after incompatibility is determined. “Normal work” is sufficiently constrained
by the exception for the compatibility barrier itself; a narrowly necessary
probe is not ordinary work being admitted under known mismatch.

The draft remains distinct from Data/Ontology semantics and Operations failure
recording. Data rules govern meaning and record structure; Operations can
truthfully record a failure after work was accepted. COM-002 prevents admission
of known incompatible work in the first place.

**Verdict: APPROVE FOR RATIFICATION SURVEY.** No exact revision is required.

## Cross-standard boundary

The standards are distinct and complementary. COM-001 asks whether intended
deployment state actually materialised in the asserted target. COM-002 asks
whether that deployed code may admit normal work against its persistent state.
A deployment can satisfy COM-001 but fail COM-002 when the intended artifact is
running with a known incompatible schema. It can satisfy COM-002 but fail
COM-001 when a different, compatible artifact/configuration/wiring is running.
No merge or wording revision is required.

## Fleet Law / ADR reconciliation

| Governance | Verified status | Relationship | Review finding |
|---|---|---|---|
| Fleet Law 5 | ACTIVE | COMPLEMENTARY | It owns scheduler/notification authority exclusivity; COM-001 verifies completion congruence. |
| Fleet Law 6 | ACTIVE | DEFER TO EXISTING AUTHORITY | It owns host-evidenced SHA/digest mechanics; COM-001 requires comparable parity without restating mechanics. |
| Fleet Law 9 | DEFERRED | DISTINCT | Its deployment-convergence proposal remains unactivated; no separate identity standard is resurrected. |
| ADR-0008 | existing ADR governance | NARROW COMPLEMENT | Execution liveness/materialisation is not intended-vs-running completion truth. |
| ADR-0009 | PROPOSED — REVIEWED DRAFT | DEFER TO EXISTING AUTHORITY | Destructive state mutation remains outside both drafts and is neither activated nor restated. |
| GIC-14 | architecture risk governance | COMPLEMENTARY | It identifies schema-drift risk; COM-002 supplies the narrow admission gate. |

No active Fleet Law is restated. Target identity remains only the stated scope
of a completion claim, not a standalone standard.

## Evidence sufficiency

Evidence disclosure remains explicit: all 10 Deployment Pass 0 incidents were
reused from Operations Pass 0; newly discovered Deployment-specific incidents
were **0**. The evidence is nevertheless sufficient for these two narrow
contracts because the adjudication demonstrated distinct normative failure
shapes, rather than counting reused events as new votes: honest Operations
records can describe an unintended runtime, and they can honestly describe a
failure after incompatible work was admitted. Independent positive convergence
supports each mechanism-neutral boundary. This is sufficient for a
ratification survey, not ratification itself.

## Hash/CRLF guard assessment

Pass 1's forward correction is adequate. The Pass 0/0B evidence guards now
hash LF-normalized semantic content (`CRLF` is normalized to `LF`) before
comparison with fixed canonical content hashes. A Windows `core.autocrlf`
checkout can therefore not create a false failure without a content change;
changing any normalized byte still fails the fixed hash. Frozen tags retain
their independent Git-resolution checks. No further harness change is needed.

## Ratification-readiness summary

Both drafts are ready for a separate ratification survey. That future survey
must independently decide whether to ratify; this review creates no ratified
status, no third Deployment standard, and no target or architecture mutation.
