
import re

from database import get_connection


class SignalAnalysisService:

    CATEGORY_KEYWORDS = {
        "customers": [
            "student", "customer", "feedback", "satisfaction",
            "complaint", "experience", "enrollment", "application",
            "admission", "retention"
        ],
        "competitors": [
            "competitor", "partnership", "pricing", "launch",
            "expansion", "acquisition", "market share",
            "new service", "new product"
        ],
        "market": [
            "market", "industry", "policy", "regulation",
            "sales", "revenue", "growth", "investment",
            "financial", "results", "demand", "electric",
            "technology", "partnership", "launch", "export",
            "units", "quarter", "acquisition", "competition"
        ],
        "internal intelligence": [
            "internal", "operations", "employee", "staff",
            "process", "performance", "crm", "sales team",
            "customer feedback", "internal report"
        ]
    }

    EVENT_KEYWORDS = [
        "announced", "launch", "launched", "partnership",
        "acquisition", "growth", "decline", "investment",
        "expansion", "agreement", "results", "revenue",
        "sales", "collaboration", "regulation"
    ]

    URGENT_PHRASES = [
        "urgent",
        "product recall",
        "service suspension",
        "service disruption",
        "regulatory ban",
        "regulatory warning",
        "security incident",
        "immediate action required",
        "application deadline"
    ]

    def analyze_signals(self, company_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                title,
                content,
                category,
                impact,
                relevance_score,
                source_url,
                published_at
            FROM signals
            WHERE company_id = ?
            ORDER BY discovered_at DESC
            """,
            (company_id,)
        )

        rows = cursor.fetchall()
        conn.close()

        analyzed_signals = []

        for row in rows:

            signal = dict(row)

            title = signal.get("title") or "Untitled signal"
            content = signal.get("content") or ""
            category = signal.get("category") or "Uncategorized"
            existing_impact = signal.get("impact") or ""

            relevance_score, score_reasons = (
                self._calculate_relevance_score(
                    category,
                    title,
                    content,
                    signal.get("source_url")
                )
            )

            urgency = self._determine_urgency(
                category,
                existing_impact,
                relevance_score,
                content
            )

            why_it_matters = self._explain_importance(
                category,
                title,
                content
            )

            business_impact = self._assess_business_impact(
                category,
                existing_impact
            )

            recommended_action = self._recommend_action(
                category,
                urgency
            )

            analyzed_signals.append({
                "signal_id": signal["id"],
                "title": title,
                "category": category,
                "content": content,
                "why_it_matters": why_it_matters,
                "business_impact": business_impact,
                "urgency": urgency,
                "recommended_action": recommended_action,
                "source_url": signal.get("source_url"),
                "published_at": signal.get("published_at"),
                "relevance_score": relevance_score,
                "score_reasons": score_reasons,
                "analysis_type": "Explainable rule-based preliminary analysis",
                "requires_human_review": True
            })

        return {
            "company_id": company_id,
            "total_signals_analyzed": len(analyzed_signals),
            "signals": analyzed_signals,
            "limitations": [
                "Relevance scores are calculated using predefined keywords.",
                "A relevance score is not a measure of source credibility.",
                "Page-level content may contain multiple separate developments.",
                "Business impact is an interpretation, not a verified outcome.",
                "Analysis does not establish causation.",
                "Signals require human review before business decisions."
            ]
        }

    def _calculate_relevance_score(
        self, category, title, content, source_url
    ):

        category_key = category.lower().strip()
        text = f"{title} {content}".lower()

        keywords = self.CATEGORY_KEYWORDS.get(
            category_key, []
        )

        matched_category = [
            word for word in keywords if word in text
        ]

        matched_events = [
            word for word in self.EVENT_KEYWORDS if word in text
        ]

        score = 10
        reasons = []

        if matched_category:
            points = min(len(matched_category), 6) * 6
            score += points
            reasons.append(
                f"Category relevance: {', '.join(matched_category[:6])}"
            )

        if matched_events:
            points = min(len(matched_events), 4) * 5
            score += points
            reasons.append(
                f"Development indicators: {', '.join(matched_events[:4])}"
            )

        if re.search(r"\b(20\d{2}|Q[1-4]|FY\d{2})\b", text):
            score += 8
            reasons.append("Contains date or reporting-period references.")

        if re.search(r"\d", text):
            score += 5
            reasons.append("Contains numerical information.")

        if len(content) >= 200:
            score += 5
            reasons.append("Contains substantial extracted content.")

        if source_url:
            score += 3
            reasons.append("A source URL is available for verification.")

        general_page_terms = [
            "investor relations",
            "official website",
            "home page",
            "about us"
        ]

        if any(term in title.lower() for term in general_page_terms):
            score -= 12
            reasons.append(
                "General webpage: individual developments need separate review."
            )

        score = max(0, min(100, score))

        if not reasons:
            reasons.append(
                "Insufficient matching evidence for a strong relevance assessment."
            )

        return round(score, 2), reasons

    def _determine_urgency(
        self, category, impact, relevance_score, content=""
    ):

        impact = (impact or "").lower()
        content = (content or "").lower()

        combined_text = f"{impact} {content}"

        if any(
            re.search(
                r"\b" + re.escape(phrase) + r"\b",
                combined_text
            )
            for phrase in self.URGENT_PHRASES
        ):
            return "High"

        if relevance_score >= 55:
            return "Medium"

        return "Low"

    def _explain_importance(self, category, title, content):

        explanations = {
            "customers": (
                "This signal may reveal changes in student needs, "
                "customer experience or demand."
            ),
            "competitors": (
                "This signal may indicate competitor activity, "
                "service changes or market positioning."
            ),
            "market": (
                "This signal may reflect a change in industry activity, "
                "market conditions, regulation or business performance."
            ),
            "internal intelligence": (
                "This signal may provide information about the "
                "company's own operations or business activities."
            )
        }

        explanation = explanations.get(
            category.lower(),
            "This signal may contain information relevant to the company."
        )

        if len(content) < 100:
            explanation += (
                " Extracted content is limited, so further verification is needed."
            )

        return explanation

    def _assess_business_impact(self, category, existing_impact):

        category = category.lower()

        impacts = {
            "customers": (
                "Potential impact on student satisfaction, "
                "customer experience or demand."
            ),
            "competitors": (
                "Potential impact on competitive positioning "
                "and service strategy."
            ),
            "market": (
                "Potential impact on market opportunities, "
                "business planning or industry positioning."
            ),
            "internal intelligence": (
                "Potential impact on internal operations "
                "and decision-making."
            )
        }

        result = impacts.get(
            category,
            "Potential business impact requires further investigation."
        )

        if existing_impact and existing_impact.lower() not in [
            "needs assessment",
            "unknown",
            "none"
        ]:
            result += (
                f" Existing database note: {existing_impact}. "
                "Verify this information independently."
            )

        return result

    def _recommend_action(self, category, urgency):

        actions = {
            "customers": (
                "Review the evidence and assess whether a customer response is needed."
            ),
            "competitors": (
                "Verify the competitor activity and assess its strategic relevance."
            ),
            "market": (
                "Review the development, verify its date and evidence, "
                "and assess its implications for the business."
            ),
            "internal intelligence": (
                "Share with the relevant internal team for review."
            )
        }

        action = actions.get(
            category.lower(),
            "Review the signal and verify its relevance."
        )

        if urgency == "High":
            return "Prioritize human review. " + action

        if urgency == "Medium":
            return "Schedule for review. " + action

        return action
