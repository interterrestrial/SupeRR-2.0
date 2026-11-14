# Phase 3 — Structural Pressure Modelling Report

## Decision

The earlier score/target/required-rate Phase 3 is **superseded**. Phase 2 showed
that the supplied fields do not support reliable reconstruction of innings
scores, targets, legal-ball progression, or balls remaining. This corrected
model therefore measures **structural pressure**, using only verified
pre-delivery state variables.

It must not be interpreted as win probability, required-rate pressure, or a
complete scoreboard-pressure model.

## Analytical population

- Phase 2 source: **192,235** regulation delivery records across
  **813** eligible matches.
- Primary Phase 3 population: **188,330** records across
  **789** whole unrevised matches.
- Excluded: **24** revised/shortened-schedule matches and
  **3,905** records.
- Super Overs were already excluded by Phase 2.
- The 257 unresolved legal-ball evidence records remain usable because this
  model never converts delivery records into inferred legal balls.

## Locked state definition

For every record, pressure is known before the current delivery outcome:

1. **Wicket strain** — wickets already lost compared with a leave-one-match-out
   expectation for the same format, innings, and source over. Only positive
   z-scores contribute; they are capped at 3 SD and divided by 3.
2. **Recent wicket shock** — wickets in the prior 12 delivery records, divided
   by 3 and capped at 1. These are delivery records, not assumed legal balls.
3. **Stage urgency** — `(source over - 1) / 19`, using the supplied over
   annotation from 1 to 20.

The primary continuous index is the equal-weight mean of these three bounded
components. Equal weights are the neutral pre-ranking choice; weight and recent
window alternatives are reported below. No current-delivery run, wicket,
dismissal, or extra enters the current record's pressure state.

## Benchmark hierarchy and provenance

The first choice is format × innings × source over, excluding the entire
current match. A benchmark is accepted only with at least
**100** out-of-match records and positive variance. The
predeclared fallbacks are format × innings × stage, then format × innings.

On this dataset, all **30,290** match-state benchmarks use the
exact source-over level. Support ranges from
**1,092** to
**2,724** records; no fallback is
required.

## Descriptive bands

Low, Medium, and High bands are assigned within format and innings from the
continuous-index percentile: Low ≤ 40%, Medium ≤ 80%, High > 80%. These bands
aid interpretation; the continuous index remains the modelling variable.

| format_group | innings | structural_pressure_category | records | share |
| --- | --- | --- | --- | --- |
| IPL | 1 | High | 9015 | 0.2020 |
| IPL | 1 | Low | 17766 | 0.3982 |
| IPL | 1 | Medium | 17839 | 0.3998 |
| IPL | 2 | High | 8320 | 0.2000 |
| IPL | 2 | Low | 16631 | 0.3999 |
| IPL | 2 | Medium | 16641 | 0.4001 |
| T20I | 1 | High | 10686 | 0.1995 |
| T20I | 1 | Low | 21486 | 0.4012 |
| T20I | 1 | Medium | 21386 | 0.3993 |
| T20I | 2 | High | 9578 | 0.1972 |
| T20I | 2 | Low | 19363 | 0.3987 |
| T20I | 2 | Medium | 19619 | 0.4040 |

## Robustness

All window and weight variants retain a Spearman rank correlation above 0.95
with the primary continuous index. High-band overlap is lower for the shortest
recent window because observations near the 80th-percentile boundary can cross
the descriptive cut. This is a boundary-classification limitation, not a
failure of the continuous measure.

| variant | spearman_vs_primary | category_agreement_vs_primary | high_category_jaccard_vs_primary |
| --- | --- | --- | --- |
| primary_equal_w12 | 1.0000 | 1.0000 | 1.0000 |
| equal_w6 | 0.9527 | 0.8319 | 0.6403 |
| equal_w18 | 0.9629 | 0.8528 | 0.6677 |
| wicket_heavy_w12 | 0.9798 | 0.8922 | 0.7092 |
| shock_heavy_w12 | 0.9749 | 0.8947 | 0.8964 |
| stage_heavy_w12 | 0.9571 | 0.8314 | 0.6883 |

## Validation gates

| check_name | status | observed | acceptance_rule |
| --- | --- | --- | --- |
| source_key_unique | PASS | 0 | 0 duplicate match/innings/record keys |
| primary_population_partition | PASS | 188330 | retained rows + excluded rows = source rows |
| revised_matches_fully_excluded | PASS | 0 | 0 retained rows with revision metadata |
| source_over_in_t20_range | PASS | 1..20 | all source over values in 1..20 |
| only_supported_formats | PASS | IPL, T20I | exactly IPL and T20I |
| pre_delivery_wickets_excludes_current_record | PASS | 0 | 0 mismatches against prior-only cumulative wickets |
| innings_open_with_zero_prior_wickets | PASS | 0 | 0 innings opening with a prior wicket |
| innings_open_with_zero_recent_wickets | PASS | 0 | 0 innings opening with a recent prior wicket |
| benchmark_complete | PASS | 0 | 0 unbenchmarked records |
| benchmark_support_adequate | PASS | 1092 | minimum support >= 100 |
| benchmark_variation_positive | PASS | 0.2636 | all selected benchmark SD values > 0 |
| pressure_index_complete | PASS | 0 | 0 missing primary pressure values |
| pressure_index_bounded | PASS | 0.000000..0.935625 | all primary pressure values in [0, 1] |
| pressure_category_complete | PASS | High, Low, Medium | only Low, Medium, High |
| sensitivity_rank_stability | PASS | 0.9527 | minimum non-primary Spearman correlation >= 0.90 |

## Limitations and downstream rules

- This model captures innings-stage urgency and wicket-related disruption. It
  cannot identify a steep chase rate, a small target, score parity, or a close
  finish.
- Benchmarks are delivery-record-weighted. An over with additional recorded
  deliveries contributes additional observations because Phase 2 cannot
  establish a definitive legal-ball sequence.
- Revised/shortened matches are excluded from primary Phase 3 and must not be
  silently reintroduced in Phase 4.
- Pressure is identical for batter and bowler on a given pre-delivery record;
  role-specific value must be measured from later outcome metrics, not by
  changing the state label.
- Phase 4 may join outcomes to these labels, but must retain the pre-delivery
  construction and must separately feasibility-audit any run/extras metric.
- Category counts are calibrated by design and are not evidence of validity.
  Validation rests on leakage checks, benchmark independence/support, bounded
  construction, and robustness.

## Deliverables

The authoritative artifacts are in `phase3_outputs/`. The former root-level
`deliveries_pressure_labelled.csv`, `par_score_benchmarks.csv`,
`chase_rate_benchmarks.csv`, and `first_innings_totals.csv` belong to the
superseded implementation and must not be used downstream.
