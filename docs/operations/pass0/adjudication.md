# Operations Pass 0B — Adversarial Adjudication (2026-08-31)

Adjudicates the 11 HIGH-priority clusters and 4 MEDIUM clusters from the
Operations Pass 0A handoff ([handoff.md](handoff.md)), against
[evidence-log.md](evidence-log.md), [incident-ledger.md](incident-ledger.md)
(46 incidents), and [terminology-map.md](terminology-map.md). Spot-checks:
none required — every load-bearing claim resolved from the package; ADR
statuses verified once in clank-architecture (governance-load-bearing, see
below).

**Governing governance discovery:** clank-architecture **ADR-0008,
ADR-0009, and ADR-0011 are all `PROPOSED — REVIEWED DRAFT (activates on
reviewed merge)` — NOT ACTIVE**. Only Fleet Laws 3, 5, 7, 8 are ACTIVE
(CI-enforced); Law 9 is DEFERRED. This materially changes reconciliation:
where the handoff implied "clank-architecture already owns it," three of
the strongest clusters actually overlap *reviewed-but-unactivated*
drafts. The reconciliation below accounts for this precisely.

## Disposition table — all 15 clusters

| # | Cluster | Pri | Disposition | Candidate | Recommendation |
|---|---|---|---|---|---|
| 1 | scheduler-truth-materialization-gap | HIGH | **KEEP DISTINCT** (+ merge with #11) | OPS-A Execution materialization truth | **ADVANCE** |
| 2 | pid-namespace-unsafe-stale-lock-reclaim | HIGH | **KEEP DISTINCT** | OPS-D Lock reclaim soundness | **ADVANCE** |
| 3 | health-state-vs-scheduler-enabled-conflation | HIGH | **MERGE WITH #4** | OPS-B Health-honesty two-axis complement | **ADVANCE** |
| 4 | source-starvation-zero-vs-healthy-conflation | HIGH | **MERGE WITH #3** | OPS-B | **ADVANCE** |
| 5 | natural-cycle-vs-manual-trigger-provenance-gap | HIGH | **MERGE WITH #6, #7, #13** | OPS-C Promotion/soak evidence integrity | **ADVANCE** |
| 6 | soak-clock-reset-semantics-and-material-change-judgment | HIGH | **MERGE WITH #5, #7, #13** | OPS-C | **ADVANCE** |
| 7 | dual-gate-promotion-authority-drift | HIGH | **MERGE WITH #5, #6, #13** | OPS-C | **ADVANCE** |
| 8 | config-drift-local-repo-deployed | HIGH | **MERGE WITH #9, #12** | REHOME → future DEPLOYMENT domain | **REHOME** |
| 9 | remote-host-deployment-truth-verification | HIGH | **MERGE WITH #8, #12** | REHOME → future DEPLOYMENT domain | **REHOME** |
| 10 | destructive-action-authority-before-mutation | HIGH | **KEEP DISTINCT** (concern) | DEFER to ADR-0009 | **DEFER** |
| 11 | stale-duplicate-automation-surviving-migration | HIGH | **MERGE WITH #1** | OPS-A | **ADVANCE** |
| 12 | schema-deploy-fail-closed-gating | MED | **MERGE WITH #8, #9** | REHOME → future DEPLOYMENT domain | **REHOME** |
| 13 | safe-manual-intervention-during-soak | MED | **MERGE WITH #5, #6, #7** | OPS-C | **ADVANCE** (clause) |
| 14 | lifecycle-state-model-blocked-is-prose-not-code | MED | **HOLD** (standalone) | — | **HOLD** |
| 15 | retry-restart-authority-and-idempotency | MED | **REHOME DOMAIN** | REHOME → future DELIVERY domain | **REHOME** |

Result: **3 ADVANCE candidates** (OPS-A, OPS-B, OPS-C), 1 DEFER, 3 REHOME
targets (future DEPLOYMENT domain ×1 merged seed incl. #12; future
DELIVERY domain; clank-architecture), 1 HOLD, 0 KEEP-AS-STANDALONE-
REMAINING. Fewer, stronger candidates — per the handoff's own preference.

## Fleet-Law / ADR reconciliation table

| Concern | Fleet Law / ADR | Relationship | Recommended authority model |
|---|---|---|---|
| Execution materialization (OPS-A) | ADR-0008 (PROPOSED draft), ADR-0011 (PROPOSED draft) | COMPLEMENT — SC ratifies the two-fact minimum; ADR-0008's six-stage vocabulary stays clank-architecture's; ADR-0011 owns no-work semantics (referenced, not restated) | complement + coordinate on activation |
| Zombie/duplicate automation (#11, in OPS-A) | Fleet Law 5 (ACTIVE) | DEFER principle (single scheduler authority per lane); OPS-A adds the detectability complement | complement + reference |
| Health-honesty two-axis (OPS-B) | Fleet Law 3 (ACTIVE, CI-enforced) | NARROW COMPLEMENT — principle deferred to Law 3; SC ratifies the axis vocabulary + conflation-forbidden semantics Law 3 leaves open | complement + reference |
| Source starvation (#4, in OPS-B) | Fleet Law 3 (ACTIVE) | same complement, source-level facet | complement + reference |
| Promotion/soak evidence integrity (OPS-C) | Fleet Law 8 (ACTIVE, 3 named violators) | NARROW COMPLEMENT — Law 8 owns promotion-gate authority; OPS-C owns evidence verifiability, reset semantics, drift detectability | complement + reference |
| Soak reset on incident/manual recovery (in OPS-C) | ADR-0006 (PROPOSED) | REFERENCE — adopt the incident-does-not-reset rule, cite ADR-0006 as source | reference |
| Destructive production actions (#10) | ADR-0009 (PROPOSED REVIEWED DRAFT) | DEFER — ADR-0009 is the complete, incident-authored contract; SC declines to compete | defer + operator activation flag |
| Deployment truth + config drift (#8/#9/#12) | Fleet Law 9 (DEFERRED), RISK_REGISTER R-001 | REHOME — future DEPLOYMENT domain; Law 9's deferred status means the ratification home is genuinely open (SC-first is possible later) | rehome (defer for now) |
| Delivery retry/idempotency (#15) | none | REHOME → future DELIVERY domain | rehome |

## Per-cluster adjudication (HIGH clusters)

### 1. Scheduler-truth materialization gap — KEEP DISTINCT, ADVANCE (OPS-A)

The corpus's most severe operational incident (INC-027: one root-privileged
redeploy silently broke cron across **three Clanks** for ~36 hours) plus
INC-002 (stale launcher, silent parallel firing), INC-021 (due-gate
aggregation bug, ~4× request rate for a week), and INC-012 (165 lost
APScheduler executions). The standardizable core is deliberately coarser
than ADR-0008's six-stage model: **a Clank that fires collection must
record two facts in its own store — that an invocation happened, and what
outcome it produced — and "scheduler says enabled/next-run" is not
either of them.** ADR-0008's finer stage vocabulary stays
clank-architecture's (COMPLEMENT + coordinate on activation); ADR-0011's
no-work semantics are referenced to kill the INC-028 false-positive shape
(a legitimately empty, correctly-due cycle is a recorded *no-work
outcome*, never a materialization gap).

**Counterexample:** "a Clank scheduled entirely by an external platform
has no invocation record of its own." Narrowed and survived: the
invariant binds the Clank's own recorded evidence of what happened after
any trigger — who fired it is out of scope. **Merge #11:** zombie/duplicate
automation becomes *detectable* under the two-fact contract (two
invocation streams visible in records); Fleet Law 5 remains the
single-authority governing rule (deferred to, not restated).

### 2. PID-namespace-unsafe stale-lock reclaim — KEEP DISTINCT, ADVANCE (OPS-D)

Three independent incident discoveries (oem-radar ~81 hours blocked,
INC-009; watch-clank's inverse wrong-process kill, INC-006;
smartwatch-clank proven broken in one-shot Docker) with the identical
root shape: a reclaim decision fooled by PID-namespace ambiguity. The fix
propagated by explicit porting (one implementation lineage) — but the
*incidents* are independent discoveries of the same structural
unsoundness, which is what counts. Standardize the consequence (a lock
reclaim decision MUST NOT depend on a PID-liveness check where PID scope
is ambiguous) with the fleet-proven OS-advisory-lock mechanism named as
the endorsed implementation. **Open verification item flagged to
operator:** chinese-tech-wire and korean-tech-wire were not confirmed to
have hit this — untested-but-exposed vs safe-by-different-design is
unknown. **Counterexample:** "a strictly single-instance-by-construction
Clank (one user, one container, no reuse risk) — PID checks are safe."
Narrowed: applicability wherever locks must survive container/namespace
boundaries or PID reuse; the fleet runs Docker, NAS, and Windows
simultaneously, so fleet-wide applicability stands.

> **Pass 1.5 resolution (2026-08-31):** OPS-D advanced as a distinct
> candidate — the invariant abstracts to exclusivity-marker soundness
> (an exclusivity/ownership marker must never be reclaimed, honored, or
> acted upon solely from an identifier whose liveness/ownership cannot
> be proven in the current execution context). Card:
> [candidates/ops-d-exclusivity-marker-soundness.md](candidates/ops-d-exclusivity-marker-soundness.md).
> Pass 1 omitted it from commissioned scope; Pass 1.5 resolves the
> omission — see
> [../../pass1/ops-d-resolution.md](../../pass1/ops-d-resolution.md).
> No STD-OPS-COM-004 drafted (reserved for separate commission).

### 3+4. Health-honesty two-axis complement — MERGE, ADVANCE (OPS-B)

The most convergently-adopted pattern in the survey (7/9 Clanks, several
citing Fleet Law 3 by name) plus the sharpest incident pair (watch's
ZERO_ITEMS-as-HEALTHY masking 20 consecutive empty runs, INC-006;
diagnostic-clank's ADR-0007 built from a green-dashboard/missing-delivery
incident). Law 3 is ACTIVE and owns the principle — SC does not restate
it. The narrow complement SC ratifies: **the two-axis semantics and their
vocabulary** (scheduler-liveness/trigger provenance ⊥ outcome health; and
within health: acquisition ⊥ yield), which Law 3 leaves open — nine
repos, nine different axis names. Source-starvation (#4) is the
source-level facet of the same axis split and merges in with its
independent convergence evidence (ctw/ktw found-vs-new zero-streak pair;
INC-022 catch) and its incident. **Live finding flagged to operator:**
smartphone-clank's `health_score()` is a documented, unfixed gap against
this pattern. **Counterexample:** "a Clank with no scheduler at all."
Survives: the axis pair becomes trigger-provenance ⊥ outcome-health; the
conflation ban is unchanged.

### 5+6+7+13. Promotion/soak evidence integrity — MERGE, ADVANCE (OPS-C)

One coherent evidence-integrity invariant with four facets:
(1) **trigger provenance** must be structurally verifiable from stored
data, wherever promotion/soak qualification depends on it (semi-int's
OperationalScheduler routing proves the structural form; half the fleet
has no verifiable field; korean-tech-wire's promotion evidence is a YAML
comment; chinese-tech-wire's flag is self-asserted and un-cross-checked);
(2) **soak clock semantics**: a material change resets the clock and the
reset decision is recorded (build identity + reason); an incident, host
move, or manual recovery does not reset it (ADR-0006-aligned); operator
interventions during soak are distinguishable from natural cycles (#13);
(3) **promotion gate drift** must be detectable and fail-closed: where two
gates must agree, demotion-through-either or equivalent cross-validation
is required (INC-013 Motorola near-miss; Law 8 complement; tablet's
cascade and fp's single-gate both conform). Cycle counts (12/20) are
policy parameters — explicitly not standardized. **No confirmed harm
incident exists for facet (1) alone** — but facet (1) is the
verifiability foundation the other facets' incidents (INC-013) depend on,
and semi-int proves the structural form is achievable; the merged
candidate's evidence is STRONG jointly.

**Counterexample:** "a Clank with no soak/promotion lifecycle — everything
is production immediately." Trigger-unmet (nothing to qualify). Second:
"manual diagnostic invocation during soak would become forbidden." No —
the invariant requires interventions be *distinguishable and
non-qualifying*, never forbidden. Survives both.

---

## MEDIUM-cluster notes

- **#12 schema-deploy fail-closed gating**: 2 confirmed incidents
  (smartphone INC-016 zero-row table; the Alembic single-authority fix),
  but half the fleet has no equivalent mechanism and no incidents —
  deployment-migration territory. REHOME to the future DEPLOYMENT domain
  as a seed candidate.
- **#13 safe-manual-intervention-during-soak**: the one dated incident
  shows correct handling; merged into OPS-C as the
  interventions-are-distinguishable clause (with C5's provenance
  verifiability this becomes enforceable rather than aspirational).
- **#14 lifecycle-state blocked-is-prose**: real mechanism gap (blocked
  state exists as documentation, not code), zero confirmed harmful
  promotion. HOLD — standalone, revisit with maturity evidence.
- **#15 retry/restart/idempotency**: one duplicate-notification incident,
  low severity; delivery-side. REHOME → future DELIVERY domain.

## Special disposition: destructive production actions (#10)

The concern is real and the severity is the highest in the corpus:
INC-041 (agent-run volume deletion on a naming-pattern guess → **total,
unrecoverable production data loss**, feature-phone-clank) and INC-036
(the same root cause against smartwatch-clank one week later, partial
loss, stale-backup recovery) — both agent-caused, both pre-dating and
directly motivating ADR-0009's 8-step contract (DISCOVER → RESOLVE
IDENTITY → CLASSIFY → PROVE BACKUP → DISPLAY TARGET → AUTHORISE → MUTATE
→ VERIFY).

**Disposition: DEFER to ADR-0009 as the sole governing contract.** Three
reasons: (1) ADR-0009 is complete, reviewed, and written in direct
response to these exact incidents — a SC restatement would be a competing
authority for zero marginal safety; (2) the contract is runtime/
architecture governance, whose home is clank-architecture; (3) nothing
in the surveyed evidence suggests the 8-step contract is insufficient.
**Operator flags (out of this pass's authority):** (a) ADR-0009 is still
`PROPOSED — REVIEWED DRAFT` despite post-dating both incidents — consider
activating it out-of-band; (b) both real incidents were *agent-performed*
operations — consider whether ADR-0009 should name agent-executed
destructive actions as an explicit risk class. SC declines to standardize
here; this deferral is the strongest governance-respect signal in the
program so far.
