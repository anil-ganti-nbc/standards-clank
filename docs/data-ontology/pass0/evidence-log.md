# Pass 0A — Raw Evidence Log

Six read-only survey agents, each following the same domain definition and
cluster taxonomy (A–G, see [../README.md](../README.md)). Preserved
verbatim (light formatting only) for traceability — the [clusters/](.)
files are a synthesis of this material, not a replacement for it. Every
citation below is file:line in the named repo at the HEAD noted.

---

## Survey 1 — watch-clank + oem-radar

**watch-clank** HEAD `fbf228f7ecccf2de4119fca29f8344aff9c49441`, clean, matches origin.
**oem-radar** checked out on branch `experimental/japan-mini-pc-hetzner-soak`, HEAD `95464658fb6d991cab18eeb8012cfe958fda563a`, matches that branch's own upstream. Note: the repo's *default* branch (`origin/HEAD`) is a different, unmerged commit `d720e0635894ddcc9a39f116e2aa4a1768090042` — this survey ran against the experimental branch, not the default branch.

### Cluster A — Temporal Truth

**watch-clank** — `app/services/freshness.py` module docstring: "DISCOVERY NOVELTY ('has Clank seen this before' -- is_baseline, dedup-by-URL) and EDITORIAL FRESHNESS ('is this current enough to show a journalist as news') are different questions" (freshness.py:6-9). Two classifiers: `classify_lead_freshness` (FRESH/STALE_PUBLICATION/UNKNOWN_TIMESTAMP/MANUAL_UNDATED/BASELINE) and `classify_baseline_product_freshness`. `publication_timestamp_is_usable()` (freshness.py:62-76) rejects any `published_at` more than 1-minute clock-skew after `observed_at` — future-dated timestamps are evidence-rejected, never negative-evidence, and the raw value is preserved ("we reject it as EVIDENCE, never delete it," freshness.py:57-58). A real, fixed incident: `ai/handoff/INCIDENT_EPOCH1_FRESHNESS.md` — a GUI displayed `discovered_at` labeled "Time" for specialist leads whose real `published_at` spanned March–August; root cause: "there was no freshness field to conflate *with* — freshness simply didn't exist as a concept" (lines 70-74). `SourceObservation.is_baseline`/`CollectorRun.is_baseline` (discovery-time) kept separate from `FreshnessResult.state == "BASELINE"` (editorial-time).

**oem-radar** — `NormalizedProduct.first_seen`/`last_seen` excluded from `content_hash()` "so a re-crawl never looks like a change" (core/models.py:183-186). `docs/ARCHITECTURE.md:19`: "Notifications report **detection time**, never pretend to be launch time." Baseline tagged explicitly on `ChangeEvent.meta`, "never inferred from a timestamp" (core/models.py:93-97). `EvidenceCandidate.dedup_key()`: "observation time must never create noise" (models.py:394-395). Incident: `docs/CURRENT_STATUS.md:12-26` — baseline events (tagged correctly) were still counted as live alerts because nothing downstream read the flag; put "all 1,875 baseline records in front of the first genuine alert." Structurally identical to watch-clank's Epoch-1 incident; no cross-reference found between the two repos.

### Cluster B — Unknown/Negative/Absent

**watch-clank** — `app/services/editorial.py:11-13`: "SOLD_OUT/UNAVAILABLE must never be inferred from source failure, zero results, redirects, or parse errors — only from a genuinely successful before/after observation pair." `classify_price_availability_transition()` returns `(None, ["UNKNOWN: ..."])` when either side is unhealthy (editorial.py:211-216). `FIRST_SEEN_BY_CLANK` vs `NEW_REFERENCE` (editorial.py:70-92): "A reference that is merely absent from this database until today is not, by itself, evidence the manufacturer launched it today." `WATCH_EVENT_SEMANTICS.md:2-3`: "Fleet Law 2: prefer UNKNOWN / observation-only over a confident false event." Incident: `CITIZEN_STALE_FLOOD_AUTOPSY_20260818.md` — discovery path never carried inventory data, `availability_status` NULL for 47/47 items; never asserted false unavailability, but genuinely-almost-gone stock was indistinguishable from sold-out at discovery time.

**oem-radar** — `Availability` enum: `IN_STOCK`/`PREORDER`/`SOLD_OUT`/`UNKNOWN` as a first-class member (core/models.py:41-46). `Component.known: bool | None` — three-valued, "None means not yet determined... renderers must caveat, not guess" (models.py:118-119, pipeline.py:136-138). `diff.py:150-155`: "Do not emit a transition *to* UNKNOWN: that normally means a source stopped exposing a field, not that a product became unavailable." `EvidenceLinks.product_key: str | None` — "NULL = deliberately unlinked/ambiguous," a valid non-error state (schema.sql:256, EVIDENCE_ARCHITECTURE.md:58). Narrower than watch-clank: no dedicated OUT_OF_STOCK-equivalent review outcome — `alert_reviews.outcome` is only HIT/INTERESTING/NOISE/BUG.

### Cluster C — Entity Identity/Dedup

**watch-clank** — Canonical identity `(manufacturer, brand, reference_canonical)` (watch.py:35-40); `reference_raw` always preserved. Brand-by-brand conservative dedup: Casio has a real evidence-built suffix allowlist; Citizen/Seiko/Timex are deliberate pass-through "until brand-specific evidence justifies otherwise" (references.py:11-14,187-263). `WatchFamily` grouping is explicitly provisional, separate from canonical identity (watch.py:27-31,90-152). No fuzzy/similarity matching — conservative, allowlist-driven only.

**oem-radar** — Much richer explicit hierarchy: FAMILY→MODEL→SKU/CONFIG→REGIONAL LISTING→URL (identity.py:9). Six-way `IdentityDecision` enum with an explicit match cascade (identity.py:25-31,125-216). `config_signature()` deliberately excludes the model string: "a marketing rename must not mask identical hardware" (identity.py:112-122). **Real, twice-recurring dedup failure**: `resolve_prior`'s coarse `model_key` fallback merged two genuinely different SKUs sharing a model_key+tier word (Galaxy Book6 Ultra 64GB vs 32GB) — fixed with a vendor-SKU-disagreement guard (docs/STAGE8.md:65-86, providers/sqlite/__init__.py:356-365); **the same bug class recurred independently** months later in the Evidence Fusion identity-linking code (docs/EVIDENCE_ARCHITECTURE.md:122-135), caught by a dedicated regression test naming the exact failure mode.

### Cluster D — Observation vs Canonical Fact

**watch-clank** — Three-tier: `SnapshotFetch`/`SnapshotBlob` (raw, content-addressed) → `SourceObservation` (one parse) → `Watch` (canonical). Identity fields set once at creation; no code path found overwriting them from a later observation (not exhaustively verified — full `pipeline.py` transition logic not fully read, flagged as a gap). `SourceObservation.field_confidence`/`parser_warnings` carry disagreement/uncertainty alongside every observation rather than resolving it away. `EventReview` docstring: "a later pipeline run could in principle correct the canonical Watch/Event row underneath a Review; this snapshot preserves what the operator actually looked at" (review.py:86-89) — explicit acknowledgment that canonical facts can be corrected later, and human-judgment provenance must be pinned to evidence-at-judgment-time. Timex case: a real fact (`published_at`) was captured into `extra_specs` but never consulted by the transition pipeline for ten days of production (`INCIDENT_TIMEX_BASELINE_ABSORPTION.md:62-63,76-77`).

**oem-radar** — `docs/EVIDENCE_ARCHITECTURE.md` directly answers "should an alternate source be forced into `NormalizedProduct` or modeled as a sibling concept?" → sibling concept (`EvidenceItem`), because forcing it would mean inventing values forever (EVIDENCE_ARCHITECTURE.md:20-25). **Documented, corrected mistake**: Stage 11 wrote evidence observations into `change_events` (canonical product-alert table); Stage 11.1 reverted because "different claims with different consumers" — measured harm: 44.6% of all "alerts" were evidence, filling 300/300 visible dashboard slots and burying real product changes (EVIDENCE_ARCHITECTURE.md:82-104). `_OBSERVATION_FIELDS` excluded from `content_hash()` "or every crawl would look like a change (ADR-4)" (models.py:183-186). Content-hash dedup: identical content → `touch()` only; differing content → new immutable snapshot row, never overwrite (ADR-4). Cross-listing merge precedence is an explicit cascade, never silent (providers/sqlite/__init__.py:328-368).

### Cluster E — Evidence/Provenance

**watch-clank** — Full chain: `source_url`/`collector_id`+version/`parser_id`+version/`fetch_id` → `SnapshotFetch` (HTTP metadata) → `SnapshotBlob` (content-addressed bytes) (observation.py:47-91, snapshot.py:30-88). `PipelineLedger` (pipeline.py:73-107) — append-only, stage-level, keyed by `correlation_id`, recording rule versions per step. `EventReview` carries its own provenance snapshot "at review time" distinct from the live chain (review.py:101-105). `WATCH_EVENT_SEMANTICS.md:25-31` — full evidence-grade vocabulary (OFFICIAL_PRODUCT_PAGE > ... > RUMOUR), "preserved not acted on."

