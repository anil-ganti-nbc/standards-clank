# Data/Ontology Pass 0A — Evidence Inventory

**Status: evidence only. Nothing in this directory is a standard, a draft
standard, ratification, or remediation.** No `STD-DATA-*` file exists
anywhere in this repository, and none should be created from this
directory without a separate, explicit ratification pass — see
[docs/governance.md](../../governance.md).

## What this is

A structured inventory of how the Clank fleet represents *what
information means and how truth is represented* — first-seen vs. novelty,
unknown vs. false, entity identity, observation vs. canonical fact,
evidence/provenance, baselining, and availability/lifecycle facts — mined
read-only from nine fleet Clanks, `clank-architecture`, and
`diagnostic-clank` at their current GitHub HEADs (2026-08-31/09-01; see
each survey's HEAD citations preserved in [evidence-log.md](evidence-log.md)).

This inventory does **not** decide which patterns should become standards.
It exists so a separate adjudication pass (Pass 0B, not started here) has
a structured, cited corpus to work from instead of re-surveying the fleet.

## Built on top of

The UI standards baseline, frozen at tag `ui-standards-v1.0`
(commit `d113207`). This pass did not read that freeze as a constraint on
scope — data/ontology is a distinct domain from UI — but it also did not
touch `standards/ui/`, `docs/ui/`, or any UI-domain decision/audit file.
See [../../../decisions/](../../../decisions/) for the UI ratification
history if useful context.

## Method

Six parallel read-only survey agents (five covering the nine fleet Clanks
in pairs, one mining `diagnostic-clank` specifically for cross-fleet
incidents), each instructed to cite file:line for every claim, classify
lineage (independent / inherited-copied / lineage-uncertain), and
prioritize incident evidence. `clank-architecture` was surveyed for
evidence only, read-only, not modified. Full per-repo survey output is
preserved in [evidence-log.md](evidence-log.md) — the cluster files below
are a synthesis of it, not a replacement; where a cluster file's citation
looks incomplete, the evidence log has the fuller original text.

## Contents

- [evidence-log.md](evidence-log.md) — the six raw survey reports, preserved verbatim for traceability
- [incident-ledger.md](incident-ledger.md) — every incident found, one row per incident, with repo/date/harm/root-cause/remediation/recurrence-risk
- [terminology-map.md](terminology-map.md) — cross-fleet table of what each temporal/identity/state term actually means per repo
- [clusters/](clusters/) — 13 candidate-cluster files, each a structured writeup of one concern (see below)
- [handoff.md](handoff.md) — the compact adjudication package for the next (ZLM) pass — HIGH-priority clusters only

## Candidate clusters

| Cluster | Confidence | Priority |
|---|---|---|
| [baseline-epoch-continuity.md](clusters/baseline-epoch-continuity.md) | STRONG | HIGH |
| [novelty-vs-discovery-time.md](clusters/novelty-vs-discovery-time.md) | STRONG | HIGH |
| [entity-identity-coarse-key-merge.md](clusters/entity-identity-coarse-key-merge.md) | STRONG | HIGH |
| [availability-lifecycle-data-model.md](clusters/availability-lifecycle-data-model.md) | STRONG | HIGH |
| [evidence-provenance-granularity.md](clusters/evidence-provenance-granularity.md) | STRONG | HIGH |
| [timestamp-shaped-values.md](clusters/timestamp-shaped-values.md) | MODERATE | HIGH |
| [cross-clank-fleet-identity.md](clusters/cross-clank-fleet-identity.md) | MODERATE | HIGH |
| [unknown-absent-vs-false.md](clusters/unknown-absent-vs-false.md) | STRONG | MEDIUM |
| [canonical-fact-overwrite-discipline.md](clusters/canonical-fact-overwrite-discipline.md) | STRONG | MEDIUM |
| [confidence-and-certainty-semantics.md](clusters/confidence-and-certainty-semantics.md) | MODERATE | MEDIUM |
| [editorial-freshness-vs-novelty.md](clusters/editorial-freshness-vs-novelty.md) | MODERATE | MEDIUM |
| [regional-variant-identity.md](clusters/regional-variant-identity.md) | MODERATE | MEDIUM |
| [source-disagreement-representation.md](clusters/source-disagreement-representation.md) | WEAK | LOW |

Each cluster file follows a fixed structure (concern name, current
terminology, repos surveyed, independent evidence, inherited evidence,
incidents, implementations, counterexamples, harm if violated, likely
domain, unresolved questions, confidence, adjudication priority) —
enforced by [tests/test_pass0_evidence.py](../../../tests/test_pass0_evidence.py).

## What this pass explicitly did not do

- Did not write any `STD-DATA-*` file or acceptance criteria.
- Did not ratify, retire, or alter any existing standard.
- Did not modify any target Clank, `clank-architecture`, or
  `diagnostic-clank`.
- Did not touch the frozen UI baseline.
- Did not begin adjudicating which candidate clusters are correct — that
  is explicitly Pass 0B's job, not this pass's.
