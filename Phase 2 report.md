# SupeRR Selector Season 2 — Phase 2 Data Reconstruction

## Executive summary

Phase 2 was rebuilt from `ball_by_ball updated.csv`. The validated master contains **192,235** regulation delivery records, **813** eligible matches, **1,626** innings, and **61** columns. All 11 validation gates pass.

The rebuild preserves source values, normalizes only the documented dismissal spelling variant, derives legal-ball evidence from `extras_type`, attaches verified match/competition/team context, and records unresolved cases instead of imputing them.

## Population and scope

| Measure | Value |
| --- | ---: |
| Target matches | 853 |
| Eligible matches | 813 |
| Excluded incomplete/no-result matches | 40 |
| Regulation delivery records | 192,235 |
| Super Over records kept separately | 26 |
| Competitions represented | 136 |
| Integrated columns | 61 |

Super Overs are retained in the dismissal and identity evidence outputs but excluded from the regulation master used by Phase 3.

## Corrected runs and extras treatment

`extras1_runs` is now treated as a numeric extras-run quantity. `extras_type` supplies the event category. The prior code mapping (1=overstep, 2=wide, and so on) is superseded and is not used anywhere in the refreshed pipeline.

Wide and `Overstep` records provide explicit non-legal evidence (**7,976** records). Byes, leg-byes, and rows without an extras category are not marked non-legal. The **257** `other`/penalty records remain unresolved rather than being guessed.

| Evidence treatment | Records |
| --- | ---: |
| Explicit non-legal evidence: wide/overstep | 7,976 |
| No recorded wide or overstep | 184,002 |
| Unresolved other/penalty | 257 |
| **Total** | **192,235** |

One regulation row has no `extras_type` despite non-zero extras fields. It is preserved and separately registered. Non-zero `extras_2_runs` values are also preserved because their exact semantics are not fully documented.

## Legal-ball and over-sequence evidence

There are **147** overs with more than six delivery records but no recorded wide or overstep. This is why Phase 2 still does not claim definitive legal-ball progression.

All **30,921** recorded over sequences have unique, contiguous `over_ball_num` values from 1 through their recorded delivery count. `innings_ball_num` and `over_ball_num` remain delivery-record sequences, not guaranteed legal-ball counters.

## Dismissals and identities

All striker, non-striker, bowler, and populated dismissed-player competition/team/player mappings reconcile. The analytical copy normalizes `Obstracting the field` to `Obstructing the field` while retaining `dismissal_type_original`. One wicket lacks a dismissed-player ID, and 11 non-wicket records have populated dismissed-player IDs; neither condition is silently changed.

Player IDs remain the analytical identity key. Updated delivery names flow through the master, including `Aneurin Donald`; the mapping-table alias `AHT Donald` remains documented in Phase 1 rather than forcing an ID or name rewrite.

## Integrated master and consistency

The master retains all 33 updated delivery columns, adds original/normalized dismissal labels and three legal-ball evidence fields, and attaches match, competition, season, and team names. It has zero duplicate delivery keys, zero missing competition/team context values, and no unexpected or missing approved matches.

## Exception register

The refreshed exception register contains **30** audit entries. It covers 11 played registrations with missing batting order, 13 individual `other` records with secondary extras, 2 missing-extras-type inconsistency, 1 wicket with a missing dismissed-player ID, 11 non-wicket dismissed-player records, the dismissal spelling variant, and the aggregate legal-ball limitation. Entries may overlap in their underlying delivery evidence.

## Validation

The validation gates confirm exact source-key preservation, approved population counts, complete evidence classifications, expected wide/overstep and unresolved counts, contiguous over sequences, complete player/team mappings, and complete attached context. The CSV outputs were reread during downstream validation, and the manifest records every file's dimensions, bytes, and SHA-256 hash.

## Deliverables

The refreshed master, dismissal table, legal-ball evidence, over audit, unexplained-over register, identity audit, exception register, validation gates, completion summary, and hash manifest are in `phase2_outputs/`. The manifest records the official updated source name and SHA-256 hash.

## Downstream limitations

Phase 3 must not infer exact legal balls or balls remaining from unresolved records. Revised/shortened matches require separate treatment. Phase 4 may use batter runs and verified dismissal outcomes under its locked record filters, but must not relabel its run-suppression metric as conventional economy.
