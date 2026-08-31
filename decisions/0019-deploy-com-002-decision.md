# 0019 — Deployment ratification: STD-DEPLOY-COM-002 (Persistent-state compatibility gates normal operation)

Date: 2026-08-31
Status: PENDING (operator decision required)
Survey dossier: [../docs/deployment/pass3/ratification-survey.md](../docs/deployment/pass3/ratification-survey.md)
Standard: [../standards/deployment/STD-DEPLOY-COM-002.json](../standards/deployment/STD-DEPLOY-COM-002.json) (v1, PROPOSED)

An agent MUST NOT ratify this standard (see
[0002-no-agent-self-ratification.md](0002-no-agent-self-ratification.md)).
This record creates no normative status; the standard remains PROPOSED.

## Standard ID / version

STD-DEPLOY-COM-002, version 1, PROPOSED.

## Recommendation

RATIFY AS WRITTEN (agent recommendation in
[docs/deployment/pass3/ratification-survey.md](../docs/deployment/pass3/ratification-survey.md) —
operator decides).

## Evidence basis

Pass 0A/0B corpus: 10 confirmed Deployment incidents, **all reused from
Operations Pass 0; 0 newly discovered Deployment-specific incidents**
(disclosed, not hidden). Relevant lineages for this standard: DEP-INC-002
(smartphone recurring incorrect production schema state; `create_all()` as
schema authority was not a compatibility gate) and DEP-INC-001 (stale image
predating migrations) — both REUSED FROM OPERATIONS PASS 0 — plus two
independently built fail-closed safeguards (watch mismatch-refusing schema
check; smartphone Alembic-sole-authority fail-closed entrypoints).

## Strongest supporting argument

No ratified standard imposes a preventive admission gate at the
deploy/runtime boundary: Data/Ontology governs meaning and record structure;
Operations records failures honestly after incompatible work was already
admitted — which is exactly how the smartphone recurrence kept happening.
COM-002 prevents admission in the first place, and two fleets converged on
the gate independently.

## Strongest objection

The "known incompatibility" loophole: a system could simply never check
compatibility, so nothing ever becomes "known" and the gate never fires.
Answer on record: the requirement is a positive duty — "MUST determine
compatibility at a barrier that occurs before normal incompatible work is
accepted" — and acceptance 1 requires the running application to distinguish
compatible from known-incompatible state before normal incompatible work is
admitted. A never-checking system cannot perform the determination and
cannot conform. "Known" bounds only the impossible prediction of unknown
defects.

## Evidence-sufficiency result

SUFFICIENT — two independent incident/remediation lineages plus two
independent implementations; the reused events evidence a preventive duty
distinct from anything ratified, not a relabelling of Operations
failure-recording.

## Governance-overlap result

No PROBLEMATIC DUPLICATION. Fleet Law 5 (ACTIVE) DISTINCT; Fleet Law 6
(ACTIVE) DISTINCT; Law 9 (DEFERRED) DISTINCT; ADR-0009 (PROPOSED – REVIEWED
DRAFT, not ACTIVE) DISTINCT — no destructive-state obligation created, ADR-0009
neither activated nor restated; GIC-14 (architecture risk governance)
COMPLEMENTARY.

## Option A

Ratify STD-DEPLOY-COM-002 v1 as written (recommended by the Pass 3 survey).

## Option B (genuine alternative)

HOLD until a second independent schema-compatibility incident appears.
Genuine and defensible for an operator weighting incident novelty over
invariant distinctness — but it leaves a known, already-recurred production
failure shape unstandardised while two fleets have independently converged
on the gate.

## Operator decision

**PENDING** — awaiting operator ruling. Not ratified by this record or by
any agent.
