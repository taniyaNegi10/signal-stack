from services.source_service import SourceService
from services.research_service import ResearchService

source_service = SourceService()
research_service = ResearchService()

company_id = 3
sources = source_service.get_sources(company_id)

print("TATA MOTORS PAGE ACCESS TEST")
print("=" * 60)

for source in sources:
    print("\nSource:", source["name"])
    print("URL:", source["url"])

    result = research_service.research_website(source["url"])

    print("Research result:")
    print(result)
    print("-" * 60)