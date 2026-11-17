# Signal Stack — Company Intelligence & Executive Briefing Engine

Signal Stack is a Python and Streamlit application that collects information from permitted public sources, organizes business signals, and generates executive briefing reports for multiple companies.

## Technology
- Python
- Streamlit
- SQLite
- Requests and BeautifulSoup
- Feedparser
- Pandas
- APScheduler
- pypdf and openpyxl

## Features
- Multi-company profiles and company interviews
- Source discovery, categorization, approval, and rejection
- Public webpage and RSS information collection
- Signal storage and duplicate detection
- Preliminary rule-based signal analysis
- Competitor research and comparison
- Internal document uploads
- Executive briefing report generation

## Sample Companies
- MeetUniversity — Education Technology
- Tata Motors — Automotive
- Infosys — Information Technology

## Generated Reports
The reports directory contains exported reports generated from the local database:
- meetuniversity_report.md
- tata_motors_report.md
- infosys_report.md

Evidence coverage differs between companies. Infosys currently has no collected signals because its tested source URLs were blocked by robots.txt. Tata Motors has limited collected evidence.

## Limitations
- The company interview uses a fixed set of ten questions, not an adaptive interview.
- Signal analysis and opportunity identification use preliminary rule-based logic, not a validated predictive AI model.
- Extracted webpage content may represent general page information rather than a distinct news event.
- Sources and generated interpretations require human verification.
- Automated weekly scheduling has not been verified as operational.
- Internal uploaded documents are user-provided and are not independently verified.

## Local Setup

Create and activate a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

Run the application:

    streamlit run app.py

## Responsible Data Collection
The application does not bypass robots.txt restrictions. Inaccessible sources remain unapproved rather than being accessed through workarounds.

## Project Status
This is an assignment-stage prototype. Source coverage, analysis quality, and automated scheduling require further validation.
