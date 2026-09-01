# Fleet Qualification Planning M4 — 2026-09-01

```json
{"clank":"fleet","date":"2026-09-01","findings":[]}
```

This is a read-only planning artifact for the six Clanks that the canonical
M1 sweep classified as having an unresolved
`STD-OPS-COM-003` qualification-provenance/reset evidence gap. It is derived
from the M1 sweep and M2 remediation ledger and inspects each target's current
source shape at its audited revision. It does not change target code, run
target tests, perform host or deployment work, admit evidence, or draft a new
standard.

The reusable contract is:

`execution authority establishes provenance → material identity is computed →
required epoch reset occurs before gated use → evidence is persisted against
execution/epoch → downstream gates consume but never invent provenance`.

The contract is shared; storage, runtime, migration, and authority adapters
remain target-specific. A missing trigger fact remains `UNKNOWN` and must
fail closed where the gate requires trustworthy provenance. Reset facts and
terminal execution facts remain distinct records when one execution would
otherwise consume the same identity slot.

## Qualification boundary matrix

The M1 status shown here is the starting evidence state, not a new conformance
decision. All six targets remain `INSUFFICIENT_EVIDENCE` for
`STD-OPS-COM-003` until independently remediated and re-audited.

| Clank | Authority boundary | Evidence boundary | Material identity | Reset boundary | Gate boundary | Persistence model | Migration need | Risk |
|---|---|---|---|---|---|---|---|---|
| OEM Radar | External OS scheduler, manual CLI, and dashboard invocation all converge on a stateless one-shot runner; no trigger is passed into the runner. | SQLite `crawler_runs` plus snapshots, events, and source health. | Product/configuration keys and content hashes describe observed products, not release/config material identity. | None. No qualification epoch or reset lineage exists; first decision is whether a real qualification lifecycle is applicable. | Due/health/completed-run checks, not an epoch-aware promotion gate; production is explicitly unverified/frozen. | Embedded SQLite schema v7 with local migrations. | Additive qualification records only after applicability is confirmed; preserve crawler history and avoid overloading product hashes. | Highest ambiguity: the target has no obvious qualification authority or lifecycle, so inventing one would be a governance change. |
| Semiconductor Intelligence | `OperationalScheduler` structurally records MANUAL_CLI, MANUAL_GUI, SCHEDULER, STARTUP_CATCHUP, RETRY, and TEST on `OperationalJobRun`; owner and lease are also persisted. | Operational job runs/leases, provider runs, signal items/candidates, promotion events, evidence, and editorial stories. | Candidate fingerprints/content hashes identify signal evidence, not deployed code/config or qualification material identity. | None. Job trigger provenance exists, but no qualification epoch, material-change detector, or explicit reset lineage. | Candidate eligibility, thresholds, budgets, and manual/automatic promotion; this is editorial promotion, not soak qualification. | SQLAlchemy/Alembic migrations (latest phase-9 operational automation migration). | Add a dedicated qualification projection linked to job execution; do not retrofit free-form `promoted_by` or candidate fingerprints. | Strongest scheduler evidence, but high semantic risk of confusing editorial promotion with deployment qualification. |
| Korean Tech Wire | Foreground CLI/dashboard and portable soak invoke the same collector path; any future scheduler is external. `RunLock` serializes execution but does not establish trigger provenance. | Aggregate `runs`, per-source health, fetch attempts, errors, articles, and QC/archive history. | Canonical URLs/content hashes and source status identify content, not release/config material identity. | None. No qualification epoch; source history and production/experimental policy are narrative. | Source status plus health-history/promotion-policy review; no persisted fail-closed qualification gate. | Embedded SQLite migrations v1–v4. | Additive per-invocation/per-source provenance and qualification tables; preserve aggregate history and migration versions. | Aggregate run versus per-source evidence can lose authority linkage; policy is narrative and has no single existing gate boundary. |
| Feature Phone | Manual dashboard controller and scheduled/CLI production runs converge on `_run`; production and experimental use separate stores/locks. The current runner passes no trigger provenance. | SQLite `collector_runs`, observations, classification log, events, and append-only continuity JSONL. | Product keys, content hashes, and classifications identify data; production allowlist is configuration, not a recorded material identity. | Continuity JSONL has a data-loss epoch (`fpc-epoch-2`), but it is not a qualification epoch and must not be reused for this purpose. | Scope allowlist and healthy/baseline run status; no explicit epoch-aware qualification gate. | SQLite schema v4 plus hash-tamper-evident JSONL continuity registry. | Add separate qualification/epoch/reset records and additive run provenance; keep continuity/data-loss epochs and historical unknowns intact. | High collision risk between continuity epochs and qualification epochs; distinct production/experimental stores require explicit scope binding. |
| Smartwatch | CLI production/experimental, manual controller, and soak cycle establish structured run metadata; `RunProvenance` carries app version, config fingerprint, and git revision, with UUID run identity. | Run/observation/discovery tables, health, soak state, host migrations, and continuity evidence. | Already records git revision, config fingerprint, schema version, and run UUID; this is the closest existing material identity. | None. Host migration is continuity evidence, not a qualification reset; no explicit prior identity/reset lineage or epoch gate. | Production allowlist and soak health summary; no fail-closed qualification epoch gate. | SQLite schema v2 with embedded schema evolution, plus continuity/soak metadata. | Additive qualification epoch/reset tables or records linked to existing run UUID/provenance; preserve host migration history. | Lowest implementation risk, but existing provenance must not be mistaken for closed qualification; material-change policy still needs an explicit detector. |
| Tablet | Bounded soak/campaign (`run_bounded`) and production/manual collection are serialized by the OS advisory lock; campaign manifests bind roster and environment. | SQLite collector runs, source state, observations, `change_events.run_id`, and append-only campaign JSONL/manifests. | Product identity and observations plus roster hash/interpreter environment; no code/config/release identity is tied to qualification. | None. Campaign closure and historical host records are evidence, not a qualification reset. | Readiness/integrity, allowlist, healthy-cycle count, and human promotion; no epoch-aware fail-closed gate. | Inline SQLite schema v1 plus additive v2 `change_events.run_id` migration, and JSONL campaign reports. | Additive qualification/epoch/reset records linked to existing `run_id`; preserve the v2 run-id migration and separate reset from terminal facts. | Close to per-execution integration, but campaign and production evidence can be conflated unless scope, epoch, and terminal records are explicit. |

