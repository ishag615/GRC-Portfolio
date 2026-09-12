# risk_analyzer.py
# Calculates risk scores, levels, and highlights risks above appetite threshold.

from __future__ import annotations

from pathlib import Path
from typing import Any

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
    raise TypeError('Unsupported data type for risk analysis')


def _risk_level(score: float) -> str:
    if score >= 16:
        return 'Critical'
    if score >= 10:
        return 'High'
    if score >= 5:
        return 'Medium'
    return 'Low'


def load_risk_register(filepath: str | Path) -> pd.DataFrame:
    path = Path(filepath)
    if not path.is_absolute():
        path = (PROJECT_ROOT / path).resolve()
    df = pd.read_excel(path, sheet_name='Register')
    df = df.copy()
    df['Likelihood (1-5)'] = pd.to_numeric(df['Likelihood (1-5)'], errors='coerce').fillna(0)
    df['Impact (1-5)'] = pd.to_numeric(df['Impact (1-5)'], errors='coerce').fillna(0)
    df['Risk Score'] = df['Likelihood (1-5)'] * df['Impact (1-5)']
    df['Risk Level'] = df['Risk Score'].apply(_risk_level)
    return df


def calculate_risk_summary(data: Any) -> dict[str, dict[str, Any]]:
    df = _coerce_frame(data)
    summary: dict[str, dict[str, Any]] = {}
    for index, row in df.iterrows():
        risk_id = str(row.get('Risk ID', f'R-{index + 1}'))
        likelihood = pd.to_numeric(row.get('Likelihood (1-5)', 0), errors='coerce')
        impact = pd.to_numeric(row.get('Impact (1-5)', 0), errors='coerce')
        score = float(likelihood * impact)
        level = _risk_level(score)
        summary[risk_id] = {
            'risk_id': risk_id,
            'risk_name': row.get('Risk Name', 'Unnamed Risk'),
            'likelihood': float(likelihood),
            'impact': float(impact),
            'score': int(score),
            'risk_level': level,
            'owner': row.get('Owner', 'Unassigned'),
            'treatment': row.get('Treatment', 'TBD'),
        }
    return summary


def identify_risks_above_appetite(summary: dict[str, dict[str, Any]], threshold: int = 9) -> list[str]:
    return [risk_id for risk_id, info in summary.items() if info.get('score', 0) > threshold]


def print_risk_summary(summary: dict[str, dict[str, Any]], threshold: int = 9) -> None:
    print('\n=== RISK REGISTER SUMMARY ===')
    counts = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
    for info in summary.values():
        level = info.get('risk_level', 'Low')
        if level in counts:
            counts[level] += 1
    for level in ['Critical', 'High', 'Medium', 'Low']:
        print(f'{level}: {counts[level]}')
    above = identify_risks_above_appetite(summary, threshold)
    print(f'Risks above appetite threshold ({threshold}): {len(above)}')
    for risk_id in above:
        out = summary[risk_id]
        print(f' - {risk_id}: {out["risk_name"]} ({out["score"]})')


def main() -> None:
    risk_path = ASSESSMENTS_DIR / 'Risk Register.xlsx'
    risk_df = load_risk_register(risk_path)
    print(f'✓ Loaded {len(risk_df)} risks from the risk register')
    risk_summary = calculate_risk_summary(risk_df)
    print_risk_summary(risk_summary)


if __name__ == '__main__':
    main()