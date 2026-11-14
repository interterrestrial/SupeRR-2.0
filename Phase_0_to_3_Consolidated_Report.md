# SupeRR Selector Season 2 — Consolidated Report (Phases 0–3)

## Data audit, reconstruction, and corrected structural-pressure model

**Competition:** Rajasthan Royals — SupeRR Selector Season 2

**Dataset coverage:** Historical IPL and Men's T20I, 2022–2026

**Scope:** Phase 0 design, Phase 1 audit, Phase 2 reconstruction, and corrected Phase 3 modelling

**Authoritative Phase 3 output:** `phase3_outputs/phase3_structural_pressure_labelled.csv`

**Status:** Corrected Phase 3 implemented and validated

---

## 1. Executive decision

The previously consolidated score/target/required-rate Phase 3 is rejected and
superseded. It assumed that every innings had 120 legal balls, reconstructed
team totals from unresolved run/extras semantics, and used those reconstructions
to create par-score and chase-rate pressure. Those assumptions conflict with
the Phase 2 evidence and are not defensible.

The corrected Phase 3 measures **structural pressure** only. It uses:

1. the supplied source over annotation;
2. wickets already lost before the current delivery record;
3. wickets in prior delivery records; and
4. leave-one-match-out expectations separated by IPL/T20I and innings.

It does not use reconstructed scores, targets, required rates, inferred legal
balls, balls remaining, or the outcome of the current delivery.

The former root-level files `deliveries_pressure_labelled.csv`,
`par_score_benchmarks.csv`, `chase_rate_benchmarks.csv`, and
`first_innings_totals.csv` are retained only as superseded artifacts and must
not be used in Phase 4.

---

## 2. Phase 0 — Scope and methodology governance

Phase 0 established principles that remain binding:

- Pressure must be a pre-delivery property.
- IPL and T20I must retain separate baselines.
- Batter and bowler on the same delivery must share the same pressure state.
- Unsupported fields must not be imputed as cricket facts.
- Eligibility, reliability, and robustness must be assessed before rankings are
  accepted.

The original score/chase implementation proposed in Phase 0 became infeasible
after Phase 2 established that exact legal-ball and team-score reconstruction
was unsupported. Corrected Phase 3 is therefore a documented methodological
amendment: it narrows the construct to structural pressure instead of claiming
complete scoreboard pressure.

---

## 3. Phase 1 — Data understanding and audit

### 3.1 Source inventory

| Dataset | Rows | Columns | Primary role |
|---|---:|---:|---|
| `ball_by_ball.csv` | 200,999 | 33 | Delivery records |
| `playing_eleven.csv` | 28,381 | 9 | Squad/XI registrations |
| `matches.csv` | 883 | 22 | Match metadata and results |
| `competition_team_player_mapping.csv` | 6,413 | 6 | Player registrations |
| `teams.csv` | 353 | 3 | Competition-team identities |
| `competitions.csv` | 141 | 4 | Competition registry |
| **Total** | **237,170** | — | Six supplied CSVs |

### 3.2 Approved population

- Approved target population: 853 matches after competition-scope filtering.
- Eligible completed population: 813 matches.
- Eligible formats: 362 IPL matches and 451 T20I matches.
- Identity key: `player_id`; names are descriptive and are not unique keys.
- Developmental competitions and incomplete/no-result contests are excluded
  according to the Phase 1 rules.

Detailed identity, match-population, schema, missing-value, and exception
findings remain in `Phase 1 Report.md`.

---

## 4. Phase 2 — Validated analytical master

The authoritative Phase 2 input is
`phase2_outputs/phase2_integrated_cleaned_deliveries.csv`.

| Measure | Validated value |
|---|---:|
| Regulation delivery records | 192,235 |
| Eligible matches | 813 |
| Regulation innings | 1,626 |
| Columns | 61 |
| Duplicate delivery keys | 0 |
| Super Over records kept separately | 26 |

### 4.1 Legal-ball evidence boundary

| Evidence treatment | Records |
|---|---:|
| Recorded non-legal evidence: wide/overstep | 7,976 |
| No recorded wide or overstep | 184,002 |
| Unresolved: `other`/penalty | 257 |
| **Total** | **192,235** |

These are evidence classifications, not a definitive legal-ball reconstruction.
There are also 147 extended overs without a recorded wide or overstep. Phase 2
therefore does not infer exact legal balls or balls remaining.

### 4.2 Runs and extras boundary

`extras1_runs` is a source category code, while the full semantics of
`extras_2_runs` remain unresolved. Phase 2 preserves these fields and records
the limitation; it does not claim a fully reconstructed team-score progression.

### 4.3 Dismissal and sequence integrity

- All 10,392 wicket records have a dismissal type.
- Original and normalized dismissal labels are retained.
- The one missing dismissed-player identity and other exceptions are not
  silently imputed.
- `innings_ball_num` and `over_ball_num` were validated as record sequences,
  not converted into an unsupported legal-ball counter.

The complete evidence and exception treatment remains in `Phase 2 report.md`.

---

## 5. Phase 3 — Corrected structural-pressure model

### 5.1 Primary population

Any match with populated `first_inn_revised_overs`,
`second_inn_revised_overs`, or `revised_target` is excluded as a whole match
from the primary Phase 3 population. This prevents a shortened/revised schedule
from being represented on the standard 1–20-over urgency scale.

| Population | Matches | Delivery records |
|---|---:|---:|
| Phase 2 regulation master | 813 | 192,235 |
| Revised/shortened matches excluded | 24 | 3,905 |
| **Corrected Phase 3 primary population** | **789** | **188,330** |

The 257 unresolved legal-ball evidence records do not need to be removed,
because Phase 3 never infers legal balls from delivery records.

