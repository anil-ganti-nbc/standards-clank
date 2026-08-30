# Agent-facing UI Constitution

This is the compact, implementation-facing layer over Standards Clank's
RATIFIED `STD-UI-*` standards. It exists so an agent building or auditing
a Clank UI doesn't have to read every standard file individually — but it
is a summary, not a replacement. **Where this document and a cited
standard file disagree, the standard file governs.** For the full
`requirement`/`rationale`/`acceptance`/`evidence` text behind any
principle here, read `standards/ui/<ID>.json` directly, or look it up in
[`ratified-index.json`](../../standards/ui/ratified-index.json).

**Authority rule for this document:** every normative statement below (a
MUST, MUST NOT, or MAY) is derived from, and cites inline, a RATIFIED
`STD-UI-*` standard. Nothing here is invented. A rule that is still
`PROPOSED` is listed only in the "Pending / Not Yet Normative" section at
the end, and is never phrased as a requirement — do not implement or
enforce it as one. See
[decisions/0003](../../decisions/0003-operator-ratification-decision-001.md)
and
[decisions/0004](../../decisions/0004-operator-ratification-decision-002.md)
for how each of the following was ratified.

**Backend requirements are not cosmetic UI advice.** Several principles
below (especially section B) require specific *backend* behavior — an
atomic write, a race guard, a read-side query filter. Presenting the
correct visual state without the underlying operation actually being safe
does not conform. Do not summarize a backend requirement down to "show a
success message."

---

## A. Safety and authority

**A1.** Loading or launching a Clank's GUI/dashboard MUST NOT, by itself,
start a collector run. (`STD-UI-COM-001`)

**A2.** This governs the GUI process's own behavior only. A collector may
still run automatically from a mechanism entirely outside the GUI (an OS
scheduler, a separate daemon process) without violating A1 — the
requirement is that the GUI never implicitly triggers it. (`STD-UI-COM-001`)

## B. QC and operator decisions

**B1.** A QC/review decision on a queue item MUST be recorded as an
atomic, append-only record carrying a full provenance snapshot (what was
decided, on what evidence, by whom/when), kept distinguishable from
mutation of the item's own live operational record. (`STD-UI-COM-002`)

**B2.** Two concurrent decisions on the same item MUST NOT both succeed as
independent writes. The collision MUST be caught (e.g. a uniqueness
constraint) and resolved as a rejection, a no-op, or an explicit
correction — never a silent duplicate, a crash, or lost data.
(`STD-UI-COM-002`)

**B3.** The UI MUST NOT present a QC decision as safely committed unless
the underlying write has actually satisfied B1 and B2. A confirmation
toast or a queue-removal animation is not itself conformance — the write
it represents must be. Do not implement this as "show success," implement
it as "show success only once the atomic/race-safe write is confirmed."
(`STD-UI-COM-002`)

## C. Queue behaviour

**C1.** Once a QC decision is recorded for an item, that item MUST NOT
appear in the default/active queue view on the very next render, for any
operator. This MUST be achieved by excluding already-decided ids at read
time — not by deleting or mutating the item's live row. (`STD-UI-COM-003`)

**C2.** If a Clank's GUI exposes a QC queue, it MUST also expose an
operator-visible resolved/QC-history surface covering recently-made QC
decisions, sourced from the QC decision archive — not reconstructed from
the live operational table. (`STD-UI-COM-004`)

**C3.** Neither C1's exclusion mechanism nor C2's history surface is tied
to a specific route, tab name, or literal label. "Recently QC'd" is
canonical UI language where a label is shown, not a mandated string or
route. A dedicated route and an inline section both satisfy C2.
(`STD-UI-COM-003`, `STD-UI-COM-004`)

## D. Collector controls

**D1.** Where a Clank's collector/source registry distinguishes production
(finalized) from experimental/soak maturity, promoting a collector to
production MUST be an explicit, out-of-band configuration change — never a
button in the GUI, and never an automatic promotion triggered purely by
runtime metrics (soak duration, success count, etc.). (`STD-UI-COM-005`)

**D2.** Where a GUI exposes a bulk "run all collectors" control, it MUST
NOT include experimental/soak/non-promoted collectors by default. Only
collectors on the production/finalized list may run as part of a bulk
action. (`STD-UI-COM-006`)

**D3.** D1 and D2 apply only where the underlying maturity-tier concept
exists at all. A Clank with no production/experimental distinction is out
of scope for both — not in violation of either. (`STD-UI-COM-005`,
`STD-UI-COM-006`)

## E. Health and coverage

**E1.** An operator MUST be able to determine a source's operational
health (reachable, erroring, blocked, stale) without that determination
being silently affected by its coverage/output volume, and vice versa.
(`STD-UI-COM-008`)

**E2.** A source producing zero new items in a period MUST NOT
automatically read as "unhealthy" purely because output is low, unless the
Clank's own health model explicitly and visibly treats sustained
zero-output as a health-relevant signal — in which case that MUST be a
distinctly labeled dimension, not folded into one ambiguous score.
(`STD-UI-COM-008`)

**E3.** This requires semantic separation, not page separation. One screen
or even one table MAY show both health and coverage together, provided
they remain clearly distinct, separately-labeled dimensions. Coexisting on
one surface is not itself non-conformant; conflating them into one blended
metric is. (`STD-UI-COM-008`)

## F. Run observability

**F1.** Where a Clank's backend already models a run as passing through
distinct pipeline stages, the primary run surface MUST NOT present a
single terminal status (e.g. FAILED) in a way that erases a distinction
the backend itself already tracks, when that distinction would materially
change what an operator should do next. (`STD-UI-COM-009`)

