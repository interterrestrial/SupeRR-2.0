SUPERR SELECTOR SEASON 2

# Phase 1 Report

Data Understanding & Audit

Approved analysis population and data-quality assessment

## Document status

| Item \| Status / value \|

| --- \| --- \|

| Project \| SupeRR Selector Season 2 \|

| Phase \| Phase 1 --- Data Understanding & Audit \|

| Status \| Approved by user \|

| Approval \| Approve proposed population and documented treatment
  approach; retain unresolved issues rather than silently correcting
  them. \|

| Primary population \| 813 matches; 192,235 regulation deliveries \|

| Super Overs \| 26 deliveries across 4 matches, retained separately \|

| Boundary \| No pressure-event definition, performance scoring or
  player rankings in this phase. \|

## 1. Executive summary

Phase 1 audited six supplied CSV datasets: ball-by-ball deliveries,
playing-XI/player registrations, matches, competition-team-player
mappings, teams and competitions. The audit examined dataset structure,
identifier relationships, player identity, team and competition
consistency, delivery-level fields, playing-XI structure, competition
coverage, match eligibility and the proposed primary delivery
population.

The approved primary population contains 813 matches: 362 T20 and 451
T20I. These matches are represented in 192,235 regulation deliveries
from innings 1 and 2. Four Super Over matches contribute 26 additional
deliveries, retained separately. The full target competition set
contains 853 matches: 371 T20 and 482 T20I.

Most match, team, competition and player-mapping relationships
reconciled. The audit also found field-semantic ambiguity and localized
source inconsistencies. The user approved retaining those issues as
documented limitations, without silent correction or inferred
replacement values.

## 2. Scope and dataset inventory

| Dataset \| Rows \| Columns \| Exact duplicate rows \|

| --- \| --- \| --- \| --- \|

| ball_by_ball \| 200,999 \| 33 \| 0 \|

| playing_eleven \| 28,381 \| 9 \| 0 \|

| matches \| 883 \| 22 \| 0 \|

| competition_team_player_mapping \| 6,413 \| 6 \| 0 \|

| teams \| 353 \| 3 \| 0 \|

| competitions \| 141 \| 4 \| 0 \|

| Total \| 236,970 \| 77 across files \| 0 in each file \|

Zero exact duplicate rows does not establish uniqueness at every
business key. The playing_eleven table contains repeated
match-team-player registrations with differing batting-order values.

## 3. Identifier integrity and player identity

-   matches contains 883 unique match IDs; ball_by_ball contains 867
    match IDs; playing_eleven contains 880.

-   All match IDs in ball_by_ball and playing_eleven exist in matches.
    Sixteen matches have no ball-by-ball records; all are labelled Match
    Abandoned.

-   Three matches have no playing_eleven records; all three are among
    the 16 abandoned matches without deliveries.

-   All home/away team IDs, match competition IDs, mapping competition
    IDs and match home/away team-competition pairs reconciled to their
    reference tables.

-   All actual delivery-role competition-team-player combinations were
    present in the mapping: striker 4,327/4,327; non-striker
    4,165/4,165; bowler 3,101/3,101.

Across identity observations, 1,217 player IDs and 1,210 names were
observed. No ID was associated with multiple names. Seven names were
associated with two IDs: Abdul Samad, Bashir Ahmad, Basil Hameed, Haider
Ali, Mohammad Ali, Muhammad Farooq and Rashid Khan. The user confirmed
Abdul Samad IDs 6922/7446 and Haider Ali IDs 7338/28756 are different
people from different countries. These are legitimate namesakes. Use
player_id as the identity key; names are not unique.

Other same-name registration conflicts were not automatically merged. In
particular, conflicting Basil Hameed and Muhammad Farooq registration
evidence was retained as a source-level inconsistency.

## 4. Team, competition and playing-XI consistency

-   Of 5,646 unique playing-XI match-team-player combinations, 5,645
    matched the competition-team-player mapping.

-   The sole unmatched combination is comp_id 2670, team_id 4444,
    player_id 29833 (Bashir Ahmad, Afghanistan A). It appears in five XI
    registrations marked is_played=False, with no delivery involvement;
    the mapping lists the corresponding Afghanistan A registration under
    another ID. Treat as unresolved registration inconsistency.

-   All delivery-role competition-team-player combinations were mapped.

-   playing_eleven is not a literal clean list of exactly 11 players per
    team-match. It includes non-playing squad registrations,
    impact-related records and repeated player registrations.

-   All 8,667 non-playing records have missing batting_order, captain
    and wicketkeeper flags, and no impact flags.

-   There are 35 repeated match-team-player groups comprising 75 rows,
    concentrated in matches 13613, 21176 and 28962. Repeated records
    have different batting-order values. The unique player sets
    reconcile exactly to the 11 delivery participants per team in the
    six affected match-team groups.

