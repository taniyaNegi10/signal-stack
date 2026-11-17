
from services.report_generation_service import ReportGenerationService

service = ReportGenerationService()
company_id = 3

print("TATA MOTORS MONDAY MORNING BRIEF")
print("=" * 70)

result = service.generate_report(company_id)

print("\nReport ID:", result["report_id"])
print("Title:", result["title"])

print("\nREPORT SECTIONS")
print("-" * 70)

sections = result["sections"]

if isinstance(sections, dict):
    for title, content in sections.items():
        print(f"\n{title}")
        print("-" * 50)
        print(content)
else:
    for section in sections:
        print("\n", section)
        print("-" * 50)

print("\nLIMITATIONS")
print("-" * 70)
print(result["limitations"])

print("\nReport generation completed.")
