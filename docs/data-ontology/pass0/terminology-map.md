# Pass 0A — Terminology Map

What each cross-cutting term actually means, per repo, as observed in code
(not assumed from the name). Compiled from [evidence-log.md](evidence-log.md).
Where a cell says "absent," the concept genuinely does not exist in that
repo's schema/code, as distinct from existing-but-conflated.

## Temporal fields

| Term | watch-clank | oem-radar | CTW | KTW | feature-phone-clank | tablet-clank | smartwatch-clank | smartphone-clank | semiconductor-intelligence |
|---|---|---|---|---|---|---|---|---|---|
| `first_seen`/`first_seen_at` | Not primary; identity created once, observations accumulate | `NormalizedProduct.first_seen` — observation bookkeeping, excluded from content hash | absent (uses `discovered_at`) | `articles.first_seen_at` — set once, never touched on update | `products.first_seen_at` | `products.first_seen_at` | `Device.first_seen` | `Device.first_seen` | `SignalCandidate.first_observed_at` |
| `discovered_at`/`observed_at` | `SourceObservation.observed_at` | implicit via snapshot `fetched_at` | `Article.discovered_at` — when crawler found it, distinct from `published_at` | `articles.discovered_at` | `Discovery.observed_at` — sole timestamp, excluded from change-detection basis | `NormalizedProduct.observed_at` — sole timestamp in live schema | `Observation.observed_at` | `Evidence.first_seen`/`last_seen` (system-observed) vs `published_at` (source-claimed) | `SignalItem.collected_at` |
| `published_at`/`announced_at` | Captured (Timex `published_at` in `extra_specs`); historically captured-but-unconsulted (INC-02) | `EvidenceItem.published_at` | `Article.published_at` — publisher's claimed time, distinct field | `articles.published_at` — extracted only from explicit OG/JSON-LD fields, never inferred | Lava `launch_date` — explicitly distrusted, quarantined to raw evidence only, never wired to pipeline | Research-stage only (Lenovo `Announce Date`) — doctrine exists ("FIRST_SEEN != NOVELTY"), no live field yet | absent (firmware_version misuse, INC-20, shows the *risk* of not having this) | absent as a modeled field (see "release_state" below) | `SignalItem.posted_at`, nullable, provider-asserted |
| "novelty"/"freshness" as a distinct concept | `app/services/freshness.py` — two explicit classifiers, discovery-novelty vs. editorial-freshness kept separate | `novelty_reason` field; explicit doctrine "observation time must never create noise" | `novelty_score` — collapses first-in-cluster + new-spec-content into **one scalar** (the one conflation point found) | Explicitly named gap: `docs/editorial-policy.md` says freshness judgment is deferred, not yet built | absent (no novelty/freshness scoring at all — pure discovery pipeline) | Doctrine-only, no scoring built yet | absent | absent | **Three distinct, deliberately non-colliding meanings**, explicitly documented as such (`docs/CANDIDATE_INTELLIGENCE.md`) |
| Epoch/continuity ledger | `OperationalEpoch` + a second `initial_fill.py` mechanism; production instance currently empty (INC-03, unresolved) | Doc-only cutover bookkeeping, no schema column | absent | absent | `core/continuity.py`, built after a real data-loss incident (INC-13) | absent | `core/continuity.py`, explicitly cites clank-architecture ADR-0006 as its authority | absent (an admitted, unresolved gap — schema-mutation-leak incident INC-19 has no epoch-boundary concept at all) | absent |

## Unknown/negative/absent state

