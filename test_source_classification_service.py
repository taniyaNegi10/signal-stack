
from services.source_classification_service import SourceClassificationService

service = SourceClassificationService()

test_cases = [
    {
        "name": "Student Testimonials",
        "title": "Student Reviews and Success Stories",
        "description": "Read student experiences and reviews."
    },
    {
        "name": "Meet My Uni",
        "title": "Study Abroad Education Consultancy",
        "description": "Helping students study overseas."
    },
    {
        "name": "Education News",
        "title": "Latest Education Policy Updates",
        "description": "Updates about university admissions."
    },
    {
        "name": "About Us",
        "title": "About MeetUniversity",
        "description": "Learn about our company and team."
    },
    {
        "name": "Study In UK",
        "title": "Study In UK | Meet University",
        "description": ""
    },
    {
        "name": "Immigration",
        "title": "Immigration Services | Meet University",
        "description": ""
    },
    {
        "name": "Ivy",
        "title": "Ivy Profile Building | Meet University",
        "description": ""
    },
    {
        "name": "Blog",
        "title": "Our Blogs | Meet University",
        "description": ""
    }
]

print("\nSOURCE CLASSIFICATION RESULTS\n")

for source in test_cases:

    result = service.classify_source(
        source["name"],
        source["title"],
        source["description"]
    )

    print("Source:", source["name"])
    print("Suggested category:", result["category"])
    print("Matched keywords:", result["confidence"])
    print("Reason:", result["reason"])
    print("-" * 50)
