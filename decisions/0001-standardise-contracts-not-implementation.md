# 0001 — Standardise contracts, not implementation technology

Date: 2026-08-30
Status: Accepted

## Decision

Standards Clank standardises contracts, invariants, semantics, and
observable behaviour across the Clank fleet. It does not standardise
programming language, framework, database engine, hosting provider, or
other internal implementation details.

## Rationale

The fleet's Clanks are independent repositories that have each made
reasonable, sometimes different, implementation choices. Forcing
implementation uniformity would create unnecessary migration cost without
improving reliability or auditability. What actually matters — whether a
collector is manually triggered, whether QC actions are transactional and
provenance-tracked, whether events distinguish FIRST_SEEN from editorial
novelty — is observable regardless of implementation.

## Consequence

A standard's `acceptance` criteria (see
[../schemas/standard.schema.json](../schemas/standard.schema.json)) must be
checkable from outside the implementation. A proposal that only makes sense
by mandating a specific library, framework, or database should be
rejected or rewritten as a contract-level requirement instead.

See [../docs/charter.md](../docs/charter.md) section D.
