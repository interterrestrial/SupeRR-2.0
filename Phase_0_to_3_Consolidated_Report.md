# SupeRR Selector Season 2 — Consolidated Report (Phases 0–3)
## Data Audit, Reconstruction & Pre-Delivery Pressure Modelling

**Competition:** Rajasthan Royals — SupeRR Selector Season 2  
**Dataset Coverage:** Historical IPL and Men's T20I (2022–2026)  
**Scope:** Phase 0 (Design), Phase 1 (Audit), Phase 2 (Reconstruction), and Phase 3 (Pressure Modelling)  
**Deliverables Produced:** Validated Master Delivery Dataset (`deliveries_pressure_labelled.csv`) and Benchmark Tables  
**Status:** Phases 0–3 Complete & Verified  

---

## 1. Executive Summary & Scope

The Rajasthan Royals SupeRR Selector Season 2 challenge requires identifying the players who perform most reliably under pressure in T20 cricket. Traditional cricket metrics (raw aggregate runs, overall strike rates, and raw bowling economy rates) fail to distinguish between low-leverage "stat-padding" and elite execution in critical moments.

Phases 0 through 3 establish the methodological foundation, data integrity, and mathematical modeling of match pressure:

1. **Phase 0 (Scope & Methodology Design):** Closed. Established the core principles: pressure is strictly a pre-delivery property; IPL and T20I must be evaluated with format-specific baselines; innings 1 pressure is governed by par score deviation and wicket depletion, while innings 2 pressure is governed by relative chase demand strain.
2. **Phase 1 (Data Understanding & Audit):** Audited six supplied CSV datasets (236,970 total records). Established `player_id` as the unique identity key, identified squad/impact-player redundancies in `playing_eleven.csv`, and approved the primary match population of **813 completed matches** (362 IPL, 451 T20I).
3. **Phase 2 (Data Cleaning & Cricket State Reconstruction):** Reconciled 192,235 regulation deliveries, classified legal balls (`is_legal_ball`), resolved runs and bowler attribution, and reconstructed cumulative innings progression strictly prior to delivery outcome.
4. **Phase 3 (Pressure Modelling & Benchmark Construction):** Constructed 320 first-innings par score benchmark states and 327 second-innings chase scoring rate benchmark states with adaptive stage fallback. Formulated a continuous `pressure_index` $\in [0, 1]$, classifying 32,527 deliveries (16.92%) into **High Pressure**.

---

## 2. Phase 1 — Data Understanding & Audit

### 2.1 Dataset Inventory
The six source CSV files provided in the data pack were ingested and audited:

| Dataset | Rows | Columns | Description | Key Audit Findings |
|---|---:|---:|---|---|
| `ball_by_ball.csv` | 200,999 | 33 | Delivery-level records | Zero duplicate rows. Covers 867 of the 883 matches. Contains 38 Super Over deliveries across 6 matches. |
| `matches.csv` | 883 | 22 | Match metadata & results | 16 abandoned matches have zero delivery records. 22 matches contain official DLS `revised_target` values. |
| `competitions.csv` | 141 | 4 | Competition registry | Spans IPL (2022–2026: 5 seasons) and 134 bilateral/ICC T20I series, plus 2 developmental tournaments. |
| `playing_eleven.csv` | 28,381 | 9 | Squad & XI registrations | Not a clean 11-player roster; contains non-playing squad reserves (8,667 rows with missing batting order) and paired impact-player flags. |
| `teams.csv` | 353 | 3 | Team identity per comp | Composite key `(comp_id, team_id)` reconciles 100% with match home/away team identifiers. |
| `competition_team_player_mapping.csv` | 6,413 | 6 | Player registration mapping | Reconciles 100% of delivery-role appearances (striker, non-striker, bowler, dismissed player). |

### 2.2 Player Identity Disambiguation & Dropping of Inactive/Phantom IDs
Across all source files, 1,217 unique player IDs and 1,210 unique names were observed. Exactly **seven names** were associated with two distinct `player_id`s in the raw tables. A complete forensic audit resolves these cases cleanly:

#### Category A: Inactive / "Phantom" IDs Dropped (Zero Deliveries in Eligible Matches)
Several secondary IDs only existed as unplayed squad roster rows in `competition_team_player_mapping.csv` or in excluded developmental competitions (`comp_id 2670`). Because our analytical dataset is constructed strictly from actual deliveries in eligible completed matches, **these phantom IDs have 0 deliveries and are completely dropped from the delivery pipeline**:
- **Mohammad Ali (`player_id 3083`):** 0 deliveries bowled or faced across all matches. Dropped.
- **Bashir Ahmad (`player_id 39479`):** 0 deliveries bowled or faced across all matches. Dropped.
- **Rashid Khan (`player_id 20172`):** Unplayed Nepal squad registration for the UAE vs Nepal 2026 series (0 deliveries). Dropped.
- **Muhammad Farooq (`player_id 28978`):** Unplayed squad row in comp 2670 (0 deliveries). Dropped.
- **Basil Hameed (`player_id 39444`):** An artificial duplicate created in comp 2670 (Emerging Teams Asia Cup). Because comp 2670 is excluded from the eligible population, ID 39444 has **0 deliveries** in the eligible dataset. Dropped.