| Term | watch-clank | oem-radar | CTW | KTW | feature-phone-clank | tablet-clank | smartwatch-clank | smartphone-clank | semiconductor-intelligence |
|---|---|---|---|---|---|---|---|---|---|
| Unknown vs. false vs. absent | `field_confidence`/`parser_warnings` preserve uncertainty; `safe_overall_confidence()` defaults to a conservative 50, never 0/100 | `Component.known: bool\|None` — explicit three-valued; `ValidationIssue.fatal` zeroes confidence, never drops the row | `certainty: confirmed\|probable\|unknown` on every "missed story" finding; explicit "never invents new certainty" | Three-way failure taxonomy separates infra noise from genuine defects | `Discovery` docstring: "unknown stays None," never invented | "Unknown values remain unknown; do not fabricate" (HANDOFF.md) | `Component`-equivalent not modeled the same way; SamsungRelationship enum structurally cannot assert unavailability | **"Release state defaults to unknown" is a hardcoded UI string with no backing field at all** — the flagship absence-of-real-model finding of this pass | `SignalMentionStatus`: RESOLVED/CANDIDATE/REJECTED/IGNORED, explicit "nothing downstream may treat candidate as resolved" |
| Availability vocabulary | `availability_status: str\|None` (free text), `AVAILABILITY_EVENT_TYPES = {SOLD_OUT, RESTOCK}` | `Availability` enum: IN_STOCK/PREORDER/SOLD_OUT/UNKNOWN (closed type, stronger typing) | n/a (news) | n/a (news) | `availability: str\|None`, populated by 3/N collectors, **never read by the diff/event pipeline** | **absent entirely** — no availability column anywhere in schema | `Observation.price/currency/availability` — first-class, richer `ChangeType` vocabulary than smartphone-clank | absent (see "release_state" above) | n/a for the claims/evidence layer; oem_radar sub-system has `products.status`: active/removed/pre_release/uncertain |
| QC-vocabulary "OUT_OF_STOCK"/"DUPLICATE" 4th disposition | `EventReview.DISPOSITIONS` includes `OUT_OF_STOCK`; `SpecialistLeadReview` uses `DUPLICATE` (two vocabularies, one repo) | n/a at review layer (alert_reviews: HIT/INTERESTING/NOISE/BUG, no OOS-equivalent) | `DUPLICATE` (LeadOutcome) | `DUPLICATE` (`QC_DECISIONS`) | `OUT_OF_STOCK` — **lineage: explicitly ported from watch-clank's `EventReview`**, but underlying `availability` field is unused | `OUT_OF_STOCK` — **lineage: explicitly ported from korean-tech-wire, NOT watch-clank** (corrects a standing assumption); no availability field backs it at all | n/a (no QC review layer found) | n/a (no QC review layer at all, per prior UI-domain audit) | `DUPLICATE` — docstring explicitly cites watch-clank's `SpecialistLeadReview` as its model |

## Entity identity

| Term | watch-clank | oem-radar | CTW | KTW | feature-phone-clank | tablet-clank | smartwatch-clank | smartphone-clank | semiconductor-intelligence |
|---|---|---|---|---|---|---|---|---|---|
| Canonical identity key | `(manufacturer, brand, reference_canonical)` | Hierarchical: FAMILY→MODEL→SKU/CONFIG→REGIONAL LISTING→URL, 6-way `IdentityDecision` cascade | exact URL + fuzzy title + entity overlap (3-tier, conservative) | `UNIQUE(source_id, canonical_url)` only — no cross-source dedup by design | `manufacturer:slug` (`product_key`), no cross-source merge by design | `manufacturer+(model_number\|SKU\|name)+region+connectivity+RAM+storage`, fallback admittedly under-distinguishing | opaque `identity: str`, per-run/per-source-class uniqueness only | `(manufacturer, model_number)`, DB-enforced unique constraint | `(provider, external_id)` for SignalItem; `content_hash` for Evidence (two different trust-tier identity schemes, deliberately) |
| Fuzzy/alias matching | Conservative, brand-specific allowlists only, no fuzzy matching | Yes — alias table + fuzzy config-signature match, every match records method+confidence | Yes — RapidFuzz title similarity + deterministic CJK/Latin alias map | **None at all** (explicit scope decision, treats cross-source overlap as corroboration signal, not redundancy) | None (no cross-source dedup attempted) | None (fallback is conservative pass-through, not fuzzy) | None (no alias table exists — a gap, not documented as deliberate) | Family-key stripping tuned for Samsung regional suffixes only | Exact-normalized-group human resolution only — explicitly never fuzzy/embedding-based |
| Known coarse-key false-merge incidents | — | **Yes, recurred twice independently** (Samsung/Lenovo tier-word bug; Evidence Fusion identity-linking bug) | Admitted risk, not yet incident: "brand overlap can soft-match different model numbers" | n/a (no merging attempted) | Yes — `IDENTITY_ANOMALY` duplicate-notification bug (fixed) | Yes — Apple Store carrier/unlocked URL dedup failure, 48 false events (fixed) | n/a in this pass's evidence | n/a (contamination incident was validation-gate absence, not a merge bug) | Yes — Signal Radar's single-shared-entity clustering flaw (Jensen Huang incident) |

