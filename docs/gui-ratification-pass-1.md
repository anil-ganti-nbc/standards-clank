# GUI Ratification Pass 1 — evidence and candidate standards

Status: **superseded by ratification.** This document captures the
original Pass 1 evidence-gathering and drafting. On 2026-08-30 the operator
reviewed it rule by rule and issued
[Operator Ratification Decision 001](../decisions/0003-operator-ratification-decision-001.md):
7 of the 9 candidates below are now `RATIFIED` (two with wording changes —
see the decision record and each standard's own `notes` field for what
changed and why); the other 2 (`STD-UI-COM-007`, `STD-UI-SKU-001`) were
returned for revision and were rewritten (version 2, still `PROPOSED`) —
their tables rows below describe the *original* Pass 1 drafts, not the
revised text; read the JSON files under
[`standards/ui/`](../standards/ui/) for the current wording. This page is
kept as the historical evidence record, not edited to match the outcome.

Built on top of the repository-groundwork baseline, commit `dca1e37`. No
governance or schema decisions from that baseline were revisited — none of
this pass's findings required it. `clank-architecture` was read for
evidence only (see the `read-only reference` / `read-only, this repo is
explicitly off-limits for consolidation` notes below); nothing in it was
modified, and no consolidation was attempted.

## Method

Five parallel, read-only survey passes inspected all nine fleet Clanks
(watch-clank, oem-radar, chinese-tech-wire, korean-tech-wire,
feature-phone-clank, tablet-clank, smartwatch-clank, smartphone-clank,
semiconductor-intelligence) plus `clank-architecture` for cross-fleet
governance evidence, with file:line citations required for every claim.
Every candidate rule below cites its actual evidence; see each standard's
`evidence[]` array under `standards/ui/` for the full citation list — this
table summarizes, it doesn't replace those files.

**Governing principle applied throughout** (the operator's framing,
verbatim): *existing practice is evidence, not precedent. A pattern
appearing in several Clanks does not make it a standard if those Clanks
merely copied the same bad design. Conversely, a pattern appearing in only
one Clank may still be a strong candidate if it demonstrably solves a
fleet-wide operational failure.* Where a pattern's presence in multiple
Clanks is mostly attributable to direct copying (a documented port or
scaffold, not independent design), the table's evidence column says so
explicitly and that alone did not earn a STRONG rating. Independent
convergence — two or more Clanks arriving at the same contract from
different starting points, or a pattern traceable to a named incident —
is what earned STRONG ratings here.

## Profiles used

This pass populated `profiles/sku-based.json` and `profiles/news-based.json`
from direct evidence of what each Clank actually collects (not from any
assumption). `watch-clank` and `semiconductor-intelligence` are notable:
watch-clank is a genuine hybrid — it has both `EventReview` (product/SKU
events, using `OUT_OF_STOCK`) and a separate `SpecialistLeadReview`
(specialist leads, using `DUPLICATE`) — and appears in both profiles' member
lists rather than being forced into one. `smartphone-clank` is SKU-based by
subject matter (phone-model leaks) but is a documented exception case for
several rules below, since it has no QC-queue UI at all.

## Ratification table

| Rule | Family | Level | Evidence | Counter-evidence / caveats | Recommendation |
|---|---|---|---|---|---|
| [STD-UI-COM-001](../standards/ui/STD-UI-COM-001.json) — GUI must never auto-trigger collection on load/launch | Both | MUST | 9/9 Clanks; oem-radar cites a named 2026-08-27 incident plus clank-architecture Fleet Law 5 | smartphone-clank's separate daemon *does* autorun on a schedule, but architecturally outside the GUI — not a violation of this narrowly-scoped rule | **STRONG** |
| [STD-UI-COM-002](../standards/ui/STD-UI-COM-002.json) — QC decisions atomic, provenance-bearing, race-guarded | Both | MUST | Two independently-originated lineages (watch-clank's table-based; CTW's file-based) converge on the same contract, then propagate | smartphone-clank's `qc-action` is a raw INSERT with no archive, no unique constraint — the anti-pattern this rule forbids, currently in production | **STRONG** (contract itself); smartphone-clank gap flagged below, not resolved here |
| [STD-UI-COM-003](../standards/ui/STD-UI-COM-003.json) — resolved item leaves active queue immediately, read-side | Both | MUST | 8/9 Clanks with a queue implement identical anti-join pattern | smartphone-clank has no queue view at all (N/A, not counter-evidence) | **STRONG** |
| [STD-UI-COM-004](../standards/ui/STD-UI-COM-004.json) — "Recently QC'd" view required if a queue exists | Both | MUST | 8/9 Clanks with a queue have this; its absence correlates exactly with the one Clank lacking a QC archive | smartphone-clank: absent, consistent with STD-UI-COM-002 gap | **STRONG** |
| [STD-UI-COM-005](../standards/ui/STD-UI-COM-005.json) — promotion is explicit config change, not GUI/automatic | Both (conditional) | MUST | Independently articulated in watch-clank (SKU) *and* korean-tech-wire (news) with separate written rationale, not copied text | CTW, semiconductor-intelligence, smartphone-clank have no maturity-tier concept — out of scope, not violations | **STRONG** |
| [STD-UI-COM-006](../standards/ui/STD-UI-COM-006.json) — bulk "run all" excludes non-production collectors | Both (conditional) | MUST | 5 Clanks with an explicit maturity concept all exclude experimental from bulk runs | oem-radar's exclusion is by runtime cost, a related but distinct axis; semiconductor-intelligence's "collect all enabled" doesn't map cleanly | **STRONG**, with a noted encoding caveat |
| [STD-UI-COM-007](../standards/ui/STD-UI-COM-007.json) — individual control may target an experimental collector | Both | SHOULD | 4 Clanks allow it | smartwatch-clank explicitly forbids it (config-promote-first only); oem-radar doesn't wire experimental collectors into the GUI at all | **QUALIFIED** — genuine fleet split, needs an operator judgment call, not more evidence |
| [STD-UI-SKU-001](../standards/ui/STD-UI-SKU-001.json) — 4th QC action = OUT_OF_STOCK (SKU family) | SKU | MUST | watch-clank (origin), feature-phone-clank, tablet-clank, smartwatch-clank match literally | oem-radar encodes the same semantics differently (`AVAILABILITY_CHANGED` + reason code, no literal 4th enum value) | **QUALIFIED** — acceptance criteria written to allow oem-radar's encoding; confirm that framing is acceptable |
| [STD-UI-NEWS-001](../standards/ui/STD-UI-NEWS-001.json) — 4th QC action = DUPLICATE (news family) | News | MUST | **Two independent origins** (CTW's LeadOutcome, watch-clank's own SpecialistLeadReview) converge on DUPLICATE before any cross-copying; semiconductor-intelligence cites watch-clank directly, not CTW/KTW | CTW's extra `WRITTEN` value is an allowed superset addition, not a conflict | **STRONG** — best-evidenced rule in this pass |

