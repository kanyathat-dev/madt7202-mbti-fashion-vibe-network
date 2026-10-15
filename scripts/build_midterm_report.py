#!/usr/bin/env python3
"""Build a one-page MADT7202 midterm report in the user's reference layout.

When executed from the project root after the notebook, it reads the generated
metrics/sensitivity CSVs and uses the fresh network figure produced by the notebook.
"""
from __future__ import annotations
import argparse
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import Paragraph, Table, TableStyle, Image as RLImage
from reportlab.pdfgen import canvas

NAVY = colors.HexColor('#1F3454')
BLUE = colors.HexColor('#2B507F')
ORANGE = colors.HexColor('#E87500')
PALE_BLUE = colors.HexColor('#F1F5FA')
PALE_ORANGE = colors.HexColor('#FFF7EB')
BORDER = colors.HexColor('#D5DFEA')
BODY = colors.HexColor('#28374B')
MUTED = colors.HexColor('#607086')
WHITE = colors.white
PAGE_W, PAGE_H = A4

STYLES = {
    'body': ParagraphStyle('body', fontName='Helvetica', fontSize=7.1, leading=8.55,
                           textColor=BODY, alignment=TA_LEFT, spaceAfter=0),
    'body_small': ParagraphStyle('body_small', fontName='Helvetica', fontSize=6.0, leading=7.0,
                                  textColor=BODY, alignment=TA_LEFT, spaceAfter=0),
    'table_body': ParagraphStyle('table_body', fontName='Helvetica', fontSize=6.15, leading=7.2,
                                 textColor=BODY, alignment=TA_LEFT, spaceAfter=0),
    'table_label': ParagraphStyle('table_label', fontName='Helvetica-Bold', fontSize=6.05,
                                  leading=7.1, textColor=BLUE, alignment=TA_LEFT, spaceAfter=0),
    'card_heading': ParagraphStyle('card_heading', fontName='Helvetica-Bold', fontSize=7.1,
                                   leading=8.2, textColor=ORANGE, spaceAfter=2),
    'card_body': ParagraphStyle('card_body', fontName='Helvetica', fontSize=6.5, leading=7.7,
                                textColor=BODY, spaceAfter=0),
}

def para(text, style='body'):
    return Paragraph(text, STYLES[style] if isinstance(style, str) else style)

def draw_section(c, x, top, title, width):
    c.setFillColor(ORANGE)
    c.setFont('Helvetica-Bold', 9.0)
    c.drawString(x, top, title.upper())
    c.setStrokeColor(colors.HexColor('#E8CBA7'))
    c.setLineWidth(0.55)
    c.line(x, top - 5.5, x + width, top - 5.5)

def draw_para(c, text, x, top, width, style='body'):
    p = para(text, style)
    _, h = p.wrap(width, 500)
    p.drawOn(c, x, top - h)
    return top - h

def make_table(rows, width, label_width, font='table_body', padd=4):
    data = [[para(label, 'table_label'), para(txt, font)] for label, txt in rows]
    t = Table(data, colWidths=[label_width, width-label_width], hAlign='LEFT')
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,-1), PALE_BLUE),
        ('BACKGROUND', (1,0), (1,-1), WHITE),
        ('LINEBELOW', (0,0), (-1,-2), 0.45, BORDER),
        ('BOX', (0,0), (-1,-1), 0.45, BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), padd),
        ('RIGHTPADDING', (0,0), (-1,-1), padd),
        ('TOPPADDING', (0,0), (-1,-1), 3.3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.3),
    ]))
    return t

def draw_card(c, x, top, width, height, title, heading, body, accent, bg):
    c.setFillColor(bg)
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.55)
    c.roundRect(x, top-height, width, height, 2.0, stroke=1, fill=1)
    c.setFillColor(accent)
    c.rect(x, top-height, 2.4, height, stroke=0, fill=1)
    tx = x + 8
    p1 = para(title, 'card_heading')
    _, h1 = p1.wrap(width-15, height)
    p1.drawOn(c, tx, top-7-h1)
    p2 = para(heading, ParagraphStyle('dynamic_heading', parent=STYLES['card_body'],
                 fontName='Helvetica-Bold', fontSize=7.25, leading=8.2, textColor=NAVY))
    _, h2 = p2.wrap(width-15, height)
    y = top - 10 - h1 - h2
    p2.drawOn(c, tx, y)
    p3 = para(body, 'card_body')
    _, h3 = p3.wrap(width-15, height)
    p3.drawOn(c, tx, y - h3 - 3)

