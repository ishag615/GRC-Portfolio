# MediSync Solutions — GRC Portfolio Project

## Overview

This repository contains a comprehensive Governance, Risk, and Compliance (GRC) portfolio project built around **MediSync Solutions** — a fictional 78-person healthcare SaaS company processing Protected Health Information (PHI) for 47 hospital systems, 312 physician practices, and 8 accountable care organizations.

The project simulates the real-world work of a GRC Analyst preparing an organization for **ISO 27001:2022 certification**, **SOC 2 Type II audit readiness**, and **HIPAA compliance** — producing the documentation, risk assessments, automation scripts, and a Streamlit web dashboard that a GRC professional would deliver on the job.

> **Why this scenario?** Healthcare is one of the most heavily regulated and breach-prone industries, making it the richest environment for demonstrating GRC fundamentals. MediSync's obligation to protect 2.3 million patient records under HIPAA, ISO 27001, and SOC 2 simultaneously reflects the multi-framework reality most GRC analysts face.

---

## What This Project Demonstrates

| Skill Area | Evidence |
|---|---|
| **NIST CSF 2.0** | Full gap assessment — all 106 subcategories rated, top gaps identified, remediation roadmap produced |
| **ISO 27001:2022** | All 93 Annex A controls assessed with applicability, implementation status, and HIPAA/NIST cross-mapping |
| **HIPAA Security Rule** | Embedded throughout all policies and risk assessments; breach notification requirements in IR Policy |
| **SOC 2** | Trust Service Criteria referenced in control assessments and risk register |
| **Risk Assessment** | 20-risk register with likelihood × impact scoring, risk appetite threshold, treatment plans, residual risk |
| **Policy Writing** | 3 professional security policies — Information Security, Access Control, Incident Response |
| **Python Automation** | Compliance checker, risk analyzer, heatmap generator, PDF report generator |
| **Web Dashboard** | Streamlit dashboard with KPI cards, compliance progress indicators, and risk filtering |
| **GRC Platform Awareness** | Automation replicates core Drata/Vanta compliance monitoring workflow |
| **Technical Writing** | All documents written at professional GRC analyst standard |

---

## Repository Structure

```
GRC-Portfolio/
├── README.md
└── MediSync-GRC-Project/
    ├── dashboard_app.py                         ← Streamlit web dashboard
    ├── Automation/
    │   ├── compliance_checker.py                ← NIST CSF + ISO 27001 scoring
    │   ├── risk_analyzer.py                     ← Risk register analysis
    │   ├── risk_heatmap.py                      ← Risk heat map generator
    │   ├── report_generator.py                  ← PDF compliance report generator
    │   └── requirements.txt                     ← Python dependencies
    ├── Assessments/
    │   ├── Risk-Register.xlsx                   ← 20-risk register with scoring
    │   ├── NIST-CSF-Gap-Assessment.xlsx         ← All 106 subcategories assessed
    │   └── ISO27001-Controls.xlsx               ← All 93 Annex A controls assessed
    ├── Documentation/
    │   ├── Company-Profile.md                   ← MediSync organization overview
    │   └── Policies/
    │       ├── POL001_InfoSec_Policy.pdf        ← Information Security Policy
    │       ├── POL003_Access_Control_Policy.pdf ← Access Control Policy
    │       └── POL004_Incident_Response_Policy.pdf ← Incident Response Policy
    └── Output/
        ├── Risk-Heatmap.png                     ← Generated risk heat map
        ├── Compliance-Report.pdf                ← Generated compliance report
        └── screenshots/                         ← Terminal and dashboard screenshots
```

---

## How to Run

### 1. Prerequisites

From the project root, create and activate a Python virtual environment, then install dependencies:

```bash
cd "GRC-Portfolio/MediSync-GRC-Project"
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r Automation/requirements.txt
```

Dependencies: `pandas`, `openpyxl`, `matplotlib`, `reportlab`, `streamlit`, `plotly`

---

### 2. Terminal Version

Run individual scripts from the `MediSync-GRC-Project` directory with the virtual environment active.

**NIST CSF + ISO 27001 compliance checker**
```bash
python3 Automation/compliance_checker.py
```
Output: overall NIST CSF score, overall ISO 27001 score, total gaps, high-priority gaps, top 5 control gaps, risk summary by severity, risks above appetite threshold.

**Risk register analyzer**
```bash
python3 Automation/risk_analyzer.py
```
Output: risk count by severity (Critical / High / Medium / Low), risks above the appetite threshold of 9.

**Risk heat map generator**
```bash
python3 Automation/risk_heatmap.py
```
Output: `Output/Risk-Heatmap.png` — a color-coded 5×5 likelihood × impact matrix with each risk plotted by ID.

**PDF compliance report generator**
```bash
python3 Automation/report_generator.py
```
Output: `Output/Compliance-Report.pdf` — a formatted compliance report suitable for executive review or audit support.

---

### 3. Web Dashboard

```bash
python3 -m streamlit run dashboard_app.py --server.headless true --server.port 8501
```

Then open **http://localhost:8501** in your browser.

