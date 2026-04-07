"""
KHA0SYS3 - Strategy Storytelling PDF Generator
Genera un documento PDF completo, divertido y profesional
sobre la estrategia de trading Opening Range Breakout.
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import (
    HexColor, white, black, Color
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Polygon
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics import renderPDF
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import math
import random

# ============================================================
# COLORES Y TEMA
# ============================================================
DARK_BG = HexColor('#0D1117')
CARD_BG = HexColor('#161B22')
ACCENT_GREEN = HexColor('#00D68F')
ACCENT_BLUE = HexColor('#58A6FF')
ACCENT_PURPLE = HexColor('#BC8CF2')
ACCENT_ORANGE = HexColor('#F0883E')
ACCENT_RED = HexColor('#F85149')
ACCENT_YELLOW = HexColor('#E3B341')
TEXT_PRIMARY = HexColor('#C9D1D9')
TEXT_SECONDARY = HexColor('#8B949E')
TEXT_WHITE = HexColor('#FFFFFF')
BORDER_COLOR = HexColor('#30363D')

# Colores claros para el PDF (fondo blanco)
BG_WHITE = HexColor('#FFFFFF')
BG_LIGHT = HexColor('#F6F8FA')
BG_CARD = HexColor('#F0F3F6')
BG_DARK_CARD = HexColor('#24292F')
TEXT_DARK = HexColor('#1F2328')
TEXT_MEDIUM = HexColor('#57606A')
TEXT_LIGHT = HexColor('#8B949E')
GREEN_DARK = HexColor('#1A7F37')
GREEN_LIGHT = HexColor('#DDF4E4')
BLUE_DARK = HexColor('#0969DA')
BLUE_LIGHT = HexColor('#DDF4FF')
PURPLE_DARK = HexColor('#8250DF')
ORANGE_DARK = HexColor('#BC4C00')
RED_DARK = HexColor('#CF222E')

# ============================================================
# ESTILOS
# ============================================================
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'CustomTitle', parent=styles['Title'],
    fontSize=28, leading=34, textColor=BG_DARK_CARD,
    spaceAfter=6, alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

subtitle_style = ParagraphStyle(
    'CustomSubtitle', parent=styles['Normal'],
    fontSize=14, leading=18, textColor=TEXT_MEDIUM,
    spaceAfter=20, alignment=TA_CENTER,
    fontName='Helvetica-Oblique'
)

chapter_style = ParagraphStyle(
    'ChapterTitle', parent=styles['Heading1'],
    fontSize=22, leading=28, textColor=BLUE_DARK,
    spaceBefore=30, spaceAfter=12,
    fontName='Helvetica-Bold',
    borderWidth=0, borderColor=BLUE_DARK,
    borderPadding=8
)

section_style = ParagraphStyle(
    'SectionTitle', parent=styles['Heading2'],
    fontSize=16, leading=20, textColor=PURPLE_DARK,
    spaceBefore=18, spaceAfter=8,
    fontName='Helvetica-Bold'
)

subsection_style = ParagraphStyle(
    'SubSection', parent=styles['Heading3'],
    fontSize=13, leading=16, textColor=GREEN_DARK,
    spaceBefore=12, spaceAfter=6,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody', parent=styles['Normal'],
    fontSize=10.5, leading=15, textColor=TEXT_DARK,
    spaceAfter=8, alignment=TA_JUSTIFY,
    fontName='Helvetica'
)

joke_style = ParagraphStyle(
    'JokeStyle', parent=styles['Normal'],
    fontSize=10, leading=14, textColor=PURPLE_DARK,
    spaceBefore=6, spaceAfter=10, alignment=TA_CENTER,
    fontName='Helvetica-Oblique',
    borderWidth=1, borderColor=HexColor('#E8DAFF'),
    borderPadding=8, backColor=HexColor('#F8F0FF'),
    borderRadius=4
)

callout_style = ParagraphStyle(
    'CalloutStyle', parent=styles['Normal'],
    fontSize=10, leading=14, textColor=BLUE_DARK,
    spaceBefore=6, spaceAfter=10, alignment=TA_LEFT,
    fontName='Helvetica',
    borderWidth=1, borderColor=BLUE_LIGHT,
    borderPadding=10, backColor=HexColor('#F0F8FF'),
    leftIndent=12, borderRadius=4
)

warning_style = ParagraphStyle(
    'WarningStyle', parent=styles['Normal'],
    fontSize=10, leading=14, textColor=ORANGE_DARK,
    spaceBefore=6, spaceAfter=10, alignment=TA_LEFT,
    fontName='Helvetica',
    borderWidth=1, borderColor=HexColor('#FFF1E5'),
    borderPadding=10, backColor=HexColor('#FFF8F0'),
    leftIndent=12
)

code_style = ParagraphStyle(
    'CodeStyle', parent=styles['Normal'],
    fontSize=9, leading=12, textColor=TEXT_DARK,
    spaceBefore=4, spaceAfter=8,
    fontName='Courier', backColor=BG_LIGHT,
    borderWidth=1, borderColor=BORDER_COLOR,
    borderPadding=8, leftIndent=8
)

metric_label = ParagraphStyle(
    'MetricLabel', parent=styles['Normal'],
    fontSize=8, leading=10, textColor=TEXT_MEDIUM,
    alignment=TA_CENTER, fontName='Helvetica'
)

metric_value = ParagraphStyle(
    'MetricValue', parent=styles['Normal'],
    fontSize=18, leading=22, textColor=BLUE_DARK,
    alignment=TA_CENTER, fontName='Helvetica-Bold'
)

footer_style = ParagraphStyle(
    'Footer', parent=styles['Normal'],
    fontSize=8, leading=10, textColor=TEXT_LIGHT,
    alignment=TA_CENTER, fontName='Helvetica'
)

small_style = ParagraphStyle(
    'Small', parent=styles['Normal'],
    fontSize=9, leading=12, textColor=TEXT_MEDIUM,
    spaceAfter=4, fontName='Helvetica'
)

table_header_style = ParagraphStyle(
    'TableHeader', parent=styles['Normal'],
    fontSize=8.5, leading=11, textColor=TEXT_WHITE,
    alignment=TA_CENTER, fontName='Helvetica-Bold'
)

table_cell_style = ParagraphStyle(
    'TableCell', parent=styles['Normal'],
    fontSize=8.5, leading=11, textColor=TEXT_DARK,
    alignment=TA_CENTER, fontName='Helvetica'
)

table_cell_left = ParagraphStyle(
    'TableCellLeft', parent=styles['Normal'],
    fontSize=8.5, leading=11, textColor=TEXT_DARK,
    alignment=TA_LEFT, fontName='Helvetica'
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def make_spacer(h=0.5):
    return Spacer(1, h * cm)

def make_hr():
    return HRFlowable(
        width="100%", thickness=1, color=HexColor('#E1E4E8'),
        spaceBefore=8, spaceAfter=8
    )

def make_joke(text):
    return Paragraph(f'<font size="12">&#128514;</font> {text}', joke_style)

def make_callout(text, icon="&#128161;"):
    return Paragraph(f'<font size="11">{icon}</font> {text}', callout_style)

def make_warning(text):
    return Paragraph(f'<font size="11">&#9888;</font> {text}', warning_style)

def make_metric_card(label, value, color=BLUE_DARK):
    vs = ParagraphStyle('mv', parent=metric_value, textColor=color)
    data = [[Paragraph(str(value), vs)], [Paragraph(label, metric_label)]]
    t = Table(data, colWidths=[4*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, HexColor('#E1E4E8')),
        ('TOPPADDING', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,-1), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t

def make_metrics_row(metrics):
    """metrics = [(label, value, color), ...]"""
    cards = [make_metric_card(l, v, c) for l, v, c in metrics]
    row = Table([cards], colWidths=[4.5*cm]*len(cards))
    row.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return row


def make_data_table(headers, rows, col_widths=None):
    """Create a styled data table."""
    hdr = [Paragraph(h, table_header_style) for h in headers]
    data = [hdr]
    for row in rows:
        data.append([Paragraph(str(c), table_cell_style) for c in row])

    if col_widths is None:
        col_widths = [None] * len(headers)

    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ('BACKGROUND', (0,0), (-1,0), BG_DARK_CARD),
        ('TEXTCOLOR', (0,0), (-1,0), TEXT_WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8.5),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('TOPPADDING', (0,0), (-1,0), 6),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#E1E4E8')),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 8.5),
        ('TOPPADDING', (0,1), (-1,-1), 4),
        ('BOTTOMPADDING', (0,1), (-1,-1), 4),
    ]
    # Alternate row colors
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0,i), (-1,i), BG_LIGHT))
        else:
            style_cmds.append(('BACKGROUND', (0,i), (-1,i), BG_WHITE))

    t.setStyle(TableStyle(style_cmds))
    return t


def draw_orb_diagram(width=460, height=200):
    """Draw an Opening Range Breakout diagram."""
    d = Drawing(width, height)

    # Background
    d.add(Rect(0, 0, width, height, fillColor=BG_LIGHT, strokeColor=None))

    # Price levels
    or_high_y = 140
    or_low_y = 80
    or_mid_y = 110
    tp_y = 170
    sl_y = 50

    # Opening Range box
    d.add(Rect(40, or_low_y, 120, or_high_y - or_low_y,
               fillColor=HexColor('#DDF4FF'), strokeColor=BLUE_DARK, strokeWidth=1.5))

    # Labels
    d.add(String(5, or_high_y - 4, 'OR High', fontSize=7, fontName='Helvetica', fillColor=BLUE_DARK))
    d.add(String(5, or_low_y - 4, 'OR Low', fontSize=7, fontName='Helvetica', fillColor=BLUE_DARK))
    d.add(String(5, tp_y - 4, 'TP', fontSize=7, fontName='Helvetica-Bold', fillColor=GREEN_DARK))
    d.add(String(5, sl_y - 4, 'SL', fontSize=7, fontName='Helvetica-Bold', fillColor=RED_DARK))

    # Dashed lines for TP and SL
    for x in range(40, width - 20, 6):
        d.add(Line(x, tp_y, x+3, tp_y, strokeColor=GREEN_DARK, strokeWidth=1))
        d.add(Line(x, sl_y, x+3, sl_y, strokeColor=RED_DARK, strokeWidth=1))

    # OR High/Low lines
    d.add(Line(40, or_high_y, width - 20, or_high_y, strokeColor=BLUE_DARK, strokeWidth=0.5, strokeDashArray=[3,3]))
    d.add(Line(40, or_low_y, width - 20, or_low_y, strokeColor=BLUE_DARK, strokeWidth=0.5, strokeDashArray=[3,3]))

    # Price action (breakout up)
    points_x = [50, 70, 90, 110, 130, 160, 180, 200, 220, 250, 280, 310, 340, 370, 400, 430]
    points_y = [100, 115, 95, 120, 105, 130, 142, 135, 148, 155, 145, 160, 155, 165, 168, 172]

    for i in range(len(points_x) - 1):
        color = GREEN_DARK if points_y[i+1] > or_high_y else BLUE_DARK
        d.add(Line(points_x[i], points_y[i], points_x[i+1], points_y[i+1],
                   strokeColor=color, strokeWidth=2))

    # Breakout arrow
    d.add(String(170, or_high_y + 8, 'BREAKOUT!', fontSize=9,
                 fontName='Helvetica-Bold', fillColor=GREEN_DARK))

    # Entry point
    d.add(Circle(160, or_high_y, 4, fillColor=ACCENT_GREEN, strokeColor=None))
    d.add(String(165, or_high_y + 15, 'BUY STOP', fontSize=7,
                 fontName='Helvetica-Bold', fillColor=GREEN_DARK))

    # TP hit
    d.add(Circle(430, tp_y, 5, fillColor=GREEN_DARK, strokeColor=None))
    d.add(String(390, tp_y + 8, 'TP HIT +0.8R', fontSize=7,
                 fontName='Helvetica-Bold', fillColor=GREEN_DARK))

    # Time labels
    d.add(String(70, 10, '07:00', fontSize=7, fontName='Helvetica', fillColor=TEXT_MEDIUM))
    d.add(String(50, 20, 'OR Window', fontSize=7, fontName='Helvetica-Oblique', fillColor=TEXT_MEDIUM))
    d.add(String(200, 10, '08:30', fontSize=7, fontName='Helvetica', fillColor=TEXT_MEDIUM))
    d.add(String(350, 10, '11:00', fontSize=7, fontName='Helvetica', fillColor=TEXT_MEDIUM))

    # Title
    d.add(String(140, height - 15, 'Opening Range Breakout - Ejemplo LONG',
                 fontSize=10, fontName='Helvetica-Bold', fillColor=TEXT_DARK))

    return d


def draw_risk_diagram(width=460, height=160):
    """Draw risk management flow diagram."""
    d = Drawing(width, height)
    d.add(Rect(0, 0, width, height, fillColor=BG_LIGHT, strokeColor=None))

    boxes = [
        (20, 90, 'Balance\n$10,000', BLUE_DARK),
        (120, 90, 'Risk 3.5%\n= $350', ORANGE_DARK),
        (220, 90, 'OR Width\n= SL dist', PURPLE_DARK),
        (320, 90, 'Lot Size\n= Risk/SL', GREEN_DARK),
        (420, 90, 'TRADE!', RED_DARK),
    ]

    for i, (x, y, text, color) in enumerate(boxes):
        d.add(Rect(x, y, 80, 45, fillColor=color, strokeColor=None, rx=5, ry=5))
        lines = text.split('\n')
        for j, line in enumerate(lines):
            d.add(String(x + 5, y + 28 - j*14, line, fontSize=8,
                         fontName='Helvetica-Bold', fillColor=TEXT_WHITE))
        if i < len(boxes) - 1:
            # Arrow
            ax = x + 82
            d.add(Line(ax, y+22, ax+16, y+22, strokeColor=TEXT_MEDIUM, strokeWidth=2))
            d.add(Polygon([ax+16, y+27, ax+22, y+22, ax+16, y+17],
                          fillColor=TEXT_MEDIUM, strokeColor=None))

    d.add(String(120, height - 15, 'Flujo de Gestion de Riesgo por Trade',
                 fontSize=10, fontName='Helvetica-Bold', fillColor=TEXT_DARK))

    # Bottom note
    d.add(String(50, 20, 'Si pierdes: -$350 (-1R)  |  Si ganas con TP 0.8x: +$280 (+0.8R)',
                 fontSize=8, fontName='Helvetica', fillColor=TEXT_MEDIUM))
    d.add(String(50, 8, 'Con 63% win rate: Expectativa = (0.63 x 0.8) - (0.37 x 1.0) = +0.134R por trade',
                 fontSize=8, fontName='Helvetica-Bold', fillColor=GREEN_DARK))

    return d


def draw_session_timeline(width=460, height=100):
    """Draw trading sessions timeline."""
    d = Drawing(width, height)
    d.add(Rect(0, 0, width, height, fillColor=BG_LIGHT, strokeColor=None))

    # Timeline base
    y = 40
    d.add(Line(20, y, width-20, y, strokeColor=TEXT_MEDIUM, strokeWidth=1))

    # Hours
    for h in range(0, 25, 3):
        x = 20 + (h / 24) * (width - 40)
        d.add(Line(x, y-4, x, y+4, strokeColor=TEXT_MEDIUM, strokeWidth=1))
        d.add(String(x-5, y-15, f'{h:02d}:00', fontSize=6, fontName='Helvetica', fillColor=TEXT_MEDIUM))

    # Sessions
    sessions = [
        (0, 8, 'Tokyo', HexColor('#FFDEE9'), HexColor('#C23373')),
        (7, 16, 'London', HexColor('#DEE9FF'), BLUE_DARK),
        (13.5, 22, 'New York', HexColor('#DEF7E5'), GREEN_DARK),
    ]

    for start, end, name, bg, fg in sessions:
        x1 = 20 + (start / 24) * (width - 40)
        x2 = 20 + (end / 24) * (width - 40)
        sy = y + 10 + sessions.index((start, end, name, bg, fg)) * 15
        d.add(Rect(x1, sy, x2-x1, 12, fillColor=bg, strokeColor=fg, strokeWidth=0.5, rx=3, ry=3))
        d.add(String(x1 + 5, sy + 2, f'{name} ({int(start):02d}:00-{int(end):02d}:00)',
                     fontSize=7, fontName='Helvetica-Bold', fillColor=fg))

    d.add(String(150, height - 12, 'Sesiones de Trading (UTC)',
                 fontSize=9, fontName='Helvetica-Bold', fillColor=TEXT_DARK))

    return d


def draw_equity_curve(width=460, height=200):
    """Draw a simulated equity curve."""
    d = Drawing(width, height)
    d.add(Rect(0, 0, width, height, fillColor=BG_LIGHT, strokeColor=None))

    # Generate simulated equity curve data
    random.seed(42)
    n_points = 100
    equity = [1000]
    for i in range(n_points - 1):
        # 63% win rate, 0.8R win, -1R loss, 3.5% risk
        win = random.random() < 0.63
        r = 0.8 if win else -1.0
        equity.append(equity[-1] * (1 + 0.035 * r))

    # Normalize to drawing coords
    min_eq = min(equity)
    max_eq = max(equity)
    margin_left = 50
    margin_bottom = 30
    margin_top = 25
    plot_w = width - margin_left - 20
    plot_h = height - margin_bottom - margin_top

    # Axes
    d.add(Line(margin_left, margin_bottom, margin_left, height - margin_top,
               strokeColor=TEXT_MEDIUM, strokeWidth=0.5))
    d.add(Line(margin_left, margin_bottom, width - 20, margin_bottom,
               strokeColor=TEXT_MEDIUM, strokeWidth=0.5))

    # Y-axis labels
    for i in range(5):
        val = min_eq + (max_eq - min_eq) * i / 4
        y_pos = margin_bottom + plot_h * i / 4
        d.add(String(5, y_pos - 3, f'${val:,.0f}', fontSize=6, fontName='Helvetica', fillColor=TEXT_MEDIUM))
        d.add(Line(margin_left, y_pos, width - 20, y_pos,
                   strokeColor=HexColor('#E1E4E8'), strokeWidth=0.3))

    # Plot line
    for i in range(len(equity) - 1):
        x1 = margin_left + (i / (n_points - 1)) * plot_w
        x2 = margin_left + ((i + 1) / (n_points - 1)) * plot_w
        y1 = margin_bottom + ((equity[i] - min_eq) / (max_eq - min_eq)) * plot_h
        y2 = margin_bottom + ((equity[i+1] - min_eq) / (max_eq - min_eq)) * plot_h
        d.add(Line(x1, y1, x2, y2, strokeColor=GREEN_DARK, strokeWidth=1.5))

    d.add(String(130, height - 12, 'Curva de Equity Simulada (100 trades, $1K inicio)',
                 fontSize=9, fontName='Helvetica-Bold', fillColor=TEXT_DARK))

    return d


def draw_win_rate_bars(width=460, height=180):
    """Draw win rate comparison bars for top assets."""
    d = Drawing(width, height)
    d.add(Rect(0, 0, width, height, fillColor=BG_LIGHT, strokeColor=None))

    assets = [
        ('GBPUSD\nLon 15m', 65.84, GREEN_DARK),
        ('USDJPY\nTok 15m', 62.04, BLUE_DARK),
        ('XAUUSD\nLon 15m', 62.02, HexColor('#DAA520')),
        ('NAS100\nPre 15m', 65.06, PURPLE_DARK),
        ('SP500\nPre 15m', 65.38, ORANGE_DARK),
        ('VIX\nNY 15m', 60.98, RED_DARK),
        ('BRENT\nLon 30m', 70.22, HexColor('#2E8B57')),
    ]

    bar_w = 45
    gap = 12
    total_w = len(assets) * (bar_w + gap) - gap
    start_x = (width - total_w) / 2
    base_y = 35

    for i, (name, wr, color) in enumerate(assets):
        x = start_x + i * (bar_w + gap)
        bar_h = (wr / 100) * 110
        d.add(Rect(x, base_y, bar_w, bar_h, fillColor=color, strokeColor=None, rx=3, ry=3))
        d.add(String(x + 5, base_y + bar_h + 3, f'{wr:.1f}%', fontSize=7,
                     fontName='Helvetica-Bold', fillColor=color))
        lines = name.split('\n')
        for j, line in enumerate(lines):
            d.add(String(x + 2, base_y - 12 - j * 9, line, fontSize=6,
                         fontName='Helvetica', fillColor=TEXT_MEDIUM))

    # 60% threshold line
    threshold_y = base_y + (60 / 100) * 110
    for x in range(int(start_x), int(start_x + total_w), 6):
        d.add(Line(x, threshold_y, x+3, threshold_y, strokeColor=RED_DARK, strokeWidth=0.8))
    d.add(String(start_x + total_w + 5, threshold_y - 3, '60%', fontSize=7,
                 fontName='Helvetica-Bold', fillColor=RED_DARK))

    d.add(String(120, height - 12, 'Win Rate por Activo (Top Setups - 15m)',
                 fontSize=9, fontName='Helvetica-Bold', fillColor=TEXT_DARK))

    return d


def draw_pie_assets(width=220, height=180):
    """Draw pie chart of asset classes."""
    d = Drawing(width, height)

    pie = Pie()
    pie.x = 40
    pie.y = 20
    pie.width = 120
    pie.height = 120
    pie.data = [7, 2, 3, 3, 1]  # Forex, Metals, Energy, Indices, Volatility
    pie.labels = ['Forex\n7 pares', 'Metales\n2', 'Energia\n3', 'Indices\n3', 'VIX\n1']

    colors = [BLUE_DARK, HexColor('#DAA520'), ORANGE_DARK, GREEN_DARK, RED_DARK]
    for i, color in enumerate(colors):
        pie.slices[i].fillColor = color
        pie.slices[i].strokeColor = BG_WHITE
        pie.slices[i].strokeWidth = 2
        pie.slices[i].fontName = 'Helvetica'
        pie.slices[i].fontSize = 7
        pie.slices[i].labelRadius = 1.3

    d.add(pie)
    d.add(String(30, height - 10, 'Universo de Activos (16+)',
                 fontSize=9, fontName='Helvetica-Bold', fillColor=TEXT_DARK))
    return d


# ============================================================
# BUILD THE PDF
# ============================================================

def build_pdf():
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                'reports', 'KHA0SYS3_Strategy_Guide.pdf')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm,
        leftMargin=2*cm,
        rightMargin=2*cm,
        title='KHA0SYS3 - Guia Completa de Estrategia',
        author='KHA0SYS3 Quant Team'
    )

    story = []

    # ================================================================
    # PORTADA
    # ================================================================
    story.append(Spacer(1, 4*cm))
    story.append(Paragraph('KHA0SYS3', ParagraphStyle(
        'BigTitle', parent=title_style, fontSize=42, leading=50, textColor=BG_DARK_CARD
    )))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph('Quant Portfolio Engine', ParagraphStyle(
        'BigSub', parent=title_style, fontSize=20, leading=24, textColor=BLUE_DARK
    )))
    story.append(make_hr())
    story.append(Paragraph(
        'La Guia Definitiva de la Estrategia Opening Range Breakout<br/>'
        'Multi-Sesion, Multi-Activo, Optimizada con Optuna',
        subtitle_style
    ))
    story.append(Spacer(1, 1*cm))

    # Cover metrics
    cover_metrics = [
        ('Activos', '16+', BLUE_DARK),
        ('Win Rate', '60-70%', GREEN_DARK),
        ('Setups', '55', PURPLE_DARK),
        ('Risk/Trade', '3.5%', ORANGE_DARK),
    ]
    story.append(make_metrics_row(cover_metrics))
    story.append(Spacer(1, 2*cm))

    story.append(Paragraph(
        'Version 1.0 | Abril 2026<br/>'
        'Estrategia 100% automatizada en MetaTrader 5<br/>'
        'Broker: Vantage Markets | VPS 24/7',
        ParagraphStyle('CoverFooter', parent=footer_style, fontSize=10, leading=14)
    ))

    story.append(make_joke(
        '"El mercado siempre tiene razon... excepto cuando yo tengo una orden pending."'
    ))

    story.append(PageBreak())

    # ================================================================
    # INDICE
    # ================================================================
    story.append(Paragraph('Indice de Contenidos', chapter_style))
    story.append(make_hr())

    toc_items = [
        ('1.', 'Habia una vez un Rango... (Que es ORB?)'),
        ('2.', 'El Universo de Activos (Nuestros Guerreros)'),
        ('3.', 'Las Sesiones: Cuando Pelear'),
        ('4.', 'La Senal de Entrada: El Breakout'),
        ('5.', 'Gestion de Riesgo: No Seas Kamikaze'),
        ('6.', 'Los Filtros: Porteros de la Discoteca'),
        ('7.', 'Optimizacion con Optuna: El Cerebro'),
        ('8.', 'El Trinity Portfolio: Los 3 Mosqueteros'),
        ('9.', 'Backtest vs Live: Suenos vs Realidad'),
        ('10.', 'El Bot en Accion: Un Dia Tipico'),
        ('11.', 'Monitoreo: Telegram, Tu Mejor Amigo'),
        ('12.', 'Resultados: Muestra los Numeros!'),
        ('13.', 'Fortalezas y Debilidades: Sin Filtros'),
        ('14.', 'Glosario del Trader Cuantico'),
    ]

    for num, title in toc_items:
        story.append(Paragraph(
            f'<b>{num}</b> {title}',
            ParagraphStyle('TOC', parent=body_style, fontSize=11, leading=18,
                           spaceBefore=2, spaceAfter=2, leftIndent=20)
        ))

    story.append(PageBreak())

    # ================================================================
    # CAPITULO 1: QUE ES ORB
    # ================================================================
    story.append(Paragraph('1. Habia una vez un Rango...', chapter_style))
    story.append(make_hr())

    story.append(Paragraph(
        'Imaginate que cada manana el mercado se despierta, se estira, y durante los primeros '
        '<b>15 minutos</b> de cada sesion importante se mueve dentro de un rango. '
        'Arriba, abajo, arriba, abajo... como tu intentando decidir que desayunar.',
        body_style
    ))
    story.append(Paragraph(
        'Ese pequeno rango de precios tiene un nombre: el <b>Opening Range</b> (OR). '
        'Y nuestra estrategia se llama <b>Opening Range Breakout (ORB)</b> porque esperamos '
        'pacientemente a que el precio ROMPA ese rango... y entonces, como un halcon, entramos.',
        body_style
    ))

    story.append(make_joke(
        '"Que dijo el Opening Range cuando el precio lo rompio? - Oye, que yo tenia planes para hoy!"'
    ))

    story.append(Paragraph('Como funciona en 4 pasos simples:', section_style))

    steps = [
        '<b>Paso 1 - Observar:</b> Cuando abre una sesion importante (Londres, Tokyo, NY), '
        'medimos el precio maximo y minimo de los primeros 15 minutos.',
        '<b>Paso 2 - Marcar:</b> El maximo se llama <font color="#1A7F37">OR High</font> '
        'y el minimo <font color="#CF222E">OR Low</font>. La distancia entre ambos es el <b>OR Width</b>.',
        '<b>Paso 3 - Esperar:</b> Colocamos dos ordenes pendientes: una de compra (BUY STOP) '
        'justo encima del OR High, y una de venta (SELL STOP) justo debajo del OR Low.',
        '<b>Paso 4 - Ejecutar:</b> Cuando el precio rompe uno de los dos niveles, '
        'esa orden se activa y la otra se cancela automaticamente. Simple!'
    ]
    for step in steps:
        story.append(Paragraph(f'&#9654; {step}', body_style))

    story.append(make_spacer(0.5))
    story.append(draw_orb_diagram())
    story.append(make_spacer(0.3))
    story.append(Paragraph(
        '<i>Diagrama: El precio consolida en el Opening Range (caja azul), rompe hacia arriba, '
        'activa el BUY STOP y alcanza el Take Profit (+0.8R).</i>',
        small_style
    ))

    story.append(make_callout(
        '<b>Dato clave:</b> El OR Width no es solo un rango, es la medida de nuestro riesgo. '
        'Si el rango es de 30 pips, nuestro Stop Loss sera de 30 pips. Elegante, no?'
    ))

    story.append(PageBreak())

    # ================================================================
    # CAPITULO 2: UNIVERSO DE ACTIVOS
    # ================================================================
    story.append(Paragraph('2. El Universo de Activos: Nuestros Guerreros', chapter_style))
    story.append(make_hr())

    story.append(Paragraph(
        'No somos de los que se casan con un solo par. Tenemos un ejercito diversificado '
        'de <b>16+ instrumentos</b> repartidos en 5 clases de activos. '
        'Cada uno tiene su personalidad, su sesion favorita y su nivel de drama:',
        body_style
    ))

    story.append(make_spacer(0.3))
    story.append(draw_pie_assets())
    story.append(make_spacer(0.3))

    # Asset table
    asset_headers = ['Clase', 'Activos', 'Sesion Principal', 'Personalidad']
    asset_rows = [
        ['Forex Major', 'EURUSD, GBPUSD, USDJPY', 'London / Tokyo', 'Liquidos, spreads tight'],
        ['Forex Cross', 'GBPJPY, EURJPY, AUDUSD,\nGBPAUD', 'London / Tokyo', 'Volatiles, OR amplios'],
        ['Metales', 'XAUUSD (Oro), XAGUSD (Plata)', 'London', 'Safe haven, tendenciales'],
        ['Energia', 'WTI, BRENT, NATGAS', 'London', 'Supply/demand driven'],
        ['Indices', 'SP500, NAS100, VIX', 'Pre-Market NY', 'Momentum USA, alta beta'],
    ]
    story.append(make_data_table(asset_headers, asset_rows, [2.5*cm, 5*cm, 3.5*cm, 5*cm]))

    story.append(make_joke(
        '"El GBPJPY es como ese amigo que dice voy tranquilo y termina saltando de un puente... con bungee, eso si."'
    ))

    story.append(Paragraph('Dato curioso sobre cada estrella:', section_style))

    star_info = [
        ('<b>GBPUSD (La Libra):</b> Nuestro mejor soldado en Londres con 65.84% win rate. '
         'Se mueve con precision britanica... la mayoria de las veces.'),
        ('<b>USDJPY (El Yen):</b> El campeon de Tokyo con +239R de PnL neto. '
         'Se despierta temprano y cumple sus promesas.'),
        ('<b>XAUUSD (El Oro):</b> El clasico refugio seguro. Cuando todo se cae, '
         'el oro brilla. Y nuestro ORB lo captura con 62% win rate.'),
        ('<b>NAS100 (El Nasdaq):</b> Tecnologia pura. Abre a las 13:30 UTC con Pre-Market '
         'y es explosivo. 65% win rate.'),
        ('<b>VIX (El Miedo):</b> Si, operamos el indice del miedo. Y tiene el MEJOR '
         'Profit Factor (1.41) de todo el portfolio. Ironico, no?'),
    ]
    for info in star_info:
        story.append(Paragraph(f'&#11088; {info}', body_style))

    story.append(PageBreak())

    # ================================================================
    # CAPITULO 3: LAS SESIONES
    # ================================================================
    story.append(Paragraph('3. Las Sesiones: Cuando Pelear', chapter_style))
    story.append(make_hr())

    story.append(Paragraph(
        'El mercado no duerme, pero tiene horarios de maxima actividad. '
        'Nosotros no operamos TODO el dia, solo durante las horas donde '
        'las probabilidades estan a nuestro favor:',
        body_style
    ))

    story.append(make_spacer(0.3))
    story.append(draw_session_timeline())
    story.append(make_spacer(0.5))

    session_headers = ['Sesion', 'Hora UTC', 'Activos Principales', 'Caracter']
    session_rows = [
        ['Tokyo', '00:00 - 08:00', 'USDJPY, GBPJPY, EURJPY', 'Tranquila pero consistente'],
        ['London', '07:00 - 16:00', 'EURUSD, GBPUSD, XAUUSD,\nAUDUSD, GBPAUD, WTI, BRENT', 'La reina de la liquidez'],
        ['New York', '13:30 - 22:00', 'SP500, NAS100, VIX', 'Explosiva, alta volatilidad'],
    ]
    story.append(make_data_table(session_headers, session_rows, [2.5*cm, 3*cm, 5*cm, 5.5*cm]))

    story.append(make_callout(
        '<b>Overlap London-NY (13:30-16:00 UTC):</b> Es el momento de maxima liquidez del dia. '
        'Aqui es donde el NAS100 y SP500 arrancan sus operaciones. El volumen se dispara!'
    ))

    story.append(make_joke(
        '"La sesion de Tokyo es como la persona que llega puntual a la fiesta. '
        'Londres es la que arma el desmadre. Y New York llega tarde pero con mas dinero que todos."'
    ))

    story.append(PageBreak())

    # ================================================================
    # CAPITULO 4: LA SENAL DE ENTRADA
    # ================================================================
    story.append(Paragraph('4. La Senal de Entrada: El Breakout', chapter_style))
    story.append(make_hr())

    story.append(Paragraph(
        'Aqui es donde la magia ocurre. Despues de calcular el Opening Range, '
        'colocamos dos ordenes pendientes como trampas perfectas:',
        body_style
    ))

    entry_headers = ['Orden', 'Tipo', 'Precio', 'Stop Loss', 'Take Profit']
    entry_rows = [
        ['LONG', 'BUY STOP', 'OR High', 'OR Low', 'OR High + (Width x TP_opt)'],
        ['SHORT', 'SELL STOP', 'OR Low', 'OR High', 'OR Low - (Width x TP_opt)'],
    ]
    story.append(make_data_table(entry_headers, entry_rows))

    story.append(Paragraph(
        '<b>Logica OCO (One-Cancels-Other):</b> Cuando una orden se llena, '
        'la otra se cancela automaticamente. No queremos estar long Y short al mismo tiempo '
        '(eso seria un hedge, no un trade).', body_style
    ))

    story.append(Paragraph('Reglas de oro de la entrada:', section_style))
    rules = [
        '<b>Una oportunidad por activo por dia.</b> Si GBPUSD ya opero hoy, no se toca mas. '
        'Nada de revenge trading.',
        '<b>Solo durante sesion activa.</b> Las ordenes expiran 8 horas despues del OR. '
        'Si no rompe en ese tiempo, no era para nosotros.',
        '<b>Fill or Kill (FOK).</b> La orden se llena completa o no se llena. '
        'Sin ejecuciones parciales que compliquen la gestion.',
        '<b>Expiracion hardware.</b> MT5 maneja la expiracion de ordenes, '
        'no dependemos solo del software. Doble seguridad.',
    ]
    for r in rules:
        story.append(Paragraph(f'&#10003; {r}', body_style))

    story.append(make_warning(
        '<b>Importante:</b> El breakout debe ocurrir con la vela M15 CERRADA, '
        'no con el precio actual de la vela en formacion. Esto evita falsas senales '
        'por wicks intra-vela.'
    ))

    story.append(PageBreak())

    # ================================================================
    # CAPITULO 5: GESTION DE RIESGO
    # ================================================================
    story.append(Paragraph('5. Gestion de Riesgo: No Seas Kamikaze', chapter_style))
    story.append(make_hr())

    story.append(Paragraph(
        'Este es probablemente el capitulo mas importante. Puedes tener la mejor estrategia '
        'del mundo, pero si tu gestion de riesgo es un desastre, tu cuenta se va a cero '
        'mas rapido de lo que puedes decir "margin call".',
        body_style
    ))

    story.append(make_joke(
        '"Que tienen en comun un trader sin gestion de riesgo y un paracaidista sin paracaidas? '
        'Ambos disfrutan mucho... pero solo por un rato."'
    ))

    story.append(make_spacer(0.3))
    story.append(draw_risk_diagram())
    story.append(make_spacer(0.5))

    story.append(Paragraph('La formula magica:', section_style))
    story.append(Paragraph(
        '<font face="Courier" size="9">'
        'Risk Capital = Balance x 3.5%<br/>'
        'Ticks at Risk = |Entry - SL| / Tick Size<br/>'
        'Loss per Lot = Ticks at Risk x Tick Value<br/>'
        'Position Size = floor(Risk Capital / Loss per Lot)'
        '</font>',
        code_style
    ))

    story.append(Paragraph('Ejemplo practico:', subsection_style))
    story.append(Paragraph(
        'Supongamos que tienes <b>$10,000</b> de balance y quieres operar GBPUSD con un OR Width de 20 pips:',
        body_style
    ))

    example = [
        'Risk Capital = $10,000 x 3.5% = <b>$350</b>',
        'SL = 20 pips = 200 ticks (para un lote standard, 1 tick = $0.10)',
        'Loss per Lot = 200 x $0.10 = <b>$20</b>',
        'Position Size = floor($350 / $20) = floor(17.5) = <b>17 micro-lotes (0.17 lots)</b>',
    ]
    for e in example:
        story.append(Paragraph(f'&#9654; {e}', body_style))

    story.append(make_callout(
        '<b>Usamos BALANCE, no Free Margin.</b> El balance es estable y predecible. '
        'El free margin fluctua con las posiciones abiertas y puede darnos tamanios '
        'de posicion erraticos. Aqui no nos gustan las sorpresas.'
    ))

    story.append(Paragraph('Lo que NO hacemos:', subsection_style))
    no_list = [
        '<b>NO usamos trailing stop.</b> El TP se fija al abrir la operacion y no se mueve. '
        'Trailing suena sexy, pero en ORB con TP corto (<1R), devuelve mas de lo que gana.',
        '<b>NO promediamos a la baja.</b> Si el trade va en contra, acepta la perdida (-1R) '
        'y sigue adelante. Manana hay otro trade.',
        '<b>NO movemos el Stop Loss.</b> El SL esta en OR Low (para longs) o OR High (para shorts). '
        'Es sagrado. Inamovible. Como las reglas de tu abuela.',
    ]
    for n in no_list:
        story.append(Paragraph(f'&#10060; {n}', body_style))

    story.append(PageBreak())

    # ================================================================
    # CAPITULO 6: LOS FILTROS
    # ================================================================
    story.append(Paragraph('6. Los Filtros: Porteros de la Discoteca', chapter_style))
    story.append(make_hr())

    story.append(Paragraph(
        'No todo breakout merece nuestro dinero. Tenemos tres filtros que actuan como '
        'porteros de discoteca: si no cumples los requisitos, no entras.',
        body_style
    ))

    story.append(Paragraph('Filtro 1: ATR14 (El Termometro de Volatilidad)', section_style))
    story.append(Paragraph(
        'Comparamos el ancho del Opening Range con el ATR de 14 dias. '
        'El ratio debe estar entre <b>10% y 80%</b>:',
        body_style
    ))

    atr_headers = ['Ratio OR/ATR', 'Significado', 'Decision']
    atr_rows = [
        ['< 10%', 'Rango MUY tight vs volatilidad normal', 'RECHAZADO - Poco edge'],
        ['10% - 80%', 'Rango proporcional a la volatilidad', 'APROBADO'],
        ['> 80%', 'Rango ENORME vs volatilidad normal', 'RECHAZADO - Posible news/gap'],
    ]
    story.append(make_data_table(atr_headers, atr_rows, [3*cm, 6*cm, 5*cm]))

    story.append(make_joke(
        '"El ATR filter es como medir la temperatura antes de ir a la playa: '
        'si hace -10C o 50C, mejor quedarse en casa."'
    ))

    story.append(Paragraph('Filtro 2: Spread Filter (El Detector de Estafas)', section_style))
    story.append(Paragraph(
        'Antes de colocar ordenes, medimos el spread actual y lo comparamos con '
        'el promedio de las ultimas 10 velas M15:',
        body_style
    ))
    story.append(Paragraph(
        '<font face="Courier" size="9">'
        'Regla: Spread actual <= 1.5x Spread promedio<br/>'
        'Piso: Minimo 5 puntos de baseline (evita falsos positivos en spreads ultra-tight)'
        '</font>',
        code_style
    ))
    story.append(Paragraph(
        'Si el spread esta inflado (tipico en noticias o baja liquidez), no operamos. '
        'Mejor perder una oportunidad que entrar con friction excesivo.',
        body_style
    ))

    story.append(Paragraph('Filtro 3: One Trade Per Day Per Asset', section_style))
    story.append(Paragraph(
        'Una vez que un activo se ha operado hoy, queda bloqueado hasta manana a las 00:00 UTC. '
        'Sin excepciones. Sin "pero esta vez se ve bueno". NO.',
        body_style
    ))

    story.append(PageBreak())

    # ================================================================
    # CAPITULO 7: OPTUNA
    # ================================================================
    story.append(Paragraph('7. Optimizacion con Optuna: El Cerebro', chapter_style))
    story.append(make_hr())

    story.append(Paragraph(
        'Aqui es donde la ciencia entra al juego. <b>Optuna</b> es un framework de optimizacion '
        'bayesiana que usamos para encontrar el <b>TP Multiplier optimo</b> para cada setup:',
        body_style
    ))

    story.append(Paragraph(
        'La pregunta que Optuna responde es: <i>"Para GBPUSD en la sesion de Londres con OR de 15 minutos, '
        'cual es el mejor multiplicador de TP que maximiza la expectativa sin destruir el win rate?"</i>',
        body_style
    ))

    story.append(Paragraph('El proceso:', section_style))
    optuna_steps = [
        '<b>Filtrar:</b> Solo setups con >65% de probabilidad base de breakout califican.',
        '<b>Barrer:</b> Probar TP desde 0.5x hasta 3.0x en pasos de 0.1x.',
        '<b>Evaluar:</b> Expectancy = (WinRate x TP_mult) - ((1 - WinRate) x 1.0)',
        '<b>Constraintear:</b> Win Rate debe mantenerse >= 60% despues de optimizacion.',
        '<b>Seleccionar:</b> El TP que maximiza expectativa cumpliendo el constraint.',
    ]
    for s in optuna_steps:
        story.append(Paragraph(f'&#9881; {s}', body_style))

    story.append(make_callout(
        '<b>Hallazgo clave:</b> La mayoria de setups optimizan entre 0.7x y 0.8x del OR Width. '
        'Esto significa que tomamos profit ANTES de llegar a 1R. Suena contraintuitivo, '
        'pero el win rate sube tanto que la expectativa neta es mayor.'
    ))

    story.append(Paragraph('Resultado: 55 Sub-Robots Optimizados', section_style))
    story.append(Paragraph(
        'Optuna genero 55 combinaciones ganadoras (instrumento + sesion + duracion + TP). '
        'Cada una funciona como un "sub-robot" independiente que opera en su horario.',
        body_style
    ))

    # Mini tearsheet
    ts_headers = ['Setup', 'TP Opt', 'Trades', 'Win Rate', 'PF', 'PnL (R)']
    ts_rows = [
        ['USDJPY Tokyo 15m', '0.8x', '2,047', '62.04%', '1.31', '+239.0'],
        ['GBPUSD London 15m', '0.7x', '1,979', '65.84%', '1.35', '+236.1'],
        ['XAUUSD London 15m', '0.8x', '1,967', '62.02%', '1.31', '+229.0'],
        ['GBPAUD London 15m', '0.8x', '1,932', '61.85%', '1.30', '+219.0'],
        ['SP500 Pre-Mkt 15m', '0.7x', '1,872', '65.38%', '1.32', '+208.8'],
        ['NAS100 Pre-Mkt 15m', '0.7x', '1,909', '65.06%', '1.30', '+202.4'],
        ['VIX NY Cash 15m', '0.9x', '651', '60.98%', '1.41', '+103.3'],
    ]
    story.append(make_data_table(ts_headers, ts_rows, [4*cm, 1.5*cm, 1.5*cm, 2*cm, 1.5*cm, 2*cm]))

    story.append(make_joke(
        '"Optuna es como tener un becario con un doctorado en matematicas '
        'que puede probar 10,000 combinaciones sin quejarse ni pedir cafe."'
    ))

    story.append(PageBreak())

    # ================================================================
    # CAPITULO 8: TRINITY PORTFOLIO
    # ================================================================
    story.append(Paragraph('8. El Trinity Portfolio: Los 3 Mosqueteros', chapter_style))
    story.append(make_hr())

    story.append(Paragraph(
        'De los 55 sub-robots posibles, actualmente corremos <b>3 en cuenta live</b>. '
        'Los elegimos por diversificacion de sesion, baja correlacion y robustez historica:',
        body_style
    ))

    trinity_headers = ['Mosquetero', 'Simbolo', 'Sesion', 'Hora UTC', 'OR Dur.', 'TP Opt']
    trinity_rows = [
        ['Athos', 'USDJPY+', 'Tokyo', '00:00', '15 min', '0.8x'],
        ['Porthos', 'GBPUSD+', 'London', '07:00', '15 min', '0.7x'],
        ["D'Artagnan", 'NAS100', 'New York', '13:30', '15 min', '0.7x'],
    ]
    story.append(make_data_table(trinity_headers, trinity_rows))

    story.append(make_callout(
        '<b>Por que estos 3?</b><br/>'
        '&#9654; <b>Diversificacion temporal:</b> Tokyo (Asia), London (Europa), NY (America). '
        'Cubren las 3 grandes zonas horarias.<br/>'
        '&#9654; <b>Baja correlacion:</b> Yen, Libra e Indice tecnologico USA. '
        'Rara vez se mueven igual.<br/>'
        '&#9654; <b>Robustez:</b> Los 3 tienen Profit Factor >1.30 y Win Rate >62% en backtest.'
    ))

    story.append(Paragraph(
        '<b>Nota sobre los simbolos:</b> En Vantage Markets, los pares de Forex llevan un "+" '
        'al final (USDJPY+, GBPUSD+), mientras que indices y commodities usan nombres propios '
        'del broker (NAS100, no NASDAQ100). El bot tiene un mapper que traduce esto automaticamente.',
        body_style
    ))

    story.append(Paragraph('Riesgo del Portfolio:', section_style))
    port_metrics = [
        ('Riesgo/Trade', '3.5%', ORANGE_DARK),
        ('Max Trades/Dia', '3', BLUE_DARK),
        ('Max Exposure', '10.5%', RED_DARK),
        ('Win Rate Esp.', '~63%', GREEN_DARK),
    ]
    story.append(make_metrics_row(port_metrics))
    story.append(make_spacer(0.3))
    story.append(Paragraph(
        'En el peor caso del dia (los 3 pierden), perdemos ~10.5% del balance. '
        'Duele, pero no destruye. Estadisticamente, la probabilidad de que '
        'los 3 pierdan el mismo dia es baja gracias a la diversificacion.',
        body_style
    ))

    story.append(make_joke(
        '"Por que son 3 mosqueteros? Porque si fueran 10, el margin call llegaria antes que el TP."'
    ))

    story.append(PageBreak())

    # ================================================================
    # CAPITULO 9: BACKTEST VS LIVE
    # ================================================================
    story.append(Paragraph('9. Backtest vs Live: Suenos vs Realidad', chapter_style))
    story.append(make_hr())

    story.append(Paragraph(
        'Todo trader sabe que un backtest es una promesa y el live es un compromiso. '
        'Aqui las diferencias clave y como las manejamos:',
        body_style
    ))

    diff_headers = ['Aspecto', 'Backtest', 'Live']
    diff_rows = [
        ['Data', 'CSV historico M15', 'MT5 API real-time'],
        ['Fill', 'Instantaneo', 'Pending + slippage'],
        ['Spread', 'No modelado', 'Filtro activo'],
        ['Sizing', '% equity simulado', '% balance real'],
        ['ATR', 'Historico D1', 'Calculado en tiempo real'],
        ['OR Data', 'Barra completa', 'Barra cerrada (1 bar delay)'],
        ['Monitoring', 'Logs offline', 'Telegram 24/7'],
        ['Reconnect', 'N/A', 'Auto-reconexion MT5'],
    ]
    story.append(make_data_table(diff_headers, diff_rows, [3*cm, 5*cm, 5*cm]))

    story.append(make_warning(
        '<b>El enemigo invisible: el Slippage.</b> En backtest asumimos fill perfecto. '
        'En live, puede haber 1-3 pips de diferencia. Con TPs de 0.7-0.8R, cada pip cuenta. '
        'Por eso usamos Fill or Kill y monitoreamos spreads.'
    ))

    story.append(Paragraph(
        'Para mantener consistencia entre backtest y live, seguimos estas reglas de hierro:',
        body_style
    ))
    consistency = [
        'Usamos la misma logica de OR calculation (barra cerrada, no en formacion).',
        'ATR14 con shift de 1 dia (sin look-ahead bias en ninguno).',
        'Mismos filtros ATR y de sesion activa.',
        'Mismo TP multiplier optimizado por Optuna.',
        'Tie-break intra-barra: siempre asumimos LOSS (bias pesimista en backtest).',
    ]
    for c in consistency:
        story.append(Paragraph(f'&#128736; {c}', body_style))

    story.append(PageBreak())

    # ================================================================
    # CAPITULO 10: UN DIA TIPICO
    # ================================================================
    story.append(Paragraph('10. El Bot en Accion: Un Dia Tipico', chapter_style))
    story.append(make_hr())

    story.append(Paragraph(
        'Acompanemos al bot KHA0SYS3 en un dia tipico de trading. '
        'Prepara tu cafe, esto va a ser divertido:',
        body_style
    ))

    timeline = [
        ('00:00 UTC', 'TOKYO ABRE',
         'El bot detecta que es hora de USDJPY. Descarga la primera vela M15, '
         'calcula el Opening Range. OR High = 156.850, OR Low = 156.720, Width = 13 pips. '
         'Verifica ATR: ratio = 0.35, OK. Spread: 1.2 pips vs 1.0 promedio, OK. '
         'Coloca BUY STOP en 156.850 y SELL STOP en 156.720.'),
        ('01:45 UTC', 'BREAKOUT USDJPY!',
         'El precio rompe 156.850. BUY STOP se ejecuta. El bot detecta el fill en 10 segundos, '
         'cancela el SELL STOP, marca USDJPY como "operado hoy". '
         'Telegram: "USDJPY+ LONG filled @ 156.850, SL 156.720, TP 156.954 (+0.8R)"'),
        ('03:20 UTC', 'TP HIT!',
         'El precio alcanza 156.954. Posicion cerrada con ganancia. '
         'Telegram: "USDJPY+ CLOSED +$280 (+0.8R) -- Butterfly emoji"'),
        ('07:00 UTC', 'LONDON ABRE',
         'Turno del GBPUSD. OR calculado: High = 1.2650, Low = 1.2625, Width = 25 pips. '
         'ATR filter OK, Spread OK. Ordenes colocadas.'),
        ('08:30 UTC', 'BREAKOUT GBPUSD!',
         'Short! El precio rompe 1.2625 hacia abajo. SELL STOP ejecutado, BUY STOP cancelado. '
         'SL en 1.2650, TP en 1.2607 (-0.7R del width).'),
        ('10:15 UTC', 'SL HIT...',
         'El precio reversa y sube. SL ejecutado en 1.2650. Perdida: -$350 (-1R). '
         'Telegram: "GBPUSD+ CLOSED -$350 (-1R) -- Explosion emoji". Pasa, es parte del juego.'),
        ('13:30 UTC', 'NEW YORK PRE-MARKET',
         'NAS100 en accion. OR de 15 min calculado. Width = 45 puntos. '
         'Ordenes colocadas. El Nasdaq es volatil, vamos a ver...'),
        ('14:45 UTC', 'BREAKOUT NAS100!',
         'LONG! Tecnologia sube. TP hit a las 16:00 UTC. +0.7R = +$245.'),
        ('23:59 UTC', 'CIERRE DEL DIA',
         'Balance del dia: +$280 - $350 + $245 = <b>+$175 neto</b>. '
         '2 de 3 ganadores. Dia tipico. Los contadores se resetean para manana.'),
    ]

    for time, event, desc in timeline:
        story.append(KeepTogether([
            Paragraph(
                f'<font color="#0969DA"><b>{time}</b></font> - '
                f'<font color="#8250DF"><b>{event}</b></font>',
                ParagraphStyle('TimeEvent', parent=body_style, fontSize=11, spaceBefore=8)
            ),
            Paragraph(desc, ParagraphStyle('TimeDesc', parent=body_style, leftIndent=20)),
        ]))

    story.append(make_joke(
        '"Un dia sin trades es como un domingo sin futbol: '
        'tecnicaente posible, pero profundamente aburrido."'
    ))

    story.append(PageBreak())

    # ================================================================
    # CAPITULO 11: MONITOREO TELEGRAM
    # ================================================================
    story.append(Paragraph('11. Monitoreo: Telegram, Tu Mejor Amigo', chapter_style))
    story.append(make_hr())

    story.append(Paragraph(
        'El bot no solo opera, tambien se comunica contigo via Telegram como un buen empleado. '
        'Tiene dos canales: chat personal y grupo. Comandos disponibles:',
        body_style
    ))

    cmd_headers = ['Comando', 'Que hace', 'Ejemplo respuesta']
    cmd_rows = [
        ['/balance', 'Balance y equity actual', '$10,175 | Equity: $10,320'],
        ['/pnl', 'P&L diario/semanal/mensual', 'Hoy: +$175 | Semana: +$820'],
        ['/positions', 'Posiciones abiertas', 'USDJPY LONG @ 156.85, PnL: +$140'],
        ['/orders', 'Ordenes pendientes', '2 pendientes: GBPUSD BUY/SELL STOP'],
        ['/health', 'Salud del VPS', 'CPU: 12% | RAM: 45% | MT5: Connected'],
        ['/stop', 'Pausa el bot', 'Bot PAUSED. Use /resume to continue'],
        ['/resume', 'Reanuda el bot', 'Bot RESUMED. Trading active.'],
    ]
    story.append(make_data_table(cmd_headers, cmd_rows, [2.5*cm, 4.5*cm, 6*cm]))

    story.append(Paragraph('Notificaciones automaticas:', section_style))
    notif_list = [
        '<b>Cada 15 min:</b> Heartbeat con uptime y conteo de trades del dia.',
        '<b>Al detectar ORB:</b> Notifica que se colocaron ordenes pendientes.',
        '<b>Al llenarse una orden:</b> Detalles de entrada, SL, TP.',
        '<b>Al cerrarse un trade:</b> Resultado con emoji (mariposa = profit, explosion = loss).',
        '<b>Alertas criticas:</b> CPU >90%, RAM >90%, MT5 desconectado, trading deshabilitado.',
        '<b>Limpieza de ordenes:</b> Notifica cuando elimina ordenes vencidas.',
    ]
    for n in notif_list:
        story.append(Paragraph(f'&#128276; {n}', body_style))

    story.append(make_callout(
        '<b>Nada de spam:</b> El bot esta configurado para notificar lo justo y necesario. '
        'No quieres 200 mensajes al dia. Quieres saber cuando algo importa.'
    ))

    story.append(PageBreak())

    # ================================================================
    # CAPITULO 12: RESULTADOS
    # ================================================================
    story.append(Paragraph('12. Resultados: Muestra los Numeros!', chapter_style))
    story.append(make_hr())

    story.append(Paragraph(
        'Ahora si, lo que todos quieren ver: los numeros. '
        'Estos resultados vienen del backtest optimizado con Optuna sobre ~8 anos de datos:',
        body_style
    ))

    story.append(make_spacer(0.3))
    story.append(draw_win_rate_bars())
    story.append(make_spacer(0.5))

    story.append(Paragraph('Metricas del Portfolio Completo (55 sub-robots):', section_style))
    port_full_metrics = [
        ('Trades Totales', '115K+', BLUE_DARK),
        ('Win Rate Global', '63-66%', GREEN_DARK),
        ('Profit Factor', '1.15-1.25', PURPLE_DARK),
    ]
    story.append(make_metrics_row(port_full_metrics))
    story.append(make_spacer(0.3))

    story.append(Paragraph('Top 10 Setups por PnL Neto:', section_style))
    top10_headers = ['#', 'Setup', 'PnL (R)', 'Win Rate', 'PF', 'Max DD']
    top10_rows = [
        ['1', 'USDJPY Tokyo 15m', '+239.0', '62.04%', '1.31', '-11.0R'],
        ['2', 'GBPUSD London 15m', '+236.1', '65.84%', '1.35', '-9.7R'],
        ['3', 'XAUUSD London 15m', '+229.0', '62.02%', '1.31', '-19.6R'],
        ['4', 'GBPAUD London 15m', '+219.0', '61.85%', '1.30', '-16.4R'],
        ['5', 'GBPJPY London 15m', '+209.2', '61.41%', '1.27', '-16.0R'],
        ['6', 'SP500 Pre-Mkt 15m', '+208.8', '65.38%', '1.32', '-13.0R'],
        ['7', 'BRENT London 15m', '+207.6', '61.53%', '1.28', '-16.8R'],
        ['8', 'XAUUSD London 30m', '+204.0', '61.07%', '1.25', '-21.4R'],
        ['9', 'WTI London 15m', '+203.8', '61.42%', '1.27', '-10.6R'],
        ['10', 'NAS100 Pre-Mkt 15m', '+202.4', '65.06%', '1.30', '-17.5R'],
    ]
    story.append(make_data_table(top10_headers, top10_rows,
                                  [0.8*cm, 5*cm, 2*cm, 2*cm, 1.5*cm, 2*cm]))

    story.append(make_spacer(0.3))

    story.append(Paragraph('Curva de equity simulada:', section_style))
    story.append(draw_equity_curve())
    story.append(make_spacer(0.2))
    story.append(Paragraph(
        '<i>Simulacion de 100 trades con $1,000 de inicio, 3.5% risk, 63% win rate, 0.8R TP. '
        'La curva real del portfolio completo esta disponible en portfolio_curve.png.</i>',
        small_style
    ))

    story.append(Paragraph('Que significan estos numeros en dinero real?', subsection_style))
    money_headers = ['Capital Inicial', 'Retorno Mensual Est.', 'Despues de 6 meses', 'Despues de 12 meses']
    money_rows = [
        ['$1,000', '+3-5%', '$1,194 - $1,340', '$1,426 - $1,796'],
        ['$5,000', '+3-5%', '$5,970 - $6,700', '$7,129 - $8,979'],
        ['$10,000', '+3-5%', '$11,941 - $13,401', '$14,258 - $17,959'],
        ['$50,000', '+3-5%', '$59,703 - $67,005', '$71,289 - $89,793'],
    ]
    story.append(make_data_table(money_headers, money_rows, [3*cm, 4*cm, 4*cm, 4.5*cm]))

    story.append(make_warning(
        '<b>Disclaimer:</b> Estos son estimados basados en backtest. '
        'Rendimientos pasados no garantizan resultados futuros. '
        'El slippage, spreads y condiciones de mercado pueden afectar los resultados reales.'
    ))

    story.append(PageBreak())

    # ================================================================
    # CAPITULO 13: FORTALEZAS Y DEBILIDADES
    # ================================================================
    story.append(Paragraph('13. Fortalezas y Debilidades: Sin Filtros', chapter_style))
    story.append(make_hr())

    story.append(Paragraph(
        'Vamos a ser 100% honestos. Ninguna estrategia es perfecta. Aqui va lo bueno, '
        'lo malo y lo feo:',
        body_style
    ))

    story.append(Paragraph('Lo BUENO (Fortalezas):', section_style))
    strengths = [
        '<b>Cuantitativamente rigurosa:</b> Todo parametro esta validado con >2,000 trades '
        'y solo setups con >60% win rate pasan el filtro.',
        '<b>Multi-activo, multi-sesion:</b> Diversificacion real entre Forex, Metales, '
        'Energia e Indices. No dependemos de un solo mercado.',
        '<b>Risk management estricto:</b> 3.5% por trade, sin trailing, sin promediar. '
        'Reglas claras que no dejan lugar a la emocion.',
        '<b>Automatizado 24/7:</b> El bot corre en VPS, opera solo, reporta por Telegram. '
        'Tu duermes, el trabaja.',
        '<b>Monitoreo robusto:</b> Health checks, auto-reconnect, alertas criticas. '
        'Si algo falla, te enteras en segundos.',
        '<b>Parametros optimizados:</b> Optuna encuentra el TP optimo para cada setup. '
        'No es intuicion, son datos.',
    ]
    for s in strengths:
        story.append(Paragraph(f'&#9989; {s}', body_style))

    story.append(Paragraph('Lo MALO (Debilidades):', section_style))
    weaknesses = [
        '<b>Correlacion intraday:</b> En dias de panico, TODOS los activos pueden moverse '
        'en la misma direccion. Los 3 mosqueteros pueden perder juntos (-10.5%).',
        '<b>Slippage no modelado:</b> El backtest asume fills perfectos. En live, '
        'especialmente en NAS100, el slippage puede comer 1-3 pips por trade.',
        '<b>Dependencia de MT5:</b> Si MetaTrader 5 se cae y la reconexion falla, '
        'las ordenes pendientes podrian no ejecutarse.',
        '<b>TP corto (<1R):</b> El ratio riesgo/recompensa nominal es negativo (arriesgamos 1R '
        'para ganar 0.7-0.8R). Compensamos con un win rate alto, pero rachas perdedoras duelen.',
        '<b>Swap fees:</b> Si un trade no cierra en el dia, las comisiones overnight se acumulan. '
        'No es un gran problema con ORB, pero hay que monitorearlo.',
    ]
    for w in weaknesses:
        story.append(Paragraph(f'&#9888; {w}', body_style))

    story.append(Paragraph('Lo FEO (Riesgos extremos):', section_style))
    ugly = [
        '<b>Flash crash:</b> Un movimiento extremo puede saltar el SL por slippage masivo. '
        'Raro, pero posible. Fill or Kill ayuda a mitigar.',
        '<b>Broker issues:</b> Si Vantage suspende trading o cambia condiciones, '
        'el bot necesitaria ajustes inmediatos.',
        '<b>Overfitting:</b> Aunque usamos >2,000 trades por setup, siempre existe '
        'el riesgo de que los parametros optimizados no funcionen en regimenes de mercado futuros.',
    ]
    for u in ugly:
        story.append(Paragraph(f'&#128128; {u}', body_style))

    story.append(make_joke(
        '"Lo bueno de ser transparente con las debilidades es que '
        'cuando algo sale mal, puedes decir ya lo sabia. Lo malo es que... ya lo sabias."'
    ))

    story.append(PageBreak())

    # ================================================================
    # CAPITULO 14: GLOSARIO
    # ================================================================
    story.append(Paragraph('14. Glosario del Trader Cuantico', chapter_style))
    story.append(make_hr())

    glossary = [
        ('OR (Opening Range)', 'Rango de precios formado durante los primeros X minutos de una sesion.'),
        ('ORB (Opening Range Breakout)', 'Estrategia que opera la ruptura del Opening Range.'),
        ('OR High / OR Low', 'Precio maximo y minimo del Opening Range.'),
        ('OR Width', 'Distancia entre OR High y OR Low. Define nuestro riesgo por trade.'),
        ('TP Multiplier', 'Factor que multiplicamos por OR Width para calcular el Take Profit.'),
        ('R-Multiple', 'Unidad de riesgo. +1R = ganaste lo que arriesgaste. -1R = perdiste lo arriesgado.'),
        ('ATR(14)', 'Average True Range de 14 dias. Mide la volatilidad promedio diaria.'),
        ('Profit Factor', 'Ganancias brutas / Perdidas brutas. >1.0 = sistema rentable.'),
        ('Sharpe Ratio', 'Retorno ajustado por riesgo. >0.5 = bueno, >1.0 = excelente.'),
        ('Max Drawdown', 'Caida maxima desde el pico de equity. Mide el peor momento historico.'),
        ('Win Rate', 'Porcentaje de trades ganadores sobre el total.'),
        ('Expectancy', 'Ganancia promedio por trade en unidades de R.'),
        ('OCO (One-Cancels-Other)', 'Cuando una orden se ejecuta, la contraria se cancela.'),
        ('FOK (Fill or Kill)', 'La orden se ejecuta completa o se cancela. Sin parciales.'),
        ('Magic Time', 'Hora UTC a la que se activa el calculo del OR para un setup especifico.'),
        ('Trinity Portfolio', 'Los 3 setups activos en live: USDJPY, GBPUSD, NAS100.'),
        ('Optuna', 'Framework de optimizacion bayesiana usado para encontrar el TP optimo.'),
        ('VPS', 'Virtual Private Server. Servidor remoto donde corre el bot 24/7.'),
        ('Heartbeat', 'Mensaje periodico que confirma que el bot sigue vivo y operando.'),
    ]

    glos_headers = ['Termino', 'Definicion']
    glos_rows = [[t, d] for t, d in glossary]
    # Custom table for glossary with left-aligned text
    hdr = [Paragraph('Termino', table_header_style), Paragraph('Definicion', table_header_style)]
    data = [hdr]
    for term, defn in glossary:
        data.append([
            Paragraph(f'<b>{term}</b>', table_cell_left),
            Paragraph(defn, table_cell_left)
        ])

    t = Table(data, colWidths=[5*cm, 11*cm], repeatRows=1)
    style_cmds = [
        ('BACKGROUND', (0,0), (-1,0), BG_DARK_CARD),
        ('TEXTCOLOR', (0,0), (-1,0), TEXT_WHITE),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#E1E4E8')),
        ('TOPPADDING', (0,1), (-1,-1), 4),
        ('BOTTOMPADDING', (0,1), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0,i), (-1,i), BG_LIGHT))
    t.setStyle(TableStyle(style_cmds))
    story.append(t)

    story.append(PageBreak())

    # ================================================================
    # PAGINA FINAL
    # ================================================================
    story.append(Spacer(1, 5*cm))
    story.append(Paragraph('KHA0SYS3', ParagraphStyle(
        'FinalTitle', parent=title_style, fontSize=36, textColor=BG_DARK_CARD
    )))
    story.append(Paragraph('Quant Portfolio Engine', ParagraphStyle(
        'FinalSub', parent=subtitle_style, fontSize=16, textColor=BLUE_DARK
    )))
    story.append(make_hr())
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(
        '"En un mundo de traders emocionales,<br/>'
        'se cuantico, se sistematico, se disciplinado.<br/>'
        'Y sobre todo... se rentable."',
        ParagraphStyle('FinalQuote', parent=body_style, fontSize=13, leading=20,
                       alignment=TA_CENTER, textColor=PURPLE_DARK,
                       fontName='Helvetica-Oblique')
    ))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph(
        'Documento generado automaticamente por el sistema KHA0SYS3.<br/>'
        'Todos los datos provienen de backtests reales con datos historicos M15.<br/>'
        'Rendimientos pasados no garantizan resultados futuros.<br/><br/>'
        'Abril 2026',
        footer_style
    ))

    # Build
    doc.build(story)
    print(f"\n{'='*60}")
    print(f"  PDF generado exitosamente!")
    print(f"  Ubicacion: {output_path}")
    print(f"{'='*60}\n")
    return output_path


if __name__ == '__main__':
    build_pdf()
