# Enterprise GRC & IT Risk Workbench

A Python-based Governance, Risk and Compliance (GRC) portfolio project demonstrating enterprise risk assessment, security control mapping, IT audit testing, and audit finding remediation tracking.

> **Portfolio disclaimer:** This project uses fictional data for educational and demonstration purposes. It does not represent actual findings, systems, or projects from any employer or military organisation.

## Objectives

- Maintain a structured enterprise risk register.
- Calculate inherent risk scores using likelihood multiplied by impact.
- Classify risks using documented illustrative thresholds.
- Map security controls to identified risks.
- Record control tests, sample sizes, exceptions, and outcomes.
- Track audit findings, remediation owners, actions, target dates, and status.
- Present management-level summaries through a multi-page dashboard.

## Dashboard Preview

![Enterprise GRC Workbench - Executive Overview](screenshots/Screenshot%202026-10-22%20at%2015.25.08.png)


## Features

### Executive Overview
- Total risks, critical risks, and high risks.
- Security control inventory summary.
- Control testing outcome snapshot.

### Risk Register
- Risk scoring and severity classification.
- Filtering by risk level.
- CSV export.

### Security Control Library
- Control inventory and ownership.
- Control domains, frequency, and risk mappings.
- Filtering and CSV export.

### IT Control Testing
- Test results and sample sizes.
- Exception tracking and exception-rate calculations.
- Exceptions-by-control visualisation.
- CSV export.

### Audit Findings & Remediation
- Finding severity, root cause, and remediation action.
- Assigned remediation owners and target dates.
- Open, in-progress, closed, and overdue tracking.
- Filtering and CSV export.

## Technology Stack

- Python
- Streamlit
- Pandas
- Plotly

## Project Structure

```text
enterprise-grc-workbench/
├── app.py
├── app/
│   ├── dashboard.py
│   ├── risk_engine.py
│   ├── risk_report.py
│   ├── validate_controls.py
│   └── control_testing.py
├── data/
│   ├── risk_register.csv
│   ├── control_library.csv
│   ├── control_tests.csv
│   └── audit_findings.csv
├── pages/
│   ├── 1_Risk_Register.py
│   ├── 2_Control_Library.py
│   ├── 3_Control_Testing.py
│   └── 4_Audit_Findings.py
├── docs/
├── screenshots/
├── .gitignore
└── README.md
```

## Run Locally

### 1. Create and activate a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install streamlit pandas plotly
```

### 3. Launch the application

```bash
python -m streamlit run app.py
```

Streamlit will provide a local URL, typically http://localhost:8501.

## Risk Scoring Methodology

Risk score = Likelihood × Impact.

Both likelihood and impact use an illustrative scale from 1 to 5. The current demonstration classifies scores of 20 or above as Critical, 12–19 as High, 6–11 as Medium, and below 6 as Low.

These thresholds are project-specific examples, not a universal industry standard. In a production GRC implementation, scoring criteria and risk appetite should be approved and documented by the organisation.

## Audit Testing Notes

Control testing records are illustrative. Sample sizes and exceptions should be evaluated against the applicable control frequency, population, testing methodology, and audit requirements. A failed test does not automatically establish a final audit finding without further assessment.

## Future Enhancements

- Interactive risk and finding updates.
- Validation of control-to-risk mappings.
- Automated data-quality checks.
- Audit evidence register and finding lifecycle enhancements.
- Automated testing and deployment.
- Screenshots and a demonstration walkthrough.

## Disclaimer

This repository is an independent portfolio demonstration. It is not a production GRC platform and does not provide a substitute for approved organisational policies, professional audit judgement, or regulatory advice.
