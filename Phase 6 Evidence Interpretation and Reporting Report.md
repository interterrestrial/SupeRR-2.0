# Phase 6 — Evidence, Interpretation and Reporting

## Decision

The official selections remain the locked Phase 5 top 10 batters and top 10 bowlers, ranked by unrounded full-period combined rating. Phase 6 adds evidence and interpretation only; it does not change eligibility, scores, format combination, or rank.

All 20 official selections are classified as `BOUNDARY_TOP10` under the predefined requirement of at least 75% top-10 inclusion in both bootstrap modes. They remain official because bootstrap inclusion measures stability, not the probability that a player is objectively top 10.

## Official selections

| role | rank | player | formats | rating | fixed_top10 | nested_top10 | top10_scenarios |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Batter | 1 | Nicholas Pooran | IPL | 62.2121 | 0.5704 | 0.5980 | 13 |
| Batter | 2 | Jimmy Neesham | T20I | 61.8456 | 0.5204 | 0.5140 | 11 |
| Batter | 3 | Hardik Pandya | IPL+T20I | 60.4830 | 0.6564 | 0.6510 | 10 |
| Batter | 4 | Jos Buttler | IPL | 60.3904 | 0.3484 | 0.3570 | 10 |
| Batter | 5 | Jaker Ali Anik | T20I | 60.1233 | 0.4266 | 0.4310 | 10 |
| Batter | 6 | Romario Shepherd | T20I | 59.2770 | 0.2800 | 0.3110 | 9 |
| Batter | 7 | Suryakumar Yadav | IPL+T20I | 59.2151 | 0.4732 | 0.4740 | 11 |
| Batter | 8 | Iftikhar Ahmed | T20I | 58.7742 | 0.3260 | 0.3130 | 11 |
| Batter | 9 | Shreyas Iyer | IPL | 58.4195 | 0.4046 | 0.4010 | 11 |
| Batter | 10 | Rinku Singh | IPL+T20I | 57.4293 | 0.2950 | 0.2730 | 7 |
| Bowler | 1 | Sufiyan Muqeem | T20I | 69.6668 | 0.4278 | 0.4520 | 12 |
| Bowler | 2 | Kuldeep Yadav | IPL+T20I | 65.2270 | 0.7064 | 0.7400 | 13 |
| Bowler | 3 | Sunil Narine | IPL | 64.9034 | 0.7124 | 0.6890 | 13 |
| Bowler | 4 | Mohammad Nawaz | T20I | 61.7880 | 0.4450 | 0.4150 | 11 |
| Bowler | 5 | Abrar Ahmed | T20I | 61.3492 | 0.3516 | 0.3820 | 11 |
| Bowler | 6 | Mitchell Starc | IPL | 61.0654 | 0.4548 | 0.4420 | 10 |
| Bowler | 7 | Eshan Malinga | IPL | 60.2697 | 0.2042 | 0.1790 | 7 |
| Bowler | 8 | Varun Chakravarthy | IPL+T20I | 60.2034 | 0.2578 | 0.2530 | 8 |
| Bowler | 9 | Suyash Sharma | IPL | 59.8166 | 0.3140 | 0.3150 | 8 |
| Bowler | 10 | Mohit Sharma | IPL | 59.8040 | 0.3534 | 0.3590 | 6 |

## Methodology used to interpret the rankings

- The official period is the complete eligible 2022–2026 dataset with no recent-form weighting.
- Pressure is assigned before the delivery outcome from wicket strain, recent wicket shock and innings-stage urgency. High pressure is the top within-format-and-innings 20% of the continuous index.
- Batters are evaluated on contextual scoring, survival and their pressure gradients. Bowlers are evaluated on contextual wicket-taking, run suppression and their pressure gradients.
- IPL and T20I are normalized independently. They are combined 50/50 only when both formats meet Reliable eligibility; an excluded format is never assigned zero.
- Outcome residuals compare the observed result with the expected result for format, innings, source over and pressure category. High-versus-ordinary tables are descriptive; the continuous gradients remain the direct pressure-response metrics.
- Uncertainty uses 5,000 fixed-benchmark and 1,000 nested-benchmark match-level replicates, 13 deterministic scenarios and leave-one-player-out benchmark sensitivity.

## Why some selections use only one format

