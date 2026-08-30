# Exceptions

An exception is a recorded, auditable deviation from a ratified standard for
a specific Clank. Each exception is one JSON file conforming to
[../schemas/exception.schema.json](../schemas/exception.schema.json).

Suggested filename: `<standard_id>--<clank>.json` (e.g.
`STD-UI-COM-001--watch-clank.json`).

## Statuses

`PROPOSED -> APPROVED | REJECTED`, and later `EXPIRED` or `SUPERSEDED`.

## The approval restriction

**Agents may propose exceptions. Agents may not approve their own
exceptions.** `approved_by` must name a human operator, and the schema
requires it whenever `status` is `APPROVED`. This mirrors the ratification
restriction in [../docs/governance.md](../docs/governance.md).

Exceptions must be visible and auditable — they live in this directory in
plain text, not hidden in a database or a private note.