**oem-radar** — `EvidenceItem`: source_id/canonical_url/external_id/evidence_kind/provenance (6 specific values, "never a generic OFFICIAL")/published_at/observed_at/content_hash (models.py:332-370). `evidence_links.method`: exact_sku/exact_mpn/exact_model_id/alias/normalized_model/none — the *method* of linking is itself recorded provenance. `alert_review_history` records previous_outcome→new_outcome transitions with changed_by/change_note. Narrower storage-layer provenance than watch-clank (no separate content-addressed blob table; raw/parsed folded into one `snapshots` row).

### Cluster F — Baselining/Novelty

**watch-clank** — `OperationalEpoch`: exactly one active epoch per DB; baseline gates real-row-creation but never Event-row-creation (epoch.py:6-14). A *second*, independent baselining mechanism, `initial_fill.py`, added after discovering the epoch mechanism alone was insufficient for bounded-per-run-budget catalogues (slow-drip flood risk) (initial_fill.py:3-9,18-34,83-114). **Four documented incidents**: (1) Epoch-1 freshness (see A); (2) Timex baseline absorption — a genuinely recent launch silenced by an unconditional baseline guard, fixed with an empirically-tuned 72h window (validated against 1,485 real watches: a naive 30-day window would false-positive 16% of the catalogue); (3) Timex catalogue backfill burst — ~1045 real events fired on a never-baselined local DB; **unresolved structural finding in the addendum: Hetzner's production `operational_epochs` table is also empty (0 rows)** — production baseline protection currently depends entirely on a manually-passed `--force-baseline` flag per source, and "any future source onboarded to Hetzner whose first run omits `--force-baseline` would hit the exact same unprotected-burst mechanism... except with real, currently-configured Discord webhooks live." Three remediation options proposed, **none implemented**; (4) Citizen stale flood (see B) — explicitly *not* a repeat of the baseline-flood mechanism, a distinct correctly-classified incident.

**oem-radar** — `docs/DATABASE_LIFECYCLE.md` — Epoch-1→Epoch-2 cutover is documentation-only bookkeeping, no `epoch` column in schema ("the epoch boundary *is* which file is currently at data/radar.db"). `core/baseline.py` archive/import: "everything imported from the archive starts life as *known*... a post-cutover crawl of unchanged content produces ZERO events" (lines 11-14); `count_unseeded_listings()` is an explicit cutover preflight check. `baseline_quiet` suppresses notifications on a source's first-ever successful crawl, per-source not epoch-table-driven. Documented incident (see A) structurally identical to watch-clank's — independently found. No equivalent to watch-clank's "initial fill window" bounded-budget drip-flood mechanism was found — may mean the failure mode isn't present, or is untested; not conclusively determined.

### Cluster G — Availability/Lifecycle

**watch-clank** — `SourceObservation.availability_status: str | None` free-text; `AVAILABILITY_EVENT_TYPES = {SOLD_OUT, RESTOCK}` plus generic `AVAILABILITY_CHANGE` (editorial.py:35,182-260) — three distinct facts, gated on both observations being healthy. Treated as a DATA concern separate from editorial concern: the fact is recorded unconditionally, "is this newsworthy" is a separate, harder gate (editorial.py:391-417). Citizen's own `market_status` field (Current/DWS/Phase-Out/Promotion) was deliberately **not** used as an availability filter after being proven unsafe (a Phase-Out SKU had 7 units genuinely in stock) — kept as "context, not a filter."

**oem-radar** — `Availability` enum is a proper closed type, stronger than watch-clank's free text. `Configuration.availability` is per-config, not per-product — "variants must not be flattened" (models.py:129-133). `restock.py` is a dedicated availability/lifecycle subsystem with its own editorial gate keyed on hardware-generation lifecycle stage (CURRENT/PREVIOUS/OLD/LEGACY/UNKNOWN), not the raw availability fact alone — same DATA-vs-editorial split as watch-clank, different mechanism. `ProductStatus` enum (ACTIVE/PRE_RELEASE/REMOVED/UNCERTAIN) is a distinct lifecycle-status field alongside `Availability` — watch-clank has no equivalent "is this product still a going concern" field.

### Incidents (this survey)

1. watch-clank Epoch-1 stale-as-new (2026-08-11) — see A.
2. watch-clank Timex baseline absorption (2026-08-17) — see F.
3. watch-clank Timex catalogue backfill burst (2026-08-17), **live unresolved Hetzner risk** — see F.
4. watch-clank Citizen stale/out-of-stock flood (2026-08-18) — see B.
5. watch-clank Citizen regional-commercialisation miss (2026-08-12) — `TRANSITION_DETECTION_FAILURE`, no concept of "same reference, new region" existed; fixed with `NEW_REGION`.
6. watch-clank 2026-08-19 emergency hotfix batch — accessory-only false NEW_REFERENCE; `notify_correlation` missing freshness check (142-day-stale lead nearly sent as fresh); recency-only QC sort buried an 11-month-old RESTOCK at equal priority to new items; REACTIVATED tag correctly classified but needed explicit surfacing.
7. oem-radar baseline-masquerading-as-alerts (2026-08-08) — see A/F.
8. oem-radar Samsung/Lenovo cross-OEM identity merge bug, recurred twice — see C.
9. oem-radar evidence-observations-polluting-alert-stream (Stage 11→11.1) — see D.

### Lineage notes (this survey)

- `app/core/identity.py:1-6` in watch-clank explicitly cites oem-radar (among others) as the origin of its git-SHA build-provenance pattern — **inherited-copied**, but this is deployment/build provenance, not data/ontology fact provenance.
- No other cross-repo lineage citation found for any data/ontology pattern proper. Both repos independently converged on strikingly similar concepts (freshness separation, absence-discipline, coarse-key-merge guards, layered evidence/provenance, "annotation not suppression" QC) with **no shared code or citation** — assessed as **lineage-uncertain, likely independent convergence** under a shared but unstated house philosophy, not a port.

---

## Survey 2 — chinese-tech-wire + korean-tech-wire

**chinese-tech-wire** HEAD `1a47220c69e6bb91f2899a0508508c42254c9d5b`, clean, up to date.
**korean-tech-wire** HEAD `afb4aada1d4fae09ada4658fe9fcf8dfa38eb23d`, up to date; untracked `build/`/`dist/` only.

### Cluster A — Temporal Truth

**CTW** — `Article.published_at` vs `discovered_at` (models.py:36-37) always distinct. `StoryCluster` has *three* chronology axes with source+timestamp pairs: `first_seen_at`, `first_signal_source/_at` (community), `first_media_source/_at` (news), `first_documentary_source/_at` (documentary) — deliberate, non-conflated "who saw it first per layer" model (models.py:71-83, HANDOFF.md:17-23,217-224). `_ensure_utc()` recovers naive timestamps via source/region metadata rather than silently assuming UTC (normalize.py:27-54). `score_novelty()` computes first-in-cluster (structural novelty) and new-spec-content (informational novelty) as separate signals but **collapses them into one scalar** `novelty_score` — the one place two temporal concepts blend (score.py:68-94). `freshness.py` ("editorial freshness"/"mothball") is explicitly a read-only age-bucket report over `last_activity_at`, never touching how that field is computed; treats a *missing* value as active, never silently hidden (freshness.py:1-16,49-56). `LeadOutcome.recorded_at` is explicitly labeled in output as "operator-entered, not a verified publish timestamp" (editorial_validation.py:432-443).

**KTW** — `articles.published_at`/`discovered_at`/`first_seen_at`/`last_seen_at` as four distinct columns; on conflict-UPDATE, `first_seen_at` is correctly never touched, only `last_seen_at` (storage/database.py:20,167-178). `docs/editorial-policy.md:7` **explicitly names the gap**: "Do not equate a new article with an alert. Future editorial processing should separately judge freshness, originality, authority..." — i.e., "new record" ≠ "editorially fresh" is acknowledged but not yet built. `published_at` is only extracted from explicit OG/JSON-LD fields, never inferred from discovery (architecture.md:22). No cluster-level chronology concept exists at all (no StoryCluster equivalent) — "new in the world across sources" is simply unrepresented, a genuine absence not a conflation.

### Cluster B — Unknown/Negative/Absent

**CTW** — `FAILURE_STAGES` enum: UNKNOWN/SOURCE_NOT_MONITORED/SOURCE_BLOCKED/SOURCE_FAILED/PARSER_MISSED/ENTITY_MISSED/CLUSTER_MISSED/LOW_SCORE/LIFECYCLE_FILTER/ALERT_FILTER/DUPLICATE_ERROR/TOO_LATE/OTHER (missed_stories.py:24-38), each finding labeled `certainty: confirmed/probable/unknown`, module docstring: "it never invents new certainty" (lines 8,172-255). `effective_outcome()`: three-way OUTCOME/FEEDBACK/UNLABELED, with UNKNOWN itself a valid *recordable* outcome distinct from UNLABELED-nobody-recorded-anything (outcomes.py:141-159, comment line 146). `_rate()` returns `pct: None` (never 0%) with `low_sample: True` on zero denominator (editorial_validation.py:56-72). `DocumentaryRecord.record_status`: ACTIVE/MISSING/REMOVED/REAPPEARED, a 4-state lifecycle requiring repeat-confirmation before MISSING escalates to REMOVED (models.py:332-333,349).

