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

No profiles are populated yet. Anticipated initial profiles, based on the
current fleet:

- `news-based`
- `sku-based`
- `product-discovery`
- `specialist-news`
- `regional-catalogue`
- `support-source`

Populating these against real Clanks (watch-clank, oem-radar,
semiconductor-intelligence, chinese-tech-wire, korean-tech-wire,
feature-phone-clank, smartphone-clank, smartwatch-clank, tablet-clank) is
future work, not part of this repository's initial groundwork.
