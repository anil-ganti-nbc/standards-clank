# Profiles

A profile identifies a class of Clank and which standards apply to it.
Standards do not always apply fleet-wide — a `sku-based` Clank and a
`news-based` Clank have different collector and classification concerns.

Each profile is one JSON file conforming to
[../schemas/profile.schema.json](../schemas/profile.schema.json), named
after its `id` (e.g. `news-based.json`).

A profile may `inherit` from another profile to pick up shared standards
plus its own family-specific ones. Keep inheritance shallow — one level is
expected; do not build deep inheritance chains.

The populated, governance-only fleet adoption registry is
`profiles/fleet-adoption.json`.  Profiles select family candidates; they do
not by themselves satisfy conditional standard triggers.  Unknown architecture
facts remain `UNKNOWN`, never silently become false or N/A. The resolver reads
immutable baseline tags, not mutable `master`.

The initial supported profiles are:

- `news-based`
- `sku-based`
Use `python scripts/resolve_clank_standards.py watch-clank --audit-plan` to
generate a blind audit plan. It resolves applicability only and makes no
conformance claim.
