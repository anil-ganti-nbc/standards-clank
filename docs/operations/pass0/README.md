# Operations Pass 0A — Evidence Inventory

**Status: evidence only. Nothing in this directory is a standard, a draft
standard, ratification, or remediation.** No `STD-OPERATIONS-*` file
exists anywhere in this repository, and none should be created from this
directory without a separate, explicit adjudication and drafting pass —
see [docs/governance.md](../../governance.md).

## What this is

A structured inventory of Operations-domain scar tissue across the Clank
fleet — scheduler truth vs. actual execution, natural-cycle vs.
manual/deploy-cycle accounting, soak clocks and reset semantics,
lifecycle states, promotion readiness, source starvation, config drift,
schema/deploy readiness, stale automation, retry/restart authority,
health vs. scheduler state, remote host/deployment truth,
"scheduled" vs. "actually running," partial deploys, and safe manual
intervention during soak — mined read-only from nine fleet Clanks,
`clank-architecture`, and `diagnostic-clank` (both its GitHub repository
and the live NAS incident log at `http://192.168.0.105:8420/`) at their
current state as of 2026-08-31.

This inventory does **not** decide which patterns should become
standards. It exists so a separate adjudication pass (Pass 0B — assigned
to a different assistant, "ZLM," per the operator's explicit division of
labor) has a structured, cited corpus to work from instead of
re-surveying the fleet.

## Built on top of

Both frozen baselines — `ui-standards-v1.0` (tag `ui-standards-v1.0`,
commit `d113207`) and `data-ontology-standards-v1.0` (tag
`data-ontology-standards-v1.0`, commit `464a805`). This pass did not read
either freeze as a constraint on scope — operations is a distinct domain
from both — but it also did not touch `standards/ui/`, `standards/data-ontology/`,
`docs/ui/`, `docs/data-ontology/`, `baselines/`, or any UI/DATA-domain
decision/audit file.

## Method

Six parallel read-only survey agents: five covering the nine fleet
Clanks in pairs (watch-clank+oem-radar; chinese-tech-wire+korean-tech-wire;
feature-phone-clank+smartphone-clank; smartwatch-clank+tablet-clank;
semiconductor-intelligence+clank-architecture), one mining
`diagnostic-clank` specifically — both its GitHub repository (cloned
read-only into a local scratch directory for this pass only, not
vendored into this repository) and the live NAS incident log, per the
operator's explicit instruction that Operations is "probably where the
largest pile of actual incidents lives." Each agent was instructed to
cite file:line for every claim, classify lineage (independent /
inherited-copied / lineage-uncertain), and prioritize incident evidence
against the 15 topics named in the operator's brief (reproduced below).
`clank-architecture` was surveyed for evidence only, read-only, not
modified. Full per-repo survey output is preserved in
[evidence-log.md](evidence-log.md) — the cluster files below are a
synthesis of it, not a replacement; where a cluster file's citation looks
incomplete, the evidence log has the fuller original text.

### The 15 topics surveyed against

1. Scheduler truth vs. actual execution
2. Natural-cycle vs. manual/deploy-cycle accounting
3. Soak clocks and reset semantics
4. Experimental/production/mothballed/blocked lifecycle states
5. Promotion readiness
6. Source starvation / observation collapse
7. Config drift
8. Schema/deploy readiness
9. Stale automation
10. Retry/restart authority
11. Health vs. scheduler state
12. Remote host/deployment truth
13. "Scheduled" vs. "actually running"
14. Partial deploys / stale code
15. Safe manual intervention during soak

## Contents

- [evidence-log.md](evidence-log.md) — the six raw survey reports, preserved verbatim for traceability
- [incident-ledger.md](incident-ledger.md) — 45 incidents found, one row per incident, with repo/date/harm/root-cause/remediation/recurrence-risk
- [terminology-map.md](terminology-map.md) — cross-fleet table of what each scheduler/soak/lifecycle/health/lock term actually means per repo
- [clusters/](clusters/) — 15 candidate-cluster files, each a structured writeup of one concern (see below)
- [handoff.md](handoff.md) — the compact adjudication package for the next (ZLM) pass — HIGH-priority clusters only

## Candidate clusters