def read_metrics(root: Path):
    """Use regenerated CSV outputs when available; baseline values are CI-asserted."""
    result = {
        'images': 67, 'evidence_rows': 268, 'creator_count': 6,
        'anchor': 'Clean-Traditional', 'anchor_degree': 8, 'anchor_coverage': 28,
        'anchor_bc': 0.0456, 'bridge': 'Playful-Streetwear', 'bridge_bc': 0.3134,
        'bridge_load': 33.0, 'no_overlap': 58, 'total_pairs': 120,
        'loco_top_count': 4, 'loco_total': 6,
        'loco_alternatives': 'Soft-Romantic and Dark-Perfectionist',
        'thresholds': [
            'Threshold 2: 14 edges; largest component 7 nodes; 111/113 no-overlap pairs unreachable.',
            'Threshold 3: 2 edges; largest component 3 nodes; 119/119 no-overlap pairs unreachable.',
        ],
    }
    metrics_path = root / 'mbti_vibe_network_metrics.csv'
    image_path = root / 'mbti_fashion_image_level.csv'
    loco_path = root / 'leave_one_creator_out_sensitivity.csv'
    thresh_path = root / 'npmi_threshold_sensitivity.csv'
    try:
        import pandas as pd
        if metrics_path.exists():
            m = pd.read_csv(metrics_path)
            ar = m.loc[m['Fashion Vibe'] == result['anchor']].iloc[0]
            br = m.loc[m['Fashion Vibe'] == result['bridge']].iloc[0]
            result['anchor_degree'] = int(ar['Degree'])
            result['anchor_coverage'] = int(ar['Pairs covered (of 120)'])
            result['anchor_bc'] = float(ar['Betweenness (dist=1/NPMI)'])
            result['bridge_bc'] = float(br['Betweenness (dist=1/NPMI)'])
            result['bridge_load'] = float(br['Bridge Load (fractional path-load units)'])
        if image_path.exists():
            df = pd.read_csv(image_path)
            result['images'] = int(df['image_id'].nunique())
            result['creator_count'] = int(df['creator'].nunique())
        if loco_path.exists():
            lo = pd.read_csv(loco_path)
            result['loco_total'] = len(lo)
            result['loco_top_count'] = int((lo['Top bridge'] == result['bridge']).sum())
            alternatives = [str(x) for x in lo['Top bridge'].value_counts().index if x != result['bridge']]
            if alternatives:
                result['loco_alternatives'] = ' and '.join(alternatives[:2])
        if thresh_path.exists():
            th = pd.read_csv(thresh_path)
            rows = []
            for _, r in th.iterrows():
                threshold = int(r['Minimum co-occurrence'])
                if threshold == 1:
                    continue
                rows.append(
                    f"Threshold {threshold}: {int(r['Retained edges'])} edges; largest component "
                    f"{int(r['Largest component (nodes)'])} nodes; "
                    f"{int(r['Unreachable no-overlap pairs'])}/"
                    f"{int(r['No-direct-overlap pairs (of 120)'])} no-overlap pairs unreachable."
                )
            if rows:
                result['thresholds'] = rows
    except Exception as exc:
        print(f'Warning: generated CSV metrics could not be loaded; using checked baseline values: {exc}')
    return result

