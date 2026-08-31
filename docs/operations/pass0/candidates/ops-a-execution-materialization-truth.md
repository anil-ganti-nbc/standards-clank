# Candidate card OPS-A — Execution materialization truth

- **Candidate name:** Execution materialization truth (clusters 1 + 11)
- **Plain-language invariant:** A Clank that fires collection must record two facts in its own store — that an invocation happened, and what outcome it produced — and neither may be inferred from scheduler state ("enabled", "next-run", "fired"). A legitimately empty cycle is a recorded *no-work outcome*, never a materialization gap; duplicate/zombie automation becomes detectable as a second invocation stream.
- **Trigger/applicability:** any Clank that fires collection from some trigger mechanism (its own scheduler, an OS scheduler, an external platform). Scheduler technology and location are out of scope.
- **Strongest evidence:** INC-027 (one root-privileged redeploy silently broke cron across three Clanks for ~36 hours — the corpus's most severe operational incident); INC-002 (stale launcher firing invisibly alongside new timers for days); INC-021 (due-gate aggregation bug, ~4× intended request rate for a week); INC-012 (165 lost APScheduler executions); semiconductor-intelligence's invocation-vs-commit split cited fleet-wide as "the reference semantic" (Fleet Law 3's own basis).
- **Strongest contrary evidence:** INC-028 — oem-radar over-inferred a materialization gap from three genuinely empty, correctly-due-gated cycles. A rule here must not reproduce that false-positive shape.
- **Independent lineages:** five Clanks built distinct mechanisms independently (watch, oem-radar, chinese-tech-wire, korean-tech-wire, semiconductor-intelligence); ADR-0008's stage model was derived after and in response to INC-027/INC-028.
- **Incidents:** INC-027, INC-002, INC-012, INC-021, INC-035 (duplicate execution via tier/scope type-collapse), INC-011 (live retired-timer instance in diagnostic-clank fleet.yaml).
- **Fleet-Law/ADR relationship:** COMPLEMENT to ADR-0008 (six-stage vocabulary stays clank-architecture's; SC ratifies the two-fact minimum) + ADR-0011 (owns no-work semantics — referenced, not restated); DEFER to Fleet Law 5 on single-scheduler-authority (zombie detection is OPS-A's contribution; authority is Law 5's).
- **Governance reconciliation disposition:** NARROW COMPLEMENT + coordinate on ADR-0008/0011 activation.
- **Strongest counterexample:** "a Clank scheduled entirely by an external platform has no invocation record of its own to expose."
- **Why it survives:** the invariant binds the Clank's own recorded evidence of what happened after any trigger — who or what fired it is out of scope. INC-028's failure shape is excluded by requiring no-work outcomes be recorded *as outcomes*, not inferred as gaps.
- **Likely implementation freedom:** stage vocabulary granularity, storage shape, heartbeat mechanism, alerting thresholds.
- **Evidence strength:** STRONG. **Fleet impact:** HIGH. **Standardization risk:** LOW-MED.
- **Recommendation: ADVANCE.**

## Counterexample test

**Strongest plausible counterexample:** "A Clank scheduled entirely by an
external platform has no invocation record of its own to expose."

**Does the candidate still hold?** YES - the invariant binds the Clank's
own recorded evidence of what happened after any trigger; who or what
fired it is out of scope. A second: "INC-028 means gap-detection rules
will cry wolf." ADR-0011's no-work semantics are referenced precisely so
a legitimately empty, correctly-due cycle is recorded as a no-work
outcome, never inferred as a gap. Survives.
