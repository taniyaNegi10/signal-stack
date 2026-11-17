# SIGNAL STACK
## Technical Documentation
**Project:** Company Intelligence & Executive Briefing Engine  
**Technology:** Python, Streamlit, SQLite  
**Repository:** https://github.com/taniyaNegi10/signal-stack

---

## 1. Introduction

Signal Stack is a company intelligence and executive briefing application designed to collect, organize, analyse, and summarize business information from public sources and user-provided internal documents.

The system supports multiple company profiles and organizes collected information into business intelligence signals. It provides source management, competitor research, preliminary signal analysis, and executive briefing generation through a Streamlit dashboard.

The application was developed using a modular Python architecture with SQLite for local data storage.

### Objectives

- Understand and store company business context.
- Discover and manage relevant information sources.
- Collect information from permitted public webpages and RSS feeds.
- Organize information into structured business signals.
- Identify potential opportunities and business implications.
- Generate executive briefing reports.
- Incorporate user-provided internal documents into the intelligence workflow.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and backend services |
| Streamlit | Interactive dashboard and user interface |
| SQLite | Local relational database |
| Requests | HTTP requests to public webpages |
| BeautifulSoup | HTML content extraction |
| Feedparser | RSS feed processing |
| Pandas | Data processing |
| APScheduler | Scheduling implementation |
| pypdf | PDF text extraction |
| openpyxl | Excel file processing |

The project uses Python service modules to separate application responsibilities and make the code easier to maintain.

## 3. System Architecture

The application follows a modular, service-oriented structure.

**Architecture flow:**

1. User interacts with the Streamlit dashboard.
2. The application calls the relevant Python service.
3. Services perform source discovery, collection, analysis, or report generation.
4. Structured records are stored and retrieved using SQLite.
5. Results are displayed in the dashboard or included in generated reports.

### Main Components

| Component | Responsibility |
|---|---|
| `app.py` | Streamlit application and dashboard |
| `database.py` | Database connection and database initialization |
| `scheduler.py` | Scheduling-related implementation |
| `services/` | Business logic divided into individual services |
| `data/` | Local SQLite database storage |
| `reports/` | Exported executive briefing reports |
| `tests/` and `test_*.py` | Individual service and workflow test scripts |

### Important Services

- `company_service.py` — company profile management.
- `company_interview_service.py` — company interview questions and saved answers.
- `source_discovery_service.py` — discovery of potential information sources.
- `source_classification_service.py` — source categorization.
- `source_approval_workflow_service.py` — source approval workflow.
- `source_service.py` — source management.
- `signal_collection_service.py` — information collection and signal storage.
- `signal_analysis_service.py` — preliminary signal analysis.
- `competitor_analysis_service.py` — competitor intelligence analysis.
- `competitor_comparison_service.py` — competitor comparison.
- `competitor_gap_analysis_service.py` — preliminary gap analysis.
- `internal_upload_service.py` — internal document processing.
- `report_generation_service.py` — executive report generation.

## 4. Core Workflows

### 4.1 Company Understanding

Users can create and manage company profiles.

The current interview workflow contains ten fixed questions covering:

- Company activities and products.
- Target customers and markets.
- Competitive differentiation.
- Main competitors.
- Business goals and challenges.
- Relevant market trends.
- Developments to monitor.

Interview answers are saved and associated with the company profile.

**Current limitation:** The interview currently uses a fixed question set. Adaptive follow-up questioning is not yet implemented.

### 4.2 Source Discovery and Approval

The application discovers potential public information sources and organizes them for review.

The source workflow includes:

1. Discover potential sources.
2. Classify sources into relevant categories.
3. Evaluate source accessibility and available information.
4. Review recommendations.
5. Approve or reject sources.
6. Collect information from approved and accessible sources.

The source workflow includes human review rather than automatically treating every discovered source as trustworthy.

### 4.3 Signal Collection and Storage

The signal collection service retrieves information from permitted public webpages and RSS feeds.

Collected information is stored in SQLite with its associated source information. Duplicate detection helps prevent repeated records from being unnecessarily stored.

Historical records are retained in the local database.

### 4.4 Signal Analysis

