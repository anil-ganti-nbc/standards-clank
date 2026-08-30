# Agent Implementation Workflow

This is the required sequence for an agent building or auditing a Clank
GUI against Standards Clank's ratified UI standards. It complements
[constitution.md](constitution.md) (what the rules require) with *how* to
apply them safely. Follow the steps in order; do not skip to step 9
(implementation) without having produced the report in step 4.

This workflow only ever authorizes conformance work against **RATIFIED**
standards. `PROPOSED` standards are identified and set aside at step 7 —
never implemented, never treated as a requirement.

## Two modes: blind audit vs. informed remediation

There are two ways to run this workflow, and the choice of which one
matters:

```
BLIND AUDIT                        INFORMED REMEDIATION
constitution                       constitution
+ ratified-index                   + ratified-index
+ checklist                        + checklist
                                    + known-evidence-index.json
                                      (see below)
```

**Blind audit** — the default. Load only
[`constitution.md`](constitution.md),
[`ratified-index.json`](../../standards/ui/ratified-index.json), and
[`agent-checklist.json`](../../standards/ui/agent-checklist.json). Do
**not** load
[`known-evidence-index.json`](../../standards/ui/known-evidence-index.json)
or read `audits/*.md` before forming your own conclusions. This is how a
fresh conformance audit (e.g. a task explicitly asking you to validate a
Clank against the standards) should run: it independently reproduces
findings rather than being told in advance what to expect, which is the
only way a validation audit's result actually means anything. Standards
Clank's first blind audit (watch-clank, 2026-08-30 —
[`audits/watch-clank-2026-08-30.md`](../../audits/watch-clank-2026-08-30.md))
worked exactly this way.

**Informed remediation** — once a task has explicitly moved past auditing
into planning or implementing a fix, you MAY additionally load
`known-evidence-index.json` to save time re-discovering already-known
gaps. If you do, the following rule applies without exception:

> **Prior audit findings and standard `notes` are hypotheses, not
> current-state truth. When used, they MUST be re-verified against the
> target's current implementation before being reported as a present
> non-conformance.** Code changes since the prior finding, a since-applied
> partial fix, or a plain error in the earlier finding can all make a
> stale "known" violation wrong. Never cite `known-evidence-index.json` or
> a standard's `notes` field as evidence in a conformance report on its
> own — cite the current file:line you verified it against.

`known-evidence-index.json` is generated (see
`tools/ui_agent_layer.py`'s `build_known_evidence_index()`) from the
structured findings block at the top of every `audits/*.md` file. It is
deliberately kept as a separate file, not merged into
`ratified-index.json` or `agent-checklist.json` — see that file's own
note for why contaminating the normative layer with per-Clank history
would defeat the point of a blind audit.

## The sequence

1. **Identify Clank family.** Determine whether the target Clank is
   `sku-based`, `news-based`, both (a genuine hybrid, like watch-clank), or
   neither cleanly. Check
   [`profiles/sku-based.json`](../../profiles/sku-based.json) and
   [`profiles/news-based.json`](../../profiles/news-based.json) for the
   current member list, but verify against the Clank's actual collected
   content — profile membership can be wrong or stale.

2. **Read applicable ratified standards.** Start from
   [`standards/ui/ratified-index.json`](../../standards/ui/ratified-index.json)
   for the compact list, but read the full `standards/ui/<ID>.json` file
   for every standard that could plausibly apply — the index's
   `requirement_summary` is for orientation, not for citing as the
   authoritative text. Fleet-wide standards (`applies_to: []`) apply to
   every Clank; family-scoped standards (`applies_to: ["news-based"]`,
   etc.) apply only to that family. If, and only if, this is an informed
   remediation task (see "Two modes" above), you may also load
   `known-evidence-index.json` here — a blind audit does not.

3. **Inventory current UI and backend semantics relevant to those
   standards.** For each applicable standard, find and read the actual
   code: the collector-trigger routes, the QC-decision write path, the
   queue query, the health/coverage computation, the run-status model, the
   timestamp-formatting helpers, the delivery-outcome model. Do not infer
   conformance from a page's visual appearance — read the underlying query
   and write logic, per the constitution's warning against treating
   backend requirements as cosmetic.

4. **Produce a pre-code conformance report.** See the required structure
   below. This is a deliverable, not a mental note — write it down before
   touching any code.

5. **Identify specialist workflows that must be preserved.** A Clank may
   have Clank-specific surfaces, extra QC action values, or workflow
   variations that are not violations (see constitution section J,
   "Specialist flexibility") — list them explicitly so a later
   implementation step doesn't accidentally normalize them away.

6. **Identify existing violations.** Cross-reference the inventory (step
   3) against each applicable ratified standard's `acceptance` criteria.
   Be specific: cite the file/line that fails, and which standard it
   fails. If a violation traces back to `known-evidence-index.json` or a
   standard's own `notes` field (informed remediation only — see "Two
   modes" above), it must still be re-verified against the current code
   before being reported; cite what you verified, not the prior finding.

7. **Identify PROPOSED standards separately from RATIFIED standards.**
   List anything relevant that is still `PROPOSED` (see the constitution's
   "Pending / Not Yet Normative" section) in its own clearly separate part
   of the report. Do not fold these into the violations list — a Clank
   cannot violate a standard that isn't ratified.

8. **Propose remediation.** For each violation found in step 6, propose
   what would fix it. A remediation proposal is not authorization to
   implement it.

9. **Implement only after operator/task authorization.** Do not write code
   against this workflow's findings until a human operator, or the task
   that invoked this workflow, has explicitly authorized implementation.
   Producing the report (steps 1-8) does not itself authorize step 9.

10. **Run conformance tests.** After implementing an authorized
    remediation, verify it against the relevant standard's `acceptance`
    criteria and this Clank's own test suite. Use
    [`standards/ui/agent-checklist.json`](../../standards/ui/agent-checklist.json)
    as a quick self-check, but the checklist's yes/no questions are a
    coarse proxy for the full `acceptance` list — passing the checklist
    question does not by itself prove full conformance.

11. **Report remaining violations and proposed exceptions.** If full
    conformance wasn't reached (or wasn't authorized), report exactly what
    remains non-conformant and, where relevant, propose an exception per
    [`exceptions/README.md`](../../exceptions/README.md).

