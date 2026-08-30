# 0003 — Operator Ratification Decision 001 (GUI Ratification Pass 1)

Date: 2026-08-30
Status: Accepted
Frozen candidate set reviewed: commit `07d87b0` (GUI Ratification Pass 1)

## Review

The operator reviewed all 9 `PROPOSED` candidates from
[../docs/gui-ratification-pass-1.md](../docs/gui-ratification-pass-1.md)
rule by rule, evaluating evidence quality, the "evidence is not precedent"
framing, and whether each rule's wording protected the right invariant.
This review — the operator's rule-by-rule critique delivered in
conversation on 2026-08-30 — is the review artefact required by
[../docs/governance.md](../docs/governance.md) before ratification.

## Decision

```
RATIFY
STD-UI-COM-001
STD-UI-COM-002  (revised: added UI-truthfulness clause, version 2)
STD-UI-COM-003  (editorial: acceptance reworded for logical vs. DOM removal)
STD-UI-COM-004  (editorial: "Recently QC'd" clarified as canonical language, not a mandated route)
STD-UI-COM-005
STD-UI-COM-006
STD-UI-NEWS-001

RETURN FOR REVISION
STD-UI-COM-007  (rewritten as a policy-visibility invariant, version 2, still PROPOSED)
STD-UI-SKU-001  (rewritten as an ontology invariant, version 2, still PROPOSED)
```

No rule from the Pass 1 candidate set was rejected.

### Rationale highlights, per the operator

- **STD-UI-COM-001**: an operational safety invariant, not a layout
  preference; the smartphone-clank daemon counter-example is correctly out
  of scope because it is not GUI-triggered.
- **STD-UI-COM-002**: especially strong because two independent
  implementation families (watch-clank's table-based archive,
  chinese-tech-wire's file-based archive) converged on the same contract.
  Ratified with an added clause: UI conformance may depend on backend
  semantics where those semantics are necessary to make the operator
  interaction truthful — a confirmation toast is not itself conformance,
  the write it represents must be. This guards against a future reader
  interpreting the standard as "show a checkmark."
- **STD-UI-COM-003**: acceptance criteria should speak to logical/query-time
  removal, not any particular frontend rendering technology or animation
  timing.
- **STD-UI-COM-004**: applies only where a Clank exposes operator QC at
  all; "Recently QC'd" is the fleet's canonical UI language for this
  surface, not a route name every Clank must literally implement.
- **STD-UI-COM-005 / STD-UI-COM-006**: good cross-family evidence, ratified
  unchanged. oem-radar's runtime-cost (heavy-collector) filtering is a
  separate dimension from production/experimental maturity gating and is
  not counter-evidence to COM-006 — the operative semantic is that "Run
  All" must have an explicit, visible eligibility set.
- **STD-UI-NEWS-001**: the best-evidenced rule in the pass — two
  independent origins (chinese-tech-wire's LeadOutcome, watch-clank's own
  SpecialistLeadReview) converged on `DUPLICATE` before any cross-copying
  occurred. chinese-tech-wire's extra `WRITTEN` value does not conflict.
- **STD-UI-COM-007**: the fleet split (smartwatch-clank prohibits
  individually running an experimental collector; watch-clank,
  korean-tech-wire, tablet-clank, and feature-phone-clank allow it) meant
  the rule was framed at the wrong level — an implementation disagreement,
  not a settled invariant. Rewritten as a policy-visibility requirement
  (non-production collectors must be visibly identified at the point of
  their control and excluded from bulk actions; whether manual execution
  is permitted at all is left to each Clank's own authority policy) that
  accommodates every observed posture without declaring any of them wrong.
- **STD-UI-SKU-001**: the load-bearing invariant is ontological (an
  availability-negative disposition must exist, distinct from
  false-positive/duplicate/not-useful), not that a literal `OUT_OF_STOCK`
  enum value must exist. Rewritten so oem-radar's
  `AVAILABILITY_CHANGED` + reason-code encoding conforms naturally instead
  of being treated as a partial miss of a literal-string requirement.

### Smartphone-clank

No exception was filed. Per the operator's explicit instruction, the
current `qc-action` implementation is a remediation-backlog target against
`STD-UI-COM-002`, `STD-UI-COM-003`, and `STD-UI-COM-004` (once applicability
is confirmed against its actual workflow) — not a case where compliance is
inappropriate. Exceptions are reserved for cases where conformance is
genuinely wrong for a Clank, not simply for a Clank predating the standard.
See [../audits/smartphone-clank-2026-08-30.md](../audits/smartphone-clank-2026-08-30.md).

## Scope of this decision

This decision ratifies wording. **It does not authorize remediation work
on any Clank.** Turning a ratified rule into implementation guidance, and
retrofitting existing GUIs against it, is separate future work the
operator has not yet commissioned.

## What comes after this decision

```
Pass 1 frozen candidate set
        v
Operator Ratification Decision 001  (this record)
        v
new RATIFIED versions of seven rules
        v
revised PROPOSED versions of COM-007 and SKU-001
        v
integrity + tests
        v
freeze
        v
STOP
```

A future GUI Ratification Pass 2 was discussed as covering navigation
contracts, source-health vs. coverage, run-stage representation,
timestamps, evidence inspectors, delivery state, status vocabulary, and
Overview-page composition — but it is not commissioned by this decision and
has not been started.