If port 8501 is already in use:
```bash
lsof -nP -iTCP:8501 -sTCP:LISTEN
kill <PID>
```

---

## Functionalities Supported

The project supports the following GRC and reporting workflows:

- **NIST CSF 2.0** gap assessment and scoring from the Excel workbook
- **ISO 27001:2022** control assessment and gap count analysis
- Risk register scoring using **likelihood × impact**
- Risk categorization into Critical, High, Medium, and Low
- Identification of risks above the defined **appetite threshold**
- Top gap prioritization by severity and current maturity
- Matrix-style **risk heat map** generation for executive review
- Terminal console reporting for compliance snapshots
- **Streamlit dashboard** with KPI cards and progress indicators
- Risk table filtering by severity
- **PDF report generation** from the dashboard or report script
- Downloadable compliance report output for presentation or audit support

---

## Project Artifacts

### 1. Company Profile
Defines the MediSync organization — tech stack, data environment, regulatory obligations, org structure, and key business risks. Establishes the context that every other artifact references.

**Key details:** AWS-hosted (us-east-1 primary, us-west-2 DR), Okta for IAM, Splunk Cloud for SIEM, 2.3M patient records, HIPAA Business Associate for all customers.

---

### 2. Risk Register
A 20-item risk register built using a documented likelihood × impact methodology with a defined risk appetite threshold of 9. Each risk includes the asset affected, threat source, vulnerability, current controls, treatment action, residual risk score, ISO 27001 control references, and named owner.

**Risk distribution:** 2 Critical | 6 High | 10 Medium | 2 Low
**Highest risks:** R-005 Phishing attack (score: 16, Critical) | R-001 Ransomware on production database (score: 15, Critical)

---

### 3. NIST CSF 2.0 Gap Assessment
Full assessment of MediSync against all 106 NIST CSF 2.0 subcategories across all six functions — Govern, Identify, Protect, Detect, Respond, and Recover. Each subcategory includes a current maturity rating (1–4), target maturity, gap identification, MediSync-specific justification, priority level, and remediation action.

**Overall maturity:** 2.3 / 4.0 | **Target:** 3.0 / 4.0 | **Total gaps:** 78 of 106 subcategories
**Top gap:** No privileged access management (PAM) — PR.AA-01 (current: 2, target: 4)

---

### 4. ISO 27001:2022 Controls Assessment
Assessment of all 93 Annex A controls across four themes — Organizational (A.5), People (A.6), Physical (A.7), and Technological (A.8). Each control includes applicability decision with justification, implementation status, MediSync-specific notes, and cross-mapping to NIST CSF and HIPAA Security Rule.

**Applicable:** 92 of 93 (A.8.30 excluded — no outsourced development)
**Implemented:** 12 | **Partial:** 68 | **Not implemented:** 12
**Top gaps:** A.8.11 (data masking), A.8.12 (DLP), A.5.35 (independent review)

---

### 5. Security Policies

| Policy | ID | Pages | Key Coverage |
|---|---|---|---|
| Information Security Policy | POL-001 | 2 | ISMS scope, CIA triad, roles, 10 policy statements, enforcement |
| Access Control Policy | POL-003 | 2 | Provisioning, least privilege, MFA (FIDO2/Okta), NIST 800-63B passwords, quarterly reviews, same-day termination |
| Incident Response Policy | POL-004 | 2 | P1–P4 classification, 5 IR phases, HIPAA breach notification (60-day HHS), communication chain, lessons learned |

---

### 6. Python Automation & Dashboard

Four scripts plus a Streamlit dashboard that together simulate the automated compliance monitoring workflow performed by enterprise GRC platforms like **Drata** and **Vanta**.

> Enterprise platforms like Drata and Vanta automate evidence collection and continuous control monitoring at scale — connecting to cloud environments via API and generating audit-ready reports on demand. This project replicates that core workflow in Python, demonstrating understanding of the underlying compliance process these tools automate.

---

## Frameworks & Standards Applied

| Framework | Application |
|---|---|
| NIST CSF 2.0 | Full gap assessment across all 6 functions and 106 subcategories |
| ISO 27001:2022 | All 93 Annex A controls assessed; ISMS documentation built to support certification |
| HIPAA Security Rule | Embedded in all policies; breach notification requirements in IR Policy |
| NIST SP 800-63B | Password policy in Access Control Policy aligned to digital identity guidelines |
| NIST SP 800-53 | Referenced in risk register control cross-mapping |
| SOC 2 TSC | Referenced in control assessments for audit readiness context |

---

## Tools & Technologies

**Frameworks:** ISO 27001, NIST CSF 2.0, HIPAA, SOC 2, NIST SP 800-63B, NIST SP 800-53
**Automation:** Python, pandas, openpyxl, matplotlib, plotly, reportlab, streamlit
**GRC Platforms (conceptual):** Drata, Vanta, ServiceNow GRC
**Documentation:** Markdown, Microsoft Word, PDF
**Version Control:** Git / GitHub

---

*MediSync Solutions is a fictional organization created for portfolio purposes. All data, names, and scenarios are simulated.*