**KTW** — `record_status`: valid/legacy_unverified, quarantine functions demote rather than delete (database.py:24,189-197). Three-way failure classification (`environment`/`intentional_development`/`source_or_parser`) prevents infra noise from counting as evidence against a source's health (database.py:37-44). No CTW-equivalent rich absent-state vocabulary for articles (no MISSING/REAPPEARED concept) — narrower scope, not a conflation.

### Cluster C — Entity Identity/Dedup

**CTW** — Three explicit dedup levels: exact canonical_url, high fuzzy title similarity, moderate title+entity overlap; "false merges are worse than missed merges... never deletes, only clusters" (deduplicate.py:1-10). `Entity` alias map collapses CN/TW/HK spelling variants deterministically (entities.py:22-99). Known limitation, admitted: "brand overlap can soft-match different model numbers" (HANDOFF.md:305).

**KTW** — Identity is `UNIQUE(source_id, canonical_url)` only — **no cross-source, fuzzy, or entity dedup at all**. `docs/architecture.md:26`: "ETNews is intentionally not deduplicated against The Elec" — a deliberate scope decision, explicitly documented as a *feature* ("independent corroboration is valuable... rather than redundant overlap," stage4-editorial-yield.md:41) — the **opposite editorial philosophy** from CTW's cluster/corroboration model. `title_normalized` is computed and stored but write-only — never read by any dedup/lookup logic (database.py:171), unlike CTW where title normalization directly feeds `title_similarity`.

### Cluster D — Observation vs Canonical Fact

**CTW** — `_refresh_existing()`: `existing.title = raw.title or existing.title` — COALESCE-style, a new observation with a blank value cannot erase a known fact (documentary_ingest.py:163-165). `novelty_score` decays on repeat sighting, never re-inflated (`min(existing, new*0.5)`); `priority_score` damped 0.7x on repeat (documentary_ingest.py:198-202). Three granularities kept separate: raw `DocumentarySnapshot` (immutable, content-hashed) / canonical `DocumentaryRecord` (mutable) / append-only `DocumentaryEvent` (change log). `LeadOutcome` docstring: "current" is a *derived read* (max by timestamp) over an append-only log, not an overwritten field — contrast with `Article`/`StoryCluster`, which *are* mutated in place (models.py:483-513). **No explicit source-disagreement representation found** — later-observed values implicitly win within the COALESCE-preserves-non-null-only constraint; conflicting simultaneous sources are not modeled as a first-class state.

**KTW** — Same COALESCE-preserving pattern on enrichment fields, but `title_original`/`title_normalized`/`content_hash`/`raw_metadata` are unconditionally overwritten (latest-wins) on the same row — an undocumented, implicit inconsistency in which fields get which overwrite policy (database.py:177). No raw-observation-vs-canonical-fact separation at all — one row per URL, no snapshot table, no change-event log.

### Cluster E — Evidence/Provenance

**CTW** — `docs/EXPLAINABILITY_CONTRACT.md`: a formal, versioned contract (`DecisionExplanation`→`Contribution`→`ThresholdCheck`→`TimelineEvent`[with an explicit `inferred` flag]→`MaterialChange`). Rule 1: "Never invent facts not present in stored records or configuration." This is the single richest provenance-granularity artifact found across the entire fleet survey. `database/qc_archive.py` is a physically separate SQLite DB specifically so human-decision evidence "survives independent of anything that happens to the operational pipeline later." `upstream.py` — `source_type` enum (ORIGINAL_REPORTING/OFFICIAL/RETAIL_LISTING/REGULATORY/BENCHMARK/SOCIAL_MEDIA/LEAK/REPOST/ANALYSIS/UNKNOWN) traces where a claim ultimately comes from, "never fabricate."

**KTW** — `fetch_attempts`/`run_errors` tables give per-request evidence granularity, arguably finer than CTW's per-run `SourceRun` — but no `DecisionExplanation`-equivalent exists (no scoring/alerting layer yet). Extraction methodology is documented in prose per-source, not as a structured per-article field.

### Cluster F — Baselining/Novelty

**CTW** — `SourceRun.layer` comment on pre-migration rows: "Nullable/defaulted... honestly NEWS — no other layer ever wrote this table before" (models.py:145-148) — a baseline-migration honesty note. No explicit "epoch marker"/"first full crawl ever" flag — `first_seen_at` on a fresh DB is indistinguishable from a real first-in-world sighting; a 48h dedup window and conservative-merge philosophy limits but doesn't eliminate the blast radius of an initial-backfill flood. **Documented incident**: V0.5.3 (HANDOFF.md:391-421) — alert-eligibility thresholds made zero of ~3,121 real leads ever reach ACTIONABLE; separately, `notified=True` was set even when Discord send actually failed (attempted-≠-confirmed conflation).

**KTW** — `baseline_has_content()` is an explicit, first-class, correctly-scoped concept: only once a source has ever had a successful non-zero run does a subsequent zero-reference run become an anomaly rather than expected cold-start (database.py:74-76,44; architecture.md:44). **Documented, dated incident**: Stage 4 due-gating baseline-adjacent flood (2026-08-10 to 2026-08-19) — a fleet-level "due" fact was derived as an AND-aggregation over per-source due-states, so one permanently-failing source (SK hynix, HTTP 403) kept the *entire fleet* permanently "due," producing ~4x the intended request rate for over a week. Root mistake: aggregate state computed as AND over per-item state instead of per-item. Fixed with strictly-per-source due-ness. A related, correctly-handled incident: the SK hynix HTTP 403 block was explicitly classified `HOST-BLOCKED` (external infra fact) rather than demoting the source's own lifecycle/identity — "demoting a company newsroom because of a datacenter IP block would misrepresent the actual defect." A separate incident: Samsung Newsroom Korea had no editorial-filter branch at all, so 100% of 19,344 references defaulted to "accepted" — absence of a filter branch was indistinguishable at runtime from "genuinely no low-value content."

### Cluster G — Availability/Lifecycle

**CTW** — `DocumentaryRecord.record_status` (ACTIVE/MISSING/REMOVED/REAPPEARED) is CTW's product-availability analogue, applied to retail/benchmark listings. `StoryLead.lead_status` includes STALE/RESOLVED/DISMISSED as first-class lifecycle states.
**KTW** — `record_status` valid/legacy_unverified is the lifecycle analogue; no REMOVED/REAPPEARED/MISSING-streak concept — narrower scope consistent with news-only ingestion (no retail/benchmark layer).

### Incidents (this survey)

1. CTW V0.5.3 alert-eligibility gate + attempted-vs-confirmed-send conflation (dated by version, not calendar).
2. KTW Stage 4 due-gating fleet-vs-per-source aggregation flood (2026-08-10 to 2026-08-19, dated).
3. KTW SK hynix HTTP 403 host-block — correctly classified, included as a positive counterexample.
4. KTW Samsung Newsroom Korea missing editorial-filter branch (confirmed 2026-08-19) — absence indistinguishable from "no low-value content."

### Lineage notes (this survey)

CTW's `StoryCluster`/dedup/novelty design: **independent**, and explicitly positions itself as a template "intended for reuse in other collector projects" (EXPLAINABILITY_CONTRACT.md). KTW's architecture doc explicitly states it does "not import, configure, share a database with, or schedule alongside any other Wire" (architecture.md:3) — **independent by explicit self-declaration**. KTW's dedup/novelty logic is **not a port** of CTW's — categorically simpler (no clustering, no entity aliases, no fuzzy matching), and KTW's docs frame the *lack* of cross-source overlap as a deliberate, opposite editorial philosophy, not an unported feature. Shared conventions (three-way failure taxonomy, append-only-history preference, COALESCE-preserve-non-null overwrite pattern) most plausibly reflect one author/team's recurring habits across sibling projects, not shared code.

---

## Survey 3 — feature-phone-clank + tablet-clank

**feature-phone-clank** HEAD `4051b64fe7ba4dc188ec1e1a6920ce72b14f013d`, clean, up to date.
**tablet-clank** HEAD `41282f78438704d563692560a8a1fdfb8a1d66ed`, clean, up to date.

### Cluster A — Temporal Truth

**feature-phone-clank** — `Discovery.observed_at` is the only timestamp; `content_hash()` explicitly excludes it "so a re-fetch of unchanged content never looks like a change" (models.py:89-111). Documented near-miss: Lava's `launch_date` field is null or a stale 2024 date on a product named "A1 2025" — explicitly "cannot be trusted as a freshness signal," retained as raw evidence only, never wired into the diff/event pipeline (FEATURE_PHONE_SCOPE_EXPANSION.md:186-197). `first_seen_at`/`last_seen_at` are pure observation bookkeeping, never a launch-date proxy.

