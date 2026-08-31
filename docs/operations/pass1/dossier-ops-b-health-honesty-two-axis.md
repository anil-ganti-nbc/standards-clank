# Pass 1 Dossier — OPS-B: Health-honesty two-axis complement

**Drafted as:** [STD-OPS-COM-002](../../../standards/operations/STD-OPS-COM-002.json)

## Candidate

Scheduler/trigger-liveness health and outcome/yield health must remain
independently representable — success in one dimension must not imply,
or be presented as, success in the other; zero output must remain
classifiable as healthy, anomalous, or unknown according to that source's
own expected behavior, never silently collapsed into a single
undifferentiated status.

## Source clusters

Pass 0A clusters `health-state-vs-scheduler-enabled-conflation` (topic
11) and `source-starvation-zero-vs-healthy-conflation` (topic 6), merged
by Pass 0B into candidate card
[ops-b-health-honesty-two-axis.md](../pass0/candidates/ops-b-health-honesty-two-axis.md).

## Pass 0B disposition

`ADVANCE`, explicitly as a **narrow complement**, not a restatement, of
`clank-architecture` Fleet Law 3 — the one candidate in this drafting set
where the governance-overlap question was sharpest, since Law 3 is
ACTIVE and CI-enforced, not merely PROPOSED.

## Evidence strength

STRONG — the single most convergently-independently-adopted pattern
found across the entire Operations survey: 7 of 9 surveyed Clanks
independently built some version of this two-axis split.

## Strongest incidents

- INC-006 — a collector's `ZERO_ITEMS` run status was counted as a
  healthy success, masking 20 consecutive empty runs.
- INC-022 — korean-tech-wire's independently-built found-vs-new
  distinction correctly caught an 8.5-day zero-new-observations block
  from a source-side access restriction, demonstrating the pattern
  working as intended, not just as a fix for a past failure.
- INC-043 / ADR-0007 — `diagnostic-clank`'s own health contract was built
  directly from a green-dashboard/missing-delivery-path incident,
  independent evidence the same conflation recurs at the governance
  layer too.
- Live, unfixed gap (not an incident, flagged as corpus evidence): a
  health-score computation that starts at a fixed baseline and does not
  check enablement, validation status, or output realism — cited in the
  standard's `rationale` and `notes` as evidence for the gap, explicitly
  not as a conformance finding against that Clank.

## Lineage assessment

Convergent, not copied — nine different axis names across the fleet, no
shared code found for the mechanism itself. The chinese-tech-wire/korean-tech-wire
found-vs-new pair is the cleanest independent-convergence
evidence in the whole corpus (near-identical concept, zero shared code).
Several Clanks cite Fleet Law 3 by name in their own source comments —
governance lineage, not code lineage.

## Fleet Law / ADR relationship

NARROW COMPLEMENT to Fleet Law 3 (ACTIVE, CI-enforced). Law 3 owns the
underlying health-honesty principle and is deliberately not restated in
the `requirement` text; this standard ratifies only the axis-vocabulary
and conflation-forbidden slice Law 3 leaves open across nine differently-named
fleet implementations. Distinct from `STD-UI-COM-008`/`STD-UI-COM-012`,
which govern operator-facing *display* of health/coverage semantics —
this standard binds the underlying data/operations-layer state model
those UI standards' displays must not misrepresent, explicitly noted in
both the `rationale` and `notes` fields to avoid the appearance of
duplication.

## Strongest counterexample

"A Clank with genuinely no scheduler and no external sources (pure
analysis over already-imported data) — neither axis exists."

**Why the wording survives:** trigger-unmet, stated explicitly in the
`trigger` field — a pure analysis tool has nothing for either axis to
bind. Every Clank with scheduled collection has both axes in some form,
which is the trigger condition the standard actually requires.

## Unresolved wording questions

- Is "NARROW COMPLEMENT" sufficiently legible from the requirement text
  alone, or does Pass 2 need to check whether an adversarial reader could
  read `STD-OPS-COM-002`'s acceptance criteria as silently restating Law
  3's own principle rather than the narrower vocabulary/conflation slice
  it claims to occupy? This is the standardization-risk item the
  candidate card itself flagged as MED.
- The `applies_to`/`trigger` boundary against `STD-UI-COM-008` is stated
  in prose (`notes`) but not tested against a concrete Clank scenario —
  worth Pass 2 constructing one hybrid case (a Clank whose only health
  surface is a UI display, no separate data-layer state) to confirm the
  boundary holds.

## Recommendation

**READY FOR REVIEW**, flagged for Pass 2 to specifically test the Fleet
Law 3 overlap boundary as its primary adversarial question.
