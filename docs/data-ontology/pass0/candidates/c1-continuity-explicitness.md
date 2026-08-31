# Candidate card C1 — Continuity/epoch explicitness

- **Candidate name:** Continuity/epoch explicitness
- **Plain-language invariant:** A discontinuity in a Clank's data (loss, restore, re-baseline) must itself be an explicit, queryable fact — never silently treated as "nothing happened" or as fresh discovery.
- **Exact semantic distinction:** continuity state (epochs/gaps) is a first-class fact about the dataset's timeline, distinct from both the records themselves and from novelty judgements made from those records.
- **Trigger/applicability:** any Clank that derives novelty, alerts, or editorial state from its own local history (i.e., persistent Clanks with a concept of "seen before"). A purely stateless Clank is out of scope.
- **Strongest evidence:** four independent implementations (watch OperationalEpoch; oem-radar documented cutover; feature-phone + smartwatch core/continuity.py) + near-complete draft ADR-0006 that smartwatch already builds against + TIMEX catalogue backfill burst incident.
- **Strongest counterevidence:** watch-clank's production epoch table is empty — the mechanism exists but is unused at the point it matters (an adoption/exposure problem, not a falsification).
- **Independent lineages:** watch, oem-radar, feature-phone independent; smartwatch inherited from ADR-0006.
- **Known incident support:** INCIDENT_TIMEX_CATALOGUE_BACKFILL_BURST (baseline-protected records re-alerted as fresh after restore/backfill).
- **Likely failure if violated:** post-restore/backfill false novelty bursts; silent loss of "we resynced everything" context; editorial decisions made on corrupted continuity.
- **Likely implementation freedom:** epoch representation (table/marker file/flagged records), promotion workflow, alerting integration — all free.
- **Evidence strength:** STRONG. **Impact:** HIGH. **Standardization risk:** LOW-MED (ADR-0006 template exists; adoption effort is the cost).
- **Recommendation: ADVANCE** — adopt/adapt ADR-0006 as the Pass 1 starting contract.

## Counterexample test

**Strongest plausible counterexample:** "An append-only Clank with no novelty logic (e.g., a pure evidence archive) has no epochs and needs none — the invariant is untestable there."

**Does the candidate still hold?** YES, narrowed: the trigger applies only where novelty/alerting is derived from local history. For that narrowed scope the invariant holds in every surveyed implementation and every incident. A Clank that cannot lose or restore data does not exist in this fleet; a Clank that can, and derives novelty, needs explicit continuity. Survives.