| role | player | used_format | excluded_format | status | reason |
| --- | --- | --- | --- | --- | --- |
| Batter | Nicholas Pooran | IPL | T20I | Provisional | high_records 62 < 80 |
| Batter | Jimmy Neesham | T20I | IPL | Insufficient | high_records 14 < 80; high_matches 2 < 8; ordinary_records 13 < 160 |
| Batter | Jos Buttler | IPL | T20I | Provisional | high_records 50 < 80 |
| Batter | Jaker Ali Anik | T20I | IPL | No observed records | no player-format performance record in supplied analytical population |
| Batter | Romario Shepherd | T20I | IPL | Insufficient | ordinary_records 32 < 160 |
| Batter | Iftikhar Ahmed | T20I | IPL | No observed records | no player-format performance record in supplied analytical population |
| Batter | Shreyas Iyer | IPL | T20I | Provisional | high_records 40 < 80 |
| Bowler | Sufiyan Muqeem | T20I | IPL | No observed records | no player-format performance record in supplied analytical population |
| Bowler | Sunil Narine | IPL | T20I | No observed records | no player-format performance record in supplied analytical population |
| Bowler | Mohammad Nawaz | T20I | IPL | No observed records | no player-format performance record in supplied analytical population |
| Bowler | Abrar Ahmed | T20I | IPL | No observed records | no player-format performance record in supplied analytical population |
| Bowler | Mitchell Starc | IPL | T20I | Insufficient | high_records 34 < 100; high_matches 5 < 8; ordinary_records 128 < 200; high_clean_records 31 < 80; ordinary_clean_records 113 < 160 |
| Bowler | Eshan Malinga | IPL | T20I | Insufficient | high_records 45 < 100; high_clean_records 36 < 80 |
| Bowler | Suyash Sharma | IPL | T20I | No observed records | no player-format performance record in supplied analytical population |
| Bowler | Mohit Sharma | IPL | T20I | No observed records | no player-format performance record in supplied analytical population |

No observed record means no player-format performance row exists in the supplied analytical population. It does not support a claim about matches outside the supplied data.

## Batter evidence
### 1. Nicholas Pooran

- **Selection:** Ranks #1 among batters with an official combined rating of 62.21, using reliable IPL evidence. The strongest weighted component is IPL scoring quality (+0.81 weighted z); the weakest is IPL scoring pressure gradient (-0.17).
- **Formats:** The official score is the IPL rating of 62.21. T20I evidence is Provisional and is excluded because high_records 62 < 80. The excluded format is not assigned zero.
- **Pressure evidence:** IPL: high-pressure scoring residual +42.06/100 and survival residual +3.44/100 versus context; ordinary residuals +13.11 and +0.59; continuous scoring/survival gradients -27.42/+8.12.
- **Uncertainty:** Top-10 inclusion is 57.0% in the fixed-benchmark bootstrap and 59.8% in the nested bootstrap. The player remains top 10 in 13/13 deterministic scenarios. Leave-one-player-out benchmarking changes the rating by +0.044 and rank by +0; top-10 membership does not change. Classification: BOUNDARY_TOP10. Bootstrap inclusion measures ranking stability, not the probability of being objectively top 10.

### 2. Jimmy Neesham

- **Selection:** Ranks #2 among batters with an official combined rating of 61.85, using reliable T20I evidence. The strongest weighted component is T20I scoring quality (+0.41 weighted z); the weakest is T20I survival quality (+0.24).
- **Formats:** The official score is the T20I rating of 61.85. IPL evidence is Insufficient and is excluded because high_records 14 < 80; high_matches 2 < 8; ordinary_records 13 < 160. The excluded format is not assigned zero.
- **Pressure evidence:** T20I: high-pressure scoring residual +29.52/100 and survival residual +3.11/100 versus context; ordinary residuals -12.37 and -1.81; continuous scoring/survival gradients +75.92/+17.52.
- **Uncertainty:** Top-10 inclusion is 52.0% in the fixed-benchmark bootstrap and 51.4% in the nested bootstrap. The player remains top 10 in 11/13 deterministic scenarios. Leave-one-player-out benchmarking changes the rating by +0.029 and rank by +0; top-10 membership does not change. Classification: BOUNDARY_TOP10. Bootstrap inclusion measures ranking stability, not the probability of being objectively top 10.

### 3. Hardik Pandya

- **Selection:** Ranks #3 among batters with an official combined rating of 60.48, using reliable IPL+T20I evidence. The strongest weighted component is T20I scoring quality (+0.72 weighted z); the weakest is IPL survival pressure gradient (+0.01).
- **Formats:** IPL rating 55.47 and T20I rating 65.49 are combined 50/50. T20I is higher by 10.02 rating points.
- **Pressure evidence:** IPL: high-pressure scoring residual +19.60/100 and survival residual +2.54/100 versus context; ordinary residuals -16.59 and +0.45; continuous scoring/survival gradients +50.20/+2.21. T20I: high-pressure scoring residual +65.06/100 and survival residual +4.31/100 versus context; ordinary residuals -12.44 and +1.60; continuous scoring/survival gradients +101.28/+5.86.
- **Uncertainty:** Top-10 inclusion is 65.6% in the fixed-benchmark bootstrap and 65.1% in the nested bootstrap. The player remains top 10 in 10/13 deterministic scenarios. Leave-one-player-out benchmarking changes the rating by +0.113 and rank by +0; top-10 membership does not change. Classification: BOUNDARY_TOP10. Bootstrap inclusion measures ranking stability, not the probability of being objectively top 10.

