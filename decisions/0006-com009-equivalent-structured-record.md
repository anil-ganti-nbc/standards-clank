# 0006 — STD-UI-COM-009 "equivalent structured record" interpretation (PROPOSAL)

Date: 2026-08-30
Status: Proposed — awaiting operator review. NOT ratified. No normative
text has been changed; `standards/ui/STD-UI-COM-009.json` is untouched.
An agent MUST NOT ratify this proposal (see
[0002-no-agent-self-ratification.md](0002-no-agent-self-ratification.md)).

## Question

Does `STD-UI-COM-009` apply when the backend does not model an explicit
ordered stage ledger or stage field, but does record stage-attributable
outcome/counter fields such as:

- HTTP/fetch failures,
- parser failures,
- overall per-run status (e.g. success/partial/degraded/unexpected_zero/failed/blocked),
- regression notes,

associated with individual runs?

## Proposed interpretation (for operator review)

"Equivalent structured record" SHOULD mean a backend record that
preserves materially distinct pipeline-phase outcomes **in a way the
system can associate with a specific run**.

- Per-run, phase-attributable counters/status fields **likely qualify** —
  the trigger is met.
- Aggregate counters by category across a time window **do not** trigger
  COM-009 on their own.

Rationale: the standard's purpose is that the operator can act on *which
phase* went wrong for a *specific run* when the backend already knows.
Phase knowledge that exists only in aggregate cannot change what an
operator does about a particular run, so it should not trigger the
run-surface obligations.

## Applied to smartphone-clank (pending this proposal)

smartphone-clank's `CollectorRunRecord`
(`observability/metrics.py:34-68` in smartphone-clank at HEAD `09923e7`)
is an immutable per-run row carrying phase-attributable counters
(`http_failures`, `parser_failures`), a per-run status enum, and per-run
regression notes — but no stage field or stage-ordered ledger.

Under the proposed reading, the trigger **is met**, and the audit verdict
would become **FAIL**: the primary run surface (`/metrics`) indicates that
per-run detail exists (the subtitle advertises "regression notes in run
records") but provides no direct, discoverable path to any run record —
no route exposes per-run data at all.

If the operator rejects the reading (only window-aggregate semantics
count, or per-run outcome rows are not "stages"), the trigger is **unmet**
and the verdict becomes **N/A**.

Until the operator decides, the smartphone-clank audit records
`STD-UI-COM-009` as **PARTIAL / unresolved**.

## Constraints

- This decision proposes an interpretation; it does not rewrite
  `STD-UI-COM-009.json`. If the operator accepts it, the wording should
  be folded into the standard through the normal revision/versioning
  path (a v3 with recorded review), not by editing this repository's
  generated or agent-facing layers around it.
- If the operator accepts the interpretation as-is, the smartphone-clank
  audit's COM-009 verdict should be updated from PARTIAL/unresolved to
  FAIL in the *audit* (evidence layer), not silently in the standard.
