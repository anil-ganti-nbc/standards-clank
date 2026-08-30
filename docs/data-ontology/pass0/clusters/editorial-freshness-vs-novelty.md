---
id: editorial-freshness-vs-novelty
domain: data-ontology
clusters: [A]
confidence: MODERATE
priority: MEDIUM
---

# Editorial Freshness Is a Distinct Axis From Discovery Novelty

## Concern

Even after "is this new to us vs. new in the world" is correctly
separated (see
[novelty-vs-discovery-time.md](novelty-vs-discovery-time.md)), a further,
distinct question remains for news/lead-oriented Clanks: is this genuinely
new-to-the-world item *still current enough* to present as news right
now? A months-old but never-before-seen rumor is novel but not fresh.

## Current terminology

`app/services/freshness.py`'s explicit module-docstring distinction
(watch-clank, the clearest statement in the fleet), `docs/editorial-policy.md`'s
named-but-unbuilt gap (korean-tech-wire), `freshness.py`'s "mothball"
age-bucket report (chinese-tech-wire), `novelty_score`'s collapse of two
signals (chinese-tech-wire, the one conflation point).

## Repos surveyed

watch-clank, chinese-tech-wire, korean-tech-wire, semiconductor-intelligence.

## Independent evidence

- watch-clank: two explicit classifiers,
  `classify_lead_freshness` (FRESH/STALE_PUBLICATION/UNKNOWN_TIMESTAMP/
  MANUAL_UNDATED/BASELINE) and a narrower
  `classify_baseline_product_freshness` — genuinely separate from
  discovery-novelty classification.
- chinese-tech-wire: `freshness.py` (age-bucketed "mothball" report) is
  architecturally separate from `score.py`'s novelty scoring — a deliberate
  module-level separation, though the two concepts still meet inside
  `novelty_score` itself (see below).
- korean-tech-wire: **explicitly names the gap it hasn't closed**:
  `docs/editorial-policy.md:7` — "Do not equate a new article with an
  alert. Future editorial processing should separately judge freshness,
  originality, authority..." This is a rare, valuable case of a repo
  documenting its own known incompleteness precisely.

## Inherited evidence

None found — independently named and partially built in each repo.

## Incidents

watch-clank's INC-01 (Epoch-1 stale-as-new) is squarely this concern: the
root cause was stated as "editorial freshness simply didn't exist as a
concept" downstream of discovery. This is the incident that directly
motivated `freshness.py`'s creation.

## Implementations

Only watch-clank has a mature, dedicated implementation. chinese-tech-wire
has a partial one (freshness reporting exists, but is not fully isolated
from novelty scoring). korean-tech-wire has named the need but not built
it. semiconductor-intelligence's "three distinct, deliberately non-colliding
meanings of novelty" documentation is adjacent evidence of the same
general discipline (careful separation of related-but-distinct temporal
concepts) applied to a different specific problem.

## Counterexamples

None — no repo argues that discovery-novelty and editorial-freshness are
the same thing; the variance is purely in how far each has gotten toward
separating them in code.

## Harm if violated

Confirmed via watch-clank's INC-01 (a 5-month-old rumor displayed as
current news) and INC-06's `notify_correlation` gap (a 142-day-stale lead
nearly sent as fresh because that one alert path had no freshness check
at all, unlike its sibling path).

## Likely domain

Data/ontology, with an editorial-workflow edge — this concern only
clearly applies to news/lead-oriented Clanks (or the news-facing half of
hybrids like watch-clank), not SKU-only Clanks.

## Unresolved questions

1. Should this be scoped as a `news-based`-profile-specific concern
   (mirroring how the UI domain scoped `STD-UI-NEWS-*` rules), given it
   doesn't obviously apply to pure SKU-tracking Clanks?
2. chinese-tech-wire's `novelty_score` conflation point: is this worth
   flagging as a specific, named counter-example for Pass 0B, given the
   repo is otherwise unusually careful about this exact distinction?

## Confidence: MODERATE
## Adjudication priority: MEDIUM