### 4. Jos Buttler

- **Selection:** Ranks #4 among batters with an official combined rating of 60.39, using reliable IPL evidence. The strongest weighted component is IPL scoring quality (+0.46 weighted z); the weakest is IPL survival pressure gradient (-0.00).
- **Formats:** The official score is the IPL rating of 60.39. T20I evidence is Provisional and is excluded because high_records 50 < 80. The excluded format is not assigned zero.
- **Pressure evidence:** IPL: high-pressure scoring residual +39.05/100 and survival residual +4.45/100 versus context; ordinary residuals -3.17 and +1.28; continuous scoring/survival gradients +61.55/+1.88.
- **Uncertainty:** Top-10 inclusion is 34.8% in the fixed-benchmark bootstrap and 35.7% in the nested bootstrap. The player remains top 10 in 10/13 deterministic scenarios. Leave-one-player-out benchmarking changes the rating by -0.151 and rank by +0; top-10 membership does not change. Classification: BOUNDARY_TOP10. Bootstrap inclusion measures ranking stability, not the probability of being objectively top 10.

### 5. Jaker Ali Anik

- **Selection:** Ranks #5 among batters with an official combined rating of 60.12, using reliable T20I evidence. The strongest weighted component is T20I scoring quality (+0.52 weighted z); the weakest is T20I survival pressure gradient (-0.04).
- **Formats:** The official score is the T20I rating of 60.12. IPL evidence is No observed records and is excluded because no player-format performance record in supplied analytical population. The excluded format is not assigned zero.
- **Pressure evidence:** T20I: high-pressure scoring residual +29.15/100 and survival residual +2.07/100 versus context; ordinary residuals -24.32 and +0.92; continuous scoring/survival gradients +90.13/+0.76.
- **Uncertainty:** Top-10 inclusion is 42.7% in the fixed-benchmark bootstrap and 43.1% in the nested bootstrap. The player remains top 10 in 10/13 deterministic scenarios. Leave-one-player-out benchmarking changes the rating by +0.013 and rank by +0; top-10 membership does not change. Classification: BOUNDARY_TOP10. Bootstrap inclusion measures ranking stability, not the probability of being objectively top 10.

### 6. Romario Shepherd

- **Selection:** Ranks #6 among batters with an official combined rating of 59.28, using reliable T20I evidence. The strongest weighted component is T20I scoring quality (+0.47 weighted z); the weakest is T20I scoring pressure gradient (-0.14).
- **Formats:** The official score is the T20I rating of 59.28. IPL evidence is Insufficient and is excluded because ordinary_records 32 < 160. The excluded format is not assigned zero.
- **Pressure evidence:** T20I: high-pressure scoring residual +24.05/100 and survival residual +3.23/100 versus context; ordinary residuals +0.43 and -0.16; continuous scoring/survival gradients -18.47/+11.65.
- **Uncertainty:** Top-10 inclusion is 28.0% in the fixed-benchmark bootstrap and 31.1% in the nested bootstrap. The player remains top 10 in 9/13 deterministic scenarios. Leave-one-player-out benchmarking changes the rating by +0.210 and rank by +0; top-10 membership does not change. Classification: BOUNDARY_TOP10. Bootstrap inclusion measures ranking stability, not the probability of being objectively top 10.

### 7. Suryakumar Yadav

- **Selection:** Ranks #7 among batters with an official combined rating of 59.22, using reliable IPL+T20I evidence. The strongest weighted component is IPL scoring quality (+0.81 weighted z); the weakest is T20I survival pressure gradient (-0.06).
- **Formats:** IPL rating 62.20 and T20I rating 56.23 are combined 50/50. IPL is higher by 5.98 rating points.
- **Pressure evidence:** IPL: high-pressure scoring residual +47.70/100 and survival residual +2.66/100 versus context; ordinary residuals +17.46 and +0.68; continuous scoring/survival gradients +53.40/+1.12. T20I: high-pressure scoring residual +47.35/100 and survival residual +1.14/100 versus context; ordinary residuals +29.86 and +0.83; continuous scoring/survival gradients +5.95/-0.71.
- **Uncertainty:** Top-10 inclusion is 47.3% in the fixed-benchmark bootstrap and 47.4% in the nested bootstrap. The player remains top 10 in 11/13 deterministic scenarios. Leave-one-player-out benchmarking changes the rating by +0.103 and rank by +0; top-10 membership does not change. Classification: BOUNDARY_TOP10. Bootstrap inclusion measures ranking stability, not the probability of being objectively top 10.

