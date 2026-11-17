
from services.source_approval_dashboard_service import (
    SourceApprovalDashboardService
)

service = SourceApprovalDashboardService()

print("TESTING SOURCE APPROVAL DASHBOARD SERVICE")

dashboard = service.get_dashboard_data(company_id=1)

print("\nDASHBOARD SUMMARY")

print("Total sources:", dashboard["total_sources"])
print("Approved sources:", dashboard["approved_count"])
print("Pending sources:", dashboard["pending_count"])

print("\nAPPROVED SOURCES")

for source in dashboard["approved_sources"]:
    print(source["name"])

print("\nPENDING SOURCES")

for source in dashboard["pending_sources"]:
    recommendation = source["recommendation"]

    print(
        source["name"],
        "| Recommendation:",
        recommendation["recommendation"]
    )


assert dashboard["total_sources"] == 15
assert dashboard["approved_count"] == 1
assert dashboard["pending_count"] == 14


assert (
    dashboard["approved_count"] + dashboard["pending_count"]
    == dashboard["total_sources"]
)

print("\nAll approval dashboard tests passed!")
