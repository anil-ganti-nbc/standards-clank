# DEPLOY-COM-002 fleet completeness audit — M57 (2026-09-05)

```json
{"clank":"fleet-wide","date":"2026-09-05","findings":[]}
```

**This artifact records the completeness audit. It admits no fact itself** — the
two admissions it justifies live in their own per-Clank artifacts
(`watch-deploy-com-002-m57-2026-09-05.md`,
`smartphone-deploy-com-002-m57-2026-09-05.md`). Empty findings block by design.

Standards canon at takeover: `4f152d15f384b3b5c268bce3e6d36e1b08bb7124`.
Baseline: 1135 passed / 0 failed / 0 skipped, 21.27s, exit 0.

## 1. The frozen COM-002 decision rule (written before evaluating D8/D9)

Reconstructed from `standards/deployment/STD-DEPLOY-COM-002.json`, byte-identical
to `deployment-standards-v1.0`.

- **Trigger:** deployed code depends on persistent *structured* state whose
  schema/compatibility contract **can evolve independently**. Stateless,
  schema-less, and ephemeral-with-no-evolving-boundary are N/A — and acceptance
  criterion 5 makes N/A *"explicitly trigger-unmet rather than non-conforming."*
- **Obligation (three parts):** determine compatibility **at a barrier before
  normal incompatible work is accepted**; **fail closed** on known
  incompatibility; **preserve evidence** identifying compatibility gating as the
  reason work was refused.
- **Barrier location is free:** deploy preflight, startup, first normal
  transaction, or another trustworthy gate. Ordering and mechanism are not
  prescribed; no SQL engine, Alembic, migrations table, rollout order or
  rollback implementation is mandated.
- **Forbidden proxies:** process start, DB connectivity, DB existence, **table
  existence**, **`create_all` completion**, and deployment-command success are
  each explicitly insufficient *by themselves*.

**Does every Clank with persistent state necessarily apply?** No — only where the
contract can evolve independently. **May a source-level proof close it?**
**Yes.** Acceptance criterion 1 asks whether *"the running application can
distinguish compatible from known incompatible required persistent state"* — a
property of the deployed code's behaviour, not an observation of one host at one
moment. Nothing in the requirement or acceptance demands live-host observation,
in pointed contrast to COM-001, which explicitly requires the intended state be
*materially running*. **Is live proof required?** No. **How is historical
exact-source evidence scoped?** To the exact source revision at which the
property was verified.

This reading is corroborated by established practice, not invented here: all
seven pre-existing COM-002 facts are source-level admissions of the form
*"CONFORMS / CLOSED at canonical <Clank> main revision <SHA>"*, drawn from the
M11–M18 remediation audits. Not one was closed by live proof.

## 2. Why the count was seven — the structural explanation

The seven existing facts are exactly the **M10 persistent-state remediation
cohort**. `audits/fleet-persistent-state-compatibility-planning-m10-2026-09-01.json`
records `included_targets` as precisely those seven, `excluded_targets` as
`["smartphone-clank"]`, and the exclusion reason as *"Smartphone was not flagged
for this gap in the canonical M1 sweep."*

The canonical M1 blind sweep's gap entry reads:

> `PERSISTENT_STATE_COMPATIBILITY_GATE_UNPROVEN` … *"The sweep found
> schemas/migrations, but not a target-specific fail-closed compatibility barrier
> that can be trusted as deployment evidence. **Smartphone Clank's schema guard
> was the positive exception.**"*

So "7" never meant "7 applicable." It meant "7 needed remediation." Watch and
Smartphone were outside the cohort **because they already had the barrier** —
Watch adjudicated CONFORMS in the M4-series re-audit, Smartphone named as M1's
positive exception. Neither ever entered the remediation-audit pipeline, which
was the only route into the deployment evidence graph at the time.

## 3. Applicability determined independently of existing facts

Per §4, applicability was derived from the frozen trigger plus each Clank's
architecture — **not** from whether a fact already existed.

| # | Subject | Persistent structured state | Independently evolving contract | Applicability |
|---|---|---|---|---|
| 1 | watch-clank | SQLite | Alembic chain (head `015_qualification_reset_lineage`) | **APPLICABLE** |
| 2 | korean-tech-wire | SQLite + QC archive | numbered marker (main v5, archive v1) | **APPLICABLE** |
| 3 | tablet-clank | SQLite main/campaign + QC archive | numbered marker (v3 / v1) | **APPLICABLE** |
| 4 | feature-phone-clank | SqliteStore + QC archive | numbered marker (v5) | **APPLICABLE** |
| 5 | oem-radar | SQLite | `schema_migrations` v7 | **APPLICABLE** |
| 6 | smartwatch-clank | SQLite | monotonic `schema_version` v3 | **APPLICABLE** |
| 7 | smartphone-clank | SQLite | Alembic chain (head `0008_analyst_action_integrity`) | **APPLICABLE** |
| 8 | chinese-tech-wire | SQLite | `schema_meta` v1 | **APPLICABLE** |
| 9 | semiconductor-intelligence | SQLite | Alembic chain (`c7d8e9f0a1b2`) | **APPLICABLE** |

**9 applicable, 0 N/A, 0 insufficient-to-classify.** No target is stateless or
schema-less; every one carries an independently-evolving contract. The expected
final state is therefore **9 applicable / 9 closed**, and the pre-M57 seven was
genuinely incomplete — not a correct 7-plus-2-N/A.

## 4. D8 — Watch: `WATCH_COM002_RECORDING_DEFECT`

Full trace and verification in
[`watch-deploy-com-002-m57-2026-09-05.md`](watch-deploy-com-002-m57-2026-09-05.md).