### 8. Iftikhar Ahmed

- **Selection:** Ranks #8 among batters with an official combined rating of 58.77, using reliable T20I evidence. The strongest weighted component is T20I scoring quality (+0.47 weighted z); the weakest is T20I survival pressure gradient (+0.01).
- **Formats:** The official score is the T20I rating of 58.77. IPL evidence is No observed records and is excluded because no player-format performance record in supplied analytical population. The excluded format is not assigned zero.
- **Pressure evidence:** T20I: high-pressure scoring residual +33.49/100 and survival residual +2.02/100 versus context; ordinary residuals -21.21 and +0.11; continuous scoring/survival gradients +88.30/+3.63.
- **Uncertainty:** Top-10 inclusion is 32.6% in the fixed-benchmark bootstrap and 31.3% in the nested bootstrap. The player remains top 10 in 11/13 deterministic scenarios. Leave-one-player-out benchmarking changes the rating by -0.041 and rank by +0; top-10 membership does not change. Classification: BOUNDARY_TOP10. Bootstrap inclusion measures ranking stability, not the probability of being objectively top 10.

### 9. Shreyas Iyer

- **Selection:** Ranks #9 among batters with an official combined rating of 58.42, using reliable IPL evidence. The strongest weighted component is IPL scoring quality (+0.81 weighted z); the weakest is IPL survival quality (-0.20).
- **Formats:** The official score is the IPL rating of 58.42. T20I evidence is Provisional and is excluded because high_records 40 < 80. The excluded format is not assigned zero.
- **Pressure evidence:** IPL: high-pressure scoring residual +46.00/100 and survival residual -0.25/100 versus context; ordinary residuals +9.33 and +1.37; continuous scoring/survival gradients +80.59/-2.87.
- **Uncertainty:** Top-10 inclusion is 40.5% in the fixed-benchmark bootstrap and 40.1% in the nested bootstrap. The player remains top 10 in 11/13 deterministic scenarios. Leave-one-player-out benchmarking changes the rating by -0.035 and rank by +0; top-10 membership does not change. Classification: BOUNDARY_TOP10. Bootstrap inclusion measures ranking stability, not the probability of being objectively top 10.

### 10. Rinku Singh

- **Selection:** Ranks #10 among batters with an official combined rating of 57.43, using reliable IPL+T20I evidence. The strongest weighted component is T20I scoring quality (+0.58 weighted z); the weakest is T20I survival pressure gradient (-0.04).
- **Formats:** IPL rating 57.36 and T20I rating 57.50 are combined 50/50. T20I is higher by 0.13 rating points.
- **Pressure evidence:** IPL: high-pressure scoring residual +15.13/100 and survival residual +3.54/100 versus context; ordinary residuals -8.61 and +1.24; continuous scoring/survival gradients +25.07/+3.26. T20I: high-pressure scoring residual +39.01/100 and survival residual +3.01/100 versus context; ordinary residuals +3.71 and +1.99; continuous scoring/survival gradients +16.25/+0.67.
- **Uncertainty:** Top-10 inclusion is 29.5% in the fixed-benchmark bootstrap and 27.3% in the nested bootstrap. The player remains top 10 in 7/13 deterministic scenarios. Leave-one-player-out benchmarking changes the rating by +0.084 and rank by +0; top-10 membership does not change. Classification: BOUNDARY_TOP10. Bootstrap inclusion measures ranking stability, not the probability of being objectively top 10.

## Bowler evidence
### 1. Sufiyan Muqeem

- **Selection:** Ranks #1 among bowlers with an official combined rating of 69.67, using reliable T20I evidence. The strongest weighted component is T20I wicket quality (+1.03 weighted z); the weakest is T20I run suppression pressure gradient (+0.09).
- **Formats:** The official score is the T20I rating of 69.67. IPL evidence is No observed records and is excluded because no player-format performance record in supplied analytical population. The excluded format is not assigned zero.
- **Pressure evidence:** T20I: high-pressure wicket residual +5.70/100 and run-suppression residual +31.28/100 versus context; ordinary residuals -1.19 and +18.13; continuous wicket/run-suppression gradients +11.79/+41.18.
- **Uncertainty:** Top-10 inclusion is 42.8% in the fixed-benchmark bootstrap and 45.2% in the nested bootstrap. The player remains top 10 in 12/13 deterministic scenarios. Leave-one-player-out benchmarking changes the rating by -0.057 and rank by +0; top-10 membership does not change. Classification: BOUNDARY_TOP10. Bootstrap inclusion measures ranking stability, not the probability of being objectively top 10.

