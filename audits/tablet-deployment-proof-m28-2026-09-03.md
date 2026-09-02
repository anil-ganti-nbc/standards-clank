# Tablet Clank DEPLOY-COM-001 live-proof admission — 2026-09-03

```json
{"clank":"tablet-clank","date":"2026-09-03","findings":[{"standard":"STD-DEPLOY-COM-001","kind":"conformance","summary":"LIVE_PROOF_CONFIRMED at Tablet b3088ebc716227b99e1d8aa66942c8a6e87bbfcb on target hetzner/ubuntu-4gb-hel1-1:systemd-timer-experimental-dir: the M27 canonical deployment replaced the stale but honestly-labelled 2bd8929/v1 deployment (STALE_CONTENT_CONSISTENT, 10 commits behind, 3-source pre-Wave-3 scope, not a provenance lie) via a canonical-checkout -> rebuilt editable venv -> exact systemd interpreter identity chain, migrated the live database v1 -> v3 through the M13 barrier to COMPATIBLE with integrity OK (pre-deploy backup sha256 e3a5c1972925ad5a44889cb2117f507d69060905c06ab6a0ed9915a94381634b, 11071488 bytes), closed the live DEP-INC-009 allowlist drift (PRODUCTION_ALLOWLIST_DRIFT_CLOSED: all four canonical sources executed naturally, honor_uk_tablets run 162 SUCCESS with 25 accepted / 2 new), and the naturally timer-fired 2026-09-02T18:20:54Z oneshot cycle (service 18:20:54-18:20:59 UTC, exit 0, PID 1557855) recorded durable SCHEDULED provenance for runs 160-163 on the canonical SoakLock OS advisory lock path. No immutable OCI-style artifact identity exists on this venv lane and TABLET_CLANK_SOURCE_REVISION is unused on it; tracked examples still describe a /opt/tablet-clank path that differs from live (TRACKED_DEPLOYMENT_PATH_DESCRIPTION_STALE, classified NON_MATERIAL_PATH_VARIANCE)."}]}
```

## Scope and mode

This is a **Standards-only recording/admission pass** (M28, recorded
2026-09-03). Standards takeover was
`9f784326b4ec5bfd4327fc4c162d0165f6d73ee7` (origin/master, clean); Tablet
canonical remote remained `b3088ebc716227b99e1d8aa66942c8a6e87bbfcb`
(origin/main, clean; unchanged since the M13 COM-002 closure). The live-proof actions were executed in the separately
authorized M26 (read-only recon, 2026-09-02) and M27 (bounded deploy + proof,
2026-09-02 operational session) passes; this pass made **no host access, no
deployment/restart, no systemd unit/timer change, no database change, no
collector execution, and no Tablet source or docs modification**. It records
and admits `STD-DEPLOY-COM-001` at Tablet
`b3088ebc716227b99e1d8aa66942c8a6e87bbfcb`, target
`hetzner/ubuntu-4gb-hel1-1:systemd-timer-experimental-dir`, scope: this exact
source SHA + target + the actual systemd-timer/oneshot-venv mechanism + the
M26/M27 evidence package. It does not generalize to another target, another
mechanism, or future revisions.

## Pre-M27 stale deployment history — preserved exactly (M26 recon)

- Pre-M27 live source: `2bd8929459cb44ac840dc0cabcfb7ed91383cf45` — **10
  commits behind** canonical `b3088ebc…`.
- Live database at **schema v1** (159 historical runs), **no qualification
  tables, no provenance column** — the code/state pair was **internally
  coherent**.
- Live production scope was **3 sources**; `honor_uk_tablets` was absent —
  the host ran an earlier allowlist than the repository (the DEP-INC-009
  incident class).
- The deployment predated the OPS-COM-003, OPS-COM-004, and M13 COM-002
  remediations.
- Classification: **STALE_CONTENT_CONSISTENT**. The old deployment is **not**
  described as mislabelled — the defect was staleness, not lying provenance.

## Identity model — recorded honestly

Tablet's production lane does **not** use an OCI/container identity chain.
The actual identity argument is:

```text
canonical Git checkout SHA b3088ebc716227b99e1d8aa66942c8a6e87bbfcb
  -> production venv rebuilt from that checkout (editable installation)
  -> exact systemd interpreter (.venv/bin/python -m tablet_clank.cli production)
  -> imported tablet_clank modules resolve under
     /home/deploy/experimental/tablet-clank
  -> natural production execution
```

**No immutable artifact identity equivalent to an OCI digest is claimed.**
`TABLET_CLANK_SOURCE_REVISION` was **unused** on this path in M26 and was
deliberately **not added** in M27 — this limitation is recorded, not papered
over. The proof rests on checkout state + editable-install import resolution,
which M27 verified via `tablet_clank.__file__` and module-path probes.

## Canonical content probes

The executing checkout at `b3088ebc…` was probed as materially containing:
schema version **v3**; the **M13 fail-closed compatibility barrier**; the
**OPS-COM-003** qualification/provenance machinery; the **OPS-COM-004**
grant-backed advisory lock; **production allowlist = exactly 4** (including
`honor_uk_tablets`); the canonical production CLI path. These bind the
executing checkout to the intended remediation state.

## Persistent state

- Pre-deploy: schema **v1**, 159 historical runs, no qualification tables,
  no provenance column.
- Backup: `var/backups/m27-pre-deploy-2bd8929-schema-v1.sqlite`, sha256
  `e3a5c1972925ad5a44889cb2117f507d69060905c06ab6a0ed9915a94381634b`,
  11,071,488 bytes.
