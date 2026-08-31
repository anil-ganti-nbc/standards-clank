# Data/Ontology Pass 3 — Ratification Survey (2026-08-31)

Evaluates the four PROPOSED `STD-DATA-*` standards (at `d6f4e58`, the
Pass 2.5 revision commit) for operator ratification, from the stored
Pass 0A evidence, Pass 0B adjudication, Pass 1 dossiers, and Pass 2
adversarial review. **No fleet recrawl was performed** — every question
resolved from persisted evidence; no target repo was inspected.

## Standards under survey

| Standard | Title | Version | Pass 2 verdict | Pass 2.5 |
|---|---|---|---|---|
| STD-DATA-COM-001 | Continuity/epoch state must be explicit | v1 | APPROVE | n/a |
| STD-DATA-COM-002 | First-seen is not novelty; read-side exclusion | v2 | REVISE (resolved) | revision applied |
| STD-DATA-COM-003 | Identity conservatism | v2 | REVISE (resolved) | revision applied |
| STD-DATA-COM-004 | Provenance tier separation | v1 | APPROVE | n/a |

## Evidence sufficiency

| Standard | Evidence | Independent lineages | Incident support | Counterimplementation |
|---|---|---|---|---|
| COM-001 | STRONG | 3 independent (watch, oem-radar, feature-phone) + 1 inherited (smartwatch ← ADR-0006) | YES — TIMEX catalogue backfill burst | watch's empty production epoch table (adoption exposure, not falsification) |
| COM-002 | STRONG | 2 independent incident lineages (watch, oem-radar) + 1 inherited (feature-phone ← smartphone) + 2 independent doctrine restatements (diagnostic-clank, clank-architecture Fleet Law 2) | YES — EPOCH1_FRESHNESS; oem-radar baseline-flag-unread; smartphone pollution (inherited) | none |
| COM-003 | STRONG | 4 independent incidents, no cross-citation; 2 independent conforming mechanisms (oem-radar cascade; semi-int proposal-layer; watch allowlist as third posture) | YES — all four; most severe: semi-int merged-entity top-scored artifact | watch-clank allowlist is a conforming counter-model (conservative variant), not counter-evidence |
| COM-004 | STRONG | 8/9 Clanks convergent 3–5 tier stacks, zero cross-citation | YES — oem-radar Stage 11 tier-collapse (44.6% of "alerts") | single-ledger toy Clank (counterexample survived via trigger scoping) |

Lineage caution applied throughout: inherited implementations (smartwatch,
feature-phone) are not counted as independent votes; the two
incident-recurrence lineages in COM-002 are independent because the same
failure recurred with zero cross-citation.

## Counterexample outcomes

All four invariants survive their strongest counterexamples as scoped:
C1 (stateless/archive Clank → trigger-unmet), C2 (catalogue-only Clank →
novelty views out of scope; no-baseline Clanks → nothing to exclude),
C3 (conservatism misses real merges → visible benign duplicate vs silent
canon corruption; gated proposal-layers conform), C5 (single-table
discriminator conforms; no-derived-state Clanks out of scope).

## Overlap / domain assessment

- COM-001: DISTINCT from the frozen UI corpus (dataset representation vs
  displayed semantics).
- COM-002: COMPLEMENTARY to STD-UI-COM-003 (data-layer mirror of the
  ratified read-side-exclusion shape; no restatement).
- COM-003: DISTINCT (adjacent in subject to STD-UI-SKU-001, different
  layer: identity resolution vs QC vocabulary). Cross-Clank identity
  explicitly out of scope.
- COM-004: COMPLEMENTARY to STD-UI-COM-002 (general decision-tier
  traceability; UI-COM-002 is the stricter UI-specific instance). DISTINCT
  from COM-009/010/011 (data layer vs operator-facing surfaces).
- Domain fit: all four are DATA/ONTOLOGY (semantic truth contracts over
  derived data). No rehome. Domain shape confirmed single
  `data-ontology` (Pass 2 recommendation stands).

## Recommendations (one per standard)

| Standard | Recommendation |
|---|---|
| STD-DATA-COM-001 | RATIFY AS WRITTEN |
| STD-DATA-COM-002 | RATIFY AS WRITTEN |
| STD-DATA-COM-003 | RATIFY AS WRITTEN |
| STD-DATA-COM-004 | RATIFY AS WRITTEN |

All four meet the full ratification bar: STRONG evidence,
implementation-neutral wording, correctly scoped triggers, testable
acceptance criteria, meaningful forbidden behavior, no surviving
legitimate counterexample, no unresolved domain-boundary problem, no
problematic duplication.

## Unresolved operator questions

1. Per-standard ratification (decisions/0010–0013, all awaiting operator
   decision; all recommend Option A — ratify as written).
2. Pre-existing operator flags unrelated to ratification (unchanged from
   earlier passes): watch-clank's empty production epoch table (live
   exposure); smartphone-clank's presentation-only release-state badge
   (product backlog); decisions/0009 lineage annotation (tablet-clank
   archive is korean-tech-wire-derived); watch-clank's COM-007 RUN NOW
   maturity badge (ratification-created backlog).

## Decision records

- [decisions/0010-data-com-001-decision.md](../../decisions/0010-data-com-001-decision.md)
- [decisions/0011-data-com-002-decision.md](../../decisions/0011-data-com-002-decision.md)
- [decisions/0012-data-com-003-decision.md](../../decisions/0012-data-com-003-decision.md)
- [decisions/0013-data-com-004-decision.md](../../decisions/0013-data-com-004-decision.md)
