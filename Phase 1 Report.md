# SupeRR Selector Season 2 — Phase 1 Data Audit

## Status and scope

Phase 1 was rerun from all six supplied datasets. The official delivery input is `ball_by_ball updated.csv` (SHA-256 `01e2b4379edfbab6a6e456d304cb3c70f554cb312ef93d9588f3f32a82cb396e`). The audit covers schemas, relationships, identity, match eligibility, delivery fields, missingness, and source changes. Pressure modelling and player scoring remain outside Phase 1.

## Dataset inventory

| Dataset | Rows | Columns | Exact duplicate rows |
| --- | ---: | ---: | ---: |
| Updated ball by ball | 200,999 | 33 | 0 |
| Playing eleven | 28,381 | 9 | 0 |
| Matches | 883 | 22 | 0 |
| Competition-team-player mapping | 6,413 | 6 | 0 |
| Teams | 353 | 3 | 0 |
| Competitions | 141 | 4 | 0 |
| **Total** | **237,170** | **77 across files** | **0 in each file** |

The updated delivery file contains 200,999 rows and 33 columns. Its match/innings/record key is unique, and every delivery match ID exists in the match registry. The machine-readable data dictionary profiles every field in every source.

## Updated-source comparison

The updated and original delivery files have identical shapes, columns, delivery keys, and row order. The update changes 199,980 `extras1_runs` cells, 24 striker-name cells, and 33 non-striker-name cells. `extras1_runs` must now be interpreted as an extras-run quantity, not as an extras-category code. `extras_type` remains the event-category field.

## Match coverage and eligibility

The match registry contains 883 matches; the delivery feed contains 867; the playing-eleven source contains 880. All delivery and playing-eleven match IDs reconcile to the registry. Matches without deliveries are abandoned matches.

| Population | Matches | Treatment |
| --- | ---: | --- |
| Target IPL and Men's T20I | 853 | Scope population |
| Eligible completed matches | 813 | Include |
| IPL eligible | 362 | Include |
| T20I eligible | 451 | Include |
| No Result or abandoned | 40 | Exclude from completed-match analysis |

The eligible population contains 192,235 regulation delivery records from innings 1 and 2. The 26 innings 3/4 records are retained separately as Super Overs and are not mixed into regulation analysis.

## Player identity and mappings

There are 1,217 observed player IDs and 1,211 names across delivery roles and the registration mapping. Player ID remains the identity key. One cross-source alias remains for player 4458: the updated delivery feed uses `Aneurin Donald`, while the mapping still uses `AHT Donald`. Seven names map to multiple IDs and remain namesakes rather than automatic merges. No player IDs are merged on name alone.

Playing-eleven registrations remain a squad/appearance source rather than a literal clean list of exactly 11 unique rows per side. Repeated registrations, non-playing rows, impact-player fields, and missing played batting orders remain source-level evidence and are not silently rewritten.

## Runs, extras, boundaries, and wickets

The corrected `extras1_runs` is consistent with a run quantity: no-extra rows almost always contain zero, wides range from 1–5, oversteps contain 1, and byes/leg-byes carry recorded run quantities. One row has no `extras_type` but non-zero extras fields and remains an explicit source exception. `extras_2_runs` is preserved because its precise relationship to the primary extras field is not fully documented.

Boundary flags and run values are preserved independently. Dismissal types and dismissed-player IDs are audited in Phase 2; missing or contradictory source values are not imputed.

## Legal-ball limitation

Exact legal-ball reconstruction remains unsupported for 257 `other`/penalty records. Phase 2 therefore continues to preserve evidence categories instead of inventing legal-ball status.

## Validation and deliverables

All 11 Phase 1 gates pass. The refreshed data dictionary, source inventory, source-change audit, quality table, and SHA-256 manifest are in `phase1_outputs/`. These artifacts establish the approved handoff to Phase 2.
