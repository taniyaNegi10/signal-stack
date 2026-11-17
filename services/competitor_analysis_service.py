
import re
from urllib.parse import urlparse

from services.research_storage_service import ResearchStorageService


class CompetitorAnalysisService:

    COMPANY_WEBSITE = "https://www.meetuniversity.com"

    KEYWORD_GROUPS = {
        "Services mentioned": [
            "study abroad",
            "overseas education",
            "study abroad counselling",
            "career guidance",
            "university admissions",
            "application support",
            "test preparation",
            "visa assistance",
            "scholarships",
            "education consultancy",
        ],

        "Study destinations mentioned": [
            "usa",
            "united states",
            "uk",
            "united kingdom",
            "canada",
            "australia",
            "new zealand",
            "ireland",
            "germany",
        ],

        "Other offerings mentioned": [
            "profile building",
            "testimonials",
            "student community",
            "university partners",
            "course search",
            "free counselling",
        ],
    }

    def __init__(self):
        self.storage_service = ResearchStorageService()

    @staticmethod
    def _normalize_url(url):

        parsed = urlparse(url or "")

        return (
            f"{parsed.scheme.lower()}://"
            f"{parsed.netloc.lower()}"
            f"{parsed.path.rstrip('/')}"
        )

    @staticmethod
    def _heading_to_text(heading):
        """
        Supports headings stored as strings or dictionaries.
        """

        if isinstance(heading, str):
            return heading

        if isinstance(heading, dict):

            for key in (
                "text",
                "title",
                "name",
                "heading",
                "value"
            ):

                value = heading.get(key)

                if isinstance(value, str):
                    return value

            return ""

        return str(heading)

    @staticmethod
    def _contains_phrase(text, phrase):

        pattern = (
            r"(?<![a-zA-Z])"
            + re.escape(phrase)
            + r"(?![a-zA-Z])"
        )

        return re.search(
            pattern,
            text or "",
            re.IGNORECASE
        ) is not None

    def _get_headings(self, research):

        raw_headings = research.get("headings", [])

        if not isinstance(raw_headings, list):
            return []

        headings = []

        for heading in raw_headings:

            heading_text = self._heading_to_text(heading)

            if heading_text.strip():
                headings.append(heading_text.strip())

        return headings

    def _find_evidence(self, research, phrase):

        fields = [
            ("Page title", research.get("title", "")),
            ("Page description", research.get("description", "")),
        ]

        for heading in self._get_headings(research):

            fields.append(
                ("Page heading", heading)
            )

        matches = []

        for field_name, field_text in fields:

            if self._contains_phrase(field_text, phrase):

                matches.append({
                    "location": field_name,
                    "text": field_text.strip(),
                })

        return matches

    def _analyse_research(self, research):

        headings = self._get_headings(research)

        combined_text = " ".join([
            research.get("title", ""),
            research.get("description", ""),
            " ".join(headings),
        ])

        findings = {}

        for group_name, keywords in self.KEYWORD_GROUPS.items():

            group_findings = []

            for keyword in keywords:

                if self._contains_phrase(
                    combined_text,
                    keyword
                ):

                    evidence = self._find_evidence(
                        research,
                        keyword
                    )

                    group_findings.append({
                        "keyword": keyword,
                        "evidence": evidence,
                    })

            findings[group_name] = group_findings

        return findings

    def build_profiles(self, company_id):
        """
        Builds competitor profiles from saved website research.

        Duplicate URLs are represented by their latest research record.
        MeetUniversity itself is excluded from competitor results.
        Historical database records remain unchanged.
        """

        research_records = self.storage_service.get_research(
            company_id
        )

        latest_by_url = {}

        for record in research_records:

            url = record.get("url", "")

            normalized_url = self._normalize_url(url)

            if not normalized_url:
                continue

            existing = latest_by_url.get(normalized_url)

            if existing is None:

                latest_by_url[normalized_url] = record

                continue

            current_date = (
                record.get("researched_at") or ""
            )

            existing_date = (
                existing.get("researched_at") or ""
            )

            if current_date >= existing_date:

                latest_by_url[normalized_url] = record

        profiles = []

        company_url = self._normalize_url(
            self.COMPANY_WEBSITE
        )

       
        for research in latest_by_url.values():

            url = research.get("url", "")

            normalized_url = self._normalize_url(url)

          
            if normalized_url == company_url:
                continue

            domain = urlparse(url).netloc

            headings = self._get_headings(research)

            profile = {

                "company_id": company_id,

                "competitor_name": (
                    domain or "Unknown website"
                ),

                "website": url,

                "page_title": research.get("title", ""),

                "description": research.get(
                    "description",
                    ""
                ),

                "headings_count": len(headings),

                "findings": self._analyse_research(
                    research
                ),

                "researched_at": research.get(
                    "researched_at"
                ),

                "analysis_type": (
                    "Rule-based keyword analysis"
                ),

                "limitation": (
                    "Findings indicate phrases found in "
                    "collected website text. They do not "
                    "independently verify the competitor's "
                    "services or capabilities."
                ),
            }

            profiles.append(profile)

       
        profiles.sort(
            key=lambda profile: (
                profile["competitor_name"].lower()
            )
        )

        return profiles