**F2.** The primary run surface does not need to render every stage
inline, but it MUST visibly indicate that deeper stage information exists
and provide a direct, discoverable path to it — inline stage columns, an
expandable row, a linked detail drawer, or a linked run-detail page all
satisfy this. (`STD-UI-COM-009`)

**F3.** A page that technically contains the stage data but is not linked
from, or indicated on, the primary run surface does NOT satisfy F2 — an
operator having to already know the URL or guess it is technically present
but operationally absent. (`STD-UI-COM-009`)

## G. Time semantics

**G1.** Where a timestamp's meaning could be ambiguous to an operator
(published vs. discovered vs. decided vs. run-started, etc.), the UI MUST
label which of those it is. (`STD-UI-COM-010`)

**G2.** Where a timestamp's displayed value could plausibly be read in
more than one timezone, the timezone MUST be unambiguous to the operator.
This does NOT require a marker on every value — a single, clearly stated
surface-level convention (e.g. a caption reading "All times UTC"),
applied consistently, fully satisfies this. (`STD-UI-COM-010`)

**G3.** Silently converting to the viewer's browser-local time with no
stated convention and no per-value indication does NOT satisfy G2.
(`STD-UI-COM-010`)

## H. Delivery observability

**H1.** If a Clank has any mechanism that delivers items to an external
channel (Discord, webhook, or equivalent) and that mechanism records its
own outcome, the UI MUST make that delivery outcome independently
inspectable, separate from whether the item was merely discovered or
QC-reviewed. (`STD-UI-COM-011`)

**H2.** No dedicated delivery page is required. A tab, a drawer, an
outbox panel, a section within an event/item detail view, or a dedicated
route all satisfy H1, as long as an operator can distinguish
discovery/review state from delivery state. (`STD-UI-COM-011`)

**H3.** Collapsing multiple distinct delivery outcomes into one ambiguous
indicator (a single boolean that can't distinguish sent from pending from
suppressed from failed) does NOT satisfy H1. A Clank with no delivery
mechanism at all, or one that has explicitly and honestly disabled
delivery, is out of scope — not a violation. (`STD-UI-COM-011`)

## I. News-family workflow

*Applies only to Clanks in the `news-based` profile.*

**I1.** A news/lead-based Clank's QC decision vocabulary MUST support
Useful, Not-useful, and False-positive, plus a fourth terminal decision
named DUPLICATE — meaning "this story/lead is not novel; it is already
covered or a restatement of something already known" — in the vocabulary
slot a SKU-based Clank fills with OUT_OF_STOCK. (`STD-UI-NEWS-001`)

**I2.** Additional Clank-specific decision values beyond these four MAY be
added (e.g. a fifth value for editorial workflow state) without violating
I1. (`STD-UI-NEWS-001`)

**I3.** For a news-family Clank whose primary operator task is live
editorial triage, the default operational landing surface MUST expose the
live intake/review queue directly, or reach it with one single,
clearly-primary action — not a search through generic navigation.
(`STD-UI-NEWS-002`)

## J. Specialist flexibility

*This section draws together flexibility clauses already present in the
rules above — it does not add new requirements.*

**J1.** No principle in this document that requires "independent
inspectability" or "distinct labeling" mandates a specific route, tab,
page, or label. Combined, tabbed, drill-down, or inline presentations all
conform equally. (`STD-UI-COM-003`, `STD-UI-COM-004`, `STD-UI-COM-008`,
`STD-UI-COM-009`, `STD-UI-COM-011`)

**J2.** A principle scoped to "where X concept exists" (a maturity tier, a
delivery mechanism, a QC queue) neither applies to, nor is violated by, a
Clank that genuinely lacks that concept. Absence of the concept is out of
scope, not non-conformance. (`STD-UI-COM-004`, `STD-UI-COM-005`,
`STD-UI-COM-006`, `STD-UI-COM-011`)

**J3.** A Clank-specific extension beyond a rule's stated minimum (an
extra QC action value, an additional labeled health/coverage dimension) is
permitted as long as the rule's minimum is still met. (`STD-UI-NEWS-001`)

---

## Pending / Not Yet Normative

These are `PROPOSED`, not `RATIFIED`. They may be mentioned to an operator
as pending guidance or a preview of likely future direction — **an
implementation agent MUST NOT treat any of these as a requirement, MUST
NOT enforce them in a conformance report as if they were ratified, and
MUST NOT cite them as justification for a code change.**

- **`STD-UI-COM-007`** — "Manual collector controls must respect and
  visibly expose collector lifecycle/authority policy." Returned for
  revision in
  [decisions/0003](../../decisions/0003-operator-ratification-decision-001.md);
  the revision itself has not yet been reviewed.
- **`STD-UI-COM-012`** — "Primary workflow must not imply unobserved
  health." Returned for revision in
  [decisions/0004](../../decisions/0004-operator-ratification-decision-002.md);
  needs a targeted evidence check against chinese-tech-wire's,
  semiconductor-intelligence's, and smartphone-clank's landing surfaces
  before it can move to REVIEWED.
- **`STD-UI-SKU-001`** — "SKU review systems must preserve a distinct
  availability-negative disposition." Returned for revision in
  [decisions/0003](../../decisions/0003-operator-ratification-decision-001.md);
  the revision itself has not yet been reviewed.

`STD-UI-SKU-002` does not exist — it was considered during GUI
Ratification Pass 2 and explicitly not drafted; there is nothing pending
for it.
