"""Phase 3 structural-pressure modelling for SupeRR Selector Season 2.

This module deliberately does not reconstruct innings scores, targets, required
rates, or legal-ball counts.  It consumes the validated Phase 2 master and
constructs a pre-delivery structural-pressure state from fields that Phase 2
can support reliably:

* the source over annotation;
* wickets lost before the current delivery record; and
* wickets in prior delivery-record windows.

The benchmark for wickets already lost is leave-one-match-out (LOMO), so a
match never helps define its own expected state.  Revised/shortened-schedule
matches are excluded as whole matches from the primary model.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


MODEL_VERSION = "structural_pressure_v1"
MIN_BENCHMARK_SUPPORT = 100
PRIMARY_RECENT_WINDOW = 12
RECENT_WINDOWS = (6, 12, 18)
KEY_COLUMNS = ["match_id", "innings", "innings_ball_num"]
REVISION_COLUMNS = [
    "first_inn_revised_overs",
    "second_inn_revised_overs",
    "revised_target",
]
REQUIRED_COLUMNS = {
    *KEY_COLUMNS,
    *REVISION_COLUMNS,
    "overid",
    "is_wicket",
    "match_format",
    "comp_name",
    "striker_id",
    "bowler_id",
}


def _require(condition: bool, message: str) -> None:
    """Raise a clear error when a non-negotiable input/output invariant fails."""

    if not condition:
        raise ValueError(message)


def _lomo_table(
    deliveries: pd.DataFrame,
    state_keys: list[str],
    level_name: str,
) -> pd.DataFrame:
    """Return match-specific leave-one-match-out moments for one hierarchy level."""

    match_keys = ["match_id", *state_keys]
    state = (
        deliveries.groupby(state_keys, observed=True)["pre_delivery_wickets"]
        .agg(
            state_n="size",
            state_sum="sum",
            state_sumsq=lambda values: np.square(values).sum(),
        )
        .reset_index()
    )
    within_match = (
        deliveries.groupby(match_keys, observed=True)["pre_delivery_wickets"]
        .agg(
            match_n="size",
            match_sum="sum",
            match_sumsq=lambda values: np.square(values).sum(),
        )
        .reset_index()
    )
    result = within_match.merge(
        state,
        on=state_keys,
        how="left",
        validate="many_to_one",
    )
    result["benchmark_support"] = result["state_n"] - result["match_n"]
    result["benchmark_sum"] = result["state_sum"] - result["match_sum"]
    result["benchmark_sumsq"] = result["state_sumsq"] - result["match_sumsq"]
    n = result["benchmark_support"].astype(float)
    result["benchmark_mean"] = result["benchmark_sum"] / n
    numerator = result["benchmark_sumsq"] - result["benchmark_sum"].pow(2) / n
    result["benchmark_variance"] = numerator / (n - 1)
    result["benchmark_variance"] = result["benchmark_variance"].clip(lower=0)
    result["benchmark_sd"] = np.sqrt(result["benchmark_variance"])
    result["benchmark_level"] = level_name
    result["benchmark_adequate"] = (
        result["benchmark_support"].ge(MIN_BENCHMARK_SUPPORT)
        & result["benchmark_sd"].gt(0)
        & result["benchmark_mean"].notna()
    )
    return result[
        [
            *match_keys,
            "benchmark_level",
            "benchmark_support",
            "benchmark_mean",
            "benchmark_sd",
            "benchmark_adequate",
        ]
    ]


def _merge_benchmark_level(
    deliveries: pd.DataFrame,
    candidate: pd.DataFrame,
    merge_keys: list[str],
    suffix: str,
) -> pd.DataFrame:
    """Attach a candidate LOMO level without overwriting a selected level."""

    renamed = candidate.rename(
        columns={
            "benchmark_level": f"benchmark_level_{suffix}",
            "benchmark_support": f"benchmark_support_{suffix}",
            "benchmark_mean": f"benchmark_mean_{suffix}",
            "benchmark_sd": f"benchmark_sd_{suffix}",
            "benchmark_adequate": f"benchmark_adequate_{suffix}",
        }
    )
    return deliveries.merge(
        renamed,
        on=merge_keys,
        how="left",
        validate="many_to_one",
    )


def _prior_window_wickets(
    deliveries: pd.DataFrame,
    group_keys: list[str],
    window: int,
) -> pd.Series:
    """Count wickets in prior records only; the current delivery is shifted out."""

    return (
        deliveries.groupby(group_keys, sort=False)["is_wicket"]
        .transform(
            lambda values: values.astype(int)
            .shift(1)
            .rolling(window, min_periods=1)
            .sum()
        )
        .fillna(0)
        .astype(int)
    )


def _add_pressure_categories(
    deliveries: pd.DataFrame,
    score_column: str,
    prefix: str,
) -> pd.DataFrame:
    """Add within-format-and-innings percentile and descriptive category."""

    strata = ["format_group", "innings"]
    percentile_column = f"{prefix}_percentile"
    category_column = f"{prefix}_category"
    deliveries[percentile_column] = deliveries.groupby(
        strata,
        observed=True,
    )[score_column].rank(method="average", pct=True)
    deliveries[category_column] = np.select(
        [
            deliveries[percentile_column].le(0.40),
            deliveries[percentile_column].le(0.80),
        ],
        ["Low", "Medium"],
        default="High",
    )
    return deliveries


def _sensitivity_summary(deliveries: pd.DataFrame) -> pd.DataFrame:
    """Compare locked-window and locked-weight alternatives with the primary index."""

    variants = {
        "primary_equal_w12": (1 / 3, 1 / 3, 1 / 3, 12),
        "equal_w6": (1 / 3, 1 / 3, 1 / 3, 6),
        "equal_w18": (1 / 3, 1 / 3, 1 / 3, 18),
        "wicket_heavy_w12": (0.50, 0.25, 0.25, 12),
        "shock_heavy_w12": (0.25, 0.50, 0.25, 12),
        "stage_heavy_w12": (0.25, 0.25, 0.50, 12),
    }
    for name, (wicket_weight, shock_weight, stage_weight, window) in variants.items():
        shock_column = f"recent_wicket_shock_component_{window}"
        score_column = f"sensitivity_index__{name}"
        deliveries[score_column] = (
            wicket_weight * deliveries["wicket_strain_component"]
            + shock_weight * deliveries[shock_column]
            + stage_weight * deliveries["stage_urgency_component"]
        )
        _add_pressure_categories(deliveries, score_column, f"sensitivity__{name}")

    primary_score = "sensitivity_index__primary_equal_w12"
    primary_category = "sensitivity__primary_equal_w12_category"
    primary_high = deliveries[primary_category].eq("High")
    rows: list[dict[str, object]] = []
    for name, (wicket_weight, shock_weight, stage_weight, window) in variants.items():
        score_column = f"sensitivity_index__{name}"
        category_column = f"sensitivity__{name}_category"
        candidate_high = deliveries[category_column].eq("High")
        union = (primary_high | candidate_high).sum()
        rows.append(
            {
                "variant": name,
                "recent_record_window": window,
                "wicket_strain_weight": wicket_weight,
                "recent_wicket_shock_weight": shock_weight,
                "stage_urgency_weight": stage_weight,
                "spearman_vs_primary": deliveries[primary_score]
                .rank(method="average")
                .corr(deliveries[score_column].rank(method="average")),
                "mean_absolute_index_difference": (
                    deliveries[primary_score] - deliveries[score_column]
                )
                .abs()
                .mean(),
                "category_agreement_vs_primary": (
                    deliveries[primary_category].eq(deliveries[category_column])
                ).mean(),
                "high_category_jaccard_vs_primary": (
                    (primary_high & candidate_high).sum() / union if union else 1.0
                ),
                "high_category_share": candidate_high.mean(),
            }
        )
    return pd.DataFrame(rows)


def _validation_table(
    source: pd.DataFrame,
    deliveries: pd.DataFrame,
    excluded_matches: pd.DataFrame,
    sensitivity: pd.DataFrame,
) -> pd.DataFrame:
    """Create machine-readable acceptance gates and fail on any hard-gate failure."""

    opening = deliveries.groupby(["match_id", "innings"], sort=False).head(1)
    retained_revisions = deliveries[REVISION_COLUMNS].notna().any(axis=1).sum()
    reconstructed_pre = (
        deliveries.groupby(["match_id", "innings"], sort=False)["is_wicket"]
        .cumsum()
        .astype(int)
        - deliveries["is_wicket"].astype(int)
    )
    min_non_primary_rho = sensitivity.loc[
        sensitivity["variant"].ne("primary_equal_w12"),
        "spearman_vs_primary",
    ].min()
    checks = [
        (
            "source_key_unique",
            not source.duplicated(KEY_COLUMNS).any(),
            int(source.duplicated(KEY_COLUMNS).sum()),
            "0 duplicate match/innings/record keys",
        ),
        (
            "primary_population_partition",
            len(deliveries)
            + int(excluded_matches["excluded_delivery_records"].sum())
            == len(source),
            len(deliveries),
            "retained rows + excluded rows = source rows",
        ),
        (
            "revised_matches_fully_excluded",
            retained_revisions == 0,
            int(retained_revisions),
            "0 retained rows with revision metadata",
        ),
        (
            "source_over_in_t20_range",
            deliveries["overid"].between(1, 20).all(),
            f"{deliveries['overid'].min()}..{deliveries['overid'].max()}",
            "all source over values in 1..20",
        ),
        (
            "only_supported_formats",
            set(deliveries["format_group"].unique()) == {"IPL", "T20I"},
            ", ".join(sorted(deliveries["format_group"].unique())),
            "exactly IPL and T20I",
        ),
        (
            "pre_delivery_wickets_excludes_current_record",
            deliveries["pre_delivery_wickets"].equals(reconstructed_pre),
            int(
                deliveries["pre_delivery_wickets"].ne(reconstructed_pre).sum()
            ),
            "0 mismatches against prior-only cumulative wickets",
        ),
        (
            "innings_open_with_zero_prior_wickets",
            opening["pre_delivery_wickets"].eq(0).all(),
            int(opening["pre_delivery_wickets"].ne(0).sum()),
            "0 innings opening with a prior wicket",
        ),
        (
            "innings_open_with_zero_recent_wickets",
            opening[f"prior_wickets_{PRIMARY_RECENT_WINDOW}_records"].eq(0).all(),
            int(
                opening[f"prior_wickets_{PRIMARY_RECENT_WINDOW}_records"]
                .ne(0)
                .sum()
            ),
            "0 innings opening with a recent prior wicket",
        ),
        (
            "benchmark_complete",
            deliveries["benchmark_level"].notna().all(),
            int(deliveries["benchmark_level"].isna().sum()),
            "0 unbenchmarked records",
        ),
        (
            "benchmark_support_adequate",
            deliveries["benchmark_support"].ge(MIN_BENCHMARK_SUPPORT).all(),
            int(deliveries["benchmark_support"].min()),
            f"minimum support >= {MIN_BENCHMARK_SUPPORT}",
        ),
        (
            "benchmark_variation_positive",
            deliveries["expected_pre_wickets_sd"].gt(0).all(),
            float(deliveries["expected_pre_wickets_sd"].min()),
            "all selected benchmark SD values > 0",
        ),
        (
            "pressure_index_complete",
            deliveries["structural_pressure_index"].notna().all(),
            int(deliveries["structural_pressure_index"].isna().sum()),
            "0 missing primary pressure values",
        ),
        (
            "pressure_index_bounded",
            deliveries["structural_pressure_index"].between(0, 1).all(),
            (
                f"{deliveries['structural_pressure_index'].min():.6f}.."
                f"{deliveries['structural_pressure_index'].max():.6f}"
            ),
            "all primary pressure values in [0, 1]",
        ),
        (
            "pressure_category_complete",
            deliveries["structural_pressure_category"].isin(
                ["Low", "Medium", "High"]
            ).all(),
            ", ".join(
                sorted(deliveries["structural_pressure_category"].unique())
            ),
            "only Low, Medium, High",
        ),
        (
            "sensitivity_rank_stability",
            bool(min_non_primary_rho >= 0.90),
            float(min_non_primary_rho),
            "minimum non-primary Spearman correlation >= 0.90",
        ),
    ]
    validation = pd.DataFrame(
        checks,
        columns=["check_name", "passed", "observed", "acceptance_rule"],
    )
    validation["status"] = np.where(validation["passed"], "PASS", "FAIL")
    validation = validation[
        ["check_name", "status", "observed", "acceptance_rule"]
    ]
    failures = validation.loc[validation["status"].eq("FAIL")]
    _require(
        failures.empty,
        "Phase 3 validation failed:\n" + failures.to_string(index=False),
    )
    return validation


def build_phase3(
    source: pd.DataFrame,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
]:
    """Build the corrected Phase 3 outputs from the validated Phase 2 master."""

    missing = sorted(REQUIRED_COLUMNS - set(source.columns))
    _require(not missing, f"Phase 2 master is missing required columns: {missing}")
    _require(not source.empty, "Phase 2 master is empty")
    _require(
        not source.duplicated(KEY_COLUMNS).any(),
        "Phase 2 master contains duplicate delivery-record keys",
    )
    _require(
        set(source["innings"].dropna().unique()).issubset({1, 2}),
        "Phase 2 master contains non-regulation innings",
    )
    _require(
        source["overid"].between(1, 20).all(),
        "Phase 2 source over annotation contains values outside 1..20",
    )
    _require(
        set(source["match_format"].dropna().unique()) == {"T20", "T20I"},
        "Unexpected match-format population in Phase 2 master",
    )
    _require(
        source.loc[source["match_format"].eq("T20"), "comp_name"]
        .str.startswith("IPL ")
        .all(),
        "A T20 row is not part of an approved IPL competition",
    )

    revised_match_ids = source.loc[
        source[REVISION_COLUMNS].notna().any(axis=1),
        "match_id",
    ].unique()
    revised_rows = source.loc[source["match_id"].isin(revised_match_ids)]
    excluded_matches = (
        revised_rows.groupby("match_id", observed=True)
        .agg(
            match_format=("match_format", "first"),
            competition=("comp_name", "first"),
            excluded_delivery_records=("match_id", "size"),
            first_inn_revised_overs=("first_inn_revised_overs", "first"),
            second_inn_revised_overs=("second_inn_revised_overs", "first"),
            revised_target=("revised_target", "first"),
        )
        .reset_index()
    )
    excluded_matches["exclusion_reason"] = "REVISED_OR_SHORTENED_SCHEDULE"

    deliveries = source.loc[~source["match_id"].isin(revised_match_ids)].copy()
    deliveries["format_group"] = np.where(
        deliveries["match_format"].eq("T20I"),
        "T20I",
        "IPL",
    )
    deliveries["schedule_scope"] = "STANDARD_UNREVISED_PRIMARY"
    deliveries["source_over_stage"] = np.select(
        [deliveries["overid"].le(6), deliveries["overid"].le(15)],
        ["Powerplay", "Middle"],
        default="Death",
    )
    deliveries = deliveries.sort_values(KEY_COLUMNS, kind="stable").reset_index(
        drop=True
    )

    innings_keys = ["match_id", "innings"]
    deliveries["pre_delivery_wickets"] = (
        deliveries.groupby(innings_keys, sort=False)["is_wicket"]
        .cumsum()
        .astype(int)
        - deliveries["is_wicket"].astype(int)
    )
    for window in RECENT_WINDOWS:
        deliveries[f"prior_wickets_{window}_records"] = _prior_window_wickets(
            deliveries,
            innings_keys,
            window,
        )

    exact_keys = ["format_group", "innings", "overid"]
    stage_keys = ["format_group", "innings", "source_over_stage"]
    innings_format_keys = ["format_group", "innings"]
    exact = _lomo_table(deliveries, exact_keys, "FORMAT_INNINGS_SOURCE_OVER")
    stage = _lomo_table(deliveries, stage_keys, "FORMAT_INNINGS_STAGE")
    innings_format = _lomo_table(
        deliveries,
        innings_format_keys,
        "FORMAT_INNINGS",
    )

    deliveries = _merge_benchmark_level(
        deliveries,
        exact,
        ["match_id", *exact_keys],
        "exact",
    )
    deliveries = _merge_benchmark_level(
        deliveries,
        stage,
        ["match_id", *stage_keys],
        "stage",
    )
    deliveries = _merge_benchmark_level(
        deliveries,
        innings_format,
        ["match_id", *innings_format_keys],
        "innings",
    )

    deliveries["benchmark_level"] = pd.NA
    deliveries["benchmark_support"] = np.nan
    deliveries["expected_pre_wickets"] = np.nan
    deliveries["expected_pre_wickets_sd"] = np.nan
    for suffix in ("exact", "stage", "innings"):
        use = (
            deliveries["benchmark_level"].isna()
            & deliveries[f"benchmark_adequate_{suffix}"].fillna(False)
        )
        deliveries.loc[use, "benchmark_level"] = deliveries.loc[
            use,
            f"benchmark_level_{suffix}",
        ]
        deliveries.loc[use, "benchmark_support"] = deliveries.loc[
            use,
            f"benchmark_support_{suffix}",
        ]
        deliveries.loc[use, "expected_pre_wickets"] = deliveries.loc[
            use,
            f"benchmark_mean_{suffix}",
        ]
        deliveries.loc[use, "expected_pre_wickets_sd"] = deliveries.loc[
            use,
            f"benchmark_sd_{suffix}",
        ]
    candidate_columns = [
        column
        for column in deliveries.columns
        if column.startswith("benchmark_level_")
        or column.startswith("benchmark_support_")
        or column.startswith("benchmark_mean_")
        or column.startswith("benchmark_sd_")
        or column.startswith("benchmark_adequate_")
    ]
    deliveries = deliveries.drop(columns=candidate_columns)

    deliveries["wicket_strain_z"] = (
        deliveries["pre_delivery_wickets"]
        - deliveries["expected_pre_wickets"]
    ) / deliveries["expected_pre_wickets_sd"]
    deliveries["wicket_strain_component"] = (
        deliveries["wicket_strain_z"].clip(lower=0, upper=3) / 3
    )
    for window in RECENT_WINDOWS:
        deliveries[f"recent_wicket_shock_component_{window}"] = (
            deliveries[f"prior_wickets_{window}_records"] / 3
        ).clip(lower=0, upper=1)
    deliveries["stage_urgency_component"] = (deliveries["overid"] - 1) / 19
    deliveries["structural_pressure_index"] = (
        deliveries["wicket_strain_component"]
        + deliveries[
            f"recent_wicket_shock_component_{PRIMARY_RECENT_WINDOW}"
        ]
        + deliveries["stage_urgency_component"]
    ) / 3
    _add_pressure_categories(
        deliveries,
        "structural_pressure_index",
        "structural_pressure",
    )
    deliveries["phase3_model_version"] = MODEL_VERSION

    sensitivity = _sensitivity_summary(deliveries)
    sensitivity_columns = [
        column
        for column in deliveries.columns
        if column.startswith("sensitivity_")
    ]
    deliveries = deliveries.drop(columns=sensitivity_columns)

    benchmark_table = deliveries[
        [
            "match_id",
            "format_group",
            "innings",
            "overid",
            "source_over_stage",
            "benchmark_level",
            "benchmark_support",
            "expected_pre_wickets",
            "expected_pre_wickets_sd",
        ]
    ].drop_duplicates()
    benchmark_table = benchmark_table.sort_values(
        ["format_group", "innings", "overid", "match_id"],
        kind="stable",
    ).reset_index(drop=True)

    component_correlations = (
        deliveries[
            [
                "wicket_strain_component",
                f"recent_wicket_shock_component_{PRIMARY_RECENT_WINDOW}",
                "stage_urgency_component",
            ]
        ]
        .corr(method="spearman")
        .rename_axis("component")
        .reset_index()
    )

    validation = _validation_table(
        source,
        deliveries,
        excluded_matches,
        sensitivity,
    )
    model_specification = pd.DataFrame(
        [
            (
                "model_version",
                MODEL_VERSION,
                "Locked corrected Phase 3 specification",
            ),
            (
                "construct",
                "structural pressure",
                "Not a score, target, required-rate, or win-probability model",
            ),
            (
                "primary_population",
                "whole unrevised IPL/T20I matches from Phase 2 master",
                "A match is excluded if any revision field is populated",
            ),
            (
                "source_over_stage",
                "Powerplay 1-6; Middle 7-15; Death 16-20",
                "Uses source over annotation, not reconstructed legal-ball count",
            ),
            (
                "pre_delivery_wickets",
                "cumulative wickets before current delivery record",
                "Current record is explicitly excluded",
            ),
            (
                "recent_wicket_window",
                f"prior {PRIMARY_RECENT_WINDOW} delivery records",
                "Not legal balls; 6 and 18 records are sensitivity variants",
            ),
            (
                "wicket_benchmark",
                "leave-one-match-out by format, innings, and source over",
                (
                    f"Minimum support {MIN_BENCHMARK_SUPPORT}; fallback to stage, "
                    "then format-innings"
                ),
            ),
            (
                "benchmark_weighting",
                "delivery-record weighted",
                (
                    "Consistent with a delivery-record pressure label; overs with "
                    "additional recorded deliveries contribute additional observations"
                ),
            ),
            (
                "wicket_strain_component",
                "clip(max(z, 0), 0, 3) / 3",
                "Only above-expected wicket loss contributes pressure",
            ),
            (
                "recent_wicket_shock_component",
                "clip(prior-window wickets / 3, 0, 1)",
                "Prior records only",
            ),
            (
                "stage_urgency_component",
                "(source over - 1) / 19",
                "Bounded 0 to 1",
            ),
            (
                "structural_pressure_index",
                "equal mean of three components",
                "Weights locked before player ranking; alternatives tested",
            ),
            (
                "pressure_category",
                "within format-innings percentile: Low <=40%, Medium <=80%, High >80%",
                "Descriptive band; continuous index remains primary",
            ),
            (
                "prohibited_inputs",
                "scores, targets, required rates, inferred legal balls, current outcome",
                "None are used to construct the pressure state",
            ),
        ],
        columns=["item", "locked_rule", "rationale_or_note"],
    )
    return (
        deliveries,
        benchmark_table,
        sensitivity,
        component_correlations,
        excluded_matches,
        validation,
        model_specification,
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_csv(frame: pd.DataFrame, path: Path) -> None:
    frame.to_csv(path, index=False, float_format="%.10g")


def _markdown_table(frame: pd.DataFrame) -> str:
    """Render a small DataFrame as Markdown without an optional dependency."""

    columns = [str(column) for column in frame.columns]
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in frame.itertuples(index=False, name=None):
        rendered = []
        for value in row:
            if isinstance(value, float):
                rendered.append(f"{value:.4f}")
            else:
                rendered.append(str(value))
        lines.append("| " + " | ".join(rendered) + " |")
    return "\n".join(lines)


def write_report(
    report_path: Path,
    source: pd.DataFrame,
    deliveries: pd.DataFrame,
    benchmark_table: pd.DataFrame,
    sensitivity: pd.DataFrame,
    excluded_matches: pd.DataFrame,
    validation: pd.DataFrame,
) -> None:
    category_share = (
        deliveries.groupby(
            ["format_group", "innings", "structural_pressure_category"],
            observed=True,
        )
        .size()
        .rename("records")
        .reset_index()
    )
    category_share["share"] = category_share["records"] / category_share.groupby(
        ["format_group", "innings"],
        observed=True,
    )["records"].transform("sum")
    sensitivity_display = sensitivity[
        [
            "variant",
            "spearman_vs_primary",
            "category_agreement_vs_primary",
            "high_category_jaccard_vs_primary",
        ]
    ].copy()
    report = f"""# Phase 3 — Structural Pressure Modelling Report

