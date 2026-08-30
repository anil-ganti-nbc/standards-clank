---
id: cross-clank-fleet-identity
domain: data-ontology
clusters: [C]
confidence: MODERATE
priority: HIGH
---

# Same Real-World Entity Discovered by Two Different Clanks

## Concern

Distinct from within-Clank identity/dedup (see
[entity-identity-coarse-key-merge.md](entity-identity-coarse-key-merge.md)):
when two *different* Clanks (e.g. smartphone-clank and smartwatch-clank,
or watch-clank and oem-radar) each independently discover the same
real-world product or entity, there is currently no fleet-level authority
deciding whether/how these should be recognized as the same thing. This
is explicitly an open, unresolved architecture question, not a solved
problem with variance in implementation quality.

## Current terminology

`CROSS-CLANK-IDENTITY` (clank-architecture, explicit open architecture
issue, no fixture yet), `BASELINE-HANDOVER` (clank-architecture, "same
entity, replacement changes entity keys"), `ADR-0014 "Typed Evidence,
Semantic Clocks, Lane Config"` (clank-architecture, PROPOSED draft),
canonical fleet inventory doctrine (diagnostic-clank).

## Repos surveyed

clank-architecture, diagnostic-clank — this is a fleet-level concern with
no single owning Clank; individual Clanks' within-repo identity models
(watch-clank, oem-radar, smartphone-clank, etc.) are relevant context but
none of them attempt cross-Clank identity resolution today.

## Independent evidence

- clank-architecture's `RISK_REGISTER.md`/`conformance/GOLDEN_INCIDENTS.md`
  explicitly registers `CROSS-CLANK-IDENTITY` as an **open architecture
  issue**, not a solved pattern with a fixture — the corpus itself states
  no silent merge should happen before an identity ADR exists.
- diagnostic-clank's Tablet Clank incident (INC-30, "local workspace
  mistaken for canonical fleet inventory") is adjacent: it's about
  *membership* rather than *identity*, but shares the root concern of
  "what counts as the authoritative registry of what exists across the
  fleet."
- `ADR-0014` (PROPOSED, not ACTIVE) directly addresses a prerequisite for
  this: typed evidence envelopes and "semantic clocks" so that facts from
  different Clanks about (possibly) the same entity can even be compared
  meaningfully in the first place — "cross-clock comparisons that drive
  verdicts must be visibly annotated."

## Inherited evidence

Not applicable — this is a fleet-level gap, not a pattern any individual
Clank has built and others copied.

## Incidents

No confirmed incident of an actual false cross-Clank merge was found —
this cluster is HIGH priority because the *absence of any mechanism at
all* is itself the risk, registered explicitly as open in
clank-architecture, not because a concrete harm has already occurred.

## Implementations

None exist. `DO_NOT_STANDARDISE` (diagnostic-clank ADR-0002) explicitly
records a prior decision *against* building a central product identity
service — this is directly relevant context Pass 0B must reckon with: any
future cross-Clank identity standard would need to either work within
that constraint (e.g. a lightweight cross-reference contract, not a
central service) or make the case for revisiting ADR-0002.

## Counterexamples

The explicit `DO_NOT_STANDARDISE` position is itself the strongest
counter-consideration: the fleet has already, deliberately, decided
against a centralized identity service, preserving "explicit
heterogeneity" in identity by design.

## Harm if violated

Speculative — no incident evidence exists. The theoretical harm (a
false cross-Clank merge conflating, say, a smartwatch and a smartphone
sharing a marketing name) is plausible but unconfirmed.

## Likely domain

Data/ontology, fleet-level — but bounded by an existing architectural
decision (`DO_NOT_STANDARDISE`) that a future standard must not silently
override.

## Unresolved questions

1. Is any fleet-wide cross-Clank identity contract wanted at all, given
   the explicit prior decision against central identity services? Or
   should this cluster be narrowed to something lighter (a shared
   "these might be the same entity" cross-reference format, never an
   authoritative merge)?
2. Should ADR-0014 (semantic clocks/typed evidence) be adjudicated first,
   since cross-Clank identity comparison is arguably meaningless until
   facts from different Clanks can be compared on a common temporal
   footing?
3. Who would own/ratify a cross-Clank identity contract, given it spans
   every Clank rather than belonging to one?

## Confidence: MODERATE
## Adjudication priority: HIGH