### 2. Kuldeep Yadav

- **Selection:** Ranks #2 among bowlers with an official combined rating of 65.23, using reliable IPL+T20I evidence. The strongest weighted component is T20I wicket quality (+1.03 weighted z); the weakest is T20I run suppression pressure gradient (-0.01).
- **Formats:** IPL rating 63.89 and T20I rating 66.57 are combined 50/50. T20I is higher by 2.68 rating points.
- **Pressure evidence:** IPL: high-pressure wicket residual +2.94/100 and run-suppression residual +7.42/100 versus context; ordinary residuals +0.01 and +5.00; continuous wicket/run-suppression gradients +4.46/+38.16. T20I: high-pressure wicket residual +12.05/100 and run-suppression residual +19.43/100 versus context; ordinary residuals +1.71 and +14.13; continuous wicket/run-suppression gradients +10.98/+9.25.
- **Uncertainty:** Top-10 inclusion is 70.6% in the fixed-benchmark bootstrap and 74.0% in the nested bootstrap. The player remains top 10 in 13/13 deterministic scenarios. Leave-one-player-out benchmarking changes the rating by +0.037 and rank by +1; top-10 membership does not change. Classification: BOUNDARY_TOP10. Bootstrap inclusion measures ranking stability, not the probability of being objectively top 10.

### 3. Sunil Narine

- **Selection:** Ranks #3 among bowlers with an official combined rating of 64.90, using reliable IPL evidence. The strongest weighted component is IPL run suppression quality (+0.56 weighted z); the weakest is IPL run suppression pressure gradient (+0.08).
- **Formats:** The official score is the IPL rating of 64.90. T20I evidence is No observed records and is excluded because no player-format performance record in supplied analytical population. The excluded format is not assigned zero.
- **Pressure evidence:** IPL: high-pressure wicket residual +1.98/100 and run-suppression residual +31.02/100 versus context; ordinary residuals -0.69 and +27.59; continuous wicket/run-suppression gradients +4.75/+24.71.
- **Uncertainty:** Top-10 inclusion is 71.2% in the fixed-benchmark bootstrap and 68.9% in the nested bootstrap. The player remains top 10 in 13/13 deterministic scenarios. Leave-one-player-out benchmarking changes the rating by +0.431 and rank by -1; top-10 membership does not change. Classification: BOUNDARY_TOP10. Bootstrap inclusion measures ranking stability, not the probability of being objectively top 10.

### 4. Mohammad Nawaz

- **Selection:** Ranks #4 among bowlers with an official combined rating of 61.79, using reliable T20I evidence. The strongest weighted component is T20I wicket quality (+0.62 weighted z); the weakest is T20I run suppression pressure gradient (+0.10).
- **Formats:** The official score is the T20I rating of 61.79. IPL evidence is No observed records and is excluded because no player-format performance record in supplied analytical population. The excluded format is not assigned zero.
- **Pressure evidence:** T20I: high-pressure wicket residual +2.56/100 and run-suppression residual +18.47/100 versus context; ordinary residuals +1.55 and +9.40; continuous wicket/run-suppression gradients +2.38/+36.09.
- **Uncertainty:** Top-10 inclusion is 44.5% in the fixed-benchmark bootstrap and 41.5% in the nested bootstrap. The player remains top 10 in 11/13 deterministic scenarios. Leave-one-player-out benchmarking changes the rating by +0.005 and rank by +0; top-10 membership does not change. Classification: BOUNDARY_TOP10. Bootstrap inclusion measures ranking stability, not the probability of being objectively top 10.

### 5. Abrar Ahmed

- **Selection:** Ranks #5 among bowlers with an official combined rating of 61.35, using reliable T20I evidence. The strongest weighted component is T20I run suppression quality (+0.53 weighted z); the weakest is T20I run suppression pressure gradient (+0.14).
- **Formats:** The official score is the T20I rating of 61.35. IPL evidence is No observed records and is excluded because no player-format performance record in supplied analytical population. The excluded format is not assigned zero.
- **Pressure evidence:** T20I: high-pressure wicket residual +1.05/100 and run-suppression residual +27.99/100 versus context; ordinary residuals +1.07 and +11.97; continuous wicket/run-suppression gradients +3.01/+45.40.
- **Uncertainty:** Top-10 inclusion is 35.2% in the fixed-benchmark bootstrap and 38.2% in the nested bootstrap. The player remains top 10 in 11/13 deterministic scenarios. Leave-one-player-out benchmarking changes the rating by +0.027 and rank by +0; top-10 membership does not change. Classification: BOUNDARY_TOP10. Bootstrap inclusion measures ranking stability, not the probability of being objectively top 10.

