# Candidate card C3 - Identity conservatism

- **Candidate name:** Identity conservatism (false merges are worse than missed merges)
- **Plain-language invariant:** Default identity posture must prefer a missed merge to a false merge; an automatic merge must be evidence-gated, auditable, and reversible.
- **Exact semantic distinction:** a candidate/surfacing key (used to propose matches) is not an identity assertion (a committed merge); and a committed merge is not an irreversible fact.
- **Trigger/applicability:** any Clank that merges records from multiple sources/observations into canonical entities.
- **Strongest evidence:** four independent dated incidents - oem-radar (twice, same class), feature-phone-clank, tablet-clank (48 false events), semiconductor-intelligence (merged-entity artifact became the database's top-scored story; forced architectural rebuild). Counter-model: watch-clank's evidence-gated allowlist - zero false merges.
- **Strongest counterevidence:** aggressive matching is sometimes the product (oem-radar's confidence-scored cascade, semi-int's proposal-layer); a blanket conservatism rule would forbid legitimate designs.
- **Independent lineages:** all four incidents independent, no cross-citation; fixes structurally different (cascade vs proposal-layer vs allowlist).
- **Known incident support:** oem-radar STAGE8:65-86; oem-radar EVIDENCE_ARCHITECTURE:122-135; tablet-clank ARCHITECTURE:35; semiconductor-intelligence PHASE0_AUDIT section 3.
- **Likely failure if violated:** silently merged distinct entities corrupt canonical state and every downstream alert/decision; severity observed up to full rebuild.
- **Likely implementation freedom:** key design, scoring, cascade thresholds, storage of merge provenance.
- **Evidence strength:** STRONG. **Impact:** HIGH. **Standardization risk:** MED (must stay posture/consequence-level, never prescribe algorithms).
- **Recommendation: ADVANCE** - posture + reversibility/auditability invariant, algorithm-neutral.

## Counterexample test

**Strongest plausible counterexample:** "Two sources report the same product with trivially different model numbers; strict conservatism misses a real merge forever, and the operator never sees it - conservatism has a cost too."

**Does the candidate still hold?** YES, narrowed: the invariant does not ban merges - it bans ungated, unauditable, irreversible ones. A missed merge surfaces as a duplicate (visible, benign); a false merge corrupts canon silently (invisible, severe). The asymmetry justifies the default posture; the proposal-layer pattern (propose aggressively, commit conservatively, review) conforms. Survives.