**tablet-clank** — Research-stage doctrine, ahead of any implementation: `docs/SOURCE_RESEARCH.md:135` (Lenovo PSREF): "`Announce Date`... must not be treated as the time the row first appeared in the observed feed or as proof of retail launch... retain both." `docs/PROJECT_STATE.md:71`: literal repeated design phrase **"FIRST_SEEN != NOVELTY."** No `announced_at`/`published_at` exists in the live schema at all — the concern is fully deferred to research docs, never contradicted in code because it's never been implemented.

### Cluster B — Unknown/Negative/Absent

**feature-phone-clank** — Module docstring: "Collectors only ever produce Discovery objects... a collector must never invent a value: unknown stays None" (models.py:3-6). `spec_completeness: "complete"|"incomplete"` is a distinct axis from any one field being None. `diff_meaningful_fields` treats present→absent as explicitly **not** a change ("far more likely a parser hiccup... than a real spec removal," diff.py:100-110) — a single missing field is never promoted to "removed"; only whole-page absence (`spec_completeness` transition) is a first-class event, gated by `REMOVAL_CONFIRMATION_THRESHOLD=3` consecutive runs at the whole-product level.

**tablet-clank** — `HANDOFF.md:84`: "Unknown values remain unknown; do not fabricate." `docs/IDENTITY_MODEL.md:51`: "No variant/SKU/configuration ID was captured, and no ... composite is safe to synthesize." `docs/SOURCE_RESEARCH.md:139`: "an active row moving to withdrawn, a missing active row, and a stale/blocked page are different conditions. No safe disappearance rule is implemented or proposed here" — three distinct absence causes named, none collapsed. `HANDOFF.md:82`: "Do not infer product disappearance from a missed run" — reinforced by the fact that **no disappearance/removal event type exists at all** in tablet-clank's vocabulary (contrast feature-phone-clank's `PRODUCT_REMOVED`).

### Cluster C — Entity Identity/Dedup

**feature-phone-clank** — `product_key` = manufacturer+model/SKU/URL, stable within one source. `docs/FEATURE_PHONE_SCOPE_EXPANSION.md:530-549`: "Duplicate handling: not yet exercised... nothing merges across source_key values automatically... premature to build correlation logic against zero real evidence" — a **deliberate, reasoned absence** of cross-source dedup, not an oversight. Identity anomaly (SKU changed at a known URL) is flagged for review, never silently overwritten — `products.model_number` "not touched again after creation." **Real dedup bug, fixed**: `IDENTITY_ANOMALY` compared each run's SKU against the fixed-at-creation `model_number`, so a product whose SKU changed once then stayed kept re-triggering every subsequent run (2 Discord messages for 1 real flip) — fixed by gating on `is_new_obs` (DEFINITION_OF_DONE.md:149-159).

**tablet-clank** — Canonical identity: manufacturer+(model_number OR SKU OR name fallback)+region+connectivity+RAM+storage (IDENTITY_MODEL.md:5-9), fallback explicitly flagged as able to under-distinguish, "requires audit before production use." **Real incident, fixed**: Apple Store US/IN collectors didn't dedupe repeated carrier/unlocked URLs sharing one regional partNumber, producing **48 false new_product events** before a fix reclassified them `identity_correction`, retained not deleted (ARCHITECTURE.md:35, HANDOFF.md:27,96). Region is explicitly part of identity, not a variant dimension, and the model says this is *itself* provisional and unaudited (IDENTITY_MODEL.md:15,31). Multiple research-stage near-misses caught before shipping: Xiaomi Mi Mall numeric product IDs resolving to unrelated home-appliance pages (IDENTITY_MODEL.md:51); Lenovo PSREF "Global canonical Lenovo identity remains UNRESOLVED" (one family maps to many country-specific codes, IDENTITY_MODEL.md:33-47); Honor/TCL regional slugs proven stable only as source-observation identifiers, not global canonical hardware identity (IDENTITY_MODEL.md:53-63).

### Cluster D — Observation vs Canonical Fact

**feature-phone-clank** — `FieldChange.old_value/new_value` are always raw observed values, "never normalized — normalization decides *whether* something counts as a change, it never rewrites what gets shown as evidence" (models.py:114-118). Observations are strictly append-only (`INSERT OR IGNORE`, `UNIQUE(product_id, content_hash)`) — never UPDATE (schema.sql:1). Canonical `products` table carries only identity fields; all spec state lives in the append-only `observations` table.

**tablet-clank** — Raw and normalized JSON both persisted, never collapsed (ARCHITECTURE.md:30). **Real architectural difference from feature-phone-clank**: `products` spec columns (processor, ram_gb, etc.) *are* directly overwritten in place on each differing, non-null observation (pipeline/__init__.py:36-41) — the prior value is preserved as `old_value` in the corresponding `change_events` row only if baseline is complete; pre-baseline, an overwrite leaves no event and no trace except the append-only `observations` table underneath. Canonical mutation is real and by-design here, unlike feature-phone-clank's stricter isolation.

### Cluster E — Evidence/Provenance

**feature-phone-clank** — Four distinct granularities in four separate storage layers: `Discovery.raw` (fact-level, per-collector), `Event.previous_observation_id/current_observation_id` (change-level, always traceable to the exact observation pair), `classification_log` (classification-decision-level, retains evidence_json for every classify/reject/quarantine decision, not dropped), `qc_store` (operator-QC-decision-level, full snapshot-at-decision-time, non-destructive correction history).

**tablet-clank** — Three granularities: `observations.raw_values/normalized_values` (fact), `change_events.evidence_url` (`NOT NULL`, change-level), `qc_archive.py` (operator-decision, full self-contained snapshot). Plus a fourth, narrower ledger: `rejected_candidates` (reason+raw_values for candidates that never became products).

### Cluster F — Baselining/Novelty

**feature-phone-clank** — **Major documented incident**: the 2026-08-23 destructive Hetzner volume deletion destroyed all prior observation history with no backup ("NONE existed"); new epoch `fpc-epoch-2` begins fresh, the lost epoch's identity permanently recorded as unknown, "not reconstructed, estimated, or fabricated" — doctrine: "a fresh baseline is never novelty" (core/continuity.py, ADR-0006). `is_baseline = previous_count is None` gates *every* event type, not just NEW_PRODUCT. Catastrophic-zero guard blocks persistence entirely if a source with prior active catalogue reports zero — explicitly "learned from Smartphone Clank's incident history" (runner.py:1-16). `core/scope.py:1-9` names the cross-Clank lesson explicitly: "Smartphone Clank learned the hard way that a collector which can run must not thereby be allowed to write to the production catalogue — a test run polluted it with 73 junk devices" — production allowlist exists specifically because of this inherited, named incident.

**tablet-clank** — Same baseline-gates-every-event-type discipline (pipeline/__init__.py:22,32,40), repeatedly verified across every promotion wave with explicit "0 events, 0 duplicates" soak proofs, phrased as "FIRST_SEEN != NOVELTY." Soak/campaign machinery actively refuses to run a stale roster once sources are production-promoted, to prevent re-baselining/double-counting. No data-loss incident found in this repo; no continuity/epoch module exists at all.

### Cluster G — Availability/Lifecycle

**feature-phone-clank** — `availability: str|None` exists as a raw per-observation string, populated by only 3 of several collectors, **never read by the diff/event pipeline anywhere** (grep-confirmed zero references) — persisted as evidence with zero semantic weight; explicitly listed as an out-of-scope backlog item (DEFINITION_OF_DONE.md:125). The QC-layer `OUT_OF_STOCK` disposition is a pure operator judgment, disconnected from this dormant field. **Lineage correction**: feature-phone-clank's QC vocabulary is explicitly ported from **Watch Clank's** `EventReview` contract (qc_store.py:1-9) — but this inheritance is of the QC review *shape* only, not of any availability data semantics.

**tablet-clank** — **No availability/stock/lifecycle column exists anywhere in the schema at all** — a stronger absence than feature-phone-clank's dormant field. The QC `OUT_OF_STOCK` disposition's own docstring reasons about "a still-listed vs. withdrawn catalogue entry" but nothing in `products`/`change_events` stores that distinction — the reviewer's call is made by looking at the live page, not from any stored fact. **Lineage correction to a standing assumption**: tablet-clank's `qc_archive.py` is explicitly modeled on **korean-tech-wire's** pattern (module docstring line 3), *not* watch-clank — no reference to watch-clank/smartwatch-clank exists anywhere in tablet-clank's source or docs. **Net finding**: the shared `OUT_OF_STOCK` vocabulary across the fleet has *two different lineage paths* (Watch Clank → feature-phone-clank; korean-tech-wire → tablet-clank), and in *both* cases the underlying availability data model is dormant-and-unused or entirely absent beneath it.

### Incidents (this survey)

