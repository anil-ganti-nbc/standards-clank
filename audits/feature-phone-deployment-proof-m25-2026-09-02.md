# Feature Phone Clank DEPLOY-COM-001 live-proof admission — 2026-09-02

```json
{"clank":"feature-phone-clank","date":"2026-09-02","findings":[{"standard":"STD-DEPLOY-COM-001","kind":"conformance","summary":"LIVE_PROOF_CONFIRMED at Feature Phone b60e881319b16d36625268d9ba2d66cb8ea8f818 on target hetzner/ubuntu-4gb-hel1-1:cron-docker-compose-staging: the M24 canonical deployment replaced the stale but honestly-labelled 303e42ff v4 deployment (STALE_CONTENT_CONSISTENT, not a provenance lie) with the exact canonical source, migrated the live database v4 -> v5 through the M14 compatibility barrier to COMPATIBLE with integrity OK, and the natural 13:15Z production cron fire ran all six tracked production collectors with durable execution_provenance SCHEDULED on the canonical grant-backed OS advisory lock path. Operational debt is explicitly preserved: the tracked README still describes the dead Windows Task Scheduler lane as production, and the actual host production wrapper remains untracked (TRACKED_DEPLOYMENT_DESCRIPTION_STALE)."}]}
```

## Scope and mode

This is a **Standards-only recording/admission pass** (M25). Standards
takeover was `760b2949acd0a6c742ca91e370d99647d4a8c200` (origin/master,
clean); Feature Phone canonical remote remained
`b60e881319b16d36625268d9ba2d66cb8ea8f818` (origin/main, clean; unchanged
since the M14 COM-002 closure). The live-proof
actions were executed in the separately authorized M23 (read-only recon) and
M24 (bounded deploy + proof) passes; this pass made **no host access, no
deployment/restart, no cron/wrapper change, no database change, no collector
execution, and no Feature Phone source or docs modification**. It records and
admits `STD-DEPLOY-COM-001` at Feature Phone
`b60e881319b16d36625268d9ba2d66cb8ea8f818`, target
`hetzner/ubuntu-4gb-hel1-1:cron-docker-compose-staging`, scope: this exact
source SHA + target + the actual Hetzner cron/Docker-Compose mechanism + the
M23/M24 evidence package. It does not generalize to another target, another
mechanism, or future revisions.

## Pre-M24 defect history — preserved exactly (M23 recon)

- Tracked `scripts/README.md` described **Windows Task Scheduler** production
  ("FeaturePhoneClank HMD Soak", 4× daily IST) as the production mechanism.
- The Windows task was **disabled**, and its target checkout
  (`C:\Users\anil\Desktop\feature phone clank`) was **absent**.
- The **actual** production was Hetzner cron (`15 1,7,13,17 * * *`) + Docker
  Compose one-shot through a **host-local untracked** `deploy_run.sh`.
- The live selector/image revision was `303e42ff56c6929e603a85316023c16de039e6f9`
  — a **stale but honestly-labelled, content-consistent** deployment: OCI
  revision label and `FEATURE_PHONE_CLANK_SOURCE_REVISION` matched the
  selector, and the running v4 code matched the v4 volume database. This is
  **not** described as mislabelled — the defect was staleness, not lying
  provenance.
- The live v4 code/state pair predated three remediation waves: the
  OPS-COM-003 qualification remediation, the OPS-COM-004 grant-backed run
  lock, and the M14 COM-002 fail-closed compatibility barrier.

## Canonical deployment evidence (M24)

- Deployed source: `b60e881319b16d36625268d9ba2d66cb8ea8f818` (canonical
  `origin/main`, verified unchanged during this pass).
- Target: `hetzner/ubuntu-4gb-hel1-1:cron-docker-compose-staging`.
- The canonical artifact identity chain (image ID/digest, OCI revision,
  baked source revision, runtime/durable revision evidence, and the
  content probes distinguishing the canonical build from any stale image)
  was captured in the M24 evidence package and is admitted by reference;
  the deployment followed the Watch/Smartwatch remediation pattern
  (build with the `GIT_REVISION` build-arg, verify identity **and content**,
  never trust a tag alone).
- Actual cron command: `15 1,7,13,17 * * *`
  `/home/deploy/staging/feature-phone-clank/deploy_run.sh`; actual host
  wrapper semantics: `.deployed-id` → `IMAGE_TAG` →
  `docker compose -f docker-compose.staging.yml run --rm feature-phone-clank`
  (one-shot; no resident container).
