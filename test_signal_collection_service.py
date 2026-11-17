
from services.signal_collection_service import SignalCollectionService


def main():
    print("\nSIGNAL COLLECTION")
    print("=" * 65)

    service = SignalCollectionService()

    result = service.collect_signals(company_id=1)

    print("\nCOLLECTION SUMMARY")
    print("-" * 65)

    print("Sources checked:", result["sources_checked"])
    print("Signals saved:", result["signals_saved"])
    print("Duplicates skipped:", result["duplicates_skipped"])
    print("Failed sources:", len(result["failed_sources"]))

    for signal in result["signals"]:
        print("\nTitle:", signal["title"])
        print("Category:", signal["category"])
        print("Source:", signal["source_url"])

    if result["failed_sources"]:
        print("\nFAILED SOURCES")
        for source in result["failed_sources"]:
            print(source["source"], ":", source["reason"])

    print("\nSignal collection test completed!")


if __name__ == "__main__":
    main()
