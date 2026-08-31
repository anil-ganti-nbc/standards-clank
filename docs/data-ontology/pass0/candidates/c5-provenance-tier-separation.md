# Candidate card C5 — Provenance tier separation

- **Candidate name:** Provenance tier separation (observation / fact / change / decision)
- **Plain-language invariant:** Observations, canonical facts/changes, and operator decisions remain distinct record kinds — collapse causes signal burial — and every canonical fact/change stays traceable to its supporting observations, every decision to the state it was made against.
- **Exact semantic distinction:** a raw observation is not a canonical fact; a canonical change is not an operator decision. Tiers may be 3–5 depending on the Clank; the invariant binds separation and traceability, not the tier count or shapes.
- **Trigger/applicability:** any Clank with both ingested observations and derived canonical state (8 of 9 surveyed have exactly this).
- **Strongest evidence:** near-universal independent convergence on 3–5 tier models across 8/9 Clanks with zero cross-citation; oem-radar Stage 11 incident — evidence observations flooded the canonical change-event table to 44.6% of "alerts", burying real signal, until split back out; chinese-tech-wire EXPLAINABILITY_CONTRACT and semi-int Claim/Evidence stack function as mature templates.
- **Strongest counterevidence:** tiny Clanks legitimately keep observations and changes in one table — but the harm mode (review/alerting consuming unreviewed observations) is exactly what collapsed at oem-radar.
- **Independent lineages:** convergent design, no cross-repo citation for any implementation.
- **Known incident support:** oem-radar Stage 11 / EVIDENCE_ARCHITECTURE.md:82-104.
- **Likely failure if violated:** evidence floods change/alert surfaces; provenance becomes unreconstructable; review volume becomes noise.
- **Likely implementation freedom:** tier count (3–5), storage shapes, envelope formats (diagnostic-clank's draft EventEnvelope is a Pass 1 reference only — explicitly not prescribed; ADR-0002 anti-unification respected).
- **Evidence strength:** STRONG. **Impact:** HIGH. **Standardization risk:** MED (creep toward shape prescription must be resisted).
- **Recommendation: ADVANCE** — separation + traceability invariant; shapes stay free.

## Counterexample test

**Strongest plausible counterexample:** "A single-collector Clank appends everything to one ledger and has never had a burial problem — the tier mandate is ceremony."

**Does the candidate still hold?** YES, narrowed: the invariant requires that observation records and canonical change records be *distinguishable and separately consumable* — separate tables are the common mechanism, not the requirement; and the traceability half (canonical fact → supporting observations) already holds in any Clank that keeps evidence at all. A Clank with no derived canonical state is out of scope by trigger. Survives.
