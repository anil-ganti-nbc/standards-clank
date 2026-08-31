# 0017 — Operations ratification: STD-OPS-COM-004 (Exclusivity-marker soundness)

Date: 2026-08-31
Status: AWAITING OPERATOR DECISION
Survey dossier: [../docs/operations/pass3/ratification-survey.md](../docs/operations/pass3/ratification-survey.md)
Standard: [../standards/operations/STD-OPS-COM-004.json](../standards/operations/STD-OPS-COM-004.json) (v1, PROPOSED)

An agent MUST NOT ratify this standard (see
[0002-no-agent-self-ratification.md](0002-no-agent-self-ratification.md)).

## Survey outcome (Pass 3, from stored Pass 0A/0B/1.5/2/2.5 evidence — no recrawl)

- Evidence: STRONG — four independent-environment incident discoveries
  across four repos and three distinct failure directions (indefinite
  starvation on a stale-but-honored marker, wrong-process termination
  from a reused identifier, a one-shot-container reclaim failure, a
  duplicate daemon from a stale PID file). The remedy (OS-level advisory
  locks) propagated by explicit code-porting and is counted once, not as
  four independent votes, per Pass 2's own evidence-discipline note.
- Trigger: correctly scoped to any Clank using a marker capable of
  outliving or being interpreted across process/execution-context
  boundaries; purely in-process locking and marker-less Clanks are out of
  scope.
- Counterexample survived at three separate stages (the original
  candidate card, the Pass 1.5 resolution, and Pass 2's review): "DB
  advisory locks, leases, and fencing tokens look nothing like flock" —
  the invariant binds validity-proof provenance, not mechanism shape, and
  each named mechanism was individually checked to conform.
- No overlap with STD-OPS-COM-001 verified explicitly in this standard's
  own text: a Clank deadlocked on a stale-but-unsound lock can satisfy
  COM-001's materialization contract perfectly (every refused fire is a
  recorded skip outcome) while starving indefinitely — the exact shape of
  oem-radar's ~81 refused fires.

## A process note this survey is flagging honestly, not smoothing over

STD-OPS-COM-001/002/003 were each drafted, then put through a dedicated
Pass 2 adversarial review of the **actual drafted text** (verdicts:
APPROVE FOR RATIFICATION SURVEY). STD-OPS-COM-004 followed a different
path: Pass 2 adversarially reviewed the **pre-draft candidate** and
issued specific drafting constraints (verdict: DRAFT AS STD-OPS-COM-004),
and the standard was then drafted at a separate, later Pass 2.5 following
those constraints — but the resulting normative text itself has not been
through a dedicated adversarial-review pass the way the other three
were. This ratification survey and its own automated guards confirm the
drafted text follows Pass 2's stated constraints faithfully, but that is
this survey's own read, not an independent adversarial pass's verdict on
the finished wording. Recorded here for the operator's visibility rather
than assumed away.

## Recommendation

RATIFY AS WRITTEN (agent recommendation — operator decides), with the
process note above surfaced explicitly rather than treated as
equivalent-strength process to COM-001/002/003.

## Operator options

- **Option A — Ratify as written** (recommended). The drafted text
  demonstrably follows Pass 2's specific constraints (title, invariant,
  trigger, minimum acceptance/forbidden concepts, implementation
  freedoms all present and verified by test), and the underlying
  candidate itself survived two separate adversarial passes (its own
  candidate-card counterexample test, and Pass 2's review) before
  drafting.
- **Option B — Send STD-OPS-COM-004 back for a dedicated Pass 2-style
  adversarial review of the drafted text itself**, closing the process
  gap noted above before ratification, rather than treating Pass 2's
  pre-draft review of the candidate as sufficient for the finished
  wording. This is the more conservative option given COM-001/002/003
  each received that step and COM-004 has not.
