
from services.company_service import CompanyService
from services.source_service import SourceService
from services.source_discovery_service import SourceDiscoveryService
from services.source_classification_service import SourceClassificationService


company_service = CompanyService()
source_service = SourceService()
discovery_service = SourceDiscoveryService()
classification_service = SourceClassificationService()


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



result = discovery_service.discover_website_links(
    "https://www.meetuniversity.com"
)

if result["status"] != "success":
    raise RuntimeError("Website discovery failed.")



saved_count = 0
skipped_count = 0

print("\nCLASSIFYING AND SAVING DISCOVERED PAGES\n")

for link in result["links"]:

    name = link["anchor_text"] or "Unnamed page"
    url = link["url"].strip()

    validation = discovery_service.check_source({
        "name": name,
        "url": url
    })

    if validation["status"] != "accessible":
        print("Skipped:", name, "|", validation["status"])
        skipped_count += 1
        continue

    classification = classification_service.classify_source(
        name=name,
        title=validation.get("title", ""),
        description=""
    )

    category = classification["category"]

   
    if category == "Needs Review":

        if name in ["Unnamed page", "Ivy", "Blog"]:
            category = "Internal Intelligence"
            classification_reason = (
                "Recognised as a potential first-party "
                "MeetUniversity webpage. Suggested category "
                "requires human review."
            )

        else:
            print("Needs manual review:", name)
            skipped_count += 1
            continue

    else:
        classification_reason = classification["reason"]

    reason = (
        "Automatically suggested category: "
        f"{category}. "
        f"{classification_reason} "
        "Pending human review. First-party webpage."
    )

    source_id = source_service.add_source(
        company_id=company_id,
        name=name,
        url=url,
        category=category,
        reason=reason
    )

    if source_id is None:
        print("Already exists:", name)
        skipped_count += 1

    else:
        print(
            "Saved:", name,
            "| Category:", category,
            "| ID:", source_id
        )
        saved_count += 1



print("\nSUMMARY")
print("New pages saved:", saved_count)
print("Skipped pages:", skipped_count)


print("\nPENDING SOURCES\n")

for source in source_service.get_pending_sources(company_id):
    print(
        source["id"],
        "|", source["name"],
        "|", source["category"],
        "| Approved:", source["approved"]
    )
