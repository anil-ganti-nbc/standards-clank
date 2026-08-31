# Pass 1 Dossier — OPS-C: Promotion/soak evidence integrity

**Drafted as:** [STD-OPS-COM-003](../../../standards/operations/STD-OPS-COM-003.json)

## Candidate

Wherever a Clank qualifies a collector for production via soak/natural-cycle
evidence, that evidence must be structurally verifiable from the
Clank's own stored data: trigger provenance recorded by the execution
path itself, soak-clock reset decisions recorded with build identity and
reason, incidents/manual recovery never silently resetting or silently
counting as clean evidence, and promotion-gate divergence detectable and
failing closed.

## Source clusters

Pass 0A clusters `natural-cycle-vs-manual-trigger-provenance-gap` (topic
2), `soak-clock-reset-semantics-and-material-change-judgment` (topic 3),
`dual-gate-promotion-authority-drift` (topic 5), and
`safe-manual-intervention-during-soak` (topic 15), merged by Pass 0B into
candidate card
[ops-c-promotion-soak-evidence-integrity.md](../pass0/candidates/ops-c-promotion-soak-evidence-integrity.md)
— the widest merge of the three drafted candidates (four source clusters
into one).

## Pass 0B disposition

`ADVANCE`. Pass 0B explicitly notes the merge is one coherent
evidence-integrity invariant with four facets rather than four separate
standards, and explicitly flags that facet (1) (trigger provenance) alone
has no confirmed harm incident — advanced anyway because it is the
verifiability foundation the other facets' incident (INC-013) depends on,
and because semiconductor-intelligence proves the structural form is
achievable. Evidence strength recorded as STRONG jointly, MODERATE for
facet (1) alone — carried into this dossier's evidence-strength line
below rather than smoothed over.

## Evidence strength

STRONG jointly (facet 1 — trigger provenance — MODERATE alone, per Pass
0B's own explicit caveat).

## Strongest incidents

- INC-013 — smartphone-clank's Motorola near-miss: two independent,
  uncross-checked promotion gates; only one updated during a real
  promotion; caught same-day, averting ~18 false alerts the next
  scheduled run would otherwise have produced. The clearest, most severe
  incident in this candidate's evidence.
- Fleet Law 8's three named historical violators (tablet, smartwatch,
  oem-radar) — governance-level confirmation this is not a one-off.
- INC-032 (tablet-clank operator-abort mid-soak) — the one dated
  intervention-during-soak incident; shows correct handling (partial
  cycles excluded from later promotion evidence), used as positive
  evidence that "distinguishable, non-qualifying" is achievable, not as
  evidence of harm.
- No confirmed harm incident exists for trigger provenance alone —
  recorded honestly in both the candidate card and here, not smoothed
  into the incident list as if it had independent incident backing.

## Lineage assessment

Soak-reset convergence (material-change-resets) is independent across
four repos, all narrative-only, none code-enforced. Trigger-provenance
mechanisms are independent wherever they exist at all (roughly half the
fleet has none). feature-phone-clank's single-gate promotion design is
**explicit incident inheritance** from smartphone-clank's INC-013, not
independent invention — counted once per Pass 0B's own lineage
discipline note, not double-counted as two separate pieces of evidence.

## Fleet Law / ADR relationship

NARROW COMPLEMENT to Fleet Law 8 (ACTIVE) — promotion-gate authority
itself stays Law 8's; this standard ratifies the evidence-verifiability,
reset-traceability, and drift-detectability slice Law 8 leaves open.
REFERENCES, does not restate, ADR-0006's incident-does-not-reset
principle (PROPOSED, not ACTIVE) — cited by name in `notes`, its
substance adopted as one acceptance criterion rather than incorporated by
reference.

## Strongest counterexample

Two, both tested explicitly in the candidate card:
1. "A Clank with no soak/promotion lifecycle — everything is production
   immediately — has nothing for these rules to bind."
2. "Manual diagnostic invocation during soak would become forbidden."

**Why the wording survives:** (1) is trigger-unmet, stated explicitly.
(2) is a misreading the `acceptance` criteria guard against directly —
"interventions are never required to be forbidden, only distinguishable
and non-qualifying unless policy explicitly says otherwise."

## Unresolved wording questions

- This is the widest merge of the three candidates (four clusters). Pass
  2 should specifically test whether the four facets in the
  `requirement` text (numbered 1-4) read as one coherent invariant or as
  four loosely-related rules wearing one standard's clothing — the
  candidate card asserts coherence but a fresh adversarial read is the
  right check.
- Facet (1)'s MODERATE-alone evidence strength is the weakest link in
  this candidate. Should Pass 2 consider whether facet (1) should be
  narrowed further, or whether its dependency relationship to facet (3)'s
  incident (INC-013) is sufficient justification as currently worded in
  the `rationale`?
- "Fail closed" (facet 4 / acceptance criterion 5) is stated as a
  requirement but the standard deliberately does not prescribe *how*
  divergence detection is implemented (automated check vs. periodic
  manual audit) — worth Pass 2 confirming this is intentional
  implementation-freedom rather than an under-specified acceptance
  criterion.

## Recommendation

**READY FOR REVIEW**, with an explicit flag that facet (1)'s standalone
evidence strength is the candidate's weakest point and the four-facet
coherence is the primary adversarial question for Pass 2.
