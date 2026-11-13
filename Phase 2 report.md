# SupeRR Selector Season 2
## Phase 2 — Data Cleaning & Reconstruction Report

**Status:** Final validation and export completed; report pending review  
**Primary output:** Integrated regulation-delivery dataset

---

## 1. Executive Summary

Phase 2 focused on data cleaning and reconstruction of the cricket delivery dataset, including match eligibility, player identity, delivery classification, dismissal handling, innings and over sequence integrity, and preparation of an integrated analytical dataset.

The approved target population contained 853 matches. After applying the established eligibility criteria, 813 matches were retained, containing 192,235 regulation deliveries. A further 26 Super Over deliveries were retained separately.

The final integrated dataset contains:

- 192,235 regulation delivery records
- 813 eligible matches
- 136 competitions
- 61 columns
- Zero duplicate delivery keys
- Zero duplicate complete rows
- Zero unmatched batting or bowling team identities

The final dataset was exported in CSV and Parquet formats. Supporting audit files and the exception register were also saved.

**Important limitation:** The available source fields do not support a definitive legal-ball count for every delivery. Phase 2 therefore preserves evidence-based classifications and explicitly records unresolved cases rather than inventing classifications.

## 2. Match Population and Eligibility

| Population measure | Records |
|---|---:|
| Target matches | 853 |
| Eligible matches | 813 |
| Excluded matches | 40 |
| Eligible regulation deliveries | 192,235 |
| Super Over deliveries, kept separate | 26 |

The target population consisted of 371 T20 matches and 482 T20I matches. The eligible population consisted of 362 T20 matches and 451 T20I matches.

The 40 excluded matches comprised:
- 16 abandoned matches with no deliveries
- 3 abandoned matches with partial deliveries
- 19 No Result matches with one innings
- 2 No Result matches with two innings

Super Over deliveries were kept separate from the regulation-delivery population.

## 3. Data Quality and Reconstruction

### 3.1 Player identity

`player_id` was retained as the identity key. Player names were not treated as unique identifiers.

All observed striker, non-striker, bowler, and dismissed-player identities were matched against the appropriate competition-team-player mapping.

The team identity audit found:
- No unmatched striker identities
- No unmatched non-striker identities
- No unmatched bowler identities
- No unmatched dismissed-player identities

The composite team identity key `(comp_id, team_id)` was validated. All 1,626 home and away team references across the eligible matches matched the team table.

### 3.2 Dismissal classification

All 10,392 wicket deliveries in the eligible population had a recorded dismissal type.

The audit identified:
- One wicket record with a missing `dismissed_player_id`
- Eleven non-wicket records with a populated `dismissed_player_id`
- Two spelling variants of the same dismissal label

The spelling variants were normalized to `Obstructing the field` in the analytical copy. Original source labels were retained separately.

No missing dismissed-player IDs were imputed, and no non-wicket records were silently reclassified.

### 3.3 Extras and boundary anomalies

The source `extras1_runs` codes were mapped to descriptive evidence categories:

| Source code | Recorded category |
|---:|---|
| 1 | Overstep |
| 2 | Wide |
| 3 | Legbyes |
| 4 | Byes |
| 5 | Other |
| 6 | No extras |
| 7 | Penalty |

The audit identified 23 boundary-flag mismatches:
- 20 records with four runs but `is_four=False`
- 3 records with six runs but `is_six=False`

These source values were preserved rather than silently corrected.

The meaning of `extras_2_runs` remains unresolved. Non-zero values were documented in the exception register.

### 3.4 Innings and over sequence integrity

The regulation-delivery sequence audit covered 1,626 innings.

Results:
- No duplicate `innings_ball_num` values
- No gaps in the observed innings delivery sequence
- 30,921 overs audited
- No duplicate or non-contiguous `over_ball_num` sequences

The `over_ball_num` field was treated as a delivery sequence position, not as a legal-ball counter.

## 4. Legal-Ball Evidence Treatment

The legal-ball audit covered all 192,235 regulation deliveries.

| Evidence category | Delivery records |
|---|---:|
| Recorded wides | 7,419 |
| Recorded oversteps | 557 |
| Recorded other | 256 |
| Recorded penalty | 1 |
| Recorded byes | 505 |
| Recorded legbyes | 2,635 |
| Recorded no extras | 180,862 |
| **Total** | **192,235** |

