# Data/Ontology Pass 0B — Adversarial Adjudication (2026-08-31)

Adjudicates the seven HIGH-priority clusters from the Pass 0A handoff
([handoff.md](handoff.md)) against the evidence package
([evidence-log.md](evidence-log.md), [clusters/](clusters/),
[incident-ledger.md](incident-ledger.md)). Standing context applied
throughout: clank-architecture **ADR-0006** (continuity/epoch, PROPOSED),
**ADR-0014** (typed evidence/semantic clocks, PROPOSED), and **ADR-0002**
(`DO_NOT_STANDARDISE` — no schema unification, no central identity
service, adopted).

Method: every cluster assumed guilty until proven useful; claims
spot-checked where load-bearing (smartphone dossier decoration and
KNOWN_LIMITATIONS note, tablet qc_archive lineage header, watch TIMEX
incident files — all verified). No target repo was modified; Pass 0A
evidence is unmodified. No standard drafts, no normative wording.

## Adjudication table

| # | Cluster | Disposition | Evidence | Impact | Risk |
|---|---|---|---|---|---|
| 1 | Baseline/epoch continuity after data loss | **KEEP DISTINCT** (+ split: live operational exposure → operator flag) | STRONG | HIGH | LOW-MED |
| 2 | "New to us" vs "new in the world" + query-level contract | **KEEP DISTINCT** (+ folds in the editorial-freshness corollary) | STRONG | HIGH | LOW |
| 3 | Coarse identity keys falsely merging entities | **KEEP DISTINCT** | STRONG | HIGH | MED |
| 4 | Availability/lifecycle honesty backing | **SPLIT** (lineage correction → operator flag; smartphone badge → product backlog; general invariant → folds into the honest-unknown candidate) | MODERATE | MEDIUM | LOW |
| 5 | Evidence/provenance granularity (fact/change/decision tiers) | **KEEP DISTINCT** (the envelope-shape prescription is explicitly out of scope) | STRONG | HIGH | MED |
| 6 | Timestamp-shaped values mistaken for chronological truth | **REHOME** (to diagnostic/testing practice; the standard form is rejected) | STRONG | MED | HIGH |
| 7 | Cross-Clank entity identity | **HOLD / DEFER** (blocked by ADR-0002 `DO_NOT_STANDARDISE`; prerequisite ADR-0014 unadjudicated) | MODERATE | HIGH (future) | HIGH (now) |

MEDIUM/LOW clusters: editorial-freshness-vs-novelty → folded into #2;
unknown-absent-vs-false → folded into the honest-unknown HOLD candidate;
confidence-and-certainty-semantics → HOLD; canonical-fact-overwrite-
discipline → HOLD (likely folds into a provenance-tiers standard at
drafting time); regional-variant-identity → HOLD (needs more evidence
before adjudication is possible); source-disagreement-representation →
REJECT (one implementation, zero incidents, insufficient evidence).

## Per-cluster adjudication

### 1. Baseline/epoch continuity — KEEP DISTINCT, ADVANCE

One concept, not several: the invariant is that a **data discontinuity
(loss, restore, re-baseline) must itself be an explicit, queryable fact**.
Evidence is the strongest in the package: four independent
implementations (watch OperationalEpoch, oem-radar doc-procedure,
feature-phone + smartwatch `core/continuity.py`), one severe incident
(TIMEX catalogue backfill burst), and a near-complete unratified draft
(ADR-0006) that smartwatch-clank already builds against. This is a
DATA/ONTOLOGY concern, not Operations: the standardizable object is the
*representation and read-side treatment of discontinuity*, not the backup
procedures around it.

**Split:** watch-clank's empty production `operational_epochs` table +
manual `--force-baseline` dependence is a live OPERATIONAL exposure, not
standardization evidence — flagged to the operator separately (below).
Answer to the handoff question: **yes, adopt/adapt ADR-0006's contract as
the fleet-wide candidate baseline (Pass 1 starting text), and yes, the
watch exposure warrants an out-of-band operator alert now** — a standing
novelty-integrity risk should not wait for a standards cycle.

### 2. First-seen vs novelty + the read-side contract — KEEP DISTINCT, ADVANCE

