# Changelog

Tracks ratifications and normative changes to standards, plus notable
changes to this repository's own governance/schemas. See
[docs/standards-lifecycle.md](docs/standards-lifecycle.md) for what counts
as normative vs. editorial.

## Unreleased

- Operator Ratification Decision 002 (2026-08-30): ratified 5 of the 6 GUI
  Ratification Pass 2 candidates — STD-UI-COM-008/009/010/011 and
  STD-UI-NEWS-002, each ratified with a wording clarification (v2):
  COM-008 requires semantic separation not separate pages; COM-009
  requires stage detail to be discoverable, not merely technically
  present (an unlinked drill-down does not satisfy it); COM-010 allows a
  stated page-level timezone convention instead of per-cell repetition,
  and was ratified despite an 8/9 remediation footprint on the explicit
  reasoning that the footprint is evidence of debt, not evidence against
  the principle; COM-011 no longer requires a dedicated Delivery page;
  NEWS-002 softened from "must be the default view" to reachable directly
  or via one obvious action. Returned STD-UI-COM-012 for revision
  (rewritten as "primary workflow must not imply unobserved health", v2,
  still PROPOSED) rather than ratifying the weaker original. Confirmed no
  rule is created for STD-UI-SKU-002. See
  [decisions/0004-operator-ratification-decision-002.md](decisions/0004-operator-ratification-decision-002.md).
  Ratification does not itself authorize any remediation work.

- GUI Ratification Pass 2 (2026-08-30): added 6 `PROPOSED` candidate
  standards (STD-UI-COM-008..012, STD-UI-NEWS-002) covering navigation,
  Overview semantics, source health vs. coverage, run-stage observability,
  timestamps/timezones, and delivery visibility. Explicitly declined to
  draft a `STD-UI-SKU-002` counterpart — evidence didn't support it. See
  [docs/gui-ratification-pass-2.md](docs/gui-ratification-pass-2.md). No
  status was set to REVIEWED or RATIFIED; none of these have been reviewed
  by the operator yet.

- Operator Ratification Decision 001 (2026-08-30): ratified 7 of the 9 GUI
  Ratification Pass 1 candidates — STD-UI-COM-001, STD-UI-COM-002 (v2,
  normative addition), STD-UI-COM-003 (editorial), STD-UI-COM-004
  (editorial), STD-UI-COM-005, STD-UI-COM-006, STD-UI-NEWS-001. Returned
  STD-UI-COM-007 and STD-UI-SKU-001 for revision (both rewritten, v2,
  still PROPOSED). No rule was rejected. Recorded smartphone-clank's
  non-conformance to COM-002/003/004 as a remediation-backlog item, not an
  exception, per explicit operator instruction. See
  [decisions/0003-operator-ratification-decision-001.md](decisions/0003-operator-ratification-decision-001.md)
  and [audits/smartphone-clank-2026-08-30.md](audits/smartphone-clank-2026-08-30.md).
  Ratification does not itself authorize any remediation work.

- GUI Ratification Pass 1 (2026-08-30): added 9 `PROPOSED` (not ratified)
  candidate standards under `standards/ui/` (STD-UI-COM-001..007,
  STD-UI-SKU-001, STD-UI-NEWS-001), evidence-backed from a read-only survey
  of all nine fleet Clanks plus `clank-architecture` (read for evidence
  only, not modified). Populated `profiles/sku-based.json` and
  `profiles/news-based.json` with real member Clanks. See
  [docs/gui-ratification-pass-1.md](docs/gui-ratification-pass-1.md) for
  the ratification table and open items. No status was set to REVIEWED or
  RATIFIED.

- Initial repository groundwork: charter, governance model, standard/
  profile/exception/evidence-reference schemas, domain scaffolding under
  `standards/`, GitHub issue/PR templates, and repository-contract tests.
  No standards ratified. See
  [decisions/0001-standardise-contracts-not-implementation.md](decisions/0001-standardise-contracts-not-implementation.md)
  and
  [decisions/0002-no-agent-self-ratification.md](decisions/0002-no-agent-self-ratification.md).
