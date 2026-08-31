# 0018 — Deployment ratification: STD-DEPLOY-COM-001 (Deployment completion verified as intended state materially running)

Date: 2026-08-31
Status: PENDING (operator decision required)
Survey dossier: [../docs/deployment/pass3/ratification-survey.md](../docs/deployment/pass3/ratification-survey.md)
Standard: [../standards/deployment/STD-DEPLOY-COM-001.json](../standards/deployment/STD-DEPLOY-COM-001.json) (v1, PROPOSED)

An agent MUST NOT ratify this standard (see
[0002-no-agent-self-ratification.md](0002-no-agent-self-ratification.md)).
This record creates no normative status; the standard remains PROPOSED.

## Standard ID / version

STD-DEPLOY-COM-001, version 1, PROPOSED.

## Recommendation

RATIFY AS WRITTEN (agent recommendation in
[docs/deployment/pass3/ratification-survey.md](../docs/deployment/pass3/ratification-survey.md) —
operator decides).

## Evidence basis

Pass 0A/0B corpus: 10 confirmed Deployment incidents, **all reused from
Operations Pass 0; 0 newly discovered Deployment-specific incidents**
(disclosed, not hidden). Relevant lineages for this standard:
DEP-INC-001 (stale image via soft default), DEP-INC-004 (production wrapper
omitting required proxy wiring), DEP-INC-009 (live host trailing its
repository) — three independent causal lineages, all reused incidents,
plus independent cross-Clank convergence on identity-verification practice
(watch, oem-radar, smartwatch, CTW, SemInt).

## Strongest supporting argument

The invariant closes a structural gap no ratified standard owns: Operations
standards govern truthful records about whatever is running, so a stale but
healthy old revision can conform to STD-OPS-COM-001/002/003/004 perfectly
while the intended deployment never materialised. Completion congruence is
the distinct duty, and three independent fleets independently built
verification shaped like it.

## Strongest objection

"Trustworthy provenance capable of comparison" delegates real strength to
implementer discretion — a weak provenance (e.g., a mutable tag) could be
nominated and congruence merely claimed. Answer on record: forbidden clause 6
requires evidence *capable of comparing* the two states; a mutable tag that
cannot establish actual running identity fails regardless of nomination.
Residual judgement is the proportionality cost of a mechanism-neutral MUST.

## Evidence-sufficiency result

SUFFICIENT — reuse is acceptable because the encoded causal invariant
(intended-vs-running completion congruence) is distinct from every ratified
contract; this is not relabelling Operations record-honesty as deployment
truth.

## Governance-overlap result

No PROBLEMATIC DUPLICATION. Fleet Law 5 (ACTIVE) COMPLEMENTARY; Fleet Law 6
(ACTIVE) — DEFER TO EXISTING AUTHORITY for identity-evidence mechanics;
Law 9 (DEFERRED) DISTINCT; ADR-0009 (PROPOSED – REVIEWED DRAFT, not ACTIVE)
DISTINCT.

## Option A

Ratify STD-DEPLOY-COM-001 v1 as written (recommended by the Pass 3 survey).

## Option B (genuine alternative)

Narrow the standard to artifact/revision identity parity only and defer
deploy-critical-config and runtime-wiring congruence to a future standard.
Genuine and internally consistent, but it leaves the strongest single
incident (DEP-INC-004 wrapper divergence) unguarded and re-opens the Pass 0B
merges of clusters 04/06 and charter DEP-C.

## Operator decision

**PENDING** — awaiting operator ruling. Not ratified by this record or by
any agent.
