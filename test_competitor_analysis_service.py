
from services.company_service import CompanyService
from services.competitor_analysis_service import CompetitorAnalysisService


COMPANY_WEBSITE = "https://www.meetuniversity.com"


def find_meetuniversity(company_service):
    companies = company_service.get_all_companies()

    for company in companies:
        if company["website"].rstrip("/") == COMPANY_WEBSITE.rstrip("/"):
            return company

    return None


def print_profile(profile):
    print("\n" + "=" * 65)
    print(f"COMPETITOR: {profile['competitor_name']}")
    print("=" * 65)

    print(f"Website: {profile['website']}")
    print(f"Page title: {profile['page_title']}")
    print(f"Description: {profile['description']}")
    print(f"Headings collected: {profile['headings_count']}")
    print(f"Researched at: {profile['researched_at']}")

    total_matches = 0

    for group_name, findings in profile["findings"].items():
        print(f"\n{group_name.upper()}")
        print("-" * 45)

        if not findings:
            print("No matching phrases found.")
            continue

        for finding in findings:
            total_matches += 1

            print(f"\nMatched phrase: {finding['keyword']}")

            if not finding["evidence"]:
                print("  No supporting evidence text available.")
                continue

            for evidence in finding["evidence"]:
                print(f"  Evidence location: {evidence['location']}")
                print(f"  Evidence text: {evidence['text']}")

    print(f"\nTotal keyword matches: {total_matches}")

    print("\nANALYSIS LIMITATION")
    print(profile["limitation"])

    print(f"\nAnalysis type: {profile['analysis_type']}")


def main():
    print("\nCOMPETITOR INTELLIGENCE ANALYSIS")
    print("=" * 65)

    company_service = CompanyService()
    analysis_service = CompetitorAnalysisService()

    company = find_meetuniversity(company_service)

    if company is None:
        print("MeetUniversity company was not found in the database.")
        return

    print(f"Company: {company['name']}")
    print(f"Company ID: {company['id']}")

    profiles = analysis_service.build_profiles(company["id"])

    if not profiles:
        print("\nNo saved competitor research was found.")
        return

    total_matches = 0

    for profile in profiles:
        print_profile(profile)

        for findings in profile["findings"].values():
            total_matches += len(findings)

    print("\n\nCOMPETITOR ANALYSIS SUMMARY")
    print("=" * 65)

    print(f"Unique researched websites: {len(profiles)}")
    print(f"Total keyword matches: {total_matches}")

    print("\nCompetitors analysed:")

    for index, profile in enumerate(profiles, start=1):
        print(
            f"{index}. {profile['competitor_name']} "
            f"({profile['headings_count']} headings)"
        )

    print("\nIMPORTANT:")
    print(
        "These findings are rule-based observations from collected "
        "website text."
    )
    print(
        "Keyword matches do not independently verify services, "
        "market position, or competitive performance."
    )
    print("Original research records remain unchanged.")

    print("\nCompetitor analysis completed successfully!")


if __name__ == "__main__":
    main()