The decisive adjudication: the semantic distinction ("first_seen is local
observation time, never novelty") is necessary but **already proven
insufficient** — watch-clank and oem-radar independently suffered the
identical failure shape (baseline flag correctly written, never read by
the display/aggregation query) with zero cross-citation. A representation-
only invariant would have been conformed-to by both repos while the bug
persisted. Therefore the standardizable core is the **query-level
contract**: any default/active view that consumes novelty (alerting,
new-item feeds) must exclude baseline/continuity-tagged records *by
construction* (read-side predicate), the same structural shape the fleet
already ratified for QC queues in COM-003. Editorial-freshness-vs-novelty
(MEDIUM) folds in as a news-family-scoped corollary of the same read-side
rule. Counterexample-tested below.

### 3. Coarse identity keys — KEEP DISTINCT, ADVANCE

Four independent, dated incidents across four repos, escalating in
severity (semiconductor-intelligence's merged-entity artifact became the
database's top-scored "story" and forced an architectural rebuild), and a
working counter-model (watch-clank's conservative evidence-gated
allowlist: zero false merges). Adoptable fleet posture: **false merges
are worse than missed merges** (chinese-tech-wire's stated philosophy,
independently validated by every repo that violated it being burned).
Implementation-neutral scoping: the invariant constrains *consequence*
(default conservative posture; automatic merges must be evidence-gated,
auditable, and reversible), never the matching algorithm — which keeps
semiconductor-intelligence's gated proposal-layer and watch's allowlist
both conformant.

### 4. Availability honesty backing — SPLIT, HOLD

Three parts, three homes. (a) **Lineage correction**: tablet-clank's
QC archive is modeled on korean-tech-wire, not watch-clank — verified
from the file header. This corrects a standing assumption recorded in
decisions/0009; decisions are append-only governance records, so the
correction is **flagged for the operator** to annotate (UI-domain
document, not this pass's to rewrite). (b) **Smartphone badge**: the
"unknown — not inferred from novelty" release-state badge is decoration
with no backing field (verified: dossier.html:20; KNOWN_LIMITATIONS.md
honestly documents it). It is not a violation of any ratified standard —
flagged to the operator as smartphone product backlog; note it exhibits
the same "guarantee exists but nothing backs it" structural shape as
cluster 2. (c) **General invariant** ("an operator-facing semantic
guarantee must be backed by queryable state") merges into the
honest-unknown HOLD candidate, with smartwatch-clank's real-enum backing
as proof the promise can be made honestly. MODERATE evidence, no
incident — HOLD is correct.

### 5. Provenance tier separation — KEEP DISTINCT, ADVANCE

Eight of nine Clanks independently converged on 3–5 tier
observation→fact→change→decision stacks without cross-citation — the
strongest convergence in the package — and oem-radar's Stage 11 incident
(evidence rows flooding the canonical change table to 44.6% of "alerts")
is the incident that proves tier COLLAPSE is the harm mode. The
standardizable invariant is **separation + traceability** (observations,
canonical facts/changes, and operator decisions remain distinct record
kinds; every canonical fact/change traceable to supporting observations;
every operator decision traceable to the state it was made against),
explicitly **not** any prescribed envelope shape. COM-002's provenance
snapshot is the decision-tier instance of this and remains untouched.
Answer to the handoff question: diagnostic-clank's draft `EventEnvelope`
is worth studying as a Pass 1 reference, but recommending a fleet-wide
shape now would trespass on ADR-0002's adopted anti-unification position.

### 6. Timestamp-shaped values — REJECT as standard, REHOME

Four fully independent incidents (23 false firmware events; wrong origin
selection; UUID-lexical ordering; single-fire-as-cadence), but the
adversarial test kills it: every counterexample ("editorial `updated_at`
is the *correct* field for last-edited recency display — COM-010 already
requires labeling it") shows the rule reduces to "check that a field
means what you're using it for before using it," which is engineering/
testing practice, not an ontological invariant. No general defense exists
anywhere in the fleet; the fixes were point-specific; a fleet-wide rule
would be unfalsifiable as stated. Standardization risk HIGH → fails the
advancement rule. **REHOME** to diagnostic/testing practice: the
adversarial-fixture pattern (`uuid_trap_db`) is the transferable artifact.

### 7. Cross-Clank entity identity — HOLD / DEFER

Explicitly blocked twice over: ADR-0002's adopted `DO_NOT_STANDARDISE`
position forbids the central identity service any solution would imply,
and ADR-0014 (semantic clocks/typed evidence) is a prerequisite for
comparing facts across Clanks at all — it is itself unadjudicated. The
open risk is real (clank-architecture's RISK_REGISTER flags
CROSS-CLANK-IDENTITY with no fixture), so it stays visible, but Pass 0B
recommends **deferring** this cluster until ADR-0014 is adjudicated. Not
a Standards Clank data-ontology candidate in this tranche.

## Advancement summary

| Candidate | Recommendation | Evidence | Impact | Risk |
|---|---|---|---|---|
| C1 — Continuity/epoch explicitness (adopt/adapt ADR-0006) | **ADVANCE** | STRONG | HIGH | LOW-MED |
| C2 — Novelty read-side exclusion contract (+ freshness corollary) | **ADVANCE** | STRONG | HIGH | LOW |
| C3 — Identity conservatism + reversible, auditable merges | **ADVANCE** | STRONG | HIGH | MED |
| C5 — Provenance tier separation + traceability | **ADVANCE** | STRONG | HIGH | MED |
| C4 — Honest-unknown backing (incl. availability honesty) | HOLD | MODERATE | MEDIUM | LOW |
| C7 — Cross-Clank identity | HOLD/DEFER | MODERATE | HIGH | HIGH |
| Confidence-and-certainty / canonical-overwrite / regional-variant | HOLD | MOD–WEAK | MED–LOW | — |
| C6 — Timestamp-shaped values | REJECT → diagnostic/testing practice | STRONG | MED | HIGH |
| Source-disagreement representation | REJECT | WEAK | LOW | — |

Strongest surviving invariant: **C2** (the read-side novelty-exclusion
contract — twice-recurred identical failure, incident-inherited across
three repos, and structurally mirrors the already-ratified COM-003
shape). Weakest surviving invariant: **C1's operational annex** (the
watch exposure) is severe but is an ops flag, not the standard itself.

## Flags requiring operator action (out of this pass's authority)

1. **watch-clank live exposure**: production `operational_epochs` table
   empty; baseline protection rests on a manual flag; three proposed
   remediations unimplemented (Pass 0A, cluster 1). Recommend out-of-band
   alert now.
2. **decisions/0009 lineage annotation**: tablet-clank's QC-archive
   lineage is korean-tech-wire, not watch-clank (verified). Append a
   correction note to the UI-domain decision record.
3. **smartphone-clank release-state badge**: decoration without backing
   field — candidate product backlog (honest today, fragile if inference
   is ever added).
