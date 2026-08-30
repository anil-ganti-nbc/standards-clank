# 0005 — QC standards applicability refinement (from the second blind validation)

Date: 2026-08-30
Status: Accepted (operator-commissioned interpretation pass; no normative text changed)
Evidence base: the second fresh-agent blind validation of smartphone-clank at
smartphone-clank HEAD `09923e7`, recorded in
[../audits/smartphone-clank-2026-08-30.md](../audits/smartphone-clank-2026-08-30.md).
Supersedes the *classification* in
[../audits/smartphone-clank-2026-08-30-pass1.md](../audits/smartphone-clank-2026-08-30-pass1.md)
(preserved verbatim as historical evidence).

## Why this pass happened

The second blind validation validated the compact agent layer across a
materially different architecture (a CLI/migration-heavy monitoring Clank
rather than a GUI-queue review Clank), and in doing so exposed four
layer-level issues:

1. The pass-1 smartphone audit classified `STD-UI-COM-003`/`004` as
   violations, while the RATIFIED rule text makes them N/A when no
   operator QC/review queue surface exists.
2. A GUI-first inventory can miss backend/operator decision paths —
   smartphone-clank's only QC path is the CLI `qc-action` command writing
   an `analyst_actions` table that is created in a raw-SQL migration, is
   referenced nowhere in the GUI, models, or templates, and is consumed
   externally (by Motherclank) rather than by this Clank's own UI.
3. `STD-UI-COM-009` has an unresolved applicability question ("equivalent
   structured record") — handled separately in
   [0006](0006-com009-equivalent-structured-record.md).
4. Surface names can mislead applicability analysis: smartphone-clank's
   "Device queue" page is a canonical catalogue, not an operator QC queue.

## Interpretation (under the unchanged ratified wording)

- **STD-UI-COM-003**: if there is no active operator QC/review queue
  surface, classify **N/A** rather than FAIL merely because such a queue
  does not exist. The rule constrains how a decided item leaves a queue;
  with no queue semantics there is nothing to conform or fail.
- **STD-UI-COM-004**: if the GUI exposes no operator QC queue and the
  standard's explicit "if, and only if" trigger is unmet, classify
  **N/A**.
- **STD-UI-COM-002**: applies to an operator decision path even when that
  path is CLI-only or otherwise outside the current GUI. The ratified
  rule contains an underlying decision-contract requirement *and* a UI
  truthfulness clause; the absence of a GUI success toast does not make
  an unsafe decision-write contract conformant. COM-002 is NOT weakened
  to "only applies when a visible button exists".
- Absence of a QC GUI may still be a product limitation, a backlog item,
  or a future design opportunity — but it is NOT automatically a
  standards violation under these current ratified rules. Record such
  gaps as backlog observations, not violations.

## Classification refinement, not evidence falsification

The pass-1 audit's factual observations (CLI-only `qc-action`, raw
INSERT, no uniqueness constraint, no QC queue, no history view) were
confirmed by the second validation against current HEAD. Only its
COM-003/004 classification changed: violation → N/A, under the standards'
own conditional wording. The pass-1 file is preserved verbatim with an
explicit `superseded_by` marker that excludes it from the generated
known-evidence index; the current assessment is the second-validation
audit.

## Effect on the agent layer

- `docs/ui/agent-implementation-workflow.md`: new "Applicability:
  semantics and behaviour, not labels" section (underlying action
  contracts vs queue-surface standards); step 3 now requires inventorying
  operator-relevant backend mutation paths even when GUI-unexposed; the
  worked example was updated to the refined classification.
- `tools/ui_agent_layer.py`: COM-002's requirement summary and checklist
  entry were sharpened to state the path-agnostic applicability above;
  `ratified-index.json` and `agent-checklist.json` were regenerated from
  the generator (not hand-edited).
- `docs/ui/constitution.md` is intentionally unchanged: its authority
  rule reserves it for ratified, cited requirements; audit methodology
  lives in the workflow.

## Self-ratification check

No standard was created, revised, ratified, or retired by this decision.
The RATIFIED set remains 12 and the PROPOSED set remains 3
(STD-UI-COM-007, STD-UI-COM-012, STD-UI-SKU-001).
`standards/ui/STD-UI-COM-009.json` is untouched; its open interpretation
question is separately proposed, and explicitly not decided, in
[0006](0006-com009-equivalent-structured-record.md).
