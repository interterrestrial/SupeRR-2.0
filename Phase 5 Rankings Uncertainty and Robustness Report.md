# Phase 5 — Rankings, Uncertainty and Robustness Report

## Decision

Official rankings use unrounded Phase 4 combined ratings over the complete eligible 2022–2026 period. No recent-form weight is used. Bootstrap and sensitivity results diagnose uncertainty; they do not silently replace the official score order.

## Official top 10

| role | rank | player_name | qualifying_formats | combined_rating |
| --- | --- | --- | --- | --- |
| Batter | 1 | Nicholas Pooran | IPL | 62.2121 |
| Batter | 2 | Jimmy Neesham | T20I | 61.8456 |
| Batter | 3 | Hardik Pandya | IPL+T20I | 60.4830 |
| Batter | 4 | Jos Buttler | IPL | 60.3904 |
| Batter | 5 | Jaker Ali Anik | T20I | 60.1233 |
| Batter | 6 | Romario Shepherd | T20I | 59.2770 |
| Batter | 7 | Suryakumar Yadav | IPL+T20I | 59.2151 |
| Batter | 8 | Iftikhar Ahmed | T20I | 58.7742 |
| Batter | 9 | Shreyas Iyer | IPL | 58.4195 |
| Batter | 10 | Rinku Singh | IPL+T20I | 57.4293 |
| Bowler | 1 | Sufiyan Muqeem | T20I | 69.6668 |
| Bowler | 2 | Kuldeep Yadav | IPL+T20I | 65.2270 |
| Bowler | 3 | Sunil Narine | IPL | 64.9034 |
| Bowler | 4 | Mohammad Nawaz | T20I | 61.7880 |
| Bowler | 5 | Abrar Ahmed | T20I | 61.3492 |
| Bowler | 6 | Mitchell Starc | IPL | 61.0654 |
| Bowler | 7 | Eshan Malinga | IPL | 60.2697 |
| Bowler | 8 | Varun Chakravarthy | IPL+T20I | 60.2034 |
| Bowler | 9 | Suyash Sharma | IPL | 59.8166 |
| Bowler | 10 | Mohit Sharma | IPL | 59.8040 |

## Bootstrap design

The analysis uses 5,000 fixed-benchmark and 1,000 nested-benchmark stratified match replicates. IPL and T20I matches are resampled separately. Eligibility, shrinkage, normalization, format scores and combined ratings are recalculated in each replicate.

## Top-10 uncertainty

| role | rank | player_name | robustness_class | top10_frequency_fixed | top10_frequency_nested |
| --- | --- | --- | --- | --- | --- |
| Batter | 1 | Nicholas Pooran | BOUNDARY_TOP10 | 0.5704 | 0.5980 |
| Batter | 2 | Jimmy Neesham | BOUNDARY_TOP10 | 0.5204 | 0.5140 |
| Batter | 3 | Hardik Pandya | BOUNDARY_TOP10 | 0.6564 | 0.6510 |
| Batter | 4 | Jos Buttler | BOUNDARY_TOP10 | 0.3484 | 0.3570 |
| Batter | 5 | Jaker Ali Anik | BOUNDARY_TOP10 | 0.4266 | 0.4310 |
| Batter | 6 | Romario Shepherd | BOUNDARY_TOP10 | 0.2800 | 0.3110 |
| Batter | 7 | Suryakumar Yadav | BOUNDARY_TOP10 | 0.4732 | 0.4740 |
| Batter | 8 | Iftikhar Ahmed | BOUNDARY_TOP10 | 0.3260 | 0.3130 |
| Batter | 9 | Shreyas Iyer | BOUNDARY_TOP10 | 0.4046 | 0.4010 |
| Batter | 10 | Rinku Singh | BOUNDARY_TOP10 | 0.2950 | 0.2730 |
| Bowler | 1 | Sufiyan Muqeem | BOUNDARY_TOP10 | 0.4278 | 0.4520 |
| Bowler | 2 | Kuldeep Yadav | BOUNDARY_TOP10 | 0.7064 | 0.7400 |
| Bowler | 3 | Sunil Narine | BOUNDARY_TOP10 | 0.7124 | 0.6890 |
| Bowler | 4 | Mohammad Nawaz | BOUNDARY_TOP10 | 0.4450 | 0.4150 |
| Bowler | 5 | Abrar Ahmed | BOUNDARY_TOP10 | 0.3516 | 0.3820 |
| Bowler | 6 | Mitchell Starc | BOUNDARY_TOP10 | 0.4548 | 0.4420 |
| Bowler | 7 | Eshan Malinga | BOUNDARY_TOP10 | 0.2042 | 0.1790 |
| Bowler | 8 | Varun Chakravarthy | BOUNDARY_TOP10 | 0.2578 | 0.2530 |
| Bowler | 9 | Suyash Sharma | BOUNDARY_TOP10 | 0.3140 | 0.3150 |
| Bowler | 10 | Mohit Sharma | BOUNDARY_TOP10 | 0.3534 | 0.3590 |

Core top-10 players have at least 75% inclusion in both bootstrap modes. Other official selections remain valid by the locked full-data ranking but are identified as boundary cases. Challengers are reported separately rather than substituted automatically.

## Robustness

The deterministic suite contains 13 factor-at-a-time scenarios covering metric weights, eligibility thresholds, pressure definitions and format combination. Leave-one-player-out outcome benchmarks separately test benchmark self-influence.

## Validation

All 16 Phase 5 gates passed. The notebook reproduced the Phase 4 candidate population and combined ratings, reconciled exactly 10 top-10 selections per role in every bootstrap replicate and deterministic scenario, and verified that the updated dataset did not change the official combined-score hashes.

## Phase 6 handoff

Phase 6 should use the official rankings together with bootstrap inclusion, self-influence, scenario stability and boundary classifications when explaining each selection. It must distinguish full-data rank from uncertainty evidence and preserve provisional status for non-official candidates.
