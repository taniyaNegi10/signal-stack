
from services.source_quality_batch_service import SourceQualityBatchService

service = SourceQualityBatchService()

print("STARTING BATCH SOURCE QUALITY EVALUATION")

results = service.evaluate_all_sources(company_id=1)

print("\nBATCH EVALUATION RESULTS")
print("Total sources:", results["total_sources"])
print("Successful:", results["successful"])
print("Failed:", results["failed"])

print("\nINDIVIDUAL RESULTS")

for item in results["evaluations"]:
    print(
        item["source_name"],
        "| Score:", item["score"],
        "| Quality:", item["quality"]
    )

print("\nERRORS")

for error in results["errors"]:
    print(error)

assert results["successful"] + results["failed"] == results["total_sources"]

print("\nBatch evaluation test passed!")
