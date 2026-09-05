# Smartphone DEPLOY-COM-002 admission — M57 evidence-model repair (2026-09-05)

```json
{"clank":"smartphone-clank","date":"2026-09-05","findings":[{"standard":"STD-DEPLOY-COM-002","kind":"conformance","summary":"CONFORMS / CLOSED at canonical Smartphone main revision e514c45dca4cf966441c27799d98761096dc8c40 (source-level fail-closed compatibility evidence; no current-canon liveness claim beyond the separately-scoped COM-001 fact): database/schema_guard.py::ensure_schema_or_refuse is the production runtime barrier and raises SchemaError without mutating schema when the database has no Alembic revision stamped, or when current != head in either direction (behind, newer, or divergent), naming the reason and the remedy; it is wired into every production entry point — main.py init (l.99), main.py run (l.131), runtime/daemon.py startup (l.82) and runtime/run_once.py startup (l.216), the last being the scheduled one-shot collector path, where the barrier precedes get_session_factory/IntelligencePipeline construction and target building, and a SchemaError is logged as 'refusing to start: …' and returns exit 1; Base.metadata.create_all is confined to init_fresh_database, which itself refuses when any table already exists, so create_all can never admit compatibility on an existing database. tests/wave1/test_schema_authority.py covers unstamped-DB refusal, old-DB refusal until upgraded, init_fresh_database refusal on a populated DB, new-model import not mutating an existing database, failed migration not stamping success, and ensure_tables_present_or_refuse raising without creating. Corroborating chronology only, NOT the proof basis: the canonical M1 blind sweep recorded Smartphone's schema guard as the positive COM-002 exception at 5684cf2c4d7bc962260bee85d0df32f68c962d46 and M10 therefore excluded Smartphone from the persistent-state remediation cohort; M48's live 0007->0008 transition is separately-scoped deployment history and is expressly not used as COM-002 proof. Resolves M56 debt D9."}]}
```

**Classification: `SMARTPHONE_COM002_RECORDING_DEFECT`** — and independently
`SUFFICIENT_BUT_UNADMITTED` on this pass's own source verification, so the
admission is safe under either reading of M57 §9.

This artifact admits existing, already-demonstrable evidence. It creates no new
proof, performs no host or source action, and does not extend Smartphone's
COM-001 liveness claim.

## Why the fact was missing

M56 recorded debt D9: Smartphone has no standalone COM-002 admission, with its
Alembic evidence appearing inside the COM-001 deployment proof.

The structural reason is now identified. The seven existing COM-002 facts are
exactly the **M10 persistent-state remediation cohort**.
`audits/fleet-persistent-state-compatibility-planning-m10-2026-09-01.json`
records:

- `included_targets`: oem-radar, semiconductor-intelligence, chinese-tech-wire,
  korean-tech-wire, feature-phone-clank, smartwatch-clank, tablet-clank — the
  seven, exactly.
- `excluded_targets`: `["smartphone-clank"]`
- `exclusion_reason`: *"Smartphone was not flagged for this gap in the canonical
  M1 sweep; no source evidence in this pass overturns that bookkeeping."*

And the canonical M1 blind sweep
(`audits/fleet-blind-audit-sweep-m1-2026-09-01.json`) records the gap as:

> `PERSISTENT_STATE_COMPATIBILITY_GATE_UNPROVEN` … *"The sweep found
> schemas/migrations, but not a target-specific fail-closed compatibility
> barrier that can be trusted as deployment evidence. **Smartphone Clank's
> schema guard was the positive exception.**"*

M1's Smartphone entry lists `insufficient_standards` as
`["STD-UI-COM-011","STD-DATA-COM-001","STD-DEPLOY-COM-001"]` — **DEPLOY-COM-002
is absent**, i.e. it was counted among Smartphone's 12 CONFORMS, with basis
*"current lock and schema-guard implementations are positive evidence."*

So Smartphone was excluded from remediation **because it already conformed**.
The only encoding pathway into the deployment graph at that time was the
remediation-audit pipeline, which by definition Smartphone never entered. The
project explicitly concluded COM-002 and simply had no route to record it.

## A. Source-level fail-closed compatibility evidence — the proof basis

Verified read-only at `e514c45dca4c…` this pass, independent of any live
transition.

| Frozen COM-002 element | Evidence at `e514c45` | Result |
| --- | --- | --- |
| Trigger: persistent structured state, independently evolving contract | SQLite under an Alembic chain (`0008_analyst_action_integrity` at head) | **APPLICABLE** |
| Barrier before normal incompatible work is accepted | `ensure_schema_or_refuse` at `runtime/run_once.py:216`, **before** `get_session_factory`, `IntelligencePipeline(...)` and target building; also `main.py:99`/`:131`, `runtime/daemon.py:82` | **Satisfied** |
| Fail closed on known incompatibility | raises `SchemaError` *"never mutates schema"*; `run_once` logs `refusing to start: …` and returns exit 1 | **Satisfied** |
| Handles missing / older / newer / divergent state | `current is None` → refuse (unstamped); `current != head` → refuse, a strict inequality that also catches newer and divergent revisions | **Satisfied** |
| Evidence identifying compatibility gating as the cause | `SchemaError` message names current vs expected revision and the remedy command; `log.error("refusing to start: %s", e)` | **Satisfied** |
| `create_all` must not admit compatibility | confined to `init_fresh_database`, which raises `SchemaError` if **any** table already exists — so it can only ever run against a genuinely empty database | **Satisfied** |

Regression coverage at the same SHA, `tests/wave1/test_schema_authority.py`:
`test_ensure_schema_or_refuse_raises_on_unstamped_db`,
`test_old_db_refuses_normal_startup_until_upgraded`,
`test_init_fresh_database_refuses_on_populated_db`,
`test_importing_new_model_does_not_mutate_existing_database`,
`test_migration_failure_does_not_stamp_success`,
`test_ensure_tables_present_or_refuse_raises_without_creating`.

## B. M48's live 0007→0008 transition — corroboration only, expressly not the proof

Per M57 §14 these are kept strictly separate. The M49 COM-001 proof records that
Alembic advanced `0007 → 0008_analyst_action_integrity` on the live database,
and that this happened via a **procedural deviation**: a scratch-first
qualification was intended, `alembic/env.py` resolved `sqlalchemy.url` from its
own config rather than the supplied `-x` override, and the migration therefore
ran against **live** first, bypassing the scratch step, succeeding cleanly.

That history is preserved unchanged and is **not** used here. A successful
`0007→0008` transition demonstrates that one migration applied correctly at one
DB state; it does **not** demonstrate the COM-002 invariant, which is that normal
work is *refused* while code and state are known incompatible. The invariant is
established solely by section A above.

## Scope discipline

- Scoped to source revision `e514c45dca4cf966441c27799d98761096dc8c40`, which at
  M56 observation time was also current canon and the COM-001 proof SHA. This
  admission asserts the **code property**, not continued liveness.
- COM-001 is untouched and not re-scoped; its separate liveness claim stands on
  its own evidence.
- M1's earlier conclusion at `5684cf2c…` is recorded as chronology, not restated
  as a second fact.
