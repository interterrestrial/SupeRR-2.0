from __future__ import annotations

import math
import os
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL, WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "final_submission"
CHART_DIR = ROOT / "tmp" / "phase7d" / "charts"
OUTPUT = OUT_DIR / "SupeRR_Selector_Methodology_Report.docx"

MIDNIGHT = "08244B"
SLATE = "153B69"
TEAL = "2166A5"
GOLD = "EC008C"
CORAL = "BB0070"
OFF_WHITE = "F4F7FB"
INK = "08244B"
MUTED = "6B7280"
PALE_BLUE = "EAF2F8"
PALE_TEAL = "E7F8F5"
PALE_GOLD = "FFF7DF"
PALE_CORAL = "FFF0EE"
BORDER = "D9D9D9"
WHITE = "FFFFFF"
BLACK = "08244B"

FONT = "Arial"
FONT_FALLBACK = "Arial"


def set_cell_shading(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_border(cell, color: str = BORDER, size: str = "6") -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = f"w:{edge}"
        element = borders.find(qn(tag))
        if element is None:
            element = OxmlElement(tag)
            borders.append(element)
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), size)
        element.set(qn("w:color"), color)


def set_cell_margins(cell, top=90, start=110, bottom=90, end=110) -> None:
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}"))
        if node is None:
            node = OxmlElement(f"w:{margin}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_repeat_table_header(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    header = OxmlElement("w:tblHeader")
    header.set(qn("w:val"), "true")
    tr_pr.append(header)


def prevent_row_split(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    cant_split = OxmlElement("w:cantSplit")
    tr_pr.append(cant_split)


def set_run_font(run, name=FONT) -> None:
    run.font.name = name
    r_pr = run._element.get_or_add_rPr()
    r_fonts = r_pr.rFonts
    if r_fonts is None:
        r_fonts = OxmlElement("w:rFonts")
        r_pr.insert(0, r_fonts)
    r_fonts.set(qn("w:ascii"), name)
    r_fonts.set(qn("w:hAnsi"), name)
    r_fonts.set(qn("w:eastAsia"), name)
    r_fonts.set(qn("w:cs"), name)
    for attr in ("asciiTheme", "hAnsiTheme", "eastAsiaTheme", "cstheme"):
        r_fonts.attrib.pop(qn("w:" + attr), None)


def set_picture_alt(inline_shape, title: str, description: str) -> None:
    doc_pr = inline_shape._inline.docPr
    doc_pr.set("title", title)
    doc_pr.set("descr", description)


def add_field(paragraph, field_code: str) -> None:
    run = paragraph.add_run()
    set_run_font(run)
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = field_code
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = "1"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, instr, separate, text, end])


def set_update_fields(doc: Document) -> None:
    settings = doc.settings._element
    node = settings.find(qn("w:updateFields"))
    if node is None:
        node = OxmlElement("w:updateFields")
        settings.append(node)
    node.set(qn("w:val"), "true")


def text_color(run, hex_color: str) -> None:
    run.font.color.rgb = RGBColor.from_string(hex_color)


def add_text(paragraph, text: str, *, bold=False, italic=False, color=INK, size=None) -> object:
    run = paragraph.add_run(text)
    set_run_font(run)
    run.bold = bold
    run.italic = italic
    text_color(run, color)
    if size is not None:
        run.font.size = Pt(size)
    return run


def set_paragraph_spacing(paragraph, before=0, after=6, line=1.12) -> None:
    fmt = paragraph.paragraph_format
    fmt.space_before = Pt(before)
    fmt.space_after = Pt(after)
    fmt.line_spacing = line


def add_body(doc: Document, text: str, *, bold_lead: str | None = None, after=6) -> object:
    p = doc.add_paragraph()
    p.style = doc.styles["Body Text"]
    if bold_lead and text.startswith(bold_lead):
        add_text(p, bold_lead, bold=True, color=BLACK)
        add_text(p, text[len(bold_lead):], color=INK)
    else:
        add_text(p, text, color=INK)
    set_paragraph_spacing(p, after=after)
    return p


def add_bullet(doc: Document, text: str, *, level=0, bold_lead: str | None = None) -> object:
    p = doc.add_paragraph(style="List Bullet" if level == 0 else "List Bullet 2")
    if bold_lead and text.startswith(bold_lead):
        add_text(p, bold_lead, bold=True, color=BLACK)
        add_text(p, text[len(bold_lead):], color=INK)
    else:
        add_text(p, text, color=INK)
    set_paragraph_spacing(p, after=3)
    return p


def reset_numbering(doc: Document) -> None:
    doc._phase7d_number_counter = 0


def add_numbered(doc: Document, text: str, *, bold_lead: str | None = None) -> object:
    doc._phase7d_number_counter = getattr(doc, "_phase7d_number_counter", 0) + 1
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.28)
    p.paragraph_format.first_line_indent = Inches(-0.28)
    add_text(p, f"{doc._phase7d_number_counter}.  ", bold=True, color=BLACK)
    if bold_lead and text.startswith(bold_lead):
        add_text(p, bold_lead, bold=True, color=BLACK)
        add_text(p, text[len(bold_lead):], color=INK)
    else:
        add_text(p, text, color=INK)
    set_paragraph_spacing(p, after=4)
    return p


def add_heading(doc: Document, text: str, level=1) -> object:
    p = doc.add_heading(text, level=level)
    p.paragraph_format.keep_with_next = True
    return p


def add_kicker(doc: Document, text: str, color=GOLD) -> object:
    p = doc.add_paragraph()
    run = add_text(p, text.upper(), bold=True, color=color, size=8.5)
    run.font.letter_spacing = Pt(0.5) if hasattr(run.font, "letter_spacing") else None
    set_paragraph_spacing(p, after=4)
    return p


def add_caption(doc: Document, number: int, title: str, source: str) -> None:
    p = doc.add_paragraph()
    p.style = doc.styles["Caption"]
    add_text(p, f"Figure {number}  {title}", bold=True, color=BLACK, size=8.5)
    add_text(p, f"\nSource: {source}", color=MUTED, size=7.5)
    p.paragraph_format.keep_with_next = False
    set_paragraph_spacing(p, before=2, after=8, line=1.0)


def add_figure(doc: Document, path: Path, width: float, number: int, title: str, source: str, alt: str) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    shape = p.add_run().add_picture(str(path), width=Inches(width))
    set_picture_alt(shape, title, alt)
    set_paragraph_spacing(p, before=2, after=2)
    add_caption(doc, number, title, source)


def add_source_note(doc: Document, text: str) -> None:
    p = doc.add_paragraph()
    add_text(p, text, italic=True, color=MUTED, size=7.5)
    set_paragraph_spacing(p, before=2, after=8, line=1.0)


def add_table(
    doc: Document,
    headers: list[str],
    rows: list[list[object]],
    widths: list[float] | None = None,
    aligns: list[str] | None = None,
    font_size: float = 8.5,
    header_fill: str = MIDNIGHT,
) -> object:
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.style = "Table Grid"
    if widths:
        for column, width in zip(table.columns, widths):
            column.width = Inches(width)
    header = table.rows[0]
    set_repeat_table_header(header)
    for idx, value in enumerate(headers):
        cell = header.cells[idx]
        set_cell_shading(cell, header_fill)
        set_cell_border(cell)
        set_cell_margins(cell, top=100, bottom=100)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        if widths:
            cell.width = Inches(widths[idx])
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if not aligns or aligns[idx] == "center" else WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(0)
        add_text(p, str(value), bold=True, color=WHITE, size=font_size)
    for r_idx, row_values in enumerate(rows):
        row = table.add_row()
        prevent_row_split(row)
        fill = WHITE if r_idx % 2 == 0 else OFF_WHITE
        for c_idx, value in enumerate(row_values):
            cell = row.cells[c_idx]
            set_cell_shading(cell, fill)
            set_cell_border(cell)
            set_cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if widths:
                cell.width = Inches(widths[c_idx])
            p = cell.paragraphs[0]
            alignment = aligns[c_idx] if aligns else "left"
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if alignment == "center" else WD_ALIGN_PARAGRAPH.RIGHT if alignment == "right" else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(0)
            add_text(p, "" if value is None else str(value), color=INK, size=font_size)
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(2)
    return table


def add_metric_strip(doc: Document, metrics: list[tuple[str, str]]) -> None:
    table = doc.add_table(rows=1, cols=len(metrics))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    for idx, (value, label) in enumerate(metrics):
        cell = table.cell(0, idx)
        set_cell_shading(cell, PALE_BLUE if idx % 2 == 0 else OFF_WHITE)
        set_cell_border(cell, color=BORDER)
        set_cell_margins(cell, top=130, bottom=130)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_text(p, value, bold=True, color=BLACK, size=15)
        add_text(p, f"\n{label}", color=MUTED, size=7.5)
        p.paragraph_format.space_after = Pt(0)
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(4)