def build_report(output_path: Path, graph_path: Path, root: Path):
    m = read_metrics(root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(output_path), pagesize=A4, invariant=1)
    c.setTitle('MBTI-Fashion Vibe Network - Corrected Midterm Report')
    c.setAuthor('Kanyathat Rakdee')
    c.setSubject('MADT7202 Midterm Project - CSV-verified network analysis')

    c.setFillColor(NAVY)
    c.setFont('Helvetica-Bold', 17.2)
    c.drawString(28, 808, 'MBTI-FASHION VIBE NETWORK')
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 8.4)
    c.drawString(29, 793, 'Living Room Anchor & Compromise Bridge for Newlyweds')
    c.setFont('Helvetica', 6.7)
    c.drawString(29, 779, 'MADT7202 | Web & Social Network Analytics | Midterm Project')
    c.setFillColor(NAVY)
    c.setFont('Helvetica-Bold', 8.2)
    c.drawRightString(PAGE_W-28, 779, 'Kanyathat Rakdee | 6810424002')
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.5)
    c.line(28, 769, PAGE_W-28, 769)

    col_gap = 15
    col_w = (PAGE_W - 56 - col_gap) / 2
    x1, x2 = 28, 28 + col_w + col_gap

    draw_section(c, x1, 750, '01 The Decision', col_w)
    draw_para(c,
        'As a Lead Design Strategist, shortlist a primary living-room style (the <b>Living Room Anchor</b>) '
        'and potential bridge styles for newlyweds with different MBTI labels. The results can inform furniture '
        'collection planning and a future recommendation engine.', x1, 736, col_w, 'body')

    draw_section(c, x2, 750, '02 Why a Network', col_w)
    draw_para(c,
        'Frequency alone does not show which MBTI categories share observed Vibe links. A <b>bipartite network</b> '
        'and weighted shortest paths identify structural bridges for pairs with no shared direct Vibe. These are '
        'patterns in coded data, not proof of psychological compatibility or customer preference.', x2, 736, col_w, 'body')

    data_top = 674
    draw_section(c, x1, data_top, '03 Data', col_w)
    data_rows = [
        ('Sources', f"{m['images']} public TikTok lookbook images ({m['evidence_rows']} coded observations) from six anonymized creator labels (A-F)."),
        ('Traceability', 'CSV is the source of truth; 67/67 raw filenames were found. Proxy-to-pixel correspondence is not independently verified.'),
        ('Period', '27 September to 7 October 2026.'),
        ('Coding / bias', 'Gemini-assisted Vibe coding; Vibe-to-Room-Style mapping is researcher-defined. 65/67 images came from four main creators.'),
    ]
    t1 = make_table(data_rows, col_w, 64)
    _, th1 = t1.wrap(col_w, 400)
    t1.drawOn(c, x1, data_top-14-th1)

    draw_section(c, x2, data_top, '04 Graph Construction', col_w)
    threshold_text = ' '.join(m['thresholds'])
    graph_rows = [
        ('Nodes / edges', '16 MBTI square nodes + 12 Fashion Vibe circle nodes; 28 nodes in total.'),
        ('Weighting', 'Image-level NPMI, N = 67; shortest-path distance d = 1/NPMI for positive edges.'),
        ('Pruning / overlap', 'Retain NPMI > 0; 51/51 observed edges retained. Separately, 58/120 MBTI pairs (48.3%) have no shared direct Vibe; this is not Bridge Load.'),
        ('Sensitivity', threshold_text),
    ]
    t2 = make_table(graph_rows, col_w, 67, font='body_small', padd=3.7)
    _, th2 = t2.wrap(col_w, 420)
    t2.drawOn(c, x2, data_top-14-th2)
    print(f'Data table height: {th1:.1f} pt; graph table height: {th2:.1f} pt')

    graph_top = 553
    draw_section(c, 28, graph_top, '05 The Graph', PAGE_W-56)
    graph_path = Path(graph_path)
    if not graph_path.exists():
        raise FileNotFoundError(f'Network image is required: {graph_path}')
    img = RLImage(str(graph_path))
    native_ratio = img.imageWidth / img.imageHeight
    graph_w = 365
    graph_h = graph_w / native_ratio
    graph_x = (PAGE_W - graph_w) / 2
    graph_y = 317
    img.drawWidth, img.drawHeight = graph_w, graph_h
    img.drawOn(c, graph_x, graph_y)
    c.setFillColor(MUTED)
    c.setFont('Helvetica-Oblique', 6.4)
    c.drawCentredString(PAGE_W/2, 309,
        'ESTJ x INFP have zero direct overlap; selected weighted shortest-path sequence:')
    c.setFont('Helvetica-BoldOblique', 6.5)
    c.drawCentredString(PAGE_W/2, 300,
        'Sharp-Tailored -> Dark-Perfectionist -> Earthy-Raw')

    draw_section(c, 28, 281, '06 Findings', PAGE_W-56)
    card_y, card_h, gap = 269, 76, 8
    card_w = (PAGE_W-56-2*gap)/3
    bx1, bx2, bx3 = 28, 28+card_w+gap, 28+2*(card_w+gap)
    draw_card(c, bx1, card_y, card_w, card_h,
        'HUB / ANCHOR CANDIDATE', 'Clean-Traditional | 23.3%',
        f"- Degree: {m['anchor_degree']}<br/>- MBTI-pair coverage: {m['anchor_coverage']}/120<br/>- Weighted betweenness: {m['anchor_bc']:.4f}",
        BLUE, PALE_BLUE)
    draw_card(c, bx2, card_y, card_w, card_h,
        'TOP STRUCTURAL BRIDGE', 'Playful-Streetwear',
        f"- Weighted betweenness: {m['bridge_bc']:.4f}<br/>- Bridge Load: {m['bridge_load']:.1f} fractional path-load units<br/>- Top bridge in {m['loco_top_count']} of {m['loco_total']} creator-removal runs",
        ORANGE, PALE_BLUE)
    draw_card(c, bx3, card_y, card_w, card_h,
        'EXAMPLE MEDIATION', 'ESTJ x INFP',
        'Zero direct overlap in the observed graph.<br/>Path: Sharp-Tailored -> Dark-Perfectionist -> Earthy-Raw.',
        ORANGE, PALE_ORANGE)

    lower_top = 178
    draw_section(c, x1, lower_top, '07 Recommended Action', col_w)
    draw_para(c,
        '- Use Clean-Traditional as an anchor candidate (Classic Contemporary / Hamptons-inspired direction).<br/>'
        '- Test Playful-Streetwear alongside Soft-Romantic and Dark-Perfectionist; do not treat a single style as a universal answer.<br/>'
        '- Keep d = 1/NPMI as exploratory recommendation logic, subject to validation with couples.',
        x1, lower_top-14, col_w, 'body_small')

    draw_section(c, x2, lower_top, '08 What Would Change My Mind', col_w)
    draw_para(c,
        f"- Leave-One-Creator-Out: {m['bridge']} leads in {m['loco_top_count']}/{m['loco_total']} runs; {m['loco_alternatives']} lead in the other runs, so the ranking is sensitive to creator composition.<br/>"
        '- Threshold tests fragment the graph; alternative top-bridge names under stricter thresholds are not reliable recommendations.<br/>'
        '- A showroom A/B test with 100 couples is proposed future validation, not a completed experiment.',
        x2, lower_top-14, col_w, 'body_small')

    c.setStrokeColor(BORDER)
    c.setLineWidth(0.6)
    c.line(28, 47, PAGE_W-28, 47)
    c.setFillColor(NAVY)
    c.setFont('Helvetica-Bold', 5.7)
    c.drawString(28, 36, 'MADT7202 | WEB & SOCIAL NETWORK ANALYTICS | MIDTERM PROJECT')
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 5.7)
    c.drawString(28, 26, 'Exploratory findings from a small creator-concentrated sample; co-occurrence and centrality are not causal evidence.')
    c.setFillColor(NAVY)
    c.setFont('Helvetica-Bold', 5.7)
    c.drawString(338, 36, 'GitHub: kanyathat-dev/madt7202-mbti-fashion-vibe-network')
    c.setFillColor(BLUE)
    c.setFont('Helvetica', 5.7)
    c.drawString(338, 26, 'CSV traceability, staged Notebook, and reproducible sensitivity tests')
    c.linkURL('https://github.com/kanyathat-dev/madt7202-mbti-fashion-vibe-network', (334, 20, PAGE_W-28, 43), relative=0, thickness=0)
    c.save()
    return {'path': str(output_path), 'bytes': output_path.stat().st_size, 'graph': str(graph_path),
            'metric_values': {k:m[k] for k in ('anchor_degree','anchor_coverage','anchor_bc','bridge_bc','bridge_load','no_overlap','loco_top_count','loco_total','thresholds')}}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='6810424002_Kanyathat_Rakdee_MBTI_Fashion_Room_Network_Analytics_Midterm_CORRECTED.pdf')
    parser.add_argument('--graph', default='mbti_network_topology_labeled.png')
    parser.add_argument('--root', default='.')
    args = parser.parse_args()
    print(build_report(Path(args.output), Path(args.graph), Path(args.root)))