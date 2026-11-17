
from services.source_quality_manager_service import SourceQualityManagerService
from services.source_service import SourceService

manager = SourceQualityManagerService()
source_service = SourceService()

print("TESTING SOURCE QUALITY MANAGER")


sources = source_service.get_sources(company_id=1)

if not sources:
    raise Exception("No sources found for company ID 1")

source = dict(sources[0])

print("\nSource selected:", source["name"])


evaluation = manager.evaluate_and_save(source)

print("\nEVALUATION RESULT:")
print(evaluation)


saved_result = manager.get_saved_evaluation(source["id"])

assert saved_result is not None
assert saved_result["source_id"] == source["id"]
assert saved_result["score"] == evaluation["score"]

print("\nEvaluation and storage test passed!")


company_results = manager.get_company_evaluations(
    company_id=1
)

assert len(company_results) >= 1

print("Company evaluations retrieval test passed!")

print("\nAll manager service tests passed!")