#### Category B: Active IDs with Negligible High-Pressure Significance
Even when examining the active IDs for the above players, their high-pressure sample sizes are statistically negligible:
- **Mohammad Ali (`player_id 20229`):** Played 3 matches for Pakistan; faced only 1 ball under high pressure (0 balls bowled under high pressure).
- **Bashir Ahmad (`player_id 29833`):** Played 1 match for Afghanistan; faced only 6 balls under high pressure (0 balls bowled under high pressure).
Both players fall far below any meaningful eligibility threshold ($\ge 50$ or $60$ pressure balls) and have zero impact on pressure rankings.

#### Category C: True Cross-National Namesakes (Different Players, Different Countries)
Only two same-name pairs exhibit active, meaningful delivery volume in eligible cricket. They represent entirely different human beings playing for different national teams and must **NEVER** be merged:
1. **Abdul Samad:**
   - `player_id 7446`: **India** (Sunrisers Hyderabad / Lucknow Super Giants, IPL). Middle-order batter from Jammu & Kashmir (441 balls faced in eligible IPL matches).
   - `player_id 6922`: **Pakistan** (Pakistan national team & Pakistan A). Middle-order batter (70 balls faced in eligible T20I matches).
   - *Treatment:* Maintained as distinct entities via `player_id`. Indian Abdul Samad's IPL metrics are never blended with Pakistani Abdul Samad's T20I metrics.
2. **Haider Ali:**
   - `player_id 7338`: **Pakistan** (Pakistan national team). Top-order batter (75 balls faced in eligible T20I matches).
   - `player_id 28756`: **United Arab Emirates** (UAE national team). Left-arm spinner / all-rounder (41 balls faced, 273 balls bowled in eligible T20I matches).
   - *Treatment:* Maintained as distinct entities via `player_id`.

**Governance Rule:** `player_id` is the sole immutable primary key. Unplayed phantom IDs are eliminated automatically, while legitimate international namesakes remain cleanly segregated.

### 2.3 Match Population & Exclusion Audit
The 883 matches in `matches.csv` were audited against competition boundaries and completion criteria:

| Category | Match Count | Analytical Treatment |
|---|---:|---|
| **Total Matches in Dataset** | **883** | Full source inventory |
| *Match Abandoned (No deliveries bowled)* | 16 | Excluded (no competitive play) |
| *Match Abandoned (Partial first innings)* | 3 | Excluded (no result achievable) |
| *No Result (Completed 1st innings, rain before 2nd)* | 19 | Excluded (incomplete contest) |
| *No Result (Interrupted in 2nd innings without DLS result)* | 2 | Excluded (incomplete contest) |
| *Developmental T20 Competitions (Emerging Teams / Rising Stars)* | 30 | Excluded (developmental A-teams; outside elite IPL/T20I scope) |
| **Approved Eligible Match Population** | **813** | **Retained as Primary Analysis Population** |
| — *IPL Completed Matches* | *362* | 74 (2022), 73 (2023), 71 (2024), 71 (2025), 73 (2026) |
| — *T20I Completed Matches* | *451* | 134 international competitions spanning 2022 to 2026 |

---

## 3. Phase 2 — Data Cleaning & Cricket State Reconstruction

### 3.1 Delivery Population & Super Over Separation
- Regulation innings 1 and 2 contribute exactly **192,235 deliveries** across the 813 eligible matches.
- Super Overs (innings 3 & 4: 38 deliveries across 6 matches) were isolated to preserve regulation over progression and benchmark comparability.

### 3.2 Legal-Ball Evidence Classification
The `over_ball_num` field represents delivery sequence, not legal balls. Legal balls must be derived from extras evidence:
- **Explicit Non-Legal Deliveries (7,976 balls):** Wides (7,419) and No-balls / Oversteps (557). These incur penalty runs and do not increment the legal ball counter.
- **Explicit Legal Deliveries (184,002 balls):** Normal balls without extras (180,862), Legbyes (2,635), and Byes (505).
- **Unresolved Edge Cases (257 balls):** 256 `other` and 1 `Penalty` records. In accordance with Phase 2 principles, these are treated conservatively as legal balls with original runs preserved.

