# Operations Pass 2 — Adversarial Draft Review (2026-08-31)

Reviews the three PROPOSED `STD-OPS-COM-*` drafts and the OPS-D candidate
at the Pass 1.5 state, against the Pass 0A evidence package, the Pass 0B
adjudication, and the frozen UI/DATA corpora. No fleet recrawl; no target
repo opened; ADR statuses re-confirmed once (ADR-0008/0009/0011 all
`PROPOSED — REVIEWED DRAFT`; Fleet Laws 3/5/7/8 ACTIVE; Law 9 DEFERRED).

**Verdict summary**

| Candidate | Verdict |
|---|---|
| OPS-A / STD-OPS-COM-001 (execution materialization truth) | APPROVE FOR RATIFICATION SURVEY |
| OPS-B / STD-OPS-COM-002 (health-honesty two-axis) | APPROVE FOR RATIFICATION SURVEY |
| OPS-C / STD-OPS-COM-003 (promotion/soak evidence integrity) | APPROVE FOR RATIFICATION SURVEY |
| OPS-D (exclusivity-marker soundness, undrafted) | DRAFT AS STD-OPS-COM-004 |

---

## OPS-A — Execution materialization truth (STD-OPS-COM-001 v1)

- **Verdict: APPROVE FOR RATIFICATION SURVEY.**
- **Strongest aspect:** acceptance 3 splits the exact INC-027 failure —
  "intended/scheduled execution is distinguishable from an actually-
  materialized invocation: 'the schedule says this should run' and 'this
  ran' are never conflated" — while acceptance 4 turns INC-028's
  false-positive shape into a positive requirement (a no-work cycle is an
  explicit, positive outcome record). The two clauses together are what
  kills both failure directions.
- **Strongest weakness:** the trigger-source granularity question from
  the dossier is real — v1 binds at "an invocation occurred, from *a*
  trigger" without requiring which trigger source. Sufficient for v1 (the
  incidents were about nothing-recorded, not mis-attribution); flagged,
  not blocking.
- **Strongest counterexample:** an externally scheduled Clank with a
  reliable external scheduler and no native scheduler model. Survives:
  the trigger field states scheduler technology and location are out of
  scope; the standard binds what the Clank records *after* a trigger
  fires, and an externally-triggered run still produces an invocation and
  an outcome the Clank can record.
- **Configured/scheduled vs invoked vs outcome:** all three distinguished
  (trigger field + acceptance 1–3).
- **Explicit no-work:** a valid, positive outcome (acceptance 4,
  FORBIDDEN 3).
- **External schedulers / one-shot invocations:** both conform; location
  and cardinality are out of scope.
- **"Own stored data" wording:** does not prescribe persistence
  architecture — it requires the evidence be in data the Clank controls,
  which is the point: evidence must not live only in an external
  platform's logs the Clank cannot query. Kept as drafted.
- **Duplicate execution:** detectable (acceptance 5, FORBIDDEN 4) but
  never forbidden — single-authority stays Fleet Law 5's. No overreach.
- **Process-start-only attestation:** forbidden explicitly (FORBIDDEN 2).
- **Stage detail:** none prescribed; ADR-0008's finer vocabulary stays
  clank-architecture's.
- **Fleet Law boundary:** Law 5 owns authority; OPS-A owns
  materialization/outcome truth. The wording stays on OPS-A's side.
- **Trigger assessment:** correctly binds only Clanks that fire
  collection or comparable scheduled work from some trigger; stateless
  and never-triggered Clanks are out by trigger.
- **Acceptance-criteria assessment:** all five testable by dataset
  inspection (invocation record, outcome record, scheduled-vs-materialized
  split, positive no-work record, dual-trigger visibility).
- **Implementation-neutrality assessment:** clean — no storage shape,
  stage vocabulary, scheduler technology, or heartbeat mechanism mandated.

## OPS-B — Health-honesty two-axis complement (STD-OPS-COM-002 v1)

- **Verdict: APPROVE FOR RATIFICATION SURVEY.** Classified
  **DISTINCT NARROW COMPLEMENT** to ACTIVE Fleet Law 3 — not problematic
  duplication.
