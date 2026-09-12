from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

try:
    from Automation.compliance_checker import (
        calculate_iso_compliance,
        calculate_nist_compliance,
        load_iso_controls,
        load_nist_assessment,
    )
    from Automation.report_generator import generate_pdf_report
    from Automation.risk_analyzer import (
        calculate_risk_summary,
        identify_risks_above_appetite,
        load_risk_register,
    )
except ImportError:
    from compliance_checker import (
        calculate_iso_compliance,
        calculate_nist_compliance,
        load_iso_controls,
        load_nist_assessment,
    )
    from report_generator import generate_pdf_report
    from risk_analyzer import (
        calculate_risk_summary,
        identify_risks_above_appetite,
        load_risk_register,
    )


PROJECT_ROOT = Path(__file__).resolve().parent
ASSESSMENTS_DIR = PROJECT_ROOT / 'Assessments'
OUTPUT_DIR = PROJECT_ROOT / 'Output'
OUTPUT_DIR.mkdir(exist_ok=True)


@st.cache_data
def load_dashboard_data() -> dict:
    nist_df = load_nist_assessment(ASSESSMENTS_DIR / 'NIST-CSF-Gap-Assessment.xlsx')
    iso_df = load_iso_controls(ASSESSMENTS_DIR / 'ISO27001-Controls.xlsx')
    risk_df = load_risk_register(ASSESSMENTS_DIR / 'Risk Register.xlsx')

    nist_score, nist_gaps, nist_high, top_gaps = calculate_nist_compliance(nist_df)
    iso_score, iso_gaps = calculate_iso_compliance(iso_df)
    risk_summary = calculate_risk_summary(risk_df)
    above_appetite = identify_risks_above_appetite(risk_summary)

    risk_df = risk_df.copy()
    risk_df['Risk Score'] = pd.to_numeric(risk_df['Likelihood (1-5)'], errors='coerce') * pd.to_numeric(risk_df['Impact (1-5)'], errors='coerce')
    risk_df['Risk Level'] = risk_df['Risk Score'].apply(
        lambda score: 'Critical' if score >= 16 else 'High' if score >= 10 else 'Medium' if score >= 5 else 'Low'
    )

    return {
        'nist_score': nist_score,
        'nist_gaps': nist_gaps,
        'nist_high': nist_high,
        'iso_score': iso_score,
        'iso_gaps': iso_gaps,
        'top_gaps': top_gaps,
        'risk_summary': risk_summary,
        'risk_df': risk_df,
        'above_appetite_count': len(above_appetite),
        'above_appetite_ids': above_appetite,
    }


def make_risk_heatmap(risk_df: pd.DataFrame) -> go.Figure:
    plot_df = risk_df.copy()
    plot_df['Likelihood'] = pd.to_numeric(plot_df['Likelihood (1-5)'], errors='coerce').fillna(0)
    plot_df['Impact'] = pd.to_numeric(plot_df['Impact (1-5)'], errors='coerce').fillna(0)
    plot_df['Score'] = plot_df['Likelihood'] * plot_df['Impact']
    plot_df['Level'] = plot_df['Score'].apply(
        lambda score: 'Critical' if score >= 16 else 'High' if score >= 10 else 'Medium' if score >= 5 else 'Low'
    )
    color_map = {
        'Critical': '#EF4444',
        'High': '#F97316',
        'Medium': '#EAB308',
        'Low': '#22C55E',
    }
    plot_df['Color'] = plot_df['Level'].map(color_map)

    fig = go.Figure()
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
            fig.add_shape(
                type='rect',
                x0=j - 0.5,
                x1=j + 0.5,
                y0=i - 0.5,
                y1=i + 0.5,
                line=dict(color='rgba(255,255,255,0.08)', width=1),
                fillcolor=bg,
                opacity=0.9,
            )

    fig.add_trace(
        go.Scatter(
            x=plot_df['Impact'],
            y=plot_df['Likelihood'],
            mode='markers+text',
            text=plot_df['Risk ID'],
            textposition='top center',
            marker=dict(
                size=14,
                color=plot_df['Color'],
                line=dict(color='white', width=1),
                symbol='circle',
                opacity=0.92,
            ),
            hovertemplate=(
                '<b>%{text}</b><br>'
                'Likelihood: %{y}<br>'
                'Impact: %{x}<br>'
                'Score: %{customdata[0]}<br>'
                'Level: %{customdata[1]}<extra></extra>'
            ),
            customdata=plot_df[['Score', 'Level']].values,
        )
    )

    fig.update_layout(
        title='MediSync Risk Heat Map',
        template='plotly_dark',
        xaxis=dict(title='Impact', range=[0.5, 5.5], tickmode='array', tickvals=[1, 2, 3, 4, 5]),
        yaxis=dict(title='Likelihood', range=[0.5, 5.5], tickmode='array', tickvals=[1, 2, 3, 4, 5]),
        width=850,
        height=620,
        paper_bgcolor='#111827',
        plot_bgcolor='#111827',
        margin=dict(l=40, r=20, t=60, b=60),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0),
    )
    return fig


