# Deployment Standards v1.0 — Release Notes

## Purpose

This baseline freezes the first ratified Deployment standards corpus as an
immutable historical record. It freezes exactly two implementation-neutral
contracts; it does not prescribe Git, SSH, Docker, systemd, SQL, a migration
framework, or a deployment topology.

- **Freeze date:** 2026-08-31
- **Frozen corpus commit:** `8f7f78bb3be351d66ed1f314576e0762e1211d9e`
- **Immutable tag:** `deployment-standards-v1.0`
- **Counts:** 2 RATIFIED / 0 PROPOSED

## Frozen standards

1. **STD-DEPLOY-COM-001 v1 — Deployment completion must be verified as intended state materially running.** A deployment may be represented as complete only when declared intended state is verified as materially running in its stated target scope. Artifact/revision identity, deploy-critical configuration, and required runtime wiring are conditional facets; partial/in-progress convergence remains explicitly representable.
2. **STD-DEPLOY-COM-002 v1 — Persistent-state compatibility must gate normal operation.** Where deployed code depends on an independently evolvable persistent-state contract, compatibility is determined at a barrier before normal incompatible work and known incompatibility fails closed. This is not a requirement to run migrations before deploy.

## Evidence and provenance

Evidence moved through Pass 0A inventory, Pass 0B adjudication, Pass 1
drafting, Pass 2 adversarial review, Pass 3 ratification survey, operator
ratification through decisions 0018/0019, and Pass 4 final-gap audit.

Evidence caveat: **10 confirmed Deployment incidents were reused from
Operations Pass 0; 0 newly discovered Deployment-specific incidents.** Reuse
was sufficient because the adjudicated standards capture distinct normative
failure shapes—intended-to-running completion congruence and preventive
compatibility admission—not additional incident votes.

Pass 4 concluded exactly: **NO ESSENTIAL DEPLOYMENT CONTRACT MISSING** and
**READY TO FREEZE DEPLOYMENT STANDARDS V1.0**.

## Governance and residual boundaries

- Target-environment identity has no standalone standard; it is COM-001's
  stated-target-scope facet.
- Fleet Law 6 remains the ACTIVE authority for identity mechanics; no duplicate
  Deployment standard is created. Law 9 remains DEFERRED and unactivated.
- Destructive state, rollback, and recovery remain rehomed to ADR-0009 and
  Architecture-Security-Recovery. ADR-0009 remains PROPOSED — REVIEWED DRAFT;
  this baseline neither activates nor duplicates it.
- Config congruence and partial runtime wiring remain COM-001 facets.
- Schema migration mechanics remain implementation detail beneath COM-002's
  compatibility outcome.

The reopening triggers are recorded in `docs/deployment/holds-disposition.md`.
No residual is reopened by this mechanical freeze.

## Agent and conformance state

The agent-facing layer is current: `docs/deployment/constitution.md`,
`standards/deployment/ratified-index.json`,
`standards/deployment/agent-checklist.json`, and the deterministic generator.
No Deployment conformance audit had been performed before this baseline.
Therefore no Deployment known-evidence-index is part of v1.0. Its absence is
intentional and does not weaken the normative freeze.

## Immutability

`deployment-standards-v1.0` is an annotated immutable tag. It must never be
moved or rewritten. Any later documentation correction, harness/agent-layer
fix, provenance correction, or conformance-audit artifact must land as a
forward commit on `master`; normative change requires normal governance.

No target Clank or `clank-architecture` content changed during this freeze. No
GitHub Release was created; existing baseline convention does not require one.
