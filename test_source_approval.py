
from services.company_service import CompanyService
from services.source_service import SourceService


company_service = CompanyService()
source_service = SourceService()


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

sources = source_service.get_sources(company_id)

print("\nPENDING SOURCES\n")

pending_sources = [
    source for source in sources
    if source["approved"] == 0
]

for source in pending_sources:
    print(
        f"ID: {source['id']} | "
        f"Name: {source['name']} | "
        f"Category: {source['category']}"
    )


if pending_sources:
    selected_source = pending_sources[0]

    success = source_service.approve_source(
        selected_source["id"]
    )

    print("\nApproval result:", success)


print("\nAPPROVED SOURCES\n")

approved_sources = source_service.get_sources(
    company_id,
    approved_only=True
)

for source in approved_sources:
    print(
        f"ID: {source['id']} | "
        f"Name: {source['name']} | "
        f"Approved: {source['approved']}"
    )
