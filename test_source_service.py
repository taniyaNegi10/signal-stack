
from services.company_service import CompanyService
from services.source_service import SourceService


company_service = CompanyService()
source_service = SourceService()


companies = company_service.get_all_companies()

company = next(
    company for company in companies
    if company["website"] == "https://www.meetuniversity.com"
)

company_id = company["id"]


source_id = source_service.add_source(
    company_id,
    "MeetUniversity Official Website",
    "https://www.meetuniversity.com",
    "Customers",
    "Official website containing information about student services and testimonials."
)

if source_id:
    print("Source added! ID:", source_id)
else:
    print("Source already exists.")


if source_id:
    approved = source_service.approve_source(source_id)
    print("Source approved:", approved)


sources = source_service.get_sources(
    company_id,
    approved_only=True
)

print("\nApproved Sources:")

for source in sources:
    print(dict(source))