- Canonical classification of the v1 state: **MIGRATION_REQUIRED**.
- Canonical migration: **v1 → v3** using `Database()`; post-state schema
  migrations `(1, 2, 3)`, **COMPATIBLE**, integrity **OK**; historical data
  preserved; old v1 rows left **UNKNOWN** and not rewritten.
- This admission does **not** re-ratify `STD-DEPLOY-COM-002`; the M13
  source-level closure remains a separate fact, preserved.

## Systemd deployment mechanism (actual)

- `tablet-clank-production.service` (Type=oneshot) +
  `tablet-clank-production.timer` (enabled).
- OnCalendar: **06:20 UTC** and **18:20 UTC**, `RandomizedDelaySec=90`.
- Actual ExecStart: `/home/deploy/experimental/tablet-clank/.venv/bin/python
  -m tablet_clank.cli production --db
  /home/deploy/experimental/tablet-clank/var/tablet_clank.db`;
  WorkingDirectory `/home/deploy/experimental/tablet-clank`.
- No resident process is required or claimed: operational proof for this
  mechanism is the **naturally timer-fired oneshot cycle**.

## Tracked-vs-live path debt — left open

**TRACKED_DEPLOYMENT_PATH_DESCRIPTION_STALE**: tracked examples use
`/opt/tablet-clank`; live production uses
`/home/deploy/experimental/tablet-clank`. M27 classified this
**NON_MATERIAL_PATH_VARIANCE** because the actual unit points at the exact
canonical checkout and venv. Nothing was modified in this pass. The admission
does **not** bless arbitrary paths, does **not** prove the examples current,
and does **not** generalize to future revisions/targets.

## OPS-COM-004 live path

`STD-OPS-COM-004` remains a separate source-level closure (preserved, not
re-admitted). The deployment-relevant chain recorded here:
systemd ExecStart → canonical Tablet production CLI → **SoakLock** → OS
advisory lock acquisition. M27 evidence: natural service **PID 1557855**,
`lock_authority = os_advisory_lock`; post-run lock inspect: **stale**
(diagnostic only). PID remains diagnostic; **no kernel tracing is claimed**.

## Natural timer proof — the closing evidence

**2026-09-02 18:20:54 UTC** (naturally timer-fired, not a manual test run):
service start 18:20:54 → finish 18:20:59, **exit 0**, result **success**,
**PID 1557855**, runs **160–163**.

## Durable provenance

Runs **160–163**: all recorded **SCHEDULED** in the durable database — the
application record is the authority; provenance is not inferred from systemd.
Historical v1-era rows remain **UNKNOWN** and were not rewritten.

## DEP-INC-009 scope-drift closure

M26 live scope: 3 sources. Canonical intended scope: **4**. The M27 natural
production cycle executed **all four** canonical sources:
`honor_cn_tablets_catalogue`, `honor_cn_tablets_comparison`,
`tcl_global_tablets`, `honor_uk_tablets`.
**PRODUCTION_ALLOWLIST_DRIFT_CLOSED.** Honor UK evidence: **run 162,
SUCCESS, 25 accepted, 2 new**. Closure rests on the live natural execution,
not merely on the source containing the allowlist entry.

## Qualification evidence

Four new canonical production scopes/epochs/terminals were created with
provenance SCHEDULED; the first canonical scheduled epochs resulted in the
expected **NOT_QUALIFIED** state where applicable; historical v1 evidence was
not rewritten. The relevant COM-001 fact is that canonical scheduled
qualification machinery **materially executed** on the live deployment —
qualification *status* is not overstated here.

## Operational result

Cycle result **SUCCESS**; DB **v3 / COMPATIBLE**, integrity **OK**; timer
still enabled; checkout still exactly `b3088ebc…`; all four production
sources executed; no rollback observed. No permanent process residency is
required for this mechanism.

## Verdict

`STD-DEPLOY-COM-001` = **LIVE_PROOF_CONFIRMED / CLOSED** at Tablet
`b3088ebc716227b99e1d8aa66942c8a6e87bbfcb`, target
`hetzner/ubuntu-4gb-hel1-1:systemd-timer-experimental-dir`, matching the
canonical Standards verdict vocabulary. Scope: this exact SHA + target +
systemd-timer/oneshot-venv mechanism + the M26/M27 evidence package. This
does **not** imply: all Tablet deployments conform, future SHAs conform,
`/opt` examples are correct, immutable artifact identity exists,
`TABLET_CLANK_SOURCE_REVISION` is meaningful on this lane, `STD-UI-COM-011`
is closed, or Tablet is fully conforming.

## Remaining Tablet findings

Preserved closed: `STD-OPS-COM-003`, `STD-OPS-COM-004`,
`STD-DEPLOY-COM-002` (M13). Now closed: `STD-DEPLOY-COM-001` (this pass).
Remaining: **STD-UI-COM-011**. Tablet is not called fully conforming by this
record.

## Non-inheritance and index

Exactly one new Deployment fact is admitted (Tablet +
`b3088ebc716227b99e1d8aa66942c8a6e87bbfcb` + `STD-DEPLOY-COM-001` +
`hetzner/ubuntu-4gb-hel1-1:systemd-timer-experimental-dir` +
LIVE_PROOF_CONFIRMED/CLOSED), bringing the Deployment known-evidence index to
**11 facts**. The Tablet COM-002 fact, the Watch/Smartwatch/Feature Phone
COM-001 facts, and all other admissions are preserved. No target inherits
this proof.

## No-action declaration

This Standards-only recording pass made no host access and no host mutation:
no deploy, no restart, no systemd unit/timer change, no database change, no
collector execution. No Tablet source or docs file was modified. Frozen
Deployment standard files and immutable tags were not changed or moved.
