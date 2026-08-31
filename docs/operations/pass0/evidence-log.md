# Operations Pass 0A — Evidence Log (raw survey reports)

Six parallel read-only survey agents, each covering one to two repos (five
covering the nine fleet Clanks in pairs/singles, one mining
`diagnostic-clank` specifically — both its GitHub repo and the live NAS
incident log at `http://192.168.0.105:8420/`). Each was instructed to cite
file:line for every claim, classify lineage (independent /
inherited-copied / lineage-uncertain), and prioritize incident evidence
against 15 named Operations topics (reproduced in
[README.md](README.md)). Preserved verbatim below for traceability — the
[clusters/](clusters/) files are a synthesis of this material, not a
replacement; where a cluster file's citation looks incomplete, this log
has the fuller original text.

All surveys were run 2026-08-31 against each repo's then-current local
checkout (fleet Clanks) or GitHub HEAD (`diagnostic-clank`, cloned
read-only into a scratch directory for this pass only, not vendored into
this repository).

---

## Survey 1 of 6: watch-clank + oem-radar

I have gathered extensive, well-cited evidence. Here is the full Pass 0A evidence inventory.

---

# Pass 0A Evidence Inventory — Operations Domain

Read-only survey. No standards proposed. All citations are file:line from the local repos as of survey time.

## Repo: `C:\Users\anil\Clanks\watch-clank`

