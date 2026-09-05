# Semiconductor Intelligence — M55 DEPLOY-COM-001 live-proof admission

```json
{"clank":"semiconductor-intelligence","date":"2026-09-05","findings":[{"standard":"STD-DEPLOY-COM-001","kind":"conformance","summary":"LIVE_PROOF_CONFIRMED at Semiconductor Intelligence 53cb3f1f5358ad28a2d92ebd78efeab9534ddfa1 on target Hetzner:/home/deploy/staging/semiconductor-intelligence (cron 40 * * * * → deploy_run.sh → Docker Compose one-shot semi-intel → semintel automation cycle under the OperationalScheduler DB job lease): pre-deploy live ece4b00 (4 commits BEHIND_CANON, DB self-consistent at a0b1c2d3e404) was backed up canonically (verified .sqlite3 + SHA manifest), canonical db upgrade was scratch-proved first (SCRATCH_TARGET_PROVEN_BEFORE_MUTATION; a0b1c2d3e404 → bf599f950d56 → c7d8e9f0a1b2; exactly +3 tables candidate_reviews/qualification_epochs/qualification_events + 3 nullable qualification columns on operational_job_runs; all pre-existing rows preserved; backup_records 1→0 recorded as COMPARISON_BASE_ARTIFACT, NOT_MIGRATION_DATA_LOSS) then applied live with identical results; pointer flipped ece4b00→53cb3f1 with deploy_run.sh and compose byte-unchanged; authoritative natural proof is durable scheduled run id=345 (12:40:03.8Z→12:42:06.6Z, SCHEDULED, SUCCESSFUL, fresh container 129eedf7cd50:1, lease token 23a4ac76…, PCI ID Repository 0 new/21,475 duplicates/0 errors — normal registry sweep) whose durable row carries qualification_provenance='scheduled', a column only canon-era code writes; continuity 344→345 exact, sources 1, Alembic held at canonical head (BARRIER_HELD); delivery OFF, dashboard NOT_DEPLOYED/NOT_APPLICABLE, no rollback, old image retained with the paired-rollback rule recorded; runtime --identity honestly reports source_revision='unknown' (repo exposes no OCI revision label) with identity proven through checkout SHA + image tag + byte-unchanged tracked wiring."}]}
```

This Standards-only M55 record admits `STD-DEPLOY-COM-001`
LIVE_PROOF_CONFIRMED / CLOSED at
`53cb3f1f5358ad28a2d92ebd78efeab9534ddfa1` for the exact target
`Hetzner:/home/deploy/staging/semiconductor-intelligence` with the exact
mechanism above. Scope is exact: no generalization to future SHAs, the
Windows GUI lane, other host directories, persistent dashboards, or other
database states. This is the ninth and final fleet DEPLOY-COM-001 closure
fact; all eight prior target admissions remain preserved, as does
Semiconductor's `STD-DEPLOY-COM-002` CONFORMS / CLOSED at `8085a1bb`
(M11) — preserved, not re-closed or re-scoped. `STD-OPS-COM-003` remains
UNKNOWN; `STD-UI-COM-006`, `STD-UI-COM-007`, and `STD-UI-COM-011` remain
unresolved for Semiconductor; no overall conformance is claimed.

## Pre-M54 live state

Pre-deploy live source `ece4b001c60dd156c2a05cb92cf0ea335e0532c6`
(image `semi-intel:ece4b00`), classified **BEHIND_CANON** — exactly 4
commits: `8a356a3` (human QC review), `688b71a` (qualification
reset-traceability), `8085a1b` (the COM-002 Alembic compatibility gate
itself), `53cb3f1` (dashboard timezone convention/documentation).
The old live DB was **self-consistent with ece4b00** (its own Alembic
head `a0b1c2d3e404`): 10,231,808 bytes, quick_check ok, 50 tables,
run frontier 344, 1 source — but **migration was required before current
canon could run safely** (canonical head `c7d8e9f0a1b2`; required chain
`a0b1c2d3e404 → bf599f950d56 → c7d8e9f0a1b2`).

## Historical test debt (preserved honestly)

Classification: **CURRENT_FAILURE_REPRODUCED_DEPLOYMENT_IRRELEVANT**.
The failing historical guard
(`tests/test_deploy_com_002_m11.py::test_runtime_health_does_not_bootstrap_missing_database`)
is a diagnostic-string assertion; the substantive property remains —
application readiness false against a missing DB, no missing-DB
bootstrap, fail-closed behaviour holds. The M53 recon suite run was
**not green** (896 passed, 12 failed, 1 skipped under system Python
3.14; under the project venv the migration/dashboard tests pass and the
one remaining failure is this string assertion). The full Semiconductor
source suite is NOT claimed green, the test is NOT repaired in
Standards, and this debt is source-test debt, not a COM-001 blocker.

## Quiet window / lease gate

M54 executed 12:12–12:20 UTC, between the 11:40 fire (run 344,
SUCCESSFUL, ended 11:42:10Z) and the 12:40 fire: 0 RUNNING operational
jobs, 0 active leases. Cron cadence `40 * * * *` unchanged. Canonical
exclusivity is the **OperationalScheduler DB-level job lease**
(`operational_job_leases`: owner_identity + UUID lock_token +
expiry/stale-abandon) — not host flock.

## Verified backup

`semi-intel-backup-20260905T121316.967010Z.sqlite3` via the canonical
`docker compose run --rm semi-intel backup`: 10,231,808 bytes, SHA-256
`e5f2ac6f49e020b87e9e70b34d0847273771f932a29c4adc2d34151a27be2944`
(tool-reported and independently re-hashed), quick_check ok, Alembic
`a0b1c2d3e404`, 344 runs. Manifest generated:
`semi-intel-backup-20260905T121316.967010Z.manifest.json` (507 bytes).

