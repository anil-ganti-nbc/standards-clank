# Pass 0A → ZLM Adjudication Handoff

Seven clusters, HIGH priority only. Each gives ZLM exactly what's needed
to adjudicate without re-crawling the fleet: the claim to test, evidence
for/against, independent lineages, key citations, and the specific
question to answer. Full detail, MEDIUM/LOW clusters, and all raw survey
material: [README.md](README.md), [clusters/](clusters/),
[evidence-log.md](evidence-log.md), [incident-ledger.md](incident-ledger.md).

**Standing context that applies to all seven**: `clank-architecture`
(read-only reference, not modified) already has two PROPOSED-but-not-ACTIVE
ADRs covering large parts of this domain — **ADR-0006** (Observational
Continuity and Epoch Semantics) and **ADR-0014** (Typed Evidence, Semantic
Clocks, Lane Config) — and an explicit prior decision, **ADR-0002
(`DO_NOT_STANDARDISE`)**, rejecting full schema unification and centralized
identity services. Any adjudication should reconcile with these rather
than duplicate or silently override them.

---

## 1. Baseline/Epoch Continuity After Data Loss or Restore

**Claim to test**: a discontinuity in a Clank's data (loss, restore,
re-baseline) must be represented as an explicit fact (a new epoch, a
recorded gap), never silently treated as "nothing happened" or "fresh
discovery."

**Strongest evidence FOR**: four independent implementations
(watch-clank's `OperationalEpoch`, oem-radar's doc-only cutover procedure,
feature-phone-clank's and smartwatch-clank's `core/continuity.py`) plus a
near-complete unratified draft standard (ADR-0006) already specifying the
contract. smartwatch-clank explicitly builds against ADR-0006.

**Strongest evidence AGAINST / open risk**: watch-clank's own production
`operational_epochs` table on Hetzner is **currently empty** — the
mechanism exists in code but isn't populated in production; baseline
protection depends entirely on a manually-passed `--force-baseline` flag,
with three proposed remediations, none implemented. This is a live,
unresolved operational exposure, not just a design question.

**Independent lineages**: watch-clank, oem-radar, feature-phone-clank
independent of each other and of ADR-0006. smartwatch-clank explicitly
inherited from ADR-0006.

**Key citations**: `watch-clank/ai/handoff/INCIDENT_TIMEX_CATALOGUE_BACKFILL_BURST.md`
(addendum), `feature-phone-clank/src/feature_phone_clank/core/continuity.py`,
`smartwatch-clank/.../core/continuity.py:17-21`, `clank-architecture/adr/0006-continuity-and-epoch-semantics.md`.

