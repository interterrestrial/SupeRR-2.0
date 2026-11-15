# Phase 7A — Submission Foundation Report

## Decision

Phase 7A freezes the validated Phase 3–6 evidence used by the final submission. It creates a single source of truth for the dashboard, report, presentation, and later video. It does not recalculate or change player scores.

The official ranking order remains owned by Phase 5. Player explanations, format-status language, pressure evidence, and uncertainty language remain owned by Phase 6.

## Frozen analytical rules

- The official period is all eligible evidence from 2022 through 2026.
- No recent-form weight is used.
- IPL and T20I are evaluated and normalized separately.
- When both formats are Reliable, their ratings are combined 50/50.
- When only one format is Reliable, that format is used alone.
- A missing or unreliable format is not assigned zero.
- Official order uses the unrounded combined rating, with player ID as the deterministic tie-break.

## Frozen pressure interpretation

The submission must describe the model as structural pressure. The pressure state is determined before the current delivery outcome from:

1. Wicket strain relative to a leave-one-match-out benchmark.
2. Wickets in the previous 12 delivery records.
3. Innings-stage urgency from the supplied source-over annotation.

High pressure is the top 20 percent of the continuous structural-pressure index within format and innings. The model is not win probability, required-run-rate pressure, or a complete scoreboard-pressure model.

## Canonical evidence bundle

The Phase 7A notebook creates:

- A canonical table containing the 20 official selections and Phase 6 evidence.
- A machine-readable JSON bundle for later artifacts.
- A claim registry with approved methodology and player narratives.
- A terminology registry with required cautions.
- A source manifest containing hashes of the frozen Phase 3–6 inputs.
- Shared design tokens and submission-structure definitions.
- Validation gates and completion metrics.

The official ranking signature is calculated from role, rank, player ID, player name, qualifying formats, and the combined rating represented to ten decimal places. Later artifacts can use this signature to detect ranking drift.

## Official selections

### Batters

1. Nicholas Pooran
2. Jimmy Neesham
3. Hardik Pandya
4. Jos Buttler
5. Jaker Ali Anik
6. Romario Shepherd
7. Suryakumar Yadav
8. Iftikhar Ahmed
9. Shreyas Iyer
10. Rinku Singh

### Bowlers

1. Sufiyan Muqeem
2. Kuldeep Yadav
3. Sunil Narine
4. Mohammad Nawaz
5. Abrar Ahmed
6. Mitchell Starc
7. Eshan Malinga
8. Varun Chakravarthy
9. Suyash Sharma
10. Mohit Sharma

## Controlled uncertainty language

Bootstrap inclusion measures ranking stability under match resampling and eligibility changes. It is not the probability that a player is objectively Top 10.

All 20 official selections retain the Phase 6 `BOUNDARY_TOP10` classification. This qualification must appear in the final report and must not be hidden by presentation or dashboard styling. The locked full-data ranking remains official; boundary status does not trigger automatic replacement.

## Visual system

The Phase 7 visual identity uses midnight and slate foundations, teal for validated evidence, gold for official ranks, coral for uncertainty, and off-white report surfaces. Avenir Next is the primary typeface with Arial as fallback.

The detailed rules are maintained in `Phase 7 Visual Identity Specification.md` and mirrored as machine-readable design tokens.

## Submission structure

The artifact registry covers Phase 7A through Phase 7G. Phase 7G remains deferred and will receive a separate video plan before implementation.

Phase 7A does not create report PDFs, presentation files, dashboard code, national-team mappings, or video assets. Those remain assigned to their approved later subphases.

## Validation requirements

Phase 7A is complete only if:

- Every required source file exists and is hashed.
- All Phase 3–6 upstream validation gates pass.
- There are exactly 10 official batters and 10 official bowlers.
- Phase 5 and Phase 6 agree on role, rank, player ID, player name, qualifying formats, and rating.
- Every format used in an official score is Reliable.
- Every excluded format has an explanation.
- Each selected player has selection, format, pressure, and uncertainty claims.
- The canonical CSV and JSON bundle contain exactly the same 20 selections.
- All Phase 7A validation gates pass.

## Implementation result

Phase 7A froze 27 upstream source files and produced 90 approved claims, 12 controlled terms, and 18 shared design tokens. All 20 Phase 7A validation gates passed with zero failures. The validation also reconciles every artifact declared by the Phase 3–6 output manifests against its stored SHA-256 hash.

The official ranking signature is:

`5295c708a26033d841f85a6159c3db53096fbf20058303c7ce85093019f63f99`

## Handoff to Phase 7B

Phase 7B should read the canonical Phase 7A bundle rather than rebuilding the official selections from multiple upstream files. It may add national-team identity and dashboard filtering fields, but it must not alter ranks, ratings, qualifying formats, or approved evidence language.
