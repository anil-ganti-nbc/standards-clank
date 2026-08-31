---
id: soak-clock-reset-semantics-and-material-change-judgment
domain: operations
topics: [3]
confidence: MODERATE
priority: HIGH
---

## Concern

When does a soak/maturity clock legitimately reset to zero, and when does
prior evidence carry forward? Every repo that has a soak concept has
independently arrived at "a *material* change resets the clock, a
cosmetic one doesn't" — but the "is this change material" judgment is,
almost everywhere, a human/narrative decision, not a code-enforced
classification.

## Current terminology

See [terminology-map.md](../terminology-map.md) "Soak" table — nine
different soak models, none sharing an implementation.

## Repos surveyed

All nine fleet Clanks, plus `clank-architecture`.

## Independent evidence

- chinese-tech-wire: explicit written rule ("soak restarts on material
  change... regardless of how long the previous build had been running
  cleanly"), with a real documented example of a provenance-only change
  correctly judged non-material. Rule is narrative, not code-enforced.
- smartphone-clank: architecture redeploy explicitly resets "the mental
  soak clock" — the phrase itself, used verbatim in the migration
  mission's own instructions, signals this is an operator-applied
  judgment call, not a mechanism.
- semiconductor-intelligence: "elapsed soak time from a previous build
  does not transfer to a materially different build... its soak clock
  restarts at zero" — same shape, also narrative/runbook-only, no code
  implementation found.
- smartwatch-clank: a firmware-classification bug fix (INC-033)
  explicitly triggers "fresh soak clock at the first post-fix natural
  cycle" — the one case found where a *specific, named* code change was
  tied to an explicit soak-clock reset instruction, though still applied
  by a human following the instruction, not enforced by code.
- tablet-clank: different axis entirely — an *interruption* (not a code
  change) resets a bounded cycle counter to 1, but prior evidence is
  retained in the JSONL report rather than erased.
- oem-radar, korean-tech-wire: soak evidence derives purely from
  persisted run-history timestamps; because there's no separate "soak
  clock" data structure, there's nothing to reset — continuity survives
  host moves, timezone changes, and service restarts by construction
  (`docs/hetzner-migration.md:85` explicitly confirms this for
  korean-tech-wire).

## Inherited evidence

`clank-architecture` ADR-0006 states the fleet-level position most
explicitly: "The QC soak clock is not reset by [a] incident... Gates that
become unmeasurable for affected lanes report UNKNOWN / NOT-YET-MATURE,
never zero" — i.e. governance-level guidance already exists that a soak
clock should *not* reset merely because of an operational incident
(distinct from a *material change*, which several repos do treat as a
legitimate reset trigger). No individual Clank was found citing ADR-0006
specifically for this distinction, though several cite it for the
adjacent continuity/epoch concept (cluster overlap noted).

## Incidents

No dated incident of a soak clock being *wrongly* reset or *wrongly* not
reset was found — this cluster is evidenced by convergent design
discipline and one clean example of the rule being correctly applied
(INC-033/smartwatch-clank), not by a failure. Kept HIGH priority because
the judgment is universally manual/undocumented-in-code across a fleet
that otherwise code-enforces most other soak-adjacent invariants.

## Implementations

No repo was found to code-enforce "classify this diff as
material/non-material, then reset or don't." Every repo does this by
human judgment recorded in prose (a runbook, a ticket, a migration
mission's instructions).

## Counterexamples

None disputing that material change should reset a soak clock; the open
question is purely mechanism (code-enforced vs. narrative).

## Harm if violated

Speculative rather than incident-evidenced: if an operator's
material/non-material judgment were wrong (too permissive), stale soak
evidence could support a promotion decision that hasn't actually been
tested against the current build. No confirmed instance of this
happening was found in the survey.

## Likely domain

Operations.

## Unresolved questions

- Is "classify a diff as material" even automatable in general (it
  requires understanding semantic content of a change, not just its
  presence), or is human judgment the correct permanent answer here,
  with a standard only requiring that the *decision be recorded*
  (build/SHA + reset timestamp + reason), rather than requiring the
  classification itself be mechanized?
- Should "soak clock must not reset due to an operational incident/manual
  recovery action" (ADR-0006's position) be adopted as a distinct,
  separate acceptance criterion from "soak clock must reset on material
  change" (the fleet's independently-converged position)? They are
  logically separate rules that happen to share the word "soak clock."
