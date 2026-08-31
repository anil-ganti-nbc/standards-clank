---
id: destructive-action-authority-before-mutation
domain: operations
topics: [10]
confidence: STRONG
priority: HIGH
---

## Concern

This concern emerged from the survey rather than being one of the 15
topics named in the original brief, but is among the most severe findings
in the entire corpus: an agent (in these cases, an AI coding assistant
performing fleet remediation work) executed a destructive mutation
(`docker volume rm`) against production state by trusting a naming
pattern instead of first resolving the actual identity of the target and
confirming a backup existed. This happened **twice in one week**, once
with total, unrecoverable data loss.

## Current terminology

`clank-architecture` ADR-0009 calls this "runtime state separation and
destructive safety." No fleet Clank has its own name for this — the
concern lives entirely at the governance/tooling-discipline layer, not in
any individual Clank's code.

## Repos surveyed

`diagnostic-clank` (live NAS incident log — both incidents were logged
there), `clank-architecture` (the resulting ADR).

## Independent evidence

Two dated, real incidents, same root cause, one week apart:
- INC-041 (feature-phone-clank, 2026-08-23): an agent ran a destructive
  volume-deletion action against the real production DB volume during
  remediation work, trusting a naming-pattern guess rather than a
  read-only listing first. **No backup existed. Total, unrecoverable data
  loss.**
- INC-036/INC-029 (smartwatch-clank, 2026-08-23): the same root cause,
  same week — destructive volume deletion destroyed the live database
  including all observations newer than the newest backup; restored from
  a ~4-day-stale backup, so partial (not total) loss.

`clank-architecture/adr/0009` independently documents a second incident
family from the same window: the git-stash root-redeploy runtime-path
incident (INC-027, cluster A) — both families are described together in
ADR-0009 as evidence that destructive/high-blast-radius operator and
agent tooling needs a structural contract, not just care.

## Inherited evidence

`clank-architecture` responded with an explicit 8-step contract: DISCOVER
→ RESOLVE ACTUAL IDENTITY → CLASSIFY → PROVE BACKUP → DISPLAY EXACT
TARGET → EXPLICIT AUTHORISATION → MUTATE → VERIFY (ADR-0009). This is
governance written directly and immediately in response to these two
incidents, not speculative design. `RISK_REGISTER.md` presumably tracks
the underlying risk class, though this survey did not find a specific
R-number cross-reference for it distinct from R-001 (deployment-truth,
cluster I) — worth Pass 0B confirming.

## Incidents

INC-041 (total loss, most severe single incident in this entire survey),
INC-036 (partial loss, same week, same root cause).

## Implementations

The 8-step ADR-0009 contract is the only implementation found for this
exact concern, and it postdates both incidents — i.e. there was no
protective mechanism in place *before* either incident occurred.

## Counterexamples

None.

## Harm if violated

Total, unrecoverable production data loss (INC-041). This is the single
most severe consequence found anywhere in this survey — more severe than
any scheduler-truth or health-conflation incident, because it is
irreversible.

## Likely domain

Operations — though note this concern is explicitly about *operator and
agent tooling discipline* during remediation/maintenance work, not about
a Clank's own runtime architecture. It may sit closer to a
cross-cutting "how work gets done on this fleet" policy than a
per-Clank operational contract — worth Pass 0B's explicit judgment on
whether this belongs in a Standards Clank Operations standard at all, or
whether it's better captured as `clank-architecture`'s own governance
(where ADR-0009 already lives) with Standards Clank only cross-referencing
it.

## Unresolved questions

- This is the clearest case in the whole corpus where a fleet governance
  response (ADR-0009) already exists, was written in direct response to
  the exact incidents evidenced here, and predates any Standards Clank
  involvement. Should Standards Clank ratify anything here at all, or
  is the correct action to *not* create a competing/duplicate standard
  and instead note that `clank-architecture` already owns this?
- Both incidents involved an AI agent performing the destructive action.
  Is the standardizable rule "any destructive mutation, human or agent,
  must follow the 8-step contract" (tooling-agnostic), or does it need
  to specifically address agent-performed operations as a distinct risk
  class (given both real incidents were agent-caused)?
