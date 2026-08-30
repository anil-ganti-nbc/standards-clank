# GUI Ratification Pass 2 — information architecture and observability

Status: **evidence-gathering and drafting only. Nothing here is REVIEWED or
RATIFIED.** Same discipline as
[GUI Ratification Pass 1](gui-ratification-pass-1.md): five parallel
read-only survey agents, same repo pairings, file:line citations required
for every claim. Built on top of
[Operator Ratification Decision 001](../decisions/0003-operator-ratification-decision-001.md)
(commit `cf0b9a3`). `clank-architecture` was read for evidence only, again
not touched or consolidated.

## Scope

Six areas only, as the operator specified: navigation/page contracts,
Overview semantics, source health vs. coverage, run-stage observability,
timestamps/provenance/evidence, and delivery/Discord visibility. Visual
styling is explicitly out of scope again — every candidate rule below is
written to be satisfiable by a tab, a card, a drill-down page, or a single
combined view, never mandating a specific route or layout. See
"Ratify capabilities and semantic surfaces first, route names second" in
the operator's framing for this pass.

## The navigation-minimalism question, tested directly

The operator suspected several generated mockups over-standardise
navigation — that concepts like Source Health, Regional Matrix, Evidence,
Runs, and Health/Diagnostics might not all deserve independent top-level
tabs in every SKU Clank. This pass found direct, concrete evidence
supporting that suspicion, in both directions:

- **Confirmed mergeable in practice:** tablet-clank's "Latest Discoveries"
  and "Changes" pages run near-identical queries against the same tables
  with the same rendered columns — Discoveries is just Changes with a
  `limit=20` and no type filter. semiconductor-intelligence went further
  and actually did this: its "Evidence" section still exists in the DOM
  but has no nav button any more, replaced by a redirect stub reading
  "Evidence now lives beside its claims in Claims & Evidence" — a real,
  observable decision to de-duplicate two surfaces into one. oem-radar's
  top nav "Alerts" and "Evidence" are not separate pages at all — they are
  deep-links into one client-side tab set alongside five other views.
- **Confirmed genuinely load-bearing (not mergeable):** tablet-clank's
  Active Queue vs. Recently QCed (different underlying data: one filters
  against the QC archive, the other reads it directly) and Products vs.
  Changes (baseline-state table vs. event-log table) are backed by
  materially different queries and should stay distinct capabilities, even
  if not distinct pages.

No candidate rule below mandates a specific page/tab structure. Every
acceptance criterion is written so a single combined view, a filtered
single page, or separate dedicated pages can all conform equally — the
requirement is always about a capability being reachable, never about how
many clicks or which route name gets you there.

## Ratification table

| Rule | Level | Evidence | Counter-evidence / caveats | Recommendation |
|---|---|---|---|---|
| [STD-UI-COM-008](../standards/ui/STD-UI-COM-008.json) — health independently expressible from coverage | MUST | watch-clank's documented 2026-08-24 repair of a real conflation bug; independently corroborated by clank-architecture's GIC-02 golden incident | korean-tech-wire and smartphone-clank currently conflate them in production | **STRONG** |
| [STD-UI-COM-009](../standards/ui/STD-UI-COM-009.json) — don't collapse pipeline stages the backend already tracks | MUST | watch-clank has real stage data (PipelineLedger) that most of the fleet lacks entirely | Even watch-clank's own primary Runs page collapses it — reachable only via unlinked drill-down. Whether that satisfies the rule is left as an open question, not resolved here | **STRONG**, with an unresolved strictness question |
| [STD-UI-COM-010](../standards/ui/STD-UI-COM-010.json) — timestamp semantic role + timezone must both be explicit | MUST | Only watch-clank enforces this fleet-wide; well-motivated (its own SpecialistLead table still has a live ambiguous column where the rule isn't fully applied) | 8 of 9 Clanks fail timezone labeling to varying degrees — ratifying this creates a real, fleet-wide remediation backlog | **STRONG**, but flagged: largest remediation footprint of this pass |
| [STD-UI-COM-011](../standards/ui/STD-UI-COM-011.json) — delivery state inspectable independently from discovery/review | MUST | 3 independent, cross-family implementations (CTW, semiconductor-intelligence, smartphone-clank) | watch-clank and feature-phone-clank compute delivery outcomes and never surface them; oem-radar actively collapses distinct states into one misleading boolean | **STRONG** |
| [STD-UI-COM-012](../standards/ui/STD-UI-COM-012.json) — Overview must not omit a visible health signal | MUST | 6/9 Clanks do this | 3/9 (CTW, semiconductor-intelligence, smartphone-clank) appear to have chosen the opposite deliberately, as a separation-of-concerns design, not by oversight | **QUALIFIED** — weakest case in this pass |
| [STD-UI-NEWS-002](../standards/ui/STD-UI-NEWS-002.json) — live editorial intake surface must be the default landing view | MUST | 3/3 of the surveyed news-family Clanks, each independently the default view | none found | **STRONG** |

## Explicitly not proposed: STD-UI-SKU-002

The operator's own illustrative example — "a SKU-family Clank must provide
a primary unresolved/discovery review surface distinct from canonical
product history" — does not survive scrutiny against this pass's evidence
and is **not** being drafted as a candidate standard.

Only tablet-clank cleanly evidences both halves of this split (Active
Queue vs. Products, backed by genuinely different queries). smartphone-clank
actively contradicts the premise: it has a canonical current-state view
(`/devices`) but no discovery/review surface at all — consistent with its
already-known COM-002/003/004 gap, not new counter-evidence, but it means
the "SKU Clanks have both" premise is false for at least one member.
watch-clank, oem-radar, feature-phone-clank, and smartwatch-clank were not
clearly evidenced either way by this pass's six questions — none of them
directly asked "is there a separate canonical product catalog." Rather
than force a rule from a one-clean-example, one-contradiction, four-unclear
evidence base, this is reported back as **INSUFFICIENT** and deferred. A
future, narrowly-targeted follow-up asking specifically about canonical
product views vs. discovery queues across the SKU family would be needed
before drafting this.

## Open items for the operator

1. **STD-UI-COM-009's strictness question**: does stage detail reachable
   only via an unlinked drill-down page satisfy "observable," or must the
   primary Runs list itself surface it? watch-clank is a live test case
   either way.
2. **STD-UI-COM-010's remediation scope**: ratifying as-is means 8 of 9
   Clanks need at least a formatting-helper fix. The fix is cheap per
   Clank, but the count is large — worth ratifying with that consequence
   understood, not discovered later.
3. **STD-UI-COM-012's weaker evidence base**: 3 non-conforming Clanks
   appear to have made a deliberate design choice (lean landing page,
   health on its own page), not an oversight. Worth explicit confirmation
   that this pass's recommendation to ratify anyway (health belongs on the
   landing page even in a multi-page app) is the right call, rather than
   an assumption this pass is making unilaterally.
4. **STD-UI-SKU-002 deferred**, see above — needs a targeted follow-up,
   not force-fit now.

## What this pass did not do

No standard's status was set to REVIEWED or RATIFIED. No existing Clank
was modified. `clank-architecture` was read, not touched or consolidated.
No visual/layout decision was made — every acceptance criterion accepts
combined, tabbed, or separate-page presentation equally.