The final evidence-based treatment was:

| Treatment | Delivery records |
|---|---:|
| Explicit non-legal evidence (wide/overstep) | 7,976 |
| No recorded wide or overstep | 184,002 |
| Unresolved | 257 |
| **Total** | **192,235** |

The 257 unresolved deliveries consist of 256 `other` records and one `Penalty` record.

The extended-over audit identified 6,450 overs containing more than six delivery records:
- 6,303 had at least one recorded wide or overstep.
- 147 had no recorded wide or overstep.

The 147 unexplained extended overs contained 1,036 delivery records.

**Limitation:** These classifications do not establish an exact legal-ball count. The source does not provide sufficient evidence to resolve every `other` or penalty record, and the 147 unexplained extended overs remain documented exceptions. No legal-ball status was imputed.

## 5. Integrated Dataset

The final integrated dataset combines the approved regulation-delivery population with:

- Match metadata
- Competition name, format, and season
- Batting and bowling team names
- Normalized dismissal labels
- Legal-ball evidence classifications

Final dimensions:

| Measure | Value |
|---|---:|
| Rows | 192,235 |
| Columns | 61 |
| Eligible matches | 813 |
| Competitions | 136 |
| Duplicate delivery keys | 0 |
| Duplicate complete rows | 0 |

All cross-table validation checks passed:
- Match-to-competition mismatches: 0
- Batting team name mismatches: 0
- Bowling team name mismatches: 0
- Approved matches missing: 0
- Unexpected matches: 0

Missing values were reviewed and retained where appropriate. For example, the single match with missing `win_team_id` was recorded as `Match Tied`; no winner was inferred.

## 6. Exception Register

The final exception register contains 24 entries across six exception types:

| Exception type | Entries |
|---|---:|
| Non-wicket with dismissed-player ID | 11 |
| Non-zero extras2 with recorded other | 9 |
| Missing played batting order | 1 |
| Wicket missing dismissed-player ID | 1 |
| Dismissal label spelling variant | 1 |
| Legal-ball reconstruction limitation | 1 |
| **Total** | **24** |

Exception entries can overlap in the underlying records. The register is an audit trail, not a count of 24 independent affected deliveries.

## 7. Exported Deliverables

All required export artifacts were verified as existing and non-empty.

| Artifact | Rows |
|---|---:|
| Integrated cleaned deliveries CSV | 192,235 |
| Integrated cleaned deliveries Parquet | 192,235 |
| Exception register | 24 |
| Legal-ball evidence | 192,235 |
| Unexplained extended-over register | 147 |
| Dismissal classified dataset | 192,261 |
| Team identity audit | 4 |
| Team identity exceptions | 0 |
| Over sequence audit | 30,921 |
| Export manifest | 8 |

The CSV and Parquet datasets were read back successfully. Their dimensions, column order, delivery keys, and critical classifications matched the in-memory dataset.

The `season` column was verified as a string field, preserving both single-year labels and cross-year labels such as `2022/23`.

The completion summary was also saved as `phase2_completion_summary.csv`.

## 8. Outstanding Limitations

The following limitations must remain explicit in subsequent phases:

1. The exact legal-ball count is not established for every delivery.
2. The 257 unresolved `other` and penalty records remain unclassified for legal-ball purposes.
3. The 147 unexplained extended overs cannot be fully explained using the available source fields.
4. The semantics of `extras_2_runs` remain unresolved.
5. Source boundary-flag mismatches were preserved rather than corrected.
6. Missing metadata was not imputed where the source did not support an inference.

These limitations should be considered when constructing downstream cricket performance metrics.

## 9. Phase 2 Conclusion

The Phase 2 reconstruction and integration work has produced a validated, traceable analytical delivery dataset with supporting audit artifacts.

The approved match population was preserved, identity mappings were validated, dismissal and extras anomalies were documented, innings and over sequences were checked, and the integrated dataset passed cross-table and export verification.

The work does not claim a complete legal-ball reconstruction where the source evidence is insufficient.

**Recommended handoff:** Use the Parquet dataset as the primary analytical input for subsequent Python-based work, retain the CSV as a portable copy, and carry the exception register and unresolved limitations into the next phase.

---

**Report status:** Draft for review  
**Dataset status:** Exported and verified  
**Exception register:** 24 entries  
**Formal Phase 2 approval:** Pending review and sign-off