## Implementation families

| Family | Members | Reusable shape | Boundary that must remain target-local |
|---|---|---|---|
| Rich ORM/job provenance | Smartwatch, Semiconductor Intelligence | Qualification record keyed by an existing run/job identity; explicit provenance enum, material identity, epoch/reset, and gate projection. | Smartwatch has run-level provenance/UUID; Semiconductor has scheduler/job provenance but a separate editorial promotion model. |
| Per-source SQLite with operational scopes | Feature Phone, Tablet | Additive qualification rows linked to collector/run IDs; separate reset and terminal facts; production/experimental or campaign scope is explicit. | Feature Phone must keep data-loss continuity epochs separate; Tablet must preserve campaign manifests and `change_events.run_id`. |
| Aggregate SQLite health history | Korean Tech Wire | Additive invocation/per-source provenance and epoch projection over existing run/health history. | Aggregate invocation and per-source evidence linkage, plus narrative production policy, need explicit mechanics. |
| Stateless one-shot telemetry | OEM Radar | Applicability checkpoint first; if applicable, add a minimal execution/qualification envelope around the external trigger and existing `crawler_runs`. | There is no in-process scheduler, qualification gate, or release identity today. Do not implement a new lifecycle as if it were already present. |

The family labels are implementation-planning aids, not normative categories.
The common invariant and proof gates are reusable; no target may inherit
another target's evidence or storage schema.

## Common proof gates for every family

1. The real execution authority supplies provenance structurally. Scheduled,
   manual, deploy-verification, recovery, retry, and unknown paths remain
   distinguishable wherever they exist.
2. Material identity is computed from a trustworthy release/config/schema
   contract, not from product or content identity alone.
3. A material change appends a reset record containing the explicit prior
   material identity, new identity, reason, authority, and time before the
   first changed-run event can be evaluated by a gate.
4. Evidence is persisted against the execution and qualification epoch.
   Reset and terminal records are independently auditable.
5. Downstream delivery/gates consume the persisted provenance and epoch; they
   never fabricate `NATURAL` (or any equivalent) when provenance is absent.
   Missing or divergent evidence is `UNKNOWN`/fail-closed as required.

## Recommended batching order

1. **Smartwatch adapter/prototype.** It already has the richest trustworthy
   run provenance and material-identity fields. Prove the shared contract
   against its existing UUID/config/git records without treating that as
   qualification closure.
2. **Semiconductor Intelligence.** Reuse the contract at the scheduler/job
   boundary, while keeping editorial candidate promotion separate. This
   validates the rich-ORM family under multiple trigger types.
3. **Feature Phone + Tablet together.** Apply one per-source SQLite recipe
   with independent integrations. Keep Feature Phone's continuity epoch and
   Tablet's campaign/run-id mechanics explicitly separate from qualification
   reset/terminal facts.
4. **Korean Tech Wire.** Adapt the contract to aggregate invocation and
   per-source health history; do not infer provenance from the existing lock
   or narrative promotion policy.
5. **OEM Radar applicability checkpoint.** Before implementation, decide
   through the existing governance path whether this one-shot experimental
   collector has an applicable qualification/promotion lifecycle. If yes,
   add the smallest target-local envelope; if no, record the explicit
   applicability decision rather than manufacturing a gate.
6. **Fleet source re-audit, then per-target live proof.** Neither source
   conformance nor live deployment identity may be inherited from Watch or
   another Clank.

## Safety boundary

This pass performed source inspection only. No target repository, deployment,
host, scheduler, database, resolver fact, or known-evidence layer was
modified. No target tests, collectors, live probes, remediation, or admission
were performed. The JSON companion is the machine-readable planning ledger;
it is not a conformance audit and does not close `STD-OPS-COM-003`.