The signal analysis service provides preliminary analysis of collected information.

It evaluates signals using rule-based indicators and produces:

- Relevance scoring.
- Urgency classification.
- Explanation of why the signal matters.
- Potential business impact.
- Recommended action.
- Human-review requirement.

The analysis is heuristic and should be treated as decision-support information, not as verified business intelligence.

### 4.5 Competitor Intelligence

The competitor-related services support competitor research, comparison, and preliminary gap analysis.

The application can organize competitor information and identify potential areas for further investigation.

Potential gaps and opportunities require human verification before being treated as confirmed competitive advantages or disadvantages.

### 4.6 Internal Document Processing

The internal upload service supports user-provided documents, including supported PDF, TXT, CSV, and Excel files.

Extracted information can be incorporated into the company's intelligence workflow and generated briefing reports.

Internal documents are treated as user-provided evidence and are not independently verified.

### 4.7 Executive Briefing Generation

The report generation service combines available company context, collected signals, competitor information, opportunities, and internal intelligence.

The generated report includes sections covering:

1. Company Profile and Business Context
2. Executive Summary
3. Customer Signals
4. Competitor Intelligence
5. Market Intelligence
6. Internal Business Intelligence
7. Opportunities Identified
8. Risks and Threats
9. Recommended Actions for This Week
10. What We Should Watch
11. Source Appendix

The available content in each section depends on the evidence stored for that company.

## 5. Database and Data Management

SQLite is used as the local relational database.

The application stores company information, source records, collected intelligence, and generated reports.

The report records include:

- Report ID
- Company ID
- Report title
- Report content
- Creation timestamp

Generated reports are exported as Markdown files in the `reports/` directory.

The local database is excluded from Git using `.gitignore`. It is created and maintained locally when the application is initialized.

## 6. Testing and Validation

Individual Python test scripts were created for the major application services and workflows.

Observed validation results include:

- MeetUniversity: 20 approved sources.
- MeetUniversity collection run: 20 sources checked, 13 signals saved, 7 duplicates skipped, and 0 failures.
- MeetUniversity competitor research: 6 competitor profiles used in a generated report.
- Tata Motors: one approved source and one collected signal.
- Infosys: tested source URLs were blocked by robots.txt and remained unapproved.
- Company interviews: Tata Motors and Infosys each had 10 saved answers.
- Internal feedback document: uploaded and included in the MeetUniversity reporting workflow.
- Reports: generated and exported for MeetUniversity, Tata Motors, and Infosys.

These are observed project results, not a claim that every test script passes or that all collected information is independently verified.

## 7. Setup and Execution

### Requirements

- Python installed.
- pip package manager.
- Internet connection for public source collection.
- Git for repository setup.

### Installation

Clone the repository:

```bash
git clone https://github.com/taniyaNegi10/signal-stack.git
cd signal-stack
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal.

## 8. Limitations and Future Improvements

Current implementation limitations:

- The company interview is fixed rather than adaptive.
- Signal analysis and opportunity identification are rule-based and require further validation.
- Webpage extraction may capture general landing-page information rather than individual news events.
- Source accessibility does not establish source credibility.
- Evidence coverage varies between companies.
- Infosys currently has no collected signals because its tested source URLs were blocked by robots.txt.
- Automated weekly scheduling has not been verified as operational.
- Generated insights require human review.

Potential future improvements:

- Implement adaptive company interviews.
- Improve event-level extraction and evidence traceability.
- Introduce stronger source credibility evaluation.
- Improve semantic signal analysis and opportunity validation.
- Add automated tests and broader test coverage.
- Verify and operationalize scheduled report generation.
- Improve deployment and monitoring.

## 9. Conclusion

Signal Stack demonstrates a modular approach to company intelligence collection and executive briefing generation using Python, Streamlit, and SQLite.

The implementation brings together company profiling, source management, information collection, preliminary analysis, competitor research, internal document processing, and report generation.

The current system is an assignment-stage prototype. Its generated reports demonstrate the implemented workflow, while source coverage, analytical accuracy, and scheduling require further validation.

**GitHub Repository:**  
https://github.com/taniyaNegi10/signal-stack