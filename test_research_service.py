
from services.research_service import ResearchService

researcher = ResearchService()

result = researcher.research_website(
    "https://www.meetuniversity.com"
)

print("Research Result:")
print("Status:", result["status"])

if result["status"] == "success":
    print("Title:", result["title"])
    print("Description:", result["description"])

    print("\nWebsite Headings:")

    for heading in result["headings"]:
        print(heading["tag"], ":", heading["text"])

else:
    print("Error:", result["error"])
