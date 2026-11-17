
from urllib.parse import urlparse


class SourceQualityService:

    RELEVANCE_KEYWORDS = {
        "Customers": [
            "testimonial",
            "student review",
            "customer review",
            "success story",
            "student experience",
            "feedback",
            "case study"
        ],

        "Competitors": [
            "education consultancy",
            "study abroad agency",
            "overseas education",
            "study abroad consultant",
            "university admission consultant"
        ],

        "Market": [
            "education policy",
            "visa",
            "immigration",
            "scholarship",
            "study abroad",
            "education news",
            "university admission",
            "higher education",
            "university grants commission",
            "education regulation"
        ],

        "Internal Intelligence": [
            "about us",
            "contact",
            "our company",
            "our team",
            "company profile",
            "services",
            "profile building",
            "our blogs",
            "official website"
        ]
    }

    def evaluate_source(self, source, page_data):
        """
        Evaluate a source using accessibility, relevance,
        credibility indicators and category fit.

        This is a rule-based assessment, not an AI verification system.
        """

        result = {
            "source_name": source.get("name", "Unknown"),
            "url": source.get("url", ""),
            "category": source.get("category", ""),
            "score": 0,
            "accessibility_score": 0,
            "relevance_score": 0,
            "credibility_score": 0,
            "category_fit_score": 0,
            "quality": "Low",
            "recommendation": "Needs Review",
            "reasons": []
        }

       

        if page_data.get("status") == "success":
            result["accessibility_score"] = 25
            result["reasons"].append(
                "Webpage was successfully accessed."
            )
        else:
            result["reasons"].append(
                "Webpage could not be successfully accessed."
            )

       

        title = page_data.get("title", "") or ""
        description = page_data.get("description", "") or ""
        headings = page_data.get("headings", []) or []

        if isinstance(headings, list):
            heading_text = " ".join(str(item) for item in headings)
        else:
            heading_text = str(headings)

        content = (
            source.get("name", "")
            + " "
            + title
            + " "
            + description
            + " "
            + heading_text
        ).lower()

       

        category = source.get("category", "")

        keywords = self.RELEVANCE_KEYWORDS.get(category, [])

        matched_keywords = [
            keyword
            for keyword in keywords
            if keyword in content
        ]

        if matched_keywords:
            relevance_score = min(
                35,
                10 + (len(matched_keywords) * 5)
            )

            result["relevance_score"] = relevance_score

            result["reasons"].append(
                "Relevant keywords found: "
                + ", ".join(matched_keywords)
            )
        else:
            result["reasons"].append(
                "No strong category-relevance keywords found."
            )

       

        domain = urlparse(
            source.get("url", "")
        ).netloc.lower()

        domain = domain.removeprefix("www.")

        credibility_score = 5

        if domain.endswith(".gov.in") or domain.endswith(".gov"):
            credibility_score = 25

            result["reasons"].append(
                "Government-domain indicator found. "
                "This does not independently verify every claim."
            )

        elif domain == "indianexpress.com":
            credibility_score = 20

            result["reasons"].append(
                "Recognized news publisher domain identified."
            )

        elif domain == "meetuniversity.com":
            credibility_score = 15

            result["reasons"].append(
                "Official company-domain indicator found. "
                "Treat its promotional claims as first-party evidence."
            )

        elif domain:
            credibility_score = 8

            result["reasons"].append(
                "Domain identified, but its credibility needs "
                "independent verification."
            )

        else:
            result["reasons"].append(
                "Could not identify a valid source domain."
            )

        result["credibility_score"] = credibility_score

        if title.strip():
            result["credibility_score"] += 0

      

        if category in self.RELEVANCE_KEYWORDS and matched_keywords:
            result["category_fit_score"] = 15

            result["reasons"].append(
                "Content contains keywords supporting its assigned category."
            )
        else:
            result["reasons"].append(
                "Assigned category requires manual verification."
            )

       

        result["score"] = (
            result["accessibility_score"]
            + result["relevance_score"]
            + result["credibility_score"]
            + result["category_fit_score"]
        )


        if result["score"] >= 75:
            result["quality"] = "High"
            result["recommendation"] = "Recommended for Review"

        elif result["score"] >= 45:
            result["quality"] = "Medium"
            result["recommendation"] = "Needs Human Review"

        else:
            result["quality"] = "Low"
            result["recommendation"] = "Do Not Approve Yet"

       
        if page_data.get("status") != "success":
            result["recommendation"] = "Do Not Approve Yet"

        return result