| Cluster | Topics | Confidence | Priority |
|---|---|---|---|
| [scheduler-truth-materialization-gap](clusters/scheduler-truth-materialization-gap.md) | 1, 13 | STRONG | HIGH |
| [pid-namespace-unsafe-stale-lock-reclaim](clusters/pid-namespace-unsafe-stale-lock-reclaim.md) | 10 | STRONG | HIGH |
| [health-state-vs-scheduler-enabled-conflation](clusters/health-state-vs-scheduler-enabled-conflation.md) | 11 | STRONG | HIGH |
| [source-starvation-zero-vs-healthy-conflation](clusters/source-starvation-zero-vs-healthy-conflation.md) | 6 | STRONG | HIGH |
| [natural-cycle-vs-manual-trigger-provenance-gap](clusters/natural-cycle-vs-manual-trigger-provenance-gap.md) | 2 | STRONG | HIGH |
| [soak-clock-reset-semantics-and-material-change-judgment](clusters/soak-clock-reset-semantics-and-material-change-judgment.md) | 3 | MODERATE | HIGH |
| [dual-gate-promotion-authority-drift](clusters/dual-gate-promotion-authority-drift.md) | 5 | STRONG | HIGH |
| [config-drift-local-repo-deployed](clusters/config-drift-local-repo-deployed.md) | 7 | STRONG | HIGH |
| [remote-host-deployment-truth-verification](clusters/remote-host-deployment-truth-verification.md) | 12, 14 | STRONG | HIGH |
| [destructive-action-authority-before-mutation](clusters/destructive-action-authority-before-mutation.md) | 10 | STRONG | HIGH |
| [stale-duplicate-automation-surviving-migration](clusters/stale-duplicate-automation-surviving-migration.md) | 9 | STRONG | HIGH |
| [schema-deploy-fail-closed-gating](clusters/schema-deploy-fail-closed-gating.md) | 8 | MODERATE | MEDIUM |
| [safe-manual-intervention-during-soak](clusters/safe-manual-intervention-during-soak.md) | 15 | MODERATE | MEDIUM |
| [lifecycle-state-model-blocked-is-prose-not-code](clusters/lifecycle-state-model-blocked-is-prose-not-code.md) | 4 | MODERATE | MEDIUM |
| [retry-restart-authority-and-idempotency](clusters/retry-restart-authority-and-idempotency.md) | 10 | MODERATE | MEDIUM |

Note topic 10 (retry/restart authority) split into three distinct
clusters during synthesis — the PID-namespace locking bug, destructive-mutation
authority, and retry/idempotency policy are related but analytically
separate concerns with different evidence shapes; see each cluster's own
"Unresolved questions" for whether Pass 0B should merge any of them.

Each cluster file follows a fixed structure (concern, current
terminology, repos surveyed, independent evidence, inherited evidence,
incidents, implementations, counterexamples, harm if violated, likely
domain, unresolved questions) — enforced by
[tests/test_operations_pass0_evidence.py](../../../tests/test_operations_pass0_evidence.py).

## Relationship to existing Fleet Laws (important for Pass 0B)

Unlike the Data/Ontology domain — where the closest prior art
(`clank-architecture`'s ADR-0006/0014) was PROPOSED, not adopted — several
of the strongest clusters here (health-vs-scheduler-state,
dual-gate-promotion-authority-drift, remote-host-deployment-truth,
stale-duplicate-automation) already have **ACTIVE, not proposed**,
fleet-wide governance in `clank-architecture/FLEET_LAWS.md` (Laws 3, 5,
7, 8, and Deferred Law 9), already CI-enforced in multiple fleet repos
via a shared `conformance` test suite pulled into their own GitHub
Actions. Two dated 2026-08-22/23 incidents (the fleet-wide git-stash
scheduler outage; two agent-performed destructive-volume-deletion
incidents) already produced `clank-architecture` ADR-0008, ADR-0009, and
ADR-0011 — governance written directly in response to incidents this
survey independently rediscovered from the fleet-member side.

**This is a genuine adjudication question for Pass 0B**, not something
this evidence-only pass resolves: for each such cluster, should a
Standards Clank Operations standard (1) restate/ratify the existing Fleet
Law under Standards Clank's own governance process, (2) explicitly defer
to `clank-architecture` and standardize only the gap it leaves open, or
(3) decline to create a competing standard at all where
`clank-architecture` already owns the concern? The UI and Data/Ontology
domains never faced this exact question because no prior ACTIVE governance
existed for their concerns.

## What this pass explicitly did not do

- Did not write any `STD-OPERATIONS-*` file or acceptance criteria.
- Did not ratify, retire, or alter any existing standard.
- Did not modify any target Clank, `clank-architecture`, or
  `diagnostic-clank` (the `diagnostic-clank` clone used for this survey
  is a read-only, local-scratch checkout, not committed to this
  repository).
- Did not touch either frozen baseline (`ui-standards-v1.0`,
  `data-ontology-standards-v1.0`).
- Did not begin adjudicating which candidate clusters are correct — that
  is explicitly Pass 0B's job, not this pass's.
- Did not decide the Fleet-Laws reconciliation question above — flagged
  for Pass 0B, not resolved here.
