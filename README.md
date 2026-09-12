# MediSync Solutions — GRC Portfolio Project

## Overview

This repository contains a comprehensive Governance, Risk, and Compliance (GRC) portfolio project built around **MediSync Solutions** — a fictional 78-person healthcare SaaS company processing Protected Health Information (PHI) for 47 hospital systems, 312 physician practices, and 8 accountable care organizations.

The project simulates the real-world work of a GRC Analyst preparing an organization for **ISO 27001:2022 certification**, **SOC 2 Type II audit readiness**, and **HIPAA compliance** — producing the documentation, risk assessments, and automation artifacts a GRC professional would deliver on the job.

> **Why this scenario?** Healthcare is one of the most heavily regulated and breach-prone industries, making it the richest environment for demonstrating GRC fundamentals. MediSync's obligation to protect 2.3 million patient records under HIPAA, ISO 27001, and SOC 2 simultaneously reflects the multi-framework reality most GRC analysts face.

---

## What This Project Demonstrates

| Skill Area | Evidence |
|---|---|
| **NIST CSF 2.0** | Full gap assessment — all 106 subcategories rated, top gaps identified, remediation roadmap produced |
| **ISO 27001:2022** | All 93 Annex A controls assessed with applicability, implementation status, and HIPAA/NIST cross-mapping |
| **HIPAA Security Rule** | Embedded throughout all policies and risk assessments; breach notification requirements in IR Policy |
| **SOC 2** | Trust Service Criteria referenced in control assessments and risk register |
| **Risk Assessment** | 20-risk register with likelihood × impact scoring, risk appetite threshold, treatment plans, and residual risk |
| **Policy Writing** | 3 professional security policies — Information Security, Access Control, Incident Response |
| **Python Automation** | Risk register analyzer that calculates scores, identifies critical risks, and generates summary output |
| **GRC Platform Awareness** | Automation replicates core Drata/Vanta compliance monitoring workflow; ServiceNow GRC fundamentals completed |
| **Technical Writing** | All documents written at professional GRC analyst standard |

---

## Repository Structure

```
GRC-Portfolio/
├── README.md
├── Documentation/
│   ├── Company-Profile.md                    ← MediSync organization overview
│   └── Policies/
│       ├── POL001_InfoSec_Policy.pdf         ← Information Security Policy
│       ├── POL003_Access_Control_Policy.pdf  ← Access Control Policy
│       └── POL004_Incident_Response_Policy.pdf ← Incident Response Policy
├── Assessments/
│   ├── Risk-Register.xlsx                    ← 20-risk register with scoring
│   ├── NIST-CSF-Gap-Assessment.xlsx          ← All 106 subcategories assessed
│   └── ISO27001-Controls.xlsx                ← All 93 Annex A controls assessed
├── Automation/
│   ├── risk_analyzer.py                      ← Risk register analyzer script
│   ├── requirements.txt                      ← Python dependencies
│   └── README.md                             ← How to run the scripts
└── Output/
    ├── Risk-Heatmap.png                      ← Generated risk heat map
    └── screenshots/                          ← Script output screenshots
```

---

## Project Artifacts

### 1. Company Profile
Defines the MediSync organization — tech stack, data environment, regulatory obligations, org structure, and key business risks. Establishes the context that every other artifact references.

**Key details:** AWS-hosted (us-east-1 primary, us-west-2 DR), Okta for IAM, Splunk Cloud for SIEM, 2.3M patient records, HIPAA Business Associate for all customers.

---

### 2. Risk Register
A 20-item risk register built using a documented likelihood × impact methodology with a defined risk appetite threshold of 9. Each risk includes the asset affected, threat source, vulnerability, current controls, treatment action, residual risk score, ISO 27001 control references, and named owner.

**Risk distribution:** 2 Critical | 6 High | 10 Medium | 2 Low  
**Highest risk:** R-001 Ransomware on production database (score: 15) and R-005 Phishing attack (score: 16)

---

### 3. NIST CSF 2.0 Gap Assessment
Full assessment of MediSync against all 106 NIST CSF 2.0 subcategories across all six functions — Govern, Identify, Protect, Detect, Respond, and Recover. Each subcategory includes a current maturity rating (1–4), target maturity, gap identification, MediSync-specific justification, priority level, and remediation action.