## Explicitly considered and NOT proposed

**GUI framework/stack choice** (FastAPI+Jinja2 vs. stdlib `http.server`) —
evidence was almost evenly split (4 vs. 5 across the fleet) and might look
like a plausible candidate by vote count alone. It is excluded on principle,
not lack of evidence: per
[decisions/0001-standardise-contracts-not-implementation.md](../decisions/0001-standardise-contracts-not-implementation.md),
Standards Clank standardises observable contracts, not implementation
technology. This is the clearest example in this pass of the operator's
"evidence is not precedent" instruction cutting the other way — a pattern
present in most of the fleet is still out of scope if it's implementation,
not contract.

**Runtime mutation-authorization gating** (a token/`local_operator`-style
gate making the whole dashboard read-only until an authenticated profile is
present) — seen in smartwatch-clank, korean-tech-wire, and smartphone-clank,
all comparatively recent additions. Marked **INSUFFICIENT** — three Clanks,
all plausibly on the same recent trajectory rather than independently
converged, and the mechanism details differ enough (smartwatch-clank's
`local_operator` flag vs. KTW's Bearer token vs. smartphone-clank's
unconditional 403) that it's premature to generalize a contract from them.
Worth revisiting in a future pass once more Clanks either adopt or
explicitly reject it.

## Open items for the operator (not resolved by this pass)

1. **smartphone-clank's QC gap.** Its CLI `qc-action` writes directly into
   the live `analyst_actions` table with no archive, no uniqueness
   constraint, and no documented race handling — it would not conform to
   STD-UI-COM-002/003/004 if those are ratified as-is. This pass does not
   propose an exception (exceptions apply to ratified standards, and
   nothing is ratified yet) or attempt remediation. The operator should
   decide, at ratification time, whether this is a remediation item or a
   standing documented exception tied to the Motherclank integration.
2. **STD-UI-COM-007's fleet split** (individual-control access to
   experimental collectors) needs a direct operator decision between
   smartwatch-clank's stricter posture and the more permissive majority —
   see the table above.
3. **STD-UI-SKU-001's acceptance criteria** were written to accommodate
   oem-radar's alternate encoding of the out-of-stock outcome rather than
   forcing a rewrite. Confirm this is the right call before REVIEWED status.
4. A possible bug, found incidentally and out of scope for Standards Clank
   to fix: smartwatch-clank's macOS launcher (`native/macos/launcher.py:21`)
   does not pass `local_operator=True`, unlike its Windows launcher
   (`native/windows/launcher.py:39-42`) — GUI mutation may be silently
   unavailable on macOS. Flagged separately as an out-of-scope task, not
   fixed here.

## Resolution (added after Operator Ratification Decision 001)

All four "open items" above were resolved by
[decisions/0003-operator-ratification-decision-001.md](../decisions/0003-operator-ratification-decision-001.md):
(1) smartphone-clank's gap → remediation backlog, no exception; (2) and (3)
resolved by rewriting STD-UI-COM-007 and STD-UI-SKU-001 rather than
picking a side of either split; (4) remains open as a separately-flagged,
out-of-scope bug report, untouched by Standards Clank.

## What this pass did not do

No standard's `status` was set to `REVIEWED` or `RATIFIED`. No existing
Clank was modified. `clank-architecture` was read, not touched or
consolidated. `profiles/sku-based.json` and `profiles/news-based.json` were
populated with `members` (real evidence) but not `standards` (that field is
for post-ratification profile adoption, per
[docs/standards-lifecycle.md](standards-lifecycle.md)).