1. feature-phone-clank Hetzner volume data loss (2026-08-23) — total pre-loss history lost, no backup existed, new epoch declared, no fabrication.
2. feature-phone-clank inherited Smartphone Clank scope-contamination lesson (pre-dates this repo; "73 junk devices") — production allowlist built specifically to prevent recurrence.
3. feature-phone-clank duplicate IDENTITY_ANOMALY notification bug (fixed pre-merge).
4. feature-phone-clank itel listing-card name-extraction bug (parsing, borderline out of domain).
5. tablet-clank Apple Store carrier/unlocked URL duplication → 48 false new_product events (found, fixed, evidence retained).
6. tablet-clank Xiaomi Mi Mall stale/reassigned numeric product-ID (caught at research stage, never shipped).
7. tablet-clank Apple sitemap identifier-free baseline pollution (found, fixed, fails closed at zero accepted candidates).
8. feature-phone-clank Lava/itel weak-identity gap (open, documented limitation, not yet an incident).

### Lineage notes (this survey)

feature-phone-clank's QC layer → explicitly Watch Clank (qc_store.py:1-9). feature-phone-clank's sqlite migration pattern → explicitly OEM Radar (providers/sqlite/__init__.py:24-26, persistence-mechanics only). tablet-clank's QC archive → explicitly korean-tech-wire, **not** watch-clank (storage/qc_archive.py:1-21) — this directly narrows a standing assumption that both Clanks share one QC lineage from watch-clank. Cross-repo dedup/identity guard patterns (HMD nav-slug exclusion list vs. Apple-sitemap identifier-free rejection) solve the same problem independently, no cross-reference — convergent, not copied.

---

## Survey 4 — smartwatch-clank + smartphone-clank

**smartwatch-clank** HEAD `08a23f9`, clean, up to date.
**smartphone-clank** HEAD `5684cf2`, up to date; untracked `build/` dirs only.

### Cluster A — Temporal Truth

**smartphone-clank** — `Device.first_seen/last_seen` vs `Evidence.published_at` (source-claimed) vs `Evidence.first_seen/last_seen` (system-observed) are kept distinct (models.py:47-48, schemas.py:51-53). **Finding: the dossier's "verified/drift" confidence badge is decorative, not real** — `ConfidenceLedger.summary()` sets `ledger.confidence = device.confidence` directly (confidence_ledger.py:119-137), so the dossier's `device.confidence == ledger.confidence` comparison (dossier.html:28-33) can structurally never be false; the badge can never render "drift." Real drift computation exists (`ConfidenceService.recalculate()`, confidence_service.py:74-106) but is reachable only via a demo script and a test, not via any UI or documented CLI path — the only user-visible "trust freshness" signal is fake, the real one is unreachable. Confidence decay explicitly privileges "official" sources (never_decay_types, decay.py:38) as a single, non-duplicated mechanism.

**smartwatch-clank** — `Device.first_seen/last_seen`, `Observation.observed_at`; a comment on `firmware_version` explicitly warns "never populate it from publisher-maintained timestamps" (models.py:142-145) — a direct pointer to a real incident. **Incident**: the `coros_updates` collector wrote a Zendesk **editorial** `updated_at` into the **hardware-semantic** `firmware_version` field; because that field participates in change-detection, a single site-wide help-centre touch produced **23 simultaneous false FIRMWARE_RELEASED events sharing one timestamp** in one second of wall-clock time (2026-08-28), 0/27 verifiable as real releases. Status: source **BLOCKED from production**, remediation documented but **not yet implemented**. `core/continuity.py` — append-only, content-hashed epoch/continuity ledger separately tracking "when this happened" vs "when we found out" vs "what period is now unknown."

### Cluster B — Unknown/Negative/Absent

**smartphone-clank** — **Flagship finding of the entire pass**: `docs/KNOWN_LIMITATIONS.md:6` states "Release state defaults to unknown — novelty ≠ upcoming" as a design principle, but **there is no `release_state` field anywhere in the schema** (grep-confirmed). The dossier template literally hardcodes the string `&lt;span class="badge"&gt;unknown&lt;/span&gt;` (dossier.html:20) — it renders identically for every device forever, regardless of any evidence, because it is not bound to any data at all. The semantic guarantee is real defensive intent but implemented entirely as a UI string literal, not as data. Genuinely-modeled distinct states elsewhere: `Snapshot.meaningful: Optional[bool]` (tri-state, not a defaulted boolean); `PageMonitor.is_removed`/`consecutive_not_found` (a removal counter, not a single-observation flag); `WebhookDelivery.eligible/suppressed/attempted/delivered` as four independently-tracked booleans, fixed after a documented incident where they were conflated (see Incidents).

**smartwatch-clank** — `SMARTWATCH_CLANK_DEFINITION_OF_DONE.md:20-22`: "Support evidence proves official support presence... it does not by itself prove current retail availability... Catalogue evidence is a merchandising snapshot, not a discontinuation signal" — and this **is** backed by real code, unlike smartphone-clank's release-state finding: `SamsungRelationship`/`CandidateState` enums (9 combined states) have no state meaning "discontinued" or "unavailable" anywhere — the model *structurally cannot* assert unavailability from catalogue absence. `diff_catalogues()` never classifies catalogue/support disappearance the same as generic product removal.

### Cluster C — Entity Identity/Dedup

**smartphone-clank** — Canonical key `(manufacturer, model_number)`, DB-enforced unique constraint, "structurally prevented, not just conventionally avoided" per HANDOFF.md §7. Regional-variant family-key stripping is Samsung-tuned but verified harmless elsewhere. Alias conflicts are logged and the **existing** mapping kept, never silently repointed. `FamilyService`: "never invent a family name with no supporting pattern," returns None rather than fabricating. **Real, major documented incident**: the "August 2026 contamination incident" — non-Samsung generic collectors shipped `enabled: true` with no validation gate, marketing sentences were parsed as model_number identities, producing **73 garbage Device rows**; fixed with a structural, config-flag-immune `production_scope()` allowlist plus release-blocking regression tests. Admitted gap: regional variants are currently just multiple Evidence rows on one Device, not first-class per-region facts — the more-correct `RegionalSighting` table exists in schema but is unwired (HANDOFF.md §11.4).

**smartwatch-clank** — Identity is a single opaque `identity: str`, uniqueness enforced per-run/per-source-class at the SQLite layer, not globally canonical the way smartphone-clank's `Device` table is. No alias table / persistent codename resolver exists at all — a structural gap relative to smartphone-clank, not called out in this repo's own docs. Named, fixed bugs: an overly-permissive "no signal → ambiguous" fallback retained 2,000+ unrelated Garmin products; a registered-trademark symbol in real product names ("Approach® S70") silently broke watch-vs-non-watch classification for an entire product line (unnormalized-glyph identity bug).

### Cluster D — Observation vs Canonical Fact

**smartphone-clank** — Three-tier `Discovery`→`Evidence`→`Device`. **Overwrite semantics are asymmetric and intentional**: canonical descriptive fields (marketing_name, codename, region) are only ever filled if empty — a later source can never overwrite an already-set value, only fill a gap; identity fields are immutable post-creation. This also means an incorrect early value can never be corrected by a later, better source — a plausible latent risk, not flagged anywhere in the docs. Confidence has a single enforced writer, confirmed by an AST-scan enforcement tool (`confidence_mutation_audit.md`) after illegal direct mutations were found and removed. Evidence dedup: same content_hash/URL → refresh last_seen only; a genuinely different content_hash on the same URL is new, independent corroborating evidence, both rows persist. `AnalystAction` is a fully separate, third provenance tier with a partial-unique-index enforcing one terminal decision per target, raising `DuplicateTerminalDecision` rather than silently overwriting.

**smartwatch-clank** — Two-tier only: `Observation`→`Discovery` (diffed event); **no persisted canonical Device table at all** — canonical truth is reconstructed from "the last healthy Observation set," a structurally different architecture from smartphone-clank's separately-maintained, mutated canonical row. `record_evidence()` docstring/code: "Never overwrites an earlier first_seen... independent first-seen per source class survives later, stronger evidence" — honored, verified in code.

### Cluster E — Evidence/Provenance

**smartphone-clank** — `Evidence.raw_data` (full JSON payload retained) plus `ConfidenceLedgerEntry` (one row per point delta, unique on device_id+evidence_id+rule to prevent double-counting) — real per-contribution audit history, not a running total. `AnalystAction` = third tier. `Snapshot` retains optional full HTML + five hash types. Admitted retention gap: "Snapshot unbounded growth," prune policy not implemented, flagged not silently dropped. `TimelineEvent`: append-only, "never deleted."

**smartwatch-clank** — `evidence_records`/`evidence_timeline`, thinner — no `raw_data`/full-payload column, only generic `payload_json`; no separate content-hash-linked raw snapshot table. `discoveries` stores previous/current/evidence JSON per event but no itemized per-rule ledger (confidence here is a single enum per discovery, not an accumulating score). `core/continuity.py` is a distinct incident-provenance tier, closest analogue to smartphone-clank's `AnalystAction` but for system/operator incidents, not device QC.

### Cluster F — Baselining/Novelty

