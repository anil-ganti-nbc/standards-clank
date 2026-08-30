# 0006 — STD-UI-COM-009 "equivalent structured record" interpretation

Date: 2026-08-30
Status: Accepted (operator review, 2026-08-30)
An agent MUST NOT ratify standards unassisted (see
[0002-no-agent-self-ratification.md](0002-no-agent-self-ratification.md));
the interpretation below was accepted by the operator in the review
recorded at the end of this document.

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

## Operator review — ACCEPTED (2026-08-30)

The operator reviewed this proposal and accepted the interpretation,
stating the boundary precisely:

- **STD-UI-COM-009 applies when the system preserves materially distinct
  pipeline-phase outcomes at the level of an individual run.** A formal
  ordered stage ledger is sufficient but not required. Per-run
  phase-attributable fields — fetch failures, parse failures, validation
  outcomes, regression notes, or equivalent structured state — qualify.
  Aggregate/windowed health counters by themselves do not.
- **smartphone-clank's `CollectorRunRecord` qualifies.** That the record
  is flat rather than an ordered ledger does not matter if it preserves
  fetch-vs-parse-vs-overall-run distinctions for a specific run. The
  verdict is therefore **FAIL** — not N/A, not PARTIAL: the information
  exists in structured per-run state, but the operator cannot reach the
  corresponding run detail from the Runs/metrics surface.
- **Recorded operator principle:** applicability should follow the
  granularity of preserved evidence, not the shape of the schema. A flat
  per-run record can carry just as much pipeline truth as a formal stage
  ledger.
- **Second ruling in the same review:** the absent smartphone-clank QC
  GUI is tracked as **product/remediation backlog**, explicitly NOT a
  `STD-UI-COM-003`/`STD-UI-COM-004` violation. "Standards-compliant"
  does not mean "feature-complete", and conditional standards must not
  be distorted to express a desired operator workflow. COM-003/004
  remain N/A per [0005](0005-qc-applicability-refinement.md); the
  non-normative backlog record lives in the smartphone audit.

Actions executed under this acceptance: `STD-UI-COM-009` revised to v3
(requirement/acceptance/forbidden encode the boundary, nothing more);
smartphone audit COM-009 updated to FAIL with the prior
PARTIAL/unresolved state preserved in its history; agent-facing layer and
known-evidence index regenerated from the generator. No remediation of
any Clank was performed or authorized.
