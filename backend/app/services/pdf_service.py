import os
from typing import Dict, Any, List, Optional
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
)

from app.core.logging import logger

PRIMARY_COLOR = colors.HexColor("#4F46E5")
SECONDARY_COLOR = colors.HexColor("#6366F1")
ACCENT_COLOR = colors.HexColor("#EEF2FF")
NAVY_COLOR = colors.HexColor("#0F172A")
SLATE_COLOR = colors.HexColor("#475569")
MUTED_COLOR = colors.HexColor("#64748B")
BORDER_COLOR = colors.HexColor("#E2E8F0")
LIGHT_BG = colors.HexColor("#F8FAFC")
SUCCESS_COLOR = colors.HexColor("#0F766E")
WARNING_COLOR = colors.HexColor("#F59E0B")
RISK_COLOR = colors.HexColor("#DC2626")
WHITE = colors.white


def build_contextual_executive_summary(startup_info: Dict[str, Any], discovery: Dict[str, Any], validation: Dict[str, Any]) -> str:
    """Build a tailored executive summary from the startup inputs and agent analysis."""
    founder_name = startup_info.get("founder_name") or "the founder"
    idea = startup_info.get("idea") or "this venture"
    industry = startup_info.get("industry") or "the target sector"
    country = startup_info.get("country") or "the selected market"
    state = startup_info.get("state") or ""
    district = startup_info.get("district") or ""
    budget = startup_info.get("budget") or "a lean budget"
    stage = startup_info.get("stage") or "an early stage"
    target_market = startup_info.get("target_market") or "the intended customer base"
    location = ", ".join([part for part in [district, state, country] if part])

    problem = discovery.get("problem") or "a meaningful operating challenge"
    solution = discovery.get("solution") or "a focused software-led response"
    validation_reasoning = validation.get("reasoning") or "the concept demonstrates credible early traction"
    validation_score = validation.get("validation_score", 0)
    feasibility = validation.get("feasibility", 0)

    location_phrase = f" in {location}" if location else f" in {country}"
    return (
        f"{founder_name} is building {idea} as a tailored venture for {industry}{location_phrase}. "
        f"The product addresses {problem} by delivering {solution}, with a go-to-market emphasis on {target_market} "
        f"and a launch plan calibrated for a {budget} budget at the {stage} stage. "
        f"The current validation signal is strong, with a {validation_score}/100 validation score and {feasibility}/100 feasibility, "
        f"supported by the insight that {validation_reasoning}."
    )


def _safe_text(value: Any, fallback: str = "N/A") -> str:
    if value is None:
        return fallback
    if isinstance(value, str):
        text = value.strip()
        return text if text else fallback
    return str(value)


def _safe_list(value: Any) -> List[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, tuple):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        cleaned = [part.strip() for part in value.split("|") if part.strip()]
        return cleaned or [_safe_text(value)]
    return []


def _build_paragraph(text: Any, style: ParagraphStyle) -> Paragraph:
    return Paragraph(escape(_safe_text(text, "N/A")), style)


def _build_section_title(title: str, subtitle: Optional[str] = None, icon: str = "✦") -> List[Any]:
    lines = [Paragraph(f"{icon} {escape(title)}", ParagraphStyle("SectionTitle", fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=NAVY_COLOR, spaceAfter=4, keepWithNext=True))]
    if subtitle:
        lines.append(Paragraph(escape(subtitle), ParagraphStyle("SectionSubtitle", fontName="Helvetica", fontSize=9, leading=12, textColor=MUTED_COLOR, spaceAfter=10, keepWithNext=True)))
    return lines


def _build_highlight_card(title: str, body: str, accent: Any = PRIMARY_COLOR) -> Table:
    data = [[
        Paragraph(f"<b>{escape(title)}</b><br/><br/>{escape(body)}", ParagraphStyle("CardText", parent=None, fontName="Helvetica", fontSize=9, leading=12, textColor=NAVY_COLOR, alignment=TA_LEFT))
    ]]
    table = Table(data, colWidths=[460], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ACCENT_COLOR),
        ("LINEABOVE", (0, 0), (-1, 0), 2.5, accent),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("PADDING", (0, 0), (-1, -1), 10),
    ]))
    return table


