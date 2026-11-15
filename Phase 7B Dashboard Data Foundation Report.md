# Phase 7B — Dashboard Data Foundation

## Decision

Phase 7B creates a static, validated data contract for the dashboard. It does not recalculate player scores. The dashboard uses the existing Phase 4 format and combined ratings, Phase 5 official rankings and bootstrap evidence, Phase 6 explanations, and the Phase 7A official-ranking signature.

## Filter semantics

Mode contains exactly two independent options: IPL and T20I.

- IPL selected alone: use the Reliable IPL format rating.
- T20I selected alone: use the Reliable T20I format rating.
- IPL and T20I selected together: use the validated combined rating.
- At least one mode must remain selected.

National Team is a searchable multi-select control. All national sides in the supplied T20I competition mappings appear as options. Selecting multiple teams returns the union of their eligible players before ranking.

Examples:

- IPL and Australia ranks Australian players by IPL evidence.
- IPL and T20I with Australia ranks Australian players by the validated combined-rating rule.
- IPL with Australia and India ranks eligible Australian and Indian players together by IPL evidence.

## Candidate population

The dashboard includes the 80 reliable batter candidates and 105 reliable bowler candidates produced by Phase 4. A player may appear in both role populations. Only Reliable evidence can place a player in a single-format leaderboard.

If fewer than ten players qualify for a filter state, the dashboard reports the available Top N rather than adding Provisional or Insufficient evidence.

## National-team mapping

National-team identity is metadata for filtering only. It never changes a rating.

The primary mapping comes from the supplied T20I competition-team-player records. Reliable candidates absent from those 2022–2026 T20I mappings receive an audited supplement. The supplement covers Indian IPL-only candidates and Sunil Narine's West Indies representation.

Every reliable candidate must resolve to exactly one national team before the dashboard bundle is accepted.

## Data contract

The dashboard bundle contains:

- Model and source metadata
- Exactly two available mode values
- Every national-team option
- Role-player candidate records
- Combined and format-specific ratings
- Eligibility and sample evidence
- Metric contributions
- High-pressure and ordinary raw comparisons
- Bootstrap uncertainty where available
- Official-selection status
- Approved Phase 6 narratives for official selections
- Phase 7A official-ranking signature

The canonical JSON file and its dashboard public copy must be byte-identical.

## Validation

Phase 7B verifies:

- Mode options and default selection
- National-team option completeness
- Candidate counts and unique identities
- Complete and unambiguous national-team mapping
- Official default Top-10 reconciliation
- Reliable-only single-format ranking
- Combined-score use when both modes are selected
- Multi-team union semantics
- Filter snapshot coverage
- Ranking-signature preservation
- Canonical and public JSON equality

Execution result: all 16 Phase 7B validation gates passed. The accepted bundle contains 185 reliable role-player rows representing 165 unique players and all 23 national-team options. The canonical JSON and the dashboard copy are byte-identical.

## Handoff to Phase 7C

The React dashboard must read `dashboard/public/dashboard_data.json`. It must not reproduce scoring formulas or edit the generated data. Filter state may change the eligible population and displayed order, but it must never modify a stored rating.
