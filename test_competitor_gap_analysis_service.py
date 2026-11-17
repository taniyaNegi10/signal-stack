
from services.competitor_gap_analysis_service import CompetitorGapAnalysisService


def main():
    print("\nCOMPETITOR GAP ANALYSIS")
    print("=" * 60)

    service = CompetitorGapAnalysisService()

    result = service.analyze_gaps(company_id=1)

    print("\nCOMPETITORS ANALYZED")
    print("-" * 60)
    print(result["competitors_analyzed"])

    print("\nMEETUNIVERSITY RESEARCH FINDINGS")
    print("-" * 60)

    for category, items in result["meetuniversity_findings"].items():
        print(f"\n{category.title()}:")
        print(", ".join(items) if items else "No keyword evidence")

    print("\nPOTENTIAL COMPETITIVE GAPS")
    print("-" * 60)

    for gap in result["potential_gaps"]:
        print("\nCategory:", gap["category"])
        print("Area:", gap["area"])
        print("Competitors:", ", ".join(gap["competitors_with_evidence"]))
        print("Observation:", gap["observation"])
        print("Suggested action:", gap["suggested_action"])
        print("Confidence:", gap["confidence"])

    print("\nLIMITATIONS")
    for limitation in result["limitations"]:
        print("-", limitation)

    print("\nCompetitor gap analysis completed successfully!")


if __name__ == "__main__":
    main()
