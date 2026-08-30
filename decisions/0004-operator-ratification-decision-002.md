# 0004 — Operator Ratification Decision 002 (GUI Ratification Pass 2)

Date: 2026-08-30
Status: Accepted
Frozen candidate set reviewed: commit `5113049` (GUI Ratification Pass 2)

## Review

The operator reviewed all 6 Pass 2 candidates from
[../docs/gui-ratification-pass-2.md](../docs/gui-ratification-pass-2.md),
resolving both open questions raised in that document and providing
specific wording constraints before any status flip. This review — the
operator's rule-by-rule response delivered in conversation on 2026-08-30 —
is the review artefact required by
[../docs/governance.md](../docs/governance.md) before ratification.

## Decision

```
RATIFY
STD-UI-COM-008  (revised: semantic separation required, not separate pages, v2)
STD-UI-COM-009  (revised: unlinked drill-down does not satisfy 'observable', v2)
STD-UI-COM-010  (revised: page-level timezone convention satisfies the requirement, v2)
STD-UI-COM-011  (revised: no dedicated Delivery page required, v2)
STD-UI-NEWS-002 (revised: softened from 'default view' to a reachable-with-one-action requirement, v2)

RETURN FOR REVISION
STD-UI-COM-012  (rewritten as "primary workflow must not imply unobserved health", v2, still PROPOSED)

NO RULE CREATED
STD-UI-SKU-002
```

### Open-question resolutions

- **STD-UI-COM-009**: an unlinked drill-down does NOT count as adequately
  observable. The primary run surface does not need to render every stage
  inline, but it must visibly expose that deeper stage information exists
  and provide a direct path to it. A hidden/unlinked diagnostic page is
  technically present but operationally absent. Under this reading,
  watch-clank's current implementation (stage data only reachable via
  `/watches/{id}` and `/correlation/{id}`, not linked from the primary
  Runs page) does not conform — recorded as a live remediation-relevant
  example in the standard's own notes, not an exception.
- **STD-UI-COM-010**: ratified despite the 8/9 remediation footprint. Per
  the operator: "that footprint is evidence of technical debt, not
  evidence against the principle." Leaving it unratified would
  institutionalise ambiguity around `first seen`, `published`, `observed`,
  `run started`, and similar timestamps.

### Wording constraints applied before ratification

- **STD-UI-COM-008**: requires semantic separation, not separate pages.
  One screen/table may show both health and coverage if they are clearly
  distinct dimensions. chinese-tech-wire's and korean-tech-wire's
  coexistence of both on one Health page is not itself non-conformant;
  conflating them into one blended metric is (korean-tech-wire's
  same-row `latest_accepted` and smartphone-clank's combined `/metrics`
  score remain the flagged non-conforming examples).
- **STD-UI-COM-009**: materially distinct tracked stages must be
  operator-reachable from the run surface. Inline stage columns, an
  expandable row, a linked detail drawer, or a linked run-detail page all
  conform. An unlinked hidden route does not.
- **STD-UI-COM-010**: does not demand timezone repetition in every table
  cell. A table/page may establish "All times IST" or "All times UTC" at
  the surface level, provided the semantic role of each timestamp remains
  clear. The invariant is unambiguous time semantics, not visual clutter.
- **STD-UI-COM-011**: requires independent inspectability, not necessarily
  a dedicated Delivery page. A tab, drawer, outbox panel, event-detail
  section, or dedicated route can all conform, as long as an operator can
  distinguish event/discovery state from delivery state.
- **STD-UI-NEWS-002**: softened from a literal "MUST be the default
  landing view" to: for a news-family Clank whose primary operator task is
  live editorial triage, the default operational landing surface MUST
  expose the live intake/review queue directly, or reach it with one
  obvious action. This protects chinese-tech-wire's, korean-tech-wire's,
  and semiconductor-intelligence's actual behavior without permanently
  forcing a literal homepage-is-the-queue design.

### STD-UI-COM-012

Not ratified. The v1 counter-evidence (chinese-tech-wire, semiconductor-
intelligence, and smartphone-clank all keep health off their landing
surface) is architectural, not accidental, so a blanket "Overview must
show health" MUST was the wrong level. Rewritten to target the actual
risk — a primary surface implying health it hasn't measured, purely from
content activity — while leaving deliberate separation-of-concerns designs
intact provided the health page stays reachable. Left `PROPOSED`: per the
operator, this is a more nuanced rule than the original and needs its own
targeted evidence check against the three deliberate opt-outs (do their
landing surfaces actually imply health via content activity, or do they
stay neutral?) before it can move to REVIEWED.

### STD-UI-SKU-002

No rule was created — Pass 2 reported this as INSUFFICIENT evidence and
declined to draft it (see
[../docs/gui-ratification-pass-2.md](../docs/gui-ratification-pass-2.md#explicitly-not-proposed-std-ui-sku-002)).
Per the operator: "the absence of STD-UI-SKU-002 is a good outcome.
Standards Clank should gain credibility by refusing weak rules, not by
filling namespace slots." This decision record makes no change to that —
there is nothing to ratify or revise.

## Scope of this decision

Same as [0003](0003-operator-ratification-decision-001.md): this decision
ratifies wording. **It does not authorize remediation work on any Clank.**
Every remediation-relevant example named above (watch-clank's Runs page,
the 8/9 timezone gap, korean-tech-wire's and smartphone-clank's
health/coverage conflation) is a documented finding, not a work order.

## What comes after this decision

```
Pass 2 frozen candidate set
        v
Operator Ratification Decision 002  (this record)
        v
new RATIFIED versions of five rules
        v
revised PROPOSED version of COM-012
        v
integrity + tests
        v
freeze
        v
STOP
```

No further GUI Ratification Pass was commissioned by this decision.