**1. Scheduler truth vs actual execution**
Concrete gap found and fixed: `scripts/run_pipeline.py::run_live_or_scheduled(max_items, scheduled: bool = False)` — `scheduled` was used only for a log field with **zero effect** on behavior; manual and scheduled runs were byte-identical (`ai/handoff/INCIDENT_20260819_EMERGENCY_HOTFIX.md` line 1 area; full trace in `ai/handoff/INCIDENT_LEGACY_FCB5E91_LAUNCHER.md` lines 8-13). A second, independent scheduler-truth incident: a legacy pre-migration cron launcher (`deploy`'s crontab) fired invisibly in parallel with the new systemd-timer architecture for days, producing a real container run nobody expected (`ai/handoff/INCIDENT_LEGACY_FCB5E91_LAUNCHER.md` lines 1-117). `HOSTILE_ARCHITECTURE_AUDIT_20260821.md` (P2-10, lines 132-144) generalizes: "scheduler authority is fragmented" across invisible root cron, disabled `deploy` crontab, 19 user-systemd timers, and unreachable Windows Task Scheduler — "a silently-stopped schedule surfaces only as heartbeat WARNING... nothing pages if the DB itself stops being written."

**2. Natural-cycle vs manual/deploy-cycle accounting**
`ai/handoff/PRODUCTION_RESET_20260817.md` lines 27-32: a `RUN NOW` manual click on a fresh field-test DB (never had an operational epoch) was mistaken for/treated identically to a scheduled run, producing 300 fabricated "new" events indistinguishable from real cadence. Fix: `PipelineService._auto_baseline_for_first_run` (lines 62-70) makes the *first-ever run for a collector_id* — regardless of trigger source — silent, closing the manual-vs-scheduled conflation at the mechanism level rather than distinguishing triggers. `HOSTILE_ARCHITECTURE_AUDIT_20260821.md` P0-3 (lines 72-77) notes this originally covered only the no-epoch case, so "adding a new collector/brand/region to an existing, running deployment without remembering `--force-baseline` replays the flood... Safety of a normal growth operation depends on operator memory, not architecture" — later closed in Phase 8 of `WATCH_CLANK_REMEDIATION_PHASE2_20260821.md` (lines 405-409).

**3. Soak clocks and reset semantics**
`WATCH_SOAK_CONTRACT.md` (full file) defines an explicit soak evidence contract: minimum 4 successful *scheduled* acquisition runs before promotion review (line 41), with 10 ALL-required promotion gates (lines 75-91), including "No manual DB surgery was required during the soak" (gate 10) and "A process exit code of 0 is NOT evidence. Evidence is the DB rows" (line 56). No explicit mechanism found for what resets the soak clock if a manual run is interleaved — the contract instead forbids manual re-runs outside schedule ("do NOT add manual re-runs outside schedule," line 36) rather than defining reset semantics for a violation.

**4. Lifecycle states**
`WATCH_SOAK_CONTRACT.md` table (lines 22-25) shows `EXPERIMENTAL_READY_FOR_HETZNER` as a maturity state; `app/services/delivery_gate.py::experimental_delivery_blocked` gates external delivery by maturity (lines 6-18). `EXPERIMENTAL_MATURITY_COLLECTORS` is a registry set, cross-checked by `tests/test_production_wiring.py::test_soak_contract_experimental_set_matches_registry_controls` (line 18). "Retirement" (permanent removal, not "temporarily blocked") is a distinct, separately-documented lifecycle event: `ai/handoff/RETIREMENT_CITIZEN_DE.md` — removed from every production registry/CLI/scheduler surface but code/tests left intact "for future manual archaeology" (lines 78-84); explicitly not a flag ("no explicit 'deprecated' flag exists anywhere," line 51). No distinct "temporarily blocked/mothballed" state found for a *collector*; `BLOCKED`/`BACKED_OFF` exist only as per-run acquisition-health states (`app/services/health.py` line 118), not lifecycle states.

**5. Promotion readiness**
`WATCH_SOAK_CONTRACT.md` lines 75-91: 10-point manual gate; "Promotion decision belongs to the operator. No auto-promotion exists or will be added" (line 90). No incident of premature promotion was found in this repo (soak contract is dated 2026-08-25, collectors still in soak as of the doc).

**6. Source starvation / observation collapse**
Directly documented and fixed: `monochrome_rss` had 20 consecutive `ZERO_ITEMS` runs while `health.py` counted `ZERO_ITEMS` as a success status, so it read `HEALTHY` forever (`app/services/health.py` lines 190-208; found by `HOSTILE_ARCHITECTURE_AUDIT_20260821.md` P1-6, lines 102-106). Fixed via an explicit `zero_item_warning_streak` setting (default 3), documented in code, not a "buried magic number" (`app/services/health.py` lines 196-208).

**7. Config drift**
`ai/handoff/HOSTILE_ARCHITECTURE_AUDIT_20260821.md` P2-11 (lines 145-150): "Repo/systemd drift — Static units in `scripts/systemd/` are stale `/opt/watch-clank` artifacts missing gear-patrol/great-gshock-world/casio-europe; Hetzner actually uses registry-rendered units. Anyone installing from the repo gets a different fleet than production runs." Also `.deployed-id` on Hetzner remains stale ("`fcb5e91`") long after real deployment mechanism changed — misleading to a future investigator (`ai/handoff/HALL_OF_SHAME_AUTOPSY_20260817_POSTREPAIR.md` lines 204-211).

**8. Schema/deploy readiness**
Real incident (schema mismatch traced to deploy tooling, not schema-check code): `tests/test_deploy_image_tag_safety.py` lines 1-22 — `docker-compose.staging.yml`'s `image: watch-clank:${IMAGE_TAG:-soak-local}` silently resolved to a long-stale image (`soak-local`, predating migrations 008-011) whenever `IMAGE_TAG` was unset, "silently reproduced what looked like a schema-check defect" though `check_schema()` itself was correct. Fixed by requiring `${IMAGE_TAG:?message}` (fail loud) instead of `:-` (silent default) — test asserts no service may use the soft-default form (lines 41-54). Separately, `ai/handoff/CLOUD_READINESS_BLOCKERS.md` lines 64-72 documents the original outage this guards against: "DB pinned at `002_ops_statuses` while code was at `003_release_leads` ... every scheduled run failed with `no such table: source_component_states`" — root-caused to manual `alembic upgrade head` being an easy-to-skip step; resolved via `app/db/schema_check.py`, a startup check that refuses (exit 3) on any Alembic-head mismatch, paired with a separate explicit `scripts/migrate.py` (lines 111-127).

**9. Stale automation**
Same `INCIDENT_LEGACY_FCB5E91_LAUNCHER.md` — a stale cron entry from a pre-migration deployment ran unnoticed for days after migration to systemd timers (full file); root cause explicitly: "Watch Clank's migration to the new architecture ... built and verified the new 17-timer architecture but never located and disabled the old cron entry it was replacing" (lines 73-76).

**10. Retry/restart authority**
`ai/handoff/HOSTILE_ARCHITECTURE_AUDIT_20260821.md` P2-9 (lines 124-130): "Stale-run recovery can manufacture concurrency" — `stale_run_threshold_minutes=45` while force-baseline sweeps legitimately run longer (`max_items=None`); a second entrant's `recover_stale_runs()` can mark a live run FAILED and start a concurrent writer against single-writer SQLite. "WAL + 60s busy_timeout makes this usually survivable, not safe. The single-writer assumption is real but undocumented and un-enforced." `app/services/health.py` docstring (lines 1-9) explicitly separates read-only health checks from `RunLockService.recover_stale_runs`, which "remains ... the normal pipeline path"'s job — i.e., retry/restart authority is delegated to the pipeline's own lock service, not health/monitoring code.

**11. Health vs scheduler state**
Directly modeled: `app/services/health.py` lines 105-121 splits `SourceHealth` into `acquisition_state` (can it reach/interpret the OEM — BLOCKED/BACKED_OFF/BROKEN) vs `yield_state` (what has it produced — ZERO/STAGNANT/NOISY/HEALTHY), explicitly because "a persistent 403 that exits 0 is BLOCKED, never healthy" (line 117). Heartbeat overdue logic (lines 217-224): a source with no successful run within 3× its expected cadence flags WARNING "even if its most recent run technically succeeded a long time ago." This whole module exists because of an earlier documented conflation (comment dated 2026-08-24, line 113).

**12. Remote host/deployment truth**
`ai/handoff/HETZNER_DEPLOYMENT.md` lines 154-170 documents a "known limitation, disclosed honestly": an old, invisible `casio_multi` invocation mechanism (likely root's crontab, never found — no root access) "is very likely still firing on its own ~90-minute cadence against the **same** volume" alongside the new systemd-scheduled equivalent — a real remote-host-truth gap the operators explicitly could not close and flagged for later root-access follow-up. Three-way provenance verification pattern (git SHA vs OCI label vs runtime `get_identity()`) used to establish "what's actually deployed" (`INCIDENT_LEGACY_FCB5E91_LAUNCHER.md` lines 161-168).

**13. "Scheduled" vs "actually running" (live execution state)**
`app/services/health.py` `stale_running_count` (lines 390-393) and `active_locks` (lines 395-398) are the live/current-execution-state signals, distinct from `EXPECTED_CADENCE_MINUTES` (the schedule definition, lines 71-102). `HealthSnapshot.stale_running_count` flags `CollectorRun` rows stuck at `status == "RUNNING"` past `stale_run_threshold_minutes`.

**14. Partial deploys / stale code**
`INCIDENT_LEGACY_FCB5E91_LAUNCHER.md` is itself a partial-migration incident: old code (`watch-clank:fcb5e91`) kept running via a forgotten launcher alongside new code (`watch-clank:c81ebed`) on the same shared volume for days (full file, esp. lines 1-20, 108-133). `docker-compose.staging.yml`'s stale-tag-default bug (`test_deploy_image_tag_safety.py`) is a second, distinct partial-deploy-adjacent defect (old image silently used post-migration).

**15. Safe manual intervention during soak**
`WATCH_SOAK_CONTRACT.md` line 36: "A BLOCKED run exits the normal path; do NOT add manual re-runs outside schedule" — explicit prohibition rather than a documented safe mechanism. Gate 10 (line 88) treats *any* manual DB surgery during soak as promotion-disqualifying evidence, but no code-level guard was found preventing an operator from running a collector manually mid-soak and corrupting the "≥4 successful *scheduled* runs" count — this appears to be a documented-policy control, not an enforced one (no test found gating this).

**Incidents in this repo (dated, with root cause/fix/recurrence):**
- 2026-08-14 — `INCIDENT_SILENT_SCHEDULED_NOTIFICATIONS.md`: Casio's production path never created `Event` rows (missing `emit_events` default); fixed by adding the parameter; recurrence risk noted explicitly: "invariant is call-site opt-in (`emit_events=False` defaults), not structural — a new runner can still silently ingest" (`HOSTILE_ARCHITECTURE_AUDIT_20260821.md` line 174).
- 2026-08-14/15 — `INCIDENT_LEGACY_FCB5E91_LAUNCHER.md`: stale cron launcher fired alongside new systemd timers; fix commented out (not deleted) the crontab lines; explicitly noted as a fleet-wide pattern ("this isn't unique to Watch Clank," lines 67-70), citing smartphone-clank's identical prior fix.
- 2026-08-17 — `PRODUCTION_RESET_20260817.md` / `HALL_OF_SHAME_AUTOPSY_20260817_POSTREPAIR.md`: first-ever RUN NOW on empty DB flooded 300 fake NEW_REFERENCE events; fixed via `_auto_baseline_for_first_run`.
- 2026-08-18 — `CITIZEN_STALE_FLOOD_AUTOPSY_20260818.md`: 47 stale/out-of-stock Citizen SKUs surfaced as NEW_REFERENCE from genuine upstream catalogue churn; fixed with bounded per-item availability enrichment.
- 2026-08-19 — `INCIDENT_20260819_EMERGENCY_HOTFIX.md`: `published_at` misused as launch-date proxy causing false positives; multiple fixes (accessory gate, staleness gate, catch-up tooling).
- 2026-08-21 — `HOSTILE_ARCHITECTURE_AUDIT_20260821.md`: broad audit re-litigating prior "fixed" incidents, found 3 new defects (Timex regex, Windows `os.kill` lock-liveness hazard that could kill the wrong process, ZERO_ITEMS health gap).
- 2026-08-22 (referenced in test) — migrate-tooling stale-image incident, same root class as the legacy-launcher incident, fixed via required `IMAGE_TAG`.

**Lineage evidence:** Watch Clank explicitly ported patterns from other Clanks: `Dockerfile:30` "Pattern proven on OEM Radar / Chinese Tech Wire / Feature Phone [Clank]"; `app/core/identity.py:3` "Same pattern already proven on OEM Radar, Chinese Tech Wire, Feature Phone"; `tests/test_identity.py:3` mirrors the same; `STAGING_RELEASE_RUNBOOK.md` line 45 cites "the same proven pattern as Chinese Tech Wire" for the external-flock-wrapper requirement; `HANDOFF.md:424` and `INCIDENT_LEGACY_FCB5E91_LAUNCHER.md:123` list sibling Clanks whose crontab entries were checked as part of the incident response.

---

## Repo: `C:\Users\anil\Clanks\oem-radar`

**1. Scheduler truth vs actual execution**
Directly and explicitly documented: `docs/CURRENT_STATUS.md` lines 41-46 — a manually triggered real run confirmed "20 of 21 sources correctly skipped as not-due (`crawled within min_interval` — confirms an hourly OS trigger does **not** mean hourly Medion crawls)." This is a first-class distinction in this codebase between the OS scheduler firing and per-source cadence gating actually executing.

**2. Natural-cycle vs manual/deploy-cycle accounting**
Extensively documented as "Epoch" bookkeeping. `docs/SOAK_ARCHIVE_2026-08.md` lines 20-23: "None of this was a deliberate production run — no scheduled task for this project has ever existed on this machine, so every one of the archive's 59 `crawler_runs` rows is manual." `docs/DATABASE_LIFECYCLE.md` lines 22-33 formalizes Epoch 1 (dev+accidental soak, all manual) vs Epoch 2 (clean production baseline) — "documentation-only bookkeeping — there is no `epoch` column anywhere in the schema. The epoch boundary *is* 'which file is currently at `data/radar.db`.'" `docs/CURRENT_STATUS.md` lines 12-26 documents a real conflation incident: baseline (first-crawl) events were tagged `meta["baseline"]=True` but nothing downstream ever read the tag, so 1,875 baseline records appeared identical to genuine alerts in dashboards and signal/noise metrics — fixed with a shared `EXCLUDE_BASELINE_EVENTS_SQL` predicate.

**3. Soak clocks and reset semantics**
`data/experimental/japan-mini-pc-five-day-soak.db` — a literal 5-day soak clock exists as a database file. `src/oem_radar/experimental/japan_mini_pc_soak.py` lines 154, 190: `baseline = not self.store.has_baseline()` — the soak's own baseline/reset state is a boolean derived from "has any run ever succeeded," stored per experiment DB, isolated from the production `radar.db` (fetched read-only only for global-model cross-check, line 6). `docs/BANKAI_PAUSE_HANDOFF.md` lines 17-24 documents live soaks (Lenovo, ASUS) with explicit cadence (`PT6H`), overlap policy (`IgnoreNew`), and isolated telemetry (`soak-runs.jsonl`) — deliberately separated from the production Hourly Crawl task so a manual/experimental run cannot touch the soak clock or vice versa.

**4. Lifecycle states**
Explicit enumerated states found in `docs/BANKAI_PAUSE_HANDOFF.md`: `EXPERIMENTAL / SOAKING` (Lenovo, ASUS, line 28/36), `RESEARCH_ONLY` (Acer, JD — line 47-49), plain `EXPERIMENTAL` corroborating-only (PSREF, line 45). No collector is shown reaching a "PRODUCTION" state in this doc. `docs/ARCHITECTURE.md` grep for lifecycle vocabulary returned nothing — lifecycle states appear to live in prose handoff docs, not as a coded enum. No distinct "permanently disabled" vs "temporarily blocked" collector state was found (health-per-run states `ok/degraded/failed` exist at `tests/test_collector_health_stage41.py` lines 108-127, but these are per-run acquisition outcomes, not lifecycle states).

**5. Promotion readiness**
`docs/BANKAI_PAUSE_HANDOFF.md` "Resume triggers" (lines 62-76) is the closest analogue to a promotion gate: explicit conditions (a real sitemap delta, repeated soak failure, host migration, deliberate decision) before resuming/promoting work, plus an explicit non-mechanical evaluation checklist ("classify HIT/INTERESTING/NOISE/BUG, decide whether it is genuinely new or merely newly indexed... Do not change the collector merely because the first delta appears," lines 73-76) — readiness assessment is manual/human judgment, not automated. No incident of premature promotion found; both Lenovo and ASUS show 0/0 deltas/candidates as of the doc (lines 30, 39), i.e., still pre-promotion.

**6. Source starvation / observation collapse**
`tests/test_collector_health_stage41.py` lines 74-140 implements exactly this: `CollectorHealthConfig` with `minimum_fraction_of_previous_catalog`/`warn_fraction_of_previous_catalog` thresholds that classify a shrinking catalog as `degraded`/`failed` (`CATALOG_WARN_THRESHOLD`, `CATALOG_FAILURE_THRESHOLD`) and an explicit `unexpected_zero_is_failure` flag (`UNEXPECTED_ZERO`) — i.e., a source that goes to zero silently is caught by config-driven health classification, not left silent. `docs/DATABASE_LIFECYCLE.md` line 200-208 also treats "notifications has zero sent rows" as the thing that must hold true on a fresh source's first crawl, with an explicit stop-and-investigate rule if violated.

**7. Config drift**
`ai/handoff/KNOWN_ISSUES.md` lines 4-12: "Backup portability quirk (WAL header inheritance)" — a real drift between what the live DB's journal mode was vs. what the backup copy silently inherited, breaking read-only restores; fixed by explicit checkpoint-to-DELETE after backup. `docs/DATABASE_LIFECYCLE.md` line 172-176 requires confirming `oem-radar validate`/`coverage` source/OEM/engine counts match pre-reset numbers exactly after any DB reset, "if they don't, something other than the DB reset changed, and that needs separate investigation" — an explicit config-drift tripwire.

**8. Schema/deploy readiness**
`ai/handoff/DEPLOYMENT_PROCEDURE.md` (full file): mandates cross-checking `git rev-parse HEAD` == OCI `org.opencontainers.image.revision` label == `oem-radar identity`'s `source_revision` before trusting any deployment; explicitly: "If they don't match, do not assume the deployment is correct — investigate before proceeding, the same way a stale-deployment check should (see the 2026-08-09 OEM Radar Hetzner revision verification for a worked example...)" — implies a real prior incident of this kind, though the referenced worked example itself was not found as a separate file in this survey. `ai/handoff/CLOUD_OEM_RADAR_REPORT.md` line 9: `operational_state: degraded-until-first-run (truthful: no run history on a fresh volume reports "degraded", not "healthy")` — an explicit honest-default design choice for schema/deploy readiness signaling.

**9. Stale automation**
`docs/DATABASE_LIFECYCLE.md` lines 226-249 documents a real, reproducible scheduler-registration bug: `schtasks /tr` cannot be correctly quoted when the project path contains a space, silently producing a task that reports `SUCCESS` from `schtasks` but either runs the wrong program or literally no-ops — "the failure is only visible by inspecting the registered `Action` afterward." Fixed by switching to `Register-ScheduledTask` with separate `Execute`/`Argument` parameters (`install-hourly-task.ps1`). Same bug independently documented in `docs/CURRENT_STATUS.md` lines 27-40, including a second unrelated bug in the same batch file (unescaped `)` causing both success and failure branches to print on real success).

**10. Retry/restart authority**
`src/oem_radar/core/run_lock.py` (full file, esp. lines 1-34) documents a real, named, dated fleet incident: "the NAS canary: a run crashed mid-crawl on 2026-08-23, left `{"pid": 1, ...}` behind, and every one of the ~81 hourly scheduler fires since then also *was* PID 1 in its own namespace, so each one concluded 'the old run is still alive' and refused to start — forever, with no possible self-recovery. See Diagnostic Clank incident `5f280abf-4bf7-423d-be47-52db5dfb2b72`." Root cause: PID-liveness checks are fundamentally unsound across Docker PID namespaces (every container is PID 1 to itself). Fix: OS-level advisory file lock (`fcntl.flock`/`msvcrt.locking`) instead of PID-liveness — "No liveness check, no staleness window, no PID at all is consulted to decide whether the lock can be acquired" (line 24-25). Explicitly non-blocking: "a refusal means 'another run is genuinely active right now,' not 'wait'" (line 32-33) — no automatic retry.

**11. Health vs scheduler state**
`ai/handoff/CLOUD_OEM_RADAR_REPORT.md` line 9 (quoted above under #8) is the clearest single statement: scheduler/deployment presence does not imply health; health is truthfully derived from actual run history. `tests/test_collector_health_stage41.py` shows health computed from real catalog-size deltas per run, independent of whether the source is scheduled/enabled.

**12. Remote host/deployment truth**
`ai/handoff/DEPLOYMENT_PROCEDURE.md` (full file) is entirely about this: never trust a checkout or tag alone; three-way SHA cross-check required. `ai/handoff/ROLLBACK.md` lines 16-20: "Not applicable yet — nothing has been deployed. `docker-compose.yml` requires an explicit `IMAGE_TAG` (immutable commit SHA), so there is no bare `:latest` reference to accidentally roll forward or back to."

**13. "Scheduled" vs "actually running"**
`docs/DATABASE_LIFECYCLE.md` step 1 (lines 40-56) — before any DB operation, explicitly checks for a live lock file, a `crawler_runs` row at `status='running'`, a dashboard process holding the DB, and any about-to-fire OS task — i.e., "is it scheduled" and "is it currently running" are treated as separately-verified facts, not inferred from each other.

**14. Partial deploys / stale code**
`docs/CURRENT_STATUS.md` lines 86-90: "One real orphaned run found and corrected before archiving: `khadas-sitemap` was stuck at `status='running'` from an interrupted dashboard-triggered crawl" — a partial-execution artifact, corrected via the real application code path (`SqliteStore.run_finished`), not hand SQL. `ai/handoff/DEPLOYMENT_PROCEDURE.md`'s entire mandate exists to prevent partial/stale deploys going undetected.

**15. Safe manual intervention during soak**
`src/oem_radar/experimental/japan_mini_pc_soak.py` lines 8-9: "`radar.db` is opened read-only solely to enrich the GEEKOM global comparison; all mutable state lives in the experiment database" — architecturally isolates soak state from production so a manual production run cannot corrupt the soak clock. `docs/BANKAI_PAUSE_HANDOFF.md` line 20: experimental soak "invokes the portable Python wrapper... State and telemetry are isolated in `data/experimental/`... The production `OEM Radar Hourly Crawl` task remains separate and unchanged" — explicit separation as the safety mechanism, rather than a lock/gate on concurrent manual runs during soak.

**Incidents in this repo (dated, with root cause/fix/recurrence):**
- 2026-08-08 — Epoch 1→2 cutover (`docs/DATABASE_LIFECYCLE.md`, `docs/SOAK_ARCHIVE_2026-08.md`, `docs/CURRENT_STATUS.md`): baseline events masquerading as fresh alerts (1,875 rows); scheduler-registration quoting bug; orphaned `khadas-sitemap` run. All fixed and documented; recurrence risk explicitly generalized in the scheduler bug ("if this project is ever moved to a path *without* a space, `schtasks /tr` would likely have worked fine — the bug is specific to this repo's own folder name," `docs/DATABASE_LIFECYCLE.md` lines 244-248).
- 2026-08-09 (referenced but not independently located as a standalone doc in this repo) — "OEM Radar Hetzner revision verification," cited in `ai/handoff/DEPLOYMENT_PROCEDURE.md` line 53 as precedent for the three-way SHA-match discipline.
- 2026-08-23 — NAS canary stale-lock incident (`src/oem_radar/core/run_lock.py` lines 11-16): ~81 consecutive hourly scheduler fires all refused to start after one crash left a `pid:1` lock; cross-referenced to Diagnostic Clank incident ID `5f280abf-4bf7-423d-be47-52db5dfb2b72`. Fix (OS-level flock) explicitly generalizable — the failure mode (PID-liveness checks across container PID namespaces) is fleet-wide, not OEM-Radar-specific, and the fix was itself imported from another Clank (see lineage below), implying the bug class could recur anywhere still using PID-liveness locking.
- Undated, "found this phase" — WAL-header-inheritance backup portability bug (`ai/handoff/KNOWN_ISSUES.md` lines 4-12).

**Lineage evidence:** `src/oem_radar/core/run_lock.py` lines 27-30: "Ported from Free Game Tracker's `newsroom/run_lock.py` (same architecture, first proven there) and adapted to preserve OEM Radar's existing `RunLock.acquire()`/`lock.release()` call-site API" — explicit, named cross-repo lineage (convergent fix imported wholesale from a sibling Clank, not independently invented). `watch-clank`'s `tests/test_deploy_image_tag_safety.py` line 20 explicitly cites "OEM Radar's own `docker-compose.yml`" as the pattern its own fix now matches — i.e., lineage runs in both directions across this pair (OEM Radar → Free Game Tracker's pattern flowing in; OEM Radar's `IMAGE_TAG` convention flowing out to Watch Clank).

---

## Cross-repo pattern summary (observed, not prescribed)

- Both repos independently arrived at "distinguish OS-scheduler firing from actual per-source execution" (topic 1/13) — watch-clank via `scheduled` being a no-op flag then fixed; oem-radar via `min_interval` gating within an hourly trigger. Convergent, not shared code.
- Both repos independently built an "epoch/baseline" concept to separate natural production cadence from onboarding/backfill/manual catch-up (topic 2), with near-identical vocabulary ("baseline," "epoch") despite no shared code found for this specific mechanism.
- The run-lock stale-PID-across-containers bug (topic 10) is explicitly fleet-wide lineage: OEM Radar imported the fix from Free Game Tracker; Watch Clank has an analogous but distinct bug (`_pid_alive` on Windows killing the wrong process, `HOSTILE_ARCHITECTURE_AUDIT_20260821.md` P1-7) fixed independently in the same audit window (2026-08-21), suggesting the underlying failure class (liveness-based lock staleness) is a recurring fleet risk not yet unified into one shared primitive across all Clanks.
- Deploy-image-tag safety (`IMAGE_TAG` required vs defaulted) is explicit shared convention: OEM Radar's convention was copied into Watch Clank's regression test as the standard to match.

---

## Survey 2 of 6: chinese-tech-wire + korean-tech-wire

# Pass 0A Evidence Inventory: Operations Domain — chinese-tech-wire &amp; korean-tech-wire

Read-only survey. No files modified. All citations are `path:line`.

---

## Repo: chinese-tech-wire (`C:\Users\anil\Clanks\chinese-tech-wire`)

### 1. Scheduler truth vs actual execution
Direct evidence of a dedicated read-only scheduler-truth query, kept deliberately separate from execution truth:
- `pipeline/scheduler_status.py:1-8` — module docstring: "best-effort, read-only Windows Task Scheduler status... Never modifies the task — query only, via schtasks.exe." Returns `available`, `status`, `next_run`, `last_run`, `last_result`.
- `pipeline/operations.py:217-221` — `runtime_snapshot()` calls `get_scheduler_status()` and merges it into `/api/health/runtime` alongside `IngestionRun` DB state (`current_run`, `last_completed_run`), i.e., scheduler-claimed state and DB-recorded execution state are surfaced side-by-side but not cross-validated against each other.
- Trigger classification is **self-asserted, not schtasks-verified**: `main.py:1017` — `trigger = "SCHEDULED" if args.scheduled else "MANUAL"`, driven purely by a CLI flag (`main.py:489-490`) that anyone invoking the script manually could pass. Nothing checks that a `SCHEDULED`-tagged run actually originated from `schtasks.exe`.
- Incident (see topic 9 below): `ai/handoff/KNOWN_ISSUES.md:33-36` documents 13 genuine cron-triggered cycles being reconciled against real elapsed time as a resolved verification gap ("External scheduler firing over real elapsed time: resolved").
- `ai/handoff/CLOUD_CHINESE_TECH_WIRE_REPORT.md:14` — `scheduler_verified: false` in the same YAML block where `docker_build_verified: true`, `persistent_state_verified: true` — explicit acknowledgment that deploy verification and scheduler verification are tracked as separate, independently-gated facts.

### 2. Natural-cycle vs manual/deploy-cycle accounting
- `main.py:1017`, `pipeline/operations.py:6-8` (module docstring: "starts the exact same `python main.py --full-once` process the Windows Task Scheduler already uses. All actual collection work happens in that separate process, not in the web request") and `pipeline/operations.py:150-159` (`launch_manual_run` docstring: "no `--scheduled`, so it's never confused with a Task Scheduler run") show a deliberate `SCHEDULED` vs `MANUAL` trigger field persisted per `IngestionRun`.
- `pipeline/operations.py:114-130` (`failed_sources_for_run`) and `187-207` (`correlate_new_run`) show manual runs are tracked/correlated distinctly from natural runs via `trigger == "MANUAL"` queries.
- Conflation risk is structural, not just theoretical: the `SCHEDULED` label is unverified self-report (see topic 1) — a manually-run `--scheduled` invocation would be indistinguishable from a real Task Scheduler firing in the stored data.

### 3. Soak clocks and reset semantics
- `ai/handoff/STAGING_RELEASE_RUNBOOK.md:64-69` — explicit rule: "**Soak restarts on material change** — unchanged rule: a build that changes scraper/pipeline/scoring logic starts its soak clock at zero, regardless of how long the previous build had been running cleanly." Also documents a case where a provenance-only change (`552ffff`) did *not* restart the soak clock because it didn't touch scraper/pipeline/scoring logic.
- This rule is **documented, not code-enforced** — no code was found that automatically classifies a diff as "material" and resets a soak counter; the decision is a human judgment call recorded in the runbook only.
- Soak status itself is tracked as free-text in the runbook (`ai/handoff/STAGING_RELEASE_RUNBOOK.md:75-84`, `soak start:`, `cycles completed:`), not a queryable field — no schema-level soak-clock artifact was found in `database/models.py`.

### 4/5. Lifecycle states / promotion readiness
Chinese-tech-wire has **no per-source EXPERIMENTAL/PRODUCTION lifecycle state machine** (unlike korean-tech-wire). Instead it has two separate, non-unified maturity concepts:
- Whole-application `release_channel`, defaulting to `"soaking"`: `config.py:66` — `release_channel: str = Field(default="soaking", alias="CTW_RELEASE_CHANNEL")`. `ai/handoff/DECISIONS.md:8-14` explains this is deliberately "the least-trusted channel name appropriate to this clank's tier... since Tier B has no path to anything more trusted in this phase." No promotion mechanism/gate for this exists in the repo — `ai/handoff/CLOUD_CHINESE_TECH_WIRE_REPORT.md:78-80`: "Explicit promotion approval — per the brief, passing tests never self-authorize anything beyond soak."
- Per-source `KNOWN_STATUS` labels (`pipeline/source_health.py:43-54`): `DISABLED`, `BLOCKED`, `PARTIAL` — these are **documented policy statements, not live probe results** (comment at line 40-42: "not a live probe result, a policy statement"). No `EXPERIMENTAL`/`PRODUCTION` distinction exists for individual sources; all enabled sources run in every scheduled cycle regardless of maturity.
- No "permanently disabled" vs "temporarily blocked" state machine — `DISABLED` (ptt, geekbench) and `BLOCKED` (hkepc, xfastest) are both just static dict entries with no transition logic, timestamps, or review-date fields.

### 6. Source starvation / observation collapse
Explicit, well-developed detection logic:
- `pipeline/source_health.py:9-19` — module docstring explicitly separates "QUIET" (found&gt;0, new==0 — normal) from "DEGRADED" (found==0 despite success, or soft-blocked — "real signal something is wrong").
- `pipeline/source_health.py:156-166` — `found_zero_streak` computed distinctly from `new_zero_streak` (lines 145-154), specifically to catch "possible parser drift / silent structural change" (line 220-225: `status = "DEGRADED"`, note `"found=0 on {n} consecutive clean fetches — possible parser drift"`).
- Real starvation incident: PTT forum — `pipeline/source_health.py:48-53` comment: "PTT's own web gateway returned HTTP 500 'Server Too Busy' on the board index, hotboards, another board, and 10/10 sampled stored article URLs — confirmed via direct probe... Disabled from active production pending PTT-side recovery." Cross-referenced test: `tests/test_ptt_disablement.py` (file exists, not read in full but named directly for this).

### 7. Config drift
- `ai/handoff/DECISIONS.md:28-34` — explicit, self-flagged drift risk: "`runtime_bridge.py` duplicates `web/app.py`'s `CTW_VERSION` constant rather than importing it... The constant is documented as needing to stay in sync with `web/app.py:CTW_VERSION`; flagged in FILES_CHANGED.md/KNOWN_ISSUES.md rather than silently risking drift." This is a maintained-by-convention duplication, i.e. an accepted, known drift vector.
- Deploy-target divergence: `ai/handoff/ROLLBACK.md:26-33` — the Windows dev-machine production checkout stays permanently at `52fdd72` while GitHub/Hetzner moved to `552ffff`: "The production directory on the original Windows development machine was never touched by this migration and remains at `52fdd72` intentionally — it is not a rollback target... all GitHub changes went through a separate working copy, never the local production checkout." Explicit "never hot-patch Hetzner" rule referenced at `ROLLBACK.md:27-29`.
- Two independent execution-authority mechanisms for the same app across environments: Windows Task Scheduler with `MultipleInstances IgnoreNew` (`scripts/install_scheduler.ps1:85-91`) locally vs. cron + external `flock` lock on Hetzner (`ai/handoff/KNOWN_ISSUES.md:37-41`, `ai/handoff/STAGING_RELEASE_RUNBOOK.md:51-58`) — the app itself has no in-process run-lock (`KNOWN_ISSUES.md:37`: "this clank has no in-application run-lock (unlike OEM Radar/SemInt)").

### 8. Schema/deploy readiness
- `database/db.py:104-129` (`migrate_schema`) — additive-only migration (`ALTER TABLE ... ADD COLUMN`, `CREATE INDEX IF NOT EXISTS`), run automatically at `init_db()` (`database/db.py:150-155`) on every process start, not as a separate pre-deploy gate. No schema-version table, no explicit pre-traffic-switch schema check found.
- `ai/handoff/DECISIONS.md:18` — "Two overlapping schema-migration mechanisms exist... `Base.metadata.create_all()` (new tables) plus a hand-rolled `migrate_schema()`... This is pre-existing and untouched." Self-flagged as pre-existing architectural debt, not fixed.
- `ai/handoff/CLOUD_CHINESE_TECH_WIRE_REPORT.md:20-21` — `schema_changed: false`, `contracts_changed: false` tracked as explicit release-report fields, implying schema-change status is manually attested per release, not automatically verified against the target host before traffic switches.

### 9. Stale automation
- `ai/handoff/KNOWN_ISSUES.md:33-36` — the described incident (external scheduler cron firing verified against real elapsed time, 13 cycles from `2026-08-09 19:47 UTC` to `2026-08-10 06:00 UTC`, "5 * * * *") is essentially a "did the automation actually keep firing as configured, unmodified, over real time" check — evidence the team explicitly worried about drift between a configured cron entry and what actually executes over days.
- No evidence found of an automation that "nobody remembered existed" being discovered in this repo — the closest is the deliberate distinction between the still-active Windows Task Scheduler entry (dev machine) and the newer Hetzner cron entry; `ai/handoff/hetzner-migration` equivalent for chinese-tech-wire wasn't found as a doc, but `ROLLBACK.md:26-33` shows awareness that two separate schedule-holding hosts (Windows + Hetzner) now exist and must not both be "live."

### 10. Retry/restart authority
- Automatic retry: none found at the application level for chinese-tech-wire (no backoff/retry module analogous to korean-tech-wire's `scheduling.py`).
- Restart/duplicate-execution protection is external, not code-level: `ai/handoff/KNOWN_ISSUES.md:37-41`, `ai/handoff/STAGING_RELEASE_RUNBOOK.md:51-58` — `flock -n /tmp/ctw-run.lock` wraps the cron invocation; verified under deliberate overlap: "the second was refused immediately by `flock` (exit 1, no output, container never even started) while the first continued to a normal `SUCCESS` completion."
- Windows-side protection: `scripts/install_scheduler.ps1:85-91` sets `-MultipleInstances IgnoreNew` and a 2-hour `ExecutionTimeLimit`.
- Manual-restart authority for a stuck/crashed run: `pipeline/operations.py:29-32, 86-111` — `STALE_RUNNING_THRESHOLD_HOURS = 2.0`; a `RUNNING` `IngestionRun` row older than 2 hours is treated as crashed/abandoned and "never deleted or rewritten... it simply stops blocking new launches" (line 89-93). This is exactly a soft "stuck job" recovery gate distinct from the Task Scheduler's own 2-hour `ExecutionTimeLimit` — two independently-configured 2-hour ceilings in two different layers (scheduler process kill vs. app-level stale-row ignore), not obviously kept in sync by any single source of truth.

### 11. Health vs scheduler state
- Directly modeled as separate fields merged at read time: `pipeline/operations.py:210-259` (`runtime_snapshot`) returns `scheduler` (from `scheduler_status.py`, OS-level) and `current_run`/`last_completed_run` (DB-level, health) as siblings in one payload — no single boolean conflates them.
- `ai/handoff/DECISIONS.md:36-41` — explicit rule that a fresh container with **zero** `ingestion_runs` rows reports health `"unknown"`, not `"healthy"`: "a soak container that has proven nothing yet must not claim it is fine." This is a deliberate anti-pattern guard against exactly the "enabled masks broken" failure mode.

### 12/14. Remote host/deployment truth, partial deploys
- `ai/handoff/STAGING_RELEASE_RUNBOOK.md:23-33` (per-release identity table) and `ROLLBACK.md:9-22` (current-deployed-revision table) are hand-maintained tables recording what commit/image is believed live on Hetzner — no automated remote-state reconciliation found; provenance is checked via three independently-computed labels being compared for equality (`STAGING_RELEASE_RUNBOOK.md:41-43`: OCI label, `--identity` output, GitHub SHA all confirmed equal) rather than a single source of truth.
- `ROLLBACK.md:35-49` — rollback is a one-line `.deployed-id` file edit picked up by `deploy_run.sh` on the *next* cron tick, meaning there is a window between rollback intent and actual effect bounded by the cron interval (hourly) — a partial-deploy-adjacent gap, though not an observed incident.
- No incident of an actually-partial deploy (some containers/processes on new code, some on old) was found documented.

### 15. Safe manual intervention during soak
- `ai/handoff/STAGING_RELEASE_RUNBOOK.md:66-69` states soak continuation/reset is a policy decision made by inspecting whether a change touched "scraper/pipeline/scoring logic" — this determination appears to be manual/human judgment at release-record-writing time, not enforced by the manual-run code path itself.
- `pipeline/operations.py:150-166` (`launch_manual_run`) allows a per-source or full-cycle manual run at any time via a "Health page" button, gated only by `CTW_DISABLE_COLLECTOR_LAUNCH` env var (line 160-161) and the stale-running check (topic 10) — no code was found that treats a manual run specially with respect to soak-clock integrity (e.g., no flag preventing a manual run from being miscounted as a "clean scheduled cycle" in soak evidence). This is a plausible latent gap: the soak evidence in `STAGING_RELEASE_RUNBOOK.md:75-84` counts "13 genuine cron-triggered cycles" specifically (implying manual runs are excluded from soak-cycle counting by convention), but the counting itself is manual/narrative, not queried via `trigger == "SCHEDULED"` programmatically in any script found.

---

## Repo: korean-tech-wire (`C:\Users\anil\Clanks\korean-tech-wire`)

### 1. Scheduler truth vs actual execution
- No OS-level scheduler-query module exists (no `schtasks`/`systemctl` introspection analogous to chinese-tech-wire's `scheduler_status.py`). Instead, "due" is entirely derived from persisted DB history, not from asking the scheduler anything: `src/korean_tech_wire/scheduling.py:20-45` (`SourceDueState`, `is_due`) — "Facts derived from persisted run history for one source; no wall-clock reads" and "Everything takes `now` as an explicit parameter — nothing reads the wall clock internally."
- Documented incident where this very design still failed to catch a scheduler/execution gap: `docs/stage4.1-reliability-repair.md:5-38` — **Defect 1, "soak due-gating."**
  - **Root cause**: `run_soak`'s `if_due` check treated the fleet as one unit, skipping a cycle only if *every* selected source had a recent success; because SK hynix stopped succeeding on 2026-08-10, the fleet was "permanently due," and the 30-minute systemd timer ran a full 5-source cycle every wake instead of the documented 2-hour cadence (`stage4.1-reliability-repair.md:9`).
  - **Confirmed via** `source_run_health.attempted_at` gap analysis (median ≈1800s vs expected 7200s) and systemd journal cross-check.
  - **Impact**: ~4x intended request rate sustained "for over a week" (`docs/stage4-editorial-yield.md:33`).
  - **Fix**: per-source due evaluation (`src/korean_tech_wire/storage/database.py` `source_due_state`, `src/korean_tech_wire/scheduling.py:59-61` `due_sources`), 15 new regression tests in `tests/test_scheduling.py` (per `stage4.1-reliability-repair.md:34-38`), including a fake-clock-based "backoff survives a simulated process restart" test.
  - **Recurrence risk**: this exact class of bug (a whole-fleet AND-gate over per-item due-state, where one permanently-failing item masks the schedule for all) is a generic pattern that could recur in any Clank using an all-must-succeed gating condition — worth flagging as a fleet-wide pattern, not korean-tech-wire-specific.

### 2. Natural-cycle vs manual/deploy-cycle accounting
- **No schema-level trigger/origin field exists.** `src/korean_tech_wire/storage/database.py:17` — `CREATE TABLE runs (id INTEGER PRIMARY KEY, source_id TEXT, started_at TEXT NOT NULL, finished_at TEXT, status TEXT, summary_json TEXT)` — no `trigger`/`source_of_invocation` column, unlike chinese-tech-wire's `IngestionRun.trigger`.
- Despite this, promotion evidence explicitly claims "natural" origin in prose: `config/sources.yaml:12-14` — "2026-08-30 natural production proof: run_id 2708, 15:48:57Z, natural due-aware scheduler fire — fetch ok, 4 accepted / 1 rejected / 0 new / 4 resighted." This is a **documentation-only claim, unverifiable from the DB schema itself** — there is no stored field that would let an auditor later confirm run_id 2708 was scheduler-fired rather than a manually-invoked `korean-tech-wire run` that happened to be due. This is a real conflation risk matching topic 2's concern directly.
- `config/sources.yaml:6-11` also documents a "quiet-source clause" promotion using "~200 cycles, 99% success" as natural-cadence evidence, again asserted narratively.

### 3. Soak clocks and reset semantics
- "Soak" in this repo is the *collection-running command itself* (`src/korean_tech_wire/soak.py:18-29`, docstring: "Run normal collectors in resumable cycles; SQLite health history is the resume state"), not a separate maturity/burn-in timer. There is no distinct "soak clock" data structure — soak "progress" is just the accumulated `source_run_health` row history.
- `docs/hetzner-migration.md:3` — explicit design intent: "This procedure preserves Stage 4 evidence. It does not reset the soak, alter source lifecycles, or run collectors merely to prove deployment." And `hetzner-migration.md:17`: "Do not start a fresh source cycle before the persisted two-hour cadence says it is due" during migration — i.e., a deliberate rule to avoid a deploy/migration event artificially advancing the soak/cadence clock.
- Because due-ness is derived purely from `source_run_health` timestamps (topic 1), a deploy or host migration cannot reset it by design — confirmed explicitly at `docs/hetzner-migration.md:85`: "`--if-due` consults persisted successful health rows for every enabled source, so changing the server timezone or moving hosts does not reset the two-hour cadence." Also `docs/stage4.1-reliability-repair.md:32`: "a service restart... does not reset a persistently-failing source back into full-frequency hammering."

### 4/5. Lifecycle states / promotion readiness
- Two explicit states only: `EXPERIMENTAL` / `PRODUCTION` (`docs/promotion-policy.md:3`, `config/sources.yaml` per-source `status:` field). No formal "mothballed"/"permanently disabled" state distinct from "temporarily blocked" — `HOST-BLOCKED` is a **prose classification inside a lifecycle-repair doc**, not a stored lifecycle value; the source (`sk_hynix_newsroom`) stays `status: PRODUCTION` in `config/sources.yaml:53-60` even while completely non-functional (`docs/stage4.1-reliability-repair.md:61-69`).
- Promotion policy (`docs/promotion-policy.md:1-19`) is explicit and manual: PROMOTE / CONTINUE EXPERIMENTAL / DEFER / REWORK, evaluated by a human reviewing `korean-tech-wire health --source &lt;id&gt;` output — no automatic promotion.
- Promotion history trail is preserved in `config/sources.yaml:1-14` header comments (Stage 4 closeout 2026-08-19, 2026-08-25 additions, 2026-08-30 LG Display promotion) — functions as an informal changelog/audit trail but is not append-only structured data (just YAML comments, editable/overwritable).
- Confirmed **REWORK** decision (near-miss promotion issue, not quite "premature promotion" but adjacent): Samsung Newsroom Korea — `docs/stage4-editorial-yield.md:45,52` — 403/403 perfect run reliability (looks promotable on reliability alone) but **0 of 19,344+ discovered items ever rejected** because `editorial/filtering.py` has no branch for `samsung_newsroom_kr` (confirmed by code read, per the doc) — "the collector is reliable but has no relevance filter... most of what it currently persists is PR/marketing/lifestyle noise." This is a documented case of reliability metrics alone being insufficient/misleading for a promotion decision, caught before promotion (not after).

### 6. Source starvation / observation collapse
- `docs/promotion-policy.md:18` — explicit rule: "An unexpected drop from an established nonzero discovery baseline to zero is a source-health failure. Zero new articles is normal." (distinguishes "new" vs "discovered/references" zero, same conceptual split as chinese-tech-wire's `source_health.py`).
- `docs/architecture.md:44` — "Zero *discovered references* after a populated baseline is treated as an unexpected parser/source-health failure."
- Real starvation incident: SK hynix — `docs/stage4-editorial-yield.md:27-29,37` — production source received **0 new articles for the entire ~8.5-day Stage 4 soak** due to a host-level 403 block; caught via `korean-tech-wire health` showing "410 attempts, 9 successes... 0 consecutive successes." Diagnosed in depth in `docs/stage4.1-reliability-repair.md:40-69` (see incident write-up below).
- LG Display: `docs/stage4-editorial-yield.md:43` — zero new articles for ~7 of 8.5 soak days despite continued successful polling — explicitly *not* penalized as a defect ("naturally low-volume corporate newsroom") but flagged as insufficient fresh evidence for promotion.

### 7. Config drift
- Direct, concrete drift instance found by diff: `config/config.example.yaml` documents `show_experimental_sources: false` with an 8-line explanatory comment (lines 4-11), but `config/config.local.yaml` (the actual local config in use) **omits this key entirely** — the example/documented config and the local/actual config have diverged (verified via direct file diff during this survey).
- No incident narrative attached to this drift (not flagged in any doc as a known issue) — it is evidence of the *pattern*, not a reported incident.

### 8. Schema/deploy readiness
- `src/korean_tech_wire/storage/database.py:17` etc. — explicit `CREATE TABLE schema_migrations` referenced in `docs/architecture.md:9-11` ("SQLite migrations are explicit in `storage/database.py`... `fetch_attempts` is intentionally deferred until per-request observability is introduced").
- Deploy-time schema check is explicit and manual, run as a checklist step, not automated as a pre-traffic gate: `docs/hetzner-migration.md:60-72` — after installing the transferred DB backup, the checklist runs `pytest`, `health`, `state checkpoint`, `source list`, one `soak --if-due` cycle, then `sqlite3 ... 'PRAGMA integrity_check;'`, with the explicit instruction: "The final command above must return `ok`, and `health` must show historical runs. If it does not, stop: a newly-created empty database is not a migration success." This is a manual, sequential, human-run checklist rather than an automated gate that blocks traffic switch on failure.
- `docs/hetzner-migration.md:89` — post-cutover validation: "New records must be genuinely new; a bulk of known articles becoming new is a migration red flag requiring an immediate stop and database/configuration investigation" — an explicit signature for detecting a stale/mismatched schema or DB-identity problem after a deploy.

### 9. Stale automation
- `docs/hetzner-migration.md:76-85` ("Single scheduler ownership") — explicit incident-avoidance step: "The current ChatGPT heartbeat is local-host-only and must be paused before the Linux timer is enabled... There must be one executor." This directly documents the risk category (an old scheduler left running alongside a new one) as a *procedure to avoid*, not as an incident that already happened — no evidence found that the old heartbeat was ever left running unnoticed.
- No "forgotten automation" incident narrative found (contrast with chinese-tech-wire, which also only has a similar prevention-not-incident pattern).

### 10. Retry/restart authority
- Fully automatic, precisely specified backoff policy — no ad hoc manual retry pathway found: `src/korean_tech_wire/scheduling.py:11-17,29-34` — first 2 consecutive failures retry at normal cadence (2h); from the 3rd failure the interval doubles per failure, capped at 12x (24h ceiling). Table reproduced in `docs/stage4.1-reliability-repair.md:24-30`.
- `src/korean_tech_wire/locking.py:11-44` (`RunLock`) — cross-platform advisory file lock (`msvcrt.locking` on Windows, `fcntl.flock` on POSIX) preventing overlapping `run`/`soak`/backup processes; referenced in `docs/hetzner-migration.md:85` ("`RunLock` prevents overlapping `run`, `soak`, and SQLite-backup processes on both Linux and Windows").
- No incident of double-execution/duplicate side effects was found (the lock appears to have prevented this from ever manifesting, unlike chinese-tech-wire where the equivalent protection had to be retrofitted at the deploy-wrapper level rather than in-process).

### 11. Health vs scheduler state
- `src/korean_tech_wire/dashboard.py:105-152` (`health_state`) — a five-state derived classification (`HEALTHY`, `STALE`, `BLOCKED`, `FAILED`, `UNKNOWN`) computed from success/failure recency and failure-note text-matching (`_BLOCKED_TOKENS = ("403", "forbidden", "blocked", "cloudflare", "rate limit")`, line 112), explicitly justified against exactly this topic: comment at lines 105-110 — "Fleet Law 3 (health honesty): HTTP success without useful output is not healthy after policy cycles, and a badge must not stay HEALTHY forever off an ancient success... `STALE_AFTER` ... deliberately exceeds the backoff ceiling (24h) so a HOST-BLOCKED lane in deep backoff shows as BLOCKED, not as a flapping failure." (`STALE_AFTER = timedelta(hours=48)`, line 111).
- This is a direct example of "scheduler enabled" (source `enabled: true` in `config/sources.yaml`) being explicitly decoupled from "actually healthy" (the derived `health_state`), with a named cross-repo governance citation ("Fleet Law 3") — indicating this concept is codified fleet-wide, not local invention (see Lineage section below).

### 12/13/14. Remote host truth, live-execution-state, partial deploys
- `docs/hetzner-migration.md:5-14` — an explicit runtime-state classification table (MUST MIGRATE / SAFE TO RECREATE / MUST NOT MIGRATE) distinguishing what's authoritative on the remote host vs. locally regenerable vs. secret-only.
- Live/current-execution-state concept distinct from the schedule definition: dashboard's "running" flag (`src/korean_tech_wire/dashboard.py:39` — "One manual local run at a time"), separate from the systemd timer's own definition — but no OS-level "is this actually running right now on Hetzner" query analogous to chinese-tech-wire's `scheduler_status.py`; korean-tech-wire relies entirely on DB-recorded state.
- Partial-deploy incident-adjacent language: `docs/hetzner-migration.md:87-89` ("First due Linux cycle") — "When the persisted cadence is actually due, run nothing manually first. Let the timer execute one all-source `soak --if-due` cycle, then inspect `health`, SQLite integrity, per-source counts, and duplicate canonical identities" — a deliberate first-live-cycle observation window designed to catch a partial/incomplete migration before trusting the new host. No actual partial-deploy incident found recorded as having occurred.

### 15. Safe manual intervention during soak
- `docs/runbook.md:26` — "`soak` is a portable foreground runner, not a scheduler... stopping it cleanly leaves completed runs in SQLite, and rerunning it safely resumes the evidence history." This directly asserts manual start/stop safety.
- Because due-ness/soak evidence is derived purely from persisted `source_run_health` rows (topic 1/3), a manual `korean-tech-wire run --source X` outside of soak *does* get logged into the same history a due-check would read — meaning a manual intervention **can** affect the natural-cadence-derived "consecutive successes" evidence used for promotion decisions (topic 2's conflation risk applies directly here too: a manual run could reset `consecutive_failures` to 0 just as effectively as a scheduled one, per `scheduling.py`'s "a successful run resets `consecutive_failures` to 0 immediately" language at `docs/stage4.1-reliability-repair.md:32`). No code-level distinction prevents a manual run from being counted as a "clean natural cycle" in promotion evidence — this is the same schema gap noted in topic 2.
- Dashboard explicitly disables ad hoc manual mutation in the Phase 0 UI: `src/korean_tech_wire/dashboard.py:239` — "Manual collection is disabled in the Phase 0 dashboard. Use the approved CLI workflow" — a deliberate guardrail against uncontrolled manual intervention through the web surface specifically (CLI still permits it).

---

## Incident summary (dated, with recurrence assessment)

| Date | Repo | What broke | Root cause | Fix | Could recur elsewhere in fleet? |
|---|---|---|---|---|---|
| ~2026-08-10 through 2026-08-18 (diagnosed/fixed 2026-08-19) | korean-tech-wire | 30-min systemd timer ran full 5-source cycles instead of the documented 2h cadence, ~4x intended request rate for over a week | `run_soak`'s `if_due` treated the whole fleet as one AND-gated due/not-due unit; one permanently-failing source (SK hynix) made the gate permanently "due" (`docs/stage4.1-reliability-repair.md:5-17`) | Per-source due evaluation from persisted `source_run_health`, plus failure backoff (`src/korean_tech_wire/scheduling.py`, `docs/stage4.1-reliability-repair.md:11-38`) | **Yes** — this is a generic "whole-collection AND-gate over per-item state" bug shape; any Clank using a single shared due/health gate across multiple independent sources is susceptible to the same failure mode. Directly relevant to topics 1, 2, 10, 11, 13. |
| Since 2026-08-10T09:16 UTC, diagnosed 2026-08-19, unresolved as of latest doc | korean-tech-wire | SK hynix Korea (sole original PRODUCTION source) collected zero new articles for the entire ~8.5-day soak | AWS ALB-level IP/ASN block against the Hetzner egress IP, reproducible on every endpoint including `robots.txt` (`docs/stage4.1-reliability-repair.md:40-63`) — not a code defect, not caused by the concurrent due-gating bug (block predates the amplification) | Not recovered; source stays `PRODUCTION` but automatically backs off to a 24h retry ceiling instead of hammering; surfaced via `korean-tech-wire health`'s `schedule=` output (`docs/stage4.1-reliability-repair.md:61-69`) | **Yes, in kind** — any collector hosted from a shared datacenter egress IP is exposed to the same class of infrastructure-level block; the fleet's mitigating pattern (backoff-as-suspension, `dashboard.py`'s `BLOCKED` state) is directly reusable. |
| 2026-08-09 19:47 UTC – 2026-08-10 06:00 UTC (observed/verified 2026-08-10) | chinese-tech-wire | (Verification exercise, not a failure) 13 genuine cron-triggered cycles confirmed to match real elapsed time and the configured `5 * * * *` schedule, all SUCCESS | N/A — this closes out a previously-open scheduler-verification gap (`ai/handoff/KNOWN_ISSUES.md:33-36`) | N/A (verification, not repair) | Relevant as a *pattern*: the team explicitly treats "scheduler configured" and "scheduler verified over real elapsed time" as two separate facts requiring separate proof — same posture also shows up in korean-tech-wire's Hetzner migration checklist. |
| Undated (documented as pre-existing, "confirmed via direct probe") | chinese-tech-wire | hkepc (HTTP 402), xfastest (HTTP 403/connection reset), PTT (HTTP 500 "Server Too Busy" across board index, hotboards, and 10/10 sampled article URLs) — all non-functional | Anti-bot/access blocks and, for PTT, apparent gateway overload — verified as source-side, not CTW-side (`pipeline/source_health.py:36-54`) | Sources marked `BLOCKED`/`DISABLED` in `KNOWN_STATUS`; historical data preserved, not deleted | **Yes, in kind** — same starvation-detection shape (found==0 vs new==0 distinction) as korean-tech-wire's SK hynix case; both fleets independently arrived at the same found-vs-new zero-streak distinction. |

---

## Lineage evidence

- **No explicit in-repo textual citation** of chinese-tech-wire from korean-tech-wire or vice versa was found (searched both repos' docs, source, and YAML comments for cross-repo names). chinese-tech-wire *does* explicitly cite other fleet siblings by name — "Free Game Tracker," "OEM Radar," "Semiconductor Intelligence"/"SemInt" — for patterns it reused or diverged from (`ai/handoff/DECISIONS.md:9-10,44,55`, `ai/handoff/KNOWN_ISSUES.md:5,38,44`, `ai/handoff/ROLLBACK.md:37`, `ai/handoff/STAGING_RELEASE_RUNBOOK.md:31,92`, `docs/EXPLAINABILITY_CONTRACT.md:3`). korean-tech-wire's docs never cite chinese-tech-wire or any other named sibling repo by name anywhere found.
- **Shared governance layer confirmed**: both repos' `.github/workflows/fleet-laws.yml` pull a shared `clank-architecture` conformance suite (`chinese-tech-wire/.github/workflows/fleet-laws.yml:14-19`, `korean-tech-wire/.github/workflows/fleet-laws.yml:14-19`, identical structure, checking out `anil-ganti-nbc/clank-architecture` and running its `conformance` pytest suite). korean-tech-wire's `dashboard.py:105` explicitly names "Fleet Law 3 (health honesty)" as the reason for its `STALE_AFTER`/`health_state` design — meaning at least one Operations-relevant rule (health-vs-scheduler honesty) is externally codified in `clank-architecture`, outside these two repos. **This external repo was not surveyed** (out of scope for this survey pair) but is clearly a primary source for any future Operations-domain standard, since it appears to already assert something like a "health honesty" law.
- **Convergent-not-copied pattern**: both repos independently arrived at nearly identical *concepts* — a found-vs-new zero-streak distinction for starvation detection (korean `docs/architecture.md:44`/`docs/promotion-policy.md:18` vs. chinese `pipeline/source_health.py:145-166`), a scheduler-state-vs-health-state split (korean `dashboard.py:115-152` vs. chinese `pipeline/operations.py:210-259`), and a "known documented block" vs. "live failure" distinction (korean `dashboard.py:112,121-123` `_BLOCKED_TOKENS`/`BLOCKED` vs. chinese `pipeline/source_health.py:36-54` `KNOWN_STATUS`) — but the **implementations are structurally different** (korean-tech-wire: pure functions, explicit injectable clock, dataclasses, SQLite raw SQL; chinese-tech-wire: SQLAlchemy ORM/sessions, dict-based classification, no injectable clock found). This reads as convergent design under the same Fleet Laws constitution rather than literal code-copying.
- korean-tech-wire's per-source `EXPERIMENTAL`/`PRODUCTION` lifecycle with an explicit promotion policy document (`docs/promotion-policy.md`) has **no equivalent** in chinese-tech-wire (which uses a whole-app `release_channel` instead) — this is a structural divergence between the two repos, not an inheritance.

---

## Survey 3 of 6: feature-phone-clank + smartphone-clank

# Pass 0A Evidence Inventory — Operations Domain (Standards Clank)

Read-only survey of `feature-phone-clank` and `smartphone-clank`. No files modified. This is evidence only — no standards proposed.

---

## Repo: smartphone-clank

### 1. Scheduler truth vs actual execution

Direct, dated incident. `docs/SCHEDULER_MIGRATION.md:9-12`: "Production evidence from the resident scheduler showed **165 lost due executions** by 2026-08-14 19:59 UTC, with lateness up to 95.480 seconds. The single worker avoided database races, but APScheduler discarded other due jobs when Samsung occupied that worker beyond the default grace window." Root cause: single-worker `BlockingScheduler` + misfire grace window silently dropping due jobs when one source's run overran (`docs/SCHEDULER_MIGRATION.md:24-36`). Fix: migrated from one resident APScheduler process to one systemd timer + one-shot service per source (`docs/SCHEDULER_MIGRATION.md:16-22`). `docs/infra/HETZNER_SOAK_COMMISSIONING.md:6-8`: confirms the historical scale — "226 APScheduler misfires; latest at 07:46:51Z" before the resident scheduler was retired 2026-08-16T10:19:33Z.

`runtime/run_once.py` (tested in `tests/test_run_once_due_check.py:31-70`) implements a separate `is_due()` truth check derived from `collector_run_metrics` timestamps rather than trusting scheduler state — this is the direct fix for "scheduled ≠ ran": due-ness is now computed from actual last-successful-run evidence in the DB, per-collector, not from an in-memory scheduler.

### 2. Natural-cycle vs manual/deploy-cycle accounting

Explicitly modeled as a `run_reason` field. `tests/test_run_once_due_check.py:113-130` (`test_target_builder_keeps_scheduled_default_and_allows_manual_reason`): default is `"production_scheduled"`; a manual invocation can pass `run_reason="field_test_manual"`, and both are asserted distinct. `docs/infra/HETZNER_SOAK_COMMISSIONING.md:26-30`: "Natural timer firings have already been observed... No manual collector run was used as soak evidence." and later: "substantive Google and multi-source collection evidence remains pending and must **not** be inferred from these initial skips." This shows the team actively guarding against conflating manual/validation runs with natural cadence evidence for soak purposes.

Conflation risk flagged explicitly: `docs/infra/HETZNER_SOAK_COMMISSIONING.md:310-315` ("Each production source was polled 3 times within ~15 minutes (validation cycle, cutover startup, restart-cycle test)... Noted for future migrations: prefer reusing one validation cycle as both the pre-cutover proof and the soak-start cycle").

### 3. Soak clocks and reset semantics

Explicit, named rule. `docs/SCHEDULER_MIGRATION.md:95-99` ("## Soak rule"): "Installing this runtime starts a new soak clock. Historical database and run evidence remains intact but cannot be counted as unattended evidence for the new scheduler architecture." `docs/infra/HETZNER_SOAK_COMMISSIONING.md:276-286`: soak start timestamp is anchored to the *scheduler's* first "runtime entering scheduler loop" log line, explicitly overriding an earlier, different soak-start timestamp recorded elsewhere ("This supersedes the earlier '2026-08-11 Windows 8-OEM freeze' timestamp recorded in HANDOFF.md §12e... per the migration mission's own explicit instruction to **reset the mental soak clock**").

Longest-documented soak-clock discipline: `docs/infra/SAMSUNG_US_OWNERS_PRODUCT_CANARY_REPORT.md:1-24` — Rule-7 lifecycle table shows a soak that ran from 2026-08-26 baseline through 2026-08-30 (32 clean repeat cycles, "~8x longer than any Wave-1/2 qualification") before promotion, and explicitly separates promotion of *execution stage* (SOAK→CANARY) from promotion of *notification authority* (never touched in this transition — see topic 5).

No evidence found of a manual/deploy run *accidentally* resetting or falsely advancing a soak clock (the team appears aware of the risk and manually manages it), but also no automated protection mechanism was found that would prevent a future accidental reset — the discipline is currently narrative/operator-applied, not code-enforced.

### 4. Experimental/production/mothballed/blocked lifecycle states

Two independently documented state machines, explicitly flagged as easy to conflate — `HANDOFF.md:228-243` ("## 6. Collector eligibility / source validation states... Two independent concepts, easy to conflate"):
- **Source validation state** (recon-time): `LIVE_VALIDATED` / `LIVE_PARTIAL` / `PROMISING` / `UNSTABLE` / `BLOCKED` / `UNSUPPORTED` / `REJECTED` (`docs/wave1/SOURCE_MATRIX.md`).
- **Adapter validation state**: `EXPERIMENTAL` / `LIVE_PARTIAL` / `LIVE_VALIDATED` / `BLOCKED` / `UNSUPPORTED` (`collectors/wave1/adapter.py`).

Full lifecycle stage list (`docs/ENGINEERING_PRINCIPLES.md:40-41`): `RESEARCH_ONLY`, `FIXTURE_ONLY`, `LIVE_PARTIAL`, `LIVE_VALIDATED`, `STAGING`, `PRODUCTION`, `BLOCKED`, (line 75-76) plus the promotion path RESEARCH → LIVE VALIDATION → STAGING → BASELINE → REPEATABILITY → CANARY → PRODUCTION, with "No shortcuts."

Separate maturity axis for notification authority (`alerts/source_maturity.py:1-19,23-24`): `MATURITY_PRODUCTION` / `MATURITY_SOAK`, fail-closed — "a source id that is not explicitly listed here is treated as soak" (line 47-50). A third `maturity="canary"` value exists at the collector-registration layer (`tests/test_samsung_owners_soak.py:230-234`).

No explicit "permanently disabled" vs "temporarily blocked" distinction was found as a formal state — `BLOCKED` appears to be used for both; `alerts/source_maturity.py:26-30` notes that a legacy collector disabled by config "is intentionally absent: if one is ever re-enabled it re-enters soak by default" — i.e., disabling does not preserve prior maturity, it resets to the most conservative state.

### 5. Promotion readiness

Governed by "Fleet Law 8" (`alerts/source_maturity.py:11-13`): "Promotion to `production` requires an explicit, reviewed edit to this module (Fleet Law 8: promotion gates) — never a config-only flip." Assessment is manual/operator-reviewed, not automatic — confirmed repeatedly: `docs/SOURCE_INVENTORY.md`/canary reports (e.g. `docs/wave2/MOTOROLA_CANARY_REPORT.md`, `docs/wave1/ONEPLUS_CANARY_REPORT.md`) each require: clean live baseline, hostile SQL audit, 3+ stable repeat cycles, zero pollution, zero collisions before a "PROMOTED" verdict is written.

**Incident of premature/accidental promotion** — the baseline-completion tracker marking itself complete despite silently dropped data: `docs/wave2/MOTOROLA_CANARY_REPORT.md:17-31` (dated 2026-08-10 17:30 IST). Root cause: two independent, uncross-checked gates (`WAVE1_PRODUCTION_SCOPE` vs `config.yaml::manufacturers` allowlist) had to both say "yes"; only one was updated. The baseline-completion gate evaluated *before* the manufacturer filter, so it "still marked `motorola_regional_sitemap`'s baseline as complete" even though `process_discoveries()` silently `continue`d past all 18 real candidates. "Left uncorrected, the next scheduled run would have treated the same 18 devices as 'genuinely new since baseline' and fired 18 real newsroom alerts for devices Clank had never actually recorded." Fixed same-day; permanent regression fix in `HANDOFF.md:645-688` (§12c): fail-closed startup validation (`assert_production_scope_or_refuse()`), no-silent-drop logging, and "**Baseline completion now requires proof of persistence**" — refuses to mark baseline complete if `valid &gt; 0` but `new+updated+resighted == 0`. Regression tests: `tests/wave1/test_no_silent_drop.py`.

### 6. Source starvation / observation collapse

`HANDOFF.md:369-371`: "`database/models_v03.py::SourceHealth` exists in the schema but **nothing writes to it yet** — neither Samsung nor Wave 1. Flagged as a genuine gap." This is a direct gap in starvation detection at the schema level — a table built for exactly this purpose is dead.

Mitigation that does exist: `observability/metrics.py::MetricsRecorder` "already implements health scoring, staleness detection, and a `zero_discovery_with_healthy_fetch` regression check" (`HANDOFF.md:364-368`). Also `docs/infra/HETZNER_SOAK_COMMISSIONING.md:304-309`: Google's collector genuinely returned 0 candidates for two consecutive cutover cycles due to a `consent.google.com` redirect wall; it was caught immediately by "the collector's own `zero_candidates_despite_healthy_fetch` metric, exactly as designed" and flagged for soak-window watching — this is starvation-detection working as intended, not an incident of it failing.

Counter-example of deliberately-verified non-starvation: `docs/infra/SAMSUNG_US_OWNERS_PRODUCT_CANARY_REPORT.md:46-69` (§2, "Zero-new is health, not starvation") — the team explicitly checked 32 consecutive zero-new-device cycles were not a silently-stale-cache failure mode by verifying live HTTP redirect chains and per-cycle content-hash variance.

The V038 daily-report contamination investigation also documents the inverse failure — a collector producing zero/junk output still scored `health: 100` because health scoring "Does not check... whether candidates are real model IDs."

### 7. Config drift

Central, root-cause-confirmed incident. `docs/V038_PRODUCTION_REPORT_INVESTIGATION.md:1-51`: repository-committed `config/config.yaml` shipped with non-Samsung collectors `enabled: true`, while "the operator was instructed to set non-Samsung flags to `false` **locally**. The **repository** config was never permanently flipped. Extracting v0.3.7 over the project would restore `enabled: true`." This is a textbook local-vs-repo-vs-deployed config drift finding, dated 2026-08-06, root-caused in code (`config/config.yaml` vs local edits) at lines 33-51 and 264-279 ("Root causes ranked" / "Minimal repairs").

Second, independent config-drift incident is the Motorola allowlist gap already described (topic 5) — two config authorities drifting relative to each other within the same file tree.

`docs/infra/PRODUCTION_SCOPE_AUDIT.md` (referenced `HANDOFF.md:645-654`) traces every mechanism that can include/exclude an OEM from production and finds two independent, uncross-checked allowlists — the permanent fix (`PRODUCTION_OEM_SCOPE` vs `config.yaml::manufacturers`) is explicitly a config-drift-prevention fix.

### 8. Schema/deploy readiness

Strong, code-enforced pattern: `HANDOFF.md:59-83` (§0) — "the live daemon, `main.py run`/`init` (production), and the cloud one-shot runner all refuse to start rather than silently call `create_all()` if schema is behind" via `database/schema_guard.py::ensure_tables_present_or_refuse()`. `HANDOFF.md:411-423` (§10a): "Alembic is now the sole schema-mutation authority for production runtime... all three refuse to start rather than mutate schema if the database is behind head." Regression tests: `tests/wave1/test_schema_authority.py` (5+ tests).

Incident of schema check gap (pre-fix): `HANDOFF.md:427-436` — a `wave1_baseline_state` table repeatedly appeared **in production** with zero rows, traced to `main.py db upgrade`'s implementation being literally `Base.metadata.create_all()` — "a real, documented command, not a phantom process." A shared, unbranched working tree meant a stray model import could silently add schema to production. Confirmed reproducing at least twice in one session (`HANDOFF.md:438-463`); fix and residual risk both documented — "This may well recur again... since the underlying scheduled process keeps running and this repo is a live, shared working tree."

Deploy-vs-schema ordering during Hetzner cutover was explicitly checked, not assumed: `docs/infra/HETZNER_SOAK_COMMISSIONING.md:124-142` — schema revision verified identical (`0007_wave1_baseline_state` == head) on both source and destination before traffic switched.

### 9. Stale automation

Direct incident: `docs/infra/PROD_DEV_SPLIT.md:10-29` — a stale PID file (`runtime.pid`, PID 11756 from 2026-08-02, no longer alive) meant `SmartphoneIntelClank-HealthCheck` (a Task Scheduler job running every 15 minutes) could spawn a **duplicate daemon** without stopping an old one whose real PID wasn't the one on record: "two separate daemon process groups were found running concurrently against the same production DB (started 02:15:04 and 14:45:04 today)." Root cause explicitly documented as "a real, pre-existing bug, independent of Wave 1." `HANDOFF.md:49-54` restates the same root cause: `start-runtime.ps1`/`start-dashboard.ps1` started processes synchronously with no PID recording, so health-check "could never detect a running instance and would start a duplicate every ~15 minutes — this is the confirmed origin of two orphaned daemon processes found and stopped during this phase."

Stale artifact left running post-migration: `docs/infra/HETZNER_SOAK_COMMISSIONING.md:54-63,300-303` — a pre-existing Docker-based staging deployment (`/home/deploy/staging/smartphone-clank`, built from an old `.deployed-id`) was running hourly via a `deploy` crontab entry, discovered mid-migration, cron entry commented out but the tree/volume left in place — flagged explicitly as "dead weight an operator may want to clean up."

Zero-row table audit (`HANDOFF.md:690-706`) found 2 fully DEAD tables and 2 tables with `DUPLICATE_SEMANTICS_RISK` including `scheduler_jobs` vs APScheduler's in-memory state — evidence of stale schema/automation surface accumulating without cleanup, "Nothing removed this phase — classification only."

### 10. Retry/restart authority

`docs/SCHEDULER_MIGRATION.md:68` (Responsibility mapping table): "retry behavior | unchanged: next configured interval, no new immediate retry." Confirmed at code level: `tests/test_run_once_due_check.py:73-88` (`test_failed_run_still_counts_for_due_check_no_special_retry`) — "A failed attempt still records a CollectorRunRecord (status=failed); run_once.py does not implement its own retry -- the collector simply remains subject to the same interval as a successful run."

Double-execution incident directly tied to retry/idempotency: `HANDOFF.md:317-339` (§9) — a real SQLite `database is locked` bug was exposed when `WebhookDelivery` writes were made unconditional: a second DB connection opened mid-transaction inside `pipeline.process_discoveries()` collided with the caller's open transaction. Fixed by threading the caller's session through instead of opening a second connection. Idempotency-under-retry is explicitly regression-tested: `HANDOFF.md:317-321` and `tests/wave1/test_alert_semantics.py::test_reprocessing_a_delivered_event_does_not_duplicate_the_alert` — "a retried/restarted run that reprocesses an already-delivered discovery finds the device already exists and never re-attempts the alert."

Restart authority for the daemon itself: `deploy/systemd/` — `Restart=on-failure`, `RestartSec=30` (`docs/infra/HETZNER_SOAK_COMMISSIONING.md:82`), i.e., systemd is the sole automatic-restart authority in the current (post-migration) architecture; manual restart is operator-only via `systemctl restart`.

### 11. Health vs scheduler state

Directly documented gap: `docs/V038_PRODUCTION_REPORT_INVESTIGATION.md:211-227` (§9) — "`health_score()` Starts at 100... Does not check: whether collector is enabled in production config, validation status..., whether candidates are real model IDs... A single `status=success` run with 0 or garbage candidates → health 100." This is the exact "scheduler/config says enabled" ≠ "actually healthy" failure mode, root-caused and dated 2026-08-06.

`FEATURE_PHONE_CLANK_DEFINITION_OF_DONE.md:52-57` in the sibling repo draws the same distinction deliberately as a design choice (see feature-phone-clank section below) — worth cross-referencing as convergent thinking.

### 12. Remote host/deployment truth

Extensively documented via the Hetzner migration report. `docs/infra/HETZNER_SOAK_COMMISSIONING.md:84-115`: deployed SHA verified via `git rev-parse HEAD` read from the running service's own `WorkingDirectory`, not trusted from a tag/branch name — explicit design principle stated in `docs/SCHEDULER_MIGRATION.md:87-93` ("## Provenance"): "Deployment must still compare GitHub's accepted merge SHA, the checkout SHA, and the logged runtime SHA rather than trusting a tag or directory name."

Two real "invisible until deployed" bugs found only by doing a clean remote checkout, i.e. repo-claims vs actual-runnable-on-host drift: `docs/infra/HETZNER_SOAK_COMMISSIONING.md:89-106` — missing `alembic` in `requirements.txt` (Windows had it installed out-of-band) and an unanchored `.gitignore` rule silently excluding tracked reference YAML — both invisible on the dev machine, both broke a fresh Linux checkout.

Shared-host risk flagged directly: `docs/infra/HETZNER_SOAK_COMMISSIONING.md:44-52` — the Hetzner box is described as "a shared multi-project fleet host" running 8 other Clanks/projects each isolated by system user or the shared `deploy` user; reboot was explicitly judged unsafe and *not proven* (`docs/infra/HETZNER_SOAK_COMMISSIONING.md:221-238,295-297`): "Reboot-specifically-triggered persistence remains formally unproven — flagged as a residual risk."

### 13. "Scheduled" vs "actually running" (live execution state)

`runtime/run_once.py::is_due()` (tested `tests/test_run_once_due_check.py`) is exactly this: a live, DB-derived due/not-due decision computed at invocation time, independent of any persistent scheduler-side "enabled" flag. `docs/SCHEDULER_MIGRATION.md:19-22`: "The process first obtains a non-blocking same-source lock, then waits on a blocking shared execution lock" — i.e. current execution state is tracked via OS-level locks, separate from the timer definition that triggered the process.

### 14. Partial deploys / stale code

`docs/infra/HETZNER_SOAK_COMMISSIONING.md:89-115` documents the "fix and redeploy" pattern used when a partial/broken checkout was found (both fixes were required to be committed to GitHub *first*, then redeployed — "per the mission's explicit rule against uncommitted Hetzner-only patches"). No incident found of a deploy that *itself* partially completed (e.g., half the services updated); the closest analog is the stale Docker staging artifact left running alongside the new systemd-based production deployment (topic 9, `docs/infra/HETZNER_SOAK_COMMISSIONING.md:54-63`) — old and new infrastructure coexisting post-migration, though isolated by design (separate volume/DB) rather than accidentally so.

### 15. Safe manual intervention during soak

Directly and repeatedly addressed as policy: `docs/infra/HETZNER_SOAK_COMMISSIONING.md:288-291` — during the declared 7-day soak window: "no new OEMs, no Xiaomi work, no schema cleanup, no zero-row table deletion, no architectural refactor, no alert-policy experimentation. Only correctness/reliability fixes justified by observed soak failures." `HANDOFF.md:845-847`: "No new OEMs during the soak unless a production incident forces architectural work. The point is to observe the system, not continuously modify it."

Manual intervention that *is* explicitly declared safe and non-corrupting: restart-cycle testing during soak (`docs/infra/HETZNER_SOAK_COMMISSIONING.md:230-236`) — a live `systemctl restart` was exercised specifically to test resilience, with explicit before/after invariant checks (device counts, DB integrity, single-process confirmation) proving the soak's data wasn't corrupted by the manual restart. Also `docs/infra/SAMSUNG_US_OWNERS_PRODUCT_CANARY_REPORT.md:26-30`: one deliberate "pre-soak controlled validation run" is explicitly excluded from the natural-cycle soak count ("plus 1 pre-soak controlled validation run... deployment_pass2_controlled_validation") — the mechanism for keeping a manual/controlled run from corrupting soak evidence is to *tag it with a distinguishable run type/label and exclude it from the natural-cycle tally*, not to disallow manual runs outright.

---

## Repo: feature-phone-clank

### 1. Scheduler truth vs actual execution

`docs/FEATURE_PHONE_SCOPE_EXPANSION.md:430-442` (§5d, "HMD Hetzner operational note"): "the last observed scheduled HMD runs on Hetzner (2026-08-18 01:15 and 07:15 UTC) failed with `ReadTimeout` against `www.hmd.com`; the catastrophic-zero guard correctly held the prior 44 products rather than corrupting state. Whether that timeout is still ongoing... was not re-verified... **Flagged again: a separate follow-up session should check current HMD run status on Hetzner.**" This is a directly documented gap between "scheduled to run" and confirmed successful execution, left open across at least two work sessions.

`FEATURE_PHONE_CLANK_DEFINITION_OF_DONE.md:139-142`: "Natural cron runs continued healthy through this phase's audit (last observed 2026-08-17 01:15 UTC, 44 products...)" — the team treats "last observed" timestamp evidence, not the cron definition itself, as the truth signal.

### 2. Natural-cycle vs manual/deploy-cycle accounting

`docs/FEATURE_PHONE_SCOPE_EXPANSION.md:812-817` (§18): "Monitoring during the soak: `feature-phone-clank status`... Controlled validation (before enabling cron): one manual run each via `scripts/deploy_run_experimental.sh`" — manual pre-cron validation runs are explicitly separated from the cron-driven soak evidence that follows. `docs/FEATURE_PHONE_SCOPE_EXPANSION.md:762-764`: "Neither itel nor Lava is production-promoted" — kept distinct from experimental-soak evidence regardless of run count.

### 3. Soak clocks and reset semantics

`docs/FEATURE_PHONE_SCOPE_EXPANSION.md:765-830` (§18) documents a full experimental soak deployment with an explicit start (2026-08-18), a defined window ("3-5 day unattended soak"), review criteria, and rollback plan (crontab removal). No evidence of a formal "soak clock reset" mechanism comparable to smartphone-clank's — the concept of resetting a soak clock on redeploy is not present in feature-phone-clank's docs; the team instead runs experimental soaks in a fully separate deployment (separate checkout, image, volume, DB, lock, crontab) from production, so a redeploy of the experimental branch has no soak-clock semantics to reset. Nothing found addressing what happens to a soak's evidence-count if the *production* HMD deployment is redeployed mid-soak.

### 4. Experimental/production/mothballed/blocked lifecycle states

`FEATURE_PHONE_CLANK_DEFINITION_OF_DONE.md:1-9`: V1 scope is explicitly HMD/Nokia only; "Any other manufacturer requires an explicit later scope decision and starts experimental." `src/feature_phone_clank/core/scope.py:20-34`: single-file allowlist model — `ScopeConfig.production_collectors: list[str]`; `is_production()` is a simple membership check. A collector absent from `config/scope.yaml` "can still be run (e.g. `--experimental`) but only against an in-memory/throwaway store, never the real one" (`scope.py:8-9`).

`docs/FEATURE_PHONE_SCOPE_EXPANSION.md:121,146,209,227`: per-source explicit status lines — "Status: experimental, not production-promoted" / "Production promoted: NO" — for itel and Lava. `runtime_bridge.py:30-34,90`: `_release_channel()` defaults to `"experimental"`, with the comment: "Never hard-code 'production': FEATURE-01 has zero validated collectors as of Stage 1 and has not earned any release-channel promotion yet."

No distinct "permanently disabled/mothballed" vs "temporarily blocked" state found — same gap as smartphone-clank.

### 5. Promotion readiness

Same allowlist-gate mechanism as smartphone-clank but simpler (single YAML list vs two independently-gated allowlists) — explicitly built this way *because of* the smartphone-clank incident (see Lineage section below). `docs/FEATURE_PHONE_SCOPE_EXPANSION.md:582-594`: "so a future promotion can't accidentally leave stale" (production scope) — direct echo of the smartphone-clank Motorola incident's lesson. No incident of premature promotion found in feature-phone-clank — likely because no non-HMD source has yet been promoted (all remain experimental per DoD).

### 6. Source starvation / observation collapse

Explicitly modeled and tested: `FEATURE_PHONE_CLANK_DEFINITION_OF_DONE.md:43-45`: "A previously non-empty catalogue returning zero is `blocked_zero_result`, not a removal event." `tests/test_catastrophic_zero.py` (file present, not read in full but named exactly for this scenario) and referenced live in the HMD ReadTimeout note (topic 1 above): "the catastrophic-zero guard correctly held the prior 44 products rather than corrupting state." This is a well-built starvation *safeguard*, distinct from starvation *detection/alerting* — nothing found describing how an operator is actively notified that a source has gone quiet (only that state isn't corrupted when it does).

`FEATURE_PHONE_CLANK_DEFINITION_OF_DONE.md:20-23`: "Requires three healthy consecutive absences before removal. Failed and catastrophic-zero runs do not advance absence counters" — a specific, tested design against false-starvation-triggered removal.

### 7. Config drift

`docs/FEATURE_PHONE_SCOPE_EXPANSION.md:383-404` (§5b, "Experimental isolation proof"): explicit before/after SHA-256 verification that `config/scope.yaml` was byte-for-byte unchanged after experimental runs — "confirmed via `git diff` against `origin/main`, zero diff." `docs/FEATURE_PHONE_SCOPE_EXPANSION.md:801-806`: same check repeated for the Hetzner experimental soak deployment — production `config/scope.yaml` verified unchanged, production checkout's `.deployed-id` unchanged. This is proactive config-drift *prevention/verification* practice, not an incident report; no config-drift incident specific to feature-phone-clank was found (unlike smartphone-clank's V038).

### 8. Schema/deploy readiness

Not found as an explicit gate/incident in the files surveyed (no Alembic-equivalent schema-guard code was located in feature-phone-clank; `schema.sql` is referenced directly, `FEATURE_PHONE_CLANK_DEFINITION_OF_DONE.md:61-64`, as pre-existing and "audited first, found sufficient" for the notification-outbox feature, but no fail-closed schema-version check comparable to smartphone-clank's `schema_guard.py` was found). Report as: nothing found on this specific topic in feature-phone-clank.

### 9. Stale automation

`docs/FEATURE_PHONE_SCOPE_EXPANSION.md:785-790`: cron entries are deliberately placed under the operator's own personal crontab (`anilganti`) rather than the `deploy` user's, specifically to keep the experimental schedule "physically incapable" of colliding with production's. `docs/FEATURE_PHONE_SCOPE_EXPANSION.md:824-826`: rollback is "remove the two cron lines from `anilganti`'s crontab." No incident of a stale/forgotten cron job was found, but the design explicitly anticipates the risk class (isolating experimental crontabs from production's).

### 10. Retry/restart authority

Well-documented notification-layer retry model (distinct from collection retry): `FEATURE_PHONE_CLANK_DEFINITION_OF_DONE.md:79-86`: "**Retry safety**: a failed attempt increments `attempts`, records `last_error`, and stays `pending` until `MAX_ATTEMPTS=5`, only then does it become terminally `failed`. `deliver --requeue-failed` moves `failed` rows back to `pending` without resetting `attempts`/history." Deduplication via `INSERT OR IGNORE` on a UNIQUE `dedup_key` explicitly guards against double-execution: "a rerun, restart, or double-invocation cannot create a second row for the same event" (lines 83-86). Verified in the pre-merge review (`FEATURE_PHONE_CLANK_DEFINITION_OF_DONE.md:173-178`): "an already-`sent` row is structurally unreachable by either path — verified directly."

Single-instance run-lock with stale-lock reclaim is the collection-layer retry/restart authority: `src/feature_phone_clank/core/run_lock.py:86-135` — a lock older than the process's actual liveness (checked via `_pid_alive()`, OS-level PID probe, not just file age) is reclaimed automatically; a lock whose owning PID is confirmed alive raises `LockError` and refuses to start a concurrent run (lines 100-104). This code is explicitly a cross-repo port (see Lineage).

**Real duplicate-notification incident**: `FEATURE_PHONE_CLANK_DEFINITION_OF_DONE.md:150-159` — `IDENTITY_ANOMALY` compared each run's SKU against a field set once at creation and never updated, so "a product whose SKU changed once and then stayed at the new value kept comparing unequal on every later run, producing a second, spurious identity_anomaly event/notification for the *same* real change (verified: exactly 2 Discord messages for 1 real-world flip)." Fixed by gating event creation on `is_new_obs`. Regression test: `tests/test_pipeline.py::test_sku_mismatch_does_not_reraise_on_unchanged_rerun`.

### 11. Health vs scheduler state

Explicit, deliberate architectural separation, directly on-topic: `FEATURE_PHONE_CLANK_DEFINITION_OF_DONE.md:53-57`: "`feature-phone-clank report`'s `delivery_health` field is a distinct axis from `source_health`: a Discord outage reports `delivery_health: degraded`... never `source_health: failed` — `runtime_bridge.get_health` has no dependency on the `notifications` table at all, by construction." `runtime_bridge.py:151-153,159-164`: `get_health()` computed purely from local SQLite process/DB state ("does not run collectors, does not claim Fleet or ingestion health"), with a 3-way state derivation (`healthy`/`degraded`/`failed`) based on DB writability/existence — independent of whatever a scheduler (cron/Task Scheduler) reports about job enablement.

### 12. Remote host/deployment truth

`runtime_bridge.py:36-44`: source revision is "baked in at build time" via `GIT_REVISION` build arg → env var, "never read from a `.git` directory at runtime," with local/non-Docker runs explicitly reporting `"unknown"` rather than a fabricated value — a deliberate anti-drift design ("Pattern proven on OEM Radar / Chinese Tech Wire"). `docs/FEATURE_PHONE_SCOPE_EXPANSION.md:22-28`: production truth is queried live via the actual Hetzner Docker volume, not assumed from repo state — "Hetzner deployed revision: `c749df3`... Production DB (queried live via the Hetzner Docker volume): 44 products."

### 13. "Scheduled" vs "actually running" (live execution state)

`run_lock.py` (whole file) is exactly this mechanism — a live PID-liveness probe (`_pid_alive()`, lines 26-54) determines actual current-execution-state, entirely independent of and prerequisite-checked against any scheduler/cron definition.

### 14. Partial deploys / stale code

`docs/FEATURE_PHONE_SCOPE_EXPANSION.md:801-811`: two fully isolated deployments (production HMD checkout vs experimental itel/Lava checkout) intentionally coexist on the same Hetzner host at different pinned commits (`c749df3` vs `49eab25`) — by design, not accident, and repeatedly SHA-verified not to interfere. No incident of an *unintended* partial deploy was found in this repo.

### 15. Safe manual intervention during soak

`docs/FEATURE_PHONE_SCOPE_EXPANSION.md:793-800`: manual "controlled validation" runs are explicitly performed *before* enabling the soak cron, and their results (6/6, 11/11 accepted products) are compared against the local baseline rather than folded into the soak's own cycle count — same non-corrupting pattern as smartphone-clank's canary report. `native/windows/launcher.py:25-28`: the dashboard is "unconditionally read-only... POST always 403s" specifically so that opening the dashboard during any collection/soak window cannot mutate state — a code-level (not just policy) guarantee against accidental soak interference via the UI.

---

## Lineage evidence (cross-repo)

**Confirmed, explicit citation — the "73-device contamination" pattern**: `src/feature_phone_clank/core/scope.py:1-9` — the module docstring states directly: "Smartphone Clank learned the hard way that a collector which can run must not thereby be allowed to write to the production catalogue — a test run polluted it with **73 junk devices**. FEATURE-01 starts with the guardrail already in place: `config/scope.yaml` is the single, explicit allowlist of collectors approved to persist into the production database." This is feature-phone-clank's `scope.py` design *directly inherited as a pattern* (not code, but architecture) from smartphone-clank's incident.

Note on the "73" figure: smartphone-clank's own docs use "73" twice with two different meanings that should not be conflated:
1. `HANDOFF.md:881-892` (§14, "August 2026 contamination incident"): the V038 root cause — 73 garbage rows from mis-parsed marketing text (`docs/V038_PRODUCTION_REPORT_INVESTIGATION.md`), fixed via `production_scope()` gating + `tests/wave1/test_pollution_cannot_recur.py`.
2. `HANDOFF.md:786-789` (§12e): coincidentally, Oppo's *legitimate* promoted device count is also 73 ("73 devices in production, 0 pollution").

`scope.py`'s citation ("a test run polluted it with 73 junk devices") matches incident #1's shape (contamination, not legitimate growth) but describes it as caused by "a collector which can run... allowed to write," which more closely matches the V038 root cause (config-enabled collectors with no validation gate) than a single "test run." No smartphone-clank document was found describing the incident specifically as a "test run" causing exactly 73 junk devices — `docs/V038_PRODUCTION_REPORT_INVESTIGATION.md:150-169` estimates the illegitimate portion as "≈77 (order of magnitude)," not a confirmed exact 73. This is worth flagging as a minor inconsistency between the lineage citation's framing and the source repo's own investigation numbers — Pass 0B may want to reconcile which document is authoritative.

**Is the inherited fallout Operations-relevant, or purely data-ontology?** Based on `scope.py`'s own framing and the V038 investigation, the root failure was **not purely data-ontology** — it was a deploy/config-scheduling issue: `docs/V038_PRODUCTION_REPORT_INVESTIGATION.md:19-27,53-85` shows the trigger was `config/config.yaml` shipping with collectors `enabled: true` and no second validation gate, then *scheduled or manual* invocation (`python main.py run` / daemon / Task Scheduler — investigation lists all three as possible triggers, §3) executing them against production. So the inherited lesson feature-phone-clank encoded is explicitly an Operations-domain lesson (production-scope/promotion gating tied to what a scheduler or manual run is allowed to execute against), not solely an entity-resolution/data-ontology one — though the *symptom* (garbage devices/marketing text as model numbers) is data-ontology-shaped.

**Second confirmed lineage citation**: `src/feature_phone_clank/core/run_lock.py:1-7` — "Ported verbatim from OEM Radar's `core/run_lock.py`... 'reuse OEM Radar's established locking pattern rather than inventing a new one.' Only the docstring and log-channel name were adjusted; the algorithm is unchanged." This is convergence-by-explicit-reuse from a third Clank (OEM Radar), not smartphone-clank.

**Third confirmed lineage citation**: `src/feature_phone_clank/runtime_bridge.py:1-16,36-44` — "Deliberately mirrors OEM Radar's `runtime_bridge.py` field-for-field... Pattern proven on OEM Radar / Chinese Tech Wire." Independent evidence that health/identity/version contract design is a fleet-wide convention seeded by OEM Radar, not smartphone-clank.

**Fourth**: `src/feature_phone_clank/core/continuity.py:16-21` cites `clank-architecture` repo's ADR-0006 and `DATA_SURVIVABILITY.md`, plus `diagnostic-clank`'s `fleet.yaml`, as canon for its epoch/continuity event model — evidence of a shared cross-fleet architecture-documentation repo (`clank-architecture`) governing continuity semantics, separate from smartphone-clank.

No lineage evidence was found running in the other direction (smartphone-clank citing feature-phone-clank, or smartphone-clank citing OEM Radar/clank-architecture) in the files surveyed — smartphone-clank's docs read as self-contained/originating, consistent with it being the older/larger repo and the source of the cited incident.

---

## Survey 4 of 6: semiconductor-intelligence + clank-architecture

I now have comprehensive evidence across both repos. Compiling the final report.

# Pass 0A Evidence Inventory — Operations Domain

Read-only survey. No files modified. All citations are file:line as of repo state on disk 2026-08-31.

---

## Repo 1: `C:\Users\anil\Clanks\semiconductor-intelligence`

### Note on framing discrepancy
The task brief stated ADR-0002 carries "DO_NOT_STANDARDISE" as an adopted position. That literal string does not exist anywhere in `clank-architecture` (`grep -rn "DO_NOT_STANDARDISE"` returned nothing). What actually exists: **ADR-0002** (`adr/0002-motherclank-supervisory-architecture.md:3`) is titled "Motherclank — Supervisory Intelligence Architecture," status **PROPOSED — REVIEWED DRAFT**, not adopted/active. It does *not* argue against standardization — it's a staged-capability plan for a fleet-supervisor tool (M0–M5), with M5 (controlled actions: pause/run_now/deploy) explicitly gated as "NOT NOW" (`adr/0002:30`). This should be corrected in adjudication: no ADR in this repo currently blocks Operations-domain standardization by name. Only `FLEET_LAWS.md` is marked **ACTIVE** (`FLEET_LAWS.md:3`); every ADR 0001–0014 is PROPOSED/DRAFT except ADR-0005 (referenced as ratified integration gates, not read in full this pass).

### 1. Scheduler truth vs actual execution
Direct, load-bearing evidence. `semi_intel/operations/scheduler.py:345-349`:
```
# Scheduler liveness is not job success. Persist invocation first so a
# no-op, partial, or later failure cannot masquerade as a successful
# completed cycle.
settings.last_scheduler_invocation = now
self.session.commit()
```
`OperationalScheduler.status()` (`scheduler.py:191-207`) exposes `last_scheduler_invocation` and `last_successful_job_commit` as two distinct fields, never conflated. `deploy/crontab.example:3-6` states explicitly: "the scheduled path MUST go through the OperationalScheduler... so that scheduler invocation and successful work are recorded separately (Fleet Law 3)... Direct `pipeline run` invocations bypass scheduler evidence entirely." `PHASE0_CONTAINMENT.md:14-16`: "The success heartbeat advances only after at least one scheduled job commits with a successful or partial status; invocation alone does not create a false healthy signal." This SemInt pattern is cited verbatim in `clank-architecture/adr/0002-motherclank-supervisory-architecture.md:39` as "the reference semantic" for the whole fleet — strong lineage evidence.

### 2. Natural-cycle vs manual/deploy-cycle accounting
`semi_intel/domain/enums.py` (referenced, not fully read) defines `OperationalTriggerType` with values `SCHEDULER`, `MANUAL_CLI`, `RETRY` used throughout `scheduler.py` (e.g. `run_job(..., trigger=OperationalTriggerType.MANUAL_CLI)` default at `scheduler.py:225`, `trigger=OperationalTriggerType.SCHEDULER` at `scheduler.py:360,368`). Every `OperationalJobRun` row records which trigger caused it — this is a working natural-vs-manual accounting mechanism. `ai/handoff/STAGING_RELEASE_RUNBOOK.md:16`: "staging schedule: disabled by default; enabled only for a deliberate soak run, per the brief's 'a newly deployed candidate must not begin running merely because its container was created.'" This is a direct assertion that deploy events must not manufacture cycles.

### 3. Soak clocks and reset semantics
`ai/handoff/STAGING_RELEASE_RUNBOOK.md:29-32` (Step 5, "Soak"): "elapsed soak time from a previous build does **not** transfer to a materially different build. If this candidate changes collector logic, scoring, or anything beyond pure packaging, its soak clock restarts at zero regardless of how long the last build had been running." Step 7 (`STAGING_RELEASE_RUNBOOK.md:37-39`) requires logging "which candidate SHA is currently soaking, when it started, and what changed, so 'how long has this actually been soaking' is never a guess." No code implementation of this policy was found in this pass (it lives as documented operator discipline, not enforced in `scheduler.py`).

### 4. Lifecycle states (experimental/production/mothballed/blocked)
`config/oems/*.yaml` — per-source `support_status` field with observed values `LIVE_VALIDATED` (`config/oems/acemagic.yaml:1,10`) and `NEEDS_OWNER_PROBE` (`config/oems/ayaneo.yaml:1-4`, with `enabled: false` and comment "Do not enable without re-probe"). This is a real, lightweight lifecycle-gate mechanism. No explicit "PERMANENTLY DISABLED / RETIRED" state distinct from "temporarily blocked" was found in this repo's own code — `TROUBLESHOOTING.md:110-113` notes "If a source is permanently gone, there's currently no `semintel remove-source`... treat it as retired" — i.e., "retired" is an *operator convention*, not a modeled state.

### 5. Promotion readiness
Strong evidence. `semi_intel/domain/models.py` defines `CandidatePromotionSettings` and `CandidatePromotionEvent` (append-only audit trail, migration `a6a1b2c73e08`). Automatic promotion (`run_automatic_promotion`) "defaults off, requires every threshold in `CandidatePromotionSettings`, and enforces an hourly budget" (`CHANGELOG.md:573-574`). **Incident, caught in testing** (`CHANGELOG.md:575-578`): "caught and fixed a real transactional bug during testing where a discovery/suggestion failure's rollback would have silently discarded the just-committed promotion itself (fixed by committing the promotion before attempting either)."

### 6. Source starvation / observation collapse
No SemInt-specific incident found in this repo's own docs. `semi_intel/operations/health.py:47-59` implements a detection mechanism: if `scheduler.scheduler_enabled and not last_pipeline` → issue "Automation has not completed its first pipeline run"; if a pipeline exists but its age exceeds `pipeline_interval_minutes + missed_run_warning_minutes` → "degraded... pipeline has not run for N minutes."

### 7. Config drift
`ai/handoff/KNOWN_ISSUES.md:23-31` ("Observed, not a defect"): "Alembic head differs from the prior audit's stated head... a one-migration discrepancy from the prior audit's snapshot." Also `CHANGELOG.md` entry 3.3.13 (`CHANGELOG.md:3-11`, dated 2026-08-03): "Fixed the private 3.3.12 archive's `semintel.config.json`, which had been accidentally rewritten by a disposable frozen smoke to an absolute smoke database path... The bad config merely redirected the application to the empty smoke database."

### 8. Schema/deploy readiness
`semi_intel/operations/health.py:129-141`: health check compares live `alembic_version` against a hardcoded `EXPECTED_HEAD` and raises a "degraded" issue if mismatched — post-hoc health signal, not a pre-traffic-switch gate. `ai/handoff/ROLLBACK.md:41-49` documents the intended schema-incompatibility procedure but states "No schema changes were made this phase, so there is no schema-incompatibility scenario to plan around yet" — untested in practice.

### 9. Stale automation
`semi_intel/operations/scheduler.py:398-431` (`reconcile_stale_runs`): explicit mechanism to mark `RUNNING` job rows `ABANDONED` after `stale_run_threshold_minutes` if no active lease covers them — `health.py:66-77` explains the underlying failure mode: "A job whose process was killed outright... leaves its OperationalJobRun row stuck at RUNNING with no finished_at forever; nothing else ever revisits it... `stale_run_threshold_minutes` is exactly the operator-configurable setting for this... but was never actually consulted anywhere."

### 10. Retry/restart authority
`semi_intel/operations/scheduler.py:388-396` (`OperationalScheduler.retry`): manual/operator-triggered retry creates a new `OperationalJobRun` with `trigger=OperationalTriggerType.RETRY`, linked via `parent_retry_id`, incrementing `attempt_number`. Automatic retry is also declared (`job.next_retry_at`) but no code path was found in this pass that actually consumes it. Lease-based mutual exclusion (`LeaseManager.acquire`, `scheduler.py:119-156`) prevents duplicate concurrent execution — a concurrent second attempt is `SKIPPED`, not double-run.

### 11. Health vs scheduler state
Direct, explicit modeling. `semi_intel/operations/scheduler.py:78-105` (`effective_automation_state`): a layered state machine distinguishing `disabled` / `task_status_unavailable` / `task_not_installed` / `task_path_invalid` / `task_path_mismatch` / `task_action_mismatch` / `task_last_run_failed` / `task_never_ran` / `heartbeat_stale` / `running_normally`.

### 12. Remote host/deployment truth
`PHASE0_CONTAINMENT.md:1-9`: classification **UNVERIFIED_PRODUCTION**, "A production claim is not verified until the canonical fleet ledger records the deployed artifact digest and a real Windows task completes two unattended runs from the installed path."

### 13. "Scheduled" vs "actually running" (live execution state)
`semi_intel/operations/windows_task.py:97-157` (`WindowsTaskStatusService.status`): queries the live Windows Task Scheduler state separately from the *configured* action, and separately computes `path_matches_current`/`working_directory_matches_current`/`arguments_match_current`/`action_matches_current`.

### 14. Partial deploys / stale code
`ai/handoff/ROLLBACK.md:19-27`: describes rolling back only one of two changes from a multi-commit branch, a deliberate design to avoid partial-deploy hazards. No incident of partially-completed deploy found for SemInt itself.

### 15. Safe manual intervention during soak
`ai/handoff/STAGING_RELEASE_RUNBOOK.md:16`: staging schedule disabled by default, enabled only for a deliberate soak run. No explicit "does a manual run reset the soak clock" logic found in code — the policy answer lives only in the runbook.

### Additional incident found
`CHANGELOG.md:3-19` (v3.3.13, 2026-08-03): populated-database checkpoint accidentally repointed at an empty smoke-test database via a disposable smoke run overwriting `semintel.config.json`. Root cause: a test/smoke process's side effect leaked into a shipped config artifact. **Recurrence risk in fleet**: yes — generic "test/smoke tooling writes into a path that production config also reads from" class.

### Lineage evidence for semiconductor-intelligence
SemInt's invocation-vs-commit heartbeat pattern is explicitly named as **the fleet reference implementation** in two places outside its own repo: `clank-architecture/FLEET_LAWS.md:27` (Law 3): "**Reference:** semiconductor-intelligence invocation≠commit heartbeat columns." `clank-architecture/adr/0002-motherclank-supervisory-architecture.md:39`: "invocation vs successful-commit pair where the system evidences both (**SemInt pattern is the reference semantic**)." Additionally `clank-architecture/audits/CLANK_FLEET_ARCHAEOLOGY_REPORT_2026-08-24.md:197-198` records that SemInt's own fleet inventory found "hourly cron invoked pipeline run directly, bypassing OperationalScheduler, flagged for operator decision under Laws 3/5" — even the reference-pattern Clank had a live deployment that violated its own pattern.

---

## Repo 2: `C:\Users\anil\Clanks\clank-architecture` (reference/governance repo, not a fleet member)

### ADR adoption status (for adjudication)
- **ACTIVE**: `FLEET_LAWS.md:3` only.
- **PROPOSED — REVIEWED DRAFT** (not active): ADR-0002, 0003, 0004, 0006, 0007, 0008, 0009, 0010, 0011, 0012, 0014.
- **Proposed** (earliest/unreviewed language): ADR-0001.
- `NO_PROMOTION_POLICY.md:3`: Status **ACTIVE — PROMOTION FROZEN**, proposed 2026-08-21, scope = all 13 fleet repos including SemInt.
- No ADR titled or tagged "DO_NOT_STANDARDISE" exists in this repo.

### 1. Scheduler truth vs actual execution
`RISK_REGISTER.md:7` — R-003 (Critical): "Windows scheduled task fires but never starts SemInt." `adr/0008-execution-liveness-and-materialization-gap.md:1-25` — **Incident (dated 2026-08-22, operator-verified)**: "an interactive root redeploy ran `git stash -u` / `git stash pop` for oem-radar, smartwatch-clank, and feature-phone-clank. Untracked `logs/` directories were recreated `root:root`; cron shell redirects failed BEFORE collector execution. Result: scheduler invocations existed, zero application runs materialized, no failure records were written... the outage stayed silent ~36 hours." Codified lesson: `SCHEDULE_EXPECTED ≠ SCHEDULER_FIRED ≠ PROCESS_STARTED ≠ RUN_MATERIALIZED ≠ RUN_COMPLETED ≠ OUTCOME_RECORDED`. Registered in `conformance/GOLDEN_INCIDENTS.md:35,37` as `PRE-EXEC-MATERIALIZATION-GAP` / `P4-G1 CRON-FIRED-NO-RUN`.

### 2. Natural-cycle vs manual/deploy-cycle accounting
`adr/0011-no-work-execution-semantics.md:1-19` — **Incident (dated 2026-08-24, OEM Radar production)**: "three legitimate hourly executions fired, started, completed successfully with `done: 0 source(s) crawled` due to min-interval/due-gating - and wrote NO `crawler_runs` row. P-4 inferred MATERIALIZATION_GAP from fired+started+no-record. The inference was invalid." Fixed by introducing `materialization_policy` (ALWAYS/WHEN_WORK_ATTEMPTED/OPTIONAL/UNKNOWN) and positive `NO_WORK_DUE` evidence, never inferred from absence.

### 3. Soak clocks and reset semantics
`adr/0006-continuity-and-epoch-semantics.md:68`: "**Soak.** The QC soak clock is not reset by this incident [2026-08-23 volume-loss]. Gates that become unmeasurable for affected lanes report UNKNOWN / NOT-YET-MATURE, never zero." `QC_SOAK_PRECONDITION_VERIFICATION.md:1-24`: two-axis model — Axis A (each Clank's own soak, owned by that Clank) vs Axis B (Motherclank's own QC-corpus readiness) — "Axis B passing **never** promotes a Clank, ends a development soak, or alters deployment status."

### 4. Lifecycle states
`NO_PROMOTION_POLICY.md:20-31`: four fleet-wide labels — `PROTOTYPE`, `UNVERIFIED_PRODUCTION`, `VERIFIED_PRODUCTION` (currently unusable while freeze is active), `QUARANTINED`. `adr/0008:54-60` defines a more granular execution-expectation enum: `PERIODIC | FINITE_SOAK | MANUAL | ON_DEMAND | DISABLED | RETIRED | UNKNOWN` — explicitly separates `DISABLED` from `RETIRED`.

### 5. Promotion readiness
`FLEET_LAWS.md:65-71` (Law 8 — Promotion gates): "No source reaches production scheduling without soak evidence, an explicit promotion record, and rollback state; conversely every production-scheduled source appears in a promotion record." Violators listed: "tablet approved-never-scheduled promotion theater; smartwatch stage-c merged-but-undeployed latent notify; oem-radar bankai soaks operated outside any record until Phase 2A landed them."

### 6. Source starvation / observation collapse
`audits/CLANK_FLEET_ARCHAEOLOGY_REPORT_2026-08-24.md:179` — smartphone-clank: "Scheduler starvation/Google health repair followed in fa52929 and b8b8988." `FLEET_LAWS.md:26-31` (Law 3, Health honesty): "smartwatch failing timer lane (retired Phase 2A) fired hourly with zero observability."

### 7. Config drift
`CTW_ONBOARDING_DOGFOOD.md:37-40`: "FGT registry db filename had drifted from the live-verified inner name (`newsroom.db`); caught during this pass because the refresh script and registry were cross-checked."

### 8. Schema/deploy readiness
`GOLDEN_INCIDENT_CORPUS.md:29` — GIC-14 "schema drift / unsupported schema," plane "persistence," executable fixture exists. `DATA_SURVIVABILITY.md:24` — R4 "bad migration," detection = "schema-revision drift."

### 9. Stale automation
`conformance/GOLDEN_INCIDENTS.md:23` — "ZOMBIE-AUTHORITY | disabled timer still fires | Smartwatch fleet snapshot." `conformance/GOLDEN_INCIDENTS.md:24` — "AUTHORITY-BYPASS | cron bypasses registered scheduler | SemInt fleet snapshot." `FLEET_LAWS.md:44` (Law 5 violators): "smartwatch dual-lane (cron kept, systemd retired 2026-08-21T21:06Z)."

### 10. Retry/restart authority
`FLEET_LAWS.md:57-63` (Law 7 — Writer coordination): "All writers of one SQLite database share one cross-process lock — dashboard paths included." Violators: "FGT /api/run threading.Lock bypass; KTW feedback POST bypasses RunLock."

### 11. Health vs scheduler state
`FLEET_LAWS.md:25-31` (Law 3) is the governing law: "Scheduler invocation ≠ successful work; a failing scheduled unit must be observable in one query." Violators explicitly named: "KTW dashboard HEALTHY-iff-ever-succeeded; FGT 200+0=ok; smartphone dormant maintenance-alerting; smartwatch failing timer lane (retired Phase 2A) fired hourly with zero observability."

### 12. Remote host/deployment truth
`RISK_REGISTER.md:5` — R-001 (Critical): "Repository head is mistaken for the deployed artifact. Containment: Canonical ledger separates `source_sha` from `deployed_sha`." `FLEET_LAWS.md:73-74` (Deferred Law 9): "A repository's default branch must never trail its own production checkout longer than one review cycle... First violations already on record: KTW main-behind-production (healed in Phase 2A by merge; host checkout still trails), SemInt host pre-heartbeat-fix." `audits/CLANK_FLEET_ARCHAEOLOGY_REPORT_2026-08-24.md:185`: "Fleet snapshot reports production at b8b8988, while the repository includes later security/containment/QC work" (smartphone-clank) — still open.

### 13. "Scheduled" vs "actually running"
`adr/0008:29-36` (six-stage model) and `adr/0011:22-30` (seven-stage refinement): `SCHEDULE_EXPECTED → SCHEDULER_FIRED → PROCESS_STARTED → APPLICATION_EXECUTED → RUN_MATERIALIZED → RUN_COMPLETED → OUTCOME_RECORDED`, plus an orthogonal liveness dimension: `CURRENT | MATERIALIZATION_GAP | EXECUTION_STALE | SCHEDULER_SILENT | INTENTIONALLY_DORMANT | UNKNOWN`.

### 14. Partial deploys / stale code
`adr/0009-runtime-state-separation-and-destructive-safety.md:9-19` — two incident families (both 2026-08-22/23, operator-verified): (1) the `git stash -u` root-redeploy runtime-path incident (topic 1). (2) `docker volume rm` against pattern-inferred names "destroyed two REAL production volumes ('staging' in a name provided zero evidence of disposability)." Fix: `DISCOVER → RESOLVE ACTUAL IDENTITY → CLASSIFY → PROVE BACKUP → DISPLAY EXACT TARGET → EXPLICIT AUTHORISATION → MUTATE → VERIFY` contract.

### 15. Safe manual intervention during soak
`adr/0006-continuity-and-epoch-semantics.md:68` (topic 3) is the direct answer: manual/operator recovery actions do not reset the soak clock — affected lanes instead report UNKNOWN/NOT-YET-MATURE. `QC_SOAK_PRECONDITION_VERIFICATION.md:24`: "Motherclank may observe and report this lifecycle; it does not own or influence it" — pause/restart authority explicitly deferred to a future M5 ADR ("NOT NOW").

### Golden Incident Corpus / Risk Register — adopted vs proposed distinction
`GOLDEN_INCIDENT_CORPUS.md` and `conformance/GOLDEN_INCIDENTS.md` describe themselves as normative/machine-enforced with a CI-executed status distinction: **executable** (fixture runs in CI, 21 of 25 GIC entries) vs **registered_pending_fixture** (2 entries). This is a stronger adoption signal than the ADRs themselves — the fixtures already run in `fleet-laws.yml` CI (pulled into multiple fleet repos' GitHub Actions on every push). `RISK_REGISTER.md` (5 entries) carries no explicit adopted/proposed status column — treat all 5 rows as live/open risk tracking.

---

## Survey 5 of 6: smartwatch-clank + tablet-clank

# Pass 0A — Operations Domain Evidence Inventory

Read-only survey of `smartwatch-clank` and `tablet-clank`. No files modified. No standards proposed — evidence only.

---

## Repo: tablet-clank

### 1. Scheduler truth vs actual execution
- `docs/PROJECT_STATE.md:8` — the "2026-08-29 'timer not found' sweep covered NAS/WSL/Windows only and missed Hetzner" — a scheduler-audit that reported a schedule as absent when it was actually running.
- `HANDOFF.md:55` — same fact stated in full.
- `docs/ARCHITECTURE.md:29` and `docs/OPERATIONS.md:71` — "There is no scheduler" in-repo; all scheduling lives in deploy-time systemd artifacts outside the Python codebase.

### 2. Natural-cycle vs manual/deploy-cycle accounting
- `docs/PROJECT_STATE.md:71-72` (Wave 2 update) — "Baseline cycle accepted 23 creating **0 events** (FIRST_SEEN != NOVELTY)."
- `tablet_clank/campaign.py:16-22` — campaign cycle 1 (baseline) is immediately followed by cycle 2 (resight) with no interval sleep, an explicit manual/accelerated cadence distinguished from the natural 7200s cadence used afterward.
- No "deploy-triggered vs schedule-triggered" cycle field exists in the JSONL schema — cycle records don't carry a trigger-source tag; provenance is reconstructed only from external context, not stored in-band.

### 3. Soak clocks and reset semantics
- `docs/SOAK_OPERATIONS.md:45` — "An interrupted run restarts from cycle 1 on the next invocation; completed cycles are preserved in the JSONL report but are not fabricated as resumed state."
- `docs/SOAK_READINESS.md:54-56` — 12 consecutive two-hour cycles required for a clean `PASSED`; any non-`SUCCESS` cycle voids the run for promotion purposes.
- `tablet_clank/campaign.py:18-19` — campaign soak is stricter than the historical frozen soak: any non-SUCCESS cycle aborts the campaign.
- **Direct manual-reset incident**: `docs/PROJECT_STATE.md:109-114`, `var/campaigns/honor-uk-iso-001/operator_abort.json` — the Windows campaign `honor-uk-iso-001` was operator-terminated at cycle 2/12 for a host move. Its 2 healthy cycles were explicitly **not** counted toward the later NAS campaign's 12/12 promotion evidence.

### 4. Experimental/production/mothballed/blocked lifecycle states
- `tablet_clank/sources/registry.py:5-18` — only two `state` values exist in code: `EXPERIMENTAL` and `DISABLED`. No `BLOCKED` or "mothballed" state type exists.
- `apple_in_sitemap` (`registry.py:10`) is the one source with `DISABLED` state.
- Production eligibility is layered *on top of* `state`, not a new state value: `docs/ARCHITECTURE.md:8` — "a source can never become production-eligible by allowlist membership alone, and demoting a source's `state` automatically removes it from production even if the allowlist tuple is stale."
- Campaign approval (`CAMPAIGN_APPROVED_SOURCE_IDS`, `registry.py:35`) is a third, narrower, independent gate.
- No "temporarily blocked" state distinct from "permanently disabled" exists anywhere in this repo's code.

### 5. Promotion readiness
- `docs/SOAK_READINESS.md:58-60` — "Promotion is a separate human-reviewed phase. Soak completion never automatically promotes a source."
- Wave 3 (`honor_uk_tablets`) promotion evidence: 12/12 NAS campaign cycles SUCCESS, byte-identical canonical DB pre/post, then a separate, explicit `PRODUCTION_ALLOWLIST` edit dated 2026-08-29.
- No incident of premature promotion was found.

### 6. Source starvation / observation collapse
- `docs/SOAK_READINESS.md:24` — "disappearance detection is not implemented" — explicit gap: this repo does not detect a source going silent/collapsing production count; it only detects *zero* results.
- `docs/ARCHITECTURE.md:29` lists "repeated-healthy-run disappearance semantics" under `PLANNED` (not implemented).

### 7. Config drift
- `docs/PROJECT_STATE.md:8`, `HANDOFF.md:55` — **direct incident**: Hetzner's live checkout still runs the Wave-1 three-source `PRODUCTION_ALLOWLIST`, while the repo's `main`/registry.py already reflects the Wave-3 four-source allowlist.

### 8. Schema/deploy readiness
- `tablet_clank/storage/db.py:26-35` — schema migrations applied idempotently by the app itself at open time, not via a separate pre-deploy migration step. No explicit pre-traffic schema-compat check found; no incident of stale-schema deploy found.

### 9. Stale automation
- `HANDOFF.md:39`, `docs/SOAK_OPERATIONS.md:7`, `docs/ARCHITECTURE.md:29` — the old frozen six-source soak (`FROZEN_SOAK_SOURCE_IDS`) is retired-but-still-present code that now *refuses* to run rather than being deleted.

### 10. Retry/restart authority
- No automated retry logic exists anywhere in `tablet_clank/*.py`. All retry/restart is manual. Double-execution is prevented via `SoakLock`/production lock sharing one lock domain, an exclusive atomically-created lock file with PID+liveness-based stale-lock reclaim.

### 11. Health vs scheduler state
- No "scheduler says enabled but job unhealthy" concept found — this repo's runners have no persistent "enabled" scheduler-state field at all.
- `health` CLI command reports per-source DB-derived health independent of any scheduler state.

### 12. Remote host/deployment truth
- **Direct incident** (same as #1/#7): a fleet-wide "timer not found" sweep missed Hetzner and produced a false negative.
- `docs/PROJECT_STATE.md:11` — pre-promotion DB backup with sha256 hash recorded as an explicit truth-anchor.

### 13. "Scheduled" vs "actually running"
- No persistent "current execution state" record is written to the database — the only live-state signal is the lock file's presence, transient and PID-scoped, not a queryable execution-status row.

### 14. Partial deploys / stale code
- Same allowlist-drift incident (topic 1/7/12) is effectively a partial-deploy: old allowlist code shipped to Hetzner is behind repo `main`.

### 15. Safe manual intervention during soak
- **Direct, extensively documented incident**: `var/campaigns/honor-uk-iso-001/operator_abort.json` + `docs/PROJECT_STATE.md:109-114` + `docs/SOAK_OPERATIONS.md:17`.
  - Operator manually aborted campaign `honor-uk-iso-001` mid-soak (between cycle 2 and cycle 3) to relocate the campaign from Windows to a NAS.
  - `CTRL_C_EVENT` did not reliably reach the app's `KeyboardInterrupt` handler (shared console with unrelated processes); operator fell back to `Stop-Process -Force`/`TerminateProcess` on exact PIDs, only after confirming via JSONL + file mtimes that no I/O was in flight.
  - Campaign DB integrity verified `ok` post-stop; canonical DB proven untouched; stale lock file deliberately left in place as evidence; the 2 completed cycles preserved but explicitly excluded from later promotion-counting evidence.
  - Recurrence risk: the graceful-shutdown gap (`CTRL_C_EVENT` not reliably reaching a Python process sharing a console) is a Windows-specific mechanism issue that could recur for any other Windows-hosted long-running Clank process using the same interrupt-handling pattern; nothing in the code was changed to fix the signal-delivery gap itself, only documented as an operational workaround.
  - Design-level protection: `campaign.py:14` — canonical DB is opened `mode=ro` for preflight, structurally preventing a campaign from writing to production data regardless of how it's aborted.

---

## Repo: smartwatch-clank

### 1. Scheduler truth vs actual execution
- `docs/samsung-stage22-report.md:74-76` — "Task Scheduler is a temporary launcher, not part of soak correctness... A changed host identity is persisted as an explicit migration with the elapsed gap since the last recorded run."
- `docs/run-scope-correction-2026-08-19.md:143-150` — "Windows scheduler — explicitly unverified": "The original Windows Task Scheduler production soak... is documented but its current state cannot be checked remotely."

### 2. Natural-cycle vs manual/deploy-cycle accounting
- `docs/hetzner-deployment-2026-08-18.md:46-57` — four manual verification cycles explicitly distinguished from the timer-driven cycle.
- `docs/coros-updates-firmware-version-adjudication-2026-08-30.md:25-38` — post-repair requirement: "Fresh soak clock at the first post-fix natural 6-hour cycle; ≥12 clean natural cycles" — natural cycles are explicitly the only cycles that count toward re-promotion soak evidence.

### 3. Soak clocks and reset semantics
- `docs/ticket-coros-updates-firmware-novelty.md:66` — "Fresh soak clock at the first post-fix natural 6-hour cycle" — a data/code fix explicitly resets the soak clock for that source.
- No generic bounded-cycle promotion-runner state machine exists (unlike tablet-clank); "soak" here means an ongoing natural-cadence production-candidate observation window evaluated by an operator.

### 4. Experimental/production/mothballed/blocked lifecycle states
- `core/models.py:13-40` — `CollectorTier` enum: `PRODUCTION` / `EXPERIMENTAL` only. `RunScope` enum: `PRODUCTION` / `EXPERIMENTAL` / `ALL` (a separate concept).
- `docs/coros-updates-firmware-version-adjudication-2026-08-30.md:3` — "Promotion BLOCKED; stays EXPERIMENTAL." **`BLOCKED` exists only as prose/ticket status, never as an enum value or DB column** — a clear lifecycle-state enforcement gap.

### 5. Promotion readiness
- `docs/ticket-coros-updates-firmware-novelty.md:69-72` — re-promotion requires soak + "both production gates (tier + `production_allowlist`) applied per the standard per-source path" — two-gate pattern, matching tablet-clank's.
- **Direct near-miss/blocked-before-promotion incident**: `coros_updates` was caught, via live soak evidence, injecting 23 simultaneous false `FIRMWARE_RELEASED` HIGH-confidence events from a single Zendesk editorial timestamp touch, *before* it reached production. Root cause: an editorial `updated_at` timestamp was used as the field driving change classification.

### 6. Source starvation / observation collapse
- `src/smartwatch_clank/core/health.py:46-61` (`assess_catalogue`) — direct, implemented collapse-ratio guard: raises on unexpected zero and on a collapse ratio below `failure_ratio`.
- `var/continuity/continuity-events.jsonl` line 3 (`sw-20260818-observation-gap-0003`) — explicit, permanent record of an observation gap (2026-08-18 to 2026-08-23) with the invariant "Absence inside this window is never zero and never novelty."

### 7. Config drift
- **Direct, resolved incident**: `docs/ticket-garmin-relay-production-wiring.md`, status "RESOLVED 2026-08-30." The soak deploy path correctly propagated `SMARTWATCH_CLANK_GARMIN_PROXY`; the production deploy path (untracked deployment artefact) did not, silently disabling the Garmin proxy for production. Root cause: two independently-maintained wrapper scripts for two lanes.
- `docs/hetzner-deployment-2026-08-18.md:75-76` — a second, related drift bug: `deploy/run.sh` silently defaulted to `--mode production` instead of `--mode experimental` (fixed via PR #11).

### 8. Schema/deploy readiness
- `docs/hetzner-deployment-2026-08-18.md:13-23` — "Commit parity" table cross-checks five independent sources of truth before/after deploy. No distinct schema-version gate found (unlike tablet-clank's `schema_migrations` table).

### 9. Stale automation
- **Direct, dated incident**: `docs/run-scope-correction-2026-08-19.md`. `CollectorRegistry.selected()` treated `mode is CollectorTier.EXPERIMENTAL` as "return every collector regardless of tier" — inherited unchanged from before multi-OEM expansion. Once the new experimental soak timer went live on Hetzner (2026-08-18), it began silently re-running the four production-tier Samsung collectors on its own independent 2-hour cadence, in addition to their real production cron. Fix: new `RunScope` enum decoupled from `CollectorTier`. Explicitly flagged as a recurrence risk for any Clank reusing a similar tier/mode enum pattern.
- `docs/samsung-stage22-report.md:50` — Windows Task Scheduler task has twelve permanent daily triggers with no hard-coded end date and unverified current status.

### 10. Retry/restart authority
- `docs/samsung-stage22-report.md:13` — bounded automatic retry at the HTTP-fetch level (three bounded attempts).
- `docs/samsung-stage22-report.md:70` — "Task Scheduler `IgnoreNew` and the existing atomic database lock jointly prevent overlap."
- `src/smartwatch_clank/core/lock.py` — genuine OS-level `flock`/`msvcrt.locking` (not PID-liveness heuristic) specifically because the old PID/hostname-based reclaim logic was proven broken in Docker's one-shot `run --rm` model.

### 11. Health vs scheduler state
- `docs/hetzner-deployment-2026-08-18.md:61` — the Garmin 403 case: systemd correctly sees "failed" because health-based exit code correctly propagates a genuine partial failure — a case where health and scheduler state are deliberately kept in sync, by design.
- `src/smartwatch_clank/core/health.py:20-38` — typed exception taxonomy so a scheduler-visible failure "says why."

### 12. Remote host/deployment truth
- `docs/hetzner-deployment-2026-08-18.md:13-23` — five-way commit-parity check.
- `docs/run-scope-correction-2026-08-19.md:143-150` — direct admission that the Windows Task Scheduler host's actual state "cannot be checked remotely."

### 13. "Scheduled" vs "actually running"
- No persistent "current execution in progress" state row found — same as tablet-clank, the only live-execution signal is the `RunLock` file's OS-level lock state.

### 14. Partial deploys / stale code
- **Direct, dated incident (data loss, analogous class)**: `var/continuity/continuity-events.jsonl` — `sw-20260823-volume-loss-0001`: "Destructive volume deletion on 2026-08-23 destroyed the live database including all observations newer than the newest backup." Restored from a 2026-08-18 backup; explicit epoch bookkeeping added: "Restoration does NOT imply continuity." Root cause of the deletion itself cites `clank-architecture/adr/0006` and `DATA_SURVIVABILITY.md` (external, not detailed in this checkout).

### 15. Safe manual intervention during soak
- No formal soak-clock/maturity-timer mechanism exists in this repo, so no direct analog to tablet-clank's operator-abort incident. Manual `collect`/CLI runs and scheduled runs share the same lock domain, making concurrent manual intervention safe by construction.

### Japan mini-PC experimental soak episode
- **Nothing found.** Exhaustive search across all non-git, non-venv, non-build files in this repo returned zero matches for Japan/MousePro/GEEKOM/mini-PC. Not documented anywhere in this repository as checked out locally.

---

## Lineage evidence (cross-repo citations)

- `smartwatch-clank/src/smartwatch_clank/core/lock.py:16,27-31` — explicitly names "Diagnostic Clank incident 5f280abf" (the previously-discovered PID=1-in-container bug), "Free Game Tracker (newsroom/run_lock.py)", and "OEM Radar (core/run_lock.py, PR #4)" as the source design this file's lock mechanism was ported from.
- `tablet-clank/tablet_clank/soak.py:54` states: "The OpenProcess probe mirrors feature-phone-clank core/run_lock.py" — copied from a third sibling repo.
- `smartwatch-clank/deploy/deploy_run.sh:2` — "Feature Phone-style production cron wrapper for Smartwatch Clank."
- `smartwatch-clank/var/continuity/continuity-events.jsonl` — all three continuity events cite `clank-architecture/adr/0006-continuity-and-epoch-semantics.md` and `clank-architecture/DATA_SURVIVABILITY.md` as the authoritative shared-schema source.

**Conclusion on lineage**: both repos show clear, explicit, comment-documented pattern reuse from sibling Clanks and from a shared `clank-architecture` spec repo — not independent convergence; it is deliberate, cited borrowing, sometimes with the specific bug the borrowed code fixes named inline.

---

## Survey 6 of 6: diagnostic-clank (heavy mine — GitHub repo + live NAS incident log)

# Pass 0A Evidence Inventory: Operations Domain — diagnostic-clank

## SOURCE 1 — Repo Clone Findings (by topic)

**1. Scheduler truth vs actual execution**
Central design principle throughout. `clank-fleet/src/clank_fleet/execution_results/oem_radar.py` codifies it explicitly: exit code 2 (`LockError`) is deliberately left `UNKNOWN` rather than failed — any output not matching an attested pattern also stays `UNKNOWN` rather than inferred. `scheduler_fire.py` defines a `SchedulerFireProbe` protocol that returns empty rather than fabricating a non-fire when no evidence exists. `ctw_scheduler_probe.py` only counts a fire as positive when the expected target string literally appears in a cron log line. `fleet.yaml`'s semiconductor-intelligence entry records: "heartbeat migration a0b1c2d3e404 applied and PROVEN: invocation 2026-08-21T21:53:08Z != commit 2026-08-21T21:55:12Z."

**2. Natural-cycle vs manual/deploy-cycle accounting**
`operations/phase0/POST_MERGE_HETZNER_NAS_CONVERGENCE.md` requires "two unattended runs" as evidence distinct from a single controlled/manual verification run. `fleet.yaml`'s smartwatch-hetzner-soak-timer-retired entry shows a scheduler fired every 2 minutes but was disabled after being found FAILED on every fire.

**3. Soak clocks and reset semantics**
`clank_runtime/contracts/lifecycle.py` defines `SourceLifecycleState.SOAK` and `SoakStatus` (cycles_completed, cycles_required, failure_count, false_event_count, promotion_gate_met). ADR 0004 ("No automatic execution of stale offline operational actions") states restart/deploy/restore require live reconfirmation. `docs/runbooks/soak-test-report.md` is an unpopulated Stage-0 template — no soak methodology has been operationalized yet in this repo (governance gap, not an incident).

**4. Lifecycle states**
`lifecycle.py`'s `ALLOWED_SOURCE_TRANSITIONS` is the authoritative state machine: `DISCOVERED → RESEARCH → EXPERIMENTAL → SOAK → PRODUCTION`, with `DISABLED` and `QUARANTINED` as parallel terminal/semi-terminal states reachable from nearly every state. `PRODUCTION → SOAK` is allowed ("demote for re-soak after major change"). `fleet.yaml` shows real instances at each state.

**5. Promotion readiness**
`SoakStatus.promotion_gate_met: bool = False` (default false). `docs/runbooks/production-readiness-review.md` is an empty Stage-0 template. `operations/phase0/` establishes governance gates (`promotion_eligible: false` hardcoded, requires human reviewer sign-off) — no automated promotion path exists at this stage. `fleet.yaml`'s `promotion_policy.frozen: true` fleet-wide.

**6. Source starvation / observation collapse**
`HealthPayload` (contracts/health.py) carries `observed_count`/`previous_observed_count`/`expected_range_min/max` — directly citing the real incident it was built to prevent: "Watch Clank product-catalogue ZERO_ITEMS must not be reported as overall healthy." ADR 0007 documents the archetypal incident: "Watch Clank (and similar) could report all collectors healthy while the Discord delivery path was missing or misconfigured. Operators saw a green fleet with no newsroom output."

**7. Config drift**
`fleet.yaml` free-game-tracker entry: `database_path: container volume (repo-dir newsroom.db is STALE legacy copy mtime 2026-08-09)`. `docs/FLEET_INVENTORY.md`: "An exact `source_sha` means only that the repository head was inspected. It is not evidence that the commit is deployed."

**8. Schema/deploy readiness**
`POST_MERGE_HETZNER_NAS_CONVERGENCE.md`: "Rehearse migration against the isolated restore and record schema revisions before touching the candidate release."

**9. Stale automation**
`fleet.yaml`: `smartwatch-hetzner-soak-timer-retired` — a systemd timer that fired every cycle and failed every time until discovered and disabled during a Phase 2A repair, with guard note: "do NOT re-enable while cron lane lives (Law 5)." Also `fpc-hetzner-prod-cron-01` running "main-pinned-pre-phase0 (4 behind 201ddf9)."

**10. Retry/restart authority**
`operations.py` (`OperationType.RESTART`, `RUN_NOW`) exists only as a contract stub — Stage 0.5 explicitly implements *no* operational capability. ADR 0005 (fencing) requires a valid ownership token and definite NAS offline status before any Level-3 fallback local execution.

**11. Health vs scheduler state**
ADR 0007 is the canonical statement (collection-health vs delivery-health as separate reported domains).

**12. Remote host/deployment truth**
The entire `operations/phase0/` package exists for this: `OPERATOR_INSTANCE_CHECKLIST.md` keeps HETZNER/NAS as explicit `UNKNOWN`/`HOLD` placeholders until operator-confirmed; `preflight.py` is a read-only evidence collector, "repository head alone is not proof of deployment."

**13. "Scheduled" vs "actually running"**
`oem_radar.py`'s `locate_invocation_block()` reconciles "cron's fork time vs the container's first log line" and returns `None` rather than guessing when they don't correlate within tolerance.

**14. Partial deploys / stale code**
`fleet.yaml` chinese-tech-wire/oem-radar entries record exact deployed SHA vs `origin/main` deltas with explicit reconciliation notes.

**15. Safe manual intervention during soak**
ADR 0004: only `SAFE_OFFLINE` idempotent items may auto-sync; restart/deploy/restore require live reconfirmation specifically because of soak/continuity risk. No incident of a corrupted soak from manual intervention found in Source 1 (see Source 2 for real occurrences).

---

## SOURCE 2 — Live NAS Incident Log ("Ls") Findings

18 incidents total, all read. Nearly all are Operations-relevant.

### Full incident list (chronological by update time, newest first)

| # | Title | Clank | Status | Date | Topics | Fleet-wide vs local |
|---|---|---|---|---|---|---|
| 1 | FGT NAS parallel-soak DSM task silently stopped firing (2.4d zero fires) | free-game-tracker | RESOLVED | 2026-08-30 | 1,6,7,9,11 | Fleet-wide relevant (DSM config gotcha could recur on any Clank) |
| 2 | Watch Clank — Seiko Prospex source-gap miss | watch-clank | OPEN | 2026-08-29 | none (editorial/QC) | n/a |
| 3 | Watch Clank — Casio G-Shock operator-error miss | watch-clank | OPEN | 2026-08-29 | none (editorial/QC) | n/a |
| 4 | Smartwatch Clank NAS parallel-soak migration (lock bug found+fixed) | smartwatch-clank | PARTIAL | 2026-08-27 | 2,3,10,12,14 | Fleet-wide (lock bug class = same as OEM Radar's) |
| 5 | Watch Clank — Casio notification-layer triage | watch-clank | OPEN | 2026-08-27 | none (editorial/UX) | n/a |
| 6 | CTW cutover-readiness: Hetzner not actually canonical production | chinese-tech-wire | PARTIAL | 2026-08-27 | 4,5,9,10,14 | Fleet-wide (promotion-authority ambiguity, missing NAS lock) |
| 7 | NAS canary stuck on stale lock, ~80+ silent no-op fires | oem-radar | RESOLVED | 2026-08-27 | 1,6,9,10,11,13 | Fleet-wide (PID-namespace lock bug recurred elsewhere) |
| 8 | Watch Clank — Casio regional recall failure | watch-clank | OPEN | 2026-08-27 | none (editorial/QC) | n/a |
| 9 | ClankLift host-truth census: NAS/Hetzner access gaps | fleet-wide | RESOLVED | 2026-08-27 | 12,13 | Fleet-wide |
| 10 | Diagnostic Clank's own NAS instance stale 8 days | fleet-wide | OPEN | 2026-08-27 | 9,12,14 | diagnostic-clank/NAS-specific (but pattern is fleet-wide-relevant) |
| 11 | Agent deleted production DB volume, no backup — total loss | feature-phone-clank | RESOLVED | 2026-08-23 | 10,15 | Fleet-wide (agent-tooling discipline gap) |
| 12 | Agent deleted production DB volume, restored 4-day-stale backup | smartwatch-clank | PARTIAL | 2026-08-23 | 10,15 | Fleet-wide |
| 13 | Aug-22 fleet-wide scheduler outage (root git stash flipped log ownership) | fleet-wide | PARTIAL | 2026-08-23 | 1,9,13 | Fleet-wide (canonical exemplar) |
| 14 | Beelink ME Pro missed — source-gap hypothesis rejected | oem-radar | OPEN | 2026-08-18 | none (editorial/coverage) | n/a |
| 15 | Packaged app's subprocess used its own bootloader as interpreter | chinese-tech-wire | RESOLVED | 2026-08-18 | 10 (manual-run trigger reliability) | diagnostic-clank/desktop-specific |
| 16 | Helldivers 2 PS Plus never posted to Discord (missing delivery path) | free-game-tracker | RESOLVED | 2026-08-18 | 6,11 (health/delivery split) | Fleet-wide (relates directly to ADR 0007's dual-domain-health rationale) |
| 17 | Concurrent Docker containers both ran as full DB writers | watch-clank | RESOLVED | 2026-08-18 | 10 | Fleet-wide (containerization breaks single-host lock assumptions) |
| 18 | DSM Task Scheduler recurrence misread as hourly (was daily) | oem-radar | RESOLVED | 2026-08-18 | 1,13 | Fleet-wide (DSM UI gotcha) |

Items 2, 3, 5, 8, 14 were opened and read; confirmed on read that they are editorial/QC-domain incidents with no scheduler/deploy/config/health-infrastructure content — correctly out of scope for the 15 Operations topics.

`/reports` was also checked and cross-referenced but not separately re-mined to avoid duplicating evidence already captured with full incident structure above.

### Most significant repeated failure classes across both sources
- PID-namespace-unsafe stale-lock reclaim logic, independently found and fixed in three different Clanks (watch-clank, oem-radar, smartwatch-clank) — same bug class, same fix pattern (flock), discovered three separate times.
- "Scheduler enabled/healthy in CLI" ≠ "job actually executing" — occurred at least 4 times (Aug-22 outage, OEM Radar stale lock, FGT DSM silent stop, DSM daily-misread) across 3 different Clanks and both DSM and cron/systemd scheduler types.
- Agent-performed destructive action against production state without a prior read-only identity check — occurred twice in one week (feature-phone-clank total loss, smartwatch-clank partial loss), both explicitly attributed to "trusting a naming-pattern guess."
</content>
