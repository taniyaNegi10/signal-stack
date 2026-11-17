from services.competitor_comparison_service import CompetitorComparisonService


def main():
    print("\nCOMPETITOR COMPARISON & OPPORTUNITY ANALYSIS")
    print("=" * 60)

    service = CompetitorComparisonService()

    company_id = 1  # MeetUniversity
    result = service.compare_competitors(company_id)

    print("\nCOMPETITORS COMPARED")
    print("-" * 60)
    print("Total:", result["competitors_compared"])

    for item in result["comparison"]:
        print(f"\nCompetitor: {item['competitor']}")
        print("Website:", item["website"])
        print("Services:", ", ".join(item["services"]) or "No keyword evidence")
        print("Destinations:", ", ".join(item["destinations"]) or "No keyword evidence")
        print("Other offerings:", ", ".join(item["other_offerings"]) or "No keyword evidence")
        print("Evidence count:", item["evidence_count"])

    print("\nOPPORTUNITIES TO INVESTIGATE")
    print("-" * 60)

    for opportunity in result["opportunities"]:
        print("\nArea:", opportunity["area"])
        print("Observation:", opportunity["observation"])
        print("Competitors:", ", ".join(opportunity["evidence"]))
        print("Suggested action:", opportunity["suggested_action"])
        print("Confidence:", opportunity["confidence"])

    print("\nLIMITATIONS")
    for limitation in result["limitations"]:
        print("-", limitation)

    print("\nCompetitor comparison completed successfully!")


if __name__ == "__main__":
    main()