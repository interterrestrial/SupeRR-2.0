# SupeRR Selector Season 2
## Phase 0 — Final Scope and Methodology Design Report

**Project:** SupeRR Selector Season 2  
**Phase:** 0 — Final Scope and Methodology Design  
**Status:** Completed and approved  
**Next phase:** Phase 1 — Data Understanding and Audit

---

## 1. Executive Summary

The objective of SupeRR Selector Season 2 is to identify the top 10 batters and top 10 bowlers based on their performance under pressure in T20 cricket.

The project will evaluate IPL and men's T20I performances from 2022 onward.

Phase 0 established the project's analytical scope, pressure definitions, performance dimensions, benchmarking principles, eligibility framework, scoring architecture, uncertainty treatment and ranking-validation approach.

The methodology is designed around five principles:

1. **Contextual fairness:** Evaluate players relative to comparable cricketing situations rather than relying on raw aggregate statistics.
2. **Format-specific evaluation:** Analyse IPL and T20I separately before combining normalized results.
3. **Statistical reliability:** Account for sample sizes, uncertainty, match-level variation and benchmark quality.
4. **Transparency:** Use predefined, explainable scoring weights rather than opaque or ranking-driven optimization.
5. **Reproducibility:** Establish explicit rules for data cleaning, pressure reconstruction, scoring and ranking validation.

The primary output will be one combined ranking of 10 batters and one combined ranking of 10 bowlers.

A separate recent-form analysis will complement the historical rankings.

## 2. Project Scope

### 2.1 Selection objectives

The project will produce:

- One ranked list of the top 10 batters.
- One ranked list of the top 10 bowlers.

These are combined rankings across IPL and men's T20I, not separate top-10 lists for each competition.

Players may qualify using IPL evidence, T20I evidence or both. There is no predetermined competition quota.

### 2.2 Historical coverage

- Starting period: 2022 onward.
- Competitions: IPL and men's T20I.
- Latest available season: Subject to verification during Phase 1.
- Historical ranking: All eligible evidence within the available period.

No automatic recency weighting will be applied to the historical ranking.

### 2.3 Recent-form analysis

A secondary analysis will evaluate the latest two available seasons.

It will:

- Be calculated separately from the historical ranking.
- Use independent recent-form eligibility and reliability classifications.
- Identify improving or declining performances.
- Account for incomplete latest-season coverage.
- Not alter the official historical top-10 rankings.

## 3. Pressure Definition

Pressure is defined as the difficulty of the team's match situation immediately before a delivery.

Pressure must be calculated using the state before the delivery outcome occurs. This prevents information from the delivery itself from influencing its pressure classification.

The same underlying match-state classification will apply to the batter and bowler. Their performance outcomes will be evaluated separately.

### 3.1 First-innings pressure

First innings do not have a target or required run rate. Therefore, pressure will be constructed using:

1. Scoring position relative to expected cumulative scoring.
2. Wickets remaining.
3. Balls remaining.

Expected final innings score will be used as a diagnostic and validation measure, not as an additional initial pressure component.

The scoring deviation will be represented using:

- Raw difference: Actual cumulative score minus expected cumulative score.
- Standardized difference: The difference divided by the historical standard deviation for comparable situations.

Negative standardized deviation indicates scoring below expectation; positive deviation indicates scoring above expectation.

The deviation will not be interpreted as a standalone pressure measure or as a normal-distribution probability.

Wickets remaining and balls remaining will initially remain separate indicators. No arbitrary combined resource index will be imposed.

### 3.2 Second-innings pressure

Second-innings pressure will consider required scoring demand relative to expected scoring capability.

The central measure is:

**Relative scoring demand = Required run rate − Expected scoring rate**

A positive difference indicates that the required rate exceeds expected scoring capability. A negative difference indicates a comparatively easier chase.

The expected scoring rate will use historical comparable chase situations.

Benchmark conditioning will consider:

- Competition.
- Innings stage.
- Wickets remaining.
- Remaining resources.

Required-rate conditioning and wickets-by-scoring-demand interactions will be introduced only if they demonstrate stable, incremental analytical value.

Both absolute and proportional balls remaining will be evaluated, with absolute remaining balls serving as the primary measure.

### 3.3 Innings stages

The initial standard T20 stage definitions are:

- Powerplay: Overs 1–6.
- Middle overs: Overs 7–15.
- Death overs: Overs 16–20.

These stages are contextual benchmark groupings, not automatic pressure multipliers.

For shortened innings, actual scheduled legal-ball allocation and applicable playing conditions will determine stage mapping. Proportional progression will support comparability but will not replace absolute scheduled length.

### 3.4 Pressure scale

The project will use a hybrid representation:

- Continuous pressure score for analysis.
- Low, medium and high categories for reporting.

The continuous score remains the primary analytical measure.

Pressure intensity will not be equated with the absolute value of scoring deviation. Scoring below expectation and scoring above expectation have different interpretations.

Category boundaries and indicator weights will require validation.

## 4. Benchmarking Methodology

