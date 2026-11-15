---
name: SupeRR Selector — Report visual identity
description: Navy, pink and white report styling applied to the existing MarketSphere dashboard components.
colors:
  background: "#F5F6FA"
  surface: "#FFFFFF"
  surface-raised: "#FCECF5"
  border: "#E1E5ED"
  border-strong: "#CDD5E1"
  primary: "#B6006E"
  primary-strong: "#900057"
  brand-pink: "#EC008C"
  navy: "#08244B"
  series-blue: "#2166A5"
  on-primary: "#FFFFFF"
  tooltip: "#08244B"
  on-tooltip: "#F8FAFC"
  text: "#08244B"
  text-secondary: "#415570"
  text-muted: "#5D6A7D"
  success: "#2166A5"
  warning: "#8A4B00"
  danger: "#A91C45"
typography:
  heading:
    fontFamily: "Arial, Helvetica, sans-serif"
    fontWeight: 700
  body:
    fontFamily: "Arial, Helvetica, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.5
  mono:
    fontFamily: "Arial, Helvetica, sans-serif"
  ramp:
    micro: "11px"
    metadata: "12px"
    body: "14px"
    body-large: "16px"
    h3: "18px"
    h2: "22px"
    h2-mobile: "24px"
    h1: "28px"
    display: "32px"
rounded:
  hairline: "2px"
  focus: "3px"
  track: "4px"
  small: "4px"
  medium: "8px"
  large: "10px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "12px"
  base: "16px"
  lg: "20px"
  xl: "24px"
  2xl: "32px"
  3xl: "40px"
  4xl: "48px"
---

# Design system: Report visual identity

## Direction contract

**THESIS:** Cricket selection evidence should feel like a dependable professional tool, not a themed scorebook or an analyst-only worksheet.

**OWN-WORLD:** The methodology report and original problem statement supply the visual identity: navy text, white surfaces, pink highlights and clear sans-serif typography. Arial matches the editable report, with tabular numerals for data. The existing MarketSphere component structure remains the interaction foundation.

**STORY:** Set the eligible pool, scan the ranked shortlist, select a player, understand pressure performance and verify evidence strength.

**FIRST VIEWPORT:** A compact MarketSphere-style top bar and filter panel sit above a two-column workspace. The ranked player list is the left navigation rail; the selected-player dossier occupies the wider right canvas.

**FORM:** Responsive business-tool dashboard assembled from MarketSphere PageHeader, FilterBar, Button, StatusBadge, panel, list-row and disclosure patterns.

## Source of truth

Visual reference: `final_submission/SupeRR_Selector_Methodology_Report.docx`, inspired by the original hackathon problem statement. Component structure derives from the local MarketSphere design system. The report uses Arial as the portable alternative to the problem statement's Montserrat.

## Component rules

- Use the documented CSS variables; do not scatter raw colors through component styles.
- Panels use `--color-surface`, a subtle border, 8–10 px radius and a restrained navy-tinted shadow.
- Keep the canvas light. Gradients are limited to subtle page depth, the selected row and dossier header.
- Deep pink indicates active filters, links, keyboard focus and the selected player. The deeper shade preserves text contrast; bright brand pink remains the reference accent.
- Navy leaderboard headers mirror report table headers. High-pressure comparisons use pink and ordinary comparisons use navy. Positive component contributions and Reliable evidence use report blue; negative contributions retain a distinct berry tone and signed numbers.
- Status is always communicated with text as well as color.
- Buttons use primary, secondary and ghost hierarchy. Do not make every action dominant.
- Labels remain persistent. Inputs and menus have visible focus and at least 44 px touch targets on mobile.
- Use Arial with tabular numerals for ranks, ratings and numerical evidence.
- Explanations remain concise and progressive: primary evidence is visible; full methodology is disclosed on demand.

## Responsive rules

- Desktop: ranked player list left, player dossier right.
- Tablet: the shortlist remains above the dossier when a single-column layout is required.
- Mobile: filters stack, the team selector becomes a viewport-safe sheet, and evidence tiles become one column.
- No horizontal overflow at 390 px.

## Accessibility

- Maintain visible `:focus-visible` outlines using the deep pink primary.
- Preserve semantic headings, list structures, tabs and details/summary controls.
- Never rely on green, amber or red alone; keep the status labels.
- Respect reduced-motion preferences.