### 5.2 Pre-delivery state

For record \(i\), the current record is excluded from every outcome-based state:

\[
W_i = \sum_{j < i} I(\text{wicket}_j)
\]

The recent-wicket state is the number of wickets in the prior 12 delivery
records, not 12 assumed legal balls. Windows of 6 and 18 records are tested as
sensitivity alternatives.

The source over creates three descriptive stages:

- Powerplay: overs 1–6
- Middle: overs 7–15
- Death: overs 16–20

### 5.3 Leave-one-match-out wicket benchmark

Expected wickets already lost are calculated for the same:

- format group: IPL or T20I;
- innings: first or second; and
- source over: 1–20.

The entire current match is removed before calculating the benchmark mean and
sample standard deviation. A benchmark requires at least 100 out-of-match
records and positive variance. Predeclared fallbacks are format × innings ×
stage, then format × innings.

All 30,290 match-state benchmarks use the exact source-over level; no fallback
was required. Effective support ranges from 1,092 to 2,724 records.

The benchmark is delivery-record-weighted, consistent with applying one label
per delivery record. An over containing additional recorded deliveries
therefore contributes additional observations; exact legal-ball reweighting is
not attempted because Phase 2 does not support it.

### 5.4 Bounded components and continuous index

**Wicket strain**

\[
z_i = \frac{W_i - E(W \mid \text{format, innings, over, other matches})}
{SD(W \mid \text{format, innings, over, other matches})}
\]

\[
C_{wicket,i} = \frac{\min(3,\max(0,z_i))}{3}
\]

**Recent wicket shock**

\[
C_{shock,i} = \min\left(1,\frac{\text{wickets in prior 12 records}}{3}\right)
\]

**Stage urgency**

\[
C_{stage,i} = \frac{\text{source over}_i - 1}{19}
\]

**Primary structural-pressure index**

\[
P_i = \frac{C_{wicket,i}+C_{shock,i}+C_{stage,i}}{3}
\]

Equal weights are the neutral choice locked before player ranking. Alternative
component weights are part of the robustness output rather than selected after
seeing future player ranks.

### 5.5 Descriptive categories

Within each format × innings stratum, the continuous index is converted to a
percentile using average ranks:

- Low: percentile ≤ 40%
- Medium: 40% < percentile ≤ 80%
- High: percentile > 80%

The continuous index is primary. Category shares are calibrated by design and
must not be presented as independent validation evidence.

---

## 6. Validation and robustness

All 15 pipeline gates passed, including:

- unique source keys and exact source/exclusion partition;
- complete exclusion of revised-schedule matches;
- prior-only wicket state and zero prior wickets at every innings opening;
- complete benchmarks with minimum support 1,092 and positive variance;
- complete index bounded from 0.000000 to 0.935625; and
- minimum sensitivity Spearman correlation of 0.9527.

An independent validator then reread the persisted CSV files and passed 13
additional checks. It recomputed the prior-wicket sequence, prior-12-record
window, primary formula, all exact leave-one-match-out benchmark means and
standard deviations, and every manifest SHA-256 hash.

| Variant | Spearman vs primary | Category agreement | High-band Jaccard |
|---|---:|---:|---:|
| Prior 6 records, equal weights | 0.9527 | 0.8319 | 0.6403 |
| Prior 18 records, equal weights | 0.9629 | 0.8528 | 0.6677 |
| Wicket-heavy weights | 0.9798 | 0.8922 | 0.7092 |
| Shock-heavy weights | 0.9749 | 0.8947 | 0.8964 |
| Stage-heavy weights | 0.9571 | 0.8314 | 0.6883 |

The lower overlap for some High bands reflects observations crossing the
80th-percentile descriptive boundary; continuous ranks remain strongly stable.

---

## 7. Authoritative Phase 3 deliverables

| Artifact | Records | Purpose |
|---|---:|---|
| `phase3_structural_pressure_labelled.csv` | 188,330 | Phase 2 master plus corrected pressure state |
| `phase3_wicket_benchmarks_lomo.csv` | 30,290 | Match-specific benchmark provenance |
| `phase3_sensitivity_summary.csv` | 6 | Window/weight robustness |
| `phase3_component_correlations.csv` | 3 | Component redundancy audit |
| `phase3_excluded_revised_matches.csv` | 24 | Whole-match exclusion register |
| `phase3_validation_gates.csv` | 15 | Machine-readable acceptance gates |
| `phase3_model_specification.csv` | 14 | Locked definitions and prohibited inputs |
| `phase3_output_manifest.csv` | 7 | Dimensions, sizes, versions, and hashes |

Executable artifacts:

- `Phase_3_Structural_Pressure_Modelling.ipynb` — authoritative standalone Phase 3 notebook.
- `phase3_structural_pressure.py` — reusable implementation used by the notebook.
- `validate_phase3_outputs.py` — independent persisted-output validator.
- `SupeRR_Phases_1_to_3_Consolidated.ipynb` — consolidated handoff that reads the Phase 2 master and calls the same corrected implementation.

---

## 8. Boundary and Phase 4 handoff

Corrected Phase 3 is complete for the structural-pressure construct. It does
not claim to measure required-rate, target, score-par, or close-finish pressure.

Phase 4 must:

1. use `phase3_outputs/phase3_structural_pressure_labelled.csv` only;
2. keep the same pressure value for batter and bowler on a delivery;
3. keep revised/shortened matches outside the primary analysis;
4. use the continuous index for primary estimation and categories for
   explanation/slicing;
5. feasibility-audit run/extras-dependent outcome metrics separately; and
6. carry window/weight and category-boundary uncertainty into Phase 5.

No player score, eligibility threshold, or player ranking is produced in Phase
3.
