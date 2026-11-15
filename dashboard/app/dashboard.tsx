/*
THESIS: Cricket selection evidence should feel like a dependable professional tool, not a themed scorebook or analyst worksheet.
OWN-WORLD: The methodology report's navy ink, white pages, pink accents and Arial hierarchy, applied to compact MarketSphere components.
STORY: Set the eligible pool, scan the shortlist, select a player, understand pressure performance and verify evidence strength.
FIRST VIEWPORT: A report-inspired top bar and filter panel above a shortlist-first workspace: players on the left, selected-player evidence on the right.
FORM: Responsive business-tool dashboard built from MarketSphere header, FilterBar, panel, list-row, badge and disclosure patterns.
*/

"use client";

import { useEffect, useMemo, useState } from "react";

type Mode = "IPL" | "T20I";
type Role = "Batter" | "Bowler";

type FormatEvidence = {
  format: Mode;
  eligibility: "Reliable" | "Provisional" | "Insufficient";
  rating: number | null;
  highRecords: number;
  ordinaryRecords: number;
  highMatches: number;
  allMatches: number;
  contributions: Record<string, number | null>;
  comparisons: {
    primaryLabel: string;
    primaryHigh: number | null;
    primaryOrdinary: number | null;
    secondaryLabel: string;
    secondaryHigh: number | null;
    secondaryOrdinary: number | null;
    highQualityResidual: number | null;
    pressureGradient: number | null;
  };
};

type UncertaintyEvidence = {
  rankedFrequency: number;
  ratingMedian: number | null;
  ratingLow: number | null;
  ratingHigh: number | null;
  rankMedian: number | null;
  rankLow: number | null;
  rankHigh: number | null;
  top10Frequency: number;
};

type DashboardPlayer = {
  playerId: number;
  playerName: string;
  role: Role;
  nationalTeam: string;
  nationalTeamSource: string;
  qualifyingFormats: Mode[];
  combinedRating: number;
  globalCombinedRank: number | null;
  officialTop10: boolean;
  formats: Partial<Record<Mode, FormatEvidence>>;
  uncertainty: Partial<Record<"fixed" | "nested", UncertaintyEvidence>>;
  robustnessClass: string | null;
  narrative: {
    selection: string;
    format: string;
    pressure: string;
    uncertainty: string;
  } | null;
};

type DashboardData = {
  metadata: {
    modelVersion: string;
    period: string;
    modes: Mode[];
    defaultModes: Mode[];
    nationalTeams: string[];
    defaultNationalTeams: string[];
    roles: Role[];
    defaultRole: Role;
    eligibilityRule: string;
    bothModesRule: string;
    singleModeRule: string;
    teamRule: string;
    rankingRule: string;
    pressureDefinition: string;
    officialRankingSignature: string;
  };
  players: DashboardPlayer[];
};

type RankedPlayer = DashboardPlayer & {
  filteredRank: number;
  displayScore: number;
};

type MetricCopy = {
  label: string;
  short: string;
  definition: string;
};

const MODE_OPTIONS: Mode[] = ["IPL", "T20I"];
const ROLE_OPTIONS: Role[] = ["Batter", "Bowler"];

