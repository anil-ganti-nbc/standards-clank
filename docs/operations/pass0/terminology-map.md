# Operations Pass 0A — Terminology Map

What each fleet member actually calls the concepts this pass surveyed,
and what the term means *in that repo specifically*. Built to prevent
Pass 0B from assuming two repos mean the same thing because they use the
same word (or that they mean different things because they use different
words). Source: [evidence-log.md](evidence-log.md).

## "Was this a scheduled or a manual/deploy run?"

| Repo | Mechanism | Verifiable from stored data? |
|---|---|---|
| watch-clank | `scheduled: bool` flag on `run_live_or_scheduled` | No (was a no-op flag until fixed; even fixed, self-asserted) |
| oem-radar | No trigger field; "Epoch" (which DB file is current) is the only bookkeeping | No — epoch boundary is "which file is at `data/radar.db`," not per-run |
| smartphone-clank | `run_reason` field, default `"production_scheduled"`, explicit `field_test_manual` for manual | Yes — stored per run |
| feature-phone-clank | No schema field found; manual pre-cron validation runs kept in a fully separate deployment/DB instead | N/A by isolation, not by tagging |
| chinese-tech-wire | `IngestionRun.trigger`, `"SCHEDULED"` vs `"MANUAL"` | Self-asserted only — driven by a CLI flag anyone can pass, not cross-checked against `schtasks` |
| korean-tech-wire | No schema field at all; "natural" origin is asserted only in YAML comment prose | No — unverifiable from the DB |
| semiconductor-intelligence | `OperationalTriggerType` enum: `SCHEDULER` / `MANUAL_CLI` / `RETRY`, persisted per `OperationalJobRun` | Yes — stored per run, and the scheduled path is required to route through `OperationalScheduler` |
| tablet-clank | No trigger-source field in the JSONL cycle schema | No — reconstructed only from external context |
| smartwatch-clank | No formal trigger field; manual verification cycles distinguished only in prose docs | No |
| diagnostic-clank / fleet governance | `materialization_policy` enum (ADR-0011) governs whether a *record* is expected at all, not whether a run was manual; scheduler-truth is tracked via the six-stage `SCHEDULE_EXPECTED → ... → OUTCOME_RECORDED` model (ADR-0008) | Fleet-level model, not yet adopted by most fleet members' own schemas |

## "Soak"

| Repo | What it means here |
|---|---|
| watch-clank | ≥4 successful *scheduled* acquisition runs before promotion review, plus 10 ALL-required manual gates |
| oem-radar | A fully isolated experiment (separate DB, separate cadence) with its own baseline boolean; production Hourly Crawl task never touches it |
| smartphone-clank | An architecture-level soak clock, explicitly reset on any scheduler-architecture redeploy ("resets the mental soak clock") |
| feature-phone-clank | A time-boxed (3-5 day) unattended run of a fully separate experimental deployment (own checkout/image/volume/DB/lock/crontab) |
| chinese-tech-wire | A free-text runbook field ("soak start:", "cycles completed:"); restarts on any change to scraper/pipeline/scoring logic, by human judgment, not code |
| korean-tech-wire | Not a separate concept — "soak" is just the ordinary collection-running command; progress is the accumulated `source_run_health` row history itself |
| semiconductor-intelligence | A staging release's soak clock, explicitly tied to candidate SHA (a materially different build restarts it), documented but not code-enforced |
| tablet-clank | A bounded, resumable N-cycle state machine (12 consecutive 2h cycles); an interrupted run restarts from cycle 1 |
| smartwatch-clank | An ongoing natural-cadence observation window evaluated by an operator reading health/event history; no formal cycle-counter |
| clank-architecture (fleet) | `SourceLifecycleState.SOAK` + `SoakStatus` (cycles_completed/required, failure_count, promotion_gate_met) — a formal contract-layer model, not yet consumed by most fleet members' own code |

## "Baseline" / "epoch" / continuity

| Repo | Term used | Mechanism |
|---|---|---|
| watch-clank | "operational epoch" | `_auto_baseline_for_first_run`; per-collector-id first-run silence |
| oem-radar | "Epoch 1 / Epoch 2" | Documentation-only; no schema column, epoch = "which DB file is current" |
| smartwatch-clank | "continuity event" | Append-only `continuity-events.jsonl`, cites `clank-architecture/adr/0006` as the shared schema authority |
| feature-phone-clank | "continuity" | `core/continuity.py`, also cites ADR-0006 and diagnostic-clank's `fleet.yaml` |
| tablet-clank | "FIRST_SEEN != NOVELTY" | Baseline cycle explicitly produces 0 events by construction |
| clank-architecture | "continuity/epoch semantics" | ADR-0006 — the shared authority several fleet members already cite |

## Lifecycle / maturity states