### 6. Mitchell Starc

- **Selection:** Ranks #6 among bowlers with an official combined rating of 61.07, using reliable IPL evidence. The strongest weighted component is IPL wicket quality (+0.91 weighted z); the weakest is IPL run suppression quality (-0.26).
- **Formats:** The official score is the IPL rating of 61.07. T20I evidence is Insufficient and is excluded because high_records 34 < 100; high_matches 5 < 8; ordinary_records 128 < 200; high_clean_records 31 < 80; ordinary_clean_records 113 < 160. The excluded format is not assigned zero.
- **Pressure evidence:** IPL: high-pressure wicket residual +5.00/100 and run-suppression residual -16.68/100 versus context; ordinary residuals +0.86 and -20.05; continuous wicket/run-suppression gradients +7.58/+46.33.
- **Uncertainty:** Top-10 inclusion is 45.5% in the fixed-benchmark bootstrap and 44.2% in the nested bootstrap. The player remains top 10 in 10/13 deterministic scenarios. Leave-one-player-out benchmarking changes the rating by -0.029 and rank by +0; top-10 membership does not change. Classification: BOUNDARY_TOP10. Bootstrap inclusion measures ranking stability, not the probability of being objectively top 10.

### 7. Eshan Malinga

- **Selection:** Ranks #7 among bowlers with an official combined rating of 60.27, using reliable IPL evidence. The strongest weighted component is IPL wicket quality (+0.56 weighted z); the weakest is IPL run suppression pressure gradient (+0.06).
- **Formats:** The official score is the IPL rating of 60.27. T20I evidence is Insufficient and is excluded because high_records 45 < 100; high_clean_records 36 < 80. The excluded format is not assigned zero.
- **Pressure evidence:** IPL: high-pressure wicket residual +3.05/100 and run-suppression residual +15.56/100 versus context; ordinary residuals +0.98 and +1.78; continuous wicket/run-suppression gradients +5.31/+28.69.
- **Uncertainty:** Top-10 inclusion is 20.4% in the fixed-benchmark bootstrap and 17.9% in the nested bootstrap. The player remains top 10 in 7/13 deterministic scenarios. Leave-one-player-out benchmarking changes the rating by -0.228 and rank by +1; top-10 membership does not change. Classification: BOUNDARY_TOP10. Bootstrap inclusion measures ranking stability, not the probability of being objectively top 10.

### 8. Varun Chakravarthy

- **Selection:** Ranks #8 among bowlers with an official combined rating of 60.20, using reliable IPL+T20I evidence. The strongest weighted component is T20I wicket quality (+0.94 weighted z); the weakest is T20I wicket pressure gradient (+0.02).
- **Formats:** IPL rating 58.27 and T20I rating 62.13 are combined 50/50. T20I is higher by 3.86 rating points.
- **Pressure evidence:** IPL: high-pressure wicket residual +1.40/100 and run-suppression residual +17.62/100 versus context; ordinary residuals +0.45 and +6.01; continuous wicket/run-suppression gradients +0.87/+26.67. T20I: high-pressure wicket residual +4.02/100 and run-suppression residual +13.74/100 versus context; ordinary residuals +3.04 and +0.99; continuous wicket/run-suppression gradients +0.04/+22.90.
- **Uncertainty:** Top-10 inclusion is 25.8% in the fixed-benchmark bootstrap and 25.3% in the nested bootstrap. The player remains top 10 in 8/13 deterministic scenarios. Leave-one-player-out benchmarking changes the rating by +0.123 and rank by -1; top-10 membership does not change. Classification: BOUNDARY_TOP10. Bootstrap inclusion measures ranking stability, not the probability of being objectively top 10.

### 9. Suyash Sharma

- **Selection:** Ranks #9 among bowlers with an official combined rating of 59.82, using reliable IPL evidence. The strongest weighted component is IPL wicket quality (+0.52 weighted z); the weakest is IPL wicket pressure gradient (+0.04).
- **Formats:** The official score is the IPL rating of 59.82. T20I evidence is No observed records and is excluded because no player-format performance record in supplied analytical population. The excluded format is not assigned zero.
- **Pressure evidence:** IPL: high-pressure wicket residual +2.37/100 and run-suppression residual +16.82/100 versus context; ordinary residuals -1.96 and -10.51; continuous wicket/run-suppression gradients +0.99/+54.88.
- **Uncertainty:** Top-10 inclusion is 31.4% in the fixed-benchmark bootstrap and 31.5% in the nested bootstrap. The player remains top 10 in 8/13 deterministic scenarios. Leave-one-player-out benchmarking changes the rating by -0.028 and rank by +1; top-10 membership does not change. Classification: BOUNDARY_TOP10. Bootstrap inclusion measures ranking stability, not the probability of being objectively top 10.