### 3.3 Runs Attribution Framework
Three independent run quantities are reconstructed for every delivery:
1. `runs`: Batter runs scored off the bat. Credited to the batter for strike rate and boundary calculations.
2. `total_delivery_runs`: Team score contribution. Batter runs + 1 penalty run for wide/no-ball/bye/legbye.
3. `bowler_runs_conceded`: Runs charged to the bowler for economy calculations. Batter runs + wide/no-ball penalties. Byes and legbyes (fielding extras) are strictly excluded from the bowler's debit.
4. `is_dot_ball`: Defined as `runs == 0` on a legal delivery without wide/no-ball extras.

### 3.4 Dismissal Classification & Attribution
- All 10,392 dismissals in the eligible population have recorded dismissal types.
- Spelling variants (`Obstracting the field` vs `Obstructing the field`) were normalized.
- **Batter Attribution:** A batter dismissal is recorded only when `is_wicket == True` and `dismissed_player_id == striker_id`. Non-striker run outs are excluded from the striker's dismissal count.
- **Bowler Attribution:** Bowler wickets are strictly filtered to bowler-credited dismissals: `['Caught', 'Bowled', 'LBW', 'Stump', 'Hit Wicket']` (9,817 wickets). Run outs, obstructing the field, and retired out are excluded.

### 3.5 Pre-Delivery State Reconstruction
Every delivery is mapped to its state immediately before the ball is bowled:
- `pre_delivery_score`: Cumulative runs scored in the innings prior to this delivery.
- `pre_delivery_wickets`: Wickets fallen in the innings prior to this delivery ($0 \le W \le 9$).
- `wickets_remaining`: $10 - \text{pre\_delivery\_wickets}$.
- `legal_ball_number`: Cumulative legal balls bowled in the innings prior to this delivery.
- `legal_balls_remaining`: $\max(0, 120 - \text{legal\_ball\_number})$.
- `over_number`: Over index ($1 \le \text{Over} \le 20$).
- `innings_stage`: **Powerplay** (Overs 1–6: 60,955 balls), **Middle** (Overs 7–15: 88,603 balls), **Death** (Overs 16–20: 42,677 balls).

---

## 4. Phase 3 — Pressure Modelling & Benchmark Construction

### 4.1 First-Innings Pressure: Par Score Strain
Because the first innings lacks a target score, pressure is evaluated against the historical expected scoring baseline:

$$\text{Par Score Benchmark} = \mu(\text{Score} \mid \text{Format}, \text{Over}, \text{Wickets Fallen})$$

1. **Wicket Depletion Component:**
   $$\text{Wicket Pressure} = \frac{\text{Pre-Delivery Wickets}}{9} \in [0, 1]$$
2. **Standardized Scoring Deviation Component:**
   $$\text{Score Deviation} = \frac{\text{Pre-Delivery Score} - \text{Par Score Mean}}{\sigma(\text{Par Score})}$$
   Negative deviation reflects scoring below historical expectations. Standardized deviation is clamped at $\pm 3\sigma$ and mapped to $[0, 1]$:
   $$\text{Par Pressure} = \frac{-\text{Score Deviation} + 3}{6}$$
3. **Innings Stage Component:**
   $$\text{Stage Pressure} = \frac{\text{Over Number} - 1}{19} \in [0, 1]$$

$$\text{Pressure}_{\text{Inn1}} = 0.35 \cdot \text{Wicket Pressure} + 0.40 \cdot \text{Par Pressure} + 0.25 \cdot \text{Stage Pressure}$$

### 4.2 Second-Innings Pressure: Relative Chase Demand
In the second innings, pressure is governed by the urgency of the chase:
1. **Target Score Construction:** First Innings Total + 1, with official DLS `revised_target` values integrated for all 22 rain-affected matches.
2. **Required Run Rate (RRR):**
   $$\text{RRR} = \frac{\text{Chase Target} - \text{Pre-Delivery Score}}{\text{Legal Balls Remaining} / 6}$$
   *(When legal balls remaining reach 0, RRR is capped at 36.0 for extreme last-ball pressure).*
3. **Expected Scoring Rate Benchmark:** Historical average runs per over for that format, over, and wicket state:
   $$\text{Expected Rate Benchmark} = 6 \cdot \mu(\text{Delivery Runs} \mid \text{Format}, \text{Over}, \text{Wickets Fallen})$$
4. **Relative Chase Demand Strain:**
   $$\Delta_{\text{Demand}} = \text{RRR} - \text{Expected Rate}$$
   Clamped between $-6.0$ and $+12.0$ runs per over and mapped to $[0, 1]$:
   $$\text{Chase Demand Pressure} = \frac{\Delta_{\text{Demand}} + 6}{18}$$

$$\text{Pressure}_{\text{Inn2}} = 0.30 \cdot \text{Wicket Pressure} + 0.45 \cdot \text{Chase Demand Pressure} + 0.25 \cdot \text{Stage Pressure}$$