def add_section_break(doc: Document, title: str, kicker: str | None = None) -> None:
    if kicker:
        p = add_kicker(doc, kicker)
        p.paragraph_format.page_break_before = True
        add_heading(doc, title, 1)
    else:
        p = add_heading(doc, title, 1)
        p.paragraph_format.page_break_before = True


def human_metric(metric: str) -> str:
    return (
        metric.replace("IPL ", "IPL ")
        .replace("T20I ", "T20I ")
        .replace("scoring quality", "scoring quality")
        .replace("survival quality", "survival quality")
        .replace("wicket quality", "wicket quality")
        .replace("run suppression quality", "run suppression quality")
        .replace("pressure gradient", "pressure response")
    )


def status_for_other_format(row: pd.Series) -> str:
    if row.qualifying_formats == "IPL+T20I":
        return "Both formats Reliable"
    other = "T20I" if row.qualifying_formats == "IPL" else "IPL"
    status = row[f"evidence_status_{other.lower()}"]
    return f"{other} {status}"


def rr_fit_text(row: pd.Series) -> str:
    fits = {
        "Nicholas Pooran": "Adds IPL scoring impact with a +42.1 contextual pressure-scoring residual per 100 records and stronger survival. His negative scoring gradient means the case rests on quality in High pressure rather than continuous improvement as pressure rises.",
        "Jimmy Neesham": "Offers T20I scoring and survival evidence, including +29.5 pressure runs per 100 records above context. Insufficient IPL evidence makes competition transfer an additional scouting question.",
        "Hardik Pandya": "Adds a scoring option supported in both competitions. The T20I pressure-scoring residual of +65.1 per 100 is stronger than the IPL +19.6, making the cross-format difference relevant to an IPL role assessment.",
        "Jos Buttler": "Adds an IPL-supported scoring and survival option: 183.3 pressure runs per 100 records versus 148.4 ordinarily, with positive contextual survival. T20I evidence is Provisional.",
        "Jaker Ali Anik": "Adds a T20I scouting candidate with pressure scoring +29.2 runs per 100 records above context. No observed IPL evidence means that suitability for an IPL role requires additional assessment.",
        "Romario Shepherd": "Adds T20I pressure survival with positive contextual scoring. Raw pressure scoring is lower than ordinary scoring, so the selection case depends on context adjustment and survival rather than a raw scoring uplift.",
        "Suryakumar Yadav": "Adds scoring evidence in both formats. Pressure-scoring residuals of +47.7 in IPL and +47.4 in T20I per 100 records support a scoring contribution despite lower raw T20I scoring under pressure.",
        "Iftikhar Ahmed": "Offers a T20I scoring candidate: 146.8 runs per 100 pressure records versus 124.3 ordinarily. IPL transferability needs separate assessment.",
        "Shreyas Iyer": "Adds IPL pressure scoring at +46.0 runs per 100 records above context. A slightly negative pressure-survival residual means this is primarily a scoring contribution.",
        "Rinku Singh": "Adds a batting option with Reliable evidence and positive pressure-scoring and survival residuals in both formats. Low bootstrap inclusion makes further boundary review useful.",
        "Sufiyan Muqeem": "Offers T20I wicket threat: 12.1 wickets per 100 pressure records versus 3.8 ordinarily, plus positive contextual run control. IPL transferability requires further scouting.",
        "Kuldeep Yadav": "Adds two-format wicket threat and the highest nested inclusion among selected bowlers. Pressure wickets exceed context by 2.9 per 100 in IPL and 12.0 in T20I.",
        "Sunil Narine": "Adds IPL run control and wicket threat. Pressure batter runs allowed fall to 83.5 per 100 clean records from 121.8 ordinarily; run suppression is the strongest weighted signal.",
        "Mohammad Nawaz": "Offers a T20I combination of wickets and control, with pressure residuals of +2.6 wickets and +18.5 run suppression per 100 records. IPL suitability needs further assessment.",
        "Abrar Ahmed": "Offers a T20I control candidate with 80.4 batter runs allowed per 100 clean pressure records and +28.0 contextual run suppression. Control contributes more to the rating than wicket quality.",
        "Mitchell Starc": "Adds IPL wicket-taking impact: 11.1 wickets per 100 pressure records versus 5.3 ordinarily. Negative contextual run suppression identifies a run-cost trade-off.",
        "Eshan Malinga": "Adds IPL wicket threat and positive contextual run control. Nested inclusion of 17.9 percent makes additional match evidence valuable before an auction commitment.",
        "Varun Chakravarthy": "Adds two-format wicket threat and positive pressure run suppression in IPL and T20I. The evidence spans both formats but Top-10 inclusion remains sensitive to the sampled matches.",
        "Suyash Sharma": "Offers IPL wicket threat and control: the wicket rate increases from 2.5 ordinarily to 7.1 per 100 pressure records. Further role-specific scouting can test how that contribution fits the squad.",
        "Mohit Sharma": "Adds IPL wicket evidence at 9.1 wickets per 100 pressure records versus 4.5 ordinarily. A very small gap to rank 9 and retention in 6 of 13 scenarios make the exact rank sensitive.",
    }
    if row.player_name in fits:
        return fits[row.player_name]
    both = row.qualifying_formats == "IPL+T20I"
    metric = row.strongest_metric.lower()
    if row.role == "Batter":
        if "survival" in metric:
            main = "Adds an innings-stabilising option when wicket strain and stage urgency are elevated."
        elif "gradient" in metric:
            main = "Adds a batter whose context-adjusted output strengthens as structural pressure rises."
        else:
            main = "Adds a pressure-scoring option whose output exceeds the contextual expectation in the strongest qualifying format."
    else:
        if "run suppression" in metric:
            main = "Adds control under structural pressure by suppressing batter runs relative to the contextual expectation."
        elif "gradient" in metric:
            main = "Adds a bowler whose context-adjusted impact strengthens as structural pressure rises."
        else:
            main = "Adds wicket-taking threat in overs already carrying elevated wicket strain or stage urgency."
    breadth = " Evidence is Reliable in both IPL and T20I." if both else f" The official score is supported by Reliable {row.qualifying_formats} evidence only."
    return main + breadth


def monitoring_text(row: pd.Series) -> str:
    freq = float(row.top10_frequency_nested)
    if freq >= 0.60:
        stability = "Stronger resampling stability, but still below the predefined 75% core threshold."
    elif freq >= 0.40:
        stability = "Moderate resampling stability; use the rank as a shortlist signal rather than an automatic auction decision."
    else:
        stability = "High boundary sensitivity; role, availability and price should receive additional review."
    if row.qualifying_formats != "IPL+T20I":
        stability += " The absent or unreliable format contributes no balancing evidence and is not scored as zero."
    return stability


def fmt(value, digits=1) -> str:
    if pd.isna(value):
        return "-"
    return f"{float(value):.{digits}f}"


def pressure_lines(row: pd.Series, pressure: pd.DataFrame) -> list[str]:
    rows = pressure[
        pressure.role.eq(row.role)
        & pressure.player_id.eq(row.player_id)
        & pressure.format_group.isin(str(row.qualifying_formats).split("+"))
    ]
    output = []
    for format_name in str(row.qualifying_formats).split("+"):
        part = rows[rows.format_group.eq(format_name)].set_index("pressure_band")
        if not {"High", "Ordinary"}.issubset(part.index):
            continue
        high = part.loc["High"]
        ordinary = part.loc["Ordinary"]
        if row.role == "Batter":
            high_secondary = 100 - high.secondary_raw_rate_per100
            ordinary_secondary = 100 - ordinary.secondary_raw_rate_per100
            output.append(
                f"{format_name}: {high.primary_raw_rate_per100:.1f} vs {ordinary.primary_raw_rate_per100:.1f} runs per 100 records; "
                f"{high_secondary:.1f}% vs {ordinary_secondary:.1f}% survival."
            )
        else:
            output.append(
                f"{format_name}: {high.primary_raw_rate_per100:.1f} vs {ordinary.primary_raw_rate_per100:.1f} wickets per 100 records; "
                f"{high.secondary_raw_rate_per100:.1f} vs {ordinary.secondary_raw_rate_per100:.1f} batter runs allowed per 100 no-extras records."
            )
    return output


ARIAL = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
ARIAL_BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")


def setup_plot() -> None:
    return None


def rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def chart_font(size: int, bold: bool = False):
    path = ARIAL_BOLD if bold else ARIAL
    return ImageFont.truetype(str(path), size=max(size, 27))


def chart_canvas(width: int, height: int, title: str):
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.text((46, 28), title, fill=rgb(INK), font=chart_font(34, True))
    return image, draw


def save_image(image: Image.Image, name: str) -> Path:
    path = CHART_DIR / name
    image.save(path, format="PNG", optimize=True)
    return path


def text_center(draw, xy, text, font, fill):
    draw.text(xy, text, font=font, fill=fill, anchor="mm")


