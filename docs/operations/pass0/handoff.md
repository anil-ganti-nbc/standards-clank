# Pass 0A → ZLM Adjudication Handoff (Operations domain)

Eleven clusters, HIGH priority only. Each gives ZLM exactly what's needed
to adjudicate without re-crawling the fleet: the claim to test, evidence
for/against, independent lineages, key citations, and the specific
question to answer. Full detail, MEDIUM clusters, and all raw survey
material: [README.md](README.md), [clusters/](clusters/),
[evidence-log.md](evidence-log.md), [incident-ledger.md](incident-ledger.md),
[terminology-map.md](terminology-map.md).

**Standing context that applies to several of these**: unlike the
Data/Ontology domain, `clank-architecture` already has **ACTIVE** (not
proposed) fleet-wide governance directly overlapping four of these eleven
clusters — `FLEET_LAWS.md` Laws 3 (health honesty), 5 (single-scheduler-
authority), 7 (writer coordination), 8 (promotion gates), and Deferred
Law 9 (repo-behind-production) — already CI-enforced in multiple fleet
repos. Two 2026-08-22/23 fleet-wide incidents already produced
`clank-architecture` ADR-0008, ADR-0009, and ADR-0011. **Every cluster
below marked "Fleet Law overlap" needs an explicit adjudication of
whether Standards Clank ratifies/restates the existing law, defers to it
narrowly, or declines to compete with it** — this is a new category of
adjudication question the Data/Ontology domain never faced (its closest
prior art, ADR-0006/0014, was itself only PROPOSED).

---

## 1. Scheduler-Fired ≠ Actual Execution / Outcome Materialized

**Claim to test**: "the scheduler fired" (or shows enabled/next-run) must
never be treated as equivalent to "the collection actually happened and
was recorded" — the gap can occur at multiple distinct stages and must be
positively verified, not assumed.

