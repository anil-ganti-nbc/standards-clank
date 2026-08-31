# Operations Pass 1 — Candidate Drafting

**Status: three PROPOSED standards drafted, none ratified, none reviewed.**
This pass drafted exactly the three candidates Pass 0B advanced with a
full candidate card (OPS-A, OPS-B, OPS-C) as `standards/operations/STD-OPS-COM-001/002/003.json`.
No other Pass 0A cluster or Pass 0B disposition was revived, reopened, or
promoted — HOLD, DEFER, and REHOME dispositions all stay exactly where
Pass 0B put them; see
[docs/operations/pass0/candidates/holds-rehomes-defers.md](../pass0/candidates/holds-rehomes-defers.md).

## A note on scope: three cards, not four dispositions

Pass 0B's adjudication table (`docs/operations/pass0/adjudication.md`)
marked **four** clusters `ADVANCE`, including cluster 2
(pid-namespace-unsafe-stale-lock-reclaim, candidate name "OPS-D Lock
reclaim soundness" in the table). Pass 0B's own test suite
(`tests/test_ops_pass0b_adjudication.py::ADVANCE_CARDS`) and its
`candidates/` directory, however, only produced full candidate cards
(evidence strength, counterexample test, Fleet-Law reconciliation, a
recommendation) for three candidates — OPS-A, OPS-B, OPS-C. No
`ops-d-*.md` card exists. This drafting pass's mission explicitly named
exactly three candidates to draft and explicitly forbade a fourth; that
instruction and what Pass 0B actually produced in card form agree with
each other, so no conflict arose in practice. Recorded here so a future
pass has the full picture: cluster 2 remains `ADVANCE`-adjudicated but
undrafted, with only a one-paragraph justification in the adjudication
prose and no candidate card — a real candidate for a future Operations
Pass 1 continuation, not something this pass silently dropped.

## Method

Loaded only the referenced Pass 0 package —
[docs/operations/pass0/adjudication.md](../pass0/adjudication.md), the
three `ops-a`/`ops-b`/`ops-c` candidate cards, the specific Pass 0A
cluster files each card cites, and the Fleet Law/ADR excerpts the
adjudication table names. No fleet recrawl was performed; every citation
in the three drafted standards' `evidence` arrays traces back to a
citation already present in the Pass 0A evidence log or the Pass 0B
candidate cards, not to any new inspection of a fleet repo.

## Contents

- [dossier-ops-a-execution-materialization-truth.md](dossier-ops-a-execution-materialization-truth.md)
- [dossier-ops-b-health-honesty-two-axis.md](dossier-ops-b-health-honesty-two-axis.md)
- [dossier-ops-c-promotion-soak-evidence-integrity.md](dossier-ops-c-promotion-soak-evidence-integrity.md)

## What this pass explicitly did not do

- Did not ratify anything — all three standards are `PROPOSED`, `version: 1`.
- Did not remediate any Clank.
- Did not recrawl the fleet.
- Did not migrate, activate, or restate any `clank-architecture` Fleet
  Law or ADR as Standards Clank's own authority — each standard's `notes`
  field states explicitly that Standards Clank defines the semantic
  invariant while existing ACTIVE Fleet Laws/ADRs remain separate
  authority unless a later governance decision migrates or supersedes
  them.
- Did not modify `clank-architecture` or any target Clank.
- Did not draft a standard for destructive production mutations (DEFER
  to ADR-0009), backup/recovery, deployment revision truth, remote host
  truth, schema deployment (all REHOME → future DEPLOYMENT domain),
  notification retry/idempotency (REHOME → future DELIVERY domain), or
  blocked/mothballed vocabulary (HOLD).
- Did not create a fourth Operations standard.