- **Narrower-than-Law-3 test:** passed. Law 3 (ACTIVE) owns the
  health-honesty *principle* ("HTTP success without useful output is not
  healthy"). COM-002 ratifies only the *representability* slice: the two
  axes must be independently representable in the Clank's state model,
  whatever surfaces or names exist. The `requirement` text never restates
  Law 3's evaluation rule.
- **Wholesale-restatement test:** passed — the `rationale` and `notes`
  fields explicitly defer the principle to Law 3 and scope this standard
  to the vocabulary/conflation slice nine differently-named fleet
  implementations leave open.
- **UI COM-008 relationship:** COMPLEMENTARY, different layer — COM-008
  governs what an operator-facing display must show; COM-002 binds the
  underlying state model those displays read. A headless Clank with no
  health UI is still bound by COM-002, which is exactly why the
  Operations-layer standard is justified rather than duplicative.
- **Hybrid test (the decisive one):** a collector firing hourly with HTTP
  200 but zero observations for three days (silent parser break): the
  model represents scheduler/liveness health = healthy and yield health =
  degraded/absent as two independent facts without violating any Fleet
  Law authority — Law 3 demands precisely this honesty, so the axes are
  real and the standard adds representability, not a competing principle.
- **Zero output legitimately healthy:** yes — acceptance 3 keys expected
  behavior to the source's own baseline; FORBIDDEN 4 bans forcing it
  anomalous *or* automatically healthy.
- **Scheduler success + starvation coexisting:** yes — that is the
  two-axis requirement's core case.
- **Single-axis Clanks:** out of scope by trigger ("depends on
  distinguishing" is unmet when only one axis exists).
- **Exactly two fields:** not required — trigger and acceptance 1
  ("whatever the underlying storage or naming convention") keep
  representation free.
- **"Health" narrowing:** the requirement names the axes descriptively
  ("operational execution/liveness health", "output/yield health") and
  never mandates a score, formula, or health-*score* semantics.
- **Trigger assessment:** correctly binds only Clanks whose health,
  alerting, or monitoring depends on the liveness-vs-yield distinction;
  pure-analysis and single-axis Clanks are out by trigger.
- **Acceptance-criteria assessment:** all four testable — independent
  queryability, executed-but-zero distinct from executed-and-yielded,
  baseline-relative zero classification, no dual-meaning status field.
- **Implementation-neutrality assessment:** clean — no storage shape,
  naming convention, or score formula mandated; "at least two dimensions
  independently representable" is representation-level only.
- **Overlap assessment:** DISTINCT NARROW COMPLEMENT to Fleet Law 3
  (representability slice; principle stays Law 3's) and to
  STD-UI-COM-008/012 (display layer vs state-model layer).
- **Strongest counterexample:** pure-analysis Clank with neither axis —
  trigger-unmet, stated in the trigger field. Survives.

## OPS-C — Promotion/soak evidence integrity (STD-OPS-COM-003 v1)

- **Verdict: APPROVE FOR RATIFICATION SURVEY.**
- **Coherence test (the dossier's primary flag):** the four facets pass
  a fresh adversarial read as one invariant. The unifying question each
  facet answers is: *"can I trust the evidence claiming this collector is
  qualified?"* — (1) is the evidence what it claims (natural cycles vs
  interventions), (2) did the evidence window restart for a recorded,
  justified reason, (3) did operations accidentally destroy or silently
  count evidence, (4) do multiple qualification sources agree. Four
  attacks on one evidence chain — not four loosely-related rules.
- **Facet-1 evidence (MODERATE alone):** accepted. The clause is narrow
  (binds only where the natural/manual/deploy/recovery distinction
  *affects qualification*), it is the verifiability foundation INC-013's
  gate-drift detection depends on, and semiconductor-intelligence's
  OperationalScheduler proves the structural form is achievable. The
  dossier carries the MODERATE caveat honestly rather than smoothing it.
- **Soak itself standardized?** No — cycle counts, window lengths, and
  maturity state machines are explicitly per-Clank (trigger field and
  `requirement` closing line).
- **No-lifecycle Clanks:** out of scope by trigger, stated.
- **Manual runs counting when policy says so:** allowed — requirement
  (3) bans *silent* counting; explicit policy permitting a class of
  evidence is conforming, recorded, and distinguishable.
- **Material-change definitions:** left per-Clank — acceptance 2 requires
  only that the reset decision be recorded (build/change identity +
  stated reason), never how materiality is judged.
- **"Incidents do not reset":** correctly worded as evidence preservation
  (acceptance 3: evidence "remains intact afterward, or is explicitly
  marked not-yet-measurable"), not as "the clock can never restart."
  FORBIDDEN 2 bans *silent* discard — an explicit, recorded reset with
  reason conforms.
- **Failure legitimately resetting a clean window:** conforms — the
  failure is recorded, the clean window restarts, the incident history is
  preserved. Exactly the handoff's required shape.
- **Fail-closed wording:** implementation-neutral — acceptance 5 requires
  divergence be *detectable* and resolved as not-yet-eligible, without
  prescribing automated-vs-manual detection (confirmed intentional
  freedom, per the dossier's own flag).
- **Trigger assessment:** correctly binds only Clanks with a
  soak/promotion lifecycle; no-lifecycle Clanks are out by trigger.
- **Acceptance-criteria assessment:** all five testable — provenance
  recoverable from recorded data, reset decisions carry build identity +
  reason, pre-incident evidence survives (or is marked not-yet-measurable),
  interventions distinguishable from natural cycles, gate divergence
  detectable and failing closed.
- **Implementation-neutrality assessment:** clean — no cycle count,
  window shape, maturity state machine, gate architecture, or detection
  mechanism prescribed.
- **Strongest counterexample:** a production collector qualifying on a
  24-hour observation window with frequent manual diagnostics during the
  window. Survives: the standard binds evidence integrity of whatever
  qualification window exists — interventions must be distinguishable
  and non-qualifying unless policy permits, and reset decisions must be
  recorded — with no cycle-count or window-shape mandate anywhere.
- **Four-unrelated-rules test:** not triggered. The requirement's
  numbered facets (1)–(4) all bind the same evidence chain; the coherence
  reads naturally on a fresh adversarial pass.

## OPS-D — Exclusivity-marker soundness (undrafted)

- **Verdict: DRAFT AS STD-OPS-COM-004** (drafting in a tiny Pass 2.5;
  not in this pass).
- **Beyond-PID test:** the abstraction holds past PID locks — DB
  session-scoped advisory locks conform (the granting DB structurally
  observes connection death), expiring leases conform (clock-based
  reclamation is provable by the grantor), kernel-held handles conform
  (handle death is OS-observable), distributed leases with fencing tokens
  conform (fencing is grantor-issued proof), and a hostname+PID+
  process-start-time tuple conforms *if and only if* start-time actually
  proves the owner's identity — provenance of the proof is the invariant,
  not the identifier's shape.
- **"Structurally observable by the granting authority":** abstract but
  grounded by the card's exact-distinction line (validity is a property
  of the granting mechanism, not an inference the validating context
  interprets). Recommend the drafted standard keep the card's explanatory
  sentence verbatim alongside the formal invariant.
- **What exactly is forbidden:** any state-changing action based on
  unprovable ownership — reclaiming a marker as stale, honoring a marker
  as live, or mutating/killing a process identified by such a marker.
  Each of the four incidents is an instance.
- **Applicability:** binds markers that can outlive or refer across
  process lifetimes (cross-context coordination). Purely in-process
  locking is out of scope by trigger (the marker cannot outlive the
  context that validated it). Marker-less Clanks are out of scope.
- **Fleet Law overlap:** none. Law 5 governs scheduling authority; Law 7
  governs writer coordination as a principle; neither addresses the
  soundness of the coordination primitive's validity semantics. OPS-A
  does not overlap (a stale-lock deadlock satisfies materialization
  truth while starving — oem-radar's 81 refused fires).
- **Evidence discipline:** the shared fix lineage is one implementation
  lineage and is not counted as independent evidence; the four
  independent incident discoveries across four different environments
  (NAS container, Windows PID reuse, one-shot Docker, duplicate daemons)
  are what justify advancement.

## Drafting constraints for the Pass 2.5 STD-OPS-COM-004 task

- **Proposed title:** "Exclusivity/ownership markers must be validated by
  structurally observable proof"
- **Semantic invariant:** as per the candidate card's plain-language
  invariant, with the exact-distinction sentence kept verbatim.
- **Trigger/applicability:** any Clank using exclusivity/ownership
  markers to coordinate execution across process or context boundaries;
  purely in-process locking and marker-less Clanks are out of scope.
- **Minimum acceptance concepts:** (1) marker validity determinable from
  grantor-observable state; (2) reclamation only on grantor-observable
  proof of owner death or expiry; (3) all four fleet incidents'
  failure shapes non-conforming under the standard.
- **Minimum forbidden concepts:** reclaiming/honoring/acting on a marker
  based on an identifier whose liveness/ownership the validating context
  cannot structurally prove (PID reuse, namespace-relative PIDs, ephemeral
  hostnames); treating mechanism-prescription as the invariant.
- **Implementation freedoms:** flock/msvcrt, DB session advisory locks,
  lease services, fencing tokens, marker storage and expiry policy.
- **Fleet Law relationship:** COMPLEMENT to ACTIVE Laws 7 and 5; no ADR
  relationship (ADR-0009 governs destructive mutation, a different
  concern).
- **Strongest counterexample survived:** DB session locks and fencing
  tokens differ mechanically from flock yet conform; bare PID checks fail
  everywhere.

## Fleet Law / ADR reconciliation

| Candidate | Existing governance | Relationship | Conflict? |
|---|---|---|---|
| OPS-A | ADR-0008 (PROPOSED draft) | COMPLEMENTARY — two-fact minimum vs six-stage vocabulary | No |
| OPS-A | ADR-0011 (PROPOSED draft) | COMPLEMENTARY — no-work semantics referenced, not restated | No |
| OPS-A | Fleet Law 5 (ACTIVE) | DEFER TO EXISTING AUTHORITY (single-authority governance; OPS-A adds detection only) | No |
| OPS-B | Fleet Law 3 (ACTIVE) | NARROW COMPLEMENT (axis vocabulary/conflation slice; principle stays Law 3's) | No |
| OPS-B | STD-UI-COM-008 / COM-012 | COMPLEMENTARY (display layer vs state-model layer) | No |
| OPS-C | Fleet Law 8 (ACTIVE) | NARROW COMPLEMENT (evidence verifiability/reset/drift slice; gate authority stays Law 8's) | No |
| OPS-C | ADR-0006 (PROPOSED) | COMPLEMENTARY — incident-does-not-reset adopted as acceptance substance, cited not incorporated | No |
| OPS-C | STD-UI-COM-005 / COM-007 | COMPLEMENTARY (promotion authority/UI-control semantics vs evidence integrity) | No |
| OPS-D | Fleet Law 5 / Law 7 (ACTIVE) | COMPLEMENTARY (marker-validity soundness; authority/coordination stays the Laws') | No |
| OPS-D | ADR-0009 | DISTINCT (destructive mutation vs exclusivity markers) | No |

## Domain-boundary confirmation

Confirmed out of Operations, unchanged from prior passes: revision/config/
wiring deployment truth and schema-deployment gating (→ future DEPLOYMENT
domain, clusters 8/9/12); notification retry/idempotency (→ future
DELIVERY domain, cluster 15); destructive production mutation safety
(→ DEFER to ADR-0009 governance question, cluster 10); blocked/lifecycle
prose model (→ HOLD, cluster 14). None resurrected by this review.

## Ratification-readiness summary

OPS-A, OPS-B, and OPS-C are ready for the ratification survey as drafted
(OPS-C with its four-facet coherence confirmed on fresh read; OPS-B with
its Law 3 complement status confirmed on fresh read). OPS-D should be
drafted as STD-OPS-COM-004 in a tiny Pass 2.5 under the constraints
above, then join the same survey. No HOLD verdicts; no candidate
requires re-enrollment in the HOLD set.