def priority_rank(priority: str) -> int:
    return {'High': 3, 'Medium': 2, 'Low': 1}.get(str(priority).title(), 0)


def wrap_text(value: str, width: int = 42) -> str:
    if pd.isna(value):
        return ''
    text = str(value)
    words = text.split()
    if not words:
        return ''
    lines: list[str] = []
    current = ''
    for word in words:
        if len(current) + len(word) + (1 if current else 0) <= width:
            current = f'{current} {word}'.strip()
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return '\n'.join(lines)


def main() -> None:
    st.set_page_config(page_title='MediSync GRC Dashboard', page_icon='🛡️', layout='wide')
    data = load_dashboard_data()

    st.title('MediSync Solutions — GRC Dashboard')
    st.caption('Automated compliance monitoring with NIST CSF, ISO 27001, and risk oversight')

    cols = st.columns(2)
    with cols[0]:
        st.subheader('NIST CSF 2.0')
        st.metric('Overall Score', f"{data['nist_score']:.1f}%")
        st.progress(data['nist_score'] / 100)
        st.caption(f'{data["nist_gaps"]} total gaps | {data["nist_high"]} high-priority gaps')

    with cols[1]:
        st.subheader('ISO 27001')
        st.metric('Overall Score', f"{data['iso_score']:.1f}%")
        st.progress(data['iso_score'] / 100)
        st.caption(f'{data["iso_gaps"]} controls not implemented')

    st.markdown('---')

    left_col, right_col = st.columns([1.4, 1])

    with left_col:
        st.subheader('Top Gaps by Priority')
        gap_df = pd.DataFrame(data['top_gaps'])
        if not gap_df.empty:
            gap_df['Priority Rank'] = gap_df['priority'].apply(priority_rank)
            gap_df = gap_df.sort_values(['Priority Rank', 'current_maturity'], ascending=[False, True])
            gap_df = gap_df[['priority', 'subcategory', 'description', 'remediation']].copy()
            gap_df.columns = ['Priority', 'Subcategory', 'Description', 'Remediation']
            gap_df['Description'] = gap_df['Description'].apply(lambda x: wrap_text(x, 42))
            gap_df['Remediation'] = gap_df['Remediation'].apply(lambda x: wrap_text(x, 42))
            st.dataframe(
                gap_df,
                width='stretch',
                hide_index=True,
                column_config={
                    'Description': st.column_config.TextColumn('Description', width='large'),
                    'Remediation': st.column_config.TextColumn('Remediation', width='large'),
                },
            )
        else:
            st.info('No significant control gaps were identified.')

    with right_col:
        st.subheader('Risk Appetite')
        st.metric('Above Threshold', data['above_appetite_count'])
        risk_levels = ['Critical', 'High', 'Medium', 'Low']
        counts = {level: int((pd.Series(data['risk_summary']).apply(lambda x: x.get('risk_level')).eq(level)).sum()) for level in risk_levels}
        for level in risk_levels:
            st.markdown(f"{level}: **{counts[level]}**")

    st.markdown('---')

    st.subheader('Risk Heat Map')
    if not data['risk_df'].empty:
        fig = make_risk_heatmap(data['risk_df'])
        st.plotly_chart(fig, width='stretch')
    else:
        st.warning('No risk data available.')

    st.markdown('---')

    st.subheader('Risk Register')
    risk_table = data['risk_df'].copy()
    level_filter = st.selectbox('Filter by risk level', ['All', 'Critical', 'High', 'Medium', 'Low'])
    if level_filter != 'All':
        risk_table = risk_table[risk_table['Risk Level'] == level_filter]
    display_cols = ['Risk ID', 'Risk Name', 'Likelihood (1-5)', 'Impact (1-5)', 'Risk Score', 'Risk Level', 'Owner']
    st.dataframe(risk_table[display_cols], width='stretch', hide_index=True)

    st.markdown('---')

    st.subheader('Report Actions')
    if st.button('Generate PDF Report', type='primary'):
        pdf_data = {
            'generated_at': datetime.now().strftime('%B %d, %Y'),
            'generated_by': 'Streamlit GRC Dashboard',
            'nist_score': data['nist_score'],
            'iso_score': data['iso_score'],
            'top_gaps': data['top_gaps'],
            'risk_summary': data['risk_summary'],
            'recommendations': [
                'Resolve all HIGH-priority NIST gaps within the next 30 days.',
                'Prioritize the unimplemented ISO 27001 controls mapped to access control, vendor security, and incident handling.',
                'Implement remediation plans for all Critical and High risks.',
                'Review access administration and third-party assurance controls quarterly.'
            ],
        }
        output_path = OUTPUT_DIR / 'Streamlit-Compliance-Report.pdf'
        generate_pdf_report(pdf_data, output_path)
        st.success(f'PDF report generated: {output_path}')
        with open(output_path, 'rb') as pdf_file:
            st.download_button(
                label='Download PDF',
                data=pdf_file.read(),
                file_name='MediSync-Compliance-Report.pdf',
                mime='application/pdf',
            )


if __name__ == '__main__':
    main()
