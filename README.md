# SupeRR Selector Season 2

**Cricket player rankings under structural pressure using IPL and T20I evidence from 2022 to 2026.**

This project identifies ten batters and ten bowlers using pre-delivery match context, performance relative to expected outcomes, and match-level uncertainty checks. It includes a reproducible notebook pipeline, an interactive dashboard, and an editable methodology report for the Rajasthan Royals hackathon.

## Start here

| Explore | Entry point |
| --- | --- |
| Understand the approach and results | [Methodology report](final_submission/SupeRR_Selector_Methodology_Report.docx) |
| Review both official Top 10 lists | [Official selections](docs/RESULTS.md) |
| Run the dashboard locally | [Dashboard setup](dashboard/README.md) |
| Reproduce the analysis | [Reproduction guide](docs/REPRODUCING.md) |
| Find phase reports and design references | [Documentation index](docs/README.md) |
| Check what is complete and what remains | [Project status](docs/STATUS.md) |

## The analytical approach

1. **Audit and reconstruct.** Join the six supplied CSV sources using stable IDs, verify match and delivery records, and document unresolved evidence.
2. **Define pressure before the outcome.** Combine wicket strain, wickets in the prior 12 delivery records, and innings-stage urgency. High pressure is above the 80th percentile within format and innings.
3. **Measure value relative to context.** Compare batting scoring and survival, or bowling wickets and run suppression, with format-specific outcome benchmarks.
4. **Control sample size and format differences.** Apply eligibility gates, shrinkage and separate IPL/T20I normalization. Use a 50/50 combination only when both formats are Reliable; otherwise use the single Reliable format.
5. **Test ranking stability.** Run 5,000 fixed-benchmark and 1,000 nested-benchmark match resamples, 13 deterministic scenarios, and leave-one-player-out benchmark checks.

All eligible 2022–2026 evidence is used without recent-form weighting. The model measures **structural pressure**; it does not reconstruct required run rate, win probability or exact legal balls remaining.

## Evidence in scope

| Measure | Population |
| --- | ---: |
| Matches in the pressure model | 789 |
| Pressure-labelled delivery records | 188,330 |
| Reliable batter candidates | 80 |
| Reliable bowler candidates | 105 |
| Official selections | 10 batters and 10 bowlers |
| National-team filter options | 23 |

**Reading the results:** Nicholas Pooran leads the batter list at 62.21 using Reliable IPL evidence. Sufiyan Muqeem leads the bowler list at 69.67 using Reliable T20I evidence. Every official selection remains a **Boundary Top 10** result under the predefined requirement of at least 75% inclusion in both bootstrap modes. Bootstrap frequency describes ranking stability, not the probability of a player being objectively Top 10.

## Dashboard quick start

Requires **Node.js 22.x** and npm. The included static data snapshot is sufficient to run the dashboard; raw data and Python are not required.

```bash
cd dashboard
npm ci
npm run dev
```

Open [localhost:3000](http://localhost:3000). To check the app:

```bash
npm run lint
npm run build
```

The dashboard uses Next.js, React and TypeScript. Users can choose batters or bowlers, select IPL, T20I or both, and filter multiple national teams. Player details show pressure comparisons, score contributions, sample sizes and uncertainty. The interface uses the report's navy, pink and white visual identity.

## Repository map

```text
.
├── README.md
├── docs/                         Navigation, results, reproduction and status
├── dashboard/                    Next.js app and publishable static data
├── final_submission/             Editable methodology report
├── tools/reports/                Report authoring helper
├── SupeRR_Phases_1_to_3_Consolidated.ipynb
├── Phase_4_Player_Metrics_and_Scoring.ipynb
├── Phase_5_Rankings_Uncertainty_and_Robustness.ipynb
├── Phase_6_Evidence_Interpretation_and_Reporting.ipynb
├── Phase_7_Submission_Assembly_and_Validation.ipynb
├── Phase_7B_Dashboard_Data_Foundation.ipynb
├── Phase_3_Structural_Pressure_Modelling.ipynb  Optional Phase 3 entry point
├── phase3_structural_pressure.py  Shared analytical dependency
├── validate_phase3_outputs.py     Independent Phase 3 validation
├── requirements.txt
└── Phase … Report.md              Detailed analytical phase reports
```

Notebooks and phase reports retain their root paths because the pipeline and frozen manifests refer to them. The raw data pack, generated `phase*_outputs/` folders, environments and temporary renders remain local and are ignored by Git. See [reproduction instructions](docs/REPRODUCING.md) for the required source filenames.

## Submission status

Analysis through Phase 6, the Phase 7A evidence freeze, Phase 7B dashboard data, the local dashboard and the Phase 7D editable report are implemented. Report and dashboard review comes next. Permanent Vercel deployment is deferred. Presentation work will follow the user's final report; final submission QA and the video remain pending.

The report contains editable Word text and tables with embedded chart images. Export the reviewed document to PDF for submission. No presentation or video is claimed as complete.

## Data and attribution

The source data was supplied for SupeRR Selector Season 2. This repository does not redistribute the raw data pack or grant rights to it. Reproduction requires an authorised copy of the updated pack. The reviewed dashboard snapshot contains derived player evidence and can run independently of that pack.

Rankings represent the supplied historical evidence, not confirmed auction availability, price or the final IPL 2027 squad. The original brief and the detailed model limitations are discussed in the report.
