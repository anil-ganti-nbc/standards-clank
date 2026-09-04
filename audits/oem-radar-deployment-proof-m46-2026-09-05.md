# OEM Radar DEPLOY-COM-001 live-proof admission — 2026-09-05

```json
{"clank":"oem-radar","date":"2026-09-05","findings":[{"standard":"STD-DEPLOY-COM-001","kind":"conformance","summary":"LIVE_PROOF_CONFIRMED at OEM Radar 070914c82516c29be781a49acb77c8d86953f1e2 on target hetzner:/home/deploy/staging/oem-radar (cron-docker-compose one-shot lane): intended SHA = host checkout = OCI revision label = runtime self-report all 070914c, .deployed-id updated from a7714fc, canonical cron 20 * * * * through deploy/run.sh unchanged, and the 19:20 UTC natural fire executed real collection (gmktec-shopify 78 discovered/3 events + minisforum-shopify 59 discovered/2 events, both status ok and health ok) with zero false novelty (new = 0), DB marker 7 COMPATIBLE quick_check ok and total runs 364→366, lock mtime correlated with the natural run."}]}
```

## Scope and mode

This is a **Standards-only recording/admission pass** (M46). The live-proof
actions were executed in the separately authorized M45-OEM bounded deploy pass;
this pass made **no host access, no deployment/restart, no database change, no
collector execution, and no source modification**. It records and admits the
completed proof for `STD-DEPLOY-COM-001` at OEM Radar
`070914c82516c29be781a49acb77c8d86953f1e2`, target
`hetzner:/home/deploy/staging/oem-radar`, scope: this exact source SHA + target
+ cron-docker-compose one-shot mechanism.

## Pre-deploy divergent state

The pre-M45 live checkout was at `a7714fc15546e115d01db99b71d8f458535884ff`,
the tip of divergent branch `feature/oem-radar-2`. The merge-base with
canonical main was `e12afe9` (M4.5 QC activation). The feature branch carried
7 unique commits (OEM Radar 2.0 editorial plane, Phase 10 activation, QC
archive, PyInstaller packaging, and OS-advisory run-lock adoption); canonical
main carried 9 unique commits (M15 persistent-state barrier, 3 UI redesign
commits, 2 frozen-launcher fixes, the OS-flock run-lock fix, and the Collector
UI Design System adoption). This was **not** a simple fast-forward — the two
lineages diverged at `e12afe9`.

## Lock-equivalence gate (pre-deploy precondition — PASSED)

Both the live feature branch (`a7714fc`) and canonical main (`070914c` via
`d720e06`) carry the identical OS-level `flock` implementation derived from
NAS PR #4. Source-level comparison confirmed the lock docstrings and
mechanisms are character-identical. Switching from `a7714fc` to `070914c` did
not regress the established lock/exclusivity authority. OPS-COM-004 is not
re-admitted.

## Backup

Created using SQLite online backup API through the Docker volume
(`oem_radar_portability_data`):
`/home/deploy/staging/oem-radar/backups/radar-pre-m45-070914c.db`,
6,275,072 bytes, sha256
`4c28553de97e7e4b617cca0ddbabf580b144d727ea9502ac6b61c22d8841e591`.
The backup size matched the live DB file exactly.

## Deployment identity (three-way proven)

A. git checkout HEAD: `070914c82516c29be781a49acb77c8d86953f1e2`
B. OCI revision label on image `oem-radar:070914c`:
   `070914c82516c29be781a49acb77c8d86953f1e2`
C. runtime self-report (`runtime_bridge.identity()` → `source_revision`):
   `070914c82516c29be781a49acb77c8d86953f1e2`

`.deployed-id` transitioned from `a7714fc` to `070914c`. `.deployed-id` is a
deployment-control artifact that selects the compose image tag; it is not
sole runtime identity (the three-way chain above serves that role).

## Dependency and persistent-state gates

Dependency gate: PASSED — no effective dependency difference between
`a7714fc` and `070914c` across pyproject, requirements, uv.lock, Dockerfile,
or compose file. Persistent-state gate: PASSED — live marker 7 matches
canonical expected 7, quick_check ok, no migration required. DEPLOY-COM-002
is not re-closed.

## Natural collection proof (authoritative)

**First post-deploy timer fire (18:20 UTC):** ran the OLD image (`a7714fc`)
because `.deployed-id` had not yet been updated. Classified as a pre-deploy
due-check cycle — NOT canonical proof.

**Authoritative natural canonical fire (19:20 UTC):** cron triggered
`deploy/run.sh`, which read the updated `.deployed-id = 070914c` and ran
`docker compose run --rm oem-radar run`. Real collectors executed:
- `gmktec-shopify`: status ok, health ok, 78 discovered, 3 events
- `minisforum-shopify`: status ok, health ok, 59 discovered, 2 events
- Zero false novelty: new = 0 across all sources
- DB integrity: quick_check ok, marker 7 unchanged, total runs 364 → 366 (+2)
- Lock mtime correlated with the natural run start
- No rollback required

## Config/resource identity

The canonical main includes the `_MEIPASS` frozen-Windows path fix and the
frozen-launcher serve() fix (`d2d84dc`, `74d404a`). These are N/A to this
live container/checkout deployment (the target runs from a git checkout, not
a frozen Windows bundle). The persistent DB remains under the intended Docker
volume data root (`oem_radar_portability_data` → `/app/data`). Configuration
resolves correctly.

## Family result

`FIRST_VALIDATED_MEMBER_OF_CRON_DOCKER_COMPOSE_ONE_SHOT_COMPATIBILITY` is
descriptive process evidence naming exactly one member: OEM Radar
`070914c82516c29be781a49acb77c8d86953f1e2`. This is not a new standard and is
not merged with existing families. All other Clanks inherit nothing.

Exactly one narrow OEM Radar DEPLOY-COM-001 fact is admitted; all prior
deployment admissions remain preserved, as does OEM Radar's M1 insufficiency
history. No host, deployment, collector, production-DB, or target modification
occurred in this pass. Frozen standard files and immutable tags were not
changed or moved.
