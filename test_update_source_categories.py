
from services.source_service import SourceService
from services.company_service import CompanyService
from services.source_classification_service import SourceClassificationService
from services.research_service import ResearchService

source_service = SourceService()
company_service = CompanyService()
classification_service = SourceClassificationService()
research_service = ResearchService()

# Find MeetUniversity
companies = company_service.get_all_companies()

company = next(
    (
        item for item in companies
        if item["website"].rstrip("/") ==
        "https://www.meetuniversity.com"
    ),
    None
)

if company is None:
    raise ValueError("MeetUniversity not found.")

company_id = company["id"]

# Fetch existing sources
sources = source_service.get_sources(company_id)

print("\nIMPROVED SOURCE CLASSIFICATION\n")

updated_count = 0
review_count = 0
failed_count = 0

for source in sources:

    print("\nChecking:", source["name"])

    try:
        # Fetch actual webpage information
        page_data = research_service.research_website(
            source["url"]
        )

        if page_data.get("status") != "success":
            print("Could not research webpage. Skipping.")
            failed_count += 1
            continue

        # Use source name + actual page title + description
        result = classification_service.classify_source(
            name=source["name"],
            title=page_data.get("title", ""),
            description=page_data.get("description", "")
        )

        category = result["category"]

        print("Page title:", page_data.get("title", ""))
        print("Suggested category:", category)
        print("Reason:", result["reason"])

        if category == "Needs Review":
            print("Manual review required.")
            review_count += 1
            continue

        reason = (
            "Category suggested using webpage metadata "
            "(source name, page title and description). "
            f"{result['reason']} "
            "Requires human verification."
        )

        updated = source_service.update_source_category(
            source_id=source["id"],
            category=category,
            reason=reason
        )

        if updated:
            print("Category updated successfully.")
            updated_count += 1

    except Exception as error:
        print("Error:", error)
        failed_count += 1

print("\n========== SUMMARY ==========")
print("Sources updated:", updated_count)
print("Needs manual review:", review_count)
print("Failed to research:", failed_count)

print("\nFINAL SOURCE LIST\n")

for source in source_service.get_sources(company_id):
    print(
        source["id"],
        "|", source["name"],
        "|", source["category"],
        "| Approved:", source["approved"]
    )
