# Signal Stack — Company Intelligence & Executive Briefing Engine

Signal Stack is a Python-based company intelligence application that collects information from permitted public sources, organizes business signals, and generates executive briefing reports for multiple companies.

## Project Overview

The application combines a Streamlit interface, SQLite database, and modular Python services to support company profiling, source management, signal collection, preliminary analysis, competitor intelligence, internal document uploads, and report generation.

## Technology Stack

- **Language:** Python
- **Frontend:** Streamlit
- **Database:** SQLite
- **Web extraction:** Requests, BeautifulSoup
- **RSS processing:** Feedparser
- **Data processing:** Pandas
- **Scheduling:** APScheduler
- **Document processing:** pypdf, openpyxl

## Implemented Features

- Multi-company profiles and business context.
- Ten-question company interview and saved answers.
- Source discovery, categorization, approval, and rejection workflow.
- Public webpage and RSS-based information collection.
- Signal storage and duplicate detection.
- Historical signal records.
- Preliminary signal analysis with relevance, urgency, business impact, and suggested actions.
- Competitor profile and comparison functionality.
- Internal document uploads and extraction.
- Executive briefing report generation.
- Streamlit dashboard for accessing the application.

## Sample Companies and Reports

The project database contains records for:

1. MeetUniversity — Education Technology.
2. Tata Motors — Automotive.
3. Infosys — Information Technology.

The `reports/` directory contains the latest exported reports for these three companies:

- `meetuniversity_report.md`
- `tata_motors_report.md`
- `infosys_report.md`

These reports are generated from the project's stored data. Their evidence coverage differs by company.

## Important Limitations

- The company interview currently uses a fixed set of ten questions; it is not yet an adaptive interview.
- Signal relevance, urgency, and opportunity identification use preliminary rule-based logic rather than a validated predictive AI model.
- Signal extraction depends on the content available from accessible public webpages and feeds. A webpage-level extraction should not be treated as a verified individual news event.
- Some company sources remain unapproved or inaccessible. Sources blocked by website access policies are not bypassed.
- Infosys currently has no collected signals because its tested source URLs were blocked by robots.txt.
- Tata Motors currently has limited collected source evidence.
- MeetUniversity has broader collected evidence, but its signals and generated opportunities still require human verification.
- Automated weekly scheduling has not been verified as operational. Manual report generation is available.
- Uploaded internal documents are treated as user-provided information and are not independently verified.

## Local Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd signal-stack
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

The application will display a local URL in the terminal. Open that URL in your browser.

## Project Structure

```text
signal-stack/
├── app.py
├── database.py
├── scheduler.py
├── requirements.txt
├── services/
├── tests/
├── data/
├── reports/
├── sample_internal_feedback.txt
├── README.md
└── .gitignore
```

The SQLite database is created locally and is not included in the Git repository.

## Responsible Data Collection

Signal Stack is designed to respect public website access restrictions. Sources blocked by robots.txt are not bypassed. Collected information and automated interpretations should be reviewed by a human before business decisions are made.

## Project Status

This is an assignment-stage implementation and prototype. The exported reports demonstrate the current reporting workflow; coverage, source reliability, analysis quality, and scheduling still require further validation.