**Question for ZLM**: should Standards Clank adopt/adapt ADR-0006 as a
fleet-wide contract, and separately — is watch-clank's empty-production-
epoch-table exposure itself worth an out-of-band alert to the operator
independent of any standard (it's a live risk, not just evidence)?

---

## 2. "New to Us" vs. "New in the World" (FIRST_SEEN_BY_CLANK vs. NEW_REFERENCE)

**Claim to test**: a row's first appearance in a Clank's own database is
not, by itself, evidence the thing it represents is new in the real
world.

**Strongest evidence FOR**: watch-clank's explicit two-value vocabulary
and alert-body-visible "novelty UNCONFIRMED" marking; feature-phone-clank's
baseline-gates-every-event-type design explicitly inherited from a named
cross-Clank incident (smartphone-clank's 73-device contamination);
diagnostic-clank's fleet-wide "knowledge law"
`FIRST_SEEN_BY_CLANK != NEW_TO_MARKET`.

**Strongest evidence AGAINST**: none — no repo disputes the principle.
The interesting counter-evidence is a **recurrence pattern**: watch-clank
and oem-radar independently suffered the *identical* failure shape (a
correctly-created baseline flag, never read by the display/aggregation
layer) with zero cross-citation — suggesting the flag-exists-but-isn't-
checked failure mode is structural, not incidental.

**Independent lineages**: watch-clank and oem-radar independent of each
other (same bug, no citation). feature-phone-clank explicitly inherited
from smartphone-clank's incident.

**Key citations**: `watch-clank/app/services/editorial.py:70-92`,
`watch-clank/ai/handoff/INCIDENT_EPOCH1_FRESHNESS.md`,
`oem-radar/docs/CURRENT_STATUS.md:12-26`, `feature-phone-clank/src/feature_phone_clank/core/scope.py:1-9`.

**Question for ZLM**: is there a standardizable *query-level* contract
here (e.g. "the default/active view query must exclude baseline-tagged
records by construction"), given the same bug recurred independently
twice with the same fix shape (a shared exclusion predicate)?

---

## 3. Coarse Identity Keys Falsely Merging Distinct Entities

**Claim to test**: a key built for candidate-surfacing gets used as a
confident identity match, silently merging two distinct real-world
entities.

**Strongest evidence FOR**: four independent, dated incidents across four
repos with the same root shape — oem-radar (recurred twice, same bug
class, different code), feature-phone-clank, tablet-clank (48 false
events), semiconductor-intelligence (the most severe: a merged-entity
artifact became the highest-scored "story" in the database, motivating a
full architectural rebuild).

**Strongest evidence AGAINST**: watch-clank's conservative,
evidence-gated allowlist policy has produced zero confirmed false-merge
incidents — a working counter-model (accept less automatic matching, in
exchange for correctness).

**Independent lineages**: all four incidents independent, no
cross-citation. oem-radar's fix (confidence-scored cascade) and
semiconductor-intelligence's fix (proposal-layer + independence grouping)
are structurally different solutions to the same problem.

**Key citations**: `oem-radar/docs/STAGE8.md:65-86`,
`oem-radar/docs/EVIDENCE_ARCHITECTURE.md:122-135`,
`tablet-clank/docs/ARCHITECTURE.md:35`,
`semiconductor-intelligence/PHASE0_AUDIT.md §3`.

**Question for ZLM**: is chinese-tech-wire's stated philosophy ("false
merges are worse than missed merges") adoptable as a fleet-wide default
posture, given every repo that violated it was burned and every repo that
followed a conservative variant of it wasn't?

---

## 4. Availability/Lifecycle Facts Need an Honest Data Model

**Claim to test**: a UI/operator-facing promise about availability or
release-state honesty must be backed by an actual data field, not just
text.

**Strongest evidence FOR (that the gap is real)**: smartphone-clank's
dossier hardcodes the literal string `"unknown"` for release state with
**no backing field anywhere in the schema** — a semantic guarantee
implemented entirely as decoration.

**Strongest evidence AGAINST (that it's solvable / already solved
elsewhere)**: smartwatch-clank's equivalent disclaimer *is* backed by a
real enum set that structurally cannot assert unavailability from
absence — proof the same promise can be made honestly.

**Independent lineages**: this cluster also **corrects a standing
assumption** from prior UI-domain work — the shared `OUT_OF_STOCK` QC
vocabulary was assumed to have one lineage (watch-clank) across
feature-phone-clank and tablet-clank; this pass found tablet-clank's is
actually inherited from **korean-tech-wire**, not watch-clank. In both
lineages, the vocabulary was copied but the underlying data model was
not.

**Key citations**: `smartphone-clank/docs/KNOWN_LIMITATIONS.md:6`,
`smartphone-clank/dashboard/templates/dossier.html:20`,
`smartwatch-clank/intelligence/samsung.py:11-24`,
`tablet-clank/storage/qc_archive.py:1-21` (lineage correction),
`standards-clank/decisions/0009-pass3-sku-001-decision.md` (the standing
assumption this corrects).

**Question for ZLM**: is smartphone-clank's dossier badge a defect
worth flagging for remediation, or an acceptable honest placeholder?
Separately: should `decisions/0009`'s lineage description be
corrected/annotated given this finding? (That's a UI-domain document —
flagging for the operator's decision, not this pass's to make.)

---

## 5. Evidence/Provenance Granularity (Fact / Change / Decision Tiers)

**Claim to test**: a fact must be traceable at fact-level, change-level,
and operator-decision-level provenance, as three distinct tiers.

**Strongest evidence FOR**: near-universal independent convergence on a
3-5 tier model across 8 of 9 Clanks; chinese-tech-wire's
`EXPLAINABILITY_CONTRACT.md` and semiconductor-intelligence's
Claim/Evidence/ClaimEvent stack are both mature enough to function as
templates in their own right.

**Strongest evidence AGAINST (collapse risk)**: oem-radar's Stage 11
incident — evidence observations flooded the canonical change-event
table (44.6% of "alerts"), burying real signal, before being split back
into a separate table in Stage 11.1.

**Independent lineages**: no cross-repo citation for any specific
implementation; convergent design, not copying.

**Key citations**: `chinese-tech-wire/docs/EXPLAINABILITY_CONTRACT.md`,
`semiconductor-intelligence/semi_intel/domain/models.py:207-303`,
`oem-radar/docs/EVIDENCE_ARCHITECTURE.md:82-104`,
`diagnostic-clank/clank-runtime/src/clank_runtime/contracts/events.py:1-56`
(unwritten `EventEnvelope` draft).

**Question for ZLM**: is diagnostic-clank's draft `EventEnvelope` (already
a synthesis of what most repos independently built pieces of) worth
adopting/adapting as the fleet-wide shape?

---

## 6. Timestamp/Ordering-Shaped Values Mistaken for Chronological Truth

**Claim to test**: a value that merely looks like a temporal/ordering
signal (an editorial `updated_at`, a row's insertion-order UUID, a single
scheduler firing) gets used as validated chronological/causal truth
without checking it actually carries that meaning.

**Strongest evidence FOR**: four independent, differently-shaped
occurrences across four unrelated codebases (smartwatch-clank's
firmware-timestamp bug — 23 false events, still unfixed;
semiconductor-intelligence's origin-selection-by-id bug; a
clank-fleet adapter's UUID-lexical-ordering bug; an agent's
single-fire-mistaken-for-cadence-proof incident).

**Strongest evidence AGAINST**: none — but also no general defense
exists anywhere in the fleet; every fix was point-specific.

**Independent lineages**: fully independent, four different contexts, no
shared code.

**Key citations**: `smartwatch-clank/docs/coros-updates-firmware-version-adjudication-2026-08-30.md`,
`semiconductor-intelligence/semi_intel/signals/independence.py:181-194`,
`diagnostic-clank/clank-fleet/tests/test_m15_adapter_truth.py:1-11,63-135`.

**Question for ZLM**: is this coherent enough to standardize (a general
"never derive precedence/origin/recency from an unvalidated
timestamp-shaped or ordering-shaped field" rule), or is it better handled
as a testing-practice recommendation (adversarial fixtures like
`uuid_trap_db`) rather than a data-ontology standard?

---

## 7. Same Real-World Entity Discovered by Multiple Clanks

**Claim to test**: there is currently no fleet-level mechanism for
recognizing when two different Clanks discover the same real-world
entity — this is an explicitly open architecture question.

**Strongest evidence FOR treating this as urgent**: clank-architecture's
own `RISK_REGISTER`/`GOLDEN_INCIDENTS` registers `CROSS-CLANK-IDENTITY` as
an open issue with **no fixture yet**, and states no silent merge should
happen before an identity ADR exists.

**Strongest evidence AGAINST building anything now**: diagnostic-clank's
ADR-0002 explicitly records `DO_NOT_STANDARDISE` as an adopted position —
no central product identity service, by design. Any solution here must
work within that constraint or make an explicit case to revisit it.

**Independent lineages**: n/a — fleet-level gap, not a per-Clank pattern.

**Key citations**: `clank-architecture/conformance/GOLDEN_INCIDENTS.md:31`,
`diagnostic-clank/docs/adr/0002-adapters-not-schema-unification.md`,
`clank-architecture/adr/0014-typed-evidence-and-lane-config.md`.

**Question for ZLM**: should this even be in scope for a data-ontology
standard given the explicit prior `DO_NOT_STANDARDISE` decision, or should
Pass 0B recommend deferring it until/unless ADR-0014 (semantic
clocks/typed evidence — a prerequisite for comparing facts across
Clanks at all) is itself adjudicated?

---

## Not included above (see clusters/ for full detail)

MEDIUM priority: unknown-absent-vs-false (well-solved already, likely low
marginal value to standardize), canonical-fact-overwrite-discipline
(real inconsistency found but no confirmed harm), confidence-and-certainty-semantics
(good evidence, thinner incident backing), editorial-freshness-vs-novelty
(profile-scoped, likely news-family-only), regional-variant-identity
(every repo that's touched it says it's unresolved — needs more evidence,
not adjudication, first).

LOW priority: source-disagreement-representation (one implementation,
zero incidents, cannot tell if this is a non-issue or an unmeasured gap).