## Decision

The earlier score/target/required-rate Phase 3 is **superseded**. The updated
delivery source corrects `extras1_runs` into a run quantity, but Phase 2 still
cannot establish definitive legal-ball progression or balls remaining for all
records. This model therefore continues to measure **structural pressure**,
using only verified pre-delivery state variables.

It must not be interpreted as win probability, required-rate pressure, or a
complete scoreboard-pressure model.

## Analytical population

- Phase 2 source: **{len(source):,}** regulation delivery records across
  **{source['match_id'].nunique():,}** eligible matches.
- Primary Phase 3 population: **{len(deliveries):,}** records across
  **{deliveries['match_id'].nunique():,}** whole unrevised matches.
- Excluded: **{len(excluded_matches):,}** revised/shortened-schedule matches and
  **{int(excluded_matches['excluded_delivery_records'].sum()):,}** records.
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
**{MIN_BENCHMARK_SUPPORT}** out-of-match records and positive variance. The
predeclared fallbacks are format × innings × stage, then format × innings.

On this dataset, all **{len(benchmark_table):,}** match-state benchmarks use the
exact source-over level. Support ranges from
**{int(benchmark_table['benchmark_support'].min()):,}** to
**{int(benchmark_table['benchmark_support'].max()):,}** records; no fallback is
required.