### 4.3 Adaptive Benchmark Fallback Architecture
To prevent sample sparsity in extreme wicket states while prohibiting cross-format contamination:
- **Primary Stratum:** Exact match on `(Format, Over Number, Pre-Delivery Wickets)`.
  - First Innings: 320 exact benchmark states (median support: 219 deliveries).
  - Second Innings: 327 exact benchmark states (median support: 201 deliveries).
- **Secondary Fallback:** If an unobserved or sparse state occurs, fallback to the format stage average `(Format, Innings Stage)`. Cross-format pooling between IPL and T20I is strictly prohibited.

### 4.4 Pressure Classification & Distribution
The continuous `pressure_index` $\in [0, 1]$ is partitioned into three standardized operational categories:
- **High Pressure ($\ge 0.60$):** 32,527 deliveries (16.92%). True crisis and crunch situations (steep chases, late overs with multiple wickets down).
- **Medium Pressure ($0.35 - 0.60$):** 79,250 deliveries (41.23%). Competitive match progression, par chases, and middle-over rebuilding.
- **Low Pressure ($< 0.35$):** 80,458 deliveries (41.85%). Low-leverage situations (early powerplays with wickets intact, easy chases well ahead of rate).

#### Distribution by Match Context:
| Innings Stage | High Pressure Balls | Medium Pressure Balls | Low Pressure Balls | Total Deliveries | High Pressure % |
|---|---:|---:|---:|---:|---:|
| **Powerplay (Overs 1–6)** | 18 | 6,802 | 54,135 | 60,955 | **0.03%** |
| **Middle (Overs 7–15)** | 8,376 | 55,538 | 24,689 | 88,603 | **9.45%** |
| **Death (Overs 16–20)** | 24,133 | 16,910 | 1,634 | 42,677 | **56.55%** |

#### Distribution by Competition Format:
| Format | High Pressure Balls | Medium Pressure Balls | Low Pressure Balls | Total Deliveries | High Pressure % |
|---|---:|---:|---:|---:|---:|
| **IPL** | 13,690 | 36,645 | 36,882 | 87,217 | **15.70%** |
| **T20I** | 18,837 | 42,605 | 43,576 | 105,018 | **17.94%** |

---

## 5. Formal Validation & Acceptance Gates

All six formal Phase 3 validation gates passed successfully:
1. **Zero Null Pressure Values:** 0 null records across all 192,235 deliveries.
2. **Strict Bounded Range:** Minimum pressure index = `0.0000`, maximum = `1.0000`.
3. **Population Fidelity:** Exact reconciliation with Phase 1 approved population (813 matches, 192,235 regulation deliveries).
4. **Format Integrity:** 100% of observations belong to approved formats (IPL: 87,217 balls, T20I: 105,018 balls).
5. **Crunch Leverage Authenticity:** High Pressure constitutes 16.92% of the dataset, with 74.2% of High Pressure deliveries occurring in death overs.
6. **Death Over Stress Test:** Deliveries in overs 16–20 with $\ge 7$ wickets fallen exhibit an average pressure index of **0.812**, with **95.3% classified as High Pressure**.

---

## 6. Exported Phase 3 Deliverables

The consolidated pipeline exports the complete analytical package:

| File Name | Records | File Size | Description |
|---|---:|---:|---|
| `deliveries_pressure_labelled.csv` | 192,235 | 80.62 MB | Master delivery dataset with 60 columns including continuous pressure scores, category labels, pre-delivery scores, wickets, and benchmarks. |
| `eligible_matches.csv` | 813 | 0.15 MB | Metadata for the 813 eligible matches (comp_type, venue, toss, outcome, DLS revised targets). |
| `par_score_benchmarks.csv` | 320 | 0.01 MB | First-innings par score mean and standard deviation by `(comp_type, over_number, pre_delivery_wickets)`. |
| `chase_rate_benchmarks.csv` | 327 | 0.02 MB | Second-innings expected scoring rate benchmarks by `(comp_type, over_number, pre_delivery_wickets)`. |
| `first_innings_totals.csv` | 813 | 0.02 MB | First-innings team scores, wickets, legal balls, and chase targets per match. |

### Consolidated Notebook:
- `SupeRR_Phases_1_to_3_Consolidated.ipynb`: A clean 17-cell Jupyter notebook that runs from raw source files to final Phase 3 deliverables in under 10 seconds with zero errors.

---

## 7. Phase 3 Boundary & Handoff to Phase 4

As mandated by the project governance design, **Phase 3 is complete and formally closed**. 

- No player performance metrics, composite weights, eligibility thresholds, or player rankings have been computed.
- The master analytical dataset `deliveries_pressure_labelled.csv` provides the foundation for Phase 4 (Player Metrics & Scoring Methodology), where batting strike rate differentials, bowling economy differentials, balls per dismissal, and wicket-taking rates will be calculated across formats.

