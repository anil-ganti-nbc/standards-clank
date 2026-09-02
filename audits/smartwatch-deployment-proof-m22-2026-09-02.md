# Smartwatch Clank DEPLOY-COM-001 live-proof admission — 2026-09-02

```json
{"clank":"smartwatch-clank","date":"2026-09-02","findings":[{"standard":"STD-DEPLOY-COM-001","kind":"conformance","summary":"LIVE_PROOF_CONFIRMED at Smartwatch a93355480bb11e1bd16ae7837256ce9002fc2aa7 on target hetzner/ubuntu-4gb-hel1-1:cron-docker-compose-staging: intended SHA = host source HEAD = OCI revision = runtime/run git_revision, deployed image smartwatch-clank:a933554 (sha256:8fdace0a3847c346aa4bd989f7429be7de2cacb45d71af853017770bacab83b5), canonical v2-to-v3 migration to COMPATIBLE (integrity ok), production cron 50 1-23/2 * * * through a host wrapper now content-identical to tracked deploy/deploy_run.sh, first natural post-deploy tick exposed and preserved a MATERIAL_WIRING_DRIFT (03:50Z MANUAL provenance), and after the one-line host-only wrapper correction the second natural tick (2026-09-02T05:50:02Z, cycle 61d54662fbf344fca9888df3f5f870a3, runs 1583-1595) delivered 13/13 healthy production runs with durable SCHEDULED provenance, full canonical git_revision, schema_version_at_run 3, and config_fingerprint f24e97c47e741913."}]}
```

## Scope and mode

This is a **Standards-only recording/admission pass** (M22). The live-proof
actions were executed in the separately authorized M21/M21b/M21c passes; this
pass made **no host access, no deployment/restart, no cron change, no wrapper
change, no database change, and no collector execution**. It records and
admits the completed proof for `STD-DEPLOY-COM-001` at Smartwatch
`a93355480bb11e1bd16ae7837256ce9002fc2aa7`, target
`hetzner/ubuntu-4gb-hel1-1:cron-docker-compose-staging`, scope: this exact
source SHA + target + deployment mechanism + evidence package. It does not
generalize to another target or future revision, and it does not close
`STD-UI-COM-011`.

## Lineage

Standards takeover was `8cea2e5f4d95a40be5119bc0f1da2612bc83f11f`
(origin/master, clean); Smartwatch canonical remote remained
`a93355480bb11e1bd16ae7837256ce9002fc2aa7` (origin/main, clean; unchanged
since the M18 COM-002 closure). The M18 source-level COM-002 record
(`audits/smartwatch-persistent-state-remediation-m18-2026-09-02.md`) and the
M5 OPS-COM-003 closure remain preserved.

## Initial live state — stale selector, honestly classified

The initial deployed selector was `smartwatch-clank:08a23f9` while the
canonical intended source was `a9335548`: a **stale deployment**. The old
image's content was consistent with its `08a23f9` selector, so this was
recorded as **STALE_CONTENT_CONSISTENT** — NOT a proven mislabel or
provenance lie. It was still a material mismatch: the intended deployment had
never materialized, and closure was refused until convergence.

## Canonical deployment and the identity chain

The canonical deployment then established the authoritative four-way chain:

```text
intended source SHA = host source HEAD = OCI revision = runtime/run git_revision
                    = a93355480bb11e1bd16ae7837256ce9002fc2aa7
```

Deployed artifact: `smartwatch-clank:a933554`; image ID recorded separately:
`sha256:8fdace0a3847c346aa4bd989f7429be7de2cacb45d71af853017770bacab83b5`.
The `.deployed-id` selector alone is not treated as artifact proof; the OCI
label and the runtime/run revision corroborate it. The database migrated
canonically v2 → v3 through the M18 compatibility barrier
(`MIGRATION_REQUIRED` → canonical additive `_migrate()`), reaching
**schema 3 / expected 3 / COMPATIBLE** with `integrity_check = ok`.

## The material-wiring defect — first natural tick

The first natural post-deploy production tick at **03:50Z** exposed
**MATERIAL_WIRING_DRIFT**: the host wrapper omitted `--trigger SCHEDULED`, so
the durable runs and qualification terminal evidence recorded
**execution_provenance = MANUAL**. This blocked `DEPLOY-COM-001`: a correct
artifact with incorrect scheduler wiring is not the intended deployment
state. The historical 03:50 MANUAL evidence was **deliberately preserved** —
not rewritten or deleted.

