# Data/Ontology Standards Baseline v1.0 — freeze note (2026-08-31)

**Baseline id:** `data-ontology-standards-v1.0` · **Tag:**
`data-ontology-standards-v1.0` · **Corpus state frozen at:** `ae586c4` ·
**Status:** FROZEN

## What v1.0 means

This is the first frozen baseline of Standards Clank's Data/Ontology
standards corpus: **4 RATIFIED / 0 PROPOSED**, captured after a full
evidence-to-ratification pipeline and a dedicated hold-resolution audit
that concluded no additional held concern is required for v1. It is a
baseline of the Data/Ontology corpus only — not a declaration that the
entire Standards Clank project is complete, and not a claim about any
Clank's permanent conformance. The UI baseline (`ui-standards-v1.0`) is a
separate, independent, unchanged freeze.

## What is included

The four ratified `STD-DATA-COM-*` standards (see
[data-ontology-standards-v1.0.json](data-ontology-standards-v1.0.json) for
the exact id/version list), the agent-facing layer (constitution,
ratified-index, agent-checklist, generator), and the decision/hold-
resolution trail behind them:

- **`STD-DATA-COM-001` v1 — Continuity/epoch state must be explicit.**
  Where a Clank derives novelty or alerting from comparison against its
  own history, a discontinuity in that history (data loss, restore,
  re-baseline, collector replacement, region change) must be recorded as
  an explicit, queryable fact — distinct from the records and from any
  novelty judgement made using them — and baseline/bootstrap records must
  be distinguishable from ordinary ones at read time.
- **`STD-DATA-COM-002` v2 — First-seen is not novelty.** A record's first
  appearance in a Clank's own database must not, by itself, be treated as
  evidence the thing is new in the real world. Every default
  novelty-asserting path — including secondary or derived ones — must
  exclude baseline/continuity-tagged records by construction, verifiable
  by inspecting the path's own definition, not by a caller's convention
  or by today's clean output. Editorial freshness, where modeled, stays a
  separate judgement from discovery-novelty.
- **`STD-DATA-COM-003` v2 — Entity-identity merges must be conservative,
  evidence-gated, auditable, and reversible.** A missed merge must be
  preferred over a false merge. A coarse candidate-surfacing key alone is
  never sufficient grounds for a committed merge. Any automatic merge
  must be evidence-gated on a discriminator present in the records under
  consideration, auditable (including which mechanism performed it), and
  the pre-merge per-source identities must remain reconstructable.
- **`STD-DATA-COM-004` v1 — Observation, canonical-fact/change, and
  operator-decision records must stay separable and traceable.**
  Observation, canonical, and (where present) decision records must
  remain distinguishable and separately consumable — no unreviewed raw
  observation may reach a "canonical changes" or "operator decisions"
  stream. Every canonical fact must trace back to its supporting
  observations, every operator decision to the state it was made
  against, and every inferred value must remain distinguishable from a
  directly-stated one.

## Why the corpus is complete enough to freeze

The evidence base, in order:

1. **Pass 0A — evidence inventory.** Nine-repo fleet evidence mining, no
   standards drafted: 32 incidents, 13 clusters.
2. **Pass 0B — adversarial adjudication.** Each HIGH/MEDIUM/LOW cluster
   ruled ADVANCE, HOLD, REHOME, or REJECT; 4 clusters advanced.
3. **Pass 1 — drafting.** The 4 ADVANCE candidates drafted as PROPOSED
   standards in a new `data-ontology` schema domain.
4. **Pass 2 — adversarial review.** 2 APPROVE FOR RATIFICATION SURVEY, 2
   REVISE.
5. **Pass 2.5 — targeted revision.** The two REVISE verdicts applied
   exactly as specified, with no improvisation on the version-bump
   question (operator confirmed: bump both revised drafts to v2).
6. **Pass 3 — ratification survey.** All four surveyed against the full
   evidence corpus; all four recommended RATIFY AS WRITTEN; four
   awaiting-operator-decision records produced, none self-ratified.
7. **Operator ratification.** Explicit operator ruling ratified all four
   as written, preserving versions COM-001 v1 / COM-002 v2 / COM-003 v2 /
   COM-004 v1 (decisions/0010-0013, ratification closure `4407654`).
8. **Hold-resolution audit.** A dedicated pass
   ([holds-disposition.md](../docs/data-ontology/holds-disposition.md))
   ruled on the entire Pass 0B HOLD/REHOME backlog against the four
   now-ratified standards and the accumulated evidence. Conclusion:
   **no additional held concern advances into a DATA v1 baseline** — the
   ratified four already cover every STRONG-evidence concern the fleet
   surfaced.

A mature-enough-to-freeze corpus does not mean a finished domain — see
"What remains outside v1" below for exactly what was deliberately left
for later evidence.

## What remains OUTSIDE v1

None of the following are part of the frozen corpus. Each reopening
trigger is preserved verbatim from the hold-resolution audit — a future
pass should re-check these triggers, not re-litigate the ruling from
scratch.

**DEFER BEYOND V1** (insufficient evidence today, may return with more):

- **Honest-unknown / availability-honesty backing.** Promotion trigger: a second independent instance, an incident, or disposition of the smartphone backlog into a backed field.
- **Cross-Clank entity identity.** Promotion trigger: adjudication of clank-architecture's ADR-0014, or a concrete cross-Clank collision incident.
- **Confidence-and-certainty semantics.** Promotion trigger: an operator misreading confidence across Clanks, or a second QC-vocabulary harmonization pass.
- **Canonical fact overwrite discipline.** Promotion trigger: a documented overwrite-induced provenance loss.
- **Regional variant identity.** Promotion trigger: a real
  false-merge/false-split incident across regions (no fixed trigger
  language beyond needing operational evidence — see the audit for the
  full ruling).

**REHOME** (not a fleet rule; belongs elsewhere):

- **Timestamp-shaped values mistaken for chronological truth** — rejected
  as a data-ontology standard; the transferable artifact (adversarial
  fixtures like `uuid_trap_db`) is rehomed to diagnostic/testing
  practice.

**REJECT** (considered and declined):

- **Source-disagreement representation** — one implementation, zero
  incidents; may return with evidence if a Clank ever needs to represent
  conflicting sources.

## What this freeze does NOT mean

- **Future Data/Ontology standards are not forbidden.** New candidates,
  if evidence emerges (including any of the reopening triggers above),
  go through normal governance from evidence onward.
- **Standards may be revised or superseded through governance.**
  Versioned revisions and supersessions remain the normal path — COM-002
  and COM-003 are already v2, a precedent this freeze does not change.
- **Clanks are not automatically conformant forever.** Conformance is a
  property of a Clank at a point in time; no data-ontology conformance
  audit has been performed yet, and this freeze makes no claim about any
  specific Clank's current state.
- **v1 does not prescribe a schema, ID system, baseline/epoch mechanism,
  merge algorithm, or evidence envelope.** Every standard in this corpus
  constrains a consequence (explicitness, exclusion, reversibility,
  traceability), never an implementation — see each standard's own notes
  and `docs/data-ontology/constitution.md`'s "Consequence, not algorithm"
  section.
- **The UI baseline (`ui-standards-v1.0`) is independent and unchanged**
  by this freeze.

## Change policy after the freeze

Any later normative Data/Ontology change must use normal governance and
result in exactly one of: a **new standard**, a **versioned revision**, a
**supersession**, or a **retirement**. The `data-ontology-standards-v1.0` manifest and
tag are immutable historical records — never rewritten, never moved.
Future corpus state may therefore
diverge from v1.0 legitimately; v1.0 remains the record of what was true
at freeze time.
