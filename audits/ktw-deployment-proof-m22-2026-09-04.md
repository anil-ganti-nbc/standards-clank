# Korean Tech Wire DEPLOY-COM-001 live-proof admission — 2026-09-04

```json
{"clank":"korean-tech-wire","date":"2026-09-04","findings":[{"standard":"STD-DEPLOY-COM-001","kind":"conformance","summary":"LIVE_PROOF_CONFIRMED at Korean Tech Wire f49bd02eb214b650a146e9c0f6f348d526285a91 on target hetzner/ubuntu-4gb-hel1-1:systemd-venv-soak: intended SHA = host checkout = venv import path (systemd unit → WorkingDirectory /opt/korean-tech-wire → .venv/bin/python → src/korean_tech_wire/__init__.py), canonical additive migration DB marker 4→5 through the already-closed M12 numbered compatibility machinery (quick_check ok, 12 tables, 917 historical articles preserved, qualification tables created), first natural post-deploy timer fire at 22:14:45Z was a due-check-only cycle (no sources due, no run rows — correctly classified as NATURAL_DUE_CHECK_ONLY), and the second natural fire (trigger 23:14:27Z, execution 23:15:48–23:17:21Z, exit 0/SUCCESS) ran the canonical production scope (the_elec, lg_display_newsroom, etnews_hardware — all success) with every durable run row recording provenance SCHEDULED, six qualification epochs/terminals created with INITIAL_MATERIAL_IDENTITY and counts_for_qualification=1, gate honestly NOT_QUALIFIED (epoch 1 just started — qualification maturity is orthogonal to deployment proof), articles advancing 917→920 naturally, and the canonical lock path var/korean_tech_wire.db.lock mtime-correlated with the run."}]}
```

## Scope and mode

This is a **Standards-only recording/admission pass** (M22-KTW). Standards takeover was `e379ea59abd472cc5d86899a8e7935ec21845d95`. The live-proof
actions were executed in the separately authorized M21-KTW bounded deploy pass;
this pass made **no host access, no deployment/restart, no database change, no
collector execution, and no source modification**. It records and admits the
completed proof for `STD-DEPLOY-COM-001` at Korean Tech Wire
`f49bd02eb214b650a146e9c0f6f348d526285a91`, target
`hetzner/ubuntu-4gb-hel1-1:systemd-venv-soak`, scope: this exact source SHA +
target + systemd/venv mechanism + evidence package.

## Pre-deploy state (preserved honestly)

The pre-M21 live checkout was at `afb4aada1d4fae09ada4658fe9fcf8dfa38eb23d`
(M1-era, detached HEAD, STALE_DEPLOYMENT — 3 commits behind canon). The M20
recon observed the database marker as 2; by the time the bounded deploy was
executed, the live database's own timer-driven machinery had naturally advanced
the marker to **4** (the stale deployment's compatibility code runs on every
timer fire). This correction is recorded as a later observation — the earlier
recon is preserved, not rewritten. Pre-deploy: 8 tables, 917 articles,
quick_check ok.

## Backup

Created using the repo's own fail-closed `state backup` command as the service
user: `/opt/korean-tech-wire/backups/kbw-pre-m21-f49bd02.db`,
11,120,640 bytes, sha256
`80dcb1927598d8d22a3cf1039e05f882f467ff9a9e3d3fa95dad123974bc0407`.
The backup size matched the live DB file exactly. A second backup attempt
refused overwrite (fail-closed), corroborating first-attempt creation.

## Deployment transport and runtime identity

The host clone could not fetch from GitHub directly (the service user's
historical SSH alias was unavailable). Deployment used a **credential-free
transfer method**: a git bundle created from the canonical workstation repo at
`f49bd02`, transferred to the host, fetched locally by the service user, and
checked out at the exact SHA. This is a transport detail, not a weakness in
runtime identity.

