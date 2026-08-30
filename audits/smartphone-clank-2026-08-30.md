# smartphone-clank — conformance note, 2026-08-30

```json
{
  "clank": "smartphone-clank",
  "date": "2026-08-30",
  "findings": [
    { "standard": "STD-UI-COM-002", "kind": "violation", "summary": "qc-action writes a plain INSERT into the live analyst_actions table: no separate append-only decision record, no uniqueness constraint, no documented race handling." },
    { "standard": "STD-UI-COM-003", "kind": "violation", "summary": "No dashboard QC queue exists at all, so there is no read-side exclusion mechanism to evaluate; same root cause as the STD-UI-COM-002 gap." },
    { "standard": "STD-UI-COM-004", "kind": "violation", "summary": "No 'recently QC'd' view exists, consistent with having no QC queue or archive to source it from." }
  ]
}
```

This block is machine-read by `tools/ui_agent_layer.py` to build
[`standards/ui/known-evidence-index.json`](../standards/ui/known-evidence-index.json) —
see that file's own note on why prior findings are kept structurally
separate from the normative ratified-index/checklist.

Checked against: `STD-UI-COM-002`, `STD-UI-COM-003`, `STD-UI-COM-004`
(all `RATIFIED` as of
[decisions/0003-operator-ratification-decision-001.md](../decisions/0003-operator-ratification-decision-001.md))

Result: **does not conform**, by design decision, not oversight —
recorded as a remediation-backlog item, not an exception.

## What was found (GUI Ratification Pass 1 evidence)

smartphone-clank's only QC mechanism is the CLI `qc-action` command
(`main.py:1227-1262`), which writes a plain `INSERT` directly into the
live `analyst_actions` table:

- No separate append-only decision record distinct from the live table
  (fails `STD-UI-COM-002`).
- No uniqueness constraint or documented handling for a concurrent
  double-decision (fails `STD-UI-COM-002`).
- No dashboard QC queue at all, so no read-side exclusion of decided items
  exists to evaluate (`STD-UI-COM-003` is not applicable in the literal
  sense — there is no active queue to remove an item from — but the
  underlying gap, no queue-vs-decision separation, is the same root cause
  as the COM-002 failure).
- No "recently QC'd" view (fails `STD-UI-COM-004`, which is conditional on
  having a QC queue exposed at all — this Clank exposes none).

## Disposition

Per [decisions/0003](../decisions/0003-operator-ratification-decision-001.md),
the operator explicitly declined to file an exception for this gap:

> Exceptions should be for cases where compliance is genuinely
> inappropriate, not where a Clank predates the standard.

This is recorded as a **remediation-backlog target**, following the
intended Standards Clank flow:

```
existing implementation -> ratified standard -> conformance audit -> remediation backlog
```

## What this note does NOT do

It does not authorize or schedule remediation work. No code in
smartphone-clank was touched to produce or as a result of this note.
Applicability of `STD-UI-COM-003`/`004` against smartphone-clank's actual
Motherclank-integrated workflow should be confirmed before remediation
work is scoped, since that Clank's QC surface is architecturally different
(CLI write-through, not a GUI queue) from every other surveyed Clank.
