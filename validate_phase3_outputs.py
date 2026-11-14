"""Independent, read-only validation of the corrected Phase 3 artifacts."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd


KEYS = ["match_id", "innings", "innings_ball_num"]
REVISION_COLUMNS = [
    "first_inn_revised_overs",
    "second_inn_revised_overs",
    "revised_target",
]


def _hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate(source_path: Path, output_dir: Path) -> pd.DataFrame:
    source = pd.read_csv(source_path, low_memory=False)
    labelled_path = output_dir / "phase3_structural_pressure_labelled.csv"
    labelled = pd.read_csv(labelled_path, low_memory=False)
    excluded = pd.read_csv(output_dir / "phase3_excluded_revised_matches.csv")
    benchmarks = pd.read_csv(output_dir / "phase3_wicket_benchmarks_lomo.csv")
    sensitivity = pd.read_csv(output_dir / "phase3_sensitivity_summary.csv")
    gates = pd.read_csv(output_dir / "phase3_validation_gates.csv")
    manifest = pd.read_csv(output_dir / "phase3_output_manifest.csv")

    labelled = labelled.sort_values(KEYS, kind="stable").reset_index(drop=True)
    group_keys = ["match_id", "innings"]
    prior_wickets = (
        labelled.groupby(group_keys, sort=False)["is_wicket"]
        .cumsum()
        .astype(int)
        - labelled["is_wicket"].astype(int)
    )
    prior_12 = (
        labelled.groupby(group_keys, sort=False)["is_wicket"]
        .transform(
            lambda values: values.astype(int)
            .shift(1)
            .rolling(12, min_periods=1)
            .sum()
        )
        .fillna(0)
        .astype(int)
    )
    formula = (
        labelled["wicket_strain_component"]
        + labelled["recent_wicket_shock_component_12"]
        + labelled["stage_urgency_component"]
    ) / 3

    # Independently recompute every exact leave-one-match-out benchmark.
    state_keys = ["format_group", "innings", "overid"]
    match_state_keys = ["match_id", *state_keys]
    state = (
        labelled.groupby(state_keys, observed=True)["pre_delivery_wickets"]
        .agg(
            n="size",
            total="sum",
            sumsq=lambda values: np.square(values).sum(),
        )
        .reset_index()
    )
    within = (
        labelled.groupby(match_state_keys, observed=True)["pre_delivery_wickets"]
        .agg(
            match_n="size",
            match_total="sum",
            match_sumsq=lambda values: np.square(values).sum(),
        )
        .reset_index()
    )
    recomputed = within.merge(state, on=state_keys, validate="many_to_one")
    recomputed["support"] = recomputed["n"] - recomputed["match_n"]
    recomputed["mean"] = (
        recomputed["total"] - recomputed["match_total"]
    ) / recomputed["support"]
    eff_sumsq = recomputed["sumsq"] - recomputed["match_sumsq"]
    variance = (
        eff_sumsq
        - (recomputed["total"] - recomputed["match_total"]).pow(2)
        / recomputed["support"]
    ) / (recomputed["support"] - 1)
    recomputed["sd"] = np.sqrt(variance.clip(lower=0))
    comparison = benchmarks.merge(
        recomputed[match_state_keys + ["support", "mean", "sd"]],
        on=match_state_keys,
        how="outer",
        validate="one_to_one",
        indicator=True,
    )

    manifest_hashes_match = True
    for row in manifest.itertuples(index=False):
        artifact_path = output_dir / row.artifact
        if not artifact_path.exists() or _hash(artifact_path) != row.sha256:
            manifest_hashes_match = False
            break

    checks = [
        (
            "source_partition",
            len(labelled) + excluded["excluded_delivery_records"].sum()
            == len(source),
        ),
        ("labelled_key_unique", not labelled.duplicated(KEYS).any()),
        (
            "no_revised_metadata_in_primary",
            not labelled[REVISION_COLUMNS].notna().any(axis=1).any(),
        ),
        (
            "prior_wickets_recomputed",
            labelled["pre_delivery_wickets"].equals(prior_wickets),
        ),
        (
            "recent_window_recomputed",
            labelled["prior_wickets_12_records"].equals(prior_12),
        ),
        (
            "primary_formula_recomputed",
            np.allclose(
                labelled["structural_pressure_index"],
                formula,
                rtol=0,
                atol=1e-9,
            ),
        ),
        (
            "benchmark_keys_complete",
            comparison["_merge"].eq("both").all(),
        ),
        (
            "benchmark_support_recomputed",
            np.allclose(
                comparison["benchmark_support"],
                comparison["support"],
                rtol=0,
                atol=0,
            ),
        ),
        (
            "benchmark_mean_recomputed",
            np.allclose(
                comparison["expected_pre_wickets"],
                comparison["mean"],
                rtol=0,
                atol=1e-8,
            ),
        ),
        (
            "benchmark_sd_recomputed",
            np.allclose(
                comparison["expected_pre_wickets_sd"],
                comparison["sd"],
                rtol=0,
                atol=1e-8,
            ),
        ),
        (
            "all_pipeline_gates_pass",
            gates["status"].eq("PASS").all(),
        ),
        (
            "all_non_primary_sensitivity_rho_above_090",
            sensitivity.loc[
                sensitivity["variant"].ne("primary_equal_w12"),
                "spearman_vs_primary",
            ].ge(0.90).all(),
        ),
        ("manifest_hashes_match", manifest_hashes_match),
    ]
    result = pd.DataFrame(checks, columns=["independent_check", "passed"])
    result["status"] = np.where(result["passed"], "PASS", "FAIL")
    if not result["passed"].all():
        raise AssertionError(
            "Independent Phase 3 validation failed:\n"
            + result.loc[~result["passed"]].to_string(index=False)
        )
    return result[["independent_check", "status"]]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("phase2_outputs/phase2_integrated_cleaned_deliveries.csv"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("phase3_outputs"),
    )
    args = parser.parse_args()
    print(validate(args.source, args.output_dir).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