**smartphone-clank** — `SourceBaselineState` tracks baseline_started_at/completed_at/run_count; completion requires a genuinely successful full-enumeration run. **Real incident**: the Motorola canary — a config allowlist gap silently dropped every Motorola candidate while the baseline tracker still marked itself complete; left unfixed, the next run would have fired 18 false "new device" alerts. Generalized fix: baseline completion now requires proof of persistence (`new+updated+resighted &gt; 0` whenever `valid &gt; 0`), regression-tested. Novelty suppression (`NEWSROOM_SUPPRESSED_REASONS`) is fail-closed on unknown reasons, but explicitly **not yet wired for Samsung** — an admitted, documented asymmetry.

**smartwatch-clank** — `source_onboarding` + region-based baseline flag: on first run for a region, no FIRST_SEEN event fires for support-only sightings — an independently-implemented baseline-flood guard using a different mechanism than smartphone-clank's alert-eligibility-reason suppression. The coros firmware incident (A) is also a novelty failure by definition. **Data-loss/restore incident**: 2026-08-23, destructive volume deletion, restored from a 2026-08-18 backup; `core/continuity.py`'s seed `OBSERVATION_GAP` event states explicitly: "Absence inside this window is never zero and never novelty; post-gap source returns must be evaluated against restored history without backfilling" — the correct doctrine, code-enforced (`EPOCH_ID = "sw-epoch-1-restored"`), with an admitted permanently-unknown pre-loss epoch identifier. `SMARTWATCH_CLANK_HOST_ID` is pinned specifically to prevent ephemeral container hostnames from fabricating spurious migration/gap records.

### Cluster G — Availability/Lifecycle

**smartphone-clank** — Largely absent, and admitted as such (see B — this is the same finding: no field backs the "release state" disclaimer). No `availability`/`lifecycle_state`/`discontinued`/`stock` field anywhere; `active: bool` means "still tracked by us," never written to False on any inferred discontinuation signal.

**smartwatch-clank** — Actively modeled, in contrast: `Observation.price/currency/availability` are first-class fields; `ChangeType` distinguishes PRICE_CHANGE/AVAILABILITY_CHANGE/PREORDER_STARTED/SHIPPING_STARTED/PRODUCT_REMOVED/POSSIBLE_DISCONTINUATION/SOURCE_LISTING_REMOVED — a genuinely richer vocabulary than smartphone-clank's. But the higher-level discontinuation-inference logic is deliberately not yet built on top of these fields (`POSSIBLE_DISCONTINUATION` exists in the enum but is never constructed anywhere in `diff.py`) — the opposite gap shape from smartphone-clank (fields absent vs. inference absent).

### Incidents (this survey)

1. smartwatch-clank coros_updates false FIRMWARE_RELEASED novelty (discovered/adjudicated 2026-08-30) — 23 simultaneous false events from an editorial timestamp misused as a hardware-semantic field; BLOCKED from production; fix documented, **not implemented**.
2. smartphone-clank August 2026 contamination incident (73 fabricated devices, investigated 2026-08-06).
3. smartphone-clank Motorola false-baseline-completion incident (2026-08-10).
4. smartphone-clank Alert-table meaning drift — 129 historical rows conflating "we decided to alert" with "we successfully alerted," fixed 2026-08-10 with `WebhookDelivery` as the new source of truth; historical rows explicitly left in place, undeleted, with a documented caveat rather than rewritten.
5. smartwatch-clank volume-deletion data loss (2026-08-23) — correctly avoided treating the restored-data return as fresh baseline/novelty.
6. smartphone-clank `wave1_baseline_state` repeatedly leaking into production schema via shared-working-tree `create_all()` behavior — zero data impact both times, but "still completely real and still unresolved" per the repo's own docs.

### Lineage notes (this survey)

The two repos' ontologies are structurally different in ways arguing against direct lineage (persisted canonical Device+SQLAlchemy/Alembic vs. ephemeral in-memory reconstruction from raw SQLite). **smartwatch-clank explicitly names `clank-architecture` (ADR-0006, DATA_SURVIVABILITY.md) as its continuity/epoch model's architectural authority** — inherited from a shared standards repo, not from smartphone-clank, and smartphone-clank has no equivalent module at all (a gap, not a difference in maturity). Both independently built "baseline must not fire novelty" mechanisms via different implementation strategies, no cross-citation — convergent design under shared naming/product-family conventions, not copying.

---

## Survey 5 — semiconductor-intelligence + clank-architecture

**semiconductor-intelligence** HEAD `8a356a3bc87bea0f0d95e66c072c8e8a629156d5`, up to date; untracked new files only. **Repo shape note**: contains two unrelated systems sharing one git tree (`semi_intel/` — Claims/Evidence/Signal Radar; `src/oem_radar/` — a separate OEM product-price tracker), explicitly flagged in `docs/TECHNICAL_DEBT.md:12-14` as needing extraction into a separate repository. Findings below are labeled by sub-system.
**clank-architecture** HEAD `e9c4a2b77f0a484171b01980469eee34971f8ee5`, up to date, no source changes.

### Part A — semiconductor-intelligence

**Cluster A** — `SignalItem.posted_at` (nullable, provider-asserted) vs `collected_at` (`_now`) distinct (models.py:538-600). Timestamp precedence chain for candidate aging: `posted_at` → normalized Radar observation → `collected_at`, with disclosed fallback logging. Independence-group origin selection uses `posted_at`, not insertion order — comment documents a real prior bug: "a prior version used id alone, which silently mispicked 'origin' for any group whose earliest-posted item wasn't also earliest-inserted" (independence.py:181-194) — a null `posted_at` is mapped to `datetime.max` (maximally late), so it can never win "origin," a deliberate absent-value-to-semantic-value mapping. `docs/CANDIDATE_INTELLIGENCE.md:50-54` explicitly documents that "novelty" has **three distinct, deliberately non-colliding meanings** in this codebase and names the collision risk. oem_radar sub-system: schema v2 migration explicitly suppresses false novelty from a migration boundary ("the diff engine... emits zero events for that wave").

**Cluster B** — `SignalMentionStatus`: RESOLVED/CANDIDATE/REJECTED/IGNORED — docstring: "an unknown TitleCase-shaped phrase stays a `candidate` row... until something resolves it... nothing downstream may treat a candidate mention as equivalent to a resolved one" — the direct fix for the Jensen Huang incident (below). `CandidateReviewDisposition` docstring explicitly reasons about cross-fleet vocabulary portability: "`OUT_OF_STOCK`... has no honest equivalent here... `DUPLICATE` takes its place." oem_radar: "Absence of a review row means NEW. Historical events are never backfilled"; `signal_to_noise_ratio` is null (not 0/infinity) with a *separate* explicit boolean for the zero-denominator case; confidence buckets include an explicit `unknown` bucket, never coerced numeric. `ClaimLinkSuggestion`: "Always starts PENDING... a suggestion is never a fact until human acceptance." PHASE0_AUDIT.md: canonical-entity table explicitly excludes Radar's baked-in provisional/unknown status — "canonical entities are confirmed only," a direct architectural response to invented certainty from absence.

**Cluster C** — `SignalItem` dedup: `(provider, external_id)` is authoritative; `content_hash` is secondary. `Evidence.content_hash` is a separate identity scheme, deliberately, because Evidence and SignalItem are different trust tiers. `Evidence.origin_signal_item_id` is nullable+unique specifically for promotion idempotency (confirmed in promotion.py: select-then-reuse). "Same entity" for canonical `Entity` resolution is decided only by explicit human resolution over exact normalized groups — never fuzzy/embedding-based (ENTITY_MATCH_VERIFICATION.md:80-82). **Root-cause incident**: Radar's `_find_story` created/joined a story from *one* matching shared entity with no clustering conservatism — root cause of `United States/The Six Fi` (0.927, highest-scored "story" in the DB) and "Jensen Huang" becoming a top story; a later hard-block filter was additive-only, never retroactively purging existing junk. oem_radar sub-system: an independent, mature identity cascade (exact URL/handle → vendor SKU → alias table → fuzzy) where every match records method+confidence, and low-confidence matches become a candidate link, never a silent merge.