const METRIC_COPY: Record<string, MetricCopy> = {
  scoringQuality: {
    label: "Scoring under pressure",
    short: "Scores faster than the match context expects.",
    definition:
      "Compares the batter's high-pressure scoring rate with the expected rate for the same format, innings, over and pressure context.",
  },
  survivalQuality: {
    label: "Staying in under pressure",
    short: "Avoids dismissal more often than context expects.",
    definition:
      "Measures whether the batter survives high-pressure records more often than the contextual benchmark predicts.",
  },
  scoringPressureGradient: {
    label: "Scoring pressure response",
    short: "Shows whether scoring rises or falls as pressure increases.",
    definition:
      "The continuous relationship between structural pressure and context-adjusted scoring. Positive means scoring improves as pressure rises.",
  },
  survivalPressureGradient: {
    label: "Survival pressure response",
    short: "Shows whether dismissal resistance changes as pressure rises.",
    definition:
      "The continuous relationship between structural pressure and context-adjusted survival. Positive means survival improves as pressure rises.",
  },
  wicketQuality: {
    label: "Wickets under pressure",
    short: "Takes more wickets than the match context expects.",
    definition:
      "Compares high-pressure bowler-credited wicket rate with the expected rate for the same format, innings, over and pressure context.",
  },
  runSuppressionQuality: {
    label: "Run control under pressure",
    short: "Concedes fewer batter runs than context expects.",
    definition:
      "Measures batter-run suppression on no-extras records under high pressure. It is not conventional economy rate.",
  },
  wicketPressureGradient: {
    label: "Wicket pressure response",
    short: "Shows whether wicket threat rises as pressure increases.",
    definition:
      "The continuous relationship between structural pressure and context-adjusted wicket taking. Positive means wicket threat improves as pressure rises.",
  },
  runSuppressionPressureGradient: {
    label: "Run-control pressure response",
    short: "Shows whether run control improves as pressure increases.",
    definition:
      "The continuous relationship between structural pressure and context-adjusted run suppression. Positive means run control improves as pressure rises.",
  },
};

const formatNumber = (value: number | null | undefined, digits = 1) =>
  value == null || Number.isNaN(value) ? "—" : value.toFixed(digits);

const formatPercent = (value: number | null | undefined) =>
  value == null || Number.isNaN(value) ? "—" : (value * 100).toFixed(0) + "%";

function teamSummary(selected: string[], allTeams: string[]) {
  if (selected.length === allTeams.length) return "All " + allTeams.length + " teams";
  if (selected.length === 0) return "No teams selected";
  if (selected.length <= 2) return selected.join(" + ");
  return selected.length + " teams selected";
}

function InfoTip({ label, children }: { label: string; children: string }) {
  return (
    <span className="info-tip" tabIndex={0} role="note" aria-label={label + ": " + children}>
      <span aria-hidden="true">i</span>
      <span className="tooltip-copy">{children}</span>
    </span>
  );
}

function reliabilityLabel(player: RankedPlayer) {
  const evidence = player.uncertainty.nested ?? player.uncertainty.fixed;
  if (!evidence) return { label: "Point estimate only", tone: "neutral" };
  if (evidence.top10Frequency >= 0.6) return { label: "Higher stability", tone: "positive" };
  if (evidence.top10Frequency >= 0.4) return { label: "Competitive", tone: "watch" };
  return { label: "Boundary result", tone: "caution" };
}

function getPrimaryEvidence(player: DashboardPlayer, modes: Mode[]) {
  const candidates = MODE_OPTIONS.map((mode) => player.formats[mode])
    .filter((item): item is FormatEvidence => Boolean(item))
    .filter((item) => modes.includes(item.format) && item.eligibility === "Reliable");
  return candidates.sort((a, b) => (b.rating ?? -Infinity) - (a.rating ?? -Infinity))[0] ?? null;
}

function pressureDelta(evidence: FormatEvidence, secondary = false) {
  const label = secondary ? evidence.comparisons.secondaryLabel : evidence.comparisons.primaryLabel;
  const high = secondary ? evidence.comparisons.secondaryHigh : evidence.comparisons.primaryHigh;
  const ordinary = secondary ? evidence.comparisons.secondaryOrdinary : evidence.comparisons.primaryOrdinary;
  if (high == null || ordinary == null) return "Comparison unavailable";

  const delta = high - ordinary;
  const lowerIsBetter = label.toLowerCase().includes("allowed");
  const improved = lowerIsBetter ? delta < 0 : delta > 0;
  const direction = Math.abs(delta) < 0.05 ? "unchanged" : improved ? "better" : "weaker";
  return Math.abs(delta).toFixed(1) + " " + direction + " under pressure";
}

