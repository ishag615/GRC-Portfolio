# compliance_checker.py
# GRC Portfolio — Isha Gupta | Kent State University
# Simulates automated compliance monitoring (Drata/Vanta workflow)
# Usage: python3 compliance_checker.py

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSESSMENTS_DIR = PROJECT_ROOT / 'Assessments'


def _coerce_frame(data: Any) -> pd.DataFrame:
    if isinstance(data, pd.DataFrame):
        return data.copy()
    if isinstance(data, list):
        return pd.DataFrame(data)
    if isinstance(data, dict):
        return pd.DataFrame([data])
    raise TypeError('Unsupported data type for score calculation')


def _resolve_path(filepath: str | Path) -> Path:
    path = Path(filepath)
    if not path.is_absolute():
        path = (PROJECT_ROOT / path).resolve()
    return path


def load_nist_assessment(filepath: str | Path) -> pd.DataFrame:
    """Load the NIST CSF profile worksheet and normalize the assessment columns."""
    path = _resolve_path(filepath)
    df = pd.read_excel(path, sheet_name='Current and Target Profile')
    df = df.dropna(subset=['CSF Outcome (Function, Category, or Subcategory)']).copy()
    df['Included in Profile?'] = df['Included in Profile?'].fillna('No').astype(str).str.strip()
    df['Current Status'] = pd.to_numeric(df['Current Status'], errors='coerce')
    df['Target Maturity (1-4)'] = pd.to_numeric(df['Target Maturity (1-4)'], errors='coerce')
    df['Gap (Y/N)'] = df['Gap (Y/N)'].fillna('N').astype(str).str.strip().str.upper()
    df['Priority (High/Medium/Low)'] = (
        df['Priority (High/Medium/Low)'].fillna('Low').astype(str).str.strip().str.title()
    )
    return df


def load_iso_controls(filepath: str | Path) -> pd.DataFrame:
    """Load ISO 27001 control assessment."""
    path = _resolve_path(filepath)
    df = pd.read_excel(path, sheet_name='Sheet1')
    df = df.copy()
    df['Applicable (Yes/No)'] = df['Applicable (Yes/No)'].fillna('No').astype(str).str.strip().str.title()
    df['Implementation Status'] = (
        df['Implementation Status'].fillna('Not Implemented').astype(str).str.strip().str.title()
    )
    return df


def load_top_gaps(filepath: str | Path) -> pd.DataFrame:
    """Load the prioritized NIST gap list."""
    path = _resolve_path(filepath)
    df = pd.read_excel(path, sheet_name='Top Gaps')
    df = df.dropna(subset=['Subcategory']).copy()
    df['Priority'] = df['Priority'].fillna('Medium').astype(str).str.strip().str.title()
    return df


def calculate_nist_compliance(data: Any) -> tuple[float, int, int, list[dict[str, Any]]]:
    """Return (score, total_gaps, high_priority_gaps, top_5_gaps)."""
    df = _coerce_frame(data)
    active = df[df['Included in Profile?'].astype(str).str.strip().str.lower() == 'yes'].copy()
    if active.empty:
        return 0.0, 0, 0, []

    active['Meets_Target'] = (
        pd.to_numeric(active['Current Status'], errors='coerce')
        >= pd.to_numeric(active['Target Maturity (1-4)'], errors='coerce')
    )
    score = round((active['Meets_Target'].mean() * 100), 1)

    gaps = active[active['Gap (Y/N)'].astype(str).str.strip().str.upper() == 'Y'].copy()
    total_gaps = int(len(gaps))
    high_priority = int((gaps['Priority (High/Medium/Low)'].astype(str).str.title() == 'High').sum())

    top_records = gaps[gaps['Priority (High/Medium/Low)'].astype(str).str.title().isin(['High', 'Medium', 'Low'])].copy()
    if top_records.empty:
        top_records = active.head(5).copy()
    priority_rank = {'High': 3, 'Medium': 2, 'Low': 1}
    top_records['Priority Rank'] = top_records['Priority (High/Medium/Low)'].astype(str).str.title().map(priority_rank).fillna(0)
    top_records = top_records.sort_values(
        by=['Priority Rank', 'Current Status', 'Target Maturity (1-4)'],
        ascending=[False, True, False],
    ).head(5)
    top_gaps = []
    for row in top_records.to_dict('records'):
        top_gaps.append({
            'subcategory': row.get('CSF Outcome (Function, Category, or Subcategory)', 'N/A'),
            'priority': row.get('Priority (High/Medium/Low)', 'Medium'),
            'current_maturity': row.get('Current Status', 0),
            'target_maturity': row.get('Target Maturity (1-4)', 0),
            'description': row.get('CSF Outcome Description', 'N/A'),
            'remediation': row.get('Remediation Action', 'N/A'),
        })
    return score, total_gaps, high_priority, top_gaps


