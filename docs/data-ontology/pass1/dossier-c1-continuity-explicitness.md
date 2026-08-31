# Pass 1 drafting dossier — C1: Continuity/epoch explicitness

**Candidate ID**: C1 (Pass 0B) → **STD-DATA-COM-001** (this pass)

**Source Pass 0 cluster(s)**: `baseline-epoch-continuity` (Pass 0A,
STRONG/HIGH)

**Adjudication result** (Pass 0B): KEEP DISTINCT + ADVANCE, with a split
— the standard itself advances; watch-clank's live empty-production-epoch
exposure is separated out as an operator flag, not standardization
evidence.

## Strongest evidence

Four independent implementations (watch-clank `OperationalEpoch`,
oem-radar's documented cutover procedure, feature-phone-clank's and
smartwatch-clank's `core/continuity.py`), a near-complete unratified
draft standard already in the fleet (clank-architecture ADR-0006, which
smartwatch-clank already builds against), and a dated, real incident
(watch-clank's Timex catalogue backfill burst) demonstrating the exact
failure mode: baseline-protected records re-alerted as fresh after a
restore/backfill.

## Strongest counterexample

"An append-only evidence archive with no novelty logic has no epochs and
needs none — the invariant is untestable there." Tested in the Pass 0B
candidate card: survives by narrowing the trigger to Clanks that actually
derive novelty/alerting from local history. A Clank that cannot lose or
restore data doesn't exist in the surveyed fleet; every Clank that can,
and derives novelty from history, needs some form of explicit continuity
representation. The counterexample identifies a real boundary (trigger
scope), not a case where the invariant is false within its scope.

## Exact semantic boundary

This standard binds **the representation and read-side treatment of
discontinuity**, not the backup/restore procedures that cause it and not
any particular storage mechanism. It requires that a continuity break be
an explicit, queryable fact and that baseline/bootstrap records be
distinguishable from ordinary post-continuity records — it does not
require a specific table, event-type vocabulary, or promotion workflow.

## Overlap analysis

- **STD-DATA-COM-002** (novelty read-side exclusion) directly depends on
  this standard's concept of baseline/continuity-tagged records — COM-002
  requires default novelty views to exclude what COM-001 requires to be
  representable. They are drafted as separate standards because COM-001's
  invariant (continuity must be representable) is logically prior to and
  independently testable from COM-002's invariant (novelty views must use
  that representation); a Clank could satisfy COM-001 and still fail
  COM-002 (write the flag, never read it — exactly the incident that
  motivated COM-002).
- No overlap found with any ratified `STD-UI-*` standard. STD-UI-COM-009
  (run/stage observability) is adjacent in spirit (both concern whether
  internal state is discoverable) but governs operator-facing run-surface
  UI, not data-layer continuity representation.
- No overlap with STD-DATA-COM-003 or -004.

## Draft rationale

Adopts ADR-0006's substance (an explicit continuity fact distinct from
ordinary records; "a fresh baseline is never novelty") without adopting
its specific schema (`ContinuityEvent` type enum) or incorporating it by
reference — ADR-0006 remains clank-architecture's own PROPOSED document,
cited as evidence per the task's instruction to treat ADRs as evidence,
not automatic authority.

## Unresolved wording questions

1. Should "region change that invalidates prior comparisons" (named in
   the task's own drafting guidance) be listed explicitly as a
   discontinuity trigger, or does it properly belong to the still-HELD
   `regional-variant-identity` cluster instead? Included in the drafted
   requirement text as one example among several (data loss, restore,
   re-baseline, collector replacement, region change) — narrow enough to
   not duplicate the held cluster, since this standard only requires the
   *break* be representable, not how regional identity itself works.
2. The task explicitly forbade citing watch-clank's empty production
   epoch table as violation evidence pre-ratification. This dossier and
   the standard's own notes field observe that instruction; the exposure
   is reported only in this pass's final report as an operator flag.

## Recommendation: READY FOR REVIEW