- Production scope: **exactly six** collectors — `hmd-nokia`, `punkt-ch`,
  `doro-gb`, `mudita-com`, `sunbeam-f1-us`, `tcl-alcatel-global` — verified
  against the tracked `config/scope.yaml` `production_collectors` during
  this pass. Experimental/soak sources are outside production success.

## Persistent state

- Pre-deploy: coherent **v4** code/state pair (honestly stale).
- Canonical source classification of that state: **MIGRATION_REQUIRED**
  (v4 < expected v5 under the M14 barrier).
- Canonical migration: **v4 → v5** through the M14 read-only-first
  compatibility barrier and canonical bootstrap/migration path.
- Post: **schema v5 / COMPATIBLE, integrity OK**.
- The natural 13:15Z run recorded its schema/version evidence in the M24
  package against the v5 store.
- This admission does **not** re-ratify `STD-DEPLOY-COM-002`; the M14
  source-level closure remains a separate fact, preserved.

## OPS-COM-004 live path

Source-level `STD-OPS-COM-004` was closed separately (grant-backed OS
advisory lock; PID and marker metadata diagnostic only) and is **not**
re-admitted here. The deployment-relevant COM-001 fact is narrow: the actual
production execution path used the **canonical grant-backed OS advisory lock
path** (`core/run_lock.py`, `fcntl.flock`, `lock_authority: os_advisory_lock`)
during the M24 natural run. PID metadata is not treated as authority.

## Scheduler / provenance proof

The natural **13:15Z** production cron fire (M24) is the closing evidence:

- natural cron execution (not operator-triggered);
- the scheduler selected the canonical artifact;
- full durable source revision `b60e8813…` in the application's durable
  records;
- **`execution_provenance = SCHEDULED`** recorded durably by the application
  itself — not inferred from crontab presence;
- all production collectors succeeded.

Run/cycle identifiers and the full per-run durable records are preserved in
the M24 evidence package admitted by reference.

## Deployment-mechanism gap — explicitly left open

**TRACKED_DEPLOYMENT_DESCRIPTION_STALE** remains operational debt:

- tracked `scripts/README.md` still describes the Windows Task Scheduler
  lane as production;
- the Windows task remains disabled and its target checkout remains absent;
- the actual host production wrapper remains **untracked**.

Nothing was fixed in this pass and no Feature Phone source or docs file was
modified. This COM-001 admission closes **only** because the actual target,
mechanism, and wiring were independently evidenced live on the canonical
revision. It explicitly does **not**: bless the documented Windows
deployment, bless arbitrary host wrappers, generalize to future revisions,
or mean that Feature Phone's deployment documentation is correct.

## Verdict

`STD-DEPLOY-COM-001` = **LIVE_PROOF_CONFIRMED / CLOSED** at Feature Phone
`b60e881319b16d36625268d9ba2d66cb8ea8f818`, target
`hetzner/ubuntu-4gb-hel1-1:cron-docker-compose-staging`, matching the
canonical Standards verdict vocabulary. Scope: this exact SHA + target +
actual Hetzner cron/docker-compose mechanism + M23/M24 evidence package.

## Remaining Feature Phone findings

Preserved closed: `STD-OPS-COM-003`, `STD-OPS-COM-004`,
`STD-DEPLOY-COM-002` (M14). Now closed: `STD-DEPLOY-COM-001` (this pass).
Remaining: **STD-UI-COM-011**. Feature Phone is not called fully conforming
by this record, and the deployment-description debt above remains open.

## Non-inheritance and index

Exactly one new Deployment fact is admitted (Feature Phone +
`b60e881319b16d36625268d9ba2d66cb8ea8f818` + `STD-DEPLOY-COM-001` +
`hetzner/ubuntu-4gb-hel1-1:cron-docker-compose-staging` +
LIVE_PROOF_CONFIRMED/CLOSED), bringing the Deployment known-evidence index
to **10 facts**. The Feature Phone COM-002 fact, the Smartwatch COM-001 and
COM-002 facts, the Watch COM-001 fact, and all other admissions are
preserved. No target inherits this proof.

## No-action declaration

This Standards-only recording pass made no host access and no host mutation:
no deploy, no restart, no cron change, no wrapper change, no database change,
no collector execution. No Feature Phone source or docs file was modified.
Frozen Deployment standard files and immutable tags were not changed or
moved.
