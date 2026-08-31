# operations

Standards about whether a Clank's own claims about its operational state
— did it run, is it healthy, is its promotion evidence real — hold up
against what actually happened, as distinct from what a scheduler,
config file, or dashboard says happened. Groups three standards drafted
together from one evidence-mining and adjudication program (Pass 0A
evidence inventory, Pass 0B adversarial adjudication) because they share
lineage back to the same 15-topic survey of nine fleet Clanks plus
`clank-architecture` and `diagnostic-clank`.

**3 `PROPOSED`, 0 `RATIFIED`, as of the 2026-08-31 Pass 1 drafting pass.**
Not frozen, not reviewed, not ratified. Nothing here should be treated as
binding on any Clank yet.

| id | title | version | status |
|---|---|---|---|
| [STD-OPS-COM-001](STD-OPS-COM-001.json) | Execution invocation and outcome must be independently recorded, never inferred from scheduler-claimed state | v1 | PROPOSED |
| [STD-OPS-COM-002](STD-OPS-COM-002.json) | Scheduler/trigger-liveness health and outcome/yield health must remain independently representable | v1 | PROPOSED |
| [STD-OPS-COM-003](STD-OPS-COM-003.json) | Promotion/soak qualification evidence must be structurally verifiable, reset-traceable, and gate-drift-detectable | v1 | PROPOSED |

Full evidence, adjudication, and drafting trail:
[docs/operations/pass0/](../../docs/operations/pass0/) (evidence +
adjudication), [docs/operations/pass1/](../../docs/operations/pass1/)
(this drafting pass's dossiers). Of the 15 Pass 0A clusters, Pass 0B
advanced these three merged candidates, **deferred** destructive
production-action authority to `clank-architecture` ADR-0009, **rehomed**
deployment-truth/config-drift and delivery-retry/idempotency concerns to
future domains not yet started, and **held** the lifecycle-state/blocked-is-prose
concern standalone — none of those were drafted here; see
[docs/operations/pass0/candidates/holds-rehomes-defers.md](../../docs/operations/pass0/candidates/holds-rehomes-defers.md).

Each standard is a **narrow complement** to existing, already-ACTIVE
`clank-architecture` governance (Fleet Laws 3, 5, 8) or an explicit
reference to a still-PROPOSED ADR (0006, 0008, 0011) — none restates or
claims to replace that governance; see each standard's own `notes` field
for its specific reconciliation. `clank-architecture` was surveyed for
evidence only and was not modified by this drafting pass.
