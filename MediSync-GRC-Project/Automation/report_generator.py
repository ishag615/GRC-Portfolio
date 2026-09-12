# report_generator.py
# Generates a formatted PDF compliance report for the MediSync dashboard.

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

try:
    from .compliance_checker import (
        ASSESSMENTS_DIR,
        calculate_iso_compliance,
        calculate_nist_compliance,
        load_iso_controls,
        load_nist_assessment,
    )
    from .risk_analyzer import calculate_risk_summary, identify_risks_above_appetite, load_risk_register
except ImportError:
    from compliance_checker import (
        ASSESSMENTS_DIR,
        calculate_iso_compliance,
        calculate_nist_compliance,
        load_iso_controls,
        load_nist_assessment,
    )
    from risk_analyzer import calculate_risk_summary, identify_risks_above_appetite, load_risk_register


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / 'Output'


def _build_summary_table(report_data: dict[str, Any]) -> Table:
    nist_score = report_data.get('nist_score', 0)
    iso_score = report_data.get('iso_score', 0)
    rows = [
        ['Framework', 'Overall Compliance', 'Assessment'],
        ['NIST CSF 2.0', f'{nist_score:.1f}%', 'Current profile'],
        ['ISO 27001', f'{iso_score:.1f}%', 'Control implementation'],
    ]
    table = Table(rows, colWidths=[200, 150, 170])
    table.setStyle(
        TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
    )
    return table


def _wrap_paragraph_text(value: Any, max_chars: int = 30) -> str:
    text = str(value).strip()
    if not text:
        return ''
    words = text.split()
    if not words:
        return ''

    lines: list[str] = []
    current = ''
    for word in words:
        if len(current) + len(word) + (1 if current else 0) <= max_chars:
            current = f'{current} {word}'.strip()
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return '<br/>'.join(lines)


def _build_gap_table(top_gaps: list[dict[str, Any]]) -> Table:
    cell_style = ParagraphStyle(
        'GapCell',
        fontName='Helvetica',
        fontSize=8.2,
        leading=9,
        alignment=1,
        spaceBefore=0,
        spaceAfter=0,
        wordWrap='CJK',
        borderPadding=4,
    )

    rows = [['Priority', 'Subcategory', 'Current', 'Target', 'Action']]
    for gap in top_gaps[:5]:
        rows.append([
            Paragraph(str(gap.get('priority', 'Medium')), cell_style),
            Paragraph(str(gap.get('subcategory', 'N/A')), cell_style),
            Paragraph(str(gap.get('current_maturity', 'N/A')), cell_style),
            Paragraph(_wrap_paragraph_text(gap.get('target_maturity', 'N/A'), max_chars=18), cell_style),
            Paragraph(_wrap_paragraph_text(gap.get('remediation', 'TBD'), max_chars=34), cell_style),
        ])

    table = Table(rows, colWidths=[55, 100, 60, 90, 250], repeatRows=1)
    table.setStyle(
        TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1D4ED8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (2, 1), (-1, -1), 'CENTER'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ])
    )
    return table


def _build_risk_table(risk_summary: dict[str, dict[str, Any]]) -> Table:
    rows = [['Risk ID', 'Risk Level', 'Likelihood', 'Impact', 'Score']]
    for risk_id, info in sorted(risk_summary.items(), key=lambda item: item[1].get('score', 0), reverse=True)[:8]:
        rows.append([
            risk_id,
            info.get('risk_level', 'Low'),
            str(info.get('likelihood', 0)),
            str(info.get('impact', 0)),
            str(info.get('score', 0)),
        ])
    table = Table(rows, colWidths=[80, 90, 80, 80, 70])
    table.setStyle(
        TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#14532D')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0FDF4')]),
        ])
    )
    return table


def generate_pdf_report(report_data: dict[str, Any], output_path: str | Path | None = None) -> Path:
    project_root = PROJECT_ROOT
    if output_path is None:
        output_path = project_root / 'Output' / 'Compliance-Report.pdf'
    target_path = Path(output_path)
    if not target_path.is_absolute():
        target_path = (project_root / target_path).resolve()
    target_path.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=24, leading=30, textColor=colors.HexColor('#0F172A'))
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#475569'))
    section_style = ParagraphStyle('Section', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#1D4ED8'), leading=20)

    doc = SimpleDocTemplate(
        str(target_path),
        pagesize=(letter[0], letter[1]),
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    story = []

    story.append(Paragraph('MediSync Solutions', title_style))
    story.append(Paragraph('GRC Compliance Monitoring Report', subtitle_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f'Report Date: {report_data.get("generated_at", datetime.now().strftime("%B %d, %Y"))}', styles['Normal']))
    story.append(Paragraph(f'Generated By: {report_data.get("generated_by", "Automated GRC Dashboard")}', styles['Normal']))
    story.append(Spacer(1, 30))
    story.append(Paragraph('Executive Summary', section_style))
    story.append(_build_summary_table(report_data))
    story.append(Spacer(1, 18))
    story.append(Paragraph('Top 5 Gaps', section_style))
    story.append(_build_gap_table(report_data.get('top_gaps', [])))
    story.append(Spacer(1, 18))
    story.append(Paragraph('Risk Summary', section_style))
    story.append(_build_risk_table(report_data.get('risk_summary', {})))
    story.append(Spacer(1, 18))
    story.append(Paragraph('Recommendations', section_style))
    recommendations = report_data.get('recommendations', [
        'Address all HIGH-priority NIST gaps within the next 30 days.',
        'Prioritize unimplemented ISO 27001 controls mapped to access control and vendor security.',
        'Implement remediation plans for all Critical and High risks.',
        'Schedule recurring access reviews and third-party assurance checks.'
    ])
    for item in recommendations:
        story.append(Paragraph(f'• {item}', styles['BodyText']))
    story.append(Spacer(1, 16))

    doc.build(story)
    print(f'✓ Compliance PDF report saved to {target_path}')
    return target_path


def build_report_data() -> dict[str, Any]:
    nist_df = load_nist_assessment(ASSESSMENTS_DIR / 'NIST-CSF-Gap-Assessment.xlsx')
    iso_df = load_iso_controls(ASSESSMENTS_DIR / 'ISO27001-Controls.xlsx')
    risk_df = load_risk_register(ASSESSMENTS_DIR / 'Risk Register.xlsx')

    nist_score, nist_gaps, nist_high, top_gaps = calculate_nist_compliance(nist_df)
    iso_score, iso_gaps = calculate_iso_compliance(iso_df)
    risk_summary = calculate_risk_summary(risk_df)
    above_appetite = identify_risks_above_appetite(risk_summary)

    recommendations = [
        'Resolve all HIGH-priority NIST gaps within the next 30 days.',
        'Prioritize the unimplemented ISO 27001 controls mapped to access control, vendor security, and incident handling.',
        'Implement remediation plans for every Critical and High risk above the risk appetite threshold.',
        'Conduct quarterly access reviews and vendor assurance checks for PHI-related systems.'
    ]

    return {
        'generated_at': datetime.now().strftime('%B %d, %Y'),
        'generated_by': 'Automated GRC Dashboard',
        'nist_score': nist_score,
        'iso_score': iso_score,
        'nist_gaps': nist_gaps,
        'iso_gaps': iso_gaps,
        'top_gaps': top_gaps,
        'risk_summary': risk_summary,
        'risks_above_appetite': above_appetite,
        'recommendations': recommendations,
    }


if __name__ == '__main__':
    report_data = build_report_data()
    generate_pdf_report(report_data, OUTPUT_DIR / 'Compliance-Report.pdf')