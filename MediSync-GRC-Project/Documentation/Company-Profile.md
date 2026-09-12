# MEDISYNC SOLUTIONS
**Confidential** | Effective Date: July 2025 | Owner: CISO

---

## 1. COMPANY OVERVIEW

MediSync Solutions is a healthcare technology company founded in 2019 and headquartered in Cleveland, Ohio. The company develops and operates a cloud based platform that manages and organizes a patient’s treatment plan while facilitating communication between the patient, their family and the medical staff. This allows hospitals, clinics and independent physicians to share patient records securely. Additionally, care transitions and referrals can be managed in real time. 

**Mission:** To improve patient outcomes through secure, seamless healthcare data exchange.

- **Employee count:** 78 full-time employees
- **Annual revenue:** $11.8 million (FY 2024)
- **Primary office:** Cleveland, OH (headquarters)
- **Secondary offices:** Remote employees in 11 states
- **Founded:** 2019
- **Corporate structure:** Private, venture-backed (Series B)

---

## 2. PRODUCTS AND SERVICES

**Primary product:** MediSync Care Platform
- Web-based care coordination dashboard
- Mobile application (iOS and Android)
- HL7 FHIR-compliant API for EHR integration
- Secure messaging between care team members
- Patient referral management and tracking

Customer base:
- 47 hospital systems (primary customers)
- 312 independent physician practices
- 8 accountable care organizations (ACOs)
- Geographic coverage: primarily Midwest and Southeast US
  
---

## 3. DATA ENVIRONMENT

MediSync processes and stores the following data categories on behalf of its customers:

**Protected Health Information (PHI):**
- Patient demographics (name, DOB, address, contact)
- Diagnosis codes (ICD-10) and clinical notes
- Medication lists and prescription history
- Lab results and imaging reports
- Insurance and billing information

**Data volumes:**
- Approximately 2.3 million patient records
- 180,000 daily API transactions
- Average 4.2 TB of PHI stored in cloud environment

**Data classification levels:**
- Critical: PHI and authentication credentials
- Confidential: Business contracts, financial records
- Internal: Employee data, internal communications
- Public: Marketing materials, public API documentation
  
---

## 4. TECHNOLOGY INFRASTRUCTURE

**Cloud environment: Amazon Web Services (AWS)**
- Primary region: us-east-1 (N. Virginia)
- DR region: us-west-2 (Oregon)
- Services: EC2, RDS (PostgreSQL), S3, CloudTrail, WAF, KMS, VPC, Route 53

**On-premises:**
- Cleveland HQ: 2 physical servers (domain controller, backup), 45 workstations, Cisco network equipment
- All other employees: company-issued laptops, remote

**Key third-party systems:**
- Okta for identity and access management (IAM), SSO for all internal systems
- Salesforce (CRM — no PHI stored)
- Slack (internal communications — no PHI allowed)
- GitHub Enterprise (source code management)
- Qualys (vulnerability management)
- Splunk Cloud (SIEM and log management)

---

## 5. REGULATORY ENVIRONMENT

MediSync operates as a HIPAA Business Associate for all hospital and physician customers. Applicable regulations:
- HIPAA Privacy Rule (45 CFR Part 164 Subpart E)
- HIPAA Security Rule (45 CFR Part 164 Subpart C)
- HITECH Act amendments to HIPAA
- State privacy laws: Ohio, Florida, Texas, California
- SOC 2 Type II (annual audit — in preparation)
- ISO 27001:2022 (certification in progress)
- GLBA — not applicable (no financial institution activities)

---

## 6. ORGANIZATIONAL STRUCTURE (SECURITY-RELEVANT)

- Chief Executive Officer: Marcus Chen
- Chief Technology Officer: Priya Nair
- Chief Information Security Officer: Isha Gupta
- VP of Engineering: David Kowalski
- Head of Compliance: Sandra Rivera
- IT Manager: James Okonkwo

**Security team structure:**
- CISO (1) — overall security program ownership
- GRC Analyst (1) — compliance, risk, policy
- Security Engineer (2) — technical controls
- IT Support (3) — endpoint and helpdesk

---

## 7. KEY BUSINESS RISKS

- PHI data breach: regulatory fines up to $1.9M/year per HIPAA violation category + reputational damage
- Ransomware: potential platform outage affecting patient care continuity at 47 hospital customers
- Third-party compromise: 12 integrated EHR vendors represent significant supply chain risk
- Insider threat: 78 employees with varying PHI access
- Regulatory non-compliance: loss of HIPAA BAA eligibility would end all customer contracts
- AI/ML model risk: increasing use of AI-assisted clinical decision tools introduces model bias and explainability concerns that may conflict with HIPAA minimum necessary standards
