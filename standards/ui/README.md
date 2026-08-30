# ui

**Building or auditing a Clank UI?** Start with
[docs/ui/constitution.md](../../docs/ui/constitution.md) (the compact,
agent-facing summary of every RATIFIED rule below) and
[docs/ui/agent-implementation-workflow.md](../../docs/ui/agent-implementation-workflow.md)
(the required sequence for using it), not this directory's raw JSON files
one at a time. [`ratified-index.json`](ratified-index.json) and
[`agent-checklist.json`](agent-checklist.json) are generated from the
files below by `tools/ui_agent_layer.py` — see
`scripts/generate_ui_agent_layer.py` to regenerate them after any RATIFIED
standard changes.

12 `RATIFIED`, 3 `PROPOSED` (2 revised Pass 1 candidates, 1 revised Pass 2
candidate — all awaiting re-review), as of Operator Ratification Decision
002 (2026-08-30). See
[../../docs/gui-ratification-pass-1.md](../../docs/gui-ratification-pass-1.md),
[../../docs/gui-ratification-pass-2.md](../../docs/gui-ratification-pass-2.md),
[../../decisions/0003-operator-ratification-decision-001.md](../../decisions/0003-operator-ratification-decision-001.md),
and
[../../decisions/0004-operator-ratification-decision-002.md](../../decisions/0004-operator-ratification-decision-002.md).

## Pass 1 (operator/action/QC semantics)

| id | title | family | status |
|---|---|---|---|
| [STD-UI-COM-001](STD-UI-COM-001.json) | GUI must never auto-trigger collection on load/launch | Both | RATIFIED |
| [STD-UI-COM-002](STD-UI-COM-002.json) | QC decisions atomic, provenance-bearing, race-guarded, truthfully presented | Both | RATIFIED (v2) |
| [STD-UI-COM-003](STD-UI-COM-003.json) | Resolved item leaves active queue immediately (logical removal) | Both | RATIFIED |
| [STD-UI-COM-004](STD-UI-COM-004.json) | Resolved/QC-history surface required where a QC queue exists | Both | RATIFIED |
| [STD-UI-COM-005](STD-UI-COM-005.json) | Promotion is explicit config change | Both (conditional) | RATIFIED |
| [STD-UI-COM-006](STD-UI-COM-006.json) | Bulk "run all" excludes non-production collectors | Both (conditional) | RATIFIED |
| [STD-UI-COM-007](STD-UI-COM-007.json) | Manual controls must respect and expose collector authority policy | Both | PROPOSED (v2, revised) |
| [STD-UI-SKU-001](STD-UI-SKU-001.json) | SKU QC model must preserve a distinct availability-negative disposition | SKU | PROPOSED (v2, revised) |
| [STD-UI-NEWS-001](STD-UI-NEWS-001.json) | 4th QC action = DUPLICATE | News | RATIFIED |

## Pass 2 (information architecture and observability)

| id | title | family | status |
|---|---|---|---|
| [STD-UI-COM-008](STD-UI-COM-008.json) | Health independently expressible from coverage (semantic, not page, separation) | Both | RATIFIED (v2) |
| [STD-UI-COM-009](STD-UI-COM-009.json) | Tracked pipeline stages must be discoverable, not just technically present | Both | RATIFIED (v2) |
| [STD-UI-COM-010](STD-UI-COM-010.json) | Timestamp semantic role + timezone must both be unambiguous | Both | RATIFIED (v2) |
| [STD-UI-COM-011](STD-UI-COM-011.json) | Delivery state independently inspectable from discovery/review | Both | RATIFIED (v2) |
| [STD-UI-COM-012](STD-UI-COM-012.json) | Primary workflow must not imply unobserved health | Both | PROPOSED (v2, revised) |
| [STD-UI-NEWS-002](STD-UI-NEWS-002.json) | Live intake queue reachable directly or with one obvious action | News | RATIFIED (v2) |

`STD-UI-SKU-002` (a proposed SKU-family counterpart to NEWS-002) was
considered and explicitly not drafted — see
[../../docs/gui-ratification-pass-2.md](../../docs/gui-ratification-pass-2.md#explicitly-not-proposed-std-ui-sku-002)
for why the evidence didn't support it. No rule was ever created for it,
so there is nothing to ratify or revise.
