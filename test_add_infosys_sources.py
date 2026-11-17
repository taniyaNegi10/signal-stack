from services.source_service import SourceService

service = SourceService()

company_id = 4

sources = [
    {
        "name": "Infosys Official Website",
        "url": "https://www.infosys.com/",
        "category": "Internal Intelligence",
        "reason": "Official company website for understanding Infosys."
    },
    {
        "name": "Infosys Newsroom",
        "url": "https://www.infosys.com/newsroom/",
        "category": "Market",
        "reason": "Official company announcements and news."
    },
    {
        "name": "Infosys Press Releases",
        "url": "https://www.infosys.com/newsroom/press-releases.html",
        "category": "Market",
        "reason": "Official press releases and business updates."
    },
    {
        "name": "Infosys Investor Relations",
        "url": "https://www.infosys.com/Investors/",
        "category": "Internal Intelligence",
        "reason": "Official investor information and financial updates."
    },
    {
        "name": "Infosys Annual Reports",
        "url": "https://www.infosys.com/investors/reports-filings/annual-report/annual-reports.html",
        "category": "Internal Intelligence",
        "reason": "Official annual reports and company performance information."
    }
]

print("ADDING INFOSYS SOURCES")
print("=" * 60)

for source in sources:
    result = service.add_source(
        company_id=company_id,
        name=source["name"],
        url=source["url"],
        category=source["category"],
        reason=source["reason"]
    )

    print(source["name"], "|", "Added" if result else "Already exists or could not be added")

print("\nInfosys source setup completed.")