## Source / dependency preparation

Fast-forward `ece4b00 → 53cb3f1` confirmed (merge-base check).
Dependency diff over pyproject.toml + requirements.container.lock +
uv.lock: **0 lines**. Canonical image built from a detached temp
worktree (live clone unmoved until pointer time): image
`semi-intel:53cb3f1f5358ad28a2d92ebd78efeab9534ddfa1`, id `e3d65d657eeb`,
built 2026-09-05T12:14:23Z.

## Identity limitation (recorded honestly)

Semiconductor exposes **no** OCI revision label and `--identity` reports
`source_revision = "unknown"`. That output is recorded exactly as-is.
Canonical deployment identity was instead proven through: the exact host
checkout SHA (`53cb3f1…`), the exact canonical image tag, byte-unchanged
tracked `deploy_run.sh` (sha256
`385d7c4424fac0f0048181ed2d36544d4a208d438cae4469cac3b60714a082a2`) and
compose (`8b6e62d608ad24cce37cf1a6594f7d2def92a3bf9fe86250966b6a6f49e080c9`),
and canon-era durable runtime behaviour below. "unknown" was not
converted into a revision claim.

## Scratch targeting + migration + acceptance

Scratch copied from the verified backup (SHA identical), inspected
through the canonical container (mount marker `m54-scratch-mount-marker`
read inside; pre-state `a0b1c2d3e404`), live DB excluded:
**SCRATCH_TARGET_PROVEN_BEFORE_MUTATION**. Canonical `db upgrade` on
scratch: "Upgraded to head.", exit 0, chain
`a0b1c2d3e404 → bf599f950d56 → c7d8e9f0a1b2`. Material effects,
verified in the migrated scratch: **+3 tables** (`candidate_reviews` —
11 columns incl. disposition enum USEFUL/NOT_USEFUL/FALSE_POSITIVE/
DUPLICATE, FK → signal_candidates, unique candidate_id, 3 indexes;
`qualification_epochs` — uq job_type+material_identity; 
`qualification_events`) and **+3 nullable columns on
`operational_job_runs`** (`qualification_provenance`,
`qualification_material_identity`, `qualification_epoch_id`) + 3
indexes + 1 FK. No existing-row transformation, no destructive schema
action, all pre-existing data preserved.

The one apparent anomaly is preserved explicitly:
`backup_records` **1 → 0** was **COMPARISON_BASE_ARTIFACT,
NOT_MIGRATION_DATA_LOSS** — the live DB inserted the backup-record row
after the backup file itself had already been written, so the scratch
(copy of that file) naturally lacked the later row. Verified directly
against the backup file (0 rows) and live (1 row).

Scratch acceptance: Alembic `c7d8e9f0a1b2`, quick_check ok, expected +3
tables and nullable columns present, all relevant pre-existing rows
preserved, health healthy, readiness true, no implicit collection.
Scratch migration: **QUALIFIED**.

## Live migration + pointer + health

Live `db upgrade` executed only after the scratch proof passed; result
**matched scratch exactly** (same chain, quick_check ok, schema delta
identical, pre-existing state preserved). Pointer transition
`ece4b00 → 53cb3f1f5358ad28a2d92ebd78efeab9534ddfa1` (`.deployed-id`),
canonical image `semi-intel:53cb3f1…`, tracked `deploy_run.sh` and
compose byte-identical to the pre-deploy freeze. Live health after
migration + canonical source: healthy, readiness true, no fail-closed
refusal, no bootstrap, Alembic current.

## Authoritative natural proof

Run **id=345**: the 12:40:01Z cron fire → job_type PIPELINE,
trigger_type **SCHEDULED**, status **SUCCESSFUL**,
2026-09-05T12:40:03.801568Z → 12:42:06.589977Z, attempt 1, fresh
container `129eedf7cd50:1`, lease lock_token
`23a4ac76f6c149f99e2b22da779b1645`. Registry result: 0 new, 21,475
duplicates, 0 errors — established full-registry sweep behaviour, not a
failure.

**Canon-era durable provenance**: run 345's durable row contains
`qualification_provenance = 'scheduled'` — a field introduced by the
current canonical migration/code path. This is strong runtime
corroboration that the natural scheduled run executed the canonical-era
application against the canonical-era schema; it is used together with
the checkout + image identity, not alone as a source-SHA proof.

## Continuity / barrier / rollback

operational job runs 344 → 345, no history break, no identity reset,
source count unchanged (1), no duplicate explosion, no false novelty,
no lease regression, no failed transition. Alembic remained at
canonical head `c7d8e9f0a1b2` after normal canonical operation —
**BARRIER_HELD** (no hidden bootstrap or downgrade). Rollback was NOT
triggered. The paired rollback invariant is preserved: after the DB
upgrade to `c7d8e9f0a1b2`, old `ece4b00` code is incompatible with the
newer state, so any rollback must pair old source `ece4b00` + old image
`semi-intel:ece4b00` (retained) + restore of the pre-M54 backup at
`a0b1c2d3e404` — never one component alone.

## Fleet closure

This is the ninth DEPLOY-COM-001 closure fact: Watch (M15-era
admission), KTW (M22), Tablet (M28), Feature Phone (M25), OEM Radar
(M46), Smartwatch (M22-era), Smartphone (M49), Chinese Tech Wire (M52),
and now Semiconductor Intelligence (M55). Every prior admission is
preserved verbatim; nothing was re-closed, re-scoped, or generalized.
No Hetzner access, deploy, migration, cron/service restart, or
Semiconductor source modification occurred in this Standards-only
recording pass. Frozen standard files and immutable tags unchanged.
