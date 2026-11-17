from services.source_quality_batch_service import SourceQualityBatchService

service = SourceQualityBatchService()
company_id = 4

print("INFOSYS SOURCE QUALITY EVALUATION")
print("=" * 60)

results = service.evaluate_all_sources(company_id)

print("\nSUMMARY")
print("-" * 60)
print("Total sources:", results["total_sources"])
print("Successful:", results["successful"])
print("Failed:", results["failed"])

print("\nEVALUATIONS")
print("-" * 60)

for item in results["evaluations"]:
    print(
        item["source_name"],
        "| Score:", item["score"],
        "| Quality:", item["quality"],
        "| Recommendation:", item["recommendation"]
    )

if results["errors"]:
    print("\nERRORS")
    for error in results["errors"]:
        print(error)

print("\nEvaluation completed.")