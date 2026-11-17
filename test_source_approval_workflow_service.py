
from services.source_approval_workflow_service import (
    SourceApprovalWorkflowService
)

service = SourceApprovalWorkflowService()

print("TESTING SOURCE APPROVAL WORKFLOW SERVICE")


results = service.get_pending_sources_with_recommendations(
    company_id=1
)

print("\nPENDING SOURCES WITH RECOMMENDATIONS")

for source in results:

    recommendation = source["recommendation"]

    if recommendation:
        decision = recommendation["recommendation"]
        score = recommendation["score"]
    else:
        decision = "Not evaluated"
        score = "N/A"

    print(
        source["name"],
        "| Score:", score,
        "| Recommendation:", decision
    )

print("\nTOTAL PENDING SOURCES:", len(results))


assert len(results) == 14, (
    f"Expected 14 pending sources, got {len(results)}"
)


assert all(
    source["recommendation"] is not None
    for source in results
), "Some pending sources are missing recommendations"


assert all(
    source["name"] and source["url"]
    for source in results
), "A source is missing its name or URL"

print("\nAll approval workflow tests passed!")
