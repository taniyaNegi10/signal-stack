
from services.source_discovery_service import SourceDiscoveryService

discovery_service = SourceDiscoveryService()

sources = discovery_service.discover_sources()

print("\nSOURCE DISCOVERY RESULTS\n")

for source in sources:
    print("Name:", source["name"])
    print("Category:", source["category"])
    print("URL:", source["url"])
    print("Status:", source["status"])

    if source["status"] == "accessible":
        print("Page title:", source["verified_title"])
    else:
        print("Error:", source.get("error"))

    print("Reason:", source["reason"])
    print("-" * 50)
