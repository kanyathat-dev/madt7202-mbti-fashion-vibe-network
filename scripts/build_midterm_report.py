#!/usr/bin/env python3
"""Build a one-page MADT7202 MBTI-Fashion Vibe Network report."""
from __future__ import annotations
import argparse
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, Image as RLImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

NAVY = HexColor('#1F3454')
BLUE = HexColor('#2B507F')
ORANGE = HexColor('#E87500')
PALE_BLUE = HexColor('#F1F5FA')
PALE_ORANGE = HexColor('#FFF7EB')
BORDER = HexColor('#D5DFEA')
BODY = HexColor('#28374B')
MUTED = HexColor('#607086')
WHITE = colors.white
PAGE_W, PAGE_H = A4
M = 15 * mm
CONTENT_W = PAGE_W - 2 * M
GAP = 14
COL_W = (CONTENT_W - GAP) / 2
X1, X2 = M, M + COL_W + GAP

FONT, FONT_BOLD, FONT_ITALIC = 'Helvetica', 'Helvetica-Bold', 'Helvetica-Oblique'
font_dir = Path('/usr/share/fonts/truetype/dejavu')
try:
    if (font_dir / 'DejaVuSans.ttf').exists() and (font_dir / 'DejaVuSans-Bold.ttf').exists():
        pdfmetrics.registerFont(TTFont('DV', str(font_dir / 'DejaVuSans.ttf')))
        pdfmetrics.registerFont(TTFont('DV-Bold', str(font_dir / 'DejaVuSans-Bold.ttf')))
        pdfmetrics.registerFont(TTFont('DV-Oblique', str(font_dir / 'DejaVuSans-Oblique.ttf')))
        # Map paragraph <b> tags to the embedded bold font so emphasis is visible in the PDF.
        pdfmetrics.registerFontFamily('DV', normal='DV', bold='DV-Bold',
                                      italic='DV-Oblique', boldItalic='DV-Bold')
        FONT, FONT_BOLD, FONT_ITALIC = 'DV', 'DV-Bold', 'DV-Oblique'
except Exception as exc:
    print(f'Warning: using built-in fonts: {exc}')

ST = {
    'body': ParagraphStyle('body', fontName=FONT, fontSize=8.15, leading=9.75, textColor=BODY, spaceAfter=0),
    'body_sm': ParagraphStyle('body_sm', fontName=FONT, fontSize=7.7, leading=9.0, textColor=BODY, spaceAfter=0),
    'tbl': ParagraphStyle('tbl', fontName=FONT, fontSize=7.7, leading=9.0, textColor=BODY, spaceAfter=0),
    'tbl_label': ParagraphStyle('tbl_label', fontName=FONT_BOLD, fontSize=7.7, leading=9.0, textColor=BLUE, spaceAfter=0),
    'caption': ParagraphStyle('caption', fontName=FONT_ITALIC, fontSize=7.2, leading=8.5, textColor=MUTED, alignment=1, spaceAfter=0),
    'link': ParagraphStyle('link', fontName=FONT, fontSize=7.2, leading=8.5, textColor=BLUE, spaceAfter=0),
    'card_head': ParagraphStyle('card_head', fontName=FONT_BOLD, fontSize=7.7, leading=8.8, textColor=ORANGE, spaceAfter=1),
    'card_body': ParagraphStyle('card_body', fontName=FONT, fontSize=7.15, leading=8.1, textColor=BODY, spaceAfter=0),
}

def P(text, style='body'):
    return Paragraph(text, ST[style])

def draw_section(c, x, top, title, width):
    c.setFillColor(ORANGE)
    c.setFont(FONT_BOLD, 9.3)
    c.drawString(x, top, title.upper())
    c.setStrokeColor(HexColor('#E8CBA7'))
    c.setLineWidth(0.55)
    c.line(x, top - 5.7, x + width, top - 5.7)

def draw_para(c, text, x, top, width, style='body'):
    p = P(text, style)
    _, h = p.wrap(width, 600)
    p.drawOn(c, x, top - h)
    return top - h, h

def make_table(rows, width, label_w, font_style='tbl', padding=4.2):
    data = [[P(label, 'tbl_label'), P(text, font_style)] for label, text in rows]
    t = Table(data, colWidths=[label_w, width - label_w], hAlign='LEFT')
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (0, -1), PALE_BLUE),
        ('BACKGROUND', (1, 0), (1, -1), WHITE),
        ('LINEBELOW', (0, 0), (-1, -2), 0.45, BORDER),
        ('BOX', (0, 0), (-1, -1), 0.45, BORDER),
        ('LEFTPADDING', (0, 0), (-1, -1), padding),
        ('RIGHTPADDING', (0, 0), (-1, -1), padding),
        ('TOPPADDING', (0, 0), (-1, -1), 3.0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.0),
    ]))
    return t