IPL and T20I benchmarks will be constructed separately.

Cross-competition fallback is prohibited.

### 4.1 First-innings benchmarks

The preferred benchmark dimensions are:

- Competition.
- Innings stage.
- Wickets remaining.
- Scheduled innings length where relevant.

Expected cumulative scoring will be based on exact comparable states where sufficient evidence exists.

### 4.2 Second-innings benchmarks

Expected scoring-rate benchmarks will adapt to:

- Competition.
- Innings stage.
- Wickets remaining.
- Remaining resources.

Required-rate difficulty will initially be evaluated without conditioning the expected-rate benchmark on required rate itself. Additional conditioning requires evidence of improved out-of-sample performance and stability.

### 4.3 Adaptive fallback hierarchy

Where exact benchmark states are sparse:

1. Use exact comparable states where available.
2. Expand to nearby scheduled innings lengths while preserving important contextual dimensions.
3. Relax wicket-state matching through adjacent states.
4. Expand symmetrically where possible.
5. Use broader stage-based benchmarks only when defensible.
6. Mark the observation unavailable when no defensible benchmark exists.

Adjacent wicket states will be pooled using observation-weighted averages, not equal weighting.

If exact-state and pooled benchmarks materially disagree relative to uncertainty and practical significance, the observation will be marked unavailable.

Small exact-state samples may be retained as provisional rather than automatically discarded.

Benchmark provenance, sample size, scheduled-length range, progression range and wicket-state matching level must be recorded.

## 5. Player Performance Dimensions

### 5.1 Batting evaluation

Four dimensions were selected:

**1. Pressure-phase runs**

Measures the batter's scoring contribution during pressure situations.

**2. Context-adjusted strike rate**

Measures scoring efficiency relative to expected strike rate in comparable conditions.

**3. Survival**

Evaluates dismissal frequency and balls per dismissal.

Both statistics will be reported, but one will be designated primary and the other supporting to avoid double-counting the same underlying ability.

Dismissal attribution must distinguish batter-credited dismissals from dismissals not attributable to the batter.

**4. Consistency**

Match-to-match consistency will be treated as a reliability and stability dimension, not as an independent positive performance bonus.

### 5.2 Bowling evaluation

Four dimensions were selected:

**1. Wicket-taking contribution**

Includes bowler-credited wickets and wicket-taking rate.

Wicket-taking rate is the primary candidate measure, with total wickets providing supporting contribution context.

**2. Run prevention**

Economy and other run-prevention metrics will only be included when conceded runs can be reconstructed reliably.

**3. Dot-ball pressure**

Evaluates the bowler's ability to restrict scoring opportunities.

Dot-ball identification requires validated legal-ball and extras treatment.

**4. Consistency**

Match-to-match repeatability will be used as a reliability and stability measure, not as a positive performance bonus.

If economy and dot-ball metrics are redundant or unreliable, only defensible metrics will be retained.

## 6. Format Normalization and Combined Scoring

Raw IPL and T20I statistics will not be directly combined.

Each competition will be analysed separately, with performance metrics normalized against relevant format-specific benchmarks.

The approved starting combination is:

**When both formats have eligible evidence:**

Combined score = 0.5 × IPL normalized score + 0.5 × T20I normalized score.

**When only one format has eligible evidence:**

Use the qualifying competition's normalized score. Missing competition evidence will not be assigned zero.

There is no mandatory requirement for players to have evidence in both competitions.

Reliability will affect uncertainty reporting, eligibility and confidence in the ranking, not the primary format weights.

## 7. Metric Weights

The project will use predefined weights justified through cricketing rationale.

Separate weighting structures will be established for batting and bowling.

The following rules apply:

- Weights must be documented before examining player rankings.
- Correlated metrics must be checked for redundancy.
- Metrics that cannot be calculated reliably must be excluded or marked unavailable.
- Sensitivity analysis will evaluate alternative reasonable weights.
- Primary weights will not be changed simply to favour particular players.

Exact numerical weights remain deferred until metric feasibility and data-quality checks are completed.

## 8. Eligibility and Reliability

Numerical eligibility thresholds will be determined after the dataset audit.

They will be based on:

- Relevant pressure opportunities.
- Distinct matches.
- Distinct innings.
- Outcome completeness.
- Statistical stability.

Separate thresholds will be developed for:

- Batters and bowlers.
- IPL and T20I.

The eligibility framework will distinguish three categories:

**Reliable:** Sufficient evidence and acceptable statistical stability.

**Provisional:** Evidence is usable, but material uncertainty or benchmark limitations remain.

**Insufficient:** Evidence is inadequate for meaningful evaluation.

Reliable-only rankings will form the primary official ranking.

Provisional candidates will be shown separately in an appendix and will not be mixed into the official ranking.

Players with sufficient descriptive evidence but insufficient benchmark reliability may still be included in that appendix.

## 9. Statistical Uncertainty and Validation

### 9.1 Match-level bootstrap

Uncertainty will be estimated through match-level resampling rather than treating every delivery as independent.

