# Watch Clank DEPLOY-COM-001 live-proof observation — 2026-09-01

```json
{"clank":"watch-clank","date":"2026-09-01","findings":[]}
```

## Scope and outcome

This is a narrowly authorized, read-only observation of the deployed Watch
target for `STD-DEPLOY-COM-001`.  It performed no deployment, restart,
configuration mutation, host-file mutation, database access, scheduler change,
collector execution, or notification.

**Outcome: `LIVE_PROOF_FAILED`.**  The intended canonical revision is not
proven to be the material runtime revision, and the independently observed
deployment selector differs from it.  This artifact is not a known-evidence
admission and does not alter any standards finding state.

Source baselines at takeover: Watch `d03bc4b2f90289686331af0447d5ca4e8cf55822`
(`HEAD` and `origin/main`); Standards
`79cf5f73702575753fd56abfa343edacc93efcb2` (`HEAD` and `origin/master`).
The host observation occurred on 2026-09-01 in Asia/Kolkata; the comparator
recorded `2026-09-01T02:59:35.914352+00:00`.

## Independent facts

| Fact | Source | Observation | Comparison |
| --- | --- | --- | --- |
| Intended revision | Watch GitHub canonical `main` | `d03bc4b2f90289686331af0447d5ca4e8cf55822` | Required target revision |
| Intended artifact mechanism | Watch `scripts/systemd/docker/README.md` | `WATCH_CLANK_IMAGE=watch-clank:<git-sha>` | Artifact selector must identify the intended Git revision |
| Target identity | read-only SSH hostname | `ubuntu-4gb-hel1-1` | Target scope: `hetzner/ubuntu-4gb-hel1-1:user-systemd-docker` |
| Effective image selector | read-only SSH query of `~/.config/watch-clank/docker.env` for `WATCH_CLANK_IMAGE` only | `watch-clank:5bc8020` | Does not match intended revision |
| Immutable image revision label | read-only SSH `docker image inspect watch-clank:5bc8020` | `org.opencontainers.image.revision = unknown` | Cannot establish intended material runtime revision |
| Scheduler wiring | read-only SSH user-systemd unit listing | 22 `watch-clank-*.timer` units, all `loaded active waiting` | Matches the 22 controls returned by Watch's `all_controls()` registry |
| Persistent container | read-only SSH `docker ps` name filter | none | Expected for one-shot timer services; not used as positive revision evidence |

The target's selected image is therefore both configured to a different
revision-like tag and lacks a usable immutable revision label.  The active
timers establish that the scheduler wiring is present, but cannot repair the
revision/configuration mismatch.

## Deployment-status mechanism result

The existing Watch comparator was invoked locally with the independently
captured host facts and no substituted revision:

```text
WATCH_CLANK_RUNNING_REVISION=unknown
WATCH_CLANK_CONFIG_MATCHES=false
WATCH_CLANK_WIRING_MATCHES=true
WATCH_CLANK_COMPONENTS_CONVERGED=true
WATCH_CLANK_OBSERVATION_SOURCE=read-only-ssh:docker-image-label+docker.env-selector+user-systemd-timers
python scripts/deployment_status.py \
  --target hetzner/ubuntu-4gb-hel1-1:user-systemd-docker \
  --intended-revision d03bc4b2f90289686331af0447d5ca4e8cf55822
```

It returned the following result and its expected non-complete exit code:

```json
{"comparison_matches": false, "evidence_source": "read-only-ssh:docker-image-label+docker.env-selector+user-systemd-timers", "intended_revision": "d03bc4b2f90289686331af0447d5ca4e8cf55822", "running_revision": "unknown", "state": "UNVERIFIED", "target_scope": "hetzner/ubuntu-4gb-hel1-1:user-systemd-docker"}
```

`deployment_status.py` exited `2`, as designed for a state other than
`COMPLETE`.

## Exact read-only observation commands

```text
ssh -o BatchMode=yes -o ConnectTimeout=15 anilganti@204.168.142.1 \
  "grep '^WATCH_CLANK_IMAGE=' ~/.config/watch-clank/docker.env"
ssh -o BatchMode=yes -o ConnectTimeout=15 anilganti@204.168.142.1 \
  "systemctl --user list-units --all --no-legend 'watch-clank-*.timer'"
ssh -o BatchMode=yes -o ConnectTimeout=15 anilganti@204.168.142.1 \
  "docker ps --format '{{.Names}}' --filter name=watch-clank"
ssh -o BatchMode=yes -o ConnectTimeout=15 anilganti@204.168.142.1 \
  "docker image inspect watch-clank:5bc8020 | grep 'org.opencontainers.image.revision'"
```

The local registry count was read with:

```text
python -c "from app.services.collector_registry import all_controls; print(len(all_controls()))"
```

## Follow-up boundary

Do not admit this evidence or close `DEPLOY-COM-001` in this pass.  A separate
authorized remediation must supply a target whose immutable running revision
and effective configuration converge to the declared intended revision; only
then may a Standards re-audit evaluate admission.
