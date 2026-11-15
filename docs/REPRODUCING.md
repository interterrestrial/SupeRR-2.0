# Reproducing the analysis

## Run only the dashboard

Use [the dashboard quick start](../dashboard/README.md). Its reviewed `public/dashboard_data.json` is included with the application. Python and the raw data pack are unnecessary for browsing the rankings.

## Rebuild the analytical pipeline

The notebooks use the repository root as their working directory. Keep their filenames and run order intact. Running them regenerates analytical outputs and phase reports, so review or commit any personal edits before a full rerun. Phase 5 performs thousands of match resamples and can take substantially longer than the other phases.

### Source data

Place an authorised copy of the updated six-file pack in this exact local directory:

```text
SupeRR Selector Season 2 | Data Pack/
  ball_by_ball updated.csv
  playing_eleven.csv
  matches.csv
  competition_team_player_mapping.csv
  teams.csv
  competitions.csv
```

Use `ball_by_ball updated.csv`, not the old ball-by-ball file. The raw directory is excluded from Git. The original problem statement PDF is a reference document, not a notebook runtime dependency.

### Environment

The existing analysis environment uses **Python 3.14.7**. The analysis dependencies in [requirements.txt](../requirements.txt) match the versions installed there. Use Python 3.14 for that baseline; the notebook interface is a separate choice. The report was authored using a separate bundled Python 3.12 runtime. A clean dependency installation was not repeated during repository cleanup.

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install jupyterlab ipykernel
python -m ipykernel install --user --name superr-selector --display-name "SupeRR Selector"
jupyter lab
```

Select the **SupeRR Selector** kernel. Start Jupyter from the repository root and verify that `Path.cwd()` is the root before running cells. An IDE notebook interface can use the same environment without JupyterLab.

Parquet is an optional Phase 2 export. Install `pyarrow` if that export is needed; the downstream pipeline reads CSV.

### Execution order

| Order | Notebook | Main outputs |
| --- | --- | --- |
| 1 | [Phases 1–3 consolidated](../SupeRR_Phases_1_to_3_Consolidated.ipynb) | `phase1_outputs/`, `phase2_outputs/`, `phase3_outputs/` |
| 2 | [Phase 4 scoring](../Phase_4_Player_Metrics_and_Scoring.ipynb) | `phase4_outputs/` |
| 3 | [Phase 5 rankings](../Phase_5_Rankings_Uncertainty_and_Robustness.ipynb) | `phase5_outputs/` |
| 4 | [Phase 6 interpretation](../Phase_6_Evidence_Interpretation_and_Reporting.ipynb) | `phase6_outputs/` |
| 5 | [Phase 7A submission freeze](../Phase_7_Submission_Assembly_and_Validation.ipynb) | `phase7_outputs/` |
| 6 | [Phase 7B dashboard bundle](../Phase_7B_Dashboard_Data_Foundation.ipynb) | `phase7_dashboard_data/` and `dashboard/public/dashboard_data.json` |

Run each notebook from top to bottom and inspect its validation gates before proceeding. Generated output directories are deliberately ignored by Git; the dashboard public snapshot is the intentional exception.

The standalone [Phase 3 notebook](../Phase_3_Structural_Pressure_Modelling.ipynb) is an optional entry point after Phase 2 already exists. It is not an additional full-pipeline step. Both Phase 3 entry points import [phase3_structural_pressure.py](../phase3_structural_pressure.py); the consolidated notebook also imports [validate_phase3_outputs.py](../validate_phase3_outputs.py). These helpers are active dependencies, not cleanup leftovers.

### Read-only Phase 3 validation

```bash
python validate_phase3_outputs.py --help
```

Use its documented options against the generated Phase 2 and Phase 3 directories. This validator checks existing outputs; it does not rescore players.

## Editable report

The current deliverable is [the Word report](../final_submission/SupeRR_Selector_Methodology_Report.docx). Review and edit it directly. Export the reviewed version to PDF for submission.

The original authoring helper is preserved at [tools/reports/build_phase7d_report.py](../tools/reports/build_phase7d_report.py). It needs the local analytical outputs, `python-docx`, Pillow, NumPy, pandas and the Arial font files referenced in the script. It generates charts under `tmp/phase7d/` and overwrites the report at its configured output path. It is optional and **must not be rerun over the user's final edited report**. Word rendering and PDF export are separate steps.

## Preserving evidence

Keep model changes separate from documentation or UI edits. The analytical output manifests record SHA-256 hashes. The Phase 7 canonical bundle stores the official ranking signature. Rebuilding or changing sources can change hashes and requires a new evidence review.

The former root-level score/chase CSVs were from the superseded model and have been removed from the working repository. They are not valid inputs to Phases 4–7. Use `phase3_outputs/phase3_structural_pressure_labelled.csv`.
