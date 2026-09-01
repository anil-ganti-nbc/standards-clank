# Watch Clank DEPLOY-COM-001 live-proof remediation — 2026-09-01

```json
{"clank":"watch-clank","date":"2026-09-01","findings":[]}
```

## Outcome

**`LIVE_PROOF_CONFIRMED`** for the explicitly authorized target remediation.
This is a narrowly scoped evidence record, not a known-evidence admission and
not a standards-finding/index change.  The preceding failed observation is
preserved in `audits/watch-clank-deploy-live-proof-2026-09-01.md`.

Watch source at takeover and after remediation was
`d03bc4b2f90289686331af0447d5ca4e8cf55822` (`HEAD` = `origin/main`, clean).
Standards source was
`bf88d440e2db87edf55484f108a79dd98c44417a` (`HEAD` = `origin/master`, clean).
The target is `hetzner/ubuntu-4gb-hel1-1:user-systemd-docker` on host
`ubuntu-4gb-hel1-1` (`204.168.142.1`). Host observations were made on
2026-09-01 (Asia/Kolkata); command timestamps below are UTC as emitted by the
target or comparator.

## Pre-change state

| Facet | Independent observation |
| --- | --- |
| Target checkout | Clean detached checkout at `5bc8020caca1228d8f9c60fda47e5f175268d354` |
| Effective selector | `WATCH_CLANK_IMAGE=watch-clank:5bc8020` |
| Old image provenance | `org.opencontainers.image.revision = unknown` |
| Persistent container | None; the deployment is one-shot user-systemd Docker services |
| Service state | 22 Watch services loaded inactive/dead between runs |
| Timer wiring | 22/22 `watch-clank-*.timer` units loaded active/waiting |
| Database | `schema_actual=011_event_review_duplicate`, integrity `ok`, 8,713 watches, 0 stale runs, no active locks |

The old selector and unknown immutable label were the material mismatch that
caused the prior comparator result `UNVERIFIED` (exit `2`).

## Canonical remediation performed

The repository-defined Docker + user-systemd procedure was used.  Only these
bounded production actions occurred:

1. Fetched canonical `origin/main` into the target checkout and detached it at
   `d03bc4b2f90289686331af0447d5ca4e8cf55822`.
2. Built `watch-clank:d03bc4b2f90289686331af0447d5ca4e8cf55822` on the target
   with `--build-arg GIT_REVISION=d03bc4b2f90289686331af0447d5ca4e8cf55822`.
3. Created the rollback copy
   `/home/anilganti/watch-clank-backups/watch_clank.db.pre-deploy-d03bc4b2-20260901T032000Z`
   (317,399,040 bytes).
4. Ran the canonical explicit `python -m scripts.migrate` command in the new
   image.  It applied only committed additive migrations
   `012_lead_delivery_state`, `013_qualification_evidence`,
   `014_qualification_execution_identity`, and
   `015_qualification_reset_lineage`, reaching
   `015_qualification_reset_lineage` successfully.  Existing history was
   preserved.
5. Updated only `~/.config/watch-clank/docker.env` to
   `WATCH_CLANK_IMAGE=watch-clank:d03bc4b2f90289686331af0447d5ca4e8cf55822`.

No systemd unit definitions or timer enablement were changed.  No service was
manually started or restarted: one-shot units remain inactive between their
normal scheduled runs, and every timer remained active/waiting.

## Artifact provenance verification

Before changing the selector, read-only inspection of the new image produced:

```text
Id: sha256:a091fbe7f1736c98004c63f45c1b2c1c5abb85733e6b95779de635e4c90c7bdf
RepoDigest: watch-clank@sha256:a091fbe7f1736c98004c63f45c1b2c1c5abb85733e6b95779de635e4c90c7bdf
org.opencontainers.image.revision: d03bc4b2f90289686331af0447d5ca4e8cf55822
WATCH_CLANK_SOURCE_REVISION: d03bc4b2f90289686331af0447d5ca4e8cf55822
```

The image's `python -m scripts.identity` output independently returned the
same full SHA.  The old image's `unknown` label was not reused.

## Compatibility and post-change observation

The new image's read-only status check at
`2026-09-01T03:20:00.817522+00:00Z` reported:

```text
schema_actual=015_qualification_reset_lineage
schema_expected=015_qualification_reset_lineage
db_integrity_ok=true
total_watches=8713
stale_running_count=0
active_locks=[]
```

