# Pass 3 evidence dossier — STD-UI-COM-007

- **Standard ID:** STD-UI-COM-007 ("Manual collector controls must respect and visibly expose collector lifecycle/authority policy")
- **Current proposed version/text:** v2. Requirement: "A collector in EXPERIMENTAL or SOAK state MUST NOT become runnable merely because an individual-run control exists for it in the GUI. Where a Clank's authority/lifecycle policy explicitly permits manual execution of a non-production collector, the UI MUST identify that collector as non-production at the point of the control (not just elsewhere in the page), and the resulting run MUST remain isolated from production bulk actions (it MUST NOT be reachable via, or counted as part of, a 'run all' — see STD-UI-COM-006). Where a Clank's policy does not permit manual execution of a non-production collector, no individual-run control MAY be exposed for it at all."
- **Historical reason it remained proposed:** v1 (a SHOULD-level "individual control may target experimental collectors") was returned by Operator Ratification Decision 001 because the fleet split — watch-clank, korean-tech-wire, tablet-clank, feature-phone-clank permitting; smartwatch-clank forbidding; oem-radar structurally excluding — was a governance question, not an implementation disagreement to average over. v2 converted it into a policy-visibility invariant; v2 itself has never been reviewed.

## Survey scope (re-verified at current HEADs)

| Repo | HEAD | Maturity concept | Manual controls | Permit experimental individual runs? | Visible at control? | Isolated from bulk? |
|---|---|---|---|---|---|---|
| watch-clank | fbf228f | EXPERIMENTAL_MATURITY_COLLECTORS frozenset | `/operations/run/{id}` RUN NOW + run-all-safe | YES (policy-permitted, documented in collector_registry.py:147-159) | **NO — see finding below** | YES (default exclusion + explicit env override, off by default, restart-required) |
| smartphone-clank | 5684cf2 | soak/production (source_maturity.py) | **NONE** (read-only; POST hard-403) | no controls exist | N/A | N/A |
| korean-tech-wire | afb4aad | per-source EXPERIMENTAL/PRODUCTION in sources.yaml | `POST /collect` (all = production_only; single by id) | YES | YES — badge.production/.experimental styling, per-source Run button only for PRODUCTION unless show_experimental, control-adjacent note | YES — `production_only=(source_id is None)` (dashboard.py:82) |
| chinese-tech-wire | 1a47220 | **NO maturity concept** (flat 9-entry SOURCE_REGISTRY) | `POST /operations/run-now` (all or single) | N/A — no experimental state exists | N/A | full-cycle only; no bulk/experimental distinction exists |
| semiconductor-intelligence | 8a356a3 | **NO per-collector maturity** (enabled flag only; repo-level "soaking" release channel) | `POST /api/radar/sources/{id}/collect` + client-side collect-all loop | N/A — no experimental state exists | N/A | enabled-flag gating only |
| oem-radar | 9546465 (experimental branch) | heavy-vs-fast runtime policy; experimental collectors structurally outside GUI | `POST /api/crawl` (all or single) | NO GUI path to experimental collectors at all (scripts + isolated DBs only) | N/A — structurally excluded; heavy/Run-All distinction IS badged ("slow collector(s) excluded from Run all") | YES by construction |
| tablet-clank | 41282f7 | EXPERIMENTAL state + PRODUCTION_ALLOWLIST | `POST /collect?source=` (single) + `POST /collect/all` (production allowlist) | YES | YES — maturity badges (finalized/soaking/retired) on collect page rows; "never included, even by accident" | YES |
| feature-phone-clank | 4051b64 | config/scope.yaml production allowlist | run-all (production) + `run/{key}` + explicit `run-experimental/{key}` lane | YES | YES — Production/Experimental cards, "hidden from Run all" badge | YES — experimental lane writes to an isolated DB; "Run all deliberately only ever iterates production_collectors" |
| smartwatch-clank | 08a23f9 | CollectorTier PRODUCTION/EXPERIMENTAL + production_allowlist | run-all (finalized) + `run/{name}` (allowlist only) | **NO — policy forbids** | collapsed "Experimental / soak collectors — hidden from Run All by design" explainer; API returns 400 `not_finalized` | YES by construction |

## Key finding: watch-clank vs clause 2

Watch-clank's policy explicitly permits manual experimental runs (collector_registry.py:147-159: "an EXPERIMENTAL collector remains fully wired and individually runnable via RUN NOW / COLLECT … Only its default membership in the *bulk* 'Run all' set changes"), and its bulk isolation is exemplary (default exclusion + explicit, restart-required, off-by-default env override "explicitly with a reason, not silently"). **But its operations page labels each collector with a LAYER badge (OFFICIAL/SPECIALIST — a content-layer, not maturity) and a health badge only; EXPERIMENTAL maturity is not rendered at or near the RUN NOW control** (operations.html contains no maturity marker). Under v2 clause 2, that is a non-conformance — a small one (a badge), but a real one, and watch-clank is otherwise the fleet's reference-quality implementation.