function ComparisonRow({
  label,
  high,
  ordinary,
  definition,
  insight,
}: {
  label: string;
  high: number | null;
  ordinary: number | null;
  definition: string;
  insight: string;
}) {
  const scale = Math.max(Math.abs(high ?? 0), Math.abs(ordinary ?? 0), 1);
  const highWidth = Math.max(2, Math.min(100, (Math.abs(high ?? 0) / scale) * 100));
  const ordinaryWidth = Math.max(2, Math.min(100, (Math.abs(ordinary ?? 0) / scale) * 100));

  return (
    <div className="comparison-row">
      <div className="metric-title">
        <strong>{label}</strong>
        <InfoTip label={label}>{definition}</InfoTip>
      </div>
      <div className="comparison-values">
        <div className="situation-value high">
          <span>High pressure</span>
          <strong>{formatNumber(high)}</strong>
          <span className="comparison-track" aria-hidden="true">
            <span style={{ width: String(highWidth) + "%" }} />
          </span>
        </div>
        <div className="situation-value ordinary">
          <span>Ordinary</span>
          <strong>{formatNumber(ordinary)}</strong>
          <span className="comparison-track" aria-hidden="true">
            <span style={{ width: String(ordinaryWidth) + "%" }} />
          </span>
        </div>
      </div>
      <p className="insight-line">{insight}</p>
    </div>
  );
}

function ContributionBoard({ evidence }: { evidence: FormatEvidence }) {
  const entries = Object.entries(evidence.contributions)
    .filter((entry): entry is [string, number] => entry[1] != null)
    .map(([key, value]) => ({ key, value, points: value * 10, copy: METRIC_COPY[key] }))
    .filter((item) => item.copy);

  const max = Math.max(...entries.map((item) => Math.abs(item.points)), 1);

  if (!entries.length) {
    return (
      <div className="no-component-data">
        <strong>Component score unavailable</strong>
        <span>This format did not pass the Reliable evidence rule, so it does not contribute to the rating.</span>
      </div>
    );
  }

  return (
    <div className="contribution-board">
      {entries.map((item) => {
        const width = Math.max(3, Math.min(48, (Math.abs(item.points) / max) * 48));
        const positive = item.points >= 0;
        return (
          <div className="contribution-item" key={item.key}>
            <div className="contribution-copy">
              <div className="metric-title">
                <strong>{item.copy.label}</strong>
                <InfoTip label={item.copy.label}>{item.copy.definition}</InfoTip>
              </div>
              <span>{item.copy.short}</span>
            </div>
            <div className="contribution-visual">
              <div className="contribution-track" aria-hidden="true">
                <span className="axis" />
                <span
                  className={positive ? "contribution-fill positive" : "contribution-fill negative"}
                  style={{
                    left: positive ? "50%" : String(50 - width) + "%",
                    width: String(width) + "%",
                  }}
                />
              </div>
              <strong className={positive ? "points-positive" : "points-negative"}>
                {item.points > 0 ? "+" : ""}
                {item.points.toFixed(1)}
                <small> pts</small>
              </strong>
            </div>
          </div>
        );
      })}
      <p className="section-footnote">
        Each bar shows how many rating points this component adds to or subtracts from the neutral format baseline of 50.
      </p>
    </div>
  );
}

function EvidenceStrength({ player, evidence }: { player: RankedPlayer; evidence: FormatEvidence }) {
  const bootstrap = player.uncertainty.nested ?? player.uncertainty.fixed;
  const stability = reliabilityLabel(player);

  return (
    <div className="trust-board">
      <div className="trust-stat">
        <span className="trust-label">
          Pressure sample
          <InfoTip label="Pressure sample">
            Number of batting or bowling records classified as High structural pressure in this format.
          </InfoTip>
        </span>
        <strong>{evidence.highRecords.toLocaleString()}</strong>
        <span>records across {evidence.highMatches} matches</span>
      </div>
      <div className="trust-stat">
        <span className="trust-label">
          Match coverage
          <InfoTip label="Match coverage">Total matches contributing evidence for this player and format.</InfoTip>
        </span>
        <strong>{evidence.allMatches}</strong>
        <span>matches in the 2022–2026 window</span>
      </div>
      <div className="trust-stat">
        <span className="trust-label">
          Top-10 stability
          <InfoTip label="Top-10 stability">
            Share of match-level bootstrap resamples where the player finishes in the Top 10. It is ranking stability, not an objective probability.
          </InfoTip>
        </span>
        <strong>{bootstrap ? formatPercent(bootstrap.top10Frequency) : "—"}</strong>
        <span>{stability.label}</span>
      </div>
      <div className="trust-stat">
        <span className="trust-label">
          Rating range
          <InfoTip label="Rating range">
            Middle 95% of ratings from match-level resampling. A narrower range means the estimate moves less when matches change.
          </InfoTip>
        </span>
        <strong>
          {bootstrap ? formatNumber(bootstrap.ratingLow) + "–" + formatNumber(bootstrap.ratingHigh) : "—"}
        </strong>
        <span>95% bootstrap interval</span>
      </div>
    </div>
  );
}