-   Use distinct player IDs for appearance counts and delivery-level
    batting_order for observed batting position. Preserve repeated
    source records.

-   558 match-team groups have one is_impact=1 and one is_impact_off=1.
    Pairing is verified; exact semantics/direction are not. Preserve
    original fields.

-   Twenty-three match-team groups have zero played records. They belong
    to 12 abandoned matches, all with zero ball-by-ball deliveries.

There were 512 played-XI registrations with no striker, non-striker or
bowler delivery involvement. For 511, the listed batting order was below
the maximum observed striker order in the team innings, consistent with
players who did not come to bat; this does not establish their exact
on-field role. One exception is Mosaddek Hossain (player_id 3281),
Bangladesh, match 51385: listed as is_played=True at batting order 6,
but absent from all delivery roles despite a substantial Bangladesh
second innings (121 deliveries, six wickets). The reason is unknown;
retain as an unresolved XI/delivery-feed inconsistency.

## 5. Competition and season coverage

| Coverage \| Competitions \| Matches \| With deliveries \| With XI \|

| --- \| --- \| --- \| --- \| --- \|

| IPL / T20 \| 5 \| 371 \| 367 \| 371 \|

| T20I \| 134 \| 482 \| 470 \| 479 \|

| Target total \| 139 \| 853 \| 837 \| 850 \|

The competitions reference contains 141 records: 139 target IPL/T20I
competitions and two out-of-scope T20 competitions with match data.
Three target T20I competition records have no match records. Coverage
spans IPL seasons 2022--2026 and T20I season labels 2022, 2022/23, 2023,
2023/24, 2024, 2024/25, 2025 and 2026. Missing delivery matches in the
target set are abandoned matches.

## 6. Match eligibility and exclusions

| Classification \| Count \| Treatment \|

| --- \| --- \| --- \|

| Standard result matches \| 809 \| Include \|

| Super Over matches \| 4 \| Include regulation innings; Super Over
  separately \|

| Abandoned, no deliveries \| 16 \| Exclude \|

| Abandoned, partial deliveries \| 3 \| Exclude from primary
  completed-match population \|

| No Result, one innings \| 19 \| Exclude \|

| No Result, two innings \| 2 \| Exclude; innings incomplete \|

| Total \| 853 \| 813 included; 40 excluded/incomplete \|

The three abandoned matches with partial data contain only one innings
each. The two No Result matches with two innings were inspected and
found incomplete. Four Super Over matches are identifiable by match
result and innings 3/4 records. Their regulation innings remain in the
primary population.

Thirty-four matches contain revised-innings metadata. The recorded
revised-overs values are divisible by six and are consistent with
candidate ball-limit values when divided by six, but the source
definition is not confirmed. Raw values are preserved; no conversion is
assumed.

## 7. Approved primary analysis population

| Metric \| Approved value \|

| --- \| --- \|

| Target matches \| 853 \|

| Primary eligible matches \| 813 \|

| Eligible T20 matches \| 362 \|

| Eligible T20I matches \| 451 \|

| Regulation deliveries (innings 1 and 2) \| 192,235 \|

| Super Over deliveries (innings 3 and 4) \| 26 \|

| Total deliveries in eligible matches, including Super Overs \| 192,261
  \|

| Distinct players in regulation delivery roles \| 892 \|

The default population for subsequent regulation-match analysis is the
813-match set and its 192,235 innings 1/2 deliveries. The 26 Super Over
deliveries are a separate subset and must not be silently mixed into
regulation analysis.

## 8. Ball-by-ball data quality

### 8.1 Extras and runs

-   extras1_runs is an encoded category, not a numerical extras-run
    total: 1=Overstep, 2=wide, 3=legbyes, 4=byes, 5=other, 6=no extras,
    7=Penalty.

-   extras_2_runs is non-zero in 35 primary regulation records.
    Thirty-four are associated with Overstep or other; one has no
    extras_type. Semantics remain unresolved.

-   The runs field could not be confidently labelled as batter runs or
    total delivery runs from the evidence. Do not assume its meaning
    without further validation.

### 8.2 Boundaries and wickets

-   In the primary regulation population, 20 rows have runs=4 with
    is_four=False and 3 rows have runs=6 with is_six=False. No row has
    both boundary flags true. Preserve run values and flags
    independently.

-   is_wicket aligns with dismissal_type presence in the audited data.
    One primary regulation wicket record lacks dismissed_player_id and
    is recorded as Retire Out; do not infer the player identity.

-   Eleven non-wicket records have dismissed_player_id populated.
    Dismissal ID 10 has spelling variants 'Obstracting the field' and
    'Obstructing the field'; no standardization was applied.

### 8.3 Sequence and overs

-   No duplicate (match_id, innings, innings_ball_num) or (match_id,
    innings, overid, over_ball_num) keys were found.

-   innings_ball_num is continuous within every match-innings group.
    over_ball_num is a delivery sequence position, not a legal-ball
    counter.

