# Smartphone Clank DEPLOY-COM-001 live-proof admission — 2026-09-05

```json
{"clank":"smartphone-clank","date":"2026-09-05","findings":[{"standard":"STD-DEPLOY-COM-001","kind":"conformance","summary":"LIVE_PROOF_CONFIRMED at Smartphone e514c45dca4cf966441c27799d98761096dc8c40 on target hetzner:/opt/smartphone-clank (systemd source-specific timers + dashboard service): intended SHA = host checkout = venv import path, .deployed-id transitioned from 90a1ad4, Alembic advanced 0007→0008_analyst_action_integrity through canonical migration machinery (procedural deviation: Alembic env.py resolved to live DB instead of intended scratch, creating uq_analyst_action_terminal partial unique index on analyst_actions — migration succeeded cleanly, 0→0 rows, quick_check ok, DB size 5,902,336→5,906,432), stale dashboard process (PID 1606365 from Sep 3, HTTP 500) restarted (PID 1738142, HTTP 200), /proc/PID/fd/ proved dashboard and scheduled collectors open the same /opt/smartphone-clank/data/clank.db, natural production_scheduled timer fire at 21:46:34Z executed samsung_us_support_sitemap successfully with 0 discoveries and 0 new devices (no false novelty), collector_runs 349→350."}]}
```

## Scope and mode

This is a **Standards-only recording/admission pass** (M49). The live-proof
actions were executed in the separately authorized M48-SMARTPHONE bounded
deploy pass; this pass made **no host access, no deployment/restart, no
database change, no collector execution, and no source modification**. It
records and admits the completed proof for `STD-DEPLOY-COM-001` at Smartphone
`e514c45dca4cf966441c27799d98761096dc8c40`, target
`hetzner:/opt/smartphone-clank`, scope: this exact source SHA + target +
systemd source-specific timers + dashboard service.

## Pre-deploy state

The pre-M48 live checkout was at `90a1ad4736a871fb48eb4afe5f539d9a9097ed95`
on `main`, clean, classified `BEHIND_CANON` — 10 commits behind canonical
`e514c45`. Dependency diff was empty (no venv rebuild required). All 8
production source timers were enabled + active. The dashboard service was
active. The DB was at Alembic `0007_wave1_baseline_state` with 32 tables and
quick_check ok.

## Backup

Created using SQLite online backup API as the service user:
`/opt/smartphone-clank/backups/clank-pre-m48-e514c45.db`,
5,902,336 bytes, sha256
`a578cfadc0f8478c1f22924c4c0a4210bfc144f8ab323c2be5f3c9a8facdb673`,
quick_check ok.

## Alembic procedural deviation — preserved honestly

A scratch-first Alembic qualification was intended. The `-x sqlalchemy_url`
override was supplied to point Alembic at a scratch copy. However,
`alembic/env.py` reads `config.get_main_option("sqlalchemy.url")` from
`alembic.ini`, which contains `sqlite:///./data/clank.db` — a CWD-relative
path. The working directory remained `/opt/smartphone-clank`, so Alembic
resolved to the **live production DB**. The migration therefore ran directly
against live, bypassing the scratch-copy step entirely. This was an
**unintended mutation path** that succeeded cleanly. It is recorded as
history, not rewritten or hidden.

## Alembic 0007 → 0008 transition

The canonical migration `0008_analyst_action_integrity` adds a partial unique
index `uq_analyst_action_terminal` on `analyst_actions(target_type, target_id)
WHERE action <> 'note'`. The live DB's `analyst_actions` table already existed
with the correct columns and 0 rows, so the index creation was the only effect.
Post-migration: Alembic `0008_analyst_action_integrity`, quick_check ok, DB
size 5,902,336 → 5,906,432, all 32 tables preserved, no data loss.

## Dashboard stale-process finding and restart

The dashboard process (PID 1606365) had been running since Sep 3 — it imported
pre-deploy code and returned HTTP 500 on page GET. This was an in-scope
stale-process condition discovered during M48, not pre-existing and irrelevant.
After `systemctl restart smartphone-clank-dashboard.service`: new PID 1738142,
service active, HTTP 200 restored with production data visible. No collection
was triggered merely by restart or page GET.

## Same-state-path proof

The restarted dashboard's `/proc/PID/fd/` shows `/opt/smartphone-clank/data/clank.db`
open. Both dashboard and scheduled collectors resolve the same absolute DB
path. Both observe Alembic `0008_analyst_action_integrity`. Representative
shared counts: 270 devices, 350 collector_runs. This proves the `b935d1d`
same-state-path repair materially holds at the live target.

## Natural collection proof

The authoritative natural collection fire at 2026-09-04 21:46:34 UTC executed
`samsung_us_support_sitemap` on `e514c45` with provenance `production_scheduled`.
Result: success = 1, discoveries = 0, new_devices = 0. Durable run ID:
`2c9b9ede-cefb-429c-a53b-c2ca4bddc460`. No false novelty. No fresh-DB reset.
No duplicate discovery spike. No scope change. No source-health regression.

An earlier post-deploy fire at 20:18:43 UTC ran `google_store_category_phones`
but produced no durable run row (no sources were due). Classified honestly as
`NATURAL_EXECUTION_NO_MATERIAL_COLLECTION` — it proves timer wiring and
canonical code execution but is not the authoritative collection proof.

## Lock and exclusivity

`runtime.locks.FileLock` remains the canonical authority. Lock path:
`data/clank.db.lock`. No active lock at inspection (released after the
natural run). No kernel-level tracing claimed.

## Post-run DB integrity

Alembic `0008_analyst_action_integrity`, quick_check ok, canonical index
present, `analyst_actions` rows 0 → 0, devices 270, collector_runs 349 → 350
(natural increment), existing data preserved. Dashboard HTTP 200. Timers
enabled + active. No rollback.

## Family result

`FIRST_VALIDATED_MEMBER_OF_SYSTEMD_SOURCE_TIMER_COMPATIBILITY` is descriptive
process evidence naming exactly one member: Smartphone
`e514c45dca4cf966441c27799d98761096dc8c40`. This is not a new standard and is
not merged with existing families. All other Clanks inherit nothing.

## Deployment COM-001 verdict

`STD-DEPLOY-COM-001` = **LIVE_PROOF_CONFIRMED / CLOSED** at
`e514c45dca4cf966441c27799d98761096dc8c40`, scope: this exact source SHA +
target + systemd source-specific timers + dashboard service. Remaining
DEPLOY-COM-001 targets: CTW, Semiconductor. OEM Radar, Watch, Smartwatch,
Feature Phone, Tablet, KTW are already confirmed.
