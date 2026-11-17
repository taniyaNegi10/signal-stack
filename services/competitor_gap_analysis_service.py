
from urllib.parse import urlparse

from services.competitor_analysis_service import CompetitorAnalysisService
from services.research_storage_service import ResearchStorageService


class CompetitorGapAnalysisService:

    SERVICE_KEYWORDS = [
        "study abroad",
        "overseas education",
        "study abroad counselling",
        "career guidance",
        "university admissions",
        "application support",
        "test preparation",
        "visa assistance",
        "scholarships",
        "education consultancy"
    ]

    DESTINATION_KEYWORDS = [
        "usa", "united states", "uk", "united kingdom",
        "canada", "australia", "new zealand",
        "ireland", "germany"
    ]

    OFFERING_KEYWORDS = [
        "profile building",
        "testimonials",
        "student community",
        "university partners",
        "course search",
        "free counselling"
    ]

    def __init__(self):
        self.analysis_service = CompetitorAnalysisService()
        self.research_storage = ResearchStorageService()

    def _heading_to_text(self, heading):
        if isinstance(heading, dict):
            return str(heading.get("text", ""))

        return str(heading)

    def _extract_findings(self, research):
        text_parts = [
            research.get("title", ""),
            research.get("description", "")
        ]

        headings = research.get("headings", [])

        if isinstance(headings, str):
            import json
            try:
                headings = json.loads(headings)
            except (json.JSONDecodeError, TypeError):
                headings = [headings]

        text_parts.extend(
            self._heading_to_text(item) for item in headings
        )

        page_text = " ".join(text_parts).lower()

        return {
            "services": [
                keyword for keyword in self.SERVICE_KEYWORDS
                if keyword in page_text
            ],
            "destinations": [
                keyword for keyword in self.DESTINATION_KEYWORDS
                if keyword in page_text
            ],
            "other_offerings": [
                keyword for keyword in self.OFFERING_KEYWORDS
                if keyword in page_text
            ]
        }

    def analyze_gaps(self, company_id):
        research_records = self.research_storage.get_research(company_id)

        # Find MeetUniversity's own saved research.
        meetuniversity_records = [
            record for record in research_records
            if "meetuniversity.com" in urlparse(
                record.get("url", "")
            ).netloc.lower()
        ]

        if not meetuniversity_records:
            return {
                "competitors_analyzed": 0,
                "meetuniversity_findings": {},
                "potential_gaps": [],
                "limitations": [
                    "MeetUniversity research was not found in saved records."
                ]
            }

        # Use the latest MeetUniversity research record.
        meetuniversity_records.sort(
            key=lambda item: item.get("researched_at", ""),
            reverse=True
        )

        company_findings = self._extract_findings(
            meetuniversity_records[0]
        )

        company_services = set(company_findings["services"])
        company_destinations = set(company_findings["destinations"])
        company_offerings = set(company_findings["other_offerings"])

        # CompetitorAnalysisService already excludes MeetUniversity.
        competitor_profiles = self.analysis_service.build_profiles(
            company_id
        )

        competitor_evidence = {}

        for profile in competitor_profiles:
            competitor_name = profile["competitor_name"]
            findings = profile.get("findings", {})

            categories = [
                ("Services", "Services mentioned"),
                ("Destinations", "Study destinations mentioned"),
                ("Other offerings", "Other offerings mentioned")
            ]

            for category, finding_key in categories:
                for item in findings.get(finding_key, []):
                    keyword = item["keyword"].lower()

                    competitor_evidence.setdefault(
                        (category, keyword), []
                    ).append(competitor_name)

        potential_gaps = []

        for (category, keyword), competitor_names in competitor_evidence.items():

            if category == "Services":
                already_found = keyword in company_services

            elif category == "Destinations":
                already_found = keyword in company_destinations

            else:
                already_found = keyword in company_offerings

            if not already_found:
                potential_gaps.append({
                    "category": category,
                    "area": keyword,
                    "competitors_with_evidence": sorted(
                        set(competitor_names)
                    ),
                    "observation": (
                        f"The keyword '{keyword}' appeared in competitor "
                        "research but not in the available MeetUniversity research."
                    ),
                    "suggested_action": (
                        "Review MeetUniversity's website and internal information "
                        "to verify whether this is a genuine capability gap."
                    ),
                    "confidence": (
                        "Preliminary research gap; human verification required."
                    )
                })

        return {
            "competitors_analyzed": len(competitor_profiles),
            "meetuniversity_findings": company_findings,
            "potential_gaps": potential_gaps,
            "limitations": [
                "MeetUniversity findings are extracted from its latest saved research record.",
                "Competitor findings are based on saved page titles, descriptions and headings.",
                "Missing keywords do not prove that a company lacks a capability.",
                "Potential gaps require human verification."
            ]
        }
