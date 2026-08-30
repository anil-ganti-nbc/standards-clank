# Audits

Records of conformance checks: whether a specific Clank meets specific
ratified standards, as of a specific date. Standards Clank does not run
audits automatically — an audit here is evidence that one was performed,
by whom, and what it found.

No fixed schema for the prose itself; model it on the standard's
`acceptance` criteria and keep it lightweight (what was checked, against
which standard ids, pass/fail/exception, by whom, when).

One structural convention is fixed, though: every audit file MUST open
with a fenced ` ```json ` block, immediately after the title, of the form

```json
{
  "clank": "<clank-name>",
  "date": "YYYY-MM-DD",
  "findings": [
    { "standard": "STD-UI-...", "kind": "violation | conformance | unresolved | not_applicable", "summary": "..." }
  ]
}
```

`tools/ui_agent_layer.py` mechanically parses this block from every
`audits/*.md` file to build
[`../standards/ui/known-evidence-index.json`](../standards/ui/known-evidence-index.json)
(`kind: "violation"` entries only; `conformance`, `unresolved`, and
`not_applicable` findings are recorded but excluded from the index). See
that file's own note on why prior findings are kept structurally separate
from the normative ratified-index/checklist, and
[`../docs/ui/agent-implementation-workflow.md`](../docs/ui/agent-implementation-workflow.md)'s
re-verification clause on how a future agent should (and should not) use
it.

## Supersession

When a later audit replaces a prior audit's assessment of the same Clank,
do not delete the prior file. Keep it verbatim as historical evidence and
add `"superseded_by": "audits/<new-audit>.md"` to its structured block
plus a supersession note in its prose. The generator excludes superseded
blocks from the known-evidence index (and validates that `superseded_by`
points at an existing, non-superseded audit), so the index always
reflects the current assessment. A supersession is a *classification*
event, not an evidence rewrite: the superseded file's findings text stays
untouched. Precedent:
[smartphone-clank-2026-08-30-pass1.md](smartphone-clank-2026-08-30-pass1.md)
superseded by
[smartphone-clank-2026-08-30.md](smartphone-clank-2026-08-30.md) via
[decisions/0005](../decisions/0005-qc-applicability-refinement.md).
