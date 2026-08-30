# Pass 3 evidence dossier — STD-UI-COM-012

- **Standard ID:** STD-UI-COM-012 ("Primary workflow must not imply unobserved health")
- **Current proposed version/text:** v2. Requirement: "A primary operator surface MUST NOT present the Clank as healthy, normal, or operational solely from successful content activity (items appearing, a queue moving, counts increasing) when system/source health is not actually represented there. Where health is intentionally separated from the primary surface, that surface SHOULD provide an obvious path to current health state when operational judgement is part of the workflow."
- **Historical reason it remained proposed:** v1 ("Overview must show a visible health signal") was returned for revision by Operator Ratification Decision 002 because chinese-tech-wire, semiconductor-intelligence, and smartphone-clank deliberately keep health off their landing surfaces — a blanket MUST was the wrong level. v2 rewrote the invariant as an anti-implication rule and its own notes required a targeted evidence check against those three landing surfaces before it could move forward.

## Survey scope

| Repo | HEAD | Surveyed surface |
|---|---|---|
| chinese-tech-wire | 1a47220 (main) | `/` + `/newsroom` → `newsroom.html` |
| korean-tech-wire | afb4aad (main) | `/` → `render_overview` (single-page dashboard) |
| semiconductor-intelligence | 8a356a3 (main) | `/` → static SPA, default tab "Editorial Inbox" |
| smartphone-clank | 5684cf2 (main) | `/` → `home.html` |
| oem-radar | 9546465 (experimental/japan-mini-pc-hetzner-soak) | `/` → `render.py` overview (materially different landing model, added per handoff) |
| tablet-clank | 41282f7 (main) | `/` + `/overview` |
| feature-phone-clank | 4051b64 (main) | `/` single-page |
| smartwatch-clank | 08a23f9 (main) | `/` single-page |
| watch-clank | fbf228f (main) | `/` dashboard |

## Evidence table

| Repo | Landing claims | Measured health shown? | Implication risk observed | Health elsewhere |
|---|---|---|---|---|
| chinese-tech-wire | Actionable/Watching/New-24h/Written/Stale/Useful/FP counts; lead table | NO | none | `/health` nav-linked; "Quiet ≠ healthy. Disabled Geekbench is not a failure." (health.html:121-122) |
| korean-tech-wire | OVERALL HEALTH ("LOCAL READY"), per-source HEALTHY/STALE/BLOCKED badges, Run History | YES — measured, Fleet Law 3 ("HTTP success without useful output is not healthy after policy cycles", dashboard.py:105-110) | none (health genuinely represented) | same page |
| semiconductor-intelligence | Editorial Inbox (queue, filters, scores) | NO (health in separate "Automation & Health" tab; footer states release_channel "soaking") | none | nav-linked tab; `/api/operations/health` with explicit "degraded" state |
| smartphone-clank | Recent activity (devices by recency), "Collection disabled" card | NO | none | `/metrics` nav-linked (factor-labeled health) |
| oem-radar | Health grid with per-source ok/degraded/failed chips, "Degraded/Failed collectors" counts | YES — measured | none | same page |
| tablet-clank | "Last run" panel + recent-item tables | NO on landing | none ("Last run" is a fact, not a health claim) | "Source Health /sources/health" nav-linked |
| feature-phone-clank | OVERALL HEALTH (HEALTHY/WARNING, computed from run data), per-source health metrics | YES — measured | none | same page |
| smartwatch-clank | OVERALL HEALTH + Source Health card + Latest Runs badges; "Interpretation guard: Support presence is model/region evidence, not proof of current retail availability" | YES — measured | none (an explicit anti-implication guard exists) | same page |
| watch-clank | Stats + "See Recent Intelligence →"; no health claims | NO on landing | none | "Health / Diagnostics" nav-linked |

## Evidence FOR

1. **Nine implementations across at least four lineages, zero violations.** No surveyed primary surface presents unmeasured health as health; every Clank either shows genuinely measured health or keeps health clearly elsewhere-reachable (nav link within one click).
2. **The risk is real and the fleet has scar tissue defending against it** — three independent anti-implication artifacts, each authored per-repo:
   - chinese-tech-wire health page caption: "Quiet ≠ healthy. Disabled Geekbench is not a failure." (health.html:121-122).
   - korean-tech-wire "Fleet Law 3 (health honesty): HTTP success without useful output is not healthy after policy cycles" (dashboard.py:105-110).
   - smartwatch-clank's on-page "Interpretation guard: Support presence is model/region evidence, not proof of current retail availability" (dashboard.py:163).
3. **The v2 wording precisely handles the split that killed v1**: Clanks that show measured health on their landing (ktw, oem-radar, feature-phone, smartwatch) conform because health IS represented; Clanks that separate it (ctw, semi, smartphone, tablet, watch) conform via the obvious-path clause. Both architectures survive unchanged.

## Evidence AGAINST

1. **Partial thematic overlap with COM-008** (see overlap analysis) — a critic could call COM-012 a presentation corollary.
2. The second sentence's trigger ("when operational judgement is part of the workflow") is subjective; a pedantic audit could dispute whether a given surface's workflow includes operational judgement.
3. No observed incident where an operator actually mistook output for health was found in repo docs — the defensive captions imply the concern but do not document a concrete failure.

## Independent-lineage assessment

The three anti-implication artifacts (ctw caption, ktw Fleet Law 3, smartwatch guard) are per-repo-authored, not copied; the repos are siblings of a common fleet lineage but the HTML/API layers diverged deliberately (verified: stdlib single-file, FastAPI/Jinja, FastAPI+SPA are three different implementations). The ctw/semi `runtime_bridge.py` modules are explicitly modeled on free-game-tracker — noted, but they carry release-channel identity, not the health-display semantics at issue. Weighting independent implementations and authored doctrine over raw count: the invariant has at least three independent supporting voices.

## Overlap analysis

- **COM-008**: PARTIALLY OVERLAPS in theme, DISTINCT in requirement. COM-008 governs health that IS shown (dimensions must not blend); COM-012 governs health that is NOT shown (the primary surface must not imply it). Neither subsumes the other: COM-008 says nothing about a landing surface with no health display; COM-012 says nothing about blended dimensions. Not redundant.
- **COM-005/006/009/010/011, NEWS-001/002**: DISTINCT — no interaction with promotion mechanics, bulk runs, run detail, timestamps, delivery, or QC vocabularies.

## Applicability analysis

Applies to every Clank with a primary operator surface (universal). No surveyed implementation lacks the concept; no trigger-scoping problem.

## Testability analysis

Objectively testable by audit: enumerate health-claiming labels/status indicators on the primary surface; for each, verify it is backed by measured state (health computation) rather than content activity; verify a health path exists where separated. The nine-repo survey demonstrates the procedure works in practice.

## Recommendation

**RATIFY AS WRITTEN.** The v2 reformulation is exactly what the fleet already does everywhere, the risk it names is independently defended against in three per-repo artifacts, it is distinct from COM-008, and it is objectively testable. No surveyed implementation requires any change.

## Remaining uncertainty

Whether the SHOULD-level reachability clause's "when operational judgement is part of the workflow" qualifier adds value or friction; every surveyed Clank satisfies it trivially (health in nav), so it has caused no divergence. An operator may wish to simplify it during ratification; that is wording polish, not evidence-driven.

## Operator decision required

See decisions/0007-pass3-com-012-decision.md.