**Overall maturity:** 2.3 / 4.0  
**Target maturity:** 3.0 / 4.0  
**Total gaps identified:** 78 across 106 subcategories  
**Top gap:** No privileged access management (PAM) solution — PR.AA-01 (current: 2, target: 4)

---

### 4. ISO 27001:2022 Controls Assessment
Assessment of all 93 Annex A controls across four themes — Organizational (A.5), People (A.6), Physical (A.7), and Technological (A.8). Each control includes applicability decision with justification, implementation status (Implemented / Partial / Not Implemented), MediSync-specific implementation notes, and cross-mapping to NIST CSF and HIPAA Security Rule.

**Applicable controls:** 92 of 93 (A.8.30 excluded — no outsourced development)  
**Fully implemented:** 12 | **Partial:** 68 | **Not implemented:** 12  
**Top priority gaps:** A.8.11 (data masking), A.8.12 (DLP), A.5.35 (independent review)

---

### 5. Security Policies

Three professional security policies written specifically for MediSync, each referencing named systems, roles, and regulatory obligations:

| Policy | ID | Pages | Key Coverage |
|---|---|---|---|
| Information Security Policy | POL-001 | 2 | ISMS scope, CIA triad, roles, 10 policy statements, enforcement |
| Access Control Policy | POL-003 | 2 | Provisioning, least privilege, MFA (FIDO2/Okta), NIST 800-63B passwords, quarterly reviews, same-day termination |
| Incident Response Policy | POL-004 | 2 | P1–P4 classification, 5 IR phases, HIPAA breach notification (60-day HHS), communication chain, lessons learned |

---

### 6. Python Automation

A risk register analyzer that simulates the automated compliance monitoring workflow performed by enterprise GRC platforms like **Drata** and **Vanta**.

**What it does:**
- Reads the MediSync Risk Register from Excel using pandas
- Calculates risk scores (likelihood × impact) and assigns risk levels
- Identifies risks above the defined risk appetite threshold
- Prints a structured compliance summary report to terminal
- Generates a color-coded risk heat map (matplotlib)

**How to run:**
```bash
pip install pandas openpyxl matplotlib
python risk_analyzer.py
```

> **GRC automation context:** Enterprise platforms like Drata and Vanta automate evidence collection and continuous control monitoring at scale — connecting to cloud environments via API and generating audit-ready reports on demand. This project replicates that core workflow in Python, demonstrating understanding of the underlying compliance process these tools automate.

---

## Frameworks & Standards Applied

| Framework | Application in this project |
|---|---|
| NIST CSF 2.0 | Full gap assessment — primary framework for risk-based control evaluation |
| ISO 27001:2022 | All 93 Annex A controls assessed; ISMS documentation built to support certification |
| HIPAA Security Rule | Embedded in all policies; breach notification requirements in IR Policy |
| NIST SP 800-63B | Password policy in Access Control Policy aligned to current digital identity guidelines |
| NIST SP 800-53 | Referenced in risk register ISO control cross-mapping |
| SOC 2 TSC | Referenced in control assessments for audit readiness context |

---

## Tools & Technologies

**GRC & Compliance:** ISO 27001, NIST CSF 2.0, HIPAA, SOC 2, NIST SP 800-63B  
**Automation:** Python, pandas, openpyxl, matplotlib  
**GRC Platforms (conceptual):** Drata, Vanta, ServiceNow GRC (NowLearning certification completed)  
**Security Tools:** Wireshark, NRF Sniffer (used in faculty-mentored research), Splunk (conceptual), Qualys (conceptual)  
**Documentation:** Markdown, Microsoft Word, PDF  
**Version Control:** Git / GitHub  

---


## About This Project

This portfolio was built over the summer of 2026 as part of my preparation for entry-level GRC Analyst and Information Security Analyst roles. Every artifact is written for a specific fictional scenario — not assembled from generic templates — to demonstrate the ability to apply frameworks to a real organizational context and produce work product that a GRC professional would actually use.

---

*MediSync Solutions is a fictional organization created for portfolio purposes. All data, names, and scenarios are simulated.*