function FormatStatus({ evidence }: { evidence: FormatEvidence }) {
  return (
    <span className={"evidence-status status-" + evidence.eligibility.toLowerCase()}>
      {evidence.eligibility}
    </span>
  );
}

function PlayerDossier({
  player,
  modes,
  evidenceFormat,
  setEvidenceFormat,
}: {
  player: RankedPlayer;
  modes: Mode[];
  evidenceFormat: Mode | null;
  setEvidenceFormat: (mode: Mode) => void;
}) {
  const availableFormats = MODE_OPTIONS.filter((mode) => player.formats[mode]);
  const preferredFormat =
    evidenceFormat && player.formats[evidenceFormat]
      ? evidenceFormat
      : availableFormats.find((mode) => modes.includes(mode) && player.formats[mode]?.eligibility === "Reliable") ??
        availableFormats[0];
  const evidence = preferredFormat ? player.formats[preferredFormat] : undefined;
  const stability = reliabilityLabel(player);
  const scoreBasis = modes.length === 2 ? "Combined pressure rating" : modes[0] + " pressure rating";

  if (!evidence) {
    return <div className="dossier-empty">No format evidence is available for this player.</div>;
  }

  return (
    <article className="player-dossier" aria-live="polite">
      <header className="dossier-header">
        <div className="rank-stamp">
          <span>Rank</span>
          <strong>{player.filteredRank}</strong>
        </div>
        <div className="player-heading">
          <p>{player.nationalTeam} · {player.role}</p>
          <h2>{player.playerName}</h2>
          <div className="player-tags">
            <span className={"stability-tag " + stability.tone}>{stability.label}</span>
            {player.officialTop10 && <span>Official Top 10</span>}
            <span>Score uses {player.qualifyingFormats.join(" + ")}</span>
          </div>
        </div>
        <div className="rating-stamp">
          <span>{scoreBasis}</span>
          <strong>{player.displayScore.toFixed(2)}</strong>
          <InfoTip label="Pressure rating">
            Reliable players are normalized within IPL and T20I separately. A format rating of 50 is the reliable-player baseline; every 10 points is one weighted standard deviation.
          </InfoTip>
        </div>
      </header>

      <div className="format-switcher" role="tablist" aria-label="Player evidence format">
        <span>Inspect evidence</span>
        {availableFormats.map((mode) => {
          const formatEvidence = player.formats[mode];
          return (
            <button
              type="button"
              role="tab"
              aria-selected={preferredFormat === mode}
              className={preferredFormat === mode ? "active" : ""}
              onClick={() => setEvidenceFormat(mode)}
              key={mode}
            >
              {mode}
              {formatEvidence && <FormatStatus evidence={formatEvidence} />}
            </button>
          );
        })}
      </div>

      <section className="dossier-section at-a-glance" aria-labelledby="glance-title">
        <div className="section-title-row">
          <div>
            <h3 id="glance-title">At a glance</h3>
            <p>What changed when this player faced high structural pressure?</p>
          </div>
          <span className="format-rating">
            {evidence.rating == null ? "Not scored" : evidence.rating.toFixed(2) + " " + evidence.format}
          </span>
        </div>
        <div className="comparison-board">
          <ComparisonRow
            label={evidence.comparisons.primaryLabel}
            high={evidence.comparisons.primaryHigh}
            ordinary={evidence.comparisons.primaryOrdinary}
            definition={
              player.role === "Batter"
                ? "Batter runs per 100 no-extras batting records. This is the dashboard's scoring-rate measure."
                : "Bowler-credited wickets per 100 delivery records. Run outs and other non-bowler dismissals are excluded."
            }
            insight={pressureDelta(evidence)}
          />
          <ComparisonRow
            label={evidence.comparisons.secondaryLabel}
            high={evidence.comparisons.secondaryHigh}
            ordinary={evidence.comparisons.secondaryOrdinary}
            definition={
              player.role === "Batter"
                ? "Percentage of eligible batting records where the striker was not dismissed."
                : "Batter runs allowed per 100 no-extras records. Lower is better; this is not conventional economy rate."
            }
            insight={pressureDelta(evidence, true)}
          />
        </div>
      </section>

      <section className="dossier-section why-rank" aria-labelledby="rank-title">
        <div className="section-title-row">
          <div>
            <h3 id="rank-title">Why this rank?</h3>
            <p>Four model signals translated into rating points.</p>
          </div>
          <InfoTip label="Context adjustment">
            Before players are compared, expected outcomes are estimated for the same format, innings, over and pressure context.
          </InfoTip>
        </div>
        <ContributionBoard evidence={evidence} />
      </section>

      <section className="dossier-section can-trust" aria-labelledby="trust-title">
        <div className="section-title-row">
          <div>
            <h3 id="trust-title">Can we trust it?</h3>
            <p>Sample size and ranking stability behind the point estimate.</p>
          </div>
          <FormatStatus evidence={evidence} />
        </div>
        <EvidenceStrength player={player} evidence={evidence} />
      </section>

      <details className="model-note">
        <summary>Read the full model note</summary>
        <div>
          {player.narrative ? (
            <ul>
              <li>{player.narrative.selection}</li>
              <li>{player.narrative.format}</li>
              <li>{player.narrative.pressure}</li>
              <li>{player.narrative.uncertainty}</li>
            </ul>
          ) : (
            <p>
              This player is outside the official submission Top 10. The dashboard still shows the validated score and
              uncertainty evidence without inventing a selection explanation.
            </p>
          )}
        </div>
      </details>
    </article>
  );
}

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [modes, setModes] = useState<Mode[]>(MODE_OPTIONS);
  const [role, setRole] = useState<Role>("Batter");
  const [selectedTeams, setSelectedTeams] = useState<string[]>([]);
  const [selectedPlayerId, setSelectedPlayerId] = useState<number | null>(null);
  const [evidenceFormat, setEvidenceFormat] = useState<Mode | null>(null);
  const [teamSearch, setTeamSearch] = useState("");
  const [urlReady, setUrlReady] = useState(false);

  useEffect(() => {
    let cancelled = false;
    fetch("/dashboard_data.json")
      .then((response) => {
        if (!response.ok) throw new Error("The ranking data request failed with status " + response.status);
        return response.json() as Promise<DashboardData>;
      })
      .then((payload) => {
        if (cancelled) return;
        const params = new URLSearchParams(window.location.search);
        const modeParam = params
          .get("modes")
          ?.split(",")
          .filter((value): value is Mode => MODE_OPTIONS.includes(value as Mode));
        const teamParam = params
          .get("teams")
          ?.split(",")
          .filter((team) => payload.metadata.nationalTeams.includes(team));
        const roleParam = params.get("role") as Role | null;
        const evidenceParam = params.get("evidence") as Mode | null;
        const playerParam = Number(params.get("player"));

        setData(payload);
        setModes(modeParam?.length ? Array.from(new Set(modeParam)) : payload.metadata.defaultModes);
        setSelectedTeams(teamParam ? Array.from(new Set(teamParam)) : payload.metadata.defaultNationalTeams);
        setRole(roleParam && ROLE_OPTIONS.includes(roleParam) ? roleParam : payload.metadata.defaultRole);
        setSelectedPlayerId(Number.isFinite(playerParam) && playerParam > 0 ? playerParam : null);
        setEvidenceFormat(evidenceParam && MODE_OPTIONS.includes(evidenceParam) ? evidenceParam : null);
        setUrlReady(true);
      })
      .catch((error: Error) => {
        if (!cancelled) setLoadError(error.message);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const rankedPlayers = useMemo<RankedPlayer[]>(() => {
    if (!data || modes.length === 0) return [];
    const selectedTeamSet = new Set(selectedTeams);
    const bothModes = modes.length === 2;
    const ranked = data.players
      .filter((player) => player.role === role && selectedTeamSet.has(player.nationalTeam))
      .map((player) => {
        if (bothModes) return { player, score: player.combinedRating };
        const evidence = player.formats[modes[0]];
        if (!evidence || evidence.eligibility !== "Reliable" || evidence.rating == null) return null;
        return { player, score: evidence.rating };
      })
      .filter((row): row is { player: DashboardPlayer; score: number } => row !== null)
      .sort((a, b) => b.score - a.score || a.player.playerId - b.player.playerId);

    return ranked.map(({ player, score }, index) => ({
      ...player,
      filteredRank: index + 1,
      displayScore: score,
    }));
  }, [data, modes, role, selectedTeams]);

  const topPlayers = rankedPlayers.slice(0, 10);
  const selectedPlayer = topPlayers.find((player) => player.playerId === selectedPlayerId) ?? topPlayers[0] ?? null;
  const effectiveSelectedPlayerId = selectedPlayer?.playerId ?? null;

  useEffect(() => {
    if (!urlReady || !data) return;
    const params = new URLSearchParams();
    params.set("modes", modes.join(","));
    params.set("role", role);
    params.set("teams", selectedTeams.join(","));
    if (effectiveSelectedPlayerId) params.set("player", String(effectiveSelectedPlayerId));
    if (evidenceFormat) params.set("evidence", evidenceFormat);
    window.history.replaceState(null, "", window.location.pathname + "?" + params.toString());
  }, [data, effectiveSelectedPlayerId, evidenceFormat, modes, role, selectedTeams, urlReady]);

  const toggleMode = (mode: Mode) => {
    setModes((current) => {
      if (current.includes(mode)) {
        if (current.length === 1) return current;
        return current.filter((value) => value !== mode);
      }
      return MODE_OPTIONS.filter((value) => current.includes(value) || value === mode);
    });
    setEvidenceFormat(null);
  };

  const selectRole = (option: Role) => {
    setRole(option);
    setSelectedPlayerId(null);
    setEvidenceFormat(null);
  };

  const toggleTeam = (team: string) => {
    setSelectedTeams((current) =>
      current.includes(team) ? current.filter((value) => value !== team) : [...current, team].sort(),
    );
    setSelectedPlayerId(null);
    setEvidenceFormat(null);
  };

  const choosePlayer = (playerId: number) => {
    setSelectedPlayerId(playerId);
    setEvidenceFormat(null);
  };

  const resetFilters = () => {
    if (!data) return;
    setModes(data.metadata.defaultModes);
    setSelectedTeams(data.metadata.defaultNationalTeams);
    setRole(data.metadata.defaultRole);
    setSelectedPlayerId(null);
    setEvidenceFormat(null);
    setTeamSearch("");
  };

  if (loadError) {
    return (
      <main className="state-page">
        <span className="state-mark">!</span>
        <h1>The pressure rankings could not be loaded.</h1>
        <p>{loadError}</p>
        <button type="button" onClick={() => window.location.reload()}>
          Try loading again
        </button>
      </main>
    );
  }

  if (!data) {
    return (
      <main className="state-page loading" aria-busy="true">
        <span className="loading-ball" aria-hidden="true" />
        <h1>Preparing the selection board…</h1>
        <p>Loading validated IPL and T20I pressure evidence.</p>
      </main>
    );
  }

  const visibleTeams = data.metadata.nationalTeams.filter((team) =>
    team.toLowerCase().includes(teamSearch.toLowerCase()),
  );
  const bothModes = modes.length === 2;
  const scoreBasis = bothModes ? "Combined IPL + T20I rating" : modes[0] + " rating";
  const officialState = bothModes && selectedTeams.length === data.metadata.nationalTeams.length;
  const leaderboardTitle =
    topPlayers.length === 10
      ? "Top 10 " + (role === "Batter" ? "batters" : "bowlers")
      : "Top " + topPlayers.length + " eligible " + (role === "Batter" ? "batters" : "bowlers");

  return (
    <main className="dashboard-shell">
      <header className="product-masthead">
        <div className="brand-lockup">
          <strong>SupeRR Selector</strong>
          <span>Pressure rankings</span>
        </div>
        <div className="masthead-explainer">
          <span>2022–2026 evidence</span>
          <p>Who performs above context when structural pressure rises?</p>
        </div>
      </header>

      <section className="filter-rail" aria-label="Ranking filters">
        <div className="filter-cluster">
          <span className="filter-label">Player type</span>
          <div className="segmented-control">
            {ROLE_OPTIONS.map((option) => (
              <button
                type="button"
                key={option}
                aria-pressed={role === option}
                className={role === option ? "active" : ""}
                onClick={() => selectRole(option)}
              >
                {option}
              </button>
            ))}
          </div>
        </div>

        <div className="filter-cluster">
          <span className="filter-label">
            Format
            <InfoTip label="Format selection">
              Choose IPL, T20I or both. With both selected, the validated combined rating is used; there is no separate Both mode.
            </InfoTip>
          </span>
          <div className="segmented-control">
            {MODE_OPTIONS.map((mode) => {
              const active = modes.includes(mode);
              const lastActive = active && modes.length === 1;
              return (
                <button
                  type="button"
                  key={mode}
                  aria-pressed={active}
                  aria-disabled={lastActive}
                  disabled={lastActive}
                  className={active ? "active" : ""}
                  onClick={() => toggleMode(mode)}
                >
                  {mode}
                </button>
              );
            })}
          </div>
        </div>

        <div className="filter-cluster team-cluster">
          <span className="filter-label">
            National teams
            <InfoTip label="National-team filter">
              Choose any combination. Teams change the eligible player pool but never alter a player&apos;s stored rating.
            </InfoTip>
          </span>
          <details className="team-picker">
            <summary>
              <span>{teamSummary(selectedTeams, data.metadata.nationalTeams)}</span>
              <span className="summary-chevron" aria-hidden="true" />
            </summary>
            <div className="team-menu">
              <label className="team-search">
                <span>Find a national team</span>
                <input
                  value={teamSearch}
                  onChange={(event) => setTeamSearch(event.target.value)}
                  placeholder="Search all teams"
                />
              </label>
              <div className="team-actions">
                <button type="button" onClick={() => setSelectedTeams(data.metadata.nationalTeams)}>
                  Select all
                </button>
                <button type="button" onClick={() => setSelectedTeams([])}>
                  Clear
                </button>
                <button
                  type="button"
                  className="team-done"
                  onClick={(event) => event.currentTarget.closest("details")?.removeAttribute("open")}
                >
                  Done
                </button>
              </div>
              <div className="team-options">
                {visibleTeams.map((team) => (
                  <label key={team}>
                    <input
                      type="checkbox"
                      checked={selectedTeams.includes(team)}
                      onChange={() => toggleTeam(team)}
                    />
                    <span>{team}</span>
                  </label>
                ))}
                {!visibleTeams.length && <p>No team matches “{teamSearch}”.</p>}
              </div>
            </div>
          </details>
        </div>

        <button type="button" className="reset-filters" onClick={resetFilters}>
          Reset
        </button>
      </section>

      <section className="selection-workspace">
        <aside className="ranking-rail" aria-labelledby="ranking-title">
          <header className="ranking-header">
            <div>
              <span>{officialState ? "Official submission order" : "Filtered shortlist"}</span>
              <h1 id="ranking-title">{leaderboardTitle}</h1>
              <p>{scoreBasis} · {teamSummary(selectedTeams, data.metadata.nationalTeams)}</p>
            </div>
            <div className="eligible-total">
              <strong>{rankedPlayers.length}</strong>
              <span>eligible</span>
            </div>
          </header>

          {topPlayers.length ? (
            <ol className="ranking-list">
              {topPlayers.map((player) => {
                const evidence = getPrimaryEvidence(player, modes);
                return (
                  <li key={player.playerId}>
                    <button
                      type="button"
                      className={selectedPlayer?.playerId === player.playerId ? "ranking-row selected" : "ranking-row"}
                      onClick={() => choosePlayer(player.playerId)}
                      aria-label={
                        "View " +
                        player.playerName +
                        ", rank " +
                        player.filteredRank +
                        ", rating " +
                        player.displayScore.toFixed(2)
                      }
                    >
                      <span className="rank-number">{String(player.filteredRank).padStart(2, "0")}</span>
                      <span className="rank-player">
                        <strong>{player.playerName}</strong>
                        <span>{player.nationalTeam}</span>
                        {evidence && (
                          <small>
                            Pressure {formatNumber(evidence.comparisons.primaryHigh)} · ordinary{" "}
                            {formatNumber(evidence.comparisons.primaryOrdinary)}
                          </small>
                        )}
                      </span>
                      <span className="rank-score">
                        <strong>{player.displayScore.toFixed(2)}</strong>
                        <small>{bothModes ? "combined" : modes[0]}</small>
                      </span>
                      <span className="row-chevron" aria-hidden="true" />
                    </button>
                  </li>
                );
              })}
            </ol>
          ) : (
            <div className="empty-ranking">
              <strong>No reliable players match this pool.</strong>
              <p>Choose at least one national team with Reliable {modes.join(" and ")} evidence.</p>
              <button type="button" onClick={() => setSelectedTeams(data.metadata.defaultNationalTeams)}>
                Select all teams
              </button>
            </div>
          )}

          {rankedPlayers.length > 0 && rankedPlayers.length < 10 && (
            <p className="shortlist-note">
              Only {rankedPlayers.length} players pass the Reliable evidence rule. Provisional players are not added to
              force a Top 10.
            </p>
          )}
        </aside>

        <section className="dossier-stage">
          {selectedPlayer ? (
            <PlayerDossier
              player={selectedPlayer}
              modes={modes}
              evidenceFormat={evidenceFormat}
              setEvidenceFormat={setEvidenceFormat}
            />
          ) : (
            <div className="dossier-empty">
              <strong>Select a player from the shortlist.</strong>
              <span>Their pressure evidence will appear here.</span>
            </div>
          )}
        </section>
      </section>

      <section className="reading-guide" aria-labelledby="reading-guide-title">
        <div>
          <span>New to the model?</span>
          <h2 id="reading-guide-title">Read the rating in four moves.</h2>
        </div>
        <ol>
          <li>
            <strong>1. Set the pool</strong>
            <span>Role, format and national teams decide who can be ranked.</span>
          </li>
          <li>
            <strong>2. Compare situations</strong>
            <span>See what the player did in High pressure versus ordinary records.</span>
          </li>
          <li>
            <strong>3. Explain the score</strong>
            <span>Context-adjusted quality and pressure response add or subtract rating points.</span>
          </li>
          <li>
            <strong>4. Check stability</strong>
            <span>Samples and match-level resampling show how much confidence to place in the rank.</span>
          </li>
        </ol>
      </section>

      <details className="methodology-disclosure">
        <summary>Methodology and important limitations</summary>
        <div className="methodology-grid">
          <p><strong>Pressure:</strong> {data.metadata.pressureDefinition}.</p>
          <p><strong>Formats:</strong> {data.metadata.bothModesRule}. {data.metadata.singleModeRule}.</p>
          <p><strong>Eligibility:</strong> Only Reliable format evidence can enter a single-format ranking.</p>
          <p><strong>Limitation:</strong> Structural pressure does not include target, required run rate, score parity, win probability or exact legal balls remaining.</p>
        </div>
      </details>

      <footer className="product-footer">
        <span>SupeRR Selector Season 2 · {data.metadata.period}</span>
        <span>Model {data.metadata.modelVersion}</span>
      </footer>
    </main>
  );
}
