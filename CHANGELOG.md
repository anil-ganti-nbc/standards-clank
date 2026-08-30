# Changelog

Tracks ratifications and normative changes to standards, plus notable
changes to this repository's own governance/schemas. See
[docs/standards-lifecycle.md](docs/standards-lifecycle.md) for what counts
as normative vs. editorial.

## Unreleased

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
