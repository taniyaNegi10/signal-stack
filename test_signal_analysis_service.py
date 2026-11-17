
from services.signal_analysis_service import SignalAnalysisService


def main():
    print("\nSIGNAL ANALYSIS")
    print("=" * 65)

    service = SignalAnalysisService()
    result = service.analyze_signals(company_id=1)

    print("\nSIGNAL SUMMARY")
    print("-" * 65)
    print("Total signals analyzed:", result["total_signals_analyzed"])

    for signal in result["signals"]:
        print("\nSignal ID:", signal["signal_id"])
        print("Title:", signal["title"])
        print("Category:", signal["category"])
        print("Why it matters:", signal["why_it_matters"])
        print("Business impact:", signal["business_impact"])
        print("Urgency:", signal["urgency"])
        print("Recommended action:", signal["recommended_action"])
        print("Source:", signal["source_url"])
        print("Human review required:", signal["requires_human_review"])

    print("\nLIMITATIONS")
    for limitation in result["limitations"]:
        print("-", limitation)

    print("\nSignal analysis completed successfully!")


if __name__ == "__main__":
    main()
