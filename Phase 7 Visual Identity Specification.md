# SupeRR Selector Season 2 — Phase 7 Visual Identity

## Purpose

This specification keeps the dashboard, methodology report, presentation, and later video visually consistent. It supports a cricket-analytics story without obscuring the evidence.

## Design direction

The identity combines a dark broadcast-style presentation layer with a light, print-friendly report layer. Rankings should feel prominent, while uncertainty and limitations remain equally visible.

The design must not imply certainty beyond the underlying analysis. Decorative elements must never compete with player names, ratings, evidence status, or methodology notes.

## Colour system

| Role | Colour | Use |
| --- | --- | --- |
| Midnight | `#07111F` | Primary dark background and strongest text |
| Slate | `#132238` | Secondary dark surfaces and section bands |
| Teal | `#20C7B6` | Reliable evidence, validated states, active controls |
| Gold | `#F5B942` | Official ranks, selected players, primary highlights |
| Coral | `#FF6B5E` | Uncertainty, warnings, limitations, provisional evidence |
| Off-white | `#F4F7FB` | Light report background and text on dark surfaces |
| Ink | `#172033` | Body text on light surfaces |
| Muted grey | `#6B7280` | Secondary labels and supporting explanations |

Colour must always be paired with text, a label, or a shape. It must not be the only way a status or comparison is communicated.

## Typography

- Primary family: Avenir Next.
- Fallback: Arial.
- Use no more than three text sizes on a normal page or slide.
- Presentation title: approximately 42–48 pt.
- Presentation slide title: approximately 30–34 pt.
- Presentation body: at least 17 pt.
- Report body: 9.5–10.5 pt.
- Use tabular numerals where available for ranks and ratings.

Player names, ranks, and evidence status must remain readable at normal viewing size. Do not reduce type size to fit excess content.

## Layout rules

### Report

- A4 portrait is the default.
- Use a light background with dark text.
- Keep wide evidence tables in appendices or split them into focused tables.
- Use consistent running headers, page numbers, figure numbers, and source notes.
- Keep each player profile in one visual block where practical.

### Presentation

- Use a 16:9 canvas.
- Use the dark visual system for title, ranking, and dashboard slides.
- Give each slide one main message.
- Use two to four visual elements per slide, with one dominant element.
- Never place explanatory paragraphs on ranking slides.

### Dashboard

- Use a dark header and light evidence surface.
- Keep filters visible above the leaderboard.
- Preserve rank, player name, rating, qualifying formats, and evidence status at all responsive widths.
- Move supporting evidence into a detail panel rather than crowding the leaderboard.
- Use clear focus states and keyboard-accessible controls.

## Chart language

- Use horizontal bars for ordered player comparisons.
- Use dumbbell or paired-bar charts for pressure-versus-ordinary comparisons.
- Use interval marks for bootstrap uncertainty.
- Use contribution bars for metric components.
- Do not use radar charts, 3D charts, or decorative gauges.
- Sort ranking charts by the unrounded validated score.
- Show the displayed rounded value without using it to determine order.

Reliable evidence uses teal. Official selected players and ranks use gold. Uncertainty uses coral. Neutral comparison evidence uses slate or muted grey.

## Imagery and iconography

- Prefer analytical charts, field geometry, scorecard cues, and restrained cricket textures.
- Avoid unlicensed player photographs.
- Use one consistent icon family if icons are needed.
- Icons must support labels rather than replace them.

## Content integrity

- “Structural pressure” must be named consistently.
- Do not describe the model as win probability, required-run-rate pressure, or complete scoreboard pressure.
- Do not describe bootstrap inclusion frequency as the probability that a player is objectively Top 10.
- Show qualifying formats whenever a player rating is presented.
- Mark Provisional and Insufficient evidence explicitly and never style them as Reliable.

## Artifact-specific export rules

- Report: tagged, searchable PDF with working links and legible printed contrast.
- Presentation: editable PPTX plus PDF preview.
- Dashboard: responsive published site plus source package.
- Video: visual treatment will be decided in Phase 7G; it must reuse this identity unless the later approved video plan explicitly changes it.

