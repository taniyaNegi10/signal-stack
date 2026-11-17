
from services.report_generation_service import ReportGenerationService


def main():
    print("\nMONDAY MORNING BRIEF GENERATION")
    print("=" * 75)

    service = ReportGenerationService()

    try:
        result = service.generate_report(company_id=1)

        print("\nREPORT SUMMARY")
        print("-" * 75)
        print("Company:", result["company_name"])
        print("Report ID:", result["report_id"])
        print("Signals used:", result["signals_used"])
        print("Competitors used:", result["competitors_used"])
        print("Opportunities used:", result["opportunities_used"])

        print("\nREPORT SECTIONS")
        print("-" * 75)

        for index, section in enumerate(result["sections"], start=1):
            print(f"{index}. {section}")

        print("\nLIMITATIONS")
        for limitation in result["limitations"]:
            print("-", limitation)

        print("\nREPORT GENERATION COMPLETED!")

    except Exception as error:
        print("\nREPORT GENERATION FAILED:")
        print(error)


if __name__ == "__main__":
    main()
