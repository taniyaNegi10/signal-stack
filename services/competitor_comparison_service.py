
from services.competitor_analysis_service import CompetitorAnalysisService


class CompetitorComparisonService:

    def __init__(self):
        self.analysis_service = CompetitorAnalysisService()

    def compare_competitors(self, company_id):
        profiles = self.analysis_service.build_profiles(company_id)

        if not profiles:
            return {
                "competitors_compared": 0,
                "comparison": [],
                "opportunities": [],
                "limitations": ["No competitor research is available."]
            }

        comparison = []
        all_findings = {}

        for profile in profiles:
            competitor_name = profile["competitor_name"]
            findings = profile.get("findings", {})

            services = findings.get("Services mentioned", [])
            destinations = findings.get("Study destinations mentioned", [])
            offerings = findings.get("Other offerings mentioned", [])

            # Extract keywords while preserving their supporting evidence.
            services = [
                item["keyword"] for item in services
            ]

            destinations = [
                item["keyword"] for item in destinations
            ]

            offerings = [
                item["keyword"] for item in offerings
            ]

            all_findings[competitor_name] = {
                "services": services,
                "destinations": destinations,
                "other_offerings": offerings
            }

            comparison.append({
                "competitor": competitor_name,
                "website": profile["website"],
                "services": services,
                "destinations": destinations,
                "other_offerings": offerings,
                "evidence_count": (
                    len(services) + len(destinations) + len(offerings)
                ),
                "research_date": profile["researched_at"]
            })

        opportunities = self._identify_opportunities(all_findings)

        return {
            "competitors_compared": len(comparison),
            "comparison": comparison,
            "opportunities": opportunities,
            "limitations": [
                "Comparison is based on keywords found in saved page titles, descriptions and headings.",
                "A missing keyword does not prove that a competitor does not offer a service.",
                "Findings require human verification before business decisions."
            ]
        }

    def _identify_opportunities(self, all_findings):
        opportunities = []
        service_counts = {}

        for competitor, findings in all_findings.items():
            for service in findings["services"]:
                service_counts.setdefault(service, []).append(competitor)

        for service, competitors in service_counts.items():
            if len(competitors) >= 2:
                opportunities.append({
                    "area": service,
                    "observation": (
                        f"This keyword appeared in research for "
                        f"{len(competitors)} competitors."
                    ),
                    "evidence": competitors,
                    "suggested_action": (
                        "Review this service area and assess whether "
                        "MeetUniversity should strengthen its offering."
                    ),
                    "confidence": "Keyword-based observation; human review required."
                })

        return opportunities
