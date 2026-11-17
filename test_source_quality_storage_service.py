
from services.source_quality_storage_service import SourceQualityStorageService

service = SourceQualityStorageService()

# Sample source quality evaluation
evaluation = {
    "score": 85,
    "accessibility_score": 25,
    "relevance_score": 20,
    "credibility_score": 25,
    "category_fit_score": 15,
    "quality": "High",
    "recommendation": "Recommended for Review",
    "reasons": [
        "Website is accessible",
        "Government domain indicator found",
        "Human verification is still required"
    ]
}

print("TESTING SOURCE QUALITY STORAGE")

saved = service.save_evaluation(
    source_id=1,
    company_id=1,
    evaluation=evaluation
)

assert saved is True
print("Save evaluation test passed!")

result = service.get_evaluation(source_id=1)

assert result is not None
assert result["score"] == 85
assert result["quality"] == "High"
assert len(result["reasons"]) == 3

print("Retrieve evaluation test passed!")


company_results = service.get_company_evaluations(company_id=1)

assert len(company_results) >= 1
assert any(item["source_id"] == 1 for item in company_results)

print("Company evaluations test passed!")


updated_evaluation = evaluation.copy()
updated_evaluation["score"] = 90

service.save_evaluation(
    source_id=1,
    company_id=1,
    evaluation=updated_evaluation
)

updated_result = service.get_evaluation(source_id=1)

assert updated_result["score"] == 90

print("Update evaluation test passed!")

print("\nAll source quality storage tests passed!")
