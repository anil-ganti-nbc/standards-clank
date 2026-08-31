# watch-clank M2 — informed remediation plan

## Scope and state

This plan follows M1 finding `WC-M1-001` exactly. Watch remains at
`fbf228f7ecccf2de4119fca29f8344aff9c49441` on `main`; it has not advanced
since M1. This plan changes no Watch code, service, scheduler, database,
notification, deployment, frozen standard, or tag.

## WC-M1-001: root cause and options

`app/services/run_lock.py` grants coordination through a JSON file plus a
`CollectorRun` row, then treats timestamp expiry and `_pid_alive(pid)` as the
authority to honor or reclaim the file. The PID identifies a claimant, but is
reusable and namespace-local; a container can have PID 1 independently and a
host can reuse a PID. The database row records execution state but does not
grant the file ownership. All canonical execution paths use this service:
`app/services/pipeline.py`, `app/services/specialist_leads.py`, and dashboard
calls in `app/main.py`.

| Option | Assessment |
|---|---|
| Hold an OS/kernel advisory file-lock handle for the full run; retain JSON only as diagnostic metadata | **Preferred.** The grant itself proves current ownership; process crash closes the handle. A portable implementation must use Windows and Linux locking primitives (or one small, pinned cross-platform lock dependency), work on the shared state volume, and preserve the existing service interface. |
| Replace the file/PID reclaim path with a database-session-scoped lock/transactional ownership record | Credible where all writers share one database authority, but SQLite/container topology and cross-host semantics must first be proven. It increases migration and test risk without a demonstrated need. |

Preferred repair: make the held kernel/advisory handle the sole exclusivity
authority; never reclaim or honor a lock based on PID/timestamp. Metadata may
remain for diagnostics. Test Windows and Linux behavior, cross-process
exclusion, crash/handle-release recovery, and rejection of a stale metadata
file without a held grant.

## M1 insufficient-evidence dispositions

* `STD-OPS-COM-003`: **NON_CONFORMING.** `WATCH_SOAK_CONTRACT.md` defines
  policy and `delivery_gate.py` encodes membership, but no stored qualification
  record links natural/manual/deploy/recovery provenance, material-change reset
  identity/reason, retained incident evidence, and gate-drift failure. Minimum
  outcome: durable qualification evidence with those distinctions and a
  fail-closed structural comparison of every promotion gate.
* `STD-DEPLOY-COM-001`: **NON_CONFORMING.** `docker-compose.staging.yml` and
  `Dockerfile` require an intended image/revision, but current source has no
  deployment-completion record or verification comparing declared intended
  state, running revision, deploy-critical configuration, required wiring, and
  partial convergence. This is a repository implementation gap, not a reason
  to reverse M1 applicability. Host verification will be required later.
* Test environment: **ENVIRONMENT_SETUP_ONLY.** `pyproject.toml` declares
  `structlog>=24.4.0` and the dev test dependencies. M3 reproducible setup is
  `python -m venv .venv`, then `.venv\\Scripts\\python -m pip install -e
  ".[dev]"`, then `.venv\\Scripts\\python -m pytest -m "not live"` (use
  POSIX `.venv/bin/python` on Linux). No repository dependency defect found.

## Exact M3 implementation scope

| Area | Files | Intended change and tests |
|---|---|---|
| Lock authority | `app/services/run_lock.py`; possibly `pyproject.toml` if a pinned portable lock library is selected | Keep a live grant handle; remove PID/timestamp authority decisions; preserve diagnostic metadata and current caller contract. Add cross-process, stale-metadata, crash-release, and Windows/Linux tests in `tests/test_core.py`. |
| Caller compatibility | `app/services/pipeline.py`, `app/services/specialist_leads.py`, `app/main.py` only if required by the unchanged lock lifecycle | Ensure every acquire/release path closes the grant on all success/error paths. Add focused caller-path tests; no scheduler or dashboard redesign. |
| Qualification evidence | `app/models/` plus Alembic migration, `app/services/` qualification/promotion boundary, and `tests/` | Persist execution provenance, material-reset identity/reason, intervention/incidence treatment, and gate comparison. Migration must preserve existing evidence and fail closed on disagreement. |
| Deployment completion | deployment command/status implementation and tests, to be selected from current deployment ownership | Record target scope and intended-vs-running comparison before any completion claim; represent non-convergence as in-progress/partial. Host-only proof is a separately authorized verification step. |

Risks: advisory locking semantics on network/shared filesystems; backwards
compatibility of existing lock metadata; migration safety for qualification
history; and avoiding a deployment tool prescription. No distributed lock or
fleet service is warranted by the current single-host architecture.

## Verification order

1. Create the disposable Watch test environment above; run non-live tests.
2. Add the lock regression tests, then implement the preferred handle-held
   grant repair and run focused tests.
3. Implement durable OPS-COM-003 evidence and its migration/tests.
4. Implement DEPLOY-COM-001 completion evidence/tests without performing a
   deployment.
5. Run the full non-live Watch suite.
6. Obtain separate authorization for host/runtime proof of intended versus
   materially running deployment state.
7. Run a separate Standards Clank M3 re-audit; only then consider
   known-evidence admission.