### 10. Mohit Sharma

- **Selection:** Ranks #10 among bowlers with an official combined rating of 59.80, using reliable IPL evidence. The strongest weighted component is IPL wicket quality (+0.64 weighted z); the weakest is IPL run suppression pressure gradient (+0.07).
- **Formats:** The official score is the IPL rating of 59.80. T20I evidence is No observed records and is excluded because no player-format performance record in supplied analytical population. The excluded format is not assigned zero.
- **Pressure evidence:** IPL: high-pressure wicket residual +2.53/100 and run-suppression residual +8.11/100 versus context; ordinary residuals -0.74 and +3.70; continuous wicket/run-suppression gradients +2.86/+23.99.
- **Uncertainty:** Top-10 inclusion is 35.3% in the fixed-benchmark bootstrap and 35.9% in the nested bootstrap. The player remains top 10 in 6/13 deterministic scenarios. Leave-one-player-out benchmarking changes the rating by +0.004 and rank by -1; top-10 membership does not change. Classification: BOUNDARY_TOP10. Bootstrap inclusion measures ranking stability, not the probability of being objectively top 10.

## Leading challengers and provisional candidates

Reliable challengers have a primary reliable-format rank but remain outside the official top 10. A reliable-ranked player with a provisional additional format retains that primary rank, while the provisional format stays excluded. Provisional-only challengers have no primary rating and must not be compared as if they passed the eligibility rules. The complete appendix is exported separately; the tables below show the first five under the locked ordering.

### Batter: Reliable challengers

| player | candidate_type | rank | best_evidence_format | best_evidence_status | top10_frequency_fixed | top10_frequency_nested | scenario_top10_count | failed_reliable_gates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Naman Dhir | Reliable challenger | 11.0000 | IPL | Reliable | 0.2986 | 0.2900 | 5 | none |
| Rajat Patidar | Reliable challenger | 19.0000 | IPL | Reliable | 0.2642 | 0.2810 | 1 | none |
| Jitesh Sharma | Reliable challenger | 16.0000 | IPL | Reliable | 0.2738 | 0.2620 | 1 | none |
| Ryan Burl | Reliable challenger | 20.0000 | T20I | Reliable | 0.2216 | 0.2250 | 1 | none |
| David Miller | Reliable challenger | 12.0000 | IPL | Reliable | 0.2134 | 0.2040 | 7 | none |

### Batter: Reliable-ranked with provisional additional formats

| player | candidate_type | rank | best_evidence_format | best_evidence_status | top10_frequency_fixed | top10_frequency_nested | scenario_top10_count | failed_reliable_gates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Marcus Stoinis | Reliable-ranked with provisional additional format | 17.0000 | T20I | Provisional | 0.1856 | 0.1840 | 0 | high_records 70 < 80 |
| Dinesh Karthik | Reliable-ranked with provisional additional format | 35.0000 | T20I | Provisional | 0.1376 | 0.1200 | 0 | high_records 59 < 80; ordinary_records 120 < 160 |
| Glenn Maxwell | Reliable-ranked with provisional additional format | 55.0000 | T20I | Provisional | 0.0638 | 0.0600 | 0 | high_records 65 < 80 |
| Tristan Stubbs | Reliable-ranked with provisional additional format | 43.0000 | T20I | Provisional | 0.0412 | 0.0450 | 0 | high_records 72 < 80 |
| Nitish Reddy | Reliable-ranked with provisional additional format | 42.0000 | T20I | Provisional | 0.0426 | 0.0450 | 0 | high_records 42 < 80; ordinary_records 88 < 160 |

### Batter: Provisional-only challengers

| player | candidate_type | rank | best_evidence_format | best_evidence_status | top10_frequency_fixed | top10_frequency_nested | scenario_top10_count | failed_reliable_gates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Reeza Hendricks | Provisional-only challenger | — | T20I | Provisional | 0.1828 | 0.1670 | 1 | high_records 63 < 80 |
| Vijay Shankar | Provisional-only challenger | — | IPL | Provisional | 0.1456 | 0.1470 | 0 | high_records 73 < 80 |
| Angkrish Raghuvanshi | Provisional-only challenger | — | IPL | Provisional | 0.1262 | 0.1230 | 0 | high_records 75 < 80 |
| Harry Brook | Provisional-only challenger | — | T20I | Provisional | 0.0964 | 0.0880 | 0 | high_records 59 < 80 |
| Donovan Ferreira | Provisional-only challenger | — | IPL | Provisional | 0.0644 | 0.0700 | 0 | ordinary_records 111 < 160 |

