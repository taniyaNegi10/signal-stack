
from services.opportunity_analysis_service import OpportunityAnalysisService


def main():
    print("\nOPPORTUNITY ANALYSIS")
    print("=" * 65)

    service = OpportunityAnalysisService()
    result = service.analyze_opportunities(company_id=1)

    print("\nOPPORTUNITY SUMMARY")
    print("-" * 65)
    print("Total opportunities:", result["opportunities_identified"])

    for opportunity in result["opportunities"]:
        print("\nTitle:", opportunity["title"])
        print("Category:", opportunity["category"])
        print("Priority:", opportunity["priority"])
        print("Supporting competitors:",
              ", ".join(opportunity["supporting_competitors"]))
        print("Evidence count:", opportunity["evidence_count"])
        print("Description:", opportunity["description"])
        print("Potential impact:", opportunity["potential_impact"])
        print("Recommended action:", opportunity["recommended_action"])
        print("Status:", opportunity["status"])
        print("Confidence:", opportunity["confidence"])

    print("\nLIMITATIONS")
    for limitation in result["limitations"]:
        print("-", limitation)

    print("\nOpportunity analysis completed successfully!")


if __name__ == "__main__":
    main()
