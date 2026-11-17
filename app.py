
import streamlit as st

from database import initialize_database, get_connection

from services.company_service import CompanyService

from services.source_approval_dashboard_service import (
    SourceApprovalDashboardService
)

from services.source_approval_workflow_service import (
    SourceApprovalWorkflowService
)

from services.company_interview_service import (
    CompanyInterviewService
)

from services.internal_upload_service import (
    InternalUploadService
)


# ==================================================
# 1. CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Signal Stack | Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

initialize_database()

company_service = CompanyService()
dashboard_service = SourceApprovalDashboardService()
workflow_service = SourceApprovalWorkflowService()
interview_service = CompanyInterviewService()
upload_service = InternalUploadService()


# ==================================================
# 2. DESIGN SYSTEM
# ==================================================

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at 80% 0%,
        rgba(0, 110, 65, 0.15), transparent 40%),
        #050907;
    color: #edf5ef;
}

.block-container {
    max-width: 1450px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #09140f, #050a07);
    border-right: 1px solid rgba(65, 190, 125, 0.15);
}

[data-testid="stSidebar"] hr {
    border-color: rgba(65, 190, 125, 0.18);
}

h1, h2, h3 {
    color: #f0f8f2 !important;
    letter-spacing: -0.6px;
}

p, label, span {
    color: #c0cec4;
}

.eyebrow {
    color: #43d991;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #102d1f, #08160f);
    border: 1px solid rgba(65, 190, 125, 0.2);
    border-radius: 14px;
    padding: 20px;
}

[data-testid="stMetricLabel"] {
    color: #9aafa0 !important;
}

[data-testid="stMetricValue"] {
    color: #47df96 !important;
    font-weight: 700;
}

[data-testid="stExpander"] {
    background: rgba(10, 28, 19, 0.8);
    border: 1px solid rgba(65, 190, 125, 0.2);
    border-radius: 12px;
    margin-bottom: 12px;
}

[data-testid="stExpander"] summary {
    color: #e8f5eb;
    font-weight: 600;
}

