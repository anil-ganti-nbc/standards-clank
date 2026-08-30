# ui

7 `RATIFIED` (Pass 1 + Operator Ratification Decision 001), 8 `PROPOSED`
(2 revised Pass 1 candidates awaiting re-review, 6 new Pass 2 candidates
awaiting first review). See
[../../docs/gui-ratification-pass-1.md](../../docs/gui-ratification-pass-1.md),
[../../docs/gui-ratification-pass-2.md](../../docs/gui-ratification-pass-2.md),
and
[../../decisions/0003-operator-ratification-decision-001.md](../../decisions/0003-operator-ratification-decision-001.md).

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
| [STD-UI-COM-008](STD-UI-COM-008.json) | Health independently expressible from coverage | Both | PROPOSED |
| [STD-UI-COM-009](STD-UI-COM-009.json) | Don't collapse pipeline stages the backend already tracks | Both | PROPOSED |
| [STD-UI-COM-010](STD-UI-COM-010.json) | Timestamp semantic role + timezone must both be explicit | Both | PROPOSED |
| [STD-UI-COM-011](STD-UI-COM-011.json) | Delivery state inspectable independently from discovery/review | Both | PROPOSED |
| [STD-UI-COM-012](STD-UI-COM-012.json) | Overview must not omit a visible health signal | Both | PROPOSED |
| [STD-UI-NEWS-002](STD-UI-NEWS-002.json) | Live editorial intake surface must be the default landing view | News | PROPOSED |

`STD-UI-SKU-002` (a proposed SKU-family counterpart to NEWS-002) was
considered and explicitly not drafted — see
[../../docs/gui-ratification-pass-2.md](../../docs/gui-ratification-pass-2.md#explicitly-not-proposed-std-ui-sku-002)
for why the evidence didn't support it.
