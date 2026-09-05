# Watch DEPLOY-COM-002 admission — M57 evidence-model repair (2026-09-05)

```json
{"clank":"watch-clank","date":"2026-09-05","findings":[{"standard":"STD-DEPLOY-COM-002","kind":"conformance","summary":"CONFORMS / CLOSED at canonical Watch main revision d03bc4b2f90289686331af0447d5ca4e8cf55822 (historical exact-source scope; no current-canon claim): app/db/schema_check.py compares the database's Alembic version against the code's single expected head and never applies migrations nor lazily creates tables, and scripts/run_pipeline.py enforces it as a startup barrier before any collection work is admitted — on any mismatch, including a genuinely fresh/uninitialized database with no alembic_version table, it logs structured schema_mismatch(expected, actual), prints the identifying refusal, raises a health alert and returns the dedicated EXIT_SCHEMA_MISMATCH=3 documented as 'migration / database failure -- schema does not match the code's expected Alembic head'; migration is reachable only through the separate explicit scripts/migrate.py. tests/test_schema_check.py covers fresh-uninitialized non-match, at-head match, older-revision non-match (002_ops_statuses vs head 015_qualification_reset_lineage), run_pipeline refusal with EXIT_SCHEMA_MISMATCH, and the health-alert path. Admission records the existing M4-series adjudication (audits/watch-clank-cross-domain-2026-09-01-reaudit.json: APPLIES/CONFORMS, evidence 'schema compatibility preflight and tests/test_schema_check.py'), carried as STILL_CONFORMS in audits/watch-clank-cross-domain-2026-09-01-final.json, which was never encoded into the machine-readable graph because the generator reads the .md findings block and the verdict lived in the .json companion. Resolves M56 debt D8."}]}
```

**Classification: `WATCH_COM002_RECORDING_DEFECT`.**

This artifact admits an existing, already-concluded fact into the machine-readable
evidence graph. It creates no new proof, performs no host or source action, and
makes **no claim about current Watch canon**.

## Why this is a recording defect, not a new determination

M56 recorded debt D8: Watch's COM-002 CONFORMS appeared in the final audit's
prose table (`| STD-DEPLOY-COM-002 | Deployment | APPLIES | CONFORMS | M4G
closure unchanged |`) but not in the machine-readable graph.

Tracing that prose to its actual source, per M57 §6 (no evidence laundering):

1. The prose cites "M4G closure unchanged". **M4G is not the origin.**
   `audits/watch-clank-cross-domain-2026-09-01-reaudit-4.md` is titled *"M4G
   final OPS-COM-003 closure re-audit"*, carries an empty `findings` block, is
   `superseded_by` the final audit, and mentions the compatibility barrier only
   as *present* — it did not adjudicate DEPLOY-COM-002. Had the chain ended
   there, D8 would have remained unresolved.
2. The actual adjudication is machine-readable and earlier:
   `audits/watch-clank-cross-domain-2026-09-01-reaudit.json` line 34 —
   `{"id":"STD-DEPLOY-COM-002","applicability":"APPLIES","state":"CONFORMS",
   "evidence":"schema compatibility preflight and tests/test_schema_check.py;
   013 head is included"}`.
3. It is carried forward as `"state": "CONFORMS", "regression":
   "STILL_CONFORMS"` in `audits/watch-clank-cross-domain-2026-09-01-final.json`
   line 50.

The omission is mechanical: `tools/deployment_agent_layer.py` builds the index
from the leading ```json **findings** block of each `audits/*.md`. Watch's
COM-002 verdict lived in the `.json` companion under a different key shape
(`{"id":…,"state":…}`), which that generator does not and should not read.

## Independent verification against frozen COM-002

Per §6 the prose was **not** taken at face value. The cited evidence was read
directly from Watch source at the exact SHA `d03bc4b2f902…`, read-only via the
GitHub contents API.

| Frozen COM-002 element | Evidence at `d03bc4b` | Result |
| --- | --- | --- |
| Trigger: persistent structured state, independently evolving contract | SQLite under an Alembic revision chain (head `015_qualification_reset_lineage`) | **APPLICABLE** |
| Barrier before normal incompatible work is accepted | `scripts/run_pipeline.py` calls `check_schema(get_engine())` immediately after settings resolution and before any collector work | **Satisfied** |
| Fail closed on known incompatibility | `if not schema.matches: … return EXIT_SCHEMA_MISMATCH` (exit code 3) | **Satisfied** |
| Refuses fresh/uninitialized state too | `_actual_version` returns `None` when `alembic_version` is absent; `None != expected` → refuse. Module docstring: *"refuses to run on any mismatch -- including a completely fresh, uninitialized database"* | **Satisfied** |
| Evidence identifying compatibility gating as the cause | dedicated exit code 3 documented as schema/migration failure; `logger.error("schema_mismatch", expected=…, actual=…)`; printed refusal naming both revisions; Discord health alert | **Satisfied** |
| Must not rest on forbidden proxies (`create_all`, table existence, connectivity, deploy-command success) | *"never applies migrations automatically and never lazily creates tables"*; migration only via explicit `scripts/migrate.py` | **Satisfied** |

`tests/test_schema_check.py` at the same SHA covers
`test_fresh_uninitialized_db_does_not_match`, `test_db_at_head_matches`,
`test_db_at_older_revision_does_not_match`,
`test_run_pipeline_refuses_on_schema_mismatch` (asserting
`EXIT_SCHEMA_MISMATCH`), and
`test_run_pipeline_sends_health_alert_on_schema_mismatch`.

## Scope discipline

- Scoped to historical exact source `d03bc4b2f90289686331af0447d5ca4e8cf55822`.
- **No current-canon claim.** Watch canon has since moved (+9 commits as observed
  at M56); this admission says nothing about whether the newest revision is
  deployed or about COM-001 congruence, which M56 classified
  `CANON_MOVED_PROOF_STILL_VALID_HISTORICALLY`.
- COM-001 is untouched. The prose artifacts are left as written; original
  chronology preserved.