12. **Never self-approve exceptions.** An agent may propose an exception.
    An agent MUST NOT set an exception's `status` to `APPROVED` — that
    field requires a human `approved_by`, enforced by
    [`schemas/exception.schema.json`](../../schemas/exception.schema.json).
    This mirrors the same restriction on standards ratification itself
    (see [`docs/governance.md`](../governance.md) and
    [decisions/0002](../../decisions/0002-no-agent-self-ratification.md)).

## Pre-code conformance report — required structure

Every report produced at step 4 must contain all of the following
sections, even if a section is empty (say so explicitly rather than
omitting it):

- **Clank family** — sku-based / news-based / hybrid / unclear, with the
  evidence for that classification.
- **Applicable RATIFIED standards** — the specific `STD-UI-*` ids that
  apply to this Clank, with why (fleet-wide, or family-matched).
- **Current conformances** — which applicable standards this Clank
  already satisfies, with the file/line evidence.
- **Current violations** — which applicable standards this Clank does not
  satisfy, with the file/line evidence and which specific `acceptance`
  criterion fails.
- **Standards that are N/A** — applicable-looking standards that don't
  actually apply because the underlying concept is absent (e.g.
  `STD-UI-COM-005`/`006` for a Clank with no experimental/production
  maturity tier at all) — see constitution section J2. State why, not just
  that it's N/A.
- **Specialist surfaces to preserve** — Clank-specific pages, extra QC
  actions, or workflow variations identified in step 5 that must not be
  removed or normalized away by a later remediation pass.
- **Files expected to change** — a concrete list, even if step 9 hasn't
  happened yet.
- **Proposed exceptions** — any violation where full conformance may be
  genuinely inappropriate for this Clank (not merely inconvenient or
  predating the standard — see
  [`exceptions/README.md`](../../exceptions/README.md) and the operator's
  own stated policy in
  [decisions/0003](../../decisions/0003-operator-ratification-decision-001.md):
  "exceptions should be for cases where compliance is genuinely
  inappropriate, not where a Clank predates the standard").
- **Unresolved semantic questions** — anything the report author is
  genuinely unsure how a standard applies to this Clank's specific
  situation. Surface these; do not guess silently.

## Worked example of the family/N/A distinction

smartphone-clank is `sku-based` but has no QC-queue UI at all — per
[`audits/smartphone-clank-2026-08-30.md`](../../audits/smartphone-clank-2026-08-30.md),
this is a recorded **violation** of `STD-UI-COM-002`/`003`/`004` (a
remediation-backlog item, not an exception), not an N/A case — the concept
(a QC decision needing to be atomic and queue-excluding) plainly applies
to a Clank that reviews leaks; it's simply not implemented yet. Contrast
this with chinese-tech-wire, which has no experimental/production
maturity-tier concept at all — `STD-UI-COM-005`/`006` are genuinely N/A
there, per constitution J2, because the concept those standards govern
doesn't exist in that Clank's architecture.
