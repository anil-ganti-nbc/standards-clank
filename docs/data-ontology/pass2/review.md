# Data/Ontology Pass 2 — Adversarial Draft Review (2026-08-31)

Reviewer scope: the four PROPOSED `STD-DATA-*` drafts at `1f66cf9`,
reviewed against the Pass 0A evidence package, the Pass 0B adjudication,
and the frozen UI corpus (`ui-standards-v1.0`). No fleet recrawl; the
only source-repo inspections were Pass 0A-cited claims already
spot-verified during Pass 0B (smartphone dossier decoration + tablet
lineage header). Method: every draft attacked per the handoff's
per-standard question lists; verdicts below are final for this pass.

**Verdict summary**

| Standard | Verdict |
|---|---|
| STD-DATA-COM-001 (Continuity/epoch explicitness) | APPROVE FOR RATIFICATION SURVEY |
| STD-DATA-COM-002 (First-seen ≠ novelty; read-side exclusion) | REVISE |
| STD-DATA-COM-003 (Identity conservatism) | REVISE |
| STD-DATA-COM-004 (Provenance tier separation) | APPROVE FOR RATIFICATION SURVEY |

---

## STD-DATA-COM-001 — Continuity/epoch state must be explicit

- **Verdict: APPROVE FOR RATIFICATION SURVEY.**
- **Strongest aspect:** the acceptance criteria are cleanly
  representational — every binding test (explicit queryable boundary,
  downstream distinguishability without out-of-band knowledge, per-record
  in-gap/in-window determinability) can be checked by inspecting the
  dataset, exactly where this standard lives. The FORBIDDEN list bans the
  ephemeral-flag escape hatch ("operator memory, a manually-invoked CLI
  flag … where that reliance leaves no durable, queryable trace").
- **Strongest weakness:** the third requirement sentence ("A Clank MUST
  NOT allow historical or baseline-era records to silently acquire the
  semantics of current … records merely because they are present in the
  same table") mixes a representational clause with a consumer-facing
  clause whose subject is ambiguous (the data layer, or the views that
  read it?). The acceptance criteria are cleanly representational, so the
  blur is cosmetic — the consumer-facing half is COM-002's job, and
  COM-002 does it.
- **Strongest counterexample:** "A Clank compares against the live web
  rather than local history, and loses all local records anyway — data
  loss still hurts it, so the standard's trigger is too narrow."
  Answered: the invariant governs continuity-vs-novelty *semantics*, not
  backup/restore generally (that is OPERATIONS territory). A Clank whose
  novelty does not derive from local history has nothing for the
  continuity representation to disambiguate. Survives by scoping; a
  second counterexample (single rolling snapshot) survives trivially —
  recording the restore boundary is still meaningful and cheap.
- **Trigger assessment:** correctly binds only Clanks deriving
  novelty/alerting/editorial judgements from local prior history;
  stateless collectors, pure live-web comparators, and no-history Clanks
  are out by trigger, not by exemption. Fleet consequence if ratified:
  korean-tech-wire (derives alerting from local history, no continuity
  representation today) gains an expected backlog item — the same
  legitimate consequence pattern as watch-clank's COM-007 badge.
- **Acceptance-criteria assessment:** testable as written; acceptance 4
  ("for any given record … inside a recognized continuity gap or baseline
  window") is the strongest and directly encodes the TIMEX incident.
- **Implementation-neutrality assessment:** clean — mechanism list is
  exemplificative ("epoch marker, gap record, baseline flag, or an
  equivalent"), no table/event-type/storage mandate; ADR-0006's schema
  explicitly not adopted.
- **Overlap assessment:** DISTINCT from every UI standard (verified
  against COM-008/009/010/012 — those govern displayed semantics, this
  governs dataset representation). Correctly layered under COM-002.
- **Region-change example (Pass 1 question):** KEEP, as drafted. It is
  conditional ("that invalidates prior comparisons") and binds only that
  the *break* be representable — it presupposes no regional-identity
  model. Flag: if the HELD regional-variant-identity cluster is ever
  adjudicated, re-confirm this example still reads as a timeline fact,
  not an identity ruling.
- **Exact revision required:** none. Non-blocking wording note: consider
  clarifying the third requirement sentence's subject (data layer vs
  consumers) whenever the draft is next touched; the acceptance criteria
  already disambiguate in practice.

---

## STD-DATA-COM-002 — First-seen is not novelty; read-side exclusion

- **Verdict: REVISE** (one acceptance-criterion strengthening; the
  invariant, trigger, and every other clause are approve-grade).
- **Strongest aspect:** the scoping is exactly right — the exclusion
  binds novelty-consuming views, not catalogue/history views; the
  no-baseline-concept case is out by construction; and FORBIDDEN 1 names
  the precise incident shape (`ORDER BY first_seen DESC` presenting
  recency-of-observation as novelty).
- **Strongest weakness:** the clause doing the real work — "by
  construction" / "as part of its own definition" — has a residual
  ambiguity: does application-layer post-filtering *inside* the view's
  own code count? Would an exclusion living in a shared eligibility
  function (not textually in the query) conform? The current text can be
  read to exclude both legitimate designs or to permit a convention-
  dependent implementation, depending on the reader.
- **Strongest counterexample:** "A Clank's default novelty endpoint runs
  the unfiltered query and filters baseline rows in application code
  after fetch; the filter lives in a shared helper that a refactor can
  drop. The view 'excludes baseline records as part of its own
  definition' under a charitable reading — and the watch/oem-radar
  incident is exactly a filter that stopped being applied."
  Answered: the strengthened wording below closes this by requiring the
  predicate be *included or inherited* by the path's own definition, with
  post-hoc external filtering explicitly non-conforming.
- **Trigger assessment:** correct, including the explicit catalogue-view
  and no-baseline-concept exclusions.
- **Acceptance-criteria assessment:** acceptance 1 is the one materially
  ambiguous criterion (see weakness). Acceptances 2–4 are concrete and
  testable; acceptance 3 correctly permits operator inspection of
  baseline records without relabeling.
- **Implementation-neutrality assessment:** clean — no storage shape,
  no predicate syntax, no baseline-representation mandate (delegates to
  STD-DATA-COM-001).
- **Overlap assessment:** STD-UI-COM-003 is a deliberate structural
  mirror (read-side exclusion of decided items) at the UI layer —
  COMPLEMENTARY, not duplicative: COM-003 governs decided-QC-item
  visibility, this governs novelty correctness beneath any surface. No
  overlap with COM-008/009/010/011 (display-layer) or SKU-001. The
  editorial-freshness clause is correctly an optional-scoped corollary —
  splitting it into a separate standard would fragment one pattern for
  no ratification-tracking benefit. **One standard, not two.**
- **Does it survive catalogue-only systems?** Yes — trigger-unmet, stated
  in the trigger field.
- **Exact revision required (acceptance criterion 1, replace):**

  > "Every default query, view, or API path whose semantics assert
  > novelty — including secondary or derived such paths — excludes
  > baseline/continuity-tagged records by including, or explicitly
  > inheriting, a baseline-exclusion predicate (or an equivalent
  > eligibility rule) as part of that path's own definition. The
  > exclusion MUST be verifiable by inspecting the path's definition or
  > its explicitly-inherited eligibility rule; relying on callers to
  > filter, on filtering performed after the path's results are produced
  > by logic external to the path, or on assumptions about what got
  > written, does not conform."

  Evaluation notes (per the handoff's instruction not to adopt the
  proposed wording automatically): the "include **or inherit**" branch is
  adopted because a shared eligibility rule is legitimate and common
  (watch-clank's queue functions, korean-tech-wire's `run_collectors`
  gating); "post-hoc filtering external to the path" is adopted because
  it names the exact incident mechanism; the proposed "verifiable by
  inspecting the query itself" was **not** adopted as the sole proof —
  inspection is admissible evidence, but an inherited eligibility rule
  must also conform, and output-testing remains admissible supplementary
  evidence. This is a strengthening of the clause doing the standard's
  actual work; everything else in the draft is approve-grade.

---

## STD-DATA-COM-003 — Identity conservatism

- **Verdict: REVISE** (two exact tightenings; the invariant and posture
  are sound and the evidence is the strongest incident base in the
  corpus).
- **Strongest aspect:** consequence-level scoping — it binds *when* to
  merge and what a merge must preserve, never the matching algorithm;
  semiconductor-intelligence's gated proposal-layer and watch-clank's
  allowlist are both conformant by construction, which is the intended
  effect.
- **Strongest weakness:** FORBIDDEN 1's qualifier "available and
  conflicts" is ambiguous — available *where*? If "available anywhere",
  the forbidden is untestable; if "present in the records under
  consideration", it is testable. Additionally, the audit requirements
  do not require recording *which mechanism* performed an automatic
  merge — yet oem-radar's false-merge class recurred across two
  different code paths, and mechanism identity is precisely how
  recurrence becomes visible.
- **Strongest counterexample:** "Two sources report the same product
  with trivially different model numbers; conservatism misses a real
  merge forever, invisibly." Answered in the dossier and it holds: a
  missed merge is a visible, benign duplicate; a false merge silently
  corrupts canon. The asymmetry justifies the default posture, and the
  proposal-layer pattern conforms.
- **Trigger assessment:** correctly binds only merging Clanks; strictly
  one-to-one Clanks are out; regional variants explicitly left to the
  held cluster; cross-Clank identity explicitly out of scope (respects
  the C7 HOLD and ADR-0002).
- **Acceptance-criteria assessment:** acceptances 1–3 concrete and
  testable (reversibility named with conforming mechanisms and an
  explicit non-acceptability clause); acceptance 4 (human-reviewed path
  exists) testable. Acceptance 2's audit requirement is where the
  mechanism-recording revision belongs.
- **Implementation-neutrality assessment:** the draft's greatest strength
  — identity mechanism explicitly unprescribed, with the dossier
  documenting that two opposite mechanisms both conform. The two
  revisions below do not disturb this.
- **Overlap assessment:** DISTINCT from all UI standards; related to
  STD-DATA-COM-004 (a merge's audit trail is an instance of decision
  traceability) but separately scoped — a no-merging Clank is out of
  COM-003 yet still in COM-004. Correctly separate standards.
- **Does it improperly reach into cross-Clank identity?** No — the notes
  bind within-Clank merges only and cross-reference the C7 HOLD.
- **Pass 1 question 1 (conforming-mechanism list):** useful and correctly
  open-ended ("or an equivalent mechanism").
- **Pass 1 question 2 (fleet-wide minimum evidence bar):** **NO** — any
  universal evidentiary threshold is algorithm/ontology prescription this
  standard exists to avoid; enforceability is preserved by the audit-
  trail requirements (an auditor judges recorded bases, not declared
  confidence numbers).
- **Exact revisions required:**
  1. FORBIDDEN 1, replace "when a stronger discriminator that could
     resolve the ambiguity is available and conflicts" with "when a
     stronger discriminator that could resolve the ambiguity is present
     in the records under consideration (or in the merged record) and
     conflicts with the merge" — scoping "available" to the records
     themselves makes the forbidden testable instead of world-
     inspectable.
  2. Acceptance 2, extend to: "Any committed automatic merge records
     what evidence justified it, distinct from the coarse signal that
     merely surfaced the candidate, **and records which
     mechanism/decision-path performed the merge (e.g. a rule-set or
     code-path identity), so that a false-merge class recurring across
     code changes is detectable**" — directly motivated by oem-radar's
     recurrence pattern; records an identity label, not an algorithm
     prescription.

---

## STD-DATA-COM-004 — Provenance tier separation

- **Verdict: APPROVE FOR RATIFICATION SURVEY.**
- **Strongest aspect:** the separation requirement is mechanism-free
  (separate tables, discriminator column, or equivalent — all conform)
  while the FORBIDDEN list gives hard edges (no path back to
  observations; inferred values serialized as source claims; collapsing
  tiers so review/alerting cannot distinguish unreviewed observations).
  The inferred-vs-source-explicit clause is a genuinely new fleet
  invariant not covered by any UI standard.
- **Strongest weakness:** "at a granularity sufficient to explain why
  the Clank believes it" is qualitative — but the acceptance list anchors
  it (URL + content hash + extraction record, source-observation ID, or
  equivalent), and the FORBIDDEN edges make an audit actionable. The
  softness is the correct resistance to schema prescription (ADR-0002).
- **Strongest counterexample:** "A retention policy deletes old raw
  snapshots; the canonical fact outlives its payload — traceability is
  broken and the standard is violated by a healthy lifecycle."
  Answered: acceptance 2 explicitly admits URL + content hash +
  extraction record or an equivalent reconstructable reference, so
  payload expiry conforms as long as the *references* survive. Corollary
  now recorded explicitly: retention may expire raw payloads; it must
  never expire the traceability references themselves. This is the
  correct division — retention duration itself is lifecycle/operations
  policy and stays per-Clank (oem-radar's hash-on-disk and
  chinese-tech-wire's in-DB retention both conform), so **no
  retention-duration clause** is added.
- **Trigger assessment:** cleanly scoped — pure pass-through Clanks out;
  absent operator-decision layer excludes the decision clause without
  exempting the rest.
- **Acceptance-criteria assessment:** all four testable; the
  discriminator-column equivalence answers the handoff's "is one table
  with type discriminators enough?" — yes, and the text says so.
- **Implementation-neutrality assessment:** clean — no tier count, no
  envelope shape, no storage mandate; EventEnvelope cited as reference
  only, under an explicit ADR-0002 note.
- **Overlap assessment:** STD-UI-COM-002 is COMPLEMENTARY — it is the
  stricter, UI-specific instance (atomicity, race-guard, UI
  truthfulness) of COM-004's general decision-tier traceability; neither
  restates nor weakens the other. COM-009/010/011 govern operator-facing
  surfaces — DISTINCT. No problematic duplication anywhere.
- **Operator-decision scoping (Pass 1 question):** keep the broad "where
  an operator-decision layer exists" wording. Narrowing to decisions
  that "participate in canonical data state" would exclude separate QC
  archives — the exact pattern the fleet ratified around (watch-clank's
  separate QC store) — for no benefit; the clause adds traceability
  without conflicting with STD-UI-COM-002.
- **Exact revision required:** none.

---

## Domain shape

**KEEP SINGLE DATA-ONTOLOGY DOMAIN.** All four standards are semantic
truth contracts about how derived data relates to its sources and
history — one concern class, not four. The Pass 1 README's analysis is
endorsed: the pre-existing narrower domain names (`events`, `evidence`,
`classification`) would split C2 and C5 from C1/C3, have no home for C3
at all, and would scatter one coherent, cross-referencing pass across
mismatched folders. The `ui` domain already houses multiple
sub-concerns under one roof — same precedent. A split would create
artificial boundaries and duplicate cross-reference machinery without
improving governance.

## ADR boundary

Clean across all four drafts. ADR-0006 is cited as PROPOSED evidence
with an explicit adopted/not-adopted split (continuity concept adopted;
ContinuityEvent enum and storage shape not) and "not incorporated by
reference" (COM-001 notes). The draft EventEnvelope is cited as a
reference under an explicit ADR-0002 note (COM-004 notes). ADR-0002's
DO_NOT_STANDARDISE position is respected by COM-003's within-Clank scope
and COM-004's shape-neutrality. No draft treats a PROPOSED
clank-architecture ADR as normative fleet law. **No flag.**

## Ratification-survey readiness

COM-001 and COM-004 are ready for the ratification survey as drafted.
COM-002 and COM-003 should receive their exact revisions above (both are
single-clause changes), re-diffed, and then join the survey. No HOLD
verdicts: every draft's underlying candidate survived Pass 0B and no
Pass 1 exposure invalidated a candidate.
