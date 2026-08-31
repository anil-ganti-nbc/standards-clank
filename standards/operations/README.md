# operations

Standards about whether a Clank's own claims about its operational state
— did it run, is it healthy, is its promotion evidence real, is the
exclusivity marker coordinating its writers actually sound — hold up
against what actually happened, as distinct from what a scheduler,
config file, dashboard, or a reused identifier says happened. Groups four
standards drafted from one evidence-mining and adjudication program
(Pass 0A evidence inventory, Pass 0B adversarial adjudication) because
they share lineage back to the same 15-topic survey of nine fleet Clanks
plus `clank-architecture` and `diagnostic-clank`. The fourth
(STD-OPS-COM-004) was adjudicated alongside the first three at Pass 0B
but drafted later, in a separately-commissioned Pass 2.5 task, after a
Pass 1.5 scope-omission resolution and a Pass 2 adversarial review of the
other three surfaced and closed the gap — see
[docs/operations/pass1/README.md](../../docs/operations/pass1/README.md)'s
"A note on scope" section for the full history.

**4 `RATIFIED`, 0 `PROPOSED`, as of the 2026-08-31 ratification closure.**
**FROZEN as `operations-standards-v1.0`** (tag at commit `7100f29`), after
a hold-resolution / final-gap pass concluded **NO ESSENTIAL OPERATIONS
CONTRACT MISSING**. Building or auditing Operations behavior in a Clank?
Start with
[docs/operations/constitution.md](../../docs/operations/constitution.md)
(the compact, agent-facing summary of all four RATIFIED rules, with
inline citations) rather than these raw JSON files one at a time.
[ratified-index.json](ratified-index.json) and
[agent-checklist.json](agent-checklist.json) are generated from the files
below by `tools/operations_agent_layer.py` — see
`scripts/generate_operations_agent_layer.py` to regenerate them after any
change.

| id | title | version | status | decision |
|---|---|---|---|---|
| [STD-OPS-COM-001](STD-OPS-COM-001.json) | Execution invocation and outcome must be independently recorded, never inferred from scheduler-claimed state | v1 | RATIFIED | [0014](../../decisions/0014-ops-com-001-decision.md) |
| [STD-OPS-COM-002](STD-OPS-COM-002.json) | Scheduler/trigger-liveness health and outcome/yield health must remain independently representable | v1 | RATIFIED | [0015](../../decisions/0015-ops-com-002-decision.md) |
| [STD-OPS-COM-003](STD-OPS-COM-003.json) | Promotion/soak qualification evidence must be structurally verifiable, reset-traceable, and gate-drift-detectable | v1 | RATIFIED | [0016](../../decisions/0016-ops-com-003-decision.md) |
| [STD-OPS-COM-004](STD-OPS-COM-004.json) | Exclusivity/ownership markers must be validated by structurally observable proof | v1 | RATIFIED | [0017](../../decisions/0017-ops-com-004-decision.md) |

Full evidence, adjudication, and drafting trail:
[docs/operations/pass0/](../../docs/operations/pass0/) (evidence +
adjudication), [docs/operations/pass1/](../../docs/operations/pass1/)
(OPS-A/B/C dossiers + the OPS-D scope-omission resolution),
[docs/operations/pass2/](../../docs/operations/pass2/) (adversarial
review of all three drafted standards plus the undrafted OPS-D
candidate), [docs/operations/pass2.5/](../../docs/operations/pass2.5/)
(the OPS-D drafting dossier). Of the 15 Pass 0A clusters, Pass 0B
advanced these four merged candidates (three drafted at Pass 1, one at
Pass 2.5), **deferred** destructive production-action authority to
`clank-architecture` ADR-0009, **rehomed** deployment-truth/config-drift
and delivery-retry/idempotency concerns to future domains not yet
started, and **held** the lifecycle-state/blocked-is-prose concern
standalone — none of those were drafted here; see
[docs/operations/pass0/candidates/holds-rehomes-defers.md](../../docs/operations/pass0/candidates/holds-rehomes-defers.md).

Each standard is a **narrow complement** to existing, already-ACTIVE
`clank-architecture` governance (Fleet Laws 3, 5, 7, 8) or an explicit
reference to a still-PROPOSED ADR (0006, 0008, 0011) — none restates or
claims to replace that governance; see each standard's own `notes` field
for its specific reconciliation. `clank-architecture` was surveyed for
evidence only and was not modified by this drafting pass.
