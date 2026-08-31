# Pass 0B — HOLD and REJECT cards

> **Disposition (2026-08-31, operator-delegated triage):** every card
> below has been ruled on — see
> [../../holds-disposition.md](../../holds-disposition.md). Outcomes:
> honest-unknown, cross-Clank identity, confidence-and-certainty,
> canonical-overwrite, and regional-variant identity → **DEFER BEYOND
> V1**; timestamp-shaped values → **REHOME** (diagnostic/testing
> practice, confirmed); source-disagreement → **REJECT** (stands).
> The cards below are preserved unmodified as the Pass 0B record.

## HOLD — Honest-unknown / availability-honesty backing (absorbs cluster 4 remainder + unknown-absent-vs-false)
- **Invariant (candidate):** an operator-facing semantic guarantee ("we do not infer X") must be backed by queryable state, not presentation-only text; unknown/absence states (unknown, missing, null, not_applicable) must stay distinct from positive/negative facts (unavailable, out_of_stock, not_launched).
- **Why HOLD:** the contrast is proven (smartphone's presentation-only release-state badge vs smartwatch-clank's real enum backing) but there is no incident and only one defect instance; the gap audit already rehomed "honest unknown" to DATA/ONTOLOGY. Revisit when the smartphone backlog is dispositioned or a second instance appears.
- **Recommendation: HOLD.**

## HOLD/DEFER — Cross-Clank entity identity (cluster 7)
- Blocked twice over: ADR-0002 `DO_NOT_STANDARDISE` (adopted — no central identity service) and ADR-0014 (semantic clocks/typed evidence), which is a prerequisite for cross-Clank fact comparison and is itself unadjudicated.
- **Recommendation: HOLD/DEFER** until ADR-0014 is adjudicated; the risk stays registered in clank-architecture's RISK_REGISTER, which is its proper home.

## HOLD — Confidence-and-certainty semantics
- Good evidence of convergent confidence fields (watch confidence_score/data_completeness, smartphone confidence + ledger drift check, oem-radar confidence fields) but thinner incident backing; likely folds into a provenance-tiers or ontology standard at drafting time.
- **Recommendation: HOLD.**

## HOLD — Canonical fact overwrite discipline
- Real inconsistency found (canonical state overwriting conflicting observations) but no confirmed operator harm; likely subsumed by C5 (tier separation + traceability) at drafting time.
- **Recommendation: HOLD** pending C5 drafting.

## HOLD — Regional variant identity
- Every repo that touched it reports it unresolved; evidence is not yet sufficient to adjudicate.
- **Recommendation: HOLD** — needs evidence, not a ruling.

## REJECT → REHOME — Timestamp-shaped values (cluster 6)
- Four independent incidents but the general rule degenerates to engineering practice ("validate that a field carries the semantics you use it for before using it"). The transferable artifact is the adversarial-fixture pattern (`uuid_trap_db`).
- **Recommendation: REJECT as a data-ontology standard; REHOME to diagnostic/testing practice.**

## REJECT — Source-disagreement representation
- One implementation, zero incidents, no way to tell a non-issue from an unmeasured gap.
- **Recommendation: REJECT** (may resurface with evidence).