def table_draw(c, table, x, top, width):
    _, h = table.wrap(width, 700)
    table.drawOn(c, x, top - h)
    return top - h, h

def draw_card(c, x, top, width, height, title, headline, body, accent, bg):
    c.setFillColor(bg); c.setStrokeColor(BORDER); c.setLineWidth(0.55)
    c.roundRect(x, top-height, width, height, 2.5, stroke=1, fill=1)
    c.setFillColor(accent); c.rect(x, top-height, 2.4, height, stroke=0, fill=1)
    tx, inner_w = x+7.5, width-14
    p1 = P(title, 'card_head'); _, h1 = p1.wrap(inner_w, height); p1.drawOn(c, tx, top-5-h1)
    p2 = Paragraph(headline, ParagraphStyle('card_headline_'+title, fontName=FONT_BOLD, fontSize=8.15, leading=9.3, textColor=NAVY))
    _, h2 = p2.wrap(inner_w, height); y2 = top-8-h1-h2; p2.drawOn(c, tx, y2)
    p3 = P(body, 'card_body'); _, h3 = p3.wrap(inner_w, height); p3.drawOn(c, tx, y2-h3-2)

def read_metrics(root: Path):
    m = {
        'images': 67, 'evidence_rows': 268, 'creator_count': 6,
        'anchor': 'Clean-Traditional', 'anchor_degree': 8, 'anchor_coverage': 28,
        'anchor_bc': 0.0456, 'bridge': 'Playful-Streetwear', 'bridge_bc': 0.3134,
        'bridge_load': 33.0, 'no_overlap': 58, 'total_pairs': 120,
        'loco_top_count': 4, 'loco_total': 6,
        'thresholds': [
            'Threshold 2: 14 edges; largest component 7 nodes; 111/113 no-overlap pairs unreachable.',
            'Threshold 3: 2 edges; largest component 3 nodes; 119/119 no-overlap pairs unreachable.',
        ],
    }
    try:
        import pandas as pd
        p = root / 'mbti_vibe_network_metrics.csv'
        if p.exists():
            df = pd.read_csv(p)
            a = df.loc[df['Fashion Vibe'] == m['anchor']].iloc[0]
            b = df.loc[df['Fashion Vibe'] == m['bridge']].iloc[0]
            m['anchor_degree'] = int(a['Degree'])
            m['anchor_coverage'] = int(a['Pairs covered (of 120)'])
            m['anchor_bc'] = float(a['Betweenness (dist=1/NPMI)'])
            m['bridge_bc'] = float(b['Betweenness (dist=1/NPMI)'])
            m['bridge_load'] = float(b['Bridge Load (fractional path-load units)'])
        p = root / 'mbti_fashion_image_level.csv'
        if p.exists():
            df = pd.read_csv(p)
            m['images'] = int(df['image_id'].nunique())
            m['creator_count'] = int(df['creator'].nunique())
            m['evidence_rows'] = len(df) * 4
        p = root / 'leave_one_creator_out_sensitivity.csv'
        if p.exists():
            df = pd.read_csv(p)
            m['loco_total'] = len(df)
            m['loco_top_count'] = int((df['Top bridge'] == m['bridge']).sum())
        p = root / 'npmi_threshold_sensitivity.csv'
        if p.exists():
            df = pd.read_csv(p)
            rows = []
            for t in (2, 3):
                r = df.loc[df['Minimum co-occurrence'].astype(int) == t]
                if not r.empty:
                    r = r.iloc[0]
                    rows.append(f"Threshold {t}: {int(r['Retained edges'])} edges; largest component {int(r['Largest component (nodes)'])} nodes; {int(r['Unreachable no-overlap pairs'])}/{int(r['No-direct-overlap pairs (of 120)'])} no-overlap pairs unreachable.")
            if rows:
                m['thresholds'] = rows
    except Exception as exc:
        print(f'Warning: CSV metrics unavailable; using checked baseline values: {exc}')
    return m