The 22 expected user-systemd timer units remained loaded active/waiting.  No
persistent container was present, consistent with the one-shot architecture;
the effective selector and newly built immutable image are the material
artifact for each scheduled run, and no old/new container mix was active.

## Deployment-status comparator

The existing Watch comparator was invoked locally with independently obtained
post-remediation facts (no substituted revision):

```text
WATCH_CLANK_RUNNING_REVISION=d03bc4b2f90289686331af0447d5ca4e8cf55822
WATCH_CLANK_CONFIG_MATCHES=true
WATCH_CLANK_WIRING_MATCHES=true
WATCH_CLANK_COMPONENTS_CONVERGED=true
WATCH_CLANK_OBSERVATION_SOURCE=read-only-ssh:post-deploy-oci-label+docker.env-selector+user-systemd-timers+status
python scripts/deployment_status.py \
  --target hetzner/ubuntu-4gb-hel1-1:user-systemd-docker \
  --intended-revision d03bc4b2f90289686331af0447d5ca4e8cf55822
```

At `2026-09-01T03:20:41.396019+00:00Z`, it returned:

```json
{"comparison_matches": true, "evidence_source": "read-only-ssh:post-deploy-oci-label+docker.env-selector+user-systemd-timers+status", "intended_revision": "d03bc4b2f90289686331af0447d5ca4e8cf55822", "running_revision": "d03bc4b2f90289686331af0447d5ca4e8cf55822", "state": "COMPLETE", "target_scope": "hetzner/ubuntu-4gb-hel1-1:user-systemd-docker"}
```

Comparator exit status: `0`.

## Exact read-only observation sources

```text
ssh -o BatchMode=yes -o ConnectTimeout=15 anilganti@204.168.142.1 "hostname; uname -a; grep '^WATCH_CLANK_IMAGE=' ~/.config/watch-clank/docker.env"
ssh -o BatchMode=yes -o ConnectTimeout=15 anilganti@204.168.142.1 "cd ~/watch-clank && git rev-parse HEAD && git status --short --branch"
ssh -o BatchMode=yes -o ConnectTimeout=15 anilganti@204.168.142.1 "docker ps -a --format '{{.ID}} {{.Image}} {{.Names}} {{.Status}}' --filter name=watch-clank"
ssh -o BatchMode=yes -o ConnectTimeout=15 anilganti@204.168.142.1 "systemctl --user list-units --all --no-legend 'watch-clank-*.service'"
ssh -o BatchMode=yes -o ConnectTimeout=15 anilganti@204.168.142.1 "systemctl --user list-timers --all --no-legend 'watch-clank-*.timer'"
ssh -o BatchMode=yes -o ConnectTimeout=15 anilganti@204.168.142.1 "docker image inspect watch-clank:d03bc4b2f90289686331af0447d5ca4e8cf55822"
ssh -o BatchMode=yes -o ConnectTimeout=15 anilganti@204.168.142.1 "docker run --rm watch-clank:d03bc4b2f90289686331af0447d5ca4e8cf55822 python -m scripts.identity"
ssh -o BatchMode=yes -o ConnectTimeout=15 anilganti@204.168.142.1 "docker run --rm -v watch_clank_staging_data:/data -e DATABASE_URL=sqlite:////data/watch_clank.db watch-clank:d03bc4b2f90289686331af0447d5ca4e8cf55822 python -m scripts.status --json"
```

The mutating commands were limited to the checkout fetch/detach, Docker image
build, rollback-copy creation, the explicit additive migration, and the single
`WATCH_CLANK_IMAGE` selector update described above.

## Safety declaration and rollback

- No unrelated Clank, OS, host-wide service, scheduler definition, source or
  collector scope was changed.
- No production data was deleted or reset; the current database was backed up
  before migration.
- No collector was run, no production event was manufactured, and no Discord
  notification was sent.
- No rollback was needed: the artifact provenance, schema compatibility,
  selector, wiring, and comparator all passed.
- The captured pre-deploy database copy and the previously loaded
  `watch-clank:5bc8020` image remain available for diagnosis/rollback; no
  rollback action was performed.

Do not admit this proof into known evidence or close the Standards finding in
this pass.  The next action is a separately authorized, narrow Standards
re-audit/admission pass for `DEPLOY-COM-001` using this artifact.