The prose cite ("M4G closure unchanged") is **not** the origin — M4G is an
OPS-COM-003 re-audit with an empty findings block that mentions the barrier only
as *present*. The real adjudication is machine-readable in
`watch-clank-cross-domain-2026-09-01-reaudit.json` (APPLIES/CONFORMS, evidence
*"schema compatibility preflight and tests/test_schema_check.py"*), carried as
`STILL_CONFORMS` into `…-final.json`. The omission is mechanical: the generator
reads the `.md` findings block; the verdict lived in the `.json` companion.

Independently verified at `d03bc4b` against the frozen criteria: barrier in
`scripts/run_pipeline.py` before any collection work; refusal on any mismatch
*including a fresh uninitialized DB*; dedicated `EXIT_SCHEMA_MISMATCH=3` plus
structured log, printed reason and health alert; migrations never automatic and
tables never lazily created. Five tests cover the refusal paths.

## 5. D9 — Smartphone: `SMARTPHONE_COM002_RECORDING_DEFECT`

Full trace in
[`smartphone-deploy-com-002-m57-2026-09-05.md`](smartphone-deploy-com-002-m57-2026-09-05.md).

M1 counted Smartphone's COM-002 among its twelve CONFORMS — `DEPLOY-COM-002` is
absent from its `insufficient_standards`, with basis *"current lock and
schema-guard implementations are positive evidence"* — and the gap record names
it the positive exception. That is an explicit prior conclusion, hence
RECORDING_DEFECT. It **also** independently satisfies the
`SUFFICIENT_BUT_UNADMITTED` bar on this pass's own source verification, so the
admission is safe under either reading.

Verified at `e514c45`: `ensure_schema_or_refuse` raises without mutating schema
on unstamped state and on any `current != head` (behind, newer, or divergent);
wired into all four production entry points, and at
`runtime/run_once.py:216` the barrier precedes session-factory, pipeline
construction and target building; `create_all` is confined to
`init_fresh_database`, which refuses if any table exists. Six relevant tests in
`tests/wave1/test_schema_authority.py`.

**M48's live `0007→0008` transition is expressly not the proof basis** — a
successful migration at one DB state does not demonstrate the refusal invariant.
It is retained as corroborating chronology only, with its procedural deviation
(env.py resolving to live instead of the intended scratch) preserved unchanged.

## 6. Adversarial check of the seven pre-existing facts

Each was checked for: right subject, right standard, exact source SHA, verdict,
whether the cited evidence actually satisfies COM-002, scope clarity, duplication,
and N/A-disguised-as-CONFORMS. All seven name a specific compatibility mechanism
and fail-closed behaviour at a specific canonical revision; all carry `CONFORMS /
CLOSED`; subjects are distinct; none is N/A in disguise. **No conflict found; none
reopened.**

## 7. Final nine-target COM-002 completeness matrix

| Subject | Applicability | Compatibility mechanism | Fact? | Verdict | Admitted SHA | Evidence strength | Debt | Action |
|---|---|---|---|---|---|---|---|---|
| watch-clank | APPLICABLE | Alembic head gate, `EXIT_SCHEMA_MISMATCH=3` | **yes (M57)** | CONFORMS | `d03bc4b2` | strong (source + 5 tests + prior adjudication) | D8 resolved | none |
| korean-tech-wire | APPLICABLE | numbered marker, read-only-first barrier | yes | CONFORMS | `354cb7ae` | strong | — | none |
| tablet-clank | APPLICABLE | marker v3 + QC archive v1, fail-closed | yes | CONFORMS | `b3088ebc` | strong | — | none |
| feature-phone-clank | APPLICABLE | read-only-first barrier via `mode=ro` | yes | CONFORMS | `b60e8813` | strong | — | none |
| oem-radar | APPLICABLE | `schema_migrations` v7 + structural manifest | yes | CONFORMS | `79fbee63` | strong | — | none |
| smartwatch-clank | APPLICABLE | monotonic `schema_version` v3 barrier | yes | CONFORMS | `a9335548` | strong | — | none |
| smartphone-clank | APPLICABLE | `ensure_schema_or_refuse` Alembic gate | **yes (M57)** | CONFORMS | `e514c45d` | strong (source + 6 tests + M1 conclusion) | D9 resolved | none |
| chinese-tech-wire | APPLICABLE | `schema_meta` v1, LEGACY_UNADOPTED fails closed | yes | CONFORMS | `c340a45a` | strong | — | none |
| semiconductor-intelligence | APPLICABLE | exact Alembic-head read-only barrier | yes | CONFORMS | `8085a1bb` | strong | — | none |

**Final state: 9 applicable / 9 closed / 0 N/A.** Deployment evidence index:
**18 facts = 9 COM-001 + 9 COM-002.**

## 8. Verdict

**`DEPLOY_COM_002_FLEET_COMPLETE`**

Numerator/denominator: **9 closed / 9 applicable.** The denominator is 9 because
every named target carries persistent structured state under an independently
evolving contract; no target is trigger-unmet. The numerator reached 9 by
admitting two already-concluded, independently re-verified facts — not by
lowering the bar, and not by converting COM-001 or live-migration evidence into
COM-002 proof.

## 9. Scope discipline

Every COM-002 fact, old and new, is scoped to an exact source revision and
asserts a **code property**. None asserts current-canon liveness. M56's finding
that five repositories have moved beyond their COM-001 live proof is unchanged
and unaffected: COM-002 closure says nothing about whether the newest revision
is deployed.

No host action, no deployment, no migration, no source modification, no frozen
standard altered, no COM-001 fact re-scoped, no CUD fact retyped.
