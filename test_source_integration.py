
from services.company_service import CompanyService
from services.source_service import SourceService
from services.source_discovery_service import SourceDiscoveryService



company_service = CompanyService()
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
    raise ValueError("MeetUniversity not found in database.")

company_id = company["id"]



discovery_service = SourceDiscoveryService()
discovered_sources = discovery_service.discover_sources()



source_service = SourceService()

print("\nSAVING DISCOVERED SOURCES\n")

for source in discovered_sources:

    if source["status"] != "accessible":
        print(
            "Skipped:",
            source["name"],
            "| Status:",
            source["status"]
        )
        continue

    source_id = source_service.add_source(
        company_id=company_id,
        name=source["name"],
        url=source["final_url"],
        category=source["category"],
        reason=source["reason"]
    )

    if source_id is None:
        print("Already exists:", source["name"])
    else:
        print(
            "Saved:",
            source["name"],
            "| ID:",
            source_id
        )


print("\nPENDING SOURCES\n")

all_sources = source_service.get_sources(company_id)

for source in all_sources:
    if source["approved"] == 0:
        print(
            source["name"],
            "| Approved:",
            source["approved"]
        )
