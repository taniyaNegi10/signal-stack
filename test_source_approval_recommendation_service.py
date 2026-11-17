
from services.source_approval_recommendation_service import (
    SourceApprovalRecommendationService
)

service = SourceApprovalRecommendationService()

print("TESTING SOURCE APPROVAL RECOMMENDATION SERVICE")

results = service.get_recommendations(company_id=1)

print("\nRECOMMENDATION SUMMARY")

for category, sources in results.items():
    print(f"{category}: {len(sources)}")

print("\nSOURCES RECOMMENDED FOR REVIEW")

for source in results["recommended_for_review"]:
    print(source["source_name"], "| Score:", source["score"])

print("\nSOURCES NEEDING HUMAN REVIEW")

for source in results["needs_human_review"]:
    print(source["source_name"], "| Score:", source["score"])

print("\nSOURCES NOT READY FOR APPROVAL")

for source in results["do_not_approve_yet"]:
    print(source["source_name"], "| Score:", source["score"])


total = sum(len(sources) for sources in results.values())

assert total == 15

print("\nAll approval recommendation tests passed!")
