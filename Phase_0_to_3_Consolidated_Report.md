# SupeRR Selector Season 2 — Consolidated Report (Phases 0–3)

## Executive decision and refresh status

Phases 1–3 were rebuilt from the official updated delivery source. Source: `ball_by_ball updated.csv`; SHA-256 `01e2b4379edfbab6a6e456d304cb3c70f554cb312ef93d9588f3f32a82cb396e`. Phase 0 methodology governance remains unchanged. The updated file corrects extras-run values but does not eliminate the unresolved legal-ball cases, so the validated structural-pressure Phase 3 remains the official model.

The authoritative downstream files are `phase2_outputs/phase2_integrated_cleaned_deliveries.csv` and `phase3_outputs/phase3_structural_pressure_labelled.csv`. Root-level score/chase artifacts from the superseded implementation remain non-authoritative.

## Phase 0 — Methodology governance

The following rules remain binding: pressure is a pre-delivery state; IPL and T20I retain separate baselines; batter and bowler share the same pressure state on a delivery; unsupported cricket facts are not imputed; eligibility and reliability precede ranking; and uncertainty belongs in Phase 5.

## Phase 1 — Data audit

The six sources contain 237,170 total records. The approved population remains 813 matches and 192,235 regulation delivery records. The updated file preserves schema and keys but corrects `extras1_runs` into a run quantity and changes delivery-name observations from AHT Donald to Aneurin Donald.

| Population | Matches/records |
| --- | ---: |
| Target IPL and Men's T20I matches | 853 |
| Eligible completed matches | 813 |
| Regulation delivery records | 192,235 |
| Super Over records kept separately | 26 |

Player ID remains the identity key. The mapping-table alias for player 4458 is documented rather than merged or overwritten. All 11 Phase 1 gates pass, and the data dictionary and source-change audit are persisted in `phase1_outputs/`.

## Phase 2 — Validated analytical master

The refreshed analytical master contains 192,235 rows. Legal-ball evidence is now derived from `extras_type`, never from numeric `extras1_runs` values. There are 7,976 explicit wide/overstep records and 257 unresolved other/penalty records. All 11 Phase 2 validation gates pass.

| Evidence treatment | Records |
| --- | ---: |
| Explicit non-legal: wide/overstep | 7,976 |
| No recorded wide or overstep | 184,002 |
| Unresolved other/penalty | 257 |

The 147 extended overs without a recorded wide/overstep prevent a definitive legal-ball reconstruction. All delivery keys, over sequences, identity mappings, and attached context values pass their checks. The master preserves updated source values and records all exceptions explicitly.

## Phase 3 — Structural pressure model

The structural-pressure model remains appropriate because exact legal-ball progression is still unsupported. It labels 188,330 delivery records across 789 unrevised matches and excludes 24 revised/shortened matches. All 15 pipeline gates and 13 independent validation checks pass.

For each delivery, the model uses only state known before the current outcome: wickets already lost, wickets in the prior 12 delivery records, and source-over stage urgency. Expected wickets are leave-one-match-out by format, innings, and source over, with minimum support 100 and declared fallback levels.

The components are bounded as follows: positive wicket-strain z-scores are capped at 3 SD and divided by 3; recent wicket shock is prior-window wickets divided by 3 and capped at 1; stage urgency is `(overid - 1) / 19`. Their equal-weight mean is the continuous structural-pressure index. Low/Medium/High categories are descriptive within-format-and-innings percentile bands; the continuous index remains primary.

The primary dataset contains 30,290 match-state benchmark rows. Benchmark support ranges from 1,092 to 2,724. Sensitivity variants retain a minimum non-primary Spearman correlation of 0.9527.

## Validation and Phase 4 handoff

The refresh is reproducible through the consolidated notebook. Phase 3 manifest hashes are independently recomputed. Phase 4 must use only the authoritative pressure-labelled file, retain the pre-delivery construction, exclude revised matches, evaluate IPL and T20I separately, and preserve the full-period/no-recency-weight decision.
