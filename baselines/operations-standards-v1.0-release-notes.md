# Operations Standards Baseline v1.0 — freeze note (2026-08-31)

**Baseline id:** `operations-standards-v1.0` · **Tag:**
`operations-standards-v1.0` · **Corpus state frozen at:** `fe841ef` ·
**Status:** FROZEN

## What v1.0 means

This is the first frozen baseline of Standards Clank's Operations
standards corpus: **4 RATIFIED / 0 PROPOSED**, captured after a full
evidence-to-ratification pipeline and a dedicated hold-resolution /
final-gap pass that concluded no essential Operations contract remains
missing. It is a baseline of the Operations corpus only — not a
declaration that the entire Standards Clank project is complete, and not
a claim about any Clank's permanent conformance. The UI baseline
(`ui-standards-v1.0`) and Data/Ontology baseline
(`data-ontology-standards-v1.0`) are separate, independent, unchanged
freezes.

## What is included

The four ratified `STD-OPS-COM-*` standards (see
[operations-standards-v1.0.json](operations-standards-v1.0.json) for the
exact id/version list) and the full evidence/adjudication/drafting/review/ratification
trail behind them:

- **`STD-OPS-COM-001` v1 — Execution invocation and outcome must be
  independently recorded, never inferred from scheduler-claimed state.**
  A Clank that fires collection from any trigger mechanism must record,
  in its own store, that an invocation occurred and what outcome it
  produced — neither inferred from a scheduler's "enabled"/"next-run"
  state. A legitimately empty due-gated cycle must be recorded as an
  explicit no-work outcome, never left as an absence indistinguishable
  from a materialization failure.
- **`STD-OPS-COM-002` v1 — Scheduler/trigger-liveness health and
  outcome/yield health must remain independently representable.** A job
  can exit successfully while producing nothing useful; execution
  liveness and output/yield health must stay two independently
  determinable dimensions, and zero output must remain classifiable
  according to a source's own expected behavior rather than silently
  collapsed into ordinary "healthy."
- **`STD-OPS-COM-003` v1 — Promotion/soak qualification evidence must be
  structurally verifiable, reset-traceable, and gate-drift-detectable.**
  Trigger provenance (natural/manual/deploy/recovery), soak-clock reset
  decisions, incident/manual-recovery history, and multi-gate promotion
  agreement must all be recoverable from a Clank's own stored data, not
  merely asserted. Cycle counts and maturity-state-machine shape are
  explicitly left as per-Clank policy.
- **`STD-OPS-COM-004` v1 — Exclusivity/ownership markers must be
  validated by structurally observable proof.** A run lock, lease, or
  ownership record's validity must be determinable from state the
  granting authority itself observes, never inferred from a reusable or
  context-ambiguous identifier (PID, hostname). Mechanism is free — OS
  advisory locks, database session locks, leases, kernel handles, and
  fencing tokens all conform provided the proof itself is
  grantor-observable.

## Why the corpus is complete enough to freeze

The evidence base, in order:

1. **Pass 0A — evidence inventory.** Six parallel read-only surveys of
   all nine fleet Clanks plus `clank-architecture` and `diagnostic-clank`
   (both its GitHub repository and the live NAS incident log) against 15
   named topics: 45 incidents, 15 candidate clusters.
2. **Pass 0B — adversarial adjudication.** All 15 clusters adjudicated:
   3 ADVANCE (merging 7 clusters), 3 REHOME, 1 DEFER, 1 HOLD.
3. **Pass 1 — drafting.** The three fully-carded ADVANCE candidates
   drafted as PROPOSED standards. A fourth cluster (pid-namespace-unsafe
   locking) had been marked ADVANCE in Pass 0B's disposition table but
   lacked a full candidate card at Pass 1's commissioning — recorded
   honestly as a scope note rather than silently dropped.
4. **Pass 1.5 — scope-omission resolution.** The fourth candidate given
   a full card (OPS-D, "Exclusivity-marker soundness") and re-adjudicated
   ADVANCE, with standard drafting explicitly deferred to a later,
   separate task.
5. **Pass 2 — adversarial review.** The three drafted standards each
   independently reviewed against their own finished text (all APPROVE
   FOR RATIFICATION SURVEY); the OPS-D candidate reviewed pre-draft, with
   a verdict of DRAFT AS STD-OPS-COM-004 and explicit drafting
   constraints for a future task.
6. **Pass 2.5 — OPS-D drafting.** STD-OPS-COM-004 drafted following
   Pass 2's constraints exactly.
7. **Pass 3 — ratification survey.** All four standards surveyed against
   the full evidence corpus; all four recommended RATIFY AS WRITTEN, with
   STD-OPS-COM-004's different review path (see below) flagged rather
   than smoothed over.
8. **Operator ratification.** All four standards ratified as written at
   v1 (decisions/0014-0017, ratification closure `b345ae2`).
9. **Hold-resolution / final-gap pass**
   ([holds-disposition.md](../docs/operations/holds-disposition.md))
   reconfirmed all four HOLD/DEFER/REHOME dispositions and checked every
   one of the 15 original survey topics, plus all 45 incident-ledger
   rows, against the ratified corpus. Conclusion: **NO ESSENTIAL OPERATIONS CONTRACT MISSING.**

