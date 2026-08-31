# Candidate card C2 — Novelty read-side exclusion

- **Candidate name:** Novelty read-side exclusion (first-seen ≠ new-in-the-world)
- **Plain-language invariant:** A record's first appearance in a Clank's database is not evidence the thing is new in the world; and any default/active view that consumes novelty must exclude baseline/continuity-tagged records by construction (read-side predicate), the same structural shape COM-003 mandates for QC queues.
- **Exact semantic distinction:** FIRST_SEEN_BY_CLANK (local observation time) ≠ NEW_REFERENCE/NEW_TO_MARKET (world novelty); editorial freshness is a further, family-scoped distinction (news-family corollary), never implied by either.
- **Trigger/applicability:** Clanks whose default novelty/alerting views are derived from local history. Catalogue/history views that legitimately include baseline records are out of scope.
- **Strongest evidence:** watch editorial.py:70-92 ("merely absent from this database until today is not evidence the manufacturer launched it today"; alert body marks novelty UNCONFIRMED); diagnostic-clank knowledge law FIRST_SEEN_BY_CLANK != NEW_TO_MARKET; feature-phone baseline-gates-every-event-type, inherited from smartphone's 73-device contamination incident.
- **Strongest counterevidence:** none against the principle; the operative finding is the RECURRENCE — watch and oem-radar independently suffered the identical failure (baseline flag written, never read by the aggregation query).
- **Independent lineages:** watch and oem-radar independent (same bug, zero citation); feature-phone inherited from smartphone's incident; corollary terminology (GIC-01/Fleet Law 2) from clank-architecture.
- **Known incident support:** INCIDENT_EPOCH1_FRESHNESS (watch); oem-radar CURRENT_STATUS baseline-flag-unread; smartphone pollution (inherited).
- **Likely failure if violated:** false novelty alerts at fleet scale; editorial time wasted on known items; loss of trust in "new" as a category.
- **Likely implementation freedom:** how the tag is stored (epoch membership, is_baseline flag, freshness state), how the exclusion predicate is expressed, UI presentation.
- **Evidence strength:** STRONG. **Impact:** HIGH. **Standardization risk:** LOW (mirrors ratified COM-003's read-side-exclusion shape).
- **Recommendation: ADVANCE** — the query-level read-side exclusion contract is the standardizable core; editorial freshness rides as a news-family corollary.

## Counterexample test

**Strongest plausible counterexample:** "A catalogue-only Clank has no notion of editorial freshness and legitimately shows baseline records in its default view — the invariant fails there."

**Does the candidate still hold?** YES, narrowed: the exclusion binds views that *consume novelty* (alerts, new-item feeds, editorial queues), not catalogue/history views — which SHOULD show baseline records. Also, korean-tech-wire has no baseline concept at all: for such Clanks the trigger is unmet, not violated. Survives.
