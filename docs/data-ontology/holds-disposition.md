# Data/Ontology — Disposition of the Pass 0B HOLD/REHOME set (2026-08-31)

Operator-delegated candidate triage (this is candidate-backlog
disposition, not ratification: no normative standard is created, altered,
or retired by this document). Ruled against the four now-RATIFIED
DATA standards (COM-001 v1, COM-002 v2, COM-003 v2, COM-004 v1; ratification
closure `4407654`) and the accumulated Pass 0A/0B/1/2/3 evidence.

## Disposition summary

| Concern (Pass 0B origin) | Disposition |
|---|---|
| Honest-unknown / availability-honesty backing (cluster 4 remainder + unknown-absent-vs-false) | **DEFER BEYOND V1** |
| Cross-Clank entity identity (cluster 7) | **DEFER BEYOND V1** |
| Confidence-and-certainty semantics (MEDIUM cluster) | **DEFER BEYOND V1** |
| Canonical fact overwrite discipline (MEDIUM cluster) | **DEFER BEYOND V1** |
| Regional variant identity (MEDIUM cluster) | **DEFER BEYOND V1** |
| Timestamp-shaped values (cluster 6) | **REHOME** (confirmed: diagnostic/testing practice) |
| Source-disagreement representation (LOW cluster) | **REJECT** (stands) |

**Zero concerns advance into a DATA v1 baseline.** The ratified four
already cover every STRONG-evidence concern the fleet surfaced; the held
set is uniformly MODERATE-or-weaker evidence, and a v1 baseline should
freeze the proven core — not perimeter growth. This mirrors the final UI
gap audit's conclusion discipline.

## Per-concern rulings

### 1. Honest-unknown / availability-honesty backing — DEFER BEYOND V1

The strongest held concern, and still not strong enough for V1. Evidence:
one decoration-backed guarantee instance (smartphone-clank's release-state
badge with no backing field, KNOWN_LIMITATIONS.md:4/6) against one honest
counter-model (smartwatch-clank's enum backing), plus the fleet-wide
never-invent pattern (oem-radar's UNKNOWN non-transition, tablet's
MANUAL_UNDATED, watch/smartphone "not inferred from novelty"). No incident
has ever been caused by the gap. Partial coverage already ratified:
COM-004 acceptance 4 (inferred/derived values distinguishable from
source-explicit claims) covers the record-layer slice; the uncovered
remainder is the "presentation-only guarantee" slice, which is
smartphone-specific today. Promotion trigger: a second independent
instance, an incident, or disposition of the smartphone backlog into a
backed field. Until then it stays smartphone product backlog.

### 2. Cross-Clank entity identity — DEFER BEYOND V1

Unchanged from Pass 0B: doubly blocked (clank-architecture ADR-0002
`DO_NOT_STANDARDISE` is an adopted position; ADR-0014 semantic clocks/typed
evidence — the prerequisite for comparing facts across Clanks — is itself
unadjudicated), and the risk remains properly registered in
clank-architecture's RISK_REGISTER (CROSS-CLANK-IDENTITY). Nothing in the
DATA v1 ratification changes either blocker. Promotion trigger:
adjudication of ADR-0014, or a concrete cross-Clank collision incident.

### 3. Confidence-and-certainty semantics — DEFER BEYOND V1

Convergent practice (confidence/certainty fields in watch, smartphone,
oem-radar, tablet, feature-phone) with thinner incident backing. Partial
coverage now ratified: COM-004's inferred-vs-source-explicit
distinguishability clause already binds the record-layer slice (a
confidence value IS a derived value). The uncovered remainder — semantic
labeling of what a confidence figure is *of*, and certainty-vocabulary
uniformity — has no incident and no two independent failure lines.
Promotion trigger: an operator misreading confidence across Clanks, or a
second QC-vocabulary harmonization pass.

### 4. Canonical fact overwrite discipline — DEFER BEYOND V1

The ratification of COM-004 absorbed most of this: tier separation +
full traceability means an overwrite of canonical state remains
traceable to the observations and decisions behind it. The unresolved
sliver — whether a *conflicting* observation must be recorded as a
conflict event when canon moves — has one reported inconsistency and zero
confirmed harm. Likely folds into a future COM-004 revision if harm ever
surfaces. Promotion trigger: a documented overwrite-induced provenance
loss.

### 5. Regional variant identity — DEFER BEYOND V1

Unchanged from Pass 0B: every repo that touched it reports it unresolved
(oem-radar treats per-config truth as load-bearing; watch-clank's Regional
Matrix is a specialist UI surface; COM-003 v2 explicitly declines to
choose between regional-split and regional-attached architectures).
Needs operational evidence — a real false-merge/false-split across
regions — before a ruling is possible. COM-003's evidence/reversibility
discipline already governs any merge decision in this space in the
meantime.

### 6. Timestamp-shaped values — REHOME (stands)

REJECT as a data-ontology standard (four incidents, but the general rule
degenerates to engineering practice: "validate that a field carries the
semantics you use it for"). The transferable artifact — adversarial
fixtures like `uuid_trap_db` — is rehomed to diagnostic/testing practice,
which is where it belongs. No DATA v1 action.

### 7. Source-disagreement representation — REJECT (stands)

One implementation, zero incidents, no way to distinguish a non-issue
from an unmeasured gap. Rejected at Pass 0B; nothing since changes it. If
a Clank ever needs to represent conflicting sources, it will — and the
concern can return with evidence.

## What would reopen this document

- A second independent instance or a first incident for any DEFERred
  concern (most likely candidates: honest-unknown, confidence semantics).
- Adjudication of clank-architecture ADR-0014 (reopens #2).
- Disposition of smartphone-clank's release-state badge backlog
  (reopens #1's strongest instance).
