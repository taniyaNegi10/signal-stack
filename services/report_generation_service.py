
from datetime import datetime

from database import get_connection
from services.signal_analysis_service import SignalAnalysisService
from services.competitor_analysis_service import CompetitorAnalysisService
from services.competitor_gap_analysis_service import CompetitorGapAnalysisService
from services.opportunity_analysis_service import OpportunityAnalysisService


class ReportGenerationService:

    def __init__(self):
        self.signal_service = SignalAnalysisService()
        self.competitor_service = CompetitorAnalysisService()
        self.gap_service = CompetitorGapAnalysisService()
        self.opportunity_service = OpportunityAnalysisService()

    def generate_report(self, company_id):

        company = self._get_company(company_id)

        if not company:
            raise ValueError("Company not found.")

        company_context = self._get_company_context(company_id)
        internal_documents = self._get_internal_documents(company_id)

        signals_result = self.signal_service.analyze_signals(company_id)
        competitor_profiles = self.competitor_service.build_profiles(company_id)
        gaps_result = self.gap_service.analyze_gaps(company_id)
        opportunities_result = self.opportunity_service.analyze_opportunities(
            company_id
        )

        signals = signals_result.get("signals", [])
        opportunities = opportunities_result.get("opportunities", [])
        gaps = gaps_result.get("gaps", [])

        sections = {
            "Company Profile & Business Context": self._company_profile_section(
                company, company_context
            ),

            "Executive Summary": self._executive_summary(
                company,
                signals,
                opportunities,
                company_context,
                internal_documents
            ),

            "Customer Signals": self._signals_by_category(
                signals, "Customers"
            ),

            "Competitor Intelligence": self._competitor_intelligence(
                competitor_profiles, signals
            ),

            "Market Intelligence": self._signals_by_category(
                signals, "Market"
            ),

            "Internal Business Intelligence": self._internal_business_intelligence(
                signals, internal_documents
            ),

            "Opportunities Identified": self._opportunities_section(
                opportunities
            ),

            "Risks & Threats": self._risks_section(gaps, signals),

            "Recommended Actions for This Week": self._actions_section(
                signals, opportunities
            ),

            "What We Should Watch": self._watch_section(
                signals, gaps, company_context
            ),

            "Source Appendix": self._source_appendix(company_id)
        }

        report_content = self._format_report(company, sections)

        report_id = self._save_report(company_id, report_content)

        return {
            "company_id": company_id,
            "company_name": company["name"],
            "report_id": report_id,
            "title": f"Monday Morning Brief - {company['name']}",
            "sections": sections,
            "content": report_content,
            "company_context_questions_used": len(company_context),
            "signals_used": len(signals),
            "competitors_used": len(competitor_profiles),
            "opportunities_used": len(opportunities),
            "internal_documents_used": len(internal_documents),
            "generated_at": datetime.now().isoformat(),
            "limitations": [
                "Company context is based on saved interview answers.",
                "Interview answers may contain suggested or unverified information.",
                "The report uses currently stored research and signal records.",
                "Competitor and opportunity findings are preliminary keyword-based analysis.",
                "Uploaded internal documents are user-provided and are not independently verified.",
                "Uploaded document text is included as evidence, not treated as verified fact.",
                "No customer or market signals are invented when none are available.",
                "Recommendations require human review.",
                "This is a manually generated report, not an automated weekly schedule."
            ]
        }

    def _get_company(self, company_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, name, website, industry
            FROM companies
            WHERE id = ?
            """,
            (company_id,)
        )

        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def _get_company_context(self, company_id):
        """
        Retrieves the latest saved answer for each interview question.
        """

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT question, answer, id
            FROM interview_answers
            WHERE company_id = ?
            ORDER BY id DESC
            """,
            (company_id,)
        )

        rows = cursor.fetchall()
        conn.close()

        company_context = {}

        for row in rows:
            question = row["question"]

            if question not in company_context:
                company_context[question] = row["answer"]

        return company_context

    def _get_internal_documents(self, company_id):
        """
        Retrieves extracted text from uploaded documents belonging
        only to the selected company.

        The report includes up to the 20 most recently uploaded documents.
        Each document's preview is limited to 8,000 characters.
        """

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                file_name,
                file_type,
                extraction_status,
                extracted_text,
                uploaded_at
            FROM internal_documents
            WHERE company_id = ?
            ORDER BY uploaded_at DESC, id DESC
            LIMIT 20
            """,
            (company_id,)
        )

        rows = cursor.fetchall()
        conn.close()

        documents = []

        for row in rows:

            extracted_text = row["extracted_text"] or ""

            if row["extraction_status"] != "success":
                continue

            if not extracted_text.strip():
                continue

            documents.append({
                "document_id": row["id"],
                "file_name": row["file_name"],
                "file_type": row["file_type"],
                "uploaded_at": row["uploaded_at"],
                "extraction_status": row["extraction_status"],
                "evidence_type": "User-provided internal document",
                "extracted_text": extracted_text[:8000],
                "text_truncated": len(extracted_text) > 8000
            })

        return documents

    def _company_profile_section(self, company, context):

        return {
            "company_name": company["name"],
            "website": company["website"],
            "industry": company.get("industry"),

            "what_the_company_does": context.get(
                "What does your company do?",
                "Not provided in company interview."
            ),

            "products_and_services": context.get(
                "What products or services does your company offer?",
                "Not provided in company interview."
            ),

            "ideal_customers": context.get(
                "Who are your ideal customers?",
                "Not provided in company interview."
            ),

            "industries_and_markets": context.get(
                "Which industries or markets do you serve?",
                "Not provided in company interview."
            ),

            "competitive_differentiation": context.get(
                "What makes your company different from competitors?",
                "Not provided in company interview."
            ),

            "main_competitors": context.get(
                "Who are your main competitors?",
                "Not provided in company interview."
            ),

            "business_goals": context.get(
                "What are your company's biggest business goals?",
                "Not provided in company interview."
            ),

            "business_challenges": context.get(
                "What are the biggest challenges your company currently faces?",
                "Not provided in company interview."
            ),

            "market_trends": context.get(
                "Which market trends could affect your company?",
                "Not provided in company interview."
            ),

            "monitoring_priorities": context.get(
                "What important developments should Signal Stack monitor?",
                "Not provided in company interview."
            )
        }

    def _executive_summary(
        self,
        company,
        signals,
        opportunities,
        company_context,
        internal_documents
    ):

        return {
            "company": company["name"],
            "website": company["website"],
            "industry": company.get("industry"),
            "interview_answers_available": len(company_context),
            "total_signals": len(signals),
            "total_opportunities": len(opportunities),
            "internal_documents_available": len(internal_documents),

            "high_priority_opportunities": sum(
                1 for item in opportunities
                if item.get("priority") == "High"
            ),

            "summary": (
                f"The current research contains {len(signals)} stored signals "
                f"and {len(opportunities)} preliminary opportunities. "
                f"The report also uses {len(company_context)} saved company "
                f"interview answers and {len(internal_documents)} uploaded "
                "internal documents as business context. "
                "Uploaded documents are user-provided evidence and have "
                "not been independently verified. Findings require human review."
            )
        }

    def _signals_by_category(self, signals, category):

        matching = [
            signal for signal in signals
            if (signal.get("category") or "").lower() == category.lower()
        ]

        if not matching:
            return ["No stored signals available for this category."]

        return matching

    def _internal_business_intelligence(
        self, signals, internal_documents
    ):
        """
        Combines stored internal intelligence signals with uploaded
        internal documents without treating document text as verified facts.
        """

        internal_signals = self._signals_by_category(
            signals, "Internal Intelligence"
        )

        return {
            "stored_internal_signals": internal_signals,

            "uploaded_internal_documents": internal_documents,

            "uploaded_document_count": len(internal_documents),

            "evidence_note": (
                "Uploaded documents are user-provided material. "
                "Their contents have not been independently verified. "
                "They should be reviewed before business decisions are made."
            )
        }

    def _competitor_intelligence(self, profiles, signals):

        competitor_signals = [
            signal for signal in signals
            if (signal.get("category") or "").lower() == "competitors"
        ]

        return {
            "competitors_researched": len(profiles),
            "competitor_profiles": profiles,
            "stored_competitor_signals": competitor_signals
        }

    def _opportunities_section(self, opportunities):

        if not opportunities:
            return ["No opportunities identified in available research."]

        return opportunities

    def _risks_section(self, gaps, signals):

        risks = []

        for gap in gaps:
            risks.append({
                "area": gap.get("area"),
                "category": gap.get("category"),
                "observation": gap.get("observation"),
                "confidence": gap.get("confidence"),
                "status": "Potential risk - requires human verification"
            })

        high_urgency = [
            signal for signal in signals
            if signal.get("urgency") == "High"
        ]

        for signal in high_urgency:
            risks.append({
                "area": signal.get("title"),
                "category": signal.get("category"),
                "observation": signal.get("why_it_matters"),
                "status": "High urgency signal - requires human review"
            })

        if not risks:
            return ["No risks identified from the currently stored evidence."]

        return risks

    def _actions_section(self, signals, opportunities):

        actions = []

        for signal in signals:
            actions.append({
                "action": signal.get("recommended_action"),
                "priority": signal.get("urgency"),
                "evidence": signal.get("title")
            })

        for opportunity in opportunities:
            actions.append({
                "action": opportunity.get("recommended_action"),
                "priority": opportunity.get("priority"),
                "evidence": opportunity.get("title")
            })

        if not actions:
            return ["No actions generated from available evidence."]

        return actions

    def _watch_section(self, signals, gaps, company_context):

        watch_items = []

        for signal in signals:
            watch_items.append(
                f"Monitor developments related to: {signal.get('title')}"
            )

        for gap in gaps:
            watch_items.append(
                f"Verify potential gap: {gap.get('area')}"
            )

        monitoring_priorities = company_context.get(
            "What important developments should Signal Stack monitor?"
        )

        if monitoring_priorities:
            watch_items.append(
                "Company-defined monitoring priorities: "
                + monitoring_priorities
            )

        if not watch_items:
            return ["Collect additional evidence before defining watch items."]

        return watch_items

    def _source_appendix(self, company_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, name, url, category
            FROM sources
            WHERE company_id = ? AND approved = 1
            ORDER BY id
            """,
            (company_id,)
        )

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "source_id": row["id"],
                "name": row["name"],
                "url": row["url"],
                "category": row["category"]
            }
            for row in rows
        ]

    def _format_report(self, company, sections):

        lines = [
            "=" * 75,
            f"MONDAY MORNING BRIEF - {company['name']}",
            f"Website: {company['website']}",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "=" * 75
        ]

        for section_name, content in sections.items():
            lines.append("")
            lines.append(section_name.upper())
            lines.append("-" * 75)
            lines.append(str(content))

        lines.append("")
        lines.append("=" * 75)
        lines.append("END OF REPORT")
        lines.append("=" * 75)

        return "\n".join(lines)

    def _save_report(self, company_id, content):

        conn = get_connection()
        cursor = conn.cursor()

        title = (
            f"Monday Morning Brief - "
            f"{datetime.now().strftime('%Y-%m-%d')}"
        )

        cursor.execute(
            """
            INSERT INTO reports (company_id, title, content)
            VALUES (?, ?, ?)
            """,
            (company_id, title, content)
        )

        report_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return report_id
