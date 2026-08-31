# Operations Pass 0B — HOLD, REHOME, and DEFER cards

## DEFER — Destructive production action authority (cluster 10)

- **Concern:** a destructive mutation against production state must never proceed on a naming-pattern guess; identity positively resolved, backup proven, authority explicit.
- **Evidence:** STRONG and catastrophic — INC-041 (total, unrecoverable production data loss, feature-phone-clank, agent-caused) and INC-036 (same root cause, smartwatch-clank, partial loss, stale-backup recovery) one week apart.
- **Disposition: DEFER to clank-architecture ADR-0009 as the sole governing contract.** ADR-0009's 8-step contract (DISCOVER → RESOLVE IDENTITY → CLASSIFY → PROVE BACKUP → DISPLAY TARGET → AUTHORISE → MUTATE → VERIFY) is complete, reviewed, and was written in direct response to these exact incidents; a Standards Clank restatement would be a competing authority for zero marginal safety. The runtime/architecture governance home is clank-architecture's.
- **Operator flags (outside this pass's authority):**
  1. ADR-0009 is still `PROPOSED — REVIEWED DRAFT` despite post-dating both incidents — consider activating it out-of-band.
  2. Both real incidents were *agent-performed* operations — consider whether ADR-0009 should name agent-executed destructive actions as an explicit risk class.

## REHOME — Deployment truth + configuration drift (clusters 8 + 9 + MEDIUM #12)

- **Merged concern:** deployed-state truth — the code revision, configuration, and wiring actually present on each runtime host must be verifiable against intent, with divergence (config drift, missed hosts, stale wrappers, un-migrated schema gates) detectable rather than discovered by accident.
- **Evidence:** the broadest-repo-count cluster in the survey (8/9 + diagnostic-clank; INC-014, INC-034, live korean-tech-wire drift found by the survey itself; INC-030's false-negative cross-host sweep; smartphone's clean-checkout-only bug discovery; smartwatch's five-way cross-check as the most thorough pattern).
- **Why REHOME:** the semantic core ("repo says deployed" ≠ "host runs this"; config-in-effect ≠ config-intended) is deployment-mechanics territory. Fleet Law 9 covering it is DEFERRED (not ACTIVE), which keeps the ratification home genuinely open — a future DEPLOYMENT domain would be its natural home, with clusters 8 + 9 + #12 as seed candidates and Law 9/R-001 as the governance hook.
- **Not advanced into Operations V1.**

## REHOME — Delivery retry/idempotency (MEDIUM #15)

- One duplicate-notification incident, low severity; the concern is delivery-transport semantics (retry authority, restart safety, idempotent sends).
- **Recommendation: REHOME → future DELIVERY domain.**

## HOLD — Lifecycle state model: blocked-is-prose (MEDIUM #14)

- Real mechanism gap (blocked/mothballed state exists in documentation, not enforced code) with zero confirmed harmful promotion; adjacent to OPS-C's evidence-integrity scope and STD-UI-COM-005's promotion mechanics, but not identical to either.
- **Recommendation: HOLD** — revisit if a harmful mispromotion from prose-only state ever surfaces.
