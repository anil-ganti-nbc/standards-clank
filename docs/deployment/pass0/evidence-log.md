# Deployment Pass 0A — Evidence Log

Survey date: 2026-08-31. All fleet checkouts below were cloned read-only from
GitHub. Paths are source evidence, not mandates. `clank-architecture` was
read-only governance evidence.

| Repo | SHA inspected | Deployment-relevant findings / paths | Incidents | Confidence |
|---|---|---|---|---|
| watch-clank | `fbf228f` | `app/db/schema_check.py` fails on Alembic mismatch; `app/core/identity.py`, `scripts/identity.py`, compose and systemd material support runtime identity; `tests/test_deploy_image_tag_safety.py` forbids a soft image-tag default | DEP-INC-001, 003 | HIGH |
| oem-radar | `d720e06` | `ai/handoff/DEPLOYMENT_PROCEDURE.md` has a three-way identity check; Docker entrypoint and runtime bridge expose deployment assumptions | DEP-INC-004 | MODERATE |
| chinese-tech-wire | `1a47220` | `REPRODUCIBLE_BUILD.md`, `runtime_bridge.py`, `docker-compose.staging.yml`, and release runbook distinguish build labels/identity; no confirmed deployment incident located | — | MODERATE |
| korean-tech-wire | `afb4aad` | `docs/hetzner-migration.md` and runbook document manually checked migration/health; no automated fail-closed schema gate found | — | MODERATE |
| feature-phone-clank | `4051b64` | Experimental deployment is isolated by checkout/image/volume/DB/lock/crontab in `docs/FEATURE_PHONE_SCOPE_EXPANSION.md`; compose and experimental deploy script preserve this separation | DEP-INC-005 | HIGH |
| smartphone-clank | `5684cf2` | `database/schema_guard.py`, `docs/infra/DEPLOYMENT_MODEL.md`, `HETZNER_SOAK_COMMISSIONING.md`, and systemd docs demonstrate clean-checkout and schema checks | DEP-INC-002, 006 | HIGH |
| smartwatch-clank | `08a23f9` | `docs/hetzner-deployment-2026-08-18.md` records five-way parity and post-deploy verification; Garmin ticket records divergent wrapper wiring | DEP-INC-004, 007 | HIGH |
| tablet-clank | `41282f7` | `docs/OPERATIONS.md`, `REPRODUCIBLE_BUILD.md`, and storage/CLI files show schema and host material but no independent gate; historical fleet sweep missed Hetzner | DEP-INC-008, 009 | MODERATE |
| semiconductor-intelligence | `8a356a3` | `PHASE0_CONTAINMENT.md` calls itself `UNVERIFIED_PRODUCTION` until host-evidenced digest and unattended runs; runbook/rollback records are planning evidence | — | MODERATE |
| diagnostic-clank | `3667af0` | `operations/phase0/OPERATOR_INSTANCE_CHECKLIST.md` and `preflight.py` insist repo HEAD is not deployment proof and keep hosts UNKNOWN; no live NAS log was available in this checkout/read-only path | DEP-INC-005, 010 | HIGH |
| clank-architecture | `e9c4a2b` | `FLEET_LAWS.md`, `RISK_REGISTER.md`, Golden Incident Corpus and ADR-0009 govern overlapping risks; Law 6 ACTIVE, Law 9 DEFERRED, ADR-0009 PROPOSED — REVIEWED DRAFT | DEP-INC-008–010 | HIGH |

## Reused Operations evidence

The three declared seeds are reused, retaining their Operations identities:

| Deployment cluster | Operations origin | Deployment-specific interpretation |
|---|---|---|
| materialisation truth | INC-014 / config drift | committed configuration is not proof that runtime wiring loaded it |
| running revision identity | INC-017, INC-030, INC-031, INC-038–040 / remote-host truth | host-evidenced artifact/revision and coverage are separate from repository state |
| schema-code compatibility | INC-007, INC-016 / schema/deploy gating | startup/traffic transition must expose incompatible persisted state |

## Governance inspected

- Fleet Law 5, **ACTIVE**: single scheduler/notification authority; it overlaps partial deployment but is already binding and CI-backed in `conformance/test_fleet_laws.py`.
- Fleet Law 6, **ACTIVE**: exact SHA/digest evidenced on host; directly overlaps running revision identity and is CI-backed.
- Fleet Law 9, **DEFERRED candidate**: deployment convergence; it touches host/repo drift but is explicitly not active.
- ADR-0008, **status verified from current file as ADR governance**: execution liveness/materialisation overlap; no competing authority is created here.
- ADR-0009, **PROPOSED — REVIEWED DRAFT**: state separation and destructive-operation safety. It is not activated by this pass. Its contract arose from the feature-phone total volume loss and smartwatch partial loss, and its mechanically checkable pieces are in architecture conformance.

No existing `STD-DEPLOY-*` or deployment normative standard was found.
