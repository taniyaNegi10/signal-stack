
from services.company_service import CompanyService
from services.source_service import SourceService
from services.source_discovery_service import SourceDiscoveryService



company_service = CompanyService()
source_service = SourceService()
discovery_service = SourceDiscoveryService()



COMPETITOR_CANDIDATES = [
    {
        "name": "Leverage Edu",
        "url": "https://leverageedu.com"
    },
    {
        "name": "Yocket",
        "url": "https://yocket.com"
    },
    {
        "name": "IDP Education",
        "url": "https://www.idp.com/india/"
    },
    {
        "name": "Edwise International",
        "url": "https://www.edwiseinternational.com"
    },
    {
        "name": "SI-UK",
        "url": "https://www.studyin-uk.com"
    },
    {
        "name": "TC Global",
        "url": "https://tcglobal.com"
    },
    {
        "name": "AECC Global",
        "url": "https://www.aeccglobal.com"
    }
]


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


saved_count = 0
skipped_count = 0

print("\nCOMPETITOR DISCOVERY RESULTS\n")

for competitor in COMPETITOR_CANDIDATES:

    name = competitor["name"]
    url = competitor["url"]

    print("\nChecking:", name)

    validation = discovery_service.check_source({
        "name": name,
        "url": url
    })

    if validation["status"] != "accessible":
        print(
            "Not saved:",
            name,
            "| Status:",
            validation["status"]
        )
        skipped_count += 1
        continue

    page_title = validation.get("title", "")

    reason = (
        "Potential competitor in the overseas education "
        "consulting market. Website was accessible during "
        "discovery. This is a candidate for human review; "
        "competitive relevance has not yet been independently "
        "verified. Page title: "
        f"{page_title}. Pending human approval."
    )

    source_id = source_service.add_source(
        company_id=company_id,
        name=name,
        url=url,
        category="Competitors",
        reason=reason
    )

    if source_id is None:
        print("Already exists:", name)
        skipped_count += 1

    else:
        print(
            "Saved:",
            name,
            "| ID:",
            source_id,
            "| Category: Competitors"
        )
        saved_count += 1



print("\nCOMPETITOR DISCOVERY SUMMARY")
print("----------------------------")
print("Total candidates:", len(COMPETITOR_CANDIDATES))
print("New competitors saved:", saved_count)
print("Skipped:", skipped_count)



print("\nCOMPETITOR SOURCES IN DATABASE\n")

all_sources = source_service.get_sources(company_id)

competitor_sources = [
    source for source in all_sources
    if source["category"] == "Competitors"
]

for source in competitor_sources:
    print(
        source["id"],
        "|",
        source["name"],
        "|",
        source["url"],
        "| Approved:",
        source["approved"]
    )

print("\nTotal competitor sources:", len(competitor_sources))