This is stated plainly because it means RATIFY AS WRITTEN creates an immediate, small remediation-backlog item for watch-clank. That is the correct trade per fleet precedent: standards are ratified on the strength of the invariant, and a Clank found behind lands in backlog (same pattern as smartphone COM-002 and watch COM-009 at ratification time).

## Evidence FOR

1. **Every policy-forbidding implementation already conforms to clause 3** (smartwatch: 400 `not_finalized` + no button + explainer; oem-radar: structural exclusion) — the clause matches real, deliberate behavior.
2. **Every maturity-bearing implementation that permits manual experimental runs already labels them at/near the control** (ktw badges + control-adjacent note; tablet maturity badges + "never included, even by accident"; feature-phone "hidden from Run all" badge + separate experimental lane) — clause 2's visibility requirement is the fleet's dominant practice, not an invention.
3. **The bulk-isolation clause is already ratified doctrine**: COM-006 (ratified) requires production-only bulk; every Run All surveyed excludes non-production (watch SAFE_COLLECTOR_IDS, ktw production_only, tablet allowlist, feature-phone scope.yaml, smartwatch allowlist, oem-radar heavy-exclusion with visible badge).
4. **The no-concept Clanks (ctw, semi-int) and the no-controls Clank (smartphone) are cleanly out of scope** — the trigger clause (EXPERIMENTAL/SOAK state existing) keeps them N/A, exactly as constitution J2 intends.

## Evidence AGAINST

1. **watch-clank's missing maturity badge** (above) — the only surveyed non-conformance, and it sits in the fleet's flagship.
2. The v2 bulk-isolation clause overlaps COM-006 by design (it cross-references it); a reader could ask why the bulk rule is restated.
3. ctw and semi-int have no maturity concept, so the rule regulates nothing there today — if either later grows soak collectors, they inherit the obligation; that is forward-looking by design, not evidence-based.

## Independent-lineage assessment

The maturity-gating pattern appears in at least four lineages: ktw (config status + production_only), tablet (state enum + allowlist), feature-phone (scope.yaml allowlist + explicit experimental lane; its core/scope.py attributes the doctrine to a smartphone-clank pollution incident), smartwatch (tier enum + allowlist, modeled on watch's local_operator), watch (frozenset + env override). ctw/semi/oem-radar demonstrate the N/A structural forms independently. The visibility practice (badges at control) recurs across ktw/tablet/feature-phone independently. The one contrary data point (watch's unlabeled control) is a single-lineage omission.

## Overlap analysis

- **COM-006**: PARTIALLY OVERLAPS — COM-006 owns "bulk run-all excludes non-production"; v2's bulk-isolation clause deliberately cross-references it rather than restating authority. COM-007's distinct content is the single-control visibility requirement and the policy-forbids clause. Not redundant.
- **COM-005**: DISTINCT — COM-005 governs promotion mechanics (no GUI promotion, no auto-promotion); COM-007 governs run-control behavior for already-classified collectors. Different lifecycle moment.
- **Others**: DISTINCT.

## Applicability analysis

Trigger-scoped: applies only where (a) an EXPERIMENTAL/SOAK maturity concept exists AND (b) manual run controls exist. Verified: ctw/semi-int fail (a) → N/A; smartphone fails (b) → N/A. A Clank with no manual controls is N/A, not a violation — confirmed against the evidence.

## Testability analysis

Objectively testable: enumerate run controls; resolve each controlled collector's maturity; check (1) non-production identification at the control, (2) bulk-action membership, (3) absence of controls where policy forbids. All nine surveys applied this procedure successfully.

## Recommendation

**RATIFY AS WRITTEN.** The v2 conditional structure resolves the Pass 1 fleet split honestly (permit-with-visibility / forbid-with-no-control / no-concept-N-A), every maturity-bearing implementation except one already conforms, and the one exception (watch-clank's unlabeled RUN NOW) is a small, honest remediation-backlog item — not grounds to weaken the visibility clause that four other lineages already practice.

## Exact narrowed wording

Not applicable — no narrowing recommended.

## Remaining uncertainty

None material. Watch-clank's remediation size is trivial (one badge); whether Motherclank-side automation consumes watch's operations page in a way that makes the badge urgent is an operator prioritization call, not an evidence question.

## Operator decision required

See decisions/0008-pass3-com-007-decision.md.