def build_report(output_path: Path, graph_path: Path, root: Path):
    m = read_metrics(root)
    if not graph_path.exists():
        raise FileNotFoundError(f'Network image is required: {graph_path}')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(output_path), pagesize=A4, invariant=1)
    c.setTitle('MBTI-Fashion Vibe Network - One-page Midterm Report')
    c.setAuthor('Kanyathat Rakdee')
    c.setSubject('MADT7202 midterm report - network analysis, pruning and sensitivity')

    c.setFillColor(NAVY); c.setFont(FONT_BOLD, 19.0)
    c.drawString(M, 785, 'MBTI–FASHION VIBE NETWORK')
    c.setFillColor(MUTED); c.setFont(FONT, 10.0)
    c.drawString(M+0.5, 766, 'Living Room Anchor & Compromise Bridge for Newlyweds')
    c.setFont(FONT, 7.3)
    c.drawString(M+0.5, 751.5, 'MADT7202 | Web & Social Network Analytics | Midterm Project')
    c.setFillColor(NAVY); c.setFont(FONT_BOLD, 7.8)
    c.drawRightString(PAGE_W-M, 751.5, 'Kanyathat Rakdee | 6810424002')
    c.setStrokeColor(NAVY); c.setLineWidth(1.5); c.line(M, 741, PAGE_W-M, 741)

    draw_section(c, X1, 724, '01 The Decision', COL_W)
    draw_para(c, 'As a Lead Design Strategist, shortlist a primary living-room style (the <b>Living Room Anchor</b>) and potential bridge styles for newlyweds with different MBTI labels. Results may inform furniture-collection planning and a future recommendation engine.', X1, 710, COL_W, 'body')
    draw_section(c, X2, 724, '02 Why a Network', COL_W)
    draw_para(c, 'Frequency alone does not show which MBTI categories share observed Vibe links. A <b>bipartite network</b> and weighted shortest paths identify structural bridges for pairs with no shared direct Vibe. These are coded-data patterns, not proof of psychological compatibility or actual customer preference.', X2, 710, COL_W, 'body')

    company_url = 'https://www.myersbriggs.org/my-mbti-personality-type/the-16-mbti-personality-types/'
    data_top = 635
    draw_section(c, X1, data_top, '03 Data', COL_W)
    draw_section(c, X2, data_top, '04 Graph Construction', COL_W)
    data_rows = [
        ('Sources', f"{m['images']} public TikTok lookbook images ({m['evidence_rows']} coded observations) from six anonymized creator labels (A–F)."),
        ('Handling', 'Creator labels anonymized; usernames and identifying account details were not stored in the analysis dataset.'),
        ('Period', '27 September to 7 October 2026.'),
        ('Coding control', 'Gemini assisted with Fashion Vibe coding. Fashion Vibe categories and room-style interpretations are researcher-defined.'),
        ('Bias control', f'Coded attributes were compared against the framework of <link href="{company_url}" color="#2B507F"><u>The Myers-Briggs Company ↗</u></link>.'),
    ]
    data_table = make_table(data_rows, COL_W, 77, padding=4.2)
    data_bottom, data_h = table_draw(c, data_table, X1, data_top-15, COL_W)

    threshold_text = '<br/>'.join(m['thresholds'])
    graph_rows = [
        ('Nodes / edges', 'Bipartite graph: 16 MBTI square nodes + 12 Fashion Vibe circle nodes.'),
        ('Weighting', 'Image-level NPMI, N = 67; shortest-path distance d = 1/NPMI for positive edges.'),
        ('Pruning / overlap', 'Retain NPMI &gt; 0; 51/51 observed edges retained. Separately, 58/120 MBTI pairs (48.3%) have no shared direct Vibe; this is not Bridge Load.'),
        ('Result', '<b>28 nodes and 51 edges out of 192 possible cross-set links.</b>'),
        ('Sensitivity', threshold_text),
    ]
    graph_table = make_table(graph_rows, COL_W, 63, padding=3.0)
    graph_bottom, graph_h = table_draw(c, graph_table, X2, data_top-15, COL_W)
    print(f'Data table: {data_h:.1f} pt; graph table: {graph_h:.1f} pt')

    graph_section_top = min(data_bottom, graph_bottom) - 14
    draw_section(c, M, graph_section_top, '05 The Graph', CONTENT_W)
    img = RLImage(str(graph_path))
    img_w = 255
    img_h = img_w * img.imageHeight / img.imageWidth
    img_x = (PAGE_W-img_w)/2
    img_top = graph_section_top - 11
    img_y = img_top - img_h
    img.drawWidth, img.drawHeight = img_w, img_h
    img.drawOn(c, img_x, img_y)
    caption_top = img_y - 1
    caption_bottom, caption_height = draw_para(
        c,
        'ESTJ and INFP have zero shared direct Vibe; highlighted mediation path: Sharp-Tailored → Dark-Perfectionist → Earthy-Raw.',
        M+10, caption_top, CONTENT_W-20, 'caption'
    )

    # Position section 06 from the caption's actual bottom to keep a clear gap.
    findings_top = caption_bottom - 15
    draw_section(c, M, findings_top, '06 Findings', CONTENT_W)
    card_top = findings_top - 12
    card_gap = 7
    card_w = (CONTENT_W - 2*card_gap)/3
    card_h = 65
    draw_card(c, M, card_top, card_w, card_h, 'HUB / ANCHOR CANDIDATE', f"{m['anchor']} | 23.3%", f"Degree: {m['anchor_degree']}<br/>MBTI-pair coverage: {m['anchor_coverage']}/120<br/>Weighted betweenness: {m['anchor_bc']:.4f}", BLUE, PALE_BLUE)
    draw_card(c, M+card_w+card_gap, card_top, card_w, card_h, 'TOP STRUCTURAL BRIDGE', m['bridge'], f"Weighted betweenness: {m['bridge_bc']:.4f}<br/><b>Bridge Load: {m['bridge_load']:.1f} fractional path-load units</b><br/>Top bridge in {m['loco_top_count']} of {m['loco_total']} creator-removal runs", ORANGE, PALE_BLUE)
    draw_card(c, M+2*(card_w+card_gap), card_top, card_w, card_h, 'EXAMPLE MEDIATION', 'ESTJ × INFP', 'Zero direct overlap in the observed graph.<br/>Path: Sharp-Tailored → Dark-Perfectionist → Earthy-Raw.', ORANGE, PALE_ORANGE)

    low_top = card_top - card_h - 12
    draw_section(c, X1, low_top, '07 Recommended Action', COL_W)
    draw_section(c, X2, low_top, '08 What Would Change My Mind', COL_W)
    left_text = ('&#8226; Use Clean-Traditional as an anchor candidate (Classic Contemporary / Hamptons-inspired direction).<br/>'
                 '&#8226; Test Playful-Streetwear alongside Soft-Romantic and Dark-Perfectionist; do not treat a single style as a universal answer.<br/>'
                 '&#8226; Keep d = 1/NPMI as exploratory recommendation logic, subject to validation with couples.')
    right_text = ('&#8226; Leave-One-Creator-Out: <b>Playful-Streetwear</b> leads in 4/6 runs; <b>Dark-Perfectionist</b> and <b>Soft-Romantic</b> lead in the other runs, so the ranking is sensitive to creator composition.<br/>'
                  '&#8226; Threshold tests fragment the graph; alternative top-bridge names under stricter thresholds are not reliable recommendations.<br/>'
                  '&#8226; A showroom A/B test with 100 couples is proposed future validation, not a completed experiment.')
    left_bottom, left_h = draw_para(c, left_text, X1, low_top-14, COL_W, 'body_sm')
    right_bottom, right_h = draw_para(c, right_text, X2, low_top-14, COL_W, 'body_sm')
    print(f'Action bottoms: left={left_bottom:.1f}, right={right_bottom:.1f}; footer line=65 pt')

    c.setStrokeColor(BORDER); c.setLineWidth(0.6); c.line(M, 65, PAGE_W-M, 65)
    c.setFillColor(NAVY); c.setFont(FONT_BOLD, 6.4)
    c.drawString(M, 58, 'MADT7202 | WEB & SOCIAL NETWORK ANALYTICS | MIDTERM PROJECT')
    c.setFillColor(MUTED); c.setFont(FONT, 6.0)
    c.drawString(M, 46, 'Small creator sample; network associations are not causal evidence.')
    repo_url = 'https://github.com/kanyathat-dev/madt7202-mbti-fashion-vibe-network'
    colab_url = ('https://colab.research.google.com/github/kanyathat-dev/madt7202-mbti-fashion-vibe-network/'
                 'blob/main/MBTI_Fashion_Vibe_Network_Textbook_and_Code_Colab.ipynb')
    right_x = M + 287
    draw_para(c, f'<b>GitHub:</b> <link href="{repo_url}" color="#2B507F"><u>Repository ↗</u></link>', right_x, 61, PAGE_W-M-right_x, 'link')
    draw_para(c, f'<b>Colab:</b> <link href="{colab_url}" color="#2B507F"><u>Open executable notebook ↗</u></link>', right_x, 51, PAGE_W-M-right_x, 'link')
    c.showPage(); c.save()
    return {'path': str(output_path), 'bytes': output_path.stat().st_size,
            'layout': {'data_bottom': round(data_bottom, 1), 'graph_bottom': round(graph_bottom, 1),
                       'actions_bottom': round(min(left_bottom, right_bottom), 1)},
            'thresholds': m['thresholds']}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='6810424002_Kanyathat Rakdee_MBTI_Fashion_Room_Network_Analytics_Midterm.pdf')
    parser.add_argument('--graph', default='mbti_network_topology_labeled.png')
    parser.add_argument('--root', default='.')
    args = parser.parse_args()
    print(build_report(Path(args.output), Path(args.graph), Path(args.root)))
