# Operations Pass 3 — Ratification Survey (2026-08-31)

Evaluates the four PROPOSED `STD-OPS-*` standards (at `5aadec0`, the
Pass 2.5 OPS-D drafting commit) for operator ratification, from the
stored Pass 0A evidence, Pass 0B adjudication, Pass 1/2.5 dossiers, and
Pass 2 adversarial review. **No fleet recrawl was performed** — every
question resolved from persisted evidence; no target repo or
`clank-architecture` was inspected.

## Standards under survey

| Standard | Title | Version | Pass 2 verdict |
|---|---|---|---|
| STD-OPS-COM-001 | Execution materialization truth | v1 | APPROVE FOR RATIFICATION SURVEY |
| STD-OPS-COM-002 | Health-honesty two-axis complement | v1 | APPROVE FOR RATIFICATION SURVEY |
| STD-OPS-COM-003 | Promotion/soak evidence integrity | v1 | APPROVE FOR RATIFICATION SURVEY |
| STD-OPS-COM-004 | Exclusivity-marker soundness | v1 | DRAFT AS STD-OPS-COM-004 (drafted at Pass 2.5, not itself re-reviewed by a Pass 2 pass) |

## Evidence sufficiency

| Standard | Evidence | Independent lineages | Incident support | Counterimplementation |
|---|---|---|---|---|
| COM-001 | STRONG | 5 independent mechanisms (watch, oem-radar, chinese-tech-wire, korean-tech-wire, semiconductor-intelligence); ADR-0008 derived *after* the incidents, not a lineage input | YES — INC-027 (3 Clanks, ~36h), INC-002, INC-021, INC-012 | INC-028 (false-positive materialization-gap inference) — excluded by requiring no-work outcomes be positively recorded, not a counterexample to the standard itself |
| COM-002 | STRONG | 9 differently-named independent implementations (7/9 fleet Clanks); ctw/ktw found-vs-new pair independently convergent, zero shared code | YES — INC-006, INC-022, INC-043/ADR-0007 | tablet-clank's accepted scope gap (no disappearance detection) — trigger-unmet, not counter-evidence; smartphone's unfixed health_score() gap — cited as corpus evidence for the standard's existence, not a conformance finding |
| COM-003 | STRONG jointly (facet 1 — trigger provenance — MODERATE alone, carried honestly from the candidate card and Pass 1 dossier) | soak-reset convergence independent across 4 repos; trigger-provenance mechanisms independent wherever present; feature-phone's single-gate design is explicit incident inheritance from smartphone's INC-013, counted once | YES — INC-013 (severe, averted 18 false alerts); Fleet Law 8's 3 named historical violators; INC-032 (intervention handled correctly) | "no soak lifecycle" Clank — trigger-unmet; "manual diagnostics forbidden" — misreading, acceptance criteria require distinguishable-not-forbidden |
| COM-004 | STRONG — four independent-environment incident discoveries across four repos, three failure directions | 3 independent incident environments (oem-radar/NAS, watch-clank/Windows, smartwatch-clank/one-shot-container) + smartphone's stale-PID-file instance in the same family; the OS-advisory-lock *fix* lineage counted once (ported code, not independent votes), per Pass 2's own evidence-discipline note | YES — INC-009 (~81 refused fires), INC-006 (wrong-process kill), smartwatch-clank's proven-broken reclaim, INC-015 (duplicate daemon) | "DB advisory locks/leases look nothing like flock" — survives: invariant binds validity-proof semantics, not mechanism; tested explicitly at the candidate-card, Pass 1.5, and Pass 2 stages |

Lineage caution applied throughout, consistent with the Data/Ontology
domain's precedent: a fix propagated by explicit code-porting (the
OS-advisory-lock remedy behind COM-004, and the run-lock ports generally)
is counted once, never as one vote per repo that copied it; independent
*incident discovery* is what counts as independent evidence, and is
counted per-incident regardless of whether the eventual fix was shared.

## Counterexample outcomes

All four invariants survive their strongest counterexamples as scoped,
each already tested at drafting time and reconfirmed here from the
stored record, not re-litigated:

- **COM-001**: "an externally-scheduled Clank has no invocation record of
  its own" — survives; the requirement binds the Clank's own recorded
  evidence of what happened after a trigger fired, not who fired it.
- **COM-002**: "a Clank with no scheduler and no external sources" —
  trigger-unmet, survives by scope.
- **COM-003**: "no soak/promotion lifecycle" (trigger-unmet) and "manual
  diagnostic invocation would become forbidden" (misreading — the
  acceptance criteria require distinguishable-and-non-qualifying, never
  forbidden) — both survive.
- **COM-004**: "DB advisory locks / leases / fencing tokens look nothing
  like flock" — survives; the invariant binds validity-proof provenance,
  not mechanism shape. A PID+hostname+start-time tuple can even conform,
  provided the start-time genuinely proves identity.

## Overlap / domain assessment

- COM-001: DISTINCT from the frozen UI and Data/Ontology corpora
  (execution/scheduling truth, not data representation or operator
  display). COMPLEMENT to `clank-architecture` ADR-0008/0011 (both
  PROPOSED, not ACTIVE at drafting time); DEFER to Fleet Law 5 (ACTIVE)
  for single-scheduler authority.
