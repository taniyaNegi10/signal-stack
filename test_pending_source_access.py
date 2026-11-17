
from database import get_connection
from services.research_service import ResearchService

researcher = ResearchService()

connection = get_connection()

sources = connection.execute(
    """
    SELECT id, name, url
    FROM sources
    WHERE company_id = 1 AND approved = 0
    ORDER BY id
    """
).fetchall()

connection.close()

print("\nPENDING SOURCE ACCESS CHECK")
print("=" * 70)

successful = 0
blocked = 0
failed = 0

for source in sources:
    print(f"\nChecking: {source['name']}")
    print("URL:", source["url"])

    result = researcher.research_website(source["url"])

    status = result.get("status", "unknown")

    print("Status:", status)

    if status == "success":
        successful += 1
        print("Title:", result.get("title", "Not available"))
    elif status == "blocked":
        blocked += 1
        print("Reason:", result.get("error", "Access blocked"))
    else:
        failed += 1
        print("Reason:", result.get("error", "Unknown error"))

print("\n" + "=" * 70)
print("ACCESS SUMMARY")
print("Total checked:", len(sources))
print("Accessible:", successful)
print("Blocked:", blocked)
print("Failed:", failed)