def calculate_iso_compliance(data: Any) -> tuple[float, int]:
    """Return (score_percent, controls_not_implemented)."""
    df = _coerce_frame(data)
    applicable = df[df['Applicable (Yes/No)'].astype(str).str.strip().str.title() == 'Yes'].copy()
    if applicable.empty:
        return 0.0, 0
    implemented_mask = applicable['Implementation Status'].astype(str).str.strip().str.title() == 'Implemented'
    implemented_count = int(implemented_mask.sum())
    score = round((implemented_count / len(applicable)) * 100, 1)
    missing = int((~implemented_mask).sum())
    return score, missing


def print_compliance_report(
    nist_score: float,
    nist_gaps: int,
    nist_high: int,
    iso_score: float,
    iso_gaps: int,
    top_gaps: list[dict[str, Any]],
    risk_summary: dict[str, Any],
    risks_above_appetite: int,
) -> None:
    """Print a terminal-friendly compliance update."""
    print('\n' + '=' * 62)
    print('  MEDISYNC SOLUTIONS — COMPLIANCE STATUS REPORT')
    print(f'  Generated: {datetime.now().strftime("%B %d, %Y")}')
    print('  Prepared by: Automated GRC Dashboard')
    print('=' * 62)

    print('\n📊 FRAMEWORK COMPLIANCE SCORES')
    print(f'   NIST CSF 2.0:   {nist_score:.1f}%')
    nist_bar = '█' * int(nist_score / 10) + '░' * max(0, 10 - int(nist_score / 10))
    print(f'   [{nist_bar}]')
    print(f'   ISO 27001:      {iso_score:.1f}%')
    iso_bar = '█' * int(iso_score / 10) + '░' * max(0, 10 - int(iso_score / 10))
    print(f'   [{iso_bar}]')

    print('\n⚠️  COMPLIANCE GAPS')
    print(f'   NIST CSF gaps:     {nist_gaps} total | {nist_high} HIGH priority')
    print(f'   ISO 27001 gaps:    {iso_gaps} controls not implemented')

    print('\n🔍 TOP 5 CRITICAL GAPS')
    if not top_gaps:
        print('   No significant gaps detected.')
    else:
        for idx, gap in enumerate(top_gaps[:5], start=1):
            print(
                f"   {idx}. {gap.get('subcategory', 'N/A')} "
                f"[{gap.get('priority', 'Medium')}]: {gap.get('description', 'No description')}"
            )

    print('\n🎯 RISK SUMMARY')
    counts = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
    for info in risk_summary.values():
        level = info.get('risk_level', 'Low')
        if level in counts:
            counts[level] += 1
    icons = {'Critical': '🔴', 'High': '🟠', 'Medium': '🟡', 'Low': '🟢'}
    for level in ['Critical', 'High', 'Medium', 'Low']:
        print(f"   {icons[level]} {level:<10} {counts[level]}")
    print(f'\n   Risks above appetite threshold: {risks_above_appetite} require treatment')

    print('\n💡 RECOMMENDED ACTIONS')
    print('   1. Resolve all HIGH-priority NIST gaps within the next 30 days.')
    print('   2. Prioritize the unimplemented ISO 27001 controls mapped to A.8 and A.5.')
    print('   3. Initiate remediation plans for all Critical and High risks.')
    print('   4. Schedule monthly access review and vendor assurance checkpoints.')
    print('\n' + '=' * 62)
    print('  Next assessment due: ' + datetime.now().strftime('%B %d, %Y') + ' + 90 days')
    print('=' * 62 + '\n')


def main() -> None:
    print('MediSync GRC Compliance Checker — Starting...\n')

    nist_path = ASSESSMENTS_DIR / 'NIST-CSF-Gap-Assessment.xlsx'
    iso_path = ASSESSMENTS_DIR / 'ISO27001-Controls.xlsx'
    risk_path = ASSESSMENTS_DIR / 'Risk Register.xlsx'

    nist_df = load_nist_assessment(nist_path)
    iso_df = load_iso_controls(iso_path)
    risk_df = pd.read_excel(risk_path, sheet_name='Register')

    print(f'✓ Loaded {len(nist_df)} NIST CSF rows')
    print(f'✓ Loaded {len(iso_df)} ISO 27001 controls')
    print(f'✓ Loaded {len(risk_df)} risks')

    nist_score, nist_gaps, nist_high, top_gaps = calculate_nist_compliance(nist_df)
    iso_score, iso_gaps = calculate_iso_compliance(iso_df)

    try:
        from .risk_analyzer import calculate_risk_summary, identify_risks_above_appetite
    except ImportError:
        from risk_analyzer import calculate_risk_summary, identify_risks_above_appetite

    risk_summary = calculate_risk_summary(risk_df)
    above_appetite = identify_risks_above_appetite(risk_summary)
    print_compliance_report(
        nist_score,
        nist_gaps,
        nist_high,
        iso_score,
        iso_gaps,
        top_gaps,
        risk_summary,
        len(above_appetite),
    )


if __name__ == '__main__':
    main()
