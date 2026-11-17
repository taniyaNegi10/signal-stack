
from services.source_service import SourceService

service = SourceService()

company_id = 3

sources = [
    {
        "name": "Tata Motors Official Website",
        "url": "https://www.tatamotors.com",
        "category": "Internal Intelligence",
        "reason": "Official company information and business overview."
    },
    {
        "name": "Tata Motors Newsroom",
        "url": "https://www.tatamotors.com/newsroom/",
        "category": "Internal Intelligence",
        "reason": "Official company announcements and press releases."
    },
    {
        "name": "Tata Motors Investor Relations",
        "url": "https://cv.tatamotors.com/investors",
        "category": "Internal Intelligence",
        "reason": "Financial results, investor presentations and disclosures."
    },
    {
        "name": "Tata Motors Annual Reports",
        "url": "https://www.tatamotors.com/annual-reports/",
        "category": "Internal Intelligence",
        "reason": "Annual reports and company performance disclosures."
    },
    {
        "name": "Tata Motors Sustainability",
        "url": "https://www.tatamotors.com/corporate-responsibility/sustainability-strategy/",
        "category": "Market",
        "reason": "Public sustainability strategy and automotive industry priorities."
    }
]

print("ADDING TATA MOTORS SOURCES")
print("=" * 55)

for source in sources:
    result = service.add_source(
        company_id=company_id,
        name=source["name"],
        url=source["url"],
        category=source["category"],
        reason=source["reason"]
    )
    print(source["name"], "->", result)

print("\nTATA MOTORS SOURCE SUMMARY")
print("=" * 55)

for source in service.get_sources(company_id):
    print(source["name"], "|", source["category"], "| Approved:", source["approved"])