Runtime identity chain (proven for this non-container deployment):
systemd unit → WorkingDirectory `/opt/korean-tech-wire` → `.venv/bin/python` →
import path `/opt/korean-tech-wire/src/korean_tech_wire/__init__.py` →
checkout SHA `f49bd02` → `SCHEMA_VERSION 5`. No OCI identity is demanded for
this venv/systemd architecture.

## Persistent-state transition

Canonical startup performed the additive migration **4 → 5** through the
already-closed M12 numbered compatibility machinery. Post-migration: marker 5,
12 tables, quick_check ok, **all 917 pre-existing articles preserved**,
qualification tables created, compatibility = COMPATIBLE. The QC archive
remained absent at proof time; it will bootstrap to canonical v1 on first
QC/dashboard use. COM-002 is not re-ratified.

## Systemd / timer invariants

Timer: enabled + active, OnUnitActiveSec=30min, Persistent=true. Service:
oneshot, User=korean-tech-wire, WorkingDirectory=/opt/korean-tech-wire,
ExecStart=`.venv/bin/python -m korean_tech_wire.cli soak --cycles 1
--interval-seconds 7200 --if-due`. Cadence unchanged, no duplicate units, no
scheduler drift. EnvironmentFile `-`/etc/korean-tech-wire.env was absent
(optional per the `-` prefix) — the service ran without it.

## Lock authority

Canonical lock path `var/korean_tech_wire.db.lock` mtime 23:15:48Z,
correlated with the natural collection run (23:15:48–23:17:21Z). The chain is
systemd → CLI → canonical RunLock → collector execution. No kernel-level lock
tracing was performed and none is claimed.

## The two post-deploy timer fires

**First natural fire (22:14:45 UTC):** systemd SUCCESS / exit 0, but no source
was due (the 2-hour per-source cadence had not elapsed since the last
pre-deploy runs at 21:14Z) and **no run rows were created**. Classified
correctly as `NATURAL_DUE_CHECK_ONLY` — it proves the timer fires and
canonical code executes; it is NOT the authoritative collection-cycle proof.

**Second natural fire (trigger 23:14:27Z, execution 23:15:48–23:17:21Z):**
exit 0/SUCCESS, ran the canonical scope. This is the **authoritative natural
collection proof**.

## Natural collection evidence

Production sources: `the_elec`, `lg_display_newsroom`, `etnews_hardware` —
all success. Experimental sources also ran according to canonical soak scope.
Every durable run row recorded `provenance = SCHEDULED`. Articles advanced
917 → 920 naturally.

## Qualification status — orthogonal to deployment

The newly created qualification epochs report `NOT_QUALIFIED` (gate status on
run rows). This is **expected**: the M8 qualification machinery requires
repeated scheduled successes, and the canonical deployment had just started
its first epoch. **DEPLOYMENT LIVE PROOF: CONFIRMED. QUALIFICATION MATURITY:
NOT_YET_QUALIFIED.** These are orthogonal facts. OPS-COM-003 is not re-closed
or re-classified.

## Family result

`FIRST_VALIDATED_MEMBER_OF_SYSTEMD_VENV_SOAK_COMPATIBILITY` is descriptive
process evidence naming exactly one member: KTW
`f49bd02eb214b650a146e9c0f6f348d526285a91`. This is not a new standard and is
not merged with any existing family. All other Clanks inherit nothing.

Exactly one narrow KTW DEPLOY-COM-001 fact is admitted; all prior admissions
(Watch COM-001, Semiconductor/KTW/Tablet/Feature Phone/OEM Radar/CTW
COM-002, Smartwatch/Tablet COM-001, Feature Phone COM-001, OEM Radar COM-002,
Smartwatch COM-002, CTW COM-002) remain preserved, as does KTW's M1
insufficiency history. No host, deployment, collector, production-DB, or
target modification occurred in this pass. Frozen standard files and immutable
tags were not changed or moved.

No overall KTW conformance is claimed beyond this deployment proof.