## Observation vs. canonical fact — overwrite policy

| Repo | Can a later observation overwrite an already-set canonical value? |
|---|---|
| watch-clank | No confirmed overwrite path found for identity fields; new facts create new `SourceObservation` rows (not exhaustively verified against full pipeline — flagged gap) |
| oem-radar | Canonical "current" state = latest immutable snapshot; content-hash dedup means identical content never creates a new row, differing content always appends, never overwrites in place |
| chinese-tech-wire | COALESCE-style: a blank/None value in a new observation can never erase a known non-null fact; score fields (`novelty_score`) can only decrease on repeat, never re-inflate |
| korean-tech-wire | Same COALESCE pattern on enrichment fields, but `title_original`/`content_hash`/`raw_metadata` are **unconditionally overwritten** (latest-wins) on the same row — an undocumented, inconsistent policy split within one table |
| feature-phone-clank | Canonical `products` table carries identity fields only, never mutated; all spec state lives in append-only `observations` |
| tablet-clank | **Genuine architectural difference**: `products` spec columns ARE overwritten in place on each differing non-null observation; prior value preserved as `change_events.old_value` only if baseline is already complete |
| smartwatch-clank | `record_evidence()`: "never overwrites an earlier first_seen" — verified honored in code |
| smartphone-clank | Descriptive fields (marketing_name, codename, region) only filled if empty — first-writer-wins; identity fields immutable. Confidence has a single enforced writer (AST-scan-verified) |
| semiconductor-intelligence | `raw_payload` never overwritten even across reprocessing — a new `processing_version` replaces only derived columns |

## Confidence/certainty

| Repo | Confidence model |
|---|---|
| watch-clank | Per-field confidence dict + parser warnings; conservative default (50) on absence |
| oem-radar | **Two independent dimensions kept apart**: parse-quality confidence (on product) + identity-certainty confidence (on resolution link) — never merged into one score |
| chinese-tech-wire | `novelty_score` blends two distinct signals into one scalar (the one identified conflation point in an otherwise well-separated system) |
| korean-tech-wire | No confidence/scoring layer exists yet (pre-scoring maturity stage) |
| feature-phone-clank | No accumulating confidence score; append-only observation log serves as the "confidence" substitute (more observations = more corroboration, not formalized) |
| tablet-clank | Same as feature-phone-clank — no formal confidence score |
| smartwatch-clank | Single `Confidence` enum value per discovery, not an accumulating score |
| smartphone-clank | Per-contribution additive ledger (`ConfidenceLedgerEntry`), single enforced writer — but the only UI-visible "confidence drift" signal is a decorative badge that can structurally never fire (dossier bug); real drift computation exists but is unreachable from any UI/CLI path |
| semiconductor-intelligence | Six weighted components; **architecturally forbidden** (test-enforced) from being an input to editorial value — a claim can be low-confidence and high editorial value simultaneously |

## Fleet-wide "knowledge laws" (diagnostic-clank, evidence only — not authoritative for Standards Clank)

`CLAIM_RECORDED != CLAIM_TRUE` · `LATEST_CLAIM != AUTHORITATIVE_TRUTH` ·
`DERIVED_KNOWLEDGE != RAW_EVIDENCE` · `RAW_EVIDENCE_IS_IMMUTABLE` ·
`CONTRADICTION != CORRUPTION` · `FIRST_SEEN_BY_CLANK != NEW_TO_MARKET` ·
`BUILD_SUCCESS != OWNER_FIELD_TEST_ACCEPTANCE` ·
`LOCAL_WORKSPACE != CANONICAL_FLEET_INVENTORY` ·
`AUTOMATED_VERIFIED != OWNER_ACCEPTED`

These read as an informal, evolving draft of exactly the invariants this
pass independently found evidence for across the fleet. Cited here as a
cross-reference for Pass 0B, not adopted.
