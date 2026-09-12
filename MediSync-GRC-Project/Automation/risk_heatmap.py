# risk_heatmap.py
# Generates a 5x5 risk heat map from the MediSync risk register.

from __future__ import annotations

from pathlib import Path

import matplotlib
import matplotlib.patches as mpatches
import pandas as pd

matplotlib.use('Agg')
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSESSMENTS_DIR = PROJECT_ROOT / 'Assessments'
OUTPUT_DIR = PROJECT_ROOT / 'Output'


def _risk_level(score: float) -> str:
    if score >= 16:
        return 'Critical'
    if score >= 10:
        return 'High'
    if score >= 5:
        return 'Medium'
    return 'Low'


def _risk_color(score: float) -> str:
    if score >= 16:
        return '#EF4444'
    if score >= 10:
        return '#F97316'
    if score >= 5:
        return '#EAB308'
    return '#22C55E'


def generate_heatmap(filepath: str | Path, output_path: str | Path | None = None) -> Path:
    path = Path(filepath)
    if not path.is_absolute():
        path = (PROJECT_ROOT / path).resolve()
    df = pd.read_excel(path, sheet_name='Register')
    df = df.copy()
    df['Likelihood'] = pd.to_numeric(df['Likelihood (1-5)'], errors='coerce').fillna(0)
    df['Impact'] = pd.to_numeric(df['Impact (1-5)'], errors='coerce').fillna(0)
    df['Score'] = df['Likelihood'] * df['Impact']
    df['Risk Level'] = df['Score'].apply(_risk_level)
    df['Color'] = df['Score'].apply(_risk_color)

    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor('#111827')
    ax.set_facecolor('#0F172A')

    for i in range(1, 6):
        for j in range(1, 6):
            score = i * j
            if score >= 16:
                bg = '#3F0D12'
            elif score >= 10:
                bg = '#431407'
            elif score >= 5:
                bg = '#443800'
            else:
                bg = '#052E16'
            rect = plt.Rectangle((j - 0.5, i - 0.5), 1, 1, color=bg, zorder=0)
            ax.add_patch(rect)

    for _, row in df.iterrows():
        ax.scatter(
            row['Impact'],
            row['Likelihood'],
            color=row['Color'],
            s=120,
            zorder=5,
            edgecolors='white',
            linewidths=0.7,
        )
        ax.annotate(
            str(row.get('Risk ID', 'N/A')),
            (row['Impact'], row['Likelihood']),
            textcoords='offset points',
            xytext=(6, 4),
            fontsize=7,
            color='white',
        )

    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0.5, 5.5)
    ax.set_xticks(range(1, 6))
    ax.set_yticks(range(1, 6))
    ax.set_xlabel('Impact', color='white', fontsize=12)
    ax.set_ylabel('Likelihood', color='white', fontsize=12)
    ax.set_title('MediSync Solutions — Risk Heat Map', color='white', fontsize=14, fontweight='bold', pad=15)
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('#475569')

    legend_elements = [
        mpatches.Patch(color='#EF4444', label='Critical (16-25)'),
        mpatches.Patch(color='#F97316', label='High (10-15)'),
        mpatches.Patch(color='#EAB308', label='Medium (5-9)'),
        mpatches.Patch(color='#22C55E', label='Low (1-4)'),
    ]
    ax.legend(
        handles=legend_elements,
        loc='upper left',
        facecolor='#111827',
        labelcolor='white',
        framealpha=0.85,
    )

    if output_path is None:
        output_path = OUTPUT_DIR / 'Risk-Heatmap.png'
    target_path = Path(output_path)
    if not target_path.is_absolute():
        target_path = (PROJECT_ROOT / target_path).resolve()
    target_path.parent.mkdir(parents=True, exist_ok=True)

    plt.tight_layout()
    plt.savefig(str(target_path), dpi=150, bbox_inches='tight', facecolor='#111827')
    plt.close(fig)
    print(f'✓ Risk heatmap saved to {target_path}')
    return target_path


if __name__ == '__main__':
    generate_heatmap(ASSESSMENTS_DIR / 'Risk Register.xlsx', OUTPUT_DIR / 'Risk-Heatmap.png')