def chart_data_scope() -> Path:
    labels = ["Match registry", "Target IPL and T20I", "Eligible completed", "Pressure model"]
    values = [883, 853, 813, 789]
    colors = [SLATE, SLATE, TEAL, GOLD]
    image, draw = chart_canvas(1700, 610, "Match population through the analytical pipeline")
    label_x, bar_x, bar_w = 50, 430, 1080
    top, row_h = 120, 105
    for i, (label, value, color) in enumerate(zip(labels, values, colors)):
        y = top + i * row_h
        draw.text((label_x, y + 25), label, fill=rgb(INK), font=chart_font(24), anchor="lm")
        width = int(bar_w * value / 930)
        draw.rounded_rectangle((bar_x, y, bar_x + width, y + 52), radius=8, fill=rgb(color))
        draw.text((bar_x + width + 18, y + 26), f"{value:,}", fill=rgb(INK), font=chart_font(25, True), anchor="lm")
    return save_image(image, "data_scope.png")


def chart_pressure_distribution() -> Path:
    labels = ["IPL innings 1", "IPL innings 2", "T20I innings 1", "T20I innings 2"]
    low = [39.82, 39.99, 40.12, 39.87]
    medium = [39.98, 40.01, 39.93, 40.40]
    high = [100 - a - b for a, b in zip(low, medium)]
    image, draw = chart_canvas(1700, 660, "High pressure is the top within-format-and-innings 20 percent")
    bar_x, bar_w, top, row_h = 360, 1240, 130, 96
    for i, label in enumerate(labels):
        y = top + i * row_h
        draw.text((45, y + 27), label, fill=rgb(INK), font=chart_font(23), anchor="lm")
        parts = [(low[i], "DDE3EA", rgb(INK)), (medium[i], SLATE, rgb(WHITE)), (high[i], CORAL, rgb(WHITE))]
        x = bar_x
        for value, color, label_color in parts:
            width = int(bar_w * value / 100)
            draw.rectangle((x, y, x + width, y + 54), fill=rgb(color))
            text_center(draw, (x + width / 2, y + 27), f"{value:.1f}%", chart_font(19, True), label_color)
            x += width
    legend_y = 555
    for x, label, color in [(520, "Low", "DDE3EA"), (770, "Medium", SLATE), (1080, "High", CORAL)]:
        draw.rectangle((x, legend_y, x + 34, legend_y + 22), fill=rgb(color))
        draw.text((x + 46, legend_y + 11), label, fill=rgb(INK), font=chart_font(20), anchor="lm")
    return save_image(image, "pressure_distribution.png")


def chart_weights() -> Path:
    labels = ["Batting", "Bowling"]
    data = [
        ("Primary outcome quality", [45, 45], TEAL),
        ("Secondary outcome quality", [25, 30], SLATE),
        ("Primary pressure response", [20, 15], GOLD),
        ("Secondary pressure response", [10, 10], CORAL),
    ]
    image, draw = chart_canvas(1700, 690, "Outcome quality receives most of the rating weight")
    bar_x, bar_w = 270, 1340
    for row_idx, row_label in enumerate(labels):
        y = 150 + row_idx * 135
        draw.text((45, y + 31), row_label, fill=rgb(INK), font=chart_font(25, True), anchor="lm")
        x = bar_x
        for _, values, color in data:
            value = values[row_idx]
            width = int(bar_w * value / 100)
            draw.rectangle((x, y, x + width, y + 62), fill=rgb(color))
            text_center(draw, (x + width / 2, y + 31), f"{value}%", chart_font(19, True), rgb(INK) if color == GOLD else rgb(WHITE))
            x += width
    legend_positions = [(70, 500), (850, 500), (70, 565), (850, 565)]
    for (label, _, color), (x, y) in zip(data, legend_positions):
        draw.rectangle((x, y, x + 34, y + 22), fill=rgb(color))
        draw.text((x + 46, y + 11), label, fill=rgb(INK), font=chart_font(19), anchor="lm")
    return save_image(image, "metric_weights.png")


def chart_eligibility(eligibility: pd.DataFrame) -> Path:
    groups = ["Batter IPL", "Batter T20I", "Bowler IPL", "Bowler T20I"]
    index = {(r.role + " " + r.format_group, r.eligibility): int(r.player_format_records) for r in eligibility.itertuples()}
    categories = [("Reliable", TEAL), ("Provisional", GOLD), ("Insufficient", "CBD5E1")]
    totals = [sum(index[(g, c)] for c, _ in categories) for g in groups]
    max_total = max(totals)
    image, draw = chart_canvas(1700, 700, "Eligibility filters sparse evidence before ranking")
    bar_x, bar_w, top, row_h = 330, 1250, 130, 100
    for i, group in enumerate(groups):
        y, x = top + i * row_h, bar_x
        draw.text((45, y + 28), group, fill=rgb(INK), font=chart_font(23), anchor="lm")
        for category, color in categories:
            value = index[(group, category)]
            width = int(bar_w * value / max_total)
            draw.rectangle((x, y, x + width, y + 56), fill=rgb(color))
            if width > 70:
                text_center(draw, (x + width / 2, y + 28), str(value), chart_font(18, True), rgb(WHITE) if category == "Reliable" else rgb(INK))
            x += width
        draw.text((x + 14, y + 28), str(totals[i]), fill=rgb(MUTED), font=chart_font(18), anchor="lm")
    for x, (label, color) in zip((480, 780, 1110), categories):
        draw.rectangle((x, 575, x + 34, 597), fill=rgb(color))
        draw.text((x + 46, 586), label, fill=rgb(INK), font=chart_font(20), anchor="lm")
    return save_image(image, "eligibility.png")


def chart_rankings(players: pd.DataFrame, role: str) -> Path:
    frame = players[players.role.eq(role)].sort_values("rank")
    image, draw = chart_canvas(1700, 1040, f"Official Top 10 {role.lower()} ratings")
    top, row_h = 115, 82
    label_x, bar_x, bar_w = 45, 510, 850
    min_rating, max_rating = 50, float(frame.combined_rating.max()) + 4
    for i, row in enumerate(frame.itertuples()):
        y = top + i * row_h
        draw.text((label_x, y + 25), f"{int(row.rank):02d}", fill=rgb(MUTED), font=chart_font(20, True), anchor="lm")
        draw.text((105, y + 25), row.player_name, fill=rgb(INK), font=chart_font(22), anchor="lm")
        width = int(bar_w * (row.combined_rating - min_rating) / (max_rating - min_rating))
        color = GOLD if row.rank <= 3 else TEAL
        draw.rounded_rectangle((bar_x, y, bar_x + width, y + 50), radius=7, fill=rgb(color))
        draw.text((bar_x + width + 16, y + 25), f"{row.combined_rating:.2f}  {row.qualifying_formats}", fill=rgb(INK), font=chart_font(20, True), anchor="lm")
    draw.text((bar_x, 960), "Rating above the Reliable-format baseline of 50", fill=rgb(MUTED), font=chart_font(19))
    return save_image(image, f"{role.lower()}_rankings.png")


def primary_format_for_chart(row: pd.Series) -> str:
    if row.qualifying_formats != "IPL+T20I":
        return row.qualifying_formats
    return "IPL" if row.ipl_rating >= row.t20i_rating else "T20I"


def chart_pressure_comparison(players: pd.DataFrame, pressure: pd.DataFrame, role: str) -> Path:
    selected = players[players.role.eq(role)].sort_values("rank").copy()
    records = []
    for row in selected.itertuples(index=False):
        series = pd.Series(row._asdict())
        format_name = primary_format_for_chart(series)
        part = pressure[
            pressure.role.eq(role)
            & pressure.player_id.eq(row.player_id)
            & pressure.format_group.eq(format_name)
        ].set_index("pressure_band")
        records.append(
            {
                "player": row.player_name,
                "rank": row.rank,
                "format": format_name,
                "high": part.loc["High", "primary_raw_rate_per100"],
                "ordinary": part.loc["Ordinary", "primary_raw_rate_per100"],
            }
        )
    frame = pd.DataFrame(records).sort_values("rank")
    image, draw = chart_canvas(1700, 1040, f"High-pressure and ordinary raw outcomes for selected {role.lower()}s")
    minimum = min(frame.high.min(), frame.ordinary.min())
    maximum = max(frame.high.max(), frame.ordinary.max())
    span = maximum - minimum or 1
    label_x, plot_x, plot_w, top, row_h = 45, 585, 960, 125, 78
    for i, row in enumerate(frame.itertuples()):
        y = top + i * row_h
        draw.text((label_x, y), f"{row.player}  ({row.format})", fill=rgb(INK), font=chart_font(20), anchor="lm")
        ordinary_x = plot_x + int(plot_w * (row.ordinary - minimum) / span)
        high_x = plot_x + int(plot_w * (row.high - minimum) / span)
        draw.line((min(ordinary_x, high_x), y, max(ordinary_x, high_x), y), fill=rgb("CBD5E1"), width=6)
        draw.ellipse((ordinary_x - 10, y - 10, ordinary_x + 10, y + 10), fill=rgb(SLATE))
        draw.ellipse((high_x - 12, y - 12, high_x + 12, y + 12), fill=rgb(CORAL))
        draw.text((ordinary_x, y + 24), f"{row.ordinary:.1f}", fill=rgb(SLATE), font=chart_font(15), anchor="mm")
        draw.text((high_x, y - 24), f"{row.high:.1f}", fill=rgb(CORAL), font=chart_font(15, True), anchor="mm")
    legend_y = 950
    draw.ellipse((585, legend_y - 10, 605, legend_y + 10), fill=rgb(SLATE))
    draw.text((620, legend_y), "Ordinary", fill=rgb(INK), font=chart_font(18), anchor="lm")
    draw.ellipse((820, legend_y - 11, 842, legend_y + 11), fill=rgb(CORAL))
    draw.text((857, legend_y), "High pressure", fill=rgb(INK), font=chart_font(18), anchor="lm")
    unit = "Runs per 100 records" if role == "Batter" else "Bowler-credited wickets per 100 records"
    draw.text((585, legend_y + 48), unit, fill=rgb(MUTED), font=chart_font(17), anchor="lm")
    return save_image(image, f"{role.lower()}_pressure_comparison.png")