### Bowler: Reliable challengers

| player | candidate_type | rank | best_evidence_format | best_evidence_status | top10_frequency_fixed | top10_frequency_nested | scenario_top10_count | failed_reliable_gates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Yuzvendra Chahal | Reliable challenger | 11.0000 | IPL | Reliable | 0.3042 | 0.2930 | 7 | none |
| Jason Holder | Reliable challenger | 12.0000 | IPL | Reliable | 0.2590 | 0.2820 | 3 | none |
| Tim Southee | Reliable challenger | 13.0000 | T20I | Reliable | 0.2506 | 0.2570 | 3 | none |
| Jasprit Bumrah | Reliable challenger | 14.0000 | T20I | Reliable | 0.2376 | 0.2360 | 5 | none |
| Jacob Duffy | Reliable challenger | 17.0000 | T20I | Reliable | 0.2332 | 0.2340 | 1 | none |

### Bowler: Reliable-ranked with provisional additional formats

| player | candidate_type | rank | best_evidence_format | best_evidence_status | top10_frequency_fixed | top10_frequency_nested | scenario_top10_count | failed_reliable_gates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Lungi Ngidi | Reliable-ranked with provisional additional format | 21.0000 | IPL | Provisional | 0.1634 | 0.1720 | 0 | high_records 62 < 100; high_clean_records 60 < 80 |
| Harshit Rana | Reliable-ranked with provisional additional format | 29.0000 | T20I | Provisional | 0.1054 | 0.1020 | 0 | high_records 68 < 100; ordinary_records 193 < 200; high_clean_records 62 < 80 |
| Noor Ahmad | Reliable-ranked with provisional additional format | 59.0000 | T20I | Provisional | 0.0790 | 0.0910 | 0 | high_records 94 < 100 |
| Dushmantha Chameera | Reliable-ranked with provisional additional format | 34.0000 | IPL | Provisional | 0.0756 | 0.0820 | 0 | high_records 82 < 100; high_clean_records 75 < 80 |
| Marcus Stoinis | Reliable-ranked with provisional additional format | 35.0000 | IPL | Provisional | 0.0524 | 0.0530 | 0 | high_records 52 < 100; high_clean_records 50 < 80 |

### Bowler: Provisional-only challengers

| player | candidate_type | rank | best_evidence_format | best_evidence_status | top10_frequency_fixed | top10_frequency_nested | scenario_top10_count | failed_reliable_gates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Jamie Overton | Provisional-only challenger | — | T20I | Provisional | 0.1084 | 0.1070 | 1 | ordinary_records 156 < 200; ordinary_clean_records 146 < 160 |
| Matthew Humphreys | Provisional-only challenger | — | T20I | Provisional | 0.0840 | 0.0750 | 0 | high_records 69 < 100; high_clean_records 65 < 80 |
| Umran Malik | Provisional-only challenger | — | IPL | Provisional | 0.0694 | 0.0650 | 0 | high_records 80 < 100; high_clean_records 76 < 80 |
| Salman Mirza | Provisional-only challenger | — | T20I | Provisional | 0.0648 | 0.0630 | 0 | high_records 92 < 100 |
| Anshul Kamboj | Provisional-only challenger | — | IPL | Provisional | 0.0636 | 0.0620 | 0 | high_records 78 < 100; high_clean_records 69 < 80 |

## Limitations

- Structural pressure does not include target, required run rate, score parity, win probability or exact legal balls remaining.
- Low and Medium pressure are combined as Ordinary for the evidence tables; scoring still uses the continuous pressure percentile and contextual benchmarks.
- A delivery outcome does not create its pressure label. Runs, dots, wickets and survival are evaluated only after the pre-delivery state is fixed.
- Single-format ratings can rank highly, but the missing or unreliable format provides no balancing evidence.
- Bootstrap frequencies quantify sensitivity to match resampling and eligibility changes; they are not objective selection probabilities.
- The 75% core threshold identifies no official player as core, so all final explanations must retain the boundary qualification.

## Validation and Phase 7 handoff

All 20 Phase 6 validation gates passed. Phase 7 should preserve the official rank order, exact format-status explanations, boundary classifications and uncertainty language across the final submission and presentation.
