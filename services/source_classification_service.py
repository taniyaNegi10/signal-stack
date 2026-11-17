
class SourceClassificationService:

    CATEGORY_KEYWORDS = {
        "Customers": [
            "testimonial",
            "student review",
            "customer review",
            "success story",
            "student experience"
        ],

        "Competitors": [
            "competitor",
            "education consultancy",
            "study abroad agency",
            "overseas education consultant"
        ],

        "Market": [
            "education policy",
            "visa",
            "immigration",
            "scholarship",
            "study abroad",
            "education news",
            "university admission",
            "study in uk",
            "study in usa",
            "study in canada",
            "study in australia",
            "study in ireland",
            "study in germany",
            "study in new zealand",
            "university grants commission",
            "higher education",
            "education regulation",
            "regulatory guidelines"
        ],

        "Internal Intelligence": [
            "about us",
            "contact",
            "contact us",
            "our company",
            "our team",
            "company profile",
            "ivy profile",
            "profile building",
            "meet university blog",
            "our blogs",
            "official website"
        ]
    }

    def classify_source(self, name, title="", description=""):
        """
        Suggest a source category using keyword matching.

        Uses the source name, webpage title and description.
        This is a rule-based classifier, not an AI model.
        """

        text = f"{name} {title} {description}".lower()

        scores = {}

        for category, keywords in self.CATEGORY_KEYWORDS.items():
            scores[category] = sum(
                1
                for keyword in keywords
                if keyword in text
            )

        best_category = max(scores, key=scores.get)
        confidence = scores[best_category]

        if confidence == 0:
            return {
                "category": "Needs Review",
                "confidence": 0,
                "reason": "No matching category keywords found."
            }

        return {
            "category": best_category,
            "confidence": confidence,
            "reason": (
                f"Matched {confidence} keyword(s) "
                f"for {best_category}."
            )
        }
