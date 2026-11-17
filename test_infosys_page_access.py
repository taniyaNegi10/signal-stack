from services.source_service import SourceService
from services.research_service import ResearchService

source_service = SourceService()
research_service = ResearchService()

company_id = 4
sources = source_service.get_sources(company_id)

print("INFOSYS PAGE ACCESS TEST")
print("=" * 60)

for source in sources:
    print("\nSource:", source["name"])
    print("URL:", source["url"])

    result = research_service.research_website(source["url"])

    print("Status:", result.get("status"))
    print("Error:", result.get("error"))
    print("Title:", result.get("title"))
    print("Description:", result.get("description"))
    print("Headings:", result.get("headings"))

    print("-" * 60)