## Host-only wrapper remediation

The remediation changed **exactly one exec line** on the host wrapper to
match the tracked deployment semantics:

- no crontab change, no image rebuild, no source commit, no Standards change;
- the corrected host wrapper is **content-identical** to tracked
  `deploy/deploy_run.sh`, whose final line is
  `exec docker compose -f docker-compose.staging.yml run --rm smartwatch-clank run --mode production --trigger SCHEDULED` —
  verified against the tracked canonical source during this pass;
- the production scheduler `50 1-23/2 * * *` executing
  `/home/deploy/staging/smartwatch-clank/deploy_run.sh` matches the tracked
  wrapper's documented cron contract.

## Second natural tick — the closing evidence

The second natural production tick at **2026-09-02T05:50:02Z** (cycle
`61d54662fbf344fca9888df3f5f870a3`, runs **1583–1595**) proved:

- 13 attempted / **13 healthy** / 0 failed (the tracked
  `production_allowlist` contains exactly these 13 finalized collectors —
  verified against `config/config.yaml`);
- durable `execution_provenance = SCHEDULED` for all 13 new runs;
- run `git_revision` = full canonical `a9335548…` for all 13;
- `schema_version_at_run = 3`;
- `config_fingerprint = f24e97c47e741913`.

No migration occurred during the M21c proof observation (state was already
COMPATIBLE from the canonical deployment).

## Qualification provenance behavior

The 03:50 MANUAL epoch openings remain valid, untouched history. At 05:50:
same material identity → **no epoch reset**; **13 new TERMINAL events
appended** with provenance SCHEDULED / HEALTHY. The epoch itself was **not**
recreated as SCHEDULED; the latest durable terminal evidence now correctly
represents the scheduled execution path. This matches the tracked
qualification semantics (`SCHEDULED` is asserted only by tracked scheduler
launchers / the `--trigger SCHEDULED` argument).

## One-shot running model

Smartwatch production is cron + docker compose **one-shot** execution (the
staging compose service is `restart: "no"`, one-shot by design; no permanent
container exists between ticks). COM-001 running/operational proof is
therefore established by scheduler wiring + selected artifact + natural
one-shot execution + durable run identity/results + compatible state. No
resident service is required or claimed.

## Experimental Garmin — orthogonal

`garmin_catalogue` and `garmin_official_news` remain unhealthy in soak. They
are experimental-tier, were **not** in the production allowlist tick, and are
orthogonal to this proof. The production tick was 13/13 healthy. Aggregate
experimental health must not be read as obscuring or qualifying the
production deployment proof, and experimental Garmin is **not** claimed
healthy.

## Verdict

`STD-DEPLOY-COM-001` = **LIVE_PROOF_CONFIRMED / CLOSED** at Smartwatch
`a93355480bb11e1bd16ae7837256ce9002fc2aa7`, target
`hetzner/ubuntu-4gb-hel1-1:cron-docker-compose-staging`, matching the
repository's canonical verdict vocabulary. Closure depends on the **corrected
live wiring evidence** (the 05:50Z SCHEDULED tick), not merely on the artifact
revision. Scope: this exact SHA + target + mechanism + evidence package.

## Remaining Smartwatch state

Preserved closed: `STD-OPS-COM-003` (M5), `STD-DEPLOY-COM-002` (M18). Now
closed: `STD-DEPLOY-COM-001` (this pass). Remaining: **STD-UI-COM-011** only.
Smartwatch is not called fully conforming by this record.

## Non-inheritance and index

Exactly one new Deployment fact is admitted (Smartwatch +
`a93355480bb11e1bd16ae7837256ce9002fc2aa7` + `STD-DEPLOY-COM-001` +
`hetzner/ubuntu-4gb-hel1-1:cron-docker-compose-staging` +
LIVE_PROOF_CONFIRMED/CLOSED), bringing the Deployment known-evidence index to
9 facts. The Smartwatch COM-002 fact, the Watch COM-001 fact, and all other
admissions are preserved. No target inherits this proof; no other target or
future revision is covered.

## No-action declaration

This Standards-only recording pass made no host access and no host mutation:
no deploy, no restart, no cron change, no wrapper change, no database change,
no collector execution, no live proof. Frozen Deployment standard files and
immutable tags were not changed or moved. Smartwatch was not modified.