def _build_metric_table(rows: List[List[Any]], colWidths: Optional[List[float]] = None) -> Table:
    table = Table(rows, colWidths=colWidths or [180, 280], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("PADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return table


def _build_bullets(items: List[Any], style: ParagraphStyle, prefix: str = "•") -> List[Paragraph]:
    bullet_items = _safe_list(items)
    if not bullet_items:
        bullet_items = ["No data captured yet."]
    return [Paragraph(f"{prefix} {escape(item)}", style) for item in bullet_items]


def _build_score_chart(validation: Dict[str, Any]) -> Table:
    score_rows = []
    metrics = [
        ("Validation", validation.get("validation_score", 0), SUCCESS_COLOR),
        ("Feasibility", validation.get("feasibility", 0), PRIMARY_COLOR),
        ("Innovation", validation.get("innovation", 0), SECONDARY_COLOR),
    ]
    for label, value, color in metrics:
        bar_width = max(20, int(float(value) / 100 * 230))
        bar = Table([[Paragraph(escape(label), ParagraphStyle("MetricLabel", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=NAVY_COLOR)),
                      Table([[Paragraph(f"{int(value)}/100", ParagraphStyle("MetricValue", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=NAVY_COLOR))]], colWidths=[35], hAlign="RIGHT")]], colWidths=[80, 270], hAlign="LEFT")
        score_rows.append([
            Paragraph(escape(label), ParagraphStyle("MetricLabel", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=NAVY_COLOR)),
            Table([[
                Paragraph(f"{int(value)}/100", ParagraphStyle("MetricValue", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=NAVY_COLOR)),
                None
            ]], colWidths=[40, bar_width], hAlign="LEFT")
        ])
    # Build a simple bar table manually
    data = []
    for label, value, color in metrics:
        bar_width = max(20, int(float(value) / 100 * 220))
        data.append([
            Paragraph(escape(label), ParagraphStyle("MetricLabel", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=NAVY_COLOR)),
            Table([[Paragraph(f"{int(value)}/100", ParagraphStyle("MetricValue", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=NAVY_COLOR))]], colWidths=[35], hAlign="RIGHT"),
            Table([[Paragraph("", ParagraphStyle("MetricSpacer", fontName="Helvetica", fontSize=1, leading=1, textColor=WHITE))]], colWidths=[bar_width], hAlign="LEFT")
        ])
    table = Table(data, colWidths=[85, 45, 250], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("BACKGROUND", (2, 0), (2, 2), PRIMARY_COLOR),
        ("BACKGROUND", (2, 0), (2, 0), SUCCESS_COLOR),
        ("BACKGROUND", (2, 1), (2, 1), PRIMARY_COLOR),
        ("BACKGROUND", (2, 2), (2, 2), SECONDARY_COLOR),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return table


def _build_swot_matrix(startup_info: Dict[str, Any], discovery: Dict[str, Any], market: Dict[str, Any], competitor: Dict[str, Any], risk_data: Dict[str, Any]) -> Table:
    strengths = [
        _safe_text(startup_info.get("idea")),
        _safe_text(discovery.get("solution")),
        _safe_text(startup_info.get("industry")),
    ]
    weaknesses = [
        f"Budget constrained at {_safe_text(startup_info.get('budget'))}",
        "Early-stage execution risk and limited operating history",
        "Market education may be required in early adoption phases",
    ]
    opportunities = [
        _safe_text(market.get("industry_specific_market"), "Emerging market demand"),
        _safe_text(competitor.get("gap_analysis"), "White-space opportunity"),
        f"Strategic expansion potential in {_safe_text(startup_info.get('country'))}",
    ]
    threats = [
        _safe_text(risk_data.get("market_risk"), "Competitive response and saturation"),
        _safe_text(risk_data.get("financial_risk"), "Funding pressure and runway constraints"),
        _safe_text(risk_data.get("technical_risk"), "Delivery and scaling complexity"),
    ]
    rows = [
        [Paragraph("<b>Strengths</b>", ParagraphStyle("CellHead", fontName="Helvetica-Bold", fontSize=9, leading=11, textColor=SUCCESS_COLOR)),
         Paragraph("<b>Weaknesses</b>", ParagraphStyle("CellHead", fontName="Helvetica-Bold", fontSize=9, leading=11, textColor=RISK_COLOR))],
        [Paragraph("<br/>".join([f"• {escape(item)}" for item in strengths]), ParagraphStyle("CellBody", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)),
         Paragraph("<br/>".join([f"• {escape(item)}" for item in weaknesses]), ParagraphStyle("CellBody", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR))],
        [Paragraph("<b>Opportunities</b>", ParagraphStyle("CellHead", fontName="Helvetica-Bold", fontSize=9, leading=11, textColor=SUCCESS_COLOR)),
         Paragraph("<b>Threats</b>", ParagraphStyle("CellHead", fontName="Helvetica-Bold", fontSize=9, leading=11, textColor=RISK_COLOR))],
        [Paragraph("<br/>".join([f"• {escape(item)}" for item in opportunities]), ParagraphStyle("CellBody", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)),
         Paragraph("<br/>".join([f"• {escape(item)}" for item in threats]), ParagraphStyle("CellBody", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR))],
    ]
    table = Table(rows, colWidths=[230, 230], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("BACKGROUND", (0, 0), (1, 0), ACCENT_COLOR),
        ("BACKGROUND", (0, 2), (1, 2), ACCENT_COLOR),
        ("BACKGROUND", (0, 1), (-1, -1), LIGHT_BG),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return table


def _build_business_model_canvas(business: Dict[str, Any]) -> Table:
    kp = Paragraph("<b>Key Partners</b><br/>" + "<br/>".join([f"• {escape(x)}" for x in _safe_list(business.get("key_partners"))]), ParagraphStyle("CanvasCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR))
    ka = Paragraph("<b>Key Activities</b><br/>" + "<br/>".join([f"• {escape(x)}" for x in _safe_list(business.get("activities"))]), ParagraphStyle("CanvasCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR))
    kr = Paragraph("<b>Key Resources</b><br/>" + "<br/>".join([f"• {escape(x)}" for x in _safe_list(business.get("key_resources"))]), ParagraphStyle("CanvasCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR))
    vp = Paragraph("<b>Value Propositions</b><br/>" + "<br/>".join([f"• {escape(x)}" for x in _safe_list(business.get("value_proposition"))]), ParagraphStyle("CanvasCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR))
    cr = Paragraph("<b>Customer Relationships</b><br/>" + escape(_safe_text(business.get("customer_relationships"), "Self-serve experience with guided support")), ParagraphStyle("CanvasCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR))
    ch = Paragraph("<b>Channels</b><br/>" + "<br/>".join([f"• {escape(x)}" for x in _safe_list(business.get("channels"))]), ParagraphStyle("CanvasCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR))
    cs = Paragraph("<b>Customer Segments</b><br/>" + "<br/>".join([f"• {escape(x)}" for x in _safe_list(business.get("customer_segments"))]), ParagraphStyle("CanvasCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR))
    cos = Paragraph("<b>Cost Structure</b><br/>" + escape(_safe_text(business.get("cost_structure"), "Operating costs centered on product, delivery, and growth")), ParagraphStyle("CanvasCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR))
    rev = Paragraph("<b>Revenue Streams</b><br/>" + escape(_safe_text(business.get("revenue_model"), "Subscription / service-based revenue")) + "<br/>" + escape(_safe_text(business.get("pricing_strategy"), "Tiered pricing and value-based packaging")), ParagraphStyle("CanvasCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR))

    canvas_data = [[kp, ka, vp, cr, cs], ["", kr, "", ch, ""], [cos, "", rev, "", ""]]
    table = Table(canvas_data, colWidths=[95, 95, 95, 95, 95], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("SPAN", (0, 0), (0, 1)),
        ("SPAN", (2, 0), (2, 1)),
        ("SPAN", (4, 0), (4, 1)),
        ("SPAN", (0, 2), (1, 2)),
        ("SPAN", (2, 2), (4, 2)),
    ]))
    return table


def _build_financial_section(financial_planning: Dict[str, Any]) -> List[Any]:
    items = []
    items.extend(_build_section_title("Financial Planning & Projections", "Budget discipline, runway visibility, and growth assumptions"))
    items.append(_build_highlight_card("Capital Strategy", _safe_text(financial_planning.get("cash_flow"), "Funding and cash management are designed to preserve runway and support the next milestone")))
    items.append(Spacer(1, 8))
    items.append(_build_metric_table([
        [Paragraph("<b>Monthly Burn</b>", ParagraphStyle("MetricHeader", fontName="Helvetica-Bold", fontSize=9, leading=11, textColor=NAVY_COLOR)), Paragraph(_safe_text(financial_planning.get("monthly_burn"), "TBD"), ParagraphStyle("MetricBody", fontName="Helvetica", fontSize=9, leading=11, textColor=NAVY_COLOR))],
        [Paragraph("<b>Runway</b>", ParagraphStyle("MetricHeader", fontName="Helvetica-Bold", fontSize=9, leading=11, textColor=NAVY_COLOR)), Paragraph(_safe_text(financial_planning.get("runway"), "TBD"), ParagraphStyle("MetricBody", fontName="Helvetica", fontSize=9, leading=11, textColor=NAVY_COLOR))],
        [Paragraph("<b>Break-even</b>", ParagraphStyle("MetricHeader", fontName="Helvetica-Bold", fontSize=9, leading=11, textColor=NAVY_COLOR)), Paragraph(_safe_text(financial_planning.get("break_even"), "TBD"), ParagraphStyle("MetricBody", fontName="Helvetica", fontSize=9, leading=11, textColor=NAVY_COLOR))],
    ], [145, 315]))
    items.append(Spacer(1, 8))
    items.extend(_build_section_title("Operating Expense Breakdown", None, icon="▣"))
    expense_rows = [[Paragraph("Expense Item", ParagraphStyle("TableHeader", fontName="Helvetica-Bold", fontSize=8.5, leading=10.5, textColor=WHITE)), Paragraph("Cost Type", ParagraphStyle("TableHeader", fontName="Helvetica-Bold", fontSize=8.5, leading=10.5, textColor=WHITE)), Paragraph("Estimated Cost", ParagraphStyle("TableHeader", fontName="Helvetica-Bold", fontSize=8.5, leading=10.5, textColor=WHITE))]]
    for exp_item in financial_planning.get("expenses", []):
        expense_rows.append([
            Paragraph(_safe_text(exp_item.get("item"), "N/A"), ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)),
            Paragraph(_safe_text(exp_item.get("cost_type"), "N/A"), ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)),
            Paragraph(_safe_text(exp_item.get("estimated_cost"), "N/A"), ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)),
        ])
    if len(expense_rows) == 1:
        expense_rows.append([Paragraph("No expense assumptions captured", ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)), Paragraph("N/A", ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)), Paragraph("N/A", ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR))])
    expense_table = Table(expense_rows, colWidths=[200, 120, 140], hAlign="LEFT")
    expense_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY_COLOR),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("BACKGROUND", (0, 1), (-1, -1), LIGHT_BG),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    items.append(expense_table)
    items.append(Spacer(1, 8))
    items.extend(_build_section_title("5-Year Revenue Projections", None, icon="▣"))
    forecast_rows = [[Paragraph("Year", ParagraphStyle("TableHeader", fontName="Helvetica-Bold", fontSize=8.5, leading=10.5, textColor=WHITE)), Paragraph("Projected Revenue", ParagraphStyle("TableHeader", fontName="Helvetica-Bold", fontSize=8.5, leading=10.5, textColor=WHITE))]]
    for forecast_item in financial_planning.get("revenue_projection", []):
        forecast_rows.append([
            Paragraph(_safe_text(forecast_item.get("year"), "N/A"), ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)),
            Paragraph(_safe_text(forecast_item.get("amount"), "N/A"), ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)),
        ])
    if len(forecast_rows) == 1:
        forecast_rows.append([Paragraph("Year 1", ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)), Paragraph("TBD", ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR))])
    forecast_table = Table(forecast_rows, colWidths=[140, 320], hAlign="LEFT")
    forecast_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY_COLOR),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("BACKGROUND", (0, 1), (-1, -1), LIGHT_BG),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    items.append(forecast_table)
    return items


def _build_risk_section(risk_data: Dict[str, Any]) -> List[Any]:
    items = []
    items.extend(_build_section_title("Risk Assessment Matrix", "Risk posture, mitigation steps, and governing assumptions"))
    rows = [[Paragraph("Risk Category", ParagraphStyle("TableHeader", fontName="Helvetica-Bold", fontSize=8.5, leading=10.5, textColor=WHITE)), Paragraph("Assessment", ParagraphStyle("TableHeader", fontName="Helvetica-Bold", fontSize=8.5, leading=10.5, textColor=WHITE))]]
    rows.extend([
        [Paragraph("Technical", ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)), Paragraph(_safe_text(risk_data.get("technical_risk"), "Monitor implementation complexity and delivery dependencies"), ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR))],
        [Paragraph("Market", ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)), Paragraph(_safe_text(risk_data.get("market_risk"), "Maintain pricing flexibility and customer-response loops"), ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR))],
        [Paragraph("Financial", ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)), Paragraph(_safe_text(risk_data.get("financial_risk"), "Preserve runway and test capital efficiency"), ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR))],
        [Paragraph("Legal", ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)), Paragraph(_safe_text(risk_data.get("legal_risk"), "Stay aligned with local compliance obligations"), ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR))],
    ])
    table = Table(rows, colWidths=[120, 340], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY_COLOR),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("BACKGROUND", (0, 1), (-1, -1), LIGHT_BG),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    items.append(table)
    items.append(Spacer(1, 8))
    items.append(Paragraph("<b>Mitigation Priorities</b>", ParagraphStyle("SectionSubHead", fontName="Helvetica-Bold", fontSize=10, leading=12, textColor=NAVY_COLOR, keepWithNext=True)))
    items.extend(_build_bullets(risk_data.get("mitigation", []), ParagraphStyle("Bullet", fontName="Helvetica", fontSize=9, leading=12, textColor=NAVY_COLOR, leftIndent=12, bulletIndent=0, firstLineIndent=0, spaceAfter=4)))
    return items


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and draw total page count, running headers, and footers."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count: int):
        self.saveState()
        width, height = letter
        if self._pageNumber == 1:
            self.setFillColor(NAVY_COLOR)
            self.rect(0, 0, 32, height, fill=True, stroke=False)
            self.setFillColor(PRIMARY_COLOR)
            self.rect(32, 0, 12, height, fill=True, stroke=False)
            self.restoreState()
            return

        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(PRIMARY_COLOR)
        self.drawString(54, height - 40, "FOUNDERAI")

        self.setFont("Helvetica", 8)
        self.setFillColor(MUTED_COLOR)
        self.drawRightString(width - 54, height - 40, "AI STARTUP LAUNCH PACKAGE")

        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(54, height - 46, width - 54, height - 46)
        self.line(54, 55, width - 54, 55)

        self.setFont("Helvetica", 8)
        self.setFillColor(MUTED_COLOR)
        self.drawString(54, 40, "Confidential Document - For Internal Use Only")
        self.drawRightString(width - 54, 40, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


class PDFService:
    @staticmethod
    def generate_startup_report(state: Dict[str, Any], output_path: str) -> str:
        """Generate a polished multi-page startup launch package PDF from the graph state."""
        logger.info(f"PDFService: Generating PDF report to {output_path}...")

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            leftMargin=54,
            rightMargin=54,
            topMargin=72,
            bottomMargin=72,
        )

        styles = getSampleStyleSheet()

        h1_style = ParagraphStyle(
            "Heading1_Custom",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=NAVY_COLOR,
            spaceBefore=14,
            spaceAfter=8,
            keepWithNext=True,
            outlineLevel=1,
        )
        h2_style = ParagraphStyle(
            "Heading2_Custom",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=PRIMARY_COLOR,
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=True,
        )
        body_style = ParagraphStyle(
            "Body_Custom",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.5,
            textColor=NAVY_COLOR,
            spaceAfter=7,
            alignment=TA_JUSTIFY,
        )
        bullet_style = ParagraphStyle(
            "Bullet_Custom",
            parent=body_style,
            leftIndent=14,
            firstLineIndent=-8,
            spaceAfter=4,
        )
        cover_title_style = ParagraphStyle(
            "CoverTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=28,
            leading=32,
            textColor=NAVY_COLOR,
            spaceAfter=8,
            alignment=TA_LEFT,
        )
        cover_subtitle_style = ParagraphStyle(
            "CoverSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=MUTED_COLOR,
            spaceAfter=18,
            alignment=TA_LEFT,
        )
        meta_label_style = ParagraphStyle(
            "MetaLabel",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            textColor=NAVY_COLOR,
            alignment=TA_LEFT,
        )
        meta_value_style = ParagraphStyle(
            "MetaValue",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=NAVY_COLOR,
            alignment=TA_LEFT,
        )

        story: List[Any] = []

        startup_info = state.get("startup") or {}
        discovery = (state.get("discovery") or {}).get("data") or {}
        validation = (state.get("validation") or {}).get("data") or {}
        market = (state.get("market") or {}).get("data") or {}
        competitor = (state.get("competitors") or {}).get("data") or {}
        business = (state.get("business_model") or {}).get("data") or {}
        financial_planning = (state.get("financial") or state.get("financial_planning") or {}).get("data") or {}
        legal = (state.get("legal") or state.get("registration") or {}).get("data") or {}
        funding = (state.get("funding") or {}).get("data") or {}
        roadmap_data = (state.get("roadmap") or {}).get("data") or {}
        risk_data = (state.get("risk") or {}).get("data") or {}

        # Cover page
        story.append(Spacer(1, 0.4 * inch))
        story.append(Paragraph("FounderAI", ParagraphStyle("Logo", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=16, leading=18, textColor=PRIMARY_COLOR, spaceAfter=10, alignment=TA_LEFT)))
        story.append(Paragraph("Startup Launch Package", cover_title_style))
        story.append(Paragraph("A premium investor-ready blueprint for validating, positioning, and launching the venture.", cover_subtitle_style))
        story.append(Spacer(1, 0.15 * inch))

        meta_rows = [
            [Paragraph("<b>Startup Name</b>", meta_label_style), Paragraph(_safe_text(startup_info.get("idea"), "N/A"), meta_value_style)],
            [Paragraph("<b>Founder</b>", meta_label_style), Paragraph(_safe_text(startup_info.get("founder_name"), "N/A"), meta_value_style)],
            [Paragraph("<b>Industry</b>", meta_label_style), Paragraph(_safe_text(startup_info.get("industry"), "N/A"), meta_value_style)],
            [Paragraph("<b>Location</b>", meta_label_style), Paragraph(_safe_text(startup_info.get("country"), "N/A"), meta_value_style)],
            [Paragraph("<b>Stage</b>", meta_label_style), Paragraph(_safe_text(startup_info.get("stage"), "N/A"), meta_value_style)],
            [Paragraph("<b>Budget</b>", meta_label_style), Paragraph(_safe_text(startup_info.get("budget"), "N/A"), meta_value_style)],
        ]
        meta_table = Table(meta_rows, colWidths=[120, 340], hAlign="LEFT")
        meta_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFF")),
            ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ("PADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 0.3 * inch))
        story.append(Paragraph("Generated dynamically by FounderAI’s multi-agent analysis workflow.", ParagraphStyle("Footnote", parent=styles["Normal"], fontName="Helvetica", fontSize=8, leading=10, textColor=MUTED_COLOR, alignment=TA_LEFT)))
        story.append(PageBreak())

        # Table of contents
        story.extend(_build_section_title("Table of Contents", "Executive summary, market view, financial plan, and launch priorities"))
        toc_rows = [
            [Paragraph("1. Executive Summary", ParagraphStyle("TOCItem", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=NAVY_COLOR)), Paragraph("2", ParagraphStyle("TOCItem", fontName="Helvetica", fontSize=9, leading=12, textColor=MUTED_COLOR))],
            [Paragraph("2. Validation", ParagraphStyle("TOCItem", fontName="Helvetica", fontSize=9, leading=12, textColor=NAVY_COLOR)), Paragraph("3", ParagraphStyle("TOCItem", fontName="Helvetica", fontSize=9, leading=12, textColor=MUTED_COLOR))],
            [Paragraph("3. Market Research", ParagraphStyle("TOCItem", fontName="Helvetica", fontSize=9, leading=12, textColor=NAVY_COLOR)), Paragraph("4", ParagraphStyle("TOCItem", fontName="Helvetica", fontSize=9, leading=12, textColor=MUTED_COLOR))],
            [Paragraph("4. SWOT", ParagraphStyle("TOCItem", fontName="Helvetica", fontSize=9, leading=12, textColor=NAVY_COLOR)), Paragraph("5", ParagraphStyle("TOCItem", fontName="Helvetica", fontSize=9, leading=12, textColor=MUTED_COLOR))],
            [Paragraph("5. Business Model Canvas", ParagraphStyle("TOCItem", fontName="Helvetica", fontSize=9, leading=12, textColor=NAVY_COLOR)), Paragraph("6", ParagraphStyle("TOCItem", fontName="Helvetica", fontSize=9, leading=12, textColor=MUTED_COLOR))],
            [Paragraph("6. Funding Strategy", ParagraphStyle("TOCItem", fontName="Helvetica", fontSize=9, leading=12, textColor=NAVY_COLOR)), Paragraph("7", ParagraphStyle("TOCItem", fontName="Helvetica", fontSize=9, leading=12, textColor=MUTED_COLOR))],
            [Paragraph("7. Financial Planning", ParagraphStyle("TOCItem", fontName="Helvetica", fontSize=9, leading=12, textColor=NAVY_COLOR)), Paragraph("8", ParagraphStyle("TOCItem", fontName="Helvetica", fontSize=9, leading=12, textColor=MUTED_COLOR))],
            [Paragraph("8. Risk Assessment", ParagraphStyle("TOCItem", fontName="Helvetica", fontSize=9, leading=12, textColor=NAVY_COLOR)), Paragraph("9", ParagraphStyle("TOCItem", fontName="Helvetica", fontSize=9, leading=12, textColor=MUTED_COLOR))],
            [Paragraph("9. Final Recommendations", ParagraphStyle("TOCItem", fontName="Helvetica", fontSize=9, leading=12, textColor=NAVY_COLOR)), Paragraph("10", ParagraphStyle("TOCItem", fontName="Helvetica", fontSize=9, leading=12, textColor=MUTED_COLOR))],
        ]
        toc_table = Table(toc_rows, colWidths=[420, 40], hAlign="LEFT")
        toc_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
            ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(toc_table)
        story.append(PageBreak())

        # Executive summary
        story.extend(_build_section_title("Executive Summary", "A concise strategic overview of the venture, the problem it solves, and why the opportunity is compelling"))
        story.append(_build_highlight_card("Venture Narrative", build_contextual_executive_summary(startup_info, discovery, validation)))
        story.append(Spacer(1, 8))
        story.append(Paragraph("<b>Validation Snapshot</b>", h2_style))
        story.append(_build_score_chart(validation))
        story.append(Spacer(1, 8))
        story.append(Paragraph("<b>Strategic Indicators</b>", h2_style))
        story.append(_build_metric_table([
            [Paragraph("<b>Target Customer</b>", ParagraphStyle("MetricHeader", fontName="Helvetica-Bold", fontSize=9, leading=11, textColor=NAVY_COLOR)), Paragraph(_safe_text(startup_info.get("target_market"), "N/A"), ParagraphStyle("MetricBody", fontName="Helvetica", fontSize=9, leading=11, textColor=NAVY_COLOR))],
            [Paragraph("<b>Country</b>", ParagraphStyle("MetricHeader", fontName="Helvetica-Bold", fontSize=9, leading=11, textColor=NAVY_COLOR)), Paragraph(_safe_text(startup_info.get("country"), "N/A"), ParagraphStyle("MetricBody", fontName="Helvetica", fontSize=9, leading=11, textColor=NAVY_COLOR))],
            [Paragraph("<b>Budget</b>", ParagraphStyle("MetricHeader", fontName="Helvetica-Bold", fontSize=9, leading=11, textColor=NAVY_COLOR)), Paragraph(_safe_text(startup_info.get("budget"), "N/A"), ParagraphStyle("MetricBody", fontName="Helvetica", fontSize=9, leading=11, textColor=NAVY_COLOR))],
        ], [145, 315]))
        story.append(PageBreak())

        # Validation and market
        story.extend(_build_section_title("Validation", "Signals, feasibility, and the evidence behind the concept"))
        story.append(Paragraph(_safe_text(validation.get("reasoning"), "The concept is progressing well with positive validation signals."), body_style))
        story.append(Paragraph("<b>Key Validation Inputs</b>", h2_style))
        story.extend(_build_bullets([
            f"Validation score: {validation.get('validation_score', 0)}/100",
            f"Feasibility score: {validation.get('feasibility', 0)}/100",
            f"Innovation score: {validation.get('innovation', 0)}/100",
            f"Risk score: {validation.get('risk', 0)}/100",
        ], bullet_style))
        story.append(PageBreak())

        story.extend(_build_section_title("Market Research", "Sector context, market sizing, and commercial opportunity"))
        story.append(Paragraph(_safe_text(market.get("industry_specific_market"), "Market review is being finalized."), body_style))
        story.append(Paragraph("<b>Market Sizing</b>", h2_style))
        market_rows = [[Paragraph("Layer", ParagraphStyle("TableHeader", fontName="Helvetica-Bold", fontSize=8.5, leading=10.5, textColor=WHITE)), Paragraph("Assessment", ParagraphStyle("TableHeader", fontName="Helvetica-Bold", fontSize=8.5, leading=10.5, textColor=WHITE))],
                       [Paragraph("TAM", ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)), Paragraph(_safe_text(market.get("TAM"), "TBD"), ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR))],
                       [Paragraph("SAM", ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)), Paragraph(_safe_text(market.get("SAM"), "TBD"), ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR))],
                       [Paragraph("SOM", ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)), Paragraph(_safe_text(market.get("SOM"), "TBD"), ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR))]]
        market_table = Table(market_rows, colWidths=[90, 350], hAlign="LEFT")
        market_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), PRIMARY_COLOR),
            ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ("BACKGROUND", (0, 1), (-1, -1), LIGHT_BG),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(market_table)
        story.append(Spacer(1, 8))
        story.append(Paragraph("<b>Competitive Landscape</b>", h2_style))
        story.append(Paragraph(_safe_text(competitor.get("pricing"), "Pricing and positioning remain to be tested dynamically."), body_style))
        comp_rows = [[Paragraph("Competitor", ParagraphStyle("TableHeader", fontName="Helvetica-Bold", fontSize=8.5, leading=10.5, textColor=WHITE)), Paragraph("Gap", ParagraphStyle("TableHeader", fontName="Helvetica-Bold", fontSize=8.5, leading=10.5, textColor=WHITE)), Paragraph("Threat", ParagraphStyle("TableHeader", fontName="Helvetica-Bold", fontSize=8.5, leading=10.5, textColor=WHITE))]]
        for c in competitor.get("real_competitors", []):
            comp_rows.append([Paragraph(_safe_text(c.get("name"), "N/A"), ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)), Paragraph(_safe_text(c.get("gap"), "N/A"), ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)), Paragraph(_safe_text(c.get("threat_level"), "N/A"), ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR))])
        if len(comp_rows) == 1:
            comp_rows.append([Paragraph("No direct competitors captured", ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)), Paragraph("N/A", ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)), Paragraph("N/A", ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR))])
        comp_table = Table(comp_rows, colWidths=[120, 220, 100], hAlign="LEFT")
        comp_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), PRIMARY_COLOR),
            ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ("BACKGROUND", (0, 1), (-1, -1), LIGHT_BG),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(comp_table)
        story.append(PageBreak())

        story.extend(_build_section_title("SWOT", "A balanced view of the venture’s strategic posture"))
        story.append(_build_swot_matrix(startup_info, discovery, market, competitor, risk_data))
        story.append(PageBreak())

        story.extend(_build_section_title("Business Model Canvas", "How the venture creates, delivers, and captures value"))
        story.append(_build_business_model_canvas(business))
        story.append(PageBreak())

        story.extend(_build_section_title("Marketing Strategy", "Positioning, engagement, and route-to-market plan"))
        story.append(Paragraph(_safe_text(competitor.get("gap_analysis"), "The venture should emphasize a differentiated customer value proposition and disciplined positioning."), body_style))
        story.append(Paragraph("<b>Recommended Launch Priorities</b>", h2_style))
        story.extend(_build_bullets([
            f"Anchor the brand around {startup_info.get('idea', 'the venture')}",
            f"Prioritize the {startup_info.get('target_market', 'target customer')} segment for early adoption",
            _safe_text(competitor.get("pricing"), "Use a value-led pricing strategy to differentiate from incumbents"),
        ], bullet_style))
        story.append(PageBreak())

        story.extend(_build_section_title("Funding Strategy", "Capital approach, investor targeting, and bootstrapping logic"))
        story.append(Paragraph(_safe_text(funding.get("recommended_funding"), "A staged capital approach is recommended."), body_style))
        story.append(Paragraph(_safe_text(funding.get("bootstrap_strategy"), "Bootstrap with a lean operating model and deliberate milestone-based growth."), body_style))
        story.append(Paragraph("<b>Potential Capital Sources</b>", h2_style))
        story.extend(_build_bullets(funding.get("recommended_investors", []), bullet_style))
        story.append(PageBreak())

        story.extend(_build_section_title("Legal & Compliance", "Corporate setup, permits, and regulatory alignment"))
        story.append(Paragraph("<b>Recommended Entity</b>", h2_style))
        story.append(Paragraph(_safe_text(legal.get("entity_type"), "Entity selection should be validated with local counsel."), body_style))
        story.append(Paragraph("<b>Country Requirements</b>", h2_style))
        story.append(Paragraph(_safe_text(legal.get("country_specific_requirements"), "Local regulatory requirements should be reviewed before launch."), body_style))
        story.append(Paragraph("<b>Key Requirements</b>", h2_style))
        story.extend(_build_bullets(legal.get("licenses", []), bullet_style))
        story.append(PageBreak())

        story.extend(_build_section_title("Roadmap", "Execution milestones for the next 30/60/90 days"))
        roadmap_rows = [[Paragraph("30 Days", ParagraphStyle("TableHeader", fontName="Helvetica-Bold", fontSize=8.5, leading=10.5, textColor=WHITE)), Paragraph("60 Days", ParagraphStyle("TableHeader", fontName="Helvetica-Bold", fontSize=8.5, leading=10.5, textColor=WHITE)), Paragraph("90 Days", ParagraphStyle("TableHeader", fontName="Helvetica-Bold", fontSize=8.5, leading=10.5, textColor=WHITE))]]
        roadmap_rows.append([
            Paragraph("<br/>".join([f"• {escape(item)}" for item in roadmap_data.get("30_day_plan", [])]), ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)),
            Paragraph("<br/>".join([f"• {escape(item)}" for item in roadmap_data.get("60_day_plan", [])]), ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)),
            Paragraph("<br/>".join([f"• {escape(item)}" for item in roadmap_data.get("90_day_plan", [])]), ParagraphStyle("TableCell", fontName="Helvetica", fontSize=8.5, leading=10.5, textColor=NAVY_COLOR)),
        ])
        roadmap_table = Table(roadmap_rows, colWidths=[150, 150, 150], hAlign="LEFT")
        roadmap_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), PRIMARY_COLOR),
            ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ("BACKGROUND", (0, 1), (-1, -1), LIGHT_BG),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(roadmap_table)
        story.append(PageBreak())

        story.extend(_build_section_title("Final Recommendations", "Practical next steps and execution priorities"))
        story.append(_build_highlight_card("Launch Focus", "Prioritize validation, disciplined execution, and stakeholder confidence through a focused first 90 days of product, market, and financial execution."))
        story.append(Spacer(1, 8))
        story.extend(_build_bullets([
            "Turn the concept into a focused MVP with measurable customer feedback loops",
            "Protect runway with a strict milestone-based budget and reporting cadence",
            "Use early traction to refine positioning, pricing, and informed fundraising strategy",
        ], bullet_style))

        # Financial and risk sections
        story.append(PageBreak())
        story.extend(_build_financial_section(financial_planning))
        story.append(PageBreak())
        story.extend(_build_risk_section(risk_data))

        doc.build(story, canvasmaker=NumberedCanvas)
        logger.info("PDFService: PDF generated successfully!")
        return output_path