**Strongest evidence FOR**: the single most severe incident in the entire
corpus — a 2026-08-22 root-privileged redeploy silently broke cron
execution across **three Clanks simultaneously** for ~36 hours (INC-027),
directly motivating `clank-architecture`'s six-stage `SCHEDULE_EXPECTED →
... → OUTCOME_RECORDED` model (ADR-0008). Also: watch-clank's `scheduled`
flag was a pure no-op label (INC-002); korean-tech-wire's per-item
due-check design still produced ~4x the intended request rate for a week
because of an aggregation bug (INC-021, overlaps cluster 5 below);
semiconductor-intelligence's invocation-vs-commit split is already cited
fleet-wide as "the reference semantic" (`FLEET_LAWS.md` Law 3).

**Strongest evidence AGAINST / open risk**: a *rule* here must accommodate
a legitimate zero-work cycle — oem-radar's own monitoring tool
over-inferred a materialization gap from three genuinely empty, correctly-due-gated
cycles (INC-028), a real false-positive in the opposite direction. Any
standard needs to avoid reproducing that failure shape.

**Independent lineages**: watch-clank, oem-radar, chinese-tech-wire,
korean-tech-wire, semiconductor-intelligence all built distinct
mechanisms independently; `clank-architecture`'s stage model was derived
*after* and *in response to* INC-027/INC-028, not proposed speculatively.

**Key citations**: `clank-architecture/adr/0008-execution-liveness-and-materialization-gap.md`,
`adr/0011-no-work-execution-semantics.md`, `semi_intel/operations/scheduler.py:345-349`,
`korean_tech_wire/scheduling.py`, `docs/stage4.1-reliability-repair.md`.

**Question for ZLM**: should Standards Clank adopt `clank-architecture`'s
stage vocabulary directly (Fleet Law overlap — see standing context), or
define a coarser two-fact contract (invocation timestamp + outcome
timestamp) and leave the finer stage model to `clank-architecture`?
Separately: how should the acceptance criteria be worded so a rule here
doesn't reproduce INC-028's false-positive shape?

---

## 2. PID-Namespace-Unsafe Stale-Lock Reclaim

**Claim to test**: a run-lock that reclaims a stale lock by checking
PID-liveness is unsound wherever PID scope is ambiguous (every Docker
container is PID 1 to itself); the reclaim mechanism must use an OS-level
advisory lock instead.

**Strongest evidence FOR**: three fleet members independently hit the
*identical* bug: oem-radar's NAS canary refused to start for ~81
consecutive hourly fires after a crash left a `{"pid":1,...}` lock
(INC-009, cross-referenced to Diagnostic Clank incident `5f280abf`);
watch-clank's inverse failure (a Windows liveness check could kill the
*wrong* process, INC-006); smartwatch-clank's pre-fix PID/hostname reclaim
"proven broken in Docker's one-shot `run --rm` model." The fix (OS-level
`flock`/`msvcrt.locking`, no PID consulted) is now propagated by direct,
explicitly-cited code-porting across at least four repos (oem-radar ←
Free Game Tracker; feature-phone-clank ← oem-radar; smartwatch-clank ←
oem-radar/FGT/Diagnostic-Clank-incident; tablet-clank ← feature-phone-clank).

**Strongest evidence AGAINST**: none — no repo argues PID-liveness
locking is safe.

**Independent lineages**: this is the most explicitly-lineaged cluster in
the whole corpus — deliberate code-porting, not independent convergence,
with the specific originating bug named inline in multiple repos' own
comments.

**Key citations**: `oem-radar/src/oem_radar/core/run_lock.py:1-34`,
`smartwatch-clank/src/smartwatch_clank/core/lock.py:16,27-31`,
`feature-phone-clank/src/feature_phone_clank/core/run_lock.py:1-7`.

**Question for ZLM**: should Standards Clank standardize the mechanism
(no PID/liveness heuristic permitted) or only the consequence (a lock
reclaim decision must never depend on a check foolable by PID-namespace
reuse)? Also: chinese-tech-wire and korean-tech-wire were not confirmed
to have hit this bug — untested-but-exposed, or actually safe by a
different design? Worth flagging as an open verification item rather
than assuming either.

---

## 3. Health State vs. Scheduler-Enabled Conflation

**Claim to test**: "scheduler shows this job enabled" (or "last
invocation exited 0") must never be read as "this job is healthy" — a job
can be enabled and exit 0 while producing nothing useful.

**Strongest evidence FOR**: the most convergently-independently-adopted
pattern in the entire survey — seven of nine fleet Clanks have built some
version of a two-axis health split (see
[terminology-map.md](terminology-map.md)), several explicitly citing
`clank-architecture` Fleet Law 3 by name in their own source comments.
watch-clank's `ZERO_ITEMS`-counted-as-success bug (INC-006) and
`diagnostic-clank`'s ADR-0007 (built directly from a Watch-Clank-class
incident: green dashboard, missing Discord delivery, INC-043) are the
clearest incident evidence.

**Strongest evidence AGAINST**: none disputing the principle.
smartphone-clank's `health_score()` is a documented, currently-**unfixed**
gap — an exception to an otherwise fleet-wide-adopted pattern, worth
flagging as a live finding, not just historical evidence.

**Independent lineages**: convergent, not copied — nine different names
for the same concept, structurally different implementations.

**Key citations**: `clank-architecture/FLEET_LAWS.md:25-31` (Law 3, ACTIVE,
named violators across 4 Clanks), `watch-clank/app/services/health.py:105-121`,
`docs/V038_PRODUCTION_REPORT_INVESTIGATION.md:211-227` (smartphone-clank's
open gap).

**Question for ZLM**: **Fleet Law overlap** — Law 3 is already ACTIVE,
CI-enforced governance naming this exact concern. Does a Standards Clank
standard here restate Law 3, narrow it to the vocabulary-standardization
gap Law 3 leaves open (nine different axis names), or decline entirely?
This is likely the single clearest test case for the Fleet-Laws
reconciliation question.

---

## 4. Source Starvation / Zero-vs-Healthy Conflation

**Claim to test**: a source producing zero new observations must be
distinguishable from a source legitimately having nothing new to report;
detection of the former must not silently read as healthy.

**Strongest evidence FOR**: watch-clank's `ZERO_ITEMS`-as-success bug
(INC-006, 20 consecutive zero-item runs read HEALTHY); the cleanest
independent-convergence pair in the corpus — chinese-tech-wire and
korean-tech-wire both built a near-identical found-vs-new zero-streak
distinction with zero shared code, and korean-tech-wire's version
correctly caught a real 8.5-day zero-new-articles block (INC-022).
`diagnostic-clank`'s `HealthPayload` contract cites the watch-clank
incident directly as its motivating case.

**Strongest evidence AGAINST**: tablet-clank explicitly, by design, does
not implement disappearance detection yet — an accepted scope gap, not a
disagreement.

**Independent lineages**: chinese-tech-wire/korean-tech-wire pair is
convergent-not-copied; no repo cites another's code for this specific
mechanism.

**Key citations**: `watch-clank/app/services/health.py:190-208`,
`chinese-tech-wire/pipeline/source_health.py:9-19,145-166`,
`korean-tech-wire/docs/promotion-policy.md:18`,
`korean-tech-wire/docs/stage4.1-reliability-repair.md:40-69`.

**Question for ZLM**: given how convergently this is already built fleet-wide,
is there a standardizable gap left at all beyond naming the consequence,
or would ratifying a rule here be largely redundant with existing
best practice? Also: is tablet-clank's accepted gap a legitimate,
scope-based exception, or does any production-eligible source need this
regardless of current maturity?

---

## 5. Natural-Cycle vs. Manual-Trigger Provenance Gap

**Claim to test**: whether a run was fired naturally or manually must be
verifiable from stored data wherever that distinction is used as
promotion/soak evidence.

**Strongest evidence FOR (that the gap is real)**: over half the fleet
(oem-radar, korean-tech-wire, tablet-clank, watch-clank/feature-phone-clank-by-isolation)
has no verifiable trigger field at all; korean-tech-wire's promotion
evidence is asserted only in a YAML *comment*, unverifiable from the
database itself; chinese-tech-wire's trigger field is self-asserted by a
CLI flag nothing cross-checks against the actual scheduler.

**Strongest evidence AGAINST (that it's solvable / already solved
elsewhere)**: semiconductor-intelligence requires the scheduled path to
route through `OperationalScheduler` so the trigger can't be spoofed —
proof the same guarantee can be made structurally, not just by
convention.

**Independent lineages**: independent invention wherever it exists at
all; no cross-repo citation found for this specific mechanism (contrast
cluster 2).

**Key citations**: `smartphone-clank/tests/test_run_once_due_check.py:113-130`,
`chinese-tech-wire/main.py:1017`, `korean-tech-wire/config/sources.yaml:12-14`,
`semi_intel/operations/scheduler.py` (`OperationalTriggerType`).

**Question for ZLM**: no confirmed incident of this gap actually causing
harm was found (unlike most other HIGH clusters) — is a structural gap
with clear exploitability, absent a confirmed incident, sufficient
evidence to advance, or should this be held pending a real occurrence?
Note this overlaps directly with INC-021's AND-gate bug (cluster 1) —
worth checking whether that incident should be read as partial evidence
of harm here too.

---

## 6. Soak Clock Reset Semantics and Material-Change Judgment

**Claim to test**: a soak/maturity clock should reset on a materially
different build/change, but survive operational incidents, host moves,
and cosmetic changes.

**Strongest evidence FOR**: near-universal independent convergence on the
material-change-resets rule (chinese-tech-wire, smartphone-clank,
semiconductor-intelligence, smartwatch-clank all state some version of
it) — but in every single case the "is this material" classification is
a **human judgment recorded in prose**, never code-enforced.
`clank-architecture` ADR-0006 separately states an incident/manual-recovery
action must NOT reset the clock — a distinct, non-conflicting rule.

**Strongest evidence AGAINST**: none disputing the principle; the
open question is purely mechanism.

**Independent lineages**: convergent, not copied.

**Key citations**: `chinese-tech-wire/ai/handoff/STAGING_RELEASE_RUNBOOK.md:64-69`,
`smartphone-clank/docs/SCHEDULER_MIGRATION.md:95-99`,
`clank-architecture/adr/0006-continuity-and-epoch-semantics.md:68`.

**Question for ZLM**: is "classify a diff as material" automatable at
all, or should a standard only require that the reset decision be
*recorded* (build/SHA + timestamp + reason) without mechanizing the
classification itself? Should the two rules (material-change-resets vs.
incident-does-not-reset) be adjudicated and drafted as two separate
acceptance criteria given they're logically independent?

---

## 7. Dual-Gate Promotion Authority Drift

**Claim to test**: where promotion requires two independently-maintained
gates to agree, the gates drift, and only one being updated during a
promotion can leave a source silently mispromoted or silently believed-safe.

**Strongest evidence FOR**: smartphone-clank's Motorola incident
(INC-013) — two uncross-checked gates, only one updated, would have
produced 18 false alerts on the next scheduled run had it not been caught
same-day; directly and explicitly cited as the reason feature-phone-clank
built a deliberately simpler single-gate design. `clank-architecture`
Fleet Law 8 is **ACTIVE** governance naming this exact concern, with
three named historical violators (tablet, smartwatch, oem-radar).

**Strongest evidence AGAINST**: tablet-clank's demotion-cascades-through-both-gates
design is a working counter-model — two gates can coexist safely if
demoting either automatically revokes eligibility.

**Independent lineages**: feature-phone-clank's fix is explicit, cited,
inherited lineage from smartphone-clank's incident — not independent.

**Key citations**: `smartphone-clank/docs/wave2/MOTOROLA_CANARY_REPORT.md:17-31`,
`feature-phone-clank/src/feature_phone_clank/core/scope.py:1-9`,
`clank-architecture/FLEET_LAWS.md:65-71` (Law 8, ACTIVE, named violators).

**Question for ZLM**: **Fleet Law overlap** — same reconciliation
question as cluster 3, applied to Law 8. Also: is "collapse to a single
gate" or "keep two gates but cascade demotion through both" the better
consequence to require, given both are represented as working fleet
mitigations?

---

## 8. Config Drift (Local / Repo / Deployed)

**Claim to test**: configuration diverging across local-edit, committed-repo,
and actually-deployed layers is usually discovered by accident, not by a
systematic gate.

**Strongest evidence FOR**: the broadest-evidenced cluster by repo-count
in this survey — 8 of 9 fleet Clanks plus `diagnostic-clank` show at
least one instance, ranging from smartphone-clank's repo-committed config
silently able to restore a disabled state on re-clone (INC-014) to
smartwatch-clank's two-independently-maintained-deploy-wrapper drift
silently disabling a production proxy (INC-034) to a live,
previously-unknown drift this survey itself discovered directly in
korean-tech-wire's example-vs-local config.

**Strongest evidence AGAINST**: none disputing the concern; several repos
treat *some* drift as an accepted, explicit tradeoff (chinese-tech-wire's
intentionally-never-synced dev-machine checkout).

**Independent lineages**: independent per-instance; no shared mechanism
found across repos.

**Key citations**: `smartphone-clank/docs/V038_PRODUCTION_REPORT_INVESTIGATION.md:1-51`,
`smartwatch-clank/docs/ticket-garmin-relay-production-wiring.md`,
`clank-architecture/docs/FLEET_INVENTORY.md`.

**Question for ZLM**: given how many *distinct* drift mechanisms were
found (config files, deploy scripts, DB filenames, allowlists, WAL
headers), does this decompose into several narrower standardizable rules
rather than one? Also: should korean-tech-wire's live, previously-unknown
drift (found by this survey, not previously known to the operator) be
flagged for remediation regardless of the standards outcome?

---

## 9. Remote Host / Deployment Truth Verification

**Claim to test**: a repo's HEAD or a tag/branch name is insufficient
evidence of what's actually deployed on a remote host; only a live check
of the host itself is trustworthy.

**Strongest evidence FOR**: a strikingly consistent, independently-built
multi-way cross-check pattern (git SHA vs. OCI label vs. live runtime
identity) across at least six repos, with smartwatch-clank's five-way
check the most thorough found; smartphone-clank found two real
"invisible until deployed" bugs *only* by doing a genuinely clean remote
checkout. `clank-architecture` RISK_REGISTER R-001 and Fleet Law 9
(Deferred) independently name this exact concern at governance level,
with named open violations (KTW, SemInt).

**Strongest evidence AGAINST / open risk**: tablet-clank's own
fleet-wide "timer not found" sweep produced a **false negative** by never
checking Hetzner (INC-030) — proof that even a deliberate cross-host
verification sweep can itself be incomplete; a standard needs to guard
against both directions of failure.

**Independent lineages**: convergent-not-copied for the mechanism itself,
though the specific `IMAGE_TAG`-required convention was explicitly copied
from oem-radar into watch-clank.

**Key citations**: `smartwatch-clank/docs/hetzner-deployment-2026-08-18.md:13-23`,
`smartphone-clank/docs/infra/HETZNER_SOAK_COMMISSIONING.md:84-115`,
`clank-architecture/RISK_REGISTER.md:5`, `FLEET_LAWS.md:73-74` (Law 9,
Deferred).

**Question for ZLM**: is the standardizable gap "coverage completeness"
specifically (a verification process must enumerate every host in scope,
the exact shape of INC-030's failure) given the cross-check mechanism
itself is already well-adopted? **Fleet Law overlap** (partial — Law 9 is
explicitly Deferred, not yet ACTIVE, so this may be a case where
Standards Clank ratifying first is appropriate rather than deferring).

---

## 10. Destructive Action Authority Before Mutation

**Claim to test**: a destructive mutation (e.g. volume deletion) against
production state must never proceed on a naming-pattern guess alone —
identity must be positively resolved and a backup proven first.

**Strongest evidence FOR**: the single most severe incident in this
entire survey — an agent performing fleet remediation ran a destructive
volume-deletion action trusting a naming pattern, causing **total,
unrecoverable production data loss** for feature-phone-clank (INC-041);
the *same root cause* recurred one week later against smartwatch-clank
(INC-036, partial loss, recovered from a stale backup). `clank-architecture`
ADR-0009's 8-step contract (DISCOVER → RESOLVE IDENTITY → CLASSIFY →
PROVE BACKUP → DISPLAY TARGET → AUTHORISE → MUTATE → VERIFY) was written
directly and immediately in response to these two incidents.

**Strongest evidence AGAINST**: none — no counterexample or dissenting
design found; this is unambiguous.

**Independent lineages**: n/a — both incidents share one root cause;
ADR-0009 postdates and directly responds to both.

**Key citations**: `clank-architecture/adr/0009-runtime-state-separation-and-destructive-safety.md:9-19`,
diagnostic-clank NAS incidents (feature-phone-clank total loss,
smartwatch-clank partial loss, both 2026-08-23).

**Question for ZLM**: this concern emerged from the survey rather than
being one of the 15 named topics, and the governance response
(ADR-0009) already exists, was written in direct response to these exact
incidents, and predates any Standards Clank involvement. Should Standards
Clank ratify anything here at all, or explicitly decline because
`clank-architecture` already owns this concern completely? Separately: is
the rule "any destructive mutation, human or agent" or does it need to
specifically address agent-performed operations as a distinct risk class
(both real incidents were agent-caused)?

---

## 11. Stale/Duplicate Automation Surviving Migration

**Claim to test**: an old scheduling mechanism surviving a migration to
its replacement, unnoticed, produces invisible, redundant, or destructive
duplicate execution.

**Strongest evidence FOR**: watch-clank's stale cron launcher fired
invisibly alongside new systemd timers for days (INC-002, explicitly
noted as citing smartphone-clank's identical prior fix — not a one-off);
smartwatch-clank's tier/scope type-collapse silently duplicated
production-collector execution onto a second, independent schedule
(INC-035); `diagnostic-clank/fleet.yaml` independently records a live
instance (`smartwatch-hetzner-soak-timer-retired`, a timer that fired
every cycle and failed every time until discovered). `clank-architecture`'s
Golden Incident Corpus registers this as two named, CI-tracked classes
("ZOMBIE-AUTHORITY," "AUTHORITY-BYPASS").

**Strongest evidence AGAINST**: feature-phone-clank's preventive
cross-user cron isolation is a working counter-design (anticipates the
risk rather than reacting to it) — the one clean preventive example
found in this cluster.

**Independent lineages**: watch-clank's incident is explicitly noted as
not unique to that repo, citing a prior identical smartphone-clank fix —
partial lineage, not fully independent.

**Key citations**: `watch-clank/ai/handoff/INCIDENT_LEGACY_FCB5E91_LAUNCHER.md`,
`smartwatch-clank/docs/run-scope-correction-2026-08-19.md`,
`clank-architecture/conformance/GOLDEN_INCIDENTS.md:23-24`.

**Question for ZLM**: should a standard require an explicit "old
automation decommission" checklist step as part of any scheduler
migration, or is the more general "single scheduler authority per lane"
consequence (already named as ACTIVE `clank-architecture` Fleet Law 5)
the right level? **Fleet Law overlap.** Also: does this cluster overlap
enough with cluster 1 (scheduler-truth) to consider merging during
drafting, given the "nothing corrupted only by luck" pattern recurs in
both?

---

## Not included above (see clusters/ for full detail)

MEDIUM priority: schema-deploy-fail-closed-gating (2 confirmed incidents,
but over half the fleet has no equivalent mechanism and no incident
either — unclear if this is under-evidenced or genuinely lower-urgency),
safe-manual-intervention-during-soak (only one dated incident, and that
one shows the system being handled correctly rather than failing),
lifecycle-state-model-blocked-is-prose-not-code (clear mechanism gap, no
confirmed harmful promotion yet), retry-restart-authority-and-idempotency
(confirmed harm limited to one duplicate-notification incident,
comparatively low severity).
