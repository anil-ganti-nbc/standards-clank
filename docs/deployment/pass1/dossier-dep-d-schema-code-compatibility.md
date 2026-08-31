# Dossier — STD-DEPLOY-COM-002

- **Candidate provenance:** DEP-D, `docs/deployment/pass0/candidates/dep-d-schema-code-compatibility-gate.md`.
- **Source cluster:** 03 schema/code compatibility.
- **Pass 0B disposition:** KEEP DISTINCT / ADVANCE.
- **Recommendation:** **READY FOR REVIEW**.

## Strongest evidence and accounting

Smartphone’s recurring incorrect production schema state (DEP-INC-002) is the
anchor: `create_all()` as schema authority did not establish compatibility;
the repair made migrations authoritative and entrypoints fail closed. Watch
independently uses a mismatch-refusing check. Both incidents are **REUSED FROM OPERATIONS PASS 0**. Across Pass 0A there are 10 reused incidents and **0 newly discovered Deployment-specific incidents**.

## Independent lineages

Watch and smartphone are two independent incident/remediation lineages, with
two independently built fail-closed safeguards. Both events are **REUSED FROM OPERATIONS PASS 0**. DEP-INC-001 supplies a related stale-artifact compatibility risk but is not inflated into another schema vote.

## Existing-standard distinctness proof

Data/Ontology standards govern the meaning, identity, provenance, and
structure of records. Operations standards record whether work ran and expose
honest resulting state. Neither prevents normal work from starting against a
known incompatible persistent contract. COM-002 is that preventive admission
gate, and does not restate data contracts or post-failure observability.

## Fleet Law / ADR relationship

Architecture GIC-14 identifies the risk class and is complementary. No active
Fleet Law owns deploy-time compatibility gating. ADR-0009 is irrelevant to
this standard’s non-destructive compatibility barrier and remains unactivated.

## Strongest counterexample and trigger analysis

A stateless Clank has no persistent schema/state contract and is N/A, not
non-conforming. Schema-less/ephemeral stores with no evolving compatibility
boundary are likewise N/A. A managed database, dual-write blue/green rollout,
code-first compatibility bridge, or DB-first migration can all conform once
normal incompatible work cannot be accepted.

## Acceptance analysis and implementation freedom

The draft requires a determination before normal incompatible work, fail-closed
handling of known mismatch, and an attributable refusal. It permits preflight,
startup, lazy first-work barriers, versions, capabilities, framework support,
or platform enforcement. It mandates neither Alembic, SQL, migrations table,
`create_all`, rollout order, downtime, nor rollback mechanism.

## Unresolved wording questions

Review should test “known incompatibility”: the draft deliberately does not
require prediction of unknown defects, yet it must not allow a superficial
connectivity check to be called a gate. Review should also test whether
“normal work” clearly excludes a narrowly necessary compatibility probe.