def chart_stability(players: pd.DataFrame) -> Path:
    image, draw = chart_canvas(1800, 1050, "Every official player remains below the predefined 75 percent core threshold")
    panel_w = 850
    for panel_idx, role in enumerate(["Batter", "Bowler"]):
        frame = players[players.role.eq(role)].sort_values("rank")
        origin_x = 35 + panel_idx * 900
        draw.text((origin_x, 95), role, fill=rgb(INK), font=chart_font(26, True))
        label_w, bar_w, top, row_h = 270, 500, 145, 78
        threshold_x = origin_x + label_w + int(bar_w * 75 / 80)
        for dash_y in range(top - 20, top + row_h * 10, 18):
            draw.line((threshold_x, dash_y, threshold_x, dash_y + 10), fill=rgb(CORAL), width=3)
        for i, row in enumerate(frame.itertuples()):
            y = top + i * row_h
            draw.text((origin_x, y + 22), row.player_name, fill=rgb(INK), font=chart_font(18), anchor="lm")
            value = row.top10_frequency_nested * 100
            width = int(bar_w * value / 80)
            x = origin_x + label_w
            draw.rounded_rectangle((x, y, x + width, y + 44), radius=6, fill=rgb(TEAL))
            draw.text((x + width + 10, y + 22), f"{value:.0f}%", fill=rgb(INK), font=chart_font(17, True), anchor="lm")
    draw.line((1260, 995, 1260, 1019), fill=rgb(CORAL), width=3)
    draw.text((1280, 1007), "Predefined 75 percent core threshold", fill=rgb(MUTED), font=chart_font(18), anchor="lm")
    return save_image(image, "ranking_stability.png")


def configure_styles(doc: Document) -> None:
    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(10.2)
    normal.font.color.rgb = RGBColor.from_string(INK)
    normal._element.rPr.rFonts.set(qn("w:ascii"), FONT)
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), FONT)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.12

    body = styles["Body Text"]
    body.font.name = FONT
    body.font.size = Pt(10.2)
    body.font.color.rgb = RGBColor.from_string(INK)
    body._element.rPr.rFonts.set(qn("w:ascii"), FONT)
    body._element.rPr.rFonts.set(qn("w:hAnsi"), FONT)
    body.paragraph_format.space_after = Pt(6)
    body.paragraph_format.line_spacing = 1.12

    title = styles["Title"]
    title.font.name = FONT
    title.font.size = Pt(28)
    title.font.bold = True
    title.font.color.rgb = RGBColor.from_string(BLACK)
    title._element.rPr.rFonts.set(qn("w:ascii"), FONT)
    title._element.rPr.rFonts.set(qn("w:hAnsi"), FONT)
    title.paragraph_format.space_after = Pt(10)
    for style in styles:
        if style.type == 1:
            ppr = style._element.find(qn("w:pPr"))
            if ppr is not None:
                for border in list(ppr.findall(qn("w:pBdr"))):
                    ppr.remove(border)

    for name, size, before, after in (("Heading 1", 19, 12, 8), ("Heading 2", 13.5, 10, 5), ("Heading 3", 11.2, 8, 4)):
        style = styles[name]
        style.font.name = FONT
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor.from_string(BLACK)
        style._element.rPr.rFonts.set(qn("w:ascii"), FONT)
        style._element.rPr.rFonts.set(qn("w:hAnsi"), FONT)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True

    for list_name in ("List Bullet", "List Bullet 2", "List Number"):
        style = styles[list_name]
        style.font.name = FONT
        style.font.size = Pt(9.8)
        style.font.color.rgb = RGBColor.from_string(INK)
        style._element.rPr.rFonts.set(qn("w:ascii"), FONT)
        style._element.rPr.rFonts.set(qn("w:hAnsi"), FONT)

    caption = styles["Caption"]
    caption.font.name = FONT
    caption.font.size = Pt(8.5)
    caption.font.color.rgb = RGBColor.from_string(MUTED)
    caption._element.rPr.rFonts.set(qn("w:ascii"), FONT)
    caption._element.rPr.rFonts.set(qn("w:hAnsi"), FONT)


def configure_section(section, first=False) -> None:
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(1.7)
    section.bottom_margin = Cm(1.55)
    section.left_margin = Cm(1.7)
    section.right_margin = Cm(1.7)
    section.header_distance = Cm(0.65)
    section.footer_distance = Cm(0.65)
    if first:
        section.different_first_page_header_footer = True


def add_header_footer(section) -> None:
    header = section.header
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    add_text(p, "SupeRR Selector Season 2", bold=True, color=BLACK, size=7.8)
    add_text(p, "    Methodology Report", color=MUTED, size=7.8)
    p.paragraph_format.space_after = Pt(0)

    footer = section.footer
    table = footer.add_table(rows=1, cols=2, width=Inches(6.9))
    table.autofit = False
    table.cell(0, 0).width = Inches(5.5)
    table.cell(0, 1).width = Inches(1.4)
    left = table.cell(0, 0).paragraphs[0]
    add_text(left, "2022 to 2026 IPL and T20I evidence", color=MUTED, size=7.5)
    right = table.cell(0, 1).paragraphs[0]
    right.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    add_text(right, "Page ", color=MUTED, size=7.5)
    add_field(right, "PAGE")
    add_text(right, " of ", color=MUTED, size=7.5)
    add_field(right, "NUMPAGES")
    for cell in table.rows[0].cells:
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_margins(cell, top=0, bottom=0, start=0, end=0)
        tc_pr = cell._tc.get_or_add_tcPr()
        borders = OxmlElement("w:tcBorders")
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
            tag = OxmlElement(f"w:{edge}")
            tag.set(qn("w:val"), "nil")
            borders.append(tag)
        tc_pr.append(borders)


def ranking_table_rows(players: pd.DataFrame, role: str) -> list[list[str]]:
    frame = players[players.role.eq(role)].sort_values("rank")
    rows = []
    for row in frame.itertuples():
        rows.append(
            [
                str(int(row.rank)),
                row.player_name,
                row.qualifying_formats,
                f"{row.combined_rating:.2f}",
                f"{row.top10_frequency_nested:.0%}",
                f"{int(row.scenario_top10_count)}/13",
            ]
        )
    return rows


def add_player_profile(doc: Document, row: pd.Series, pressure: pd.DataFrame) -> None:
    heading = add_heading(doc, f"{int(row['rank'])}  {row.player_name}", 2)
    heading.paragraph_format.space_before = Pt(5)
    meta = doc.add_paragraph()
    add_text(meta, f"Official rating {row.combined_rating:.2f}", bold=True, color=BLACK, size=9.5)
    add_text(meta, f"    Qualifying formats {row.qualifying_formats}", color=INK, size=9.5)
    add_text(meta, f"    Nested Top-10 frequency {row.top10_frequency_nested:.0%}", color=INK, size=9.5)
    set_paragraph_spacing(meta, after=4)

    rows = []
    for line in pressure_lines(row, pressure):
        format_name, comparison = line.split(":", 1)
        rows.append([format_name, comparison.strip()])
    add_table(doc, ["Evidence", "High pressure compared with ordinary records"], rows, widths=[1.0, 5.65], aligns=["center", "left"], font_size=8.0, header_fill=SLATE)

    p = doc.add_paragraph()
    add_text(p, "Why selected  ", bold=True, color=BLACK, size=9.2)
    reason = f"Strongest signal: {human_metric(row.strongest_metric)} ({row.strongest_weighted_z * 10:+.1f} rating points in that format). " + str(row.format_interpretation)
    for key, label in [("ordinary_clean_records", "ordinary no-extras records"), ("high_clean_records", "High-pressure no-extras records"), ("ordinary_records", "ordinary records"), ("high_records", "High-pressure records"), ("high_matches", "matches with High-pressure records")]:
        reason = reason.replace(key, label)
    reason = reason.replace("evidence is No observed records and is excluded because no player-format performance record in supplied analytical population", "has no observed player-format records in the analytical population")
    add_text(p, reason, color=INK, size=9.2)
    set_paragraph_spacing(p, after=3)

    p = doc.add_paragraph()
    add_text(p, "How this could strengthen Rajasthan Royals  ", bold=True, color=BLACK, size=9.2)
    add_text(p, rr_fit_text(row), color=INK, size=9.2)
    set_paragraph_spacing(p, after=3)

    p = doc.add_paragraph()
    add_text(p, "What to monitor  ", bold=True, color=BLACK, size=9.2)
    add_text(p, monitoring_text(row), color=INK, size=9.2)
    set_paragraph_spacing(p, after=8)


