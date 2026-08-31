# Pass 1 drafting dossier — C2: First-seen vs novelty, read-side exclusion

**Candidate ID**: C2 (Pass 0B) → **STD-DATA-COM-002** (this pass)

**Source Pass 0 cluster(s)**: `novelty-vs-discovery-time` (STRONG/HIGH),
`editorial-freshness-vs-novelty` (MODERATE/MEDIUM, folded in as a
corollary per Pass 0B's adjudication)

**Adjudication result** (Pass 0B): KEEP DISTINCT + ADVANCE. Pass 0B's own
assessment names this the strongest surviving invariant in the entire
program.

## Strongest evidence

watch-clank and oem-radar independently suffered the *identical* failure
shape — a baseline flag correctly written at discovery time, never
consulted by the display/aggregation query that fed alerts — with zero
cross-citation between the two repos. This is the decisive fact for how
the standard is scoped: it proves the semantic distinction alone
(first-seen != novelty, which every repo in the fleet already states as a
principle) is insufficient, because both repos held the correct principle
while the bug persisted in both. Supporting: feature-phone-clank's
baseline-gating, explicitly inherited from smartphone-clank's incident;
korean-tech-wire's own docs naming the editorial-freshness gap as unbuilt
future work.

## Strongest counterexample

"A catalogue-only Clank has no editorial freshness concept and legitimately
shows baseline records in its default catalogue view — the invariant fails
there." Tested in the Pass 0B candidate card: survives, narrowed. The
exclusion binds views that *consume novelty* (alert feeds, new-item
queues, editorial intake) — not catalogue/history views, which SHOULD
show baseline records. A second counterexample considered here during
drafting: korean-tech-wire has no baseline/continuity concept at all
(see STD-DATA-COM-001's trigger) — for such a Clank, COM-002's trigger is
simply unmet (nothing to exclude), not violated.

## Exact semantic boundary

Two binding clauses, deliberately kept in one standard rather than split:
(1) discovery time alone is never sufficient evidence of real-world
novelty (a representation-level statement, restating the fleet's already-
universal principle for completeness), and (2) any default/active
novelty-consuming view MUST exclude baseline-tagged records **by
construction** — a read-side predicate, not a write-side assumption. The
second clause is the one doing the actual standardizing work, per Pass
0B's finding that (1) alone would not have caught either watch-clank's or
oem-radar's incident. Editorial freshness is a third, explicitly optional
clause: where a Clank models it, it must stay distinct from both (1) and
(2) — but no Clank is required to build it.

## Overlap analysis

- Depends on **STD-DATA-COM-001**'s continuity/baseline concept (see that
  dossier's overlap section) — logically layered, not duplicative.
- Deliberately mirrors **STD-UI-COM-003**'s shape (a decided QC item must
  be excluded from the active queue via a read-side filter, not by
  deleting the record) at the data/query layer instead of the UI layer.
  No duplication: STD-UI-COM-003 says nothing about novelty correctness
  (only that *decided* items leave the visible queue); this standard says
  nothing about QC-decision UI. A Clank could conform to one and not the
  other.
- No overlap with STD-UI-COM-009/010/011 (run observability, timestamp
  display, delivery observability) — those govern operator-facing
  surfaces; this standard governs the query/logic layer beneath any
  surface.

## Draft rationale

The "news-family corollary" framing was deliberately chosen over a
separate `applies_to: ["news-based"]`-scoped standard, because the
editorial-freshness clause is not a distinct invariant requiring separate
ratification tracking — it's a narrower instance of the same "don't let a
convenient signal stand in for the real question" pattern, worded as an
explicit optional clause inside one standard rather than fragmenting the
concept across two IDs.

## Unresolved wording questions

1. Is "by construction" precise enough as an acceptance criterion, or
   does it need a more concrete test (e.g. "the exclusion predicate must
   be part of the query definition, verifiable by inspecting the query
   itself, not by testing outputs against today's data")? Left as
   drafted; flagged for review — this is the clause doing the real work
   and deserves the closest scrutiny.
2. Should "explicit override/review workflows may inspect baseline
   records without relabeling them novel" (from the task's own guidance)
   be tightened into a positive acceptance criterion (it is, as drafted)
   or is a forbidden-behavior framing clearer? Drafted as an acceptance
   criterion (permissive, not forbidden) since it describes a MAY-shaped
   allowance, not a MUST NOT.

## Recommendation: READY FOR REVIEW