- COM-002: NARROW COMPLEMENT to Fleet Law 3 (ACTIVE, CI-enforced) —
  ratifies only the axis-vocabulary/conflation-forbidden slice Law 3
  leaves open, does not restate the principle. DISTINCT from
  `STD-UI-COM-008`/`STD-UI-COM-012` (operator-facing display of
  health/coverage; this standard binds the underlying data/operations
  state model those displays must not misrepresent).
- COM-003: NARROW COMPLEMENT to Fleet Law 8 (ACTIVE) — promotion-gate
  authority stays Law 8's; this standard owns evidence-verifiability,
  reset-traceability, and drift-detectability. REFERENCES (does not
  restate) ADR-0006 (PROPOSED) for the incident-does-not-reset principle.
- COM-004: COMPLEMENT to Fleet Laws 7 and 5 (both ACTIVE) — neither
  addresses coordination-primitive validity semantics. DISTINCT from
  ADR-0009 (destructive production mutation authority — a related-in-spirit
  but differently-scoped concern; no overlap requiring reconciliation).
  DISTINCT from COM-001 — a Clank deadlocked on a stale-but-unsound lock
  can satisfy COM-001's materialization contract perfectly (every refused
  fire is a recorded skip outcome) while starving indefinitely, exactly
  as oem-radar's ~81 refused fires did; verified explicitly in this
  standard's own `notes` field.
- Domain fit: all four are OPERATIONS (execution/scheduling/coordination
  truth contracts, distinct from UI display semantics and Data/Ontology
  data-representation semantics). No rehome. Domain shape confirmed
  single `operations` domain (no split proposed at drafting or review).

## Fleet-Law/ADR governance note (unchanged from drafting)

Three of the four standards are explicit **narrow complements** to
governance that is already **ACTIVE** (Fleet Laws 3, 5, 7, 8) — a
materially different situation from the Data/Ontology domain, where the
closest prior art (ADR-0006/0014) was itself only PROPOSED. Ratifying
these standards as written does not activate, migrate, or restate any
Fleet Law or ADR; each standard's own `notes` field states this
boundary explicitly, and nothing in this survey proposes changing that.

## Recommendations (one per standard)

| Standard | Recommendation |
|---|---|
| STD-OPS-COM-001 | RATIFY AS WRITTEN |
| STD-OPS-COM-002 | RATIFY AS WRITTEN |
| STD-OPS-COM-003 | RATIFY AS WRITTEN |
| STD-OPS-COM-004 | RATIFY AS WRITTEN |

All four meet the full ratification bar: STRONG (COM-003 STRONG jointly)
evidence, implementation-neutral wording, correctly scoped triggers,
testable acceptance criteria, meaningful forbidden behavior, no
surviving legitimate counterexample, no unresolved domain-boundary
problem, no problematic duplication of existing ACTIVE governance or
other ratified/proposed standards.

## Unresolved operator questions

1. Per-standard ratification (decisions/0014-0017, all awaiting operator
   decision; all recommend Option A — ratify as written).
2. Pre-existing operator flags unrelated to ratification, unchanged from
   earlier Operations passes and carried forward for visibility:
   - `clank-architecture` ADR-0009 is still `PROPOSED — REVIEWED DRAFT`
     despite post-dating both severe destructive-mutation incidents
     (INC-041 total loss, INC-036 partial loss) — consider activating it
     out-of-band; both incidents were agent-performed, worth naming as an
     explicit risk class in ADR-0009 (Pass 0B's operator flag, unchanged).
   - smartphone-clank's `health_score()` gap (COM-002's corpus evidence)
     remains a live, unfixed exposure against an otherwise fleet-wide
     pattern — a conformance question, not something this ratification
     survey adjudicates.
   - Two fleet members (chinese-tech-wire, korean-tech-wire) were not
     confirmed at Pass 0A to have hit the PID-namespace locking defect
     COM-004 addresses — untested-but-exposed vs. safe-by-different-design
     remains genuinely unknown; a conformance-audit question, not a
     ratification blocker.
   - Cluster 14 (lifecycle-state-blocked-is-prose) remains HELD; clusters
     8/9/12 and 15 remain REHOMEd to not-yet-started future domains — none
     of this survey's recommendations reopen those dispositions.

## Decision records

- [decisions/0014-ops-com-001-decision.md](../../decisions/0014-ops-com-001-decision.md)
- [decisions/0015-ops-com-002-decision.md](../../decisions/0015-ops-com-002-decision.md)
- [decisions/0016-ops-com-003-decision.md](../../decisions/0016-ops-com-003-decision.md)
- [decisions/0017-ops-com-004-decision.md](../../decisions/0017-ops-com-004-decision.md)

## Post-survey ratification closure (2026-08-31)

All four OPS standards ratified by operator acceptance (decisions/0014-0017).
The QC GUI absence remains non-normative product backlog; COM-003/004
remain N/A per their ratified triggers.

## Post-ratification closure note (2026-08-31)

All four OPS standards ratified by operator acceptance (decisions/0014-0017).
The QC GUI absence remains non-normative product backlog; COM-003/004
remain N/A per their ratified triggers. The destructive-production-action
concern (#10) remains DEFERRED to clank-architecture ADR-0009 governance.