def build_report() -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    players = pd.read_csv(ROOT / "phase7_outputs" / "phase7_canonical_player_evidence.csv")
    pressure = pd.read_csv(ROOT / "phase6_outputs" / "phase6_pressure_vs_ordinary_evidence.csv")
    eligibility = pd.read_csv(ROOT / "phase4_outputs" / "phase4_eligibility_summary.csv")

    players = players.sort_values(["role", "rank"]).reset_index(drop=True)
    setup_plot()
    charts = {
        "scope": chart_data_scope(),
        "pressure_distribution": chart_pressure_distribution(),
        "weights": chart_weights(),
        "eligibility": chart_eligibility(eligibility),
        "batter_rankings": chart_rankings(players, "Batter"),
        "bowler_rankings": chart_rankings(players, "Bowler"),
        "batter_pressure": chart_pressure_comparison(players, pressure, "Batter"),
        "bowler_pressure": chart_pressure_comparison(players, pressure, "Bowler"),
        "stability": chart_stability(players),
    }

    doc = Document()
    configure_styles(doc)
    configure_section(doc.sections[0], first=True)
    add_header_footer(doc.sections[0])
    set_update_fields(doc)

    # Cover
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Cm(1.2)
    add_text(p, "SUPERR SELECTOR SEASON 2", bold=True, color=GOLD, size=10)
    set_paragraph_spacing(p, after=10)

    title = doc.add_paragraph(style="Title")
    add_text(title, "SupeRR Selector Season 2 Methodology Report", bold=True, color=BLACK, size=28)
    title.paragraph_format.keep_with_next = True
    subtitle = doc.add_paragraph()
    add_text(subtitle, "Most reliable batters and bowlers under structural pressure", color=BLACK, size=15)
    set_paragraph_spacing(subtitle, after=12)

    intro = doc.add_paragraph()
    add_text(intro, "A transparent ranking system for IPL and T20I performance from 2022 to 2026, prepared for Rajasthan Royals IPL 2027 auction evaluation.", color=INK, size=11.5)
    intro.paragraph_format.line_spacing = 1.2
    intro.paragraph_format.space_after = Pt(26)

    add_metric_strip(
        doc,
        [
            ("188,330", "pressure-labelled records"),
            ("789", "unrevised matches"),
            ("20", "official selections"),
            ("2022 to 2026", "historical evidence window"),
        ],
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    add_heading(doc, "Headline selections", 2)
    top_batter = players[(players.role == "Batter") & (players["rank"] == 1)].iloc[0]
    top_bowler = players[(players.role == "Bowler") & (players["rank"] == 1)].iloc[0]
    add_table(
        doc,
        ["Role", "Rank 1 player", "Official rating", "Qualifying evidence"],
        [
            ["Batter", top_batter.player_name, f"{top_batter.combined_rating:.2f}", top_batter.qualifying_formats],
            ["Bowler", top_bowler.player_name, f"{top_bowler.combined_rating:.2f}", top_bowler.qualifying_formats],
        ],
        widths=[1.1, 2.4, 1.3, 1.85],
        aligns=["center", "left", "center", "center"],
        font_size=9,
    )
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    add_text(p, "Round 1 methodology report", bold=True, color=BLACK, size=9.5)
    add_text(p, "\nPrepared for Rajasthan Royals", color=MUTED, size=8.5)
    set_paragraph_spacing(p, after=0)

    # Executive answer
    add_section_break(doc, "Executive answer", "What the analysis concludes")
    add_body(
        doc,
        "Nicholas Pooran ranks first among batters with a 62.21 official rating from Reliable IPL evidence. Sufiyan Muqeem ranks first among bowlers with a 69.67 rating from Reliable T20I evidence. The rankings use performance above contextual expectations under a pre-delivery structural-pressure state, not player reputation or conventional averages alone.",
    )
    add_body(
        doc,
        "The system labels pressure before the current delivery outcome, evaluates IPL and T20I independently, applies predefined sample thresholds, and combines formats only when both are Reliable. All eligible 2022 to 2026 evidence receives equal historical weight; there is no recent-form adjustment.",
    )
    add_metric_strip(
        doc,
        [
            ("80", "reliable batter candidates"),
            ("105", "reliable bowler candidates"),
            ("5,000", "fixed bootstrap replicates"),
            ("1,000", "nested bootstrap replicates"),
        ],
    )
    add_heading(doc, "Top five at a glance", 2)
    batters = players[players.role.eq("Batter")].sort_values("rank").head(5).reset_index(drop=True)
    bowlers = players[players.role.eq("Bowler")].sort_values("rank").head(5).reset_index(drop=True)
    rows = []
    for idx in range(5):
        rows.append(
            [
                str(idx + 1),
                batters.loc[idx, "player_name"],
                f"{batters.loc[idx, 'combined_rating']:.2f}",
                bowlers.loc[idx, "player_name"],
                f"{bowlers.loc[idx, 'combined_rating']:.2f}",
            ]
        )
    add_table(doc, ["Rank", "Batter", "Rating", "Bowler", "Rating"], rows, widths=[0.6, 2.2, 0.9, 2.2, 0.9], aligns=["center", "left", "center", "left", "center"], font_size=8.8)
    add_heading(doc, "Five conclusions to retain", 2)
    reset_numbering(doc)
    add_numbered(doc, "Pressure is structural and pre-delivery. It uses wicket strain, recent wicket shock and innings-stage urgency.")
    add_numbered(doc, "A rating of 50 is the Reliable player baseline within a role and format. Ten rating points represent one unit of the weighted standardized composite.")
    add_numbered(doc, "IPL and T20I are never pooled before normalization. A missing or unreliable format is excluded, not scored as zero.")
    add_numbered(doc, "All 20 official selections are boundary Top 10 results because none reaches the predefined 75% inclusion threshold in both bootstrap modes.")
    add_numbered(doc, "The Rajasthan Royals interpretation describes potential pressure contribution. It does not model auction price, availability, player role negotiations or the final 2027 squad composition.")

    # Contents
    add_section_break(doc, "Contents", "How to read this report")
    add_heading(doc, "Reader guide", 2)
    add_table(
        doc,
        ["Section", "Pages"],
        [
            ["Executive answer", "2"],
            ["Challenge and analytical scope", "4"],
            ["Structural pressure model", "5"],
            ["Performance measurement and scoring", "6"],
            ["Fair comparison and eligibility", "7"],
            ["Official Top 10 batter rankings", "8"],
            ["Official Top 10 bowler rankings", "9"],
            ["Pressure evidence behind the selections", "10"],
            ["Bowler pressure evidence", "11"],
            ["Uncertainty and robustness", "12"],
            ["Rajasthan Royals auction interpretation", "13"],
            ["Batter evidence profiles", "14 to 18"],
            ["Bowler evidence profiles", "19 to 23"],
            ["Limitations and responsible use", "24"],
            ["Reproducibility and validation", "25"],
            ["Appendix and glossary", "26"],
            ["Technical scoring rules", "27"],
            ["Qualifying player samples", "28"],
        ],
        widths=[5.4, 1.2],
        aligns=["left", "center"],
        font_size=8.6,
    )

    # Scope
    add_section_break(doc, "Challenge and analytical scope", "From problem statement to analytical population")
    add_body(
        doc,
        "The challenge asks for two ordered Top 10 lists and a methodology that defines pressure, measures batting and bowling performance, makes fair IPL and T20I comparisons, supports every selection with evidence, and explains uncertainty. Rankings must come from the supplied data rather than reputation.",
    )
    add_figure(doc, charts["scope"], 6.55, 1, "Match population through the analytical pipeline", "Phase 1 audit and Phase 3 structural-pressure outputs", "Horizontal bars showing 883 registered matches, 853 target IPL and T20I matches, 813 eligible completed matches and 789 matches in the pressure model.")
    add_heading(doc, "Data included", 2)
    add_table(
        doc,
        ["Population", "Size", "Treatment"],
        [
            ["Six supplied CSV sources", "237,170 records", "Audited for schema, identity, duplicates and relationships"],
            ["Eligible completed matches", "813 matches", "362 IPL and 451 men's T20I matches"],
            ["Regulation delivery records", "192,235 records", "Innings 1 and 2 only"],
            ["Primary pressure population", "188,330 records", "789 whole unrevised matches"],
            ["Revised or shortened matches", "24 matches", "Excluded from the primary pressure model"],
            ["Super Over records", "26 records", "Kept separate from regulation analysis"],
        ],
        widths=[2.1, 1.25, 3.3],
        aligns=["left", "center", "left"],
        font_size=8.5,
    )
    add_heading(doc, "Data integrity decisions", 2)
    add_bullet(doc, "Player ID is the identity key. Names are descriptive labels and are not used to merge players.")
    add_bullet(doc, "The updated ball-by-ball source corrects extras-run values. Extras type remains the event-category field.")
    add_bullet(doc, "Exact legal-ball progression remains unresolved for 257 other or penalty records, so the pressure model does not infer balls remaining.")
    add_bullet(doc, "A match is excluded from the primary model if any revision or shortened-schedule field is populated.")

    # Pressure
    add_section_break(doc, "Structural pressure model", "Pressure is fixed before the outcome")
    add_body(
        doc,
        "Structural pressure measures the strain visible before each delivery record. It is not win probability, required-run-rate pressure or a complete scoreboard-pressure model. The same pre-delivery pressure state applies to the batter and bowler; role-specific value is measured only after the state is fixed.",
    )
    add_table(
        doc,
        ["Component", "Construction", "Why it matters"],
        [
            ["Wicket strain", "Positive z-score for wickets already lost versus a leave-one-match-out format, innings and over benchmark; capped at 3 SD and divided by 3", "Captures whether the batting side has lost more wickets than expected for that point"],
            ["Recent wicket shock", "Wickets in the prior 12 delivery records divided by 3 and capped at 1", "Captures immediate disruption without using the current delivery"],
            ["Stage urgency", "Source over minus 1 divided by 19", "Adds increasing innings-stage urgency from over 1 to over 20"],
        ],
        widths=[1.25, 3.15, 2.25],
        aligns=["left", "left", "left"],
        font_size=8.2,
    )
    add_body(doc, "The continuous structural-pressure index is the equal-weight mean of the three bounded components. Equal weights were fixed before player rankings and tested against wicket-heavy, shock-heavy, stage-heavy and alternative recent-window variants.")
    add_figure(doc, charts["pressure_distribution"], 6.55, 2, "Pressure-band calibration by format and innings", "Phase 3 structural-pressure model", "Stacked horizontal bars showing approximately 40 percent Low, 40 percent Medium and 20 percent High pressure records for each format and innings.")
    add_heading(doc, "When a delivery is High pressure", 2)
    add_body(doc, "Records are ranked by the continuous index within format and innings. Low is at or below the 40th percentile, Medium is above the 40th and at or below the 80th percentile, and High is above the 80th percentile. The current ball's dot, single, boundary, six or wicket never determines its pressure label.")
    add_heading(doc, "Benchmark independence and robustness", 2)
    add_bullet(doc, "Wicket expectations exclude the entire current match and require at least 100 out-of-match records.")
    add_bullet(doc, "All 30,290 match-state benchmarks use exact format, innings and source-over support; no fallback is required.")
    add_bullet(doc, "All alternative pressure variants retain Spearman correlation above 0.95 with the primary continuous index.")

    # Measurement
    add_section_break(doc, "Performance measurement and scoring", "What earns a high rating")
    add_body(doc, "Each outcome is compared with an expected benchmark for the same format, innings, source over and pressure category. Observed minus expected performance forms a context-adjusted residual. High-pressure quality and continuous pressure-response gradients are then shrunk, normalized and weighted within each role and format.")
    add_figure(doc, charts["weights"], 5.4, 3, "Predefined batting and bowling metric weights", "Phase 4 methodology specification", "Two stacked horizontal bars showing the four predefined rating weights for batting and bowling.")
    add_table(
        doc,
        ["Role", "Metric", "Definition"],
        [
            ["Batting", "Scoring quality", "Batter runs per 100 eligible batting records above the contextual expectation in High pressure"],
            ["Batting", "Survival quality", "Striker survival above the contextual expectation in High pressure"],
            ["Batting", "Pressure responses", "Continuous relationship between pressure percentile and context-adjusted scoring or survival"],
            ["Bowling", "Wicket quality", "Bowler-credited wickets per 100 delivery records above the contextual expectation"],
            ["Bowling", "Run suppression quality", "Batter-run suppression on no-extras records relative to context"],
            ["Bowling", "Pressure responses", "Continuous relationship between pressure percentile and wicket threat or run suppression"],
        ],
        widths=[1.0, 1.75, 3.9],
        aligns=["center", "left", "left"],
        font_size=8.2,
    )
    add_heading(doc, "From metric values to ratings", 2)
    reset_numbering(doc)
    add_numbered(doc, "Shrink each metric toward zero according to its evidence volume. Batting uses a shrinkage constant of 80 records; bowling uses 100 for wicket metrics and 80 for run-suppression metrics.")
    add_numbered(doc, "Winsorize each Reliable role-format metric at the 2.5th and 97.5th percentiles, then standardize it within that Reliable pool.")
    add_numbered(doc, "Apply the locked weights to the standardized metrics. The format rating is 50 plus 10 times the weighted composite z-score.")
    add_numbered(doc, "Normalize IPL and T20I separately. If both are Reliable, combine them 50 percent each. Otherwise use the single Reliable format alone.")
    add_heading(doc, "Why the result can differ from conventional averages", 2)
    add_body(doc, "The model does not rank conventional batting or bowling averages. It asks whether a player performs above the expected outcome for the same match context, with explicit pressure samples and shrinkage. A player can therefore rank highly without leading a conventional average table. That distinction is intentional and should be considered alongside role, price and broader cricket judgement.")

    # Fair comparison
    add_section_break(doc, "Fair comparison and eligibility", "Sample size comes before ranking")
    add_body(doc, "Only Reliable format evidence can contribute to an official score. Provisional evidence remains visible for interpretation but cannot enter the rating. Insufficient evidence and unobserved formats are excluded without assigning zero.")
    add_figure(doc, charts["eligibility"], 6.55, 4, "Player-format evidence after eligibility checks", "Phase 4 eligibility summary", "Stacked bars showing Reliable, Provisional and Insufficient player-format records for batters and bowlers in IPL and T20I.")
    add_table(
        doc,
        ["Role", "Reliable threshold", "Provisional threshold"],
        [
            ["Batter", "80 High records, 8 High matches, 160 ordinary records", "40 High records, 5 High matches, 80 ordinary records"],
            ["Bowler", "100 High records, 8 High matches, 200 ordinary records, 80 High clean and 160 ordinary clean records", "50 High records, 5 High matches, 100 ordinary records, 40 High clean and 80 ordinary clean records"],
        ],
        widths=[1.0, 2.85, 2.85],
        aligns=["center", "left", "left"],
        font_size=8.2,
    )
    add_heading(doc, "Reliable candidate pools", 2)
    add_bullet(doc, "80 batter candidates have at least one Reliable format; 11 have Reliable evidence in both formats.")
    add_bullet(doc, "105 bowler candidates have at least one Reliable format; 20 have Reliable evidence in both formats.")
    add_bullet(doc, "The official period is all eligible 2022 to 2026 evidence. There is no 15 percent recent-form weight or other recency adjustment.")
    add_bullet(doc, "Final ordering uses unrounded combined ratings, with player ID as the deterministic tie-break.")

    # Rankings
    add_section_break(doc, "Official Top 10 batter rankings", "Final ordered list")
    add_figure(doc, charts["batter_rankings"], 6.55, 5, "Official Top 10 batter ratings", "Phase 7 canonical player evidence", "Horizontal bars showing the official ratings and qualifying formats for the ten selected batters.")
    add_table(doc, ["Rank", "Player", "Formats", "Rating", "Nested Top 10", "Scenarios"], ranking_table_rows(players, "Batter"), widths=[0.5, 2.05, 1.0, 0.85, 1.05, 0.9], aligns=["center", "left", "center", "center", "center", "center"], font_size=8.4)
    add_body(doc, "Nicholas Pooran leads on Reliable IPL evidence. Hardik Pandya, Suryakumar Yadav and Rinku Singh are the three selected batters with Reliable evidence in both formats.")

    add_section_break(doc, "Official Top 10 bowler rankings", "Final ordered list")
    add_figure(doc, charts["bowler_rankings"], 6.55, 6, "Official Top 10 bowler ratings", "Phase 7 canonical player evidence", "Horizontal bars showing the official ratings and qualifying formats for the ten selected bowlers.")
    add_table(doc, ["Rank", "Player", "Formats", "Rating", "Nested Top 10", "Scenarios"], ranking_table_rows(players, "Bowler"), widths=[0.5, 2.05, 1.0, 0.85, 1.05, 0.9], aligns=["center", "left", "center", "center", "center", "center"], font_size=8.4)
    add_body(doc, "Sufiyan Muqeem leads on Reliable T20I evidence. Kuldeep Yadav and Varun Chakravarthy are the two selected bowlers with Reliable evidence in both formats.")

    # Pressure evidence
    add_section_break(doc, "Pressure evidence behind the selections", "High pressure compared with ordinary records")
    add_body(doc, "The figures below show raw outcomes for the strongest qualifying format when a player has two Reliable formats. They aid interpretation but do not replace context-adjusted residuals, shrinkage or continuous gradients in the official rating.")
    add_figure(doc, charts["batter_pressure"], 6.55, 7, "Batter scoring in High pressure and ordinary records", "Phase 6 pressure-versus-ordinary evidence", "Dumbbell chart comparing High-pressure and ordinary runs per 100 records for each selected batter, using the higher-rated qualifying format for two-format players.")
    add_heading(doc, "How to interpret the comparison", 2)
    add_bullet(doc, "A higher raw rate under High pressure is descriptive. The rating also adjusts for the expected rate in the same context.")
    add_bullet(doc, "For batting survival, higher is better. For bowling batter runs allowed, lower is better.")
    add_bullet(doc, "Ordinary combines Low and Medium pressure for reporting. Continuous pressure percentile remains the direct gradient input.")
    add_bullet(doc, "The delivery outcome is evaluated only after its pre-delivery pressure state has been fixed.")
    add_section_break(doc, "Bowler pressure evidence", "Wicket threat in High pressure and ordinary records")
    add_figure(doc, charts["bowler_pressure"], 6.55, 8, "Bowler wicket rates in High pressure and ordinary records", "Phase 6 pressure-versus-ordinary evidence", "Dumbbell chart comparing High-pressure and ordinary bowler-credited wickets per 100 records for each selected bowler, using the higher-rated qualifying format for two-format players.")
    add_body(doc, "Sufiyan Muqeem and Kuldeep Yadav show large raw wicket-rate increases in their illustrated T20I evidence. Sunil Narine and Abrar Ahmed also derive substantial rating value from contextual run suppression, which is not shown in this wicket chart. Mitchell Starc combines high wicket threat with a negative contextual run-suppression residual.")

    # Uncertainty
    add_section_break(doc, "Uncertainty and robustness", "How much confidence to place in the order")
    add_figure(doc, charts["stability"], 6.55, 9, "Nested-bootstrap Top 10 inclusion frequency", "Phase 6 uncertainty and robustness output", "Two horizontal bar charts showing nested-bootstrap Top 10 inclusion frequencies for selected batters and bowlers, with a dashed 75 percent core threshold.")
    add_table(
        doc,
        ["Test", "Scale", "Purpose"],
        [
            ["Fixed-benchmark bootstrap", "5,000 match-level replicates", "Resamples IPL and T20I matches while holding pressure labels and outcome benchmarks fixed"],
            ["Nested-benchmark bootstrap", "1,000 match-level replicates", "Rebuilds outcome benchmarks and eligibility inside each resample"],
            ["Deterministic scenarios", "13 scenarios", "Changes weights, eligibility thresholds and pressure definitions"],
            ["Leave-one-player-out", "185 reliable candidates", "Tests whether a player's own records materially influence expected-outcome benchmarks"],
        ],
        widths=[1.75, 1.65, 3.3],
        aligns=["left", "center", "left"],
        font_size=8.3,
    )
    add_heading(doc, "What the uncertainty results mean", 2)
    add_body(doc, "Every official selection remains a boundary Top 10 result because no player reaches at least 75 percent Top-10 inclusion in both bootstrap modes. The full-data order remains official, but the report does not present it as certain.")
    add_bullet(doc, "Kuldeep Yadav has the highest nested inclusion among bowlers at 74.0 percent, followed by Sunil Narine at 68.9 percent.")
    add_bullet(doc, "Hardik Pandya has the highest nested inclusion among batters at 65.1 percent, followed by Nicholas Pooran at 59.8 percent.")
    add_bullet(doc, "Leave-one-player-out benchmarking does not change Top-10 membership for any official player.")
    add_bullet(doc, "Bootstrap inclusion is ranking stability under match resampling, not the probability that a player is objectively Top 10.")

    # Auction framework
    add_section_break(doc, "Rajasthan Royals auction interpretation", "How the rankings should support IPL 2027 decisions")
    add_body(doc, "The ranking is a pressure-performance screen. Rajasthan Royals can use it to identify evidence-backed auction candidates, then layer in role requirements, availability, price, age, fitness and squad composition. The model does not estimate auction value or player availability.")
    add_heading(doc, "Three decision lenses", 2)
    reset_numbering(doc)
    add_numbered(doc, "Pressure contribution. Identify whether the player adds scoring, survival, wicket threat or run control when structural pressure is elevated.")
    add_numbered(doc, "Evidence breadth. Prefer two-format evidence when a decision needs protection against competition-specific performance, while retaining strong single-format specialists where IPL evidence is Reliable.")
    add_numbered(doc, "Ranking stability. Treat higher bootstrap inclusion and stronger scenario retention as supporting evidence, not a substitute for cricket judgement.")
    add_heading(doc, "Shortlist groups", 2)
    add_table(
        doc,
        ["Decision use", "Batters", "Bowlers", "Interpretation"],
        [
            ["Two-format evidence", "Hardik Pandya, Suryakumar Yadav, Rinku Singh", "Kuldeep Yadav, Varun Chakravarthy", "Reliable IPL and T20I ratings both contribute"],
            ["Higher stability", "Hardik Pandya, Nicholas Pooran, Jimmy Neesham", "Kuldeep Yadav, Sunil Narine", "Nested Top-10 frequency at or above 50 percent"],
            ["IPL specialist evidence", "Nicholas Pooran, Jos Buttler, Shreyas Iyer", "Sunil Narine, Mitchell Starc, Eshan Malinga, Suyash Sharma, Mohit Sharma", "Official score uses Reliable IPL evidence alone"],
            ["Additional boundary review", "Jos Buttler, Romario Shepherd, Iftikhar Ahmed, Rinku Singh", "Abrar Ahmed, Eshan Malinga, Varun Chakravarthy, Suyash Sharma, Mohit Sharma", "Nested inclusion below 40 percent"],
        ],
        widths=[1.25, 1.95, 2.15, 1.35],
        aligns=["left", "left", "left", "left"],
        font_size=7.8,
    )
    add_body(doc, "These groups are not separate rankings. A player can appear in more than one group because evidence breadth, format specialization and stability answer different auction questions.")

    # Player profiles
    add_section_break(doc, "Batter evidence profiles", "Why each batter qualifies")
    add_body(doc, "Each profile uses the official score, qualifying format evidence, raw High-versus-ordinary comparison and nested-bootstrap stability. The Rajasthan Royals interpretation describes potential contribution rather than a purchase recommendation.")
    batter_rows = players[players.role.eq("Batter")].sort_values("rank")
    for idx, (_, row) in enumerate(batter_rows.iterrows()):
        if idx > 0 and idx % 2 == 0:
            doc.add_page_break()
        add_player_profile(doc, row, pressure)

    add_section_break(doc, "Bowler evidence profiles", "Why each bowler qualifies")
    add_body(doc, "Bowler profiles separate wicket threat from batter-run suppression. Run suppression uses no-extras records and is not conventional economy rate.")
    bowler_rows = players[players.role.eq("Bowler")].sort_values("rank")
    for idx, (_, row) in enumerate(bowler_rows.iterrows()):
        if idx > 0 and idx % 2 == 0:
            doc.add_page_break()
        add_player_profile(doc, row, pressure)

    # Limitations
    add_section_break(doc, "Limitations and responsible use", "What the model does not claim")
    add_bullet(doc, "Structural pressure excludes targets, required run rate, score parity, win probability and exact legal balls remaining. It captures wicket-related disruption and innings-stage urgency only.")
    add_bullet(doc, "The High band is percentile-based. Records near the 80th-percentile boundary can change category under alternative windows or weights even when the continuous index remains highly correlated.")
    add_bullet(doc, "Single-format ratings can rank highly, but an absent or unreliable format offers no balancing evidence. The excluded format is not scored as zero.")
    add_bullet(doc, "Raw High-versus-ordinary comparisons are descriptive. Context-adjusted residuals and continuous gradients drive the official rating.")
    add_bullet(doc, "All 20 selections are boundary Top 10 results under the predefined 75 percent stability requirement. The rank order is suitable for a shortlist, not a claim of certainty.")
    add_bullet(doc, "The analysis does not model price, retention, overseas-player limits, availability, batting position, bowling phase assignment, injury, age or future squad rules.")
    add_bullet(doc, "The supplied data window is 2022 to 2026 with no recency weighting. Future 2026 records or auction developments outside the supplied data are not represented.")
    add_heading(doc, "Interpretation guardrails", 2)
    add_table(
        doc,
        ["Use this wording", "Avoid this wording"],
        [
            ["Structural pressure", "Win probability or complete scoreboard pressure"],
            ["Top-10 bootstrap frequency", "Probability that the player is objectively Top 10"],
            ["Batter-run suppression", "Conventional economy rate"],
            ["Reliable format evidence", "Guaranteed performance"],
            ["Boundary Top 10", "Invalid selection or certain selection"],
        ],
        widths=[3.0, 3.7],
        aligns=["left", "left"],
        font_size=8.5,
    )

    # Reproducibility
    add_section_break(doc, "Reproducibility and validation", "How another analyst can follow the work")
    add_heading(doc, "Seven-step analytical path", 2)
    steps = [
        "Audit all six sources and retain player ID as the identity key.",
        "Build the validated match, innings and delivery master; separate Super Overs and revised matches.",
        "Calculate prior-only wicket state and the three-component structural-pressure index.",
        "Build leave-one-match-out pressure benchmarks and assign within-format-and-innings percentile bands.",
        "Calculate role-specific context-adjusted outcomes, shrinkage, Reliable eligibility and format ratings.",
        "Combine Reliable IPL and T20I ratings under the locked rule, then rank unrounded scores.",
        "Test fixed and nested bootstraps, deterministic scenarios and leave-one-player-out benchmarks before interpretation.",
    ]
    reset_numbering(doc)
    for step in steps:
        add_numbered(doc, step)
    add_heading(doc, "Validation record", 2)
    add_table(
        doc,
        ["Phase", "Validation gates", "Failures", "Primary assurance"],
        [
            ["Phase 1", "11", "0", "Schemas, relationships, identities and scope"],
            ["Phase 2", "11", "0", "Clean analytical master and delivery evidence"],
            ["Phase 3", "15", "0", "Leakage-free pressure construction and robustness"],
            ["Phase 4", "16", "0", "Eligibility, normalization and complete scores"],
            ["Phase 5", "16", "0", "Rank reproduction, bootstrap and sensitivity"],
            ["Phase 6", "20", "0", "Selection evidence and interpretation consistency"],
            ["Phase 7A", "20", "0", "Frozen sources, claims, terminology and ranking signature"],
        ],
        widths=[1.0, 1.25, 0.85, 3.6],
        aligns=["center", "center", "center", "left"],
        font_size=8.4,
    )
    add_heading(doc, "Authoritative artifacts", 2)
    add_table(
        doc,
        ["Artifact", "Purpose"],
        [
            ["Phase 0 to 3 Consolidated Report", "Data audit, reconstruction and structural-pressure decisions"],
            ["Phase 3 model specification and labelled deliveries", "Pressure definition and record-level labels"],
            ["Phase 4 methodology, metrics and combined scores", "Eligibility, normalization, weights and ratings"],
            ["Phase 5 rankings and uncertainty outputs", "Official order, bootstrap, scenarios and self-influence"],
            ["Phase 6 selected-player evidence", "Pressure comparisons, uncertainty and approved explanations"],
            ["Phase 7 canonical player evidence", "Frozen official selection bundle and ranking signature"],
        ],
        widths=[2.8, 3.9],
        aligns=["left", "left"],
        font_size=8.4,
    )
    add_source_note(doc, "Official ranking signature: 5295c708a26033d841f85a6159c3db53096fbf20058303c7ce85093019f63f99")

    # Appendix
    add_section_break(doc, "Appendix and glossary", "Exact rules used in the report")
    add_heading(doc, "Format combination examples", 2)
    add_table(
        doc,
        ["Evidence state", "Official score"],
        [
            ["IPL Reliable and T20I Reliable", "50 percent IPL rating plus 50 percent T20I rating"],
            ["IPL Reliable and T20I Provisional or Insufficient", "IPL rating alone"],
            ["T20I Reliable and IPL Provisional or Insufficient", "T20I rating alone"],
            ["Neither format Reliable", "Not eligible for the official ranking"],
        ],
        widths=[3.2, 3.5],
        aligns=["left", "left"],
        font_size=8.5,
    )
    add_heading(doc, "Glossary", 2)
    add_table(
        doc,
        ["Term", "Meaning"],
        [
            ["Structural pressure", "Pre-delivery state built from wicket strain, recent wicket shock and innings-stage urgency"],
            ["High pressure", "Records above the 80th percentile of structural pressure within format and innings"],
            ["Ordinary", "Low and Medium pressure combined for descriptive comparisons"],
            ["Reliable", "Format evidence that passes every locked eligibility gate and may contribute to the official score"],
            ["Provisional", "Informative format evidence that fails at least one Reliable gate"],
            ["Combined rating", "Validated score after separate format normalization and the locked combination rule"],
            ["Pressure response", "Continuous association between pressure percentile and context-adjusted performance"],
            ["Boundary Top 10", "Official Top-10 player below 75 percent inclusion in at least one bootstrap mode"],
        ],
        widths=[1.55, 5.15],
        aligns=["left", "left"],
        font_size=8.3,
    )
    add_heading(doc, "Submission consistency check", 2)
    add_body(doc, "The player names and rank order in this report must match the Unstop dropdown selections exactly. Use the two official ranking tables as the submission source of truth.")

    add_section_break(doc, "Technical scoring rules", "Details needed to reproduce the ratings")
    add_heading(doc, "Outcome records and attribution", 2)
    add_body(doc, "Eligible batting records include rows with no recorded extras type, byes and leg-byes. Wides, oversteps and other extras types are excluded from batting metrics. Only batter runs count toward scoring; byes and leg-byes do not become batter runs. Survival attributes a dismissal only when the dismissed player ID matches the striker ID. A wicket record with no dismissed-player ID is excluded from the survival outcome.")
    add_body(doc, "Bowling wicket rates use all delivery records. Only Caught, Bowled, LBW, Stump and Hit Wicket dismissals count as bowler wickets; run outs and other dismissals do not. Run suppression uses records with no extras type and compares expected batter runs with observed batter runs. All rates use recorded deliveries rather than an inferred legal-ball denominator.")
    add_heading(doc, "Stages and benchmark fallback", 2)
    add_body(doc, "Powerplay covers source overs 1 to 6, Middle covers 7 to 15, and Death covers 16 to 20. The exact source over is the first benchmark choice; stage is a fallback rather than three separately ranked player lists. Outcome benchmarks require at least 100 records at format, innings, over and pressure category. If sparse, use format, innings, stage and pressure category, then format, innings and pressure category. Formats never pool. Unavailable observations are not assigned an expected outcome of zero.")
    add_body(doc, "The Phase 3 wicket-state benchmark excludes the entire current match. Phase 4 outcome benchmarks initially include the evaluated player; the Phase 5 leave-one-player-out test measures that self-influence. The nested bootstrap rebuilds Phase 4 outcome benchmarks while keeping the Phase 3 pressure definition fixed.")
    add_heading(doc, "Shrinkage and continuous response", 2)
    add_body(doc, "Shrinkage multiplies a raw metric by n divided by n plus k, where n is the player's High-pressure record count and k is the locked shrinkage constant. Bowling run-control metrics use High-pressure clean-record counts. Each pressure gradient is the least-squares slope of the delivery outcome residual on the pressure percentile across the player's available records, expressed per 100 records before shrinkage.")
    add_heading(doc, "Exact weights", 2)
    add_table(doc, ["Metric", "Batting", "Bowling"], [
        ["Scoring quality or wicket quality", "45%", "45%"],
        ["Survival quality or run suppression", "25%", "30%"],
        ["Scoring response or wicket response", "20%", "15%"],
        ["Survival response or run-control response", "10%", "10%"],
    ], widths=[4.6, 1.0, 1.0], aligns=["left", "center", "center"], font_size=8.5)
    add_body(doc, "Normalization is repeated within the Reliable role-format pool in each bootstrap replicate and deterministic scenario. IPL and T20I matches are drawn separately: 357 IPL and 432 T20I matches per replicate. Seeds are 20261114 for the fixed bootstrap and 20261115 for the nested bootstrap.")

    add_section_break(doc, "Qualifying player samples", "Evidence volume used by each selection")
    format_rows = pd.read_csv(ROOT / "phase6_outputs" / "phase6_selected_format_evidence.csv")
    used_rows = format_rows[format_rows.used_in_official_score.eq(True)].sort_values(["role", "rank", "format_group"])
    samples = []
    for r in used_rows.itertuples():
        samples.append([r.role, r.player_name, r.format_group, str(int(r.high_records)), str(int(r.high_matches)), str(int(r.ordinary_records))])
    add_table(doc, ["Role", "Player", "Format", "High records", "High matches", "Ordinary records"], samples,
              widths=[0.65, 2.0, 0.65, 1.05, 1.05, 1.2], aligns=["center", "left", "center", "center", "center", "center"], font_size=8.1)
    add_source_note(doc, "Source: Phase 6 selected-format evidence. Counts follow the role-specific record definitions above; they are not inferred legal balls.")

    # Core properties
    doc.core_properties.title = "SupeRR Selector Season 2 Methodology Report"
    doc.core_properties.subject = "Pressure-performance rankings for IPL and T20I players from 2022 to 2026"
    doc.core_properties.keywords = "cricket, IPL, T20I, pressure, Rajasthan Royals, player rankings"
    doc.core_properties.comments = "Phase 7D editable methodology report"

    doc.save(OUTPUT)
    return OUTPUT


if __name__ == "__main__":
    output = build_report()
    print(output)