IPL and T20I will be resampled separately, preserving the available format coverage.

When a player has evidence in only one competition, uncertainty estimation will use that competition only.

### 9.2 Combined-score uncertainty

The entire scoring formula will be recomputed in every bootstrap replicate.

The analysis will report:

- Combined score distributions.
- Rank distributions.
- Top-10 inclusion frequency.
- Top-10 set stability.

### 9.3 Benchmark uncertainty

Two approaches will be compared:

**Fixed benchmark bootstrap:** Resample player matches while holding benchmarks fixed.

**Nested benchmark bootstrap:** Resample both player and benchmark populations, recalculating benchmark means, standard deviations and resulting scores.

These will be reported separately.

### 9.4 Benchmark self-influence

The primary benchmark will include the evaluated player's own historical observations.

Leave-one-player-out benchmarking will be used as a sensitivity analysis.

Both benchmark-level and ranking-level effects will be examined, including changes in means, standard deviations, standardized deviations, combined scores and final ranks.

Self-influence will be reported using:

- Numerical magnitude.
- Paired bootstrap uncertainty.
- Directional bootstrap frequency.
- Practical impact on top-10 selection.

Materiality thresholds will be established before player-level ranking results are examined.

Self-influence will trigger reliability flags rather than automatically changing eligibility.

## 10. Final Ranking Rules

The official rankings will use the primary point-estimate scores.

- Reliability will not be added as a performance bonus.
- Bootstrap inclusion frequency will not replace the primary score ranking.
- Scores will be ranked before display rounding.
- Players near the tenth-place boundary will receive explicit uncertainty and sensitivity analysis.
- Alternative weights, thresholds and benchmark choices will be tested.
- Ties will use the relevant primary performance metric as the first tie-breaker, followed by eligible evidence volume.
- Remaining ties will be disclosed and resolved using a documented deterministic rule.

A bootstrap inclusion frequency describes ranking stability; it is not the probability that a player is objectively among the ten best.

## 11. Deliverables

The mandatory final submission will contain:

1. Combined ranked top-10 batters.
2. Combined ranked top-10 bowlers.
3. Methodology report.
4. Evidence supporting the selected players.
5. Reliability, uncertainty and limitations analysis.

The following are supplementary:

- Provisional candidate appendix.
- Historical versus recent-form comparison.
- Supporting statistical tables.
- Interactive dashboard.

The dashboard is optional. Analytical correctness and defensibility take priority.

## 12. Seven-Phase Project Roadmap

**Phase 0 — Final Scope and Methodology Design**

Completed. Defines project scope, analytical principles, scoring architecture and validation rules.

**Phase 1 — Data Understanding and Audit**

Inspect the six supplied CSVs, document schemas, coverage, relationships and data-quality issues.

**Phase 2 — Data Cleaning and Reconstruction**

Resolve verified identity conflicts, reconstruct cricket events, legal balls, dismissals and innings structures.

**Phase 3 — Pressure Modelling and Benchmark Construction**

Build first- and second-innings pressure states and validate benchmark coverage and fallback rules.

**Phase 4 — Player Metrics and Scoring Methodology**

Calculate player metrics, finalize numerical weights and eligibility thresholds, and generate normalized scores.

**Phase 5 — Rankings, Uncertainty and Robustness**

Generate rankings, bootstrap uncertainty, sensitivity analysis and top-10 stability assessments.

**Phase 6 — Evidence, Interpretation and Reporting**

Prepare player-level justifications, comparisons, limitations and methodology documentation.

**Phase 7 — Final Submission and Presentation**

Complete quality checks, final deliverables and optional dashboard.

## 13. Approval Gates

Progression will be controlled through four major approval gates:

| Gate | Approval requirement |
|---|---|
| After Phase 1 | Data audit and cleaning plan |
| After Phase 3 | Pressure reconstruction and benchmark validity |
| After Phase 4 | Numerical thresholds, metric weights and scoring formulas locked |
| After Phase 5 | Ranking stability and selection evidence approved |

No phase will be considered complete merely because code executes successfully.

## 14. Outstanding Phase 1 Dependencies

The following items cannot be finalized responsibly before inspecting the actual datasets:

- Exact numerical metric weights.
- Numerical eligibility thresholds.
- Actual season coverage and completeness.
- Reliable reconstruction of bowling conceded runs.
- Availability of sufficient comparable pressure benchmarks.
- Final metric inclusion and exclusion decisions.

These are explicitly deferred to the relevant phases.

## 15. Conclusion

Phase 0 established an interpretable, competition-aware and statistically defensible methodology for evaluating T20 pressure performance.

The project will prioritize contextual comparison over raw totals, statistical evidence over arbitrary thresholds, and transparent scoring over black-box optimization.

The methodology and project scope have been approved.

**Phase 0 is formally closed. Phase 1 — Data Understanding and Audit — is the next authorized project stage, subject to explicit user authorization in the designated Phase 1 conversation.**

---

**End of Phase 0 Report**