.stButton > button {
    background: linear-gradient(135deg, #19a96b, #087b4b);
    color: white;
    border: 1px solid rgba(90, 255, 170, 0.25);
    border-radius: 9px;
    font-weight: 600;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #27c982, #11945d);
    border-color: #43e99b;
    color: white;
}

[data-baseweb="select"] > div,
[data-baseweb="input"] > div {
    background-color: #102019;
    border-color: rgba(65, 190, 125, 0.3);
    border-radius: 9px;
}

hr {
    border-color: rgba(65, 190, 125, 0.15);
}

.status-panel {
    background: linear-gradient(120deg, #0d3522, #081810);
    border: 1px solid rgba(60, 210, 130, 0.2);
    border-radius: 14px;
    padding: 18px 20px;
    margin: 15px 0 22px 0;
}

.score-card {
    background: linear-gradient(145deg, #102d1f, #081810);
    border: 1px solid rgba(65, 190, 125, 0.2);
    border-radius: 12px;
    padding: 16px;
    margin: 12px 0;
}

.score-number {
    color: #47df96;
    font-size: 28px;
    font-weight: 800;
}

.muted {
    color: #8fa397;
    font-size: 12px;
}

#MainMenu, footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# 3. HELPER FUNCTIONS
# ==================================================

def matches_filters(source, search_text, selected_category):

    name = source.get("name", "").lower()
    url = source.get("url", "").lower()
    category = source.get("category", "")

    search_match = (
        not search_text
        or search_text.lower() in name
        or search_text.lower() in url
    )

    category_match = (
        selected_category == "All Categories"
        or category == selected_category
    )

    return search_match and category_match


def display_quality_evaluation(evaluation):

    if not evaluation:
        st.warning("No saved quality evaluation is available.")
        return

    score = evaluation.get("score", 0) or 0

    st.markdown("#### Source Quality")

    st.markdown(
        f"""
        <div class="score-card">
            <div class="muted">OVERALL QUALITY SCORE</div>
            <div class="score-number">{score}/100</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(max(0.0, min(float(score), 100.0)) / 100)

    st.caption(
        f"Quality: {evaluation.get('quality', 'Not available')}"
    )

    st.caption(
        f"Recommendation: "
        f"{evaluation.get('recommendation', 'Not available')}"
    )

    st.divider()

    st.markdown("#### Score Breakdown")

    components = [
        ("Accessibility", "accessibility_score"),
        ("Relevance", "relevance_score"),
        ("Credibility", "credibility_score"),
        ("Category Fit", "category_fit_score")
    ]

    columns = st.columns(4)

    for column, (label, key) in zip(columns, components):

        value = evaluation.get(key, 0) or 0

        with column:

            maximum = (
                25 if key in [
                    "accessibility_score",
                    "credibility_score"
                ]
                else 35 if key == "relevance_score"
                else 15
            )

            st.metric(label, f"{value}/{maximum}")

    reasons = evaluation.get("reasons", [])

    if reasons:

        st.markdown("#### Evaluation Notes")

        if isinstance(reasons, str):
            st.write(reasons)
        else:
            for reason in reasons:
                st.write(f"• {reason}")

    st.caption(
        "Scores are rule-based indicators, not independent proof "
        "of source credibility. Human review is required."
    )


def get_company_reports(company_id):

    connection = get_connection()

    try:
        reports = connection.execute(
            """
            SELECT id, company_id, title, content, created_at
            FROM reports
            WHERE company_id = ?
            ORDER BY created_at DESC, id DESC
            """,
            (company_id,)
        ).fetchall()

        return reports

    finally:
        connection.close()


# ==================================================
# 4. LOAD COMPANIES
# ==================================================

companies = company_service.get_all_companies()

if not companies:
    st.warning("No companies found. Please add a company first.")
    st.stop()

company_options = {
    f"{company['name']} (ID: {company['id']})": company["id"]
    for company in companies
}


# ==================================================
# 5. SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown(
        """
        <div style="padding:12px 0 22px 0;">
            <div style="font-size:27px;font-weight:800;color:#f0fff5;">
                <span style="color:#35d98b;">▥</span> SIGNAL STACK
            </div>
            <div style="color:#82998a;font-size:11px;
                        letter-spacing:2px;margin-top:5px;">
                COMPANY INTELLIGENCE
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        '<div class="eyebrow">WORKSPACE</div>',
        unsafe_allow_html=True
    )

    selected_company = st.selectbox(
        "Active Company",
        options=list(company_options.keys())
    )

    company_id = company_options[selected_company]

    st.divider()

    st.markdown(
        '<div class="eyebrow">NAVIGATION</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigate",
        [
            "Overview",
            "Company Interview",
            "Source Manager",
            "Internal Documents",
            "Reports"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown(
        """
        <div class="eyebrow">SYSTEM STATUS</div>
        <p style="font-size:12px;">● Application running</p>
        <p style="color:#718579;font-size:11px;">Signal Stack v1.0</p>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# 6. DASHBOARD DATA
# ==================================================

dashboard = dashboard_service.get_dashboard_data(company_id)

total_sources = dashboard["total_sources"]
approved_count = dashboard["approved_count"]
pending_count = dashboard["pending_count"]

approved_sources = dashboard["approved_sources"]
pending_sources = dashboard["pending_sources"]


# ==================================================
# 7. OVERVIEW PAGE
# ==================================================

if page == "Overview":

    st.markdown(
        '<div class="eyebrow">INTELLIGENCE WORKSPACE</div>',
        unsafe_allow_html=True
    )

    st.title("Company Overview")

    st.write(f"Currently viewing: **{selected_company}**")

    st.divider()

    st.subheader("Source Intelligence")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Sources", total_sources)
    col2.metric("Approved Sources", approved_count)
    col3.metric("Pending Review", pending_count)

    st.markdown(
        """
        <div class="status-panel">
            <div style="color:#45dc96;font-weight:700;">
                SOURCE MANAGEMENT STATUS
            </div>
            <p>
                Your source evaluation and approval services are
                connected. Review pending sources before using
                them for intelligence analysis.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Recently Registered Sources")

    recent_sources = approved_sources + pending_sources

    for source in recent_sources[:5]:

        with st.container(border=True):

            left, right = st.columns([3, 1])

            with left:
                st.markdown(f"**{source['name']}**")
                st.caption(source["category"])

            with right:

                status = (
                    "Approved"
                    if source.get("approved") == 1
                    else "Pending review"
                )

                st.caption(status)


# ==================================================
# 8. COMPANY INTERVIEW PAGE
# ==================================================

elif page == "Company Interview":

    st.markdown(
        '<div class="eyebrow">COMPANY DISCOVERY</div>',
        unsafe_allow_html=True
    )

    st.title("Company Interview")

    st.write(
        f"Build the business context for **{selected_company}**."
    )

    st.write(
        "Answer these questions to help Signal Stack understand "
        "the company's business, customers, competitors and goals."
    )

    st.divider()

    questions = interview_service.get_questions()
    saved_answers = interview_service.get_answers(company_id)

    answers_by_question = {}

    for answer in saved_answers:
        answers_by_question[answer["question"]] = answer

    answered_count = sum(
        1 for question in questions
        if (
            question in answers_by_question
            and answers_by_question[question]["answer"]
            and answers_by_question[question]["answer"].strip()
        )
    )

    total_questions = len(questions)
    remaining = total_questions - answered_count

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Questions", total_questions)
    col2.metric("Answered", answered_count)
    col3.metric("Remaining", remaining)

    progress = answered_count / total_questions if total_questions else 0

    st.progress(progress)

    st.caption(
        f"Interview completion: {int(progress * 100)}%"
    )

    st.divider()

    st.subheader("Business Discovery Questions")

    for index, question in enumerate(questions):

        existing_answer = answers_by_question.get(question)

        if existing_answer:
            initial_answer = existing_answer["answer"] or ""
            answer_id = existing_answer["id"]
            status = "Answered"
        else:
            initial_answer = ""
            answer_id = None
            status = "Not answered"

        with st.expander(
            f"Question {index + 1}: {question}  ·  {status}",
            expanded=(existing_answer is None)
        ):

            answer_text = st.text_area(
                "Your answer",
                value=initial_answer,
                height=120,
                placeholder="Write your company's answer here...",
                key=f"interview_answer_{company_id}_{index}"
            )

            button_label = (
                "Update Answer"
                if existing_answer
                else "Save Answer"
            )

            if st.button(
                button_label,
                key=f"save_interview_{company_id}_{index}"
            ):

                if not answer_text.strip():

                    st.warning("Please enter an answer first.")

                else:

                    try:

                        if answer_id is not None:

                            success = interview_service.update_answer(
                                answer_id,
                                answer_text
                            )

                        else:

                            success = interview_service.save_answer(
                                company_id,
                                question,
                                answer_text
                            )

                        if success:
                            st.success("Answer saved successfully!")
                            st.rerun()
                        else:
                            st.error("Could not update the answer.")

                    except Exception as error:
                        st.error(f"Unable to save answer: {error}")

    st.divider()

    if answered_count == total_questions:

        st.success(
            "Company interview completed! All 10 questions have answers."
        )

    else:

        st.info(
            f"{remaining} question(s) are still waiting for answers."
        )

    st.caption(
        "SIGNAL STACK · COMPANY INTELLIGENCE PLATFORM"
    )


# ==================================================
# 9. SOURCE MANAGER PAGE
# ==================================================

elif page == "Source Manager":

    st.markdown(
        '<div class="eyebrow">SOURCE CONTROL CENTER</div>',
        unsafe_allow_html=True
    )

    st.title("Source Manager")

    st.write(
        "Evaluate, search, review and manage company intelligence sources."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Sources", total_sources)
    col2.metric("Approved", approved_count)
    col3.metric("Awaiting Review", pending_count)

    st.divider()

    st.subheader("Find Sources")

    filter_col1, filter_col2 = st.columns([2, 1])

    with filter_col1:

        search_text = st.text_input(
            "Search sources",
            placeholder="Search by source name or website..."
        )

    categories = [
        "All Categories",
        "Customers",
        "Competitors",
        "Market",
        "Internal Intelligence"
    ]

    with filter_col2:

        selected_category = st.selectbox(
            "Filter by category",
            categories
        )

    st.divider()

    st.subheader("Approved Sources")

    filtered_approved = [
        source for source in approved_sources
        if matches_filters(
            source,
            search_text,
            selected_category
        )
    ]

    if filtered_approved:

        for source in filtered_approved:

            with st.expander(f"🟢  {source['name']}"):

                st.write("**Website:**", source["url"])
                st.write("**Category:**", source["category"])
                st.write("**Reason:**", source["reason"])

    else:

        st.info("No approved sources match these filters.")

    st.divider()

    st.subheader("Pending Sources")

    filtered_pending = [
        source for source in pending_sources
        if matches_filters(
            source,
            search_text,
            selected_category
        )
    ]

    st.caption(
        f"Showing {len(filtered_pending)} of "
        f"{len(pending_sources)} pending sources"
    )

    if filtered_pending:

        for source in filtered_pending:

            evaluation = source.get("quality_evaluation") or {}
            score = evaluation.get("score", 0) or 0

            with st.expander(
                f"◈  {source['name']}  |  {score}/100"
            ):

                st.markdown(f"**Website:** {source['url']}")
                st.markdown(f"**Category:** {source['category']}")
                st.markdown(f"**Reason:** {source['reason']}")

                st.divider()

                display_quality_evaluation(evaluation)

                st.divider()

                st.markdown("#### Human Review")

                st.caption(
                    "The recommendation is advisory. "
                    "A human reviewer makes the final decision."
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "✓ Approve Source",
                        key=f"approve_{source['source_id']}",
                        use_container_width=True
                    ):

                        workflow_service.approve_source(
                            source["source_id"]
                        )

                        st.success("Source approved.")
                        st.rerun()

                with col2:

                    if st.button(
                        "✕ Reject Source",
                        key=f"reject_{source['source_id']}",
                        use_container_width=True
                    ):

                        workflow_service.reject_source(
                            source["source_id"]
                        )

                        st.warning("Source rejected.")
                        st.rerun()

    else:

        st.success("No pending sources match these filters.")

    st.divider()

    st.caption(
        "SIGNAL STACK · COMPANY INTELLIGENCE PLATFORM"
    )


# ==================================================
# 10. INTERNAL DOCUMENTS PAGE
# ==================================================

elif page == "Internal Documents":

    st.markdown(
        '<div class="eyebrow">INTERNAL INTELLIGENCE</div>',
        unsafe_allow_html=True
    )

    st.title("Internal Documents")

    st.write(
        f"Upload and manage internal business documents for "
        f"**{selected_company}**."
    )

    st.caption(
        "Supported formats: CSV, XLSX, PDF and TXT. "
        "Maximum file size: 10 MB."
    )

    st.divider()

    st.subheader("Upload a Document")

    uploaded_file = st.file_uploader(
        "Choose a company document",
        type=["csv", "xlsx", "pdf", "txt"],
        key=f"internal_upload_{company_id}"
    )

    if uploaded_file is not None:

        if st.button(
            "Upload and Extract Text",
            key=f"upload_button_{company_id}"
        ):

            try:
                result = upload_service.upload_file(
                    company_id,
                    uploaded_file
                )

                st.success(
                    f"Successfully uploaded {result['file_name']}"
                )

                st.write(
                    f"Extracted characters: "
                    f"{result['characters_extracted']}"
                )

                st.rerun()

            except Exception as error:
                st.error(f"Upload failed: {error}")

    st.divider()

    st.subheader("Uploaded Documents")

    documents = upload_service.get_documents(company_id)

    if not documents:

        st.info(
            "No internal documents uploaded for this company yet."
        )

    else:

        st.metric("Total Documents", len(documents))

        for document in documents:

            with st.expander(
                f"{document['file_name']} "
                f"· {document['file_type']}"
            ):

                col1, col2 = st.columns(2)

                with col1:
                    st.caption(
                        f"Document ID: {document['id']}"
                    )

                    st.caption(
                        f"File size: "
                        f"{document['file_size'] / 1024:.2f} KB"
                    )

                with col2:
                    st.caption(
                        f"Uploaded: {document['uploaded_at']}"
                    )

                    st.caption(
                        f"Status: {document['extraction_status']}"
                    )

                document_text = upload_service.get_document_text(
                    document["id"],
                    company_id
                )

                if document_text:

                    st.text_area(
                        "Extracted Text Preview",
                        value=document_text[:5000],
                        height=200,
                        disabled=True,
                        key=f"preview_{document['id']}"
                    )

                    if len(document_text) > 5000:
                        st.caption(
                            "Preview limited to 5,000 characters. "
                            "The extracted text is stored in full "
                            "up to the service limit."
                        )

                if st.button(
                    "Delete Document",
                    key=f"delete_document_{document['id']}"
                ):

                    deleted = upload_service.delete_document(
                        document["id"],
                        company_id
                    )

                    if deleted:
                        st.success("Document deleted successfully.")
                        st.rerun()
                    else:
                        st.error("Document could not be deleted.")

    st.divider()

    st.caption(
        "SIGNAL STACK · INTERNAL INTELLIGENCE"
    )


# ==================================================
# 11. REPORTS PAGE
# ==================================================

elif page == "Reports":

    st.markdown(
        '<div class="eyebrow">INTELLIGENCE REPORTS</div>',
        unsafe_allow_html=True
    )

    st.title("Monday Morning Briefs")

    st.write(f"Reports for **{selected_company}**")

    st.divider()

    reports = get_company_reports(company_id)

    if not reports:

        st.info(
            "No reports have been generated for this company yet."
        )

        st.caption(
            "Generate a report using the report generation service."
        )

    else:

        st.metric("Saved Reports", len(reports))

        report_options = {
            (
                f"Report #{report['id']} | "
                f"{report['created_at']}"
            ): report
            for report in reports
        }

        selected_report_label = st.selectbox(
            "Select a report",
            options=list(report_options.keys())
        )

        selected_report = report_options[selected_report_label]

        st.divider()

        st.subheader(selected_report["title"])

        st.caption(
            f"Report ID: {selected_report['id']} | "
            f"Generated: {selected_report['created_at']}"
        )

        st.divider()

        st.markdown("### Full Report")

        st.text_area(
            "Report Content",
            value=selected_report["content"],
            height=650,
            disabled=True,
            label_visibility="collapsed"
        )

        st.download_button(
            label="Download Report",
            data=selected_report["content"],
            file_name=(
                f"signal_stack_report_"
                f"{selected_report['id']}.txt"
            ),
            mime="text/plain",
            use_container_width=True
        )

    st.divider()

    st.caption(
        "SIGNAL STACK · COMPANY INTELLIGENCE PLATFORM"
    )