| Repo | States found | Formal (enum/DB) or prose-only? |
|---|---|---|
| watch-clank | `EXPERIMENTAL_READY_FOR_HETZNER` maturity set; separate "retirement" (no flag, full removal from every surface) | Formal set for experimental; retirement is prose/process only |
| oem-radar | `EXPERIMENTAL`, `SOAKING`, `RESEARCH_ONLY` | Prose-only (handoff docs), no enum found |
| smartphone-clank | Two independent state machines: source-validation (`LIVE_VALIDATED`/`PROMISING`/`UNSTABLE`/`BLOCKED`/`REJECTED`/...) and adapter-validation (`EXPERIMENTAL`/`LIVE_PARTIAL`/`LIVE_VALIDATED`/`BLOCKED`/`UNSUPPORTED`), plus a separate `MATURITY_PRODUCTION`/`MATURITY_SOAK` notification-authority axis | Formal (Python enums / config), explicitly flagged in-repo as "two independent concepts, easy to conflate" |
| feature-phone-clank | Single allowlist (`production_collectors: list[str]`); everything else implicitly experimental | Formal but minimal — no BLOCKED/DISABLED distinction |
| chinese-tech-wire | Whole-app `release_channel` (defaults `"soaking"`); per-source `DISABLED`/`BLOCKED`/`PARTIAL` policy labels | Formal but static — no transition logic, timestamps, or review dates |
| korean-tech-wire | `EXPERIMENTAL` / `PRODUCTION` only; `HOST-BLOCKED` exists only as prose in a repair doc, not a stored state | Formal for the two main states; "blocked" is prose-only |
| semiconductor-intelligence | Per-source `support_status` (`LIVE_VALIDATED`, `NEEDS_OWNER_PROBE`, ...) | Formal (YAML field) |
| tablet-clank | `EXPERIMENTAL` / `DISABLED` only, plus two independent overlay allowlists (production eligibility, campaign approval) | Formal, deliberately minimal by design (avoids smartphone-clank's dual-gate-drift mistake) |
| smartwatch-clank | `CollectorTier`: `PRODUCTION`/`EXPERIMENTAL` only; "BLOCKED" exists only as a ticket/prose status, never an enum value or DB column | Formal for tier; "blocked" is prose-only — a confirmed gap (INC-033's collector stayed structurally promotable) |
| clank-architecture (fleet) | `ALLOWED_SOURCE_TRANSITIONS`: `DISCOVERED → RESEARCH → EXPERIMENTAL → SOAK → PRODUCTION`, plus parallel `DISABLED`/`QUARANTINED`; separately, `NO_PROMOTION_POLICY.md`'s `PROTOTYPE`/`UNVERIFIED_PRODUCTION`/`VERIFIED_PRODUCTION`/`QUARANTINED` | Formal, most complete model found in the fleet — not yet adopted by any individual Clank's own code |

## Health vs. scheduler-enabled

Every repo surveyed that has *any* health concept keeps it as a derived,
run-history-based signal, explicitly distinct from whether a scheduler
entry exists/is enabled — this is the most convergently-adopted pattern
in the whole survey (see [cluster C](clusters/health-state-vs-scheduler-enabled-conflation.md)).
Names differ: watch-clank's `acquisition_state`/`yield_state`,
oem-radar's `operational_state: degraded-until-first-run`,
smartphone-clank's `health_score()` (with a documented gap — doesn't
check enablement/validation/candidate realism),
feature-phone-clank's `source_health`/`delivery_health` split,
chinese-tech-wire's `runtime_snapshot()` merging `scheduler` (OS-level)
and `current_run`/`last_completed_run` (DB-level) as siblings,
korean-tech-wire's five-state `health_state` (explicitly citing "Fleet
Law 3"), semiconductor-intelligence's ten-condition
`effective_automation_state` layering. `clank-architecture/FLEET_LAWS.md`
Law 3 ("Health honesty") is the one **ACTIVE** (not proposed) fleet-wide
governance document already asserting this as a rule, with named
violators across multiple Clanks.

## Locking / concurrent-execution prevention

| Repo | Mechanism | Known-broken predecessor |
|---|---|---|
| watch-clank | `RunLockService`; `stale_run_threshold_minutes` | Windows `os.kill` PID-liveness check could kill the wrong process (found 2026-08-21) |
| oem-radar | OS-level `flock`/`msvcrt.locking`, no PID/liveness consulted at all | PID-liveness lock (`{"pid": 1, ...}`), broke for ~81 consecutive fires (2026-08-23) |
| feature-phone-clank | `_pid_alive()` OS-level probe, ported verbatim from OEM Radar | N/A (adopted the already-fixed pattern) |
| chinese-tech-wire | External `flock` wrapping the cron invocation (no in-process lock) | N/A |
| korean-tech-wire | `RunLock`, cross-platform advisory file lock | N/A (no incident found — lock present from early on) |
| semiconductor-intelligence | `LeaseManager`, expiring database lease + `reconcile_stale_runs` | N/A |
| tablet-clank | `SoakLock`, PID+liveness-based stale-lock reclaim (Windows `OpenProcess` probe, "mirrors feature-phone-clank") | N/A |
| smartwatch-clank | OS-level `flock`/`msvcrt.locking`, explicitly built because "the old PID/hostname-based reclaim logic was proven broken in Docker's one-shot `run --rm` model" | PID/hostname-based reclaim (pre-fix) |

Every fleet member that has fixed this bug cites another fleet member's
fix by name (see the Lineage sections of each survey report) — this is
the most explicitly-lineaged pattern found in the entire corpus.
