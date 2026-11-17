
from services.source_quality_service import SourceQualityService


quality_service = SourceQualityService()


ugc_source = {
    "name": "University Grants Commission",
    "url": "https://www.ugc.gov.in/",
    "category": "Market"
}

ugc_page = {
    "status": "success",
    "title": "University Grants Commission",
    "description": "Higher education and university regulation in India.",
    "headings": [
        "University Grants Commission",
        "Higher Education"
    ]
}


company_source = {
    "name": "MeetUniversity Official Website",
    "url": "https://www.meetuniversity.com/",
    "category": "Internal Intelligence"
}

company_page = {
    "status": "success",
    "title": "Meet University",
    "description": "Official company website providing education services.",
    "headings": [
        "About Us",
        "Our Services",
        "Contact Us"
    ]
}


failed_source = {
    "name": "Example Source",
    "url": "https://example.com/",
    "category": "Market"
}

failed_page = {
    "status": "failed",
    "title": "",
    "description": "",
    "headings": []
}


test_cases = [
    ("UGC", ugc_source, ugc_page),
    ("MeetUniversity", company_source, company_page),
    ("Inaccessible Source", failed_source, failed_page)
]


for name, source, page in test_cases:

    result = quality_service.evaluate_source(source, page)

    print("\nSOURCE:", name)
    print("Total Score:", result["score"])
    print("Accessibility:", result["accessibility_score"])
    print("Relevance:", result["relevance_score"])
    print("Credibility:", result["credibility_score"])
    print("Category Fit:", result["category_fit_score"])
    print("Quality:", result["quality"])
    print("Recommendation:", result["recommendation"])

    print("Reasons:")

    for reason in result["reasons"]:
        print("-", reason)

    print("-" * 50)
