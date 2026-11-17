
from services.source_discovery_service import SourceDiscoveryService

discovery_service = SourceDiscoveryService()

# Discover links from MeetUniversity
result = discovery_service.discover_website_links(
    "https://www.meetuniversity.com"
)

print("\nDISCOVERED PAGE VALIDATION\n")

if result["status"] != "success":
    print("Discovery failed:", result.get("error"))
else:

    accessible_count = 0

    for link in result["links"]:

        candidate = {
            "name": link["anchor_text"] or "Unnamed page",
            "url": link["url"],
            "category": "Market",
            "reason": "Discovered from the MeetUniversity website."
        }

        validation = discovery_service.check_source(candidate)

        print("Name:", validation["name"])
        print("URL:", validation["url"])
        print("Status:", validation["status"])

        if validation["status"] == "accessible":
            accessible_count += 1
            print("Title:", validation["verified_title"])
        else:
            print("Issue:", validation.get("error"))

        print("-" * 40)

    print("\nTOTAL DISCOVERED:", result["total_links"])
    print("ACCESSIBLE PAGES:", accessible_count)
