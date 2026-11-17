
from services.competitor_gap_analysis_service import CompetitorGapAnalysisService


class OpportunityAnalysisService:

    PRIORITY_RULES = {
        "Services": "High",
        "Destinations": "Medium",
        "Other offerings": "Medium"
    }

    def __init__(self):
        self.gap_service = CompetitorGapAnalysisService()

    def analyze_opportunities(self, company_id):
        gap_result = self.gap_service.analyze_gaps(company_id)

        opportunities = []

        for gap in gap_result.get("potential_gaps", []):

            category = gap["category"]
            area = gap["area"]
            competitors = gap["competitors_with_evidence"]

            if category == "Services":
                impact = (
                    "Potential to review service coverage and identify "
                    "ways to strengthen the company's education offering."
                )

            elif category == "Destinations":
                impact = (
                    "Potential to review destination coverage and identify "
                    "additional student markets."
                )

            else:
                impact = (
                    "Potential to review additional student support "
                    "and engagement offerings."
                )

            opportunities.append({
                "title": f"Explore {area.title()}",
                "category": category,
                "description": gap["observation"],
                "supporting_competitors": competitors,
                "evidence_count": len(competitors),
                "potential_impact": impact,
                "recommended_action": gap["suggested_action"],
                "priority": self.PRIORITY_RULES.get(
                    category, "Needs Review"
                ),
                "status": "Needs Human Review",
                "confidence": gap["confidence"]
            })

        opportunities.sort(
            key=lambda item: (
                {"High": 1, "Medium": 2}.get(item["priority"], 3),
                -item["evidence_count"]
            )
        )

        return {
            "company_id": company_id,
            "opportunities_identified": len(opportunities),
            "opportunities": opportunities,
            "limitations": gap_result.get("limitations", []) + [
                "Priority labels are preliminary rules, not measured business impact.",
                "All opportunities require human review before implementation."
            ]
        }
