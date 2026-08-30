---
id: canonical-fact-overwrite-discipline
domain: data-ontology
clusters: [D]
confidence: STRONG
priority: MEDIUM
---

# Overwrite Policy for Canonical Facts Is Inconsistent, Even Within One Repo

## Concern

When a new observation disagrees with (or is missing where) an existing
canonical fact, does the new observation overwrite it, get ignored, or
merge? Most repos have a policy, but it is not always applied
consistently across all fields in the same table, and the policy is
rarely stated as an explicit, testable contract.

## Current terminology

COALESCE-preserve-non-null (chinese-tech-wire, korean-tech-wire),
fill-if-empty/first-writer-wins (smartphone-clank), append-only-never-
mutate (feature-phone-clank, oem-radar snapshots), in-place-mutate
(tablet-clank `products` table), never-overwrite-first_seen
(smartwatch-clank).

## Repos surveyed

All nine fleet Clanks. See [terminology-map.md](../terminology-map.md)'s
"Observation vs. canonical fact — overwrite policy" table for the full
per-repo comparison.

## Independent evidence

Every repo has *a* policy; no two repos have exactly the same one, and
the policies cluster into genuinely different architectural families
(append-only-ledger-underneath-immutable-identity vs.
mutate-in-place-with-a-separate-change-log vs. first-writer-wins). This
diversity appears legitimate rather than accidental — feature-phone-clank's
strict append-only design and tablet-clank's in-place-mutation design
solve the same problem with different tradeoffs (write simplicity vs.
audit purity), and neither is described in either repo's docs as wrong.

## Inherited evidence

None found — each repo's policy appears independently derived.

## Incidents

**korean-tech-wire's own internal inconsistency is the most concrete
finding here**: enrichment fields (`body_original`, `author`, `category`,
`published_at`) use COALESCE-preserve-non-null on conflict-UPDATE, but
`title_original`/`title_normalized`/`content_hash`/`raw_metadata` on the
*same row* are unconditionally overwritten (latest-wins) — this
inconsistency exists in code but is not documented anywhere as a
deliberate contract, meaning it's plausibly an oversight rather than a
choice. No downstream incident was confirmed to have resulted from it,
but it's a live, unexamined risk. smartphone-clank's fill-if-empty policy
has an admitted latent risk (an incorrect early value can never be
corrected by a later, better source) that is not flagged anywhere in its
own docs.

## Implementations

Widely varied, each internally coherent except for the KTW inconsistency
noted above.

## Counterexamples

feature-phone-clank vs. tablet-clank is a genuine, reasoned counterexample
pair (see [terminology-map.md](../terminology-map.md)) — two Clanks
solving the identical problem (product spec observation) with opposite
canonical-mutation policies, both apparently working fine for their
respective use cases.

## Harm if violated

No confirmed incident traces directly to this specific concern (as
distinct from the identity/dedup and baseline incidents already covered
elsewhere) — this cluster is evidence of *inconsistency*, not of
*demonstrated harm*, which is why its priority is MEDIUM rather than HIGH.

## Likely domain

Data/ontology — but this may be a case where standardizing the *policy*
is wrong (see decisions/0001's "standardize contracts not implementation"
principle, itself from the UI domain but the same reasoning likely
applies) and standardizing only the *documentation requirement* ("state
your overwrite policy explicitly, per field, in one place") is the right
level.

## Unresolved questions

1. Is there harm in leaving overwrite policy as an implementation detail,
   provided it's documented? Or does cross-Clank consistency matter here
   (e.g. for a future cross-Clank identity/fusion effort per
   [cross-clank-fleet-identity.md](cross-clank-fleet-identity.md))?
2. Should korean-tech-wire's internal inconsistency be reported back as a
   remediation candidate (out of scope for this evidence-only pass), or
   left for Pass 0B to flag?

## Confidence: STRONG
## Adjudication priority: MEDIUM
