
from services.company_service import CompanyService
from services.research_service import ResearchService
from services.research_storage_service import ResearchStorageService


company_service = CompanyService()
research_service = ResearchService()
storage_service = ResearchStorageService()


# Find our existing MeetUniversity record
companies = company_service.get_all_companies()

company = next(
    company for company in companies
    if company["website"] == "https://www.meetuniversity.com"
)

company_id = company["id"]

# Research the website
research = research_service.research_website(
    "https://www.meetuniversity.com"
)

# Save successful research
research_id = storage_service.save_research(
    company_id,
    research
)

print("Research saved! ID:", research_id)

# Retrieve saved research
saved_records = storage_service.get_research(company_id)

print("\nSaved Research Records:")

for record in saved_records:
    print("Title:", record["title"])
    print("URL:", record["url"])
    print("Number of headings:", len(record["headings"]))
