# Candidate card OPS-C — Promotion/soak evidence integrity

- **Candidate name:** Promotion/soak qualification evidence integrity (clusters 5 + 6 + 7 + MEDIUM #13)
- **Plain-language invariant:** Wherever a Clank qualifies a collector for production via soak/natural-cycle evidence, that evidence must be structurally verifiable from the Clank's own stored data: trigger provenance (natural vs manual vs deploy) recorded by the execution path itself; soak-clock reset decisions recorded with build identity + reason (material change resets; incidents/host moves/manual recovery do not); operator interventions during soak distinguishable from natural cycles; and promotion gates either single-sourced or cross-validated with divergence failing closed.
- **Exact semantic distinction:** qualification evidence is not operator assertion; a candidate-surfacing or convenience signal is not qualification; an intervention is not a natural cycle; a reset decision is a recorded fact with a reason, not silence.
- **Trigger/applicability:** any Clank with a soak/promotion lifecycle for collectors or sources. A Clank with no promotion lifecycle (everything production immediately) is out of scope.
- **Strongest evidence:** near-universal independent convergence on material-change-resets (chinese-tech-wire, smartphone, semiconductor-intelligence, smartwatch — all prose-recorded, never code-enforced); INC-013 (smartphone Motorola: two uncross-checked gates, one updated → 18 false alerts averted same-day); semiconductor-intelligence's OperationalScheduler routing proving structural trigger verifiability is achievable; korean-tech-wire's promotion evidence asserted only in a YAML comment; chinese-tech-wire's self-asserted trigger flag; Fleet Law 8's three named historical violators.
- **Strongest contrary evidence:** chinese-tech-wire treats some drift/never-sync as an accepted tradeoff (adjacent cluster 8, rehomed); tablet-clank's cascade-demotion design proves two valid gate architectures exist — so gate-count is free, only the drift/detectability discipline binds.
- **Independent lineages:** soak-reset convergence is independent across four repos; trigger-provenance mechanisms are independent wherever they exist; feature-phone's single-gate design is explicitly inherited from smartphone's INC-013 (incident inheritance, not independent — counted once).
- **Known incident support:** INC-013 (dual-gate near-miss, severe); no confirmed harm incident for trigger-provenance alone (structural gap + clear exploitability + promotion-chain dependency is the justification); INC-021's AND-gate bug is adjacent scheduling-correctness evidence, credited to OPS-A's cluster.
- **Fleet-Law/ADR relationship:** NARROW COMPLEMENT to ACTIVE Fleet Law 8 (promotion-gate authority stays Law 8's/COM-005's); ADR-0006 referenced for incident-does-not-reset; explicitly no cycle-count standardization (12/20-cycle figures are per-Clank policy parameters).
- **Governance reconciliation disposition:** NARROW COMPLEMENT + reference.
- **Strongest counterexample:** "a Clank with no soak/promotion lifecycle — everything is production immediately" and "manual diagnostic invocation during soak would become forbidden."
- **Why it survives:** the first is trigger-unmet; the second is a misreading — the invariant requires interventions be *distinguishable and non-qualifying*, never forbidden.
- **Likely implementation freedom:** soak window length, cycle counts, reset-classification mechanism (recorded-judgment vs automated diff), provenance storage, gate architecture (single gate or cascading dual gates).
- **Evidence strength:** STRONG (jointly; facet 1 alone MODERATE). **Fleet impact:** HIGH. **Standardization risk:** MED (must not prescribe cycle counts, reset classification automation, or gate architecture).
- **Recommendation: ADVANCE.**

## Counterexample test

**Strongest plausible counterexample:** "A Clank with no soak/promotion
lifecycle - everything is production immediately - has nothing for the
evidence-integrity rules to bind, so the standard is ceremony there."

**Does the candidate still hold?** YES, narrowed: the trigger excludes
Clanks with no promotion lifecycle entirely. Second counterexample:
"manual diagnostic invocations during soak would become forbidden." No -
the invariant requires interventions to be distinguishable and
non-qualifying, never forbidden. A third: "cycle counts would have to be
standardized." No - counts are explicitly per-Clank policy parameters.
Survives.