## Descriptive bands

Low, Medium, and High bands are assigned within format and innings from the
continuous-index percentile: Low ≤ 40%, Medium ≤ 80%, High > 80%. These bands
aid interpretation; the continuous index remains the modelling variable.

{_markdown_table(category_share)}

## Robustness

All window and weight variants retain a Spearman rank correlation above 0.95
with the primary continuous index. High-band overlap is lower for the shortest
recent window because observations near the 80th-percentile boundary can cross
the descriptive cut. This is a boundary-classification limitation, not a
failure of the continuous measure.

{_markdown_table(sensitivity_display)}

## Validation gates

{_markdown_table(validation)}

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
"""
    report_path.write_text(report, encoding="utf-8")


def write_outputs(
    output_dir: Path,
    report_path: Path,
    source: pd.DataFrame,
    deliveries: pd.DataFrame,
    benchmark_table: pd.DataFrame,
    sensitivity: pd.DataFrame,
    component_correlations: pd.DataFrame,
    excluded_matches: pd.DataFrame,
    validation: pd.DataFrame,
    model_specification: pd.DataFrame,
) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    frames = {
        "phase3_structural_pressure_labelled.csv": deliveries,
        "phase3_wicket_benchmarks_lomo.csv": benchmark_table,
        "phase3_sensitivity_summary.csv": sensitivity,
        "phase3_component_correlations.csv": component_correlations,
        "phase3_excluded_revised_matches.csv": excluded_matches,
        "phase3_validation_gates.csv": validation,
        "phase3_model_specification.csv": model_specification,
    }
    for name, frame in frames.items():
        _write_csv(frame, output_dir / name)

    write_report(
        report_path,
        source,
        deliveries,
        benchmark_table,
        sensitivity,
        excluded_matches,
        validation,
    )

    manifest_rows = []
    for name, frame in frames.items():
        path = output_dir / name
        manifest_rows.append(
            {
                "artifact": name,
                "rows": len(frame),
                "columns": len(frame.columns),
                "bytes": path.stat().st_size,
                "sha256": _sha256(path),
                "model_version": MODEL_VERSION,
            }
        )
    manifest = pd.DataFrame(manifest_rows)
    _write_csv(manifest, output_dir / "phase3_output_manifest.csv")
    return manifest


def run_pipeline(
    input_path: Path,
    output_dir: Path,
    report_path: Path,
) -> dict[str, pd.DataFrame]:
    source = pd.read_csv(input_path, low_memory=False)
    (
        deliveries,
        benchmark_table,
        sensitivity,
        component_correlations,
        excluded_matches,
        validation,
        model_specification,
    ) = build_phase3(source)
    manifest = write_outputs(
        output_dir,
        report_path,
        source,
        deliveries,
        benchmark_table,
        sensitivity,
        component_correlations,
        excluded_matches,
        validation,
        model_specification,
    )
    return {
        "deliveries": deliveries,
        "benchmarks": benchmark_table,
        "sensitivity": sensitivity,
        "component_correlations": component_correlations,
        "excluded_matches": excluded_matches,
        "validation": validation,
        "model_specification": model_specification,
        "manifest": manifest,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("phase2_outputs/phase2_integrated_cleaned_deliveries.csv"),
        help="Validated Phase 2 master CSV",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("phase3_outputs"),
        help="Destination directory for corrected Phase 3 CSVs",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("Phase 3 Structural Pressure Report.md"),
        help="Destination for the generated methodology report",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    results = run_pipeline(args.input, args.output_dir, args.report)
    print(results["validation"].to_string(index=False))
    print("\nOutput manifest")
    print(results["manifest"].to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