## A process note carried forward honestly

`STD-OPS-COM-004` followed a different review path than the other three:
Pass 2 adversarially reviewed the **pre-draft OPS-D candidate** and
issued drafting constraints; the finished `STD-OPS-COM-004.json` text
itself never went through its own dedicated Pass-2-style review of the
finished wording the way `STD-OPS-COM-001/002/003` each individually
did. This was recorded explicitly in `decisions/0017-ops-com-004-decision.md`
and the Pass 3 ratification survey, and the operator ratified it as
written with that note visible — not an oversight, a disclosed process
difference the operator weighed and accepted.

## What remains OUTSIDE v1

None of the following are part of the frozen corpus. Each was
reconfirmed, not merely carried over, by the hold-resolution pass:

**HOLD** (real mechanism gap, insufficient evidence of harm to
standardize yet):

- **Lifecycle-state model: BLOCKED is prose, not code.** Several fleet
  members record a "blocked from production" determination only in a
  ticket or handoff doc, never as an enforced code-level state — a real
  gap, with zero confirmed harmful mispromotion found. Revisit if that
  changes.

**DEFER** (a complete governing contract already exists elsewhere):

- **Destructive production-action authority** — the most severe concern
  found in the entire Operations survey (two agent-performed production
  volume deletions, one with total unrecoverable data loss). Deferred to
  `clank-architecture` ADR-0009, a complete, reviewed, incident-authored
  8-step contract. A competing Standards Clank text would add no
  marginal safety. ADR-0009 remained `PROPOSED — REVIEWED DRAFT` (not
  ACTIVE) as of this freeze.

**REHOME** (deployment-mechanics and delivery-transport territory,
distinct layers from this corpus, future domain seeds):

- **Config drift, remote-host deployment truth, and schema/deploy
  fail-closed gating** — merge into a future DEPLOYMENT domain. The
  broadest-repo-count evidence cluster in the whole survey (8 of 9 fleet
  Clanks plus `diagnostic-clank`), but the semantic core ("repo says
  deployed" ≠ "host runs this") is deployment-mechanics territory,
  distinct from this corpus's scheduling/health/promotion/marker-validity
  scope. `clank-architecture` Fleet Law 9 covering part of this remains
  DEFERRED, keeping the ratification home genuinely open.
- **Delivery retry/idempotency** — one low-severity duplicate-notification
  incident; delivery-transport semantics, a future DELIVERY domain seed.

## What this freeze does NOT mean

- **Future Operations standards are not forbidden.** New candidates —
  including any of the HELD/DEFERRED/REHOMEd concerns above, if their
  reopening triggers occur — go through normal governance from evidence
  onward.
- **Standards may be revised or superseded through governance.**
  Versioned revisions and supersessions remain the normal path.
- **Clanks are not automatically conformant forever.** No Operations
  conformance audit has been performed against any specific Clank; this
  freeze makes no claim about any Clank's current state. One live finding
  worth naming: `STD-OPS-COM-004`'s evidence array does not cite
  `INC-044` (two concurrent Docker containers both acting as writers),
  even though that incident's failure shape is already covered by the
  standard's forbidden-pattern language — an evidence-citation gap noted
  by the hold-resolution pass, not a conformance finding against any
  Clank.
- **v1 does not prescribe a scheduler technology, a run-table schema, a
  health-score formula, a maturity state machine, cycle counts, or a
  locking mechanism.** Every standard in this corpus constrains a
  consequence (invocation/outcome recording, axis independence,
  evidence verifiability, validity-proof provenance), never an
  implementation.
- **Three of the four standards are explicit narrow complements to
  governance that is already ACTIVE** in `clank-architecture`
  (Fleet Laws 3, 5, 7, 8) — a materially different situation from the UI
  and Data/Ontology domains, where the closest prior art was itself only
  PROPOSED. Ratifying and freezing these standards does not activate,
  migrate, or restate any Fleet Law or ADR; each standard's own `notes`
  field states this boundary, and `clank-architecture` itself was not
  modified at any point in this domain's evidence-mining, drafting, or
  freeze work.
- **No agent-facing layer exists yet for this domain** (no
  `tools/operations_agent_layer.py`, no generated `ratified-index.json`/
  `agent-checklist.json`, no `docs/operations/constitution.md`) — unlike
  the UI and Data/Ontology domains, which both have one. This is a known
  gap recorded in the baseline manifest's `artifacts_note`, not silently
  omitted; building it is a reasonable, separately-authorized follow-up.
- **The UI and Data/Ontology baselines are independent and unchanged** by
  this freeze.

## Change policy after the freeze

Any later normative Operations change must use normal governance and
result in exactly one of: a **new standard**, a **versioned revision**, a
**supersession**, or a **retirement**. The `operations-standards-v1.0`
manifest and tag are immutable historical records — never rewritten,
never moved. Future corpus state may therefore diverge from v1.0
legitimately; v1.0 remains the record of what was true at freeze time.
