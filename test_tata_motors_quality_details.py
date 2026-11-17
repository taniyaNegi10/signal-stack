from services.source_quality_storage_service import SourceQualityStorageService

storage = SourceQualityStorageService()

company_id = 3
evaluations = storage.get_company_evaluations(company_id)

print("TATA MOTORS SOURCE QUALITY DETAILS")
print("=" * 60)

for item in evaluations:
    print("\nSource:", item["source_id"])
    print("Score:", item["score"])
    print("Quality:", item["quality"])
    print("Recommendation:", item["recommendation"])
    print("Reasons:", item["reasons"])
    print("-" * 60)