-   In the primary population, 6,450 overs have more than six delivery
    records; 147 of these have no recorded wide or Overstep.

-   Known wides/Oversteps explain many extended overs, but not all. The
    mixed 'other' extras category is not a reliable illegal-delivery
    indicator.

-   Do not derive legal-ball counts or economy-rate denominators from
    over_ball_num alone. No deliveries were removed or re-sequenced.

### 8.4 Bowling speed and timestamps

-   bowl_speed contains zero, negative, unusually low and high values;
    exclude it from primary modelling pending unit and source
    validation.

-   All delivery timestamps parsed, but 3,986 primary records have
    midnight timestamps and repeated timestamp values occur. Do not use
    timestamps as the sole event-ordering key.

## 9. Data-treatment register

| Area \| Evidence / issue \| Approved treatment \|

| --- \| --- \| --- \|

| Match population \| 813 eligible matches \| Use as primary population.
  \|

| Super Overs \| 4 matches; 26 deliveries \| Keep separate from
  regulation innings. \|

| Excluded matches \| 16 abandoned/no data; 3 abandoned/partial; 19 No
  Result/one innings; 2 No Result/two innings \| Exclude from primary
  completed-match population; preserve source rows. \|

| Player identity \| Names are not unique \| Use player_id as identity
  key. \|

| extras1_runs \| Encoded category; 6=no extras \| Do not treat as run
  quantity. \|

| extras_2_runs \| 35 non-zero primary records; semantics unresolved \|
  Preserve raw; do not infer meaning. \|

| runs \| Batter-run vs total-delivery-run semantics unresolved \| Do
  not assume semantics. \|

| Boundary flags \| 23 run/flag mismatches \| Preserve runs, is_four and
  is_six independently. \|

| Wicket fields \| One wicket lacks dismissed_player_id; 11 non-wickets
  have an ID \| Preserve source values and missingness. \|

| Dismissal labels \| ID 10 spelling variants \| Do not standardize
  without an agreed mapping. \|

| Bowling speed \| Zero, negative, low and high values \| Exclude from
  primary modelling pending validation. \|

| Timestamps \| Midnight placeholders and repeated values \| Do not use
  as sole ordering key. \|

| Over sequence \| 147 extended overs without recorded wide/Overstep \|
  Do not infer legal balls from sequence numbers. \|

| Playing XI \| Squad registrations and repeated records \| Use distinct
  player IDs; retain flags separately. \|

| Impact flags \| Paired flags, semantics unknown \| Preserve original
  fields; do not infer direction. \|

| Mosaddek Hossain \| Match 51385 XI/delivery mismatch \| Retain as
  unresolved inconsistency; do not invent participation. \|

| Mapping mismatch \| Bashir Ahmad ID 29833 vs mapping ID 39479 in comp
  2670; unplayed squad rows \| Retain as registration inconsistency; no
  ID merge. \|

## 10. Limitations and risks for later analysis

1.  Runs and extras_2_runs semantics remain unresolved. Metrics
    dependent on batter runs, total runs or extras need a defensible
    field interpretation.

2.  Legal-ball counts cannot be reliably inferred from the sequence
    fields alone. Bowling economy and balls-per-over denominators need
    validated legal-delivery classification.

3.  Boundary flags contain 23 mismatches. Boundary features must state
    whether they use runs or source flags and how mismatches are
    handled.

4.  Bowling speed is unsuitable for primary modelling until units,
    sentinel values and plausible ranges are confirmed.

5.  playing_eleven is not a clean 11-player roster. Squad rows, repeated
    registrations and participation inconsistencies must be handled
    explicitly.

6.  Impact-player flag direction and semantics are not established.

7.  The 512 played-XI records without delivery-role involvement must not
    automatically be counted as batting or bowling appearances.

8.  Super Over deliveries must remain separate unless a later
    methodology explicitly defines their use.

These limitations do not invalidate the approved match population. They
constrain which fields can be used directly and which derived metrics
require further validation or conservative treatment.

## 11. Approval and phase closure

The user explicitly approved the proposed Phase 1 population and the
approach of retaining documented unresolved issues rather than silently
correcting source data. The final Colab population checks passed: 813
eligible matches represented in regulation deliveries; 192,235
regulation deliveries; 26 Super Over deliveries kept separately; and no
source DataFrame modified by the consolidation checks.

Phase 1 is closed. Phase 2 may begin with pressure-event definitions and
baseline methodology. Pressure scoring, player ranking and top-10
selection are outside the scope of this report.

## Appendix --- Audit principles

-   Distinguish observed facts from hypotheses and unresolved semantics.

-   Do not silently rename, recode, correct or impute source fields.

-   Use player IDs, not names, as identity keys.

-   Treat exclusions as analysis-population rules, not deletion
    instructions.

-   Document source fields, assumptions, validation and exception
    handling for every future derived variable.

END OF PHASE 1 REPORT