**Cluster D** — Richest cluster in the fleet survey. Four-tier trust ladder: `SignalItem` (raw, immutable, "most never become Evidence at all") → `Evidence` (immutable, canonical, trusted) → `Claim` (falsifiable assertion, status OPEN/CONFIRMED/DEBUNKED/RETRACTED, with `ClaimEvidenceLink.stance` SUPPORTS/WEAKENS/CONTRADICTS — **a claim's truth-state is a synthesis over possibly-disagreeing evidence, not a single overwritten field**) → `ClaimEvent` (append-only audit trail, contradiction-checks "never change confidence or status by itself"). Confidence is architecturally forbidden from being an input to editorial_value ("enforced by a test") — a candidate can be low-confidence and high editorial value simultaneously. `SignalItem.raw_payload` is never overwritten once written, even across reprocessing — reprocessing creates a new `processing_version` and only replaces derived columns, never the raw source. oem_radar's parallel, independently-designed model: `listings`(one hot mutable `last_seen_at`)→`snapshots`(immutable, content-hash-deduped)→`products`(canonical)→`change_events`(derived diffs); confidence carried on *both* the product (parse quality) and the resolution link (identity certainty), kept separate, never merged into one score.

**Cluster E** — `Evidence` provenance fields include `external_id` explicitly kept distinct from the dedup key, "useful provenance for tracing... back to exactly what the source called it." `ClaimEvidenceLink` (fact-level) / `ClaimEvent` (change-level) / `ClaimLinkSuggestion.resolved_note` (human-decision-level) are three separate provenance records. oem_radar raw payloads are retained on disk under a sha256 path, reparseable forever after engine bugfixes without bloating the DB — independently motivated (storage cost) but structurally similar to clank-architecture's provenance-hash concerns. Provenance is redacted at the API boundary (`safe_error`) while retained in full in the store — a deliberate retention-vs-disclosure split, not evidence loss.

**Cluster F** — **The single most concrete baseline-flood evidence in the entire fleet survey**: PHASE0_AUDIT.md §2-3 — a live 58MB Radar DB import produced 11,150 mention rows with **zero canonical entities**, and its top-scored "stories" were confirmed artifacts of the unconservative single-entity-clustering flaw (see C), never retroactively purged when a later filter was added. This is precisely why the fresh `SignalCandidate`+independence-grouping layer was built instead of importing Radar's `stories` table as canonical. A resurfacing-logic rule prevents repeated/syndicated coverage from resetting a candidate's apparent freshness, with an explicit "Resurfaced" signal only after a genuine gap.

**Cluster G** — Genuinely N/A for semi_intel proper (confirmed by the `CandidateReviewDisposition` docstring's own reasoning about OUT_OF_STOCK having no honest equivalent). oem_radar sub-system has a literal, well-specified availability/lifecycle model: `products.status` (active/removed/pre_release/uncertain) plus a removal-detection rule requiring `removal_grace` (2 full successful passes) before emitting `product_removed` — failed/partial runs never trigger removals.

### Part A — Incidents

1. "Jensen Huang becomes a subject entity" / single-shared-entity clustering flaw (PHASE0_AUDIT.md §3) — squarely a data-semantic identity/dedup+canonical-fact-promotion conflation, not a concurrency issue.
2. Independence-group origin-selection bug: row-insertion-order mistaken for chronological origin (fixed, v1.0.0 Phase 2, regression-tested).
3. Explicitly checked and ruled OUT of this domain: the "double-write race on singleton settings" incident — pure concurrency/config-row defect, no data-semantic content.
4. Explicitly checked and confirmed IN this domain: the "idempotent, independently retryable pipeline" redesign — directly traceable to the same Radar identity/dedup and observation-vs-fact conflation root causes as #1.
5. `stale_run_threshold_minutes` dead configuration — a stuck-RUNNING job row was left invisible because a threshold setting had zero consumers; fix flags `degraded` but deliberately never rewrites the stuck row's own honest-but-stale `RUNNING` status.
6. PHASE0_AUDIT.md's own self-correction of stale numbers cited across its own prior sessions (73/78/80/84 → 90) — a direct example of stale-source-content (even the audit's own prior text) being caught by re-measurement rather than trusted.

### Part A — Lineage notes

Claims/Evidence/ClaimEvent stack: **independent** (PHASE0_AUDIT.md: Radar "has no claim/provenance layer, only story confidence label... nothing to merge"). `SignalItem`/proposal-layer/independence-grouping: **inherited-and-redesigned** from Signal Radar's flawed originals — a deliberate architectural correction, not a straight port. `processing_version` pattern: original engineering discipline, no upstream reference. oem_radar sub-system: fully independent of semi_intel (co-located only, explicitly flagged as unwanted co-location). **Notable reverse-direction lineage**: `CandidateReviewDisposition`'s docstring explicitly cites "the fleet's own Watch Clank's `SpecialistLeadReview`" as the pattern it aligns with (DUPLICATE in place of OUT_OF_STOCK) — semiconductor-intelligence consciously imported a cross-fleet vocabulary convention from watch-clank.

### Part B — clank-architecture (read-only evidence extraction; GIC-02/GIC-15 excluded, already cited in prior UI work)

| Citation | Status (as stated) | Cluster |
|---|---|---|
| GIC-01 "first_seen != new reference" | executable | A |
| GIC-03 "ZERO vs STAGNANT" | executable | B |
| GIC-08 "restored DB keeps lineage" | executable | D/F |
| GIC-09 "total loss -&gt; explicit NEW_EPOCH" | executable | A/F |
| GIC-14 "schema drift/unsupported schema" | executable | D/E |
| GIC-19 "qualification without rewriting history" | executable | D |
| GIC-20 "capability absent/unsupported/unknown tri-state" | executable | B |
| GIC-21 "directory sweep mistaken for inventory" | executable | C |
| GIC-22 "resource naming mistaken for identity" | registered_pending_fixture | C |
| GIC-25 "capability collapsed into false boolean" | executable | B |
| L-WATCH-002 "historical article treated as novelty" | Required register, fixture pending | A/F |
| DB-002 "baseline events pollute analytics" | Required register, fixture pending | F |
| CAPABILITY-ABSENCE "policy/config/deploy/unknown collapsed" | Required register, fixture pending | B |
| CROSS-CLANK-IDENTITY "same entity discovered by two Clanks" | open architecture issue | C |
| BASELINE-HANDOVER "replacement changes entity keys" | Required register, fixture pending | C |
| DB-LOSS-RESTORE "live volume deleted; older backup restored" | executable fixture | A/D/F |
| DB-LOSS-NEW-EPOCH "no backup; hard new epoch" | executable fixture | A/F |
| P4-G5 "BACKUP-NO-HASH" | fixture | E |
| P4-G6 "SMARTWATCH-HARVEST" | fixtures (both repos) | B/C |
| FLEET_LAWS.md Law 1 "Initialization/no-flood" | ACTIVE | F — explicitly cites "oem-radar staging runs pre-bankai main" as a violator |
| FLEET_LAWS.md Law 2 "Observation != novelty" | ACTIVE | A/F |
| FLEET_LAWS.md Law 6 "Provenance" | ACTIVE | E — specimen cites "SemInt d43481f claim-vs-ledger contradiction" |
| **ADR-0006 "Observational Continuity and Epoch Semantics"** | **PROPOSED — REVIEWED DRAFT, not yet ACTIVE** | A/D/F — full `ContinuityEvent` contract; "A fresh baseline is never novelty"; "UNKNOWN means UNKNOWN" |
| **ADR-0014 "Typed Evidence, Semantic Clocks, Lane Config"** | **PROPOSED — REVIEWED DRAFT, not yet ACTIVE** | A/D/E — `EvidenceEnvelope` compatibility tiers; "every timestamp carries its clock identity... unlabeled timestamps are treated as clock=UNKNOWN"; "Declaration/observation separation: configuration can never manufacture observations; observations can never rewrite declarations" |
| RISK_REGISTER.md R-001 "Repository head mistaken for deployed artifact" | Critical, open | C/E |
| DATA_SURVIVABILITY.md R10 "stale/wrong-backup restore" | designed control | D/E |

**These two ADRs are the single most important cross-reference this pass surfaced**: they are near-complete, already-written draft standards for exactly this domain, sitting unratified in a sibling repo.

---

## Survey 6 — diagnostic-clank (incident mining)

Clone HEAD `3667af0` (branch `diagnostic-clank-2026-08`, shallow clone, read-only). This repo is a staging/curriculum corpus (`diagnosticbench/`) plus a runtime-contract codebase (`clank-runtime`, `clank-fleet`) encoding lessons from fleet incidents. Several cited cases reference primary sources (`artifacts/clank-audit/CROSS_CLANK_LESSONS.md`, `FAILURE_TAXONOMY.md`) **not present in this clone** — flagged per-incident below.

### Incidents

1. **Baseline/first-crawl entities emitted as ordinary novelty (oem-radar)** — `FIRST_SEEN_BY_CLANK != NEW_TO_MARKET`. Remediation: `EXCLUDE_BASELINE_EVENTS_SQL` + meta flag. Cited: DB-002.yaml, SEED_FIRST_10.yaml:25-35. Evidence gap: primary source not in clone.
2. **Stale/historical watch-clank discovery surfaced as current novelty** — recurring class (CasioBlog/Timex). Remediation described as a required "freshness firewall," marked `CONFIRMED_L_PARTIAL_FIX` — not fully resolved. Cited: DB-008.yaml, L-WATCH-002.
3. **DSM scheduler single fire misread as proven hourly cadence** (oem-radar NAS canary, 2026-08-16) — an agent's single-observation claim was treated as proof of a recurring cadence; owner corrected it before cutover. Both the agent's claim and the owner's correction are modeled as distinct, **both-retained** claim records (`expected_fate: superseded` vs `retained`), not one overwriting the other. Remediation marked `PARTIAL`. Cited: DB-004.yaml, L-OEM-001.
4. **Zero/catalogue collapse counted as healthy success** (oem-radar primary; related: feature-phone-clank, smartwatch-clank) — failed/zero-result runs advanced "healthy" absence/baseline counters. Confirmed fleet-wide anti-pattern via shared `FailureClass.CATALOGUE_COLLAPSE`/`CHALLENGE_PAGE_AS_ZERO` enum members. Cited: DB-001.yaml; enums.py:119-148,70-87. Evidence gap: primary source not in clone.
5. **Operationally-healthy collectors masking newsroom recall failure** (BANKAI, oem-radar) — reportedly 0/50 qualifying stories recalled despite green collectors. Status explicitly `OPEN`, root cause `UNKNOWN`, `evidence_status: HISTORICAL_L_INCOMPLETE_EVIDENCE` — **treat as unconfirmed**, included per instructions to report severity-relevant near-misses even when evidence is thin. Cited: DB-003.yaml, L-OEM-003.
6. Beelink ME Pro HX 470 miss (oem-radar) — unverified stub, case explicitly warns "do not invent parser failure without evidence." Cited: L-OEM-004 only, no DB-* counterpart.
7. **Feature Phone Clank catastrophic-zero-as-normal-success** — sibling of #4; `blocked_zero_result` status, pipeline never invoked on blocked runs, regression-tested. Cited: DB-009.yaml.
8. Stale `.app` build vs. canonical bundle confusion (feature-phone-clank native client) — `BUILD_SUCCESS != OWNER_FIELD_TEST_ACCEPTANCE`; status `OPEN`, root cause `UNKNOWN`, evidence incomplete — borderline out of strict data/ontology domain (build/release identity, not fact truth). Cited: DB-010.yaml, L-PHONE-001.
9. **Tablet Clank absent from local workspace enumeration mistaken for fleet non-membership** — `LOCAL_WORKSPACE != CANONICAL_FLEET_INVENTORY`. Standing rule now documented in `clank-fleet/docs/FLEET_INVENTORY.md`, which itself warns operators not to "delete unknown systems to make fleet health appear green" — the underlying temptation is treated as an ongoing risk, not closed. Cited: L-FLEET-001 only, seed-stage.
10. **UUID-lexical ordering picked the wrong "latest" run** (smartphone-clank adapter, in diagnostic-clank's own `clank-fleet` code) — `last_run()` ordered by row `id` (a UUID, sorts lexicographically) instead of `finished_at`, risking false-STALE or false-HEALTHY reads. Fixed, adversarially regression-tested (`uuid_trap_db` fixture). Named "Motherclank M1.5 adapter truth-cleanup" — implies the bug class was found across multiple adapters by an external audit. Cited: clank-fleet/tests/test_m15_adapter_truth.py:1-11,63-135.
11. **Cross-adapter status-vocabulary collapse to UNKNOWN vs. false-upgrade risk** (watch-clank, smartphone-clank adapters) — native status vocabularies fell through to UNKNOWN before an explicit mapping was added; regression tests permanently guard that unmapped/ambiguous values must stay UNKNOWN and must never be upgraded to OK. Cited: test_m15_adapter_truth.py:1-9,28-61; feature_phone.py:49-75.
12. SQLite writer contention under timer fan-out (watch-clank) — infrastructure/concurrency, flagged as borderline out of domain, included because contention risked silent write loss (evidence-adjacent). Cited: DB-006.yaml, L-WATCH-001. Evidence gap: full report "still to be attached by owner corpus."
13. Watch Clank "Hall of Shame" — 12 real products/outcomes silently missed vs. competitor coverage, no internal signal existed to catch it. Borderline operational/discovery-coverage rather than pure meaning-representation. Cited: DB-007.yaml. Evidence gap: full per-item list and CROSS_CLANK_LESSONS source not in clone.
14. NAS dual-host delivery-authority ambiguity (oem-radar migration window) — borderline delivery/operational, included for completeness; modeled as `NotificationAuthorityRole` enum. Cited: DB-005.yaml, L-OEM-002.
15. Helldivers 2 PS Plus catalogue miss (free-game-tracker) — unverified stub, "catalogue path != subscription entitlement path," root cause `UNKNOWN`. Cited: L-FGT-001 only.
16. Samsung traversal succeeds but extracts zero valid devices (smartphone-clank) — unverified stub; "HTTP/traversal success != extraction success"; flags a "dual baseline authority risk." Cited: L-SMART-001 only.

### Cross-fleet data contracts found (evidence, not authoritative)

1. **Knowledge laws** (fixed vocabulary): `CLAIM_RECORDED != CLAIM_TRUE`, `LATEST_CLAIM != AUTHORITATIVE_TRUTH`, `DERIVED_KNOWLEDGE != RAW_EVIDENCE`, `RAW_EVIDENCE_IS_IMMUTABLE`, `CONTRADICTION != CORRUPTION`, `FIRST_SEEN_BY_CLANK != NEW_TO_MARKET`, `BUILD_SUCCESS != OWNER_FIELD_TEST_ACCEPTANCE`, `LOCAL_WORKSPACE != CANONICAL_FLEET_INVENTORY`, `AUTOMATED_VERIFIED != OWNER_ACCEPTED`. (DIAGNOSTICBENCH_V0_1.md:9-18)
2. **Semantic case schema** with an honesty gate (`evidence_status` ranging `CONFIRMED_L_CONFIRMED_FIX` … `SUSPECTED_L_DO_NOT_TREAT_AS_FACT`), `root_cause_must_not_be_invented`, `preserves_contradiction`. (DIAGNOSTICBENCH_V0_1_DESIGN.md:55-113)
3. **Incident/claim-history model, implemented**: claims are never edited/deleted; `supersede_claim()` inserts a new claim and marks the old `SUPERSEDED`/`DISPUTED`, original text/source/timestamp preserved permanently. `RootCauseCertainty`: UNKNOWN/HYPOTHESIS/REPORTED_CLAIM/CONFIRMED_FACT. (clank-runtime/.../knowledge/incidents.py:10-17,42-73,265-283)
4. **Agent Output Inbox**: content-hash dedup explicitly ≠ logical identity — a separate `external_ref` carries logical identity; changed content under the same ref inserts a new immutable versioned row. (knowledge/inbox.py:1,44-48,130-152,219-229)
5. **Append-only disposition ledger**, enforced by SQLite triggers rejecting UPDATE/DELETE (not just API convention); "canonical producer identity" rule refuses self-verification of one's own claim. (knowledge/dispositions.py:1-15,66-102,151-188)
6. **`EventEnvelope` draft contract** (Stage 0.5, not yet written to disk): `occurred_at` vs `observed_at` as separate fields; `source_references`/`evidence_references`/`domain_entity_references` as distinct link types; `correction_of` as an explicit supersession pointer (never in-place overwrite); multi-dimensional `confidence_dimensions` explicitly instructed to "never collapse to a single scalar." (contracts/events.py:1-56, contracts/confidence.py:1-30)
7. **`TelemetryEnvelope`**: `is_baseline: bool` directly on the per-event record; `lead_id` as stable dedupe/join key; `previous_observed_count` alongside counts to make deltas explicit rather than inferred. (contracts/telemetry.py:23-81)
8. **Shared enum vocabulary**: `SourceHealthStatus` (ZERO_ITEMS/BLOCKED_ZERO/NEVER_RUN distinct from UNKNOWN), `FailureClass` (BASELINE_POLLUTION/CATALOGUE_COLLAPSE/CHALLENGE_PAGE_AS_ZERO/DEDUPE_FAILURE/IDENTITY_FAILURE/FALSE_DELETION). "Prefer UNKNOWN over a false diagnosis." (contracts/enums.py)
9. `ClankAdapter` capability-declared protocol (ADR-0002) — unsupported operations raise, never silently default.
10. **Explicit rejection of full standardization**: `AUDIT_RECONCILIATION.md` records `DO_NOT_STANDARDISE` as an adopted position — "explicit heterogeneity preserved (identity, cadence, zero semantics)"; no central product identity service, no automatic source promotion, no single fleet-wide SQLite.
11. Canonical fleet inventory doctrine (`inventories/fleet.yaml` authoritative over filesystem enumeration; unknown fields stay literal UNKNOWN).
12. Ledger join-key contract (`lead_id` preferred, composite fallback; `originated_offline`+`synced_at` distinguish offline-authored records).
13. **"Null not zero" acceptance rule**: Stage 1A explicitly requires unavailable fields stay `null`, never `0`; "source-specific zero semantics preserved, not reinterpreted." Implemented: `# delivery not tracked — leave null, not zero` (feature_phone.py:346-347).

**Note on ADR-0002's `DO_NOT_STANDARDISE` position**: this is directly relevant to how Pass 0B should scope any future standard — diagnostic-clank has already, explicitly, considered and rejected full schema unification across the fleet, preserving "explicit heterogeneity" in identity/cadence/zero-semantics by design. A future data-ontology standard should reckon with this existing position, not silently override it.
