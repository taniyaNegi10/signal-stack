
from services.company_service import CompanyService
from services.source_service import SourceService
from services.research_service import ResearchService
from services.research_storage_service import ResearchStorageService



company_service = CompanyService()
source_service = SourceService()
research_service = ResearchService()
storage_service = ResearchStorageService()



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


all_sources = source_service.get_sources(company_id)

competitors = [
    source for source in all_sources
    if source["category"] == "Competitors"
    and source["approved"] == 1
]


print("\nCOMPETITOR RESEARCH")
print("-------------------")

if not competitors:
    print(
        "No approved competitor sources found."
    )
    print(
        "Review and approve competitor sources "
        "through the Source Manager first."
    )
    raise SystemExit



success_count = 0
failed_count = 0

for competitor in competitors:

    name = competitor["name"]
    url = competitor["url"]

    print("\nResearching:", name)
    print("Website:", url)

    try:

        research_data = research_service.research_website(url)

        if research_data.get("status") != "success":
            print(
                "Research failed:",
                research_data.get("error", "Unknown error")
            )
            failed_count += 1
            continue

        # Store research under MeetUniversity's company record.
        # The competitor's actual URL is retained as evidence.
        storage_data = dict(research_data)
        storage_data["company_id"] = company_id

        storage_service.save_research(
            company_id,
            storage_data
        )

        print("Research saved successfully!")
        print(
            "Page title:",
            research_data.get("title", "Not available")
        )
        print(
            "Description:",
            research_data.get("description", "Not available")
        )
        print(
            "Headings found:",
            len(research_data.get("headings", []))
        )

        success_count += 1

    except Exception as error:

        print("Research error:", str(error))
        failed_count += 1



print("\nCOMPETITOR RESEARCH SUMMARY")
print("---------------------------")
print("Approved competitors:", len(competitors))
print("Successfully researched:", success_count)
print("Failed:", failed_count)


print("\nSAVED RESEARCH RECORDS")
print("----------------------")

saved_records = storage_service.get_research(company_id)

for record in saved_records:

    print(
        "Title:", record.get("title"),
        "| URL:", record.get("url")
    )

print("\nTotal research records:", len(saved_records))
