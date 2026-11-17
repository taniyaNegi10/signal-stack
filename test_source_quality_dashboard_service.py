
from services.source_quality_dashboard_service import SourceQualityDashboardService

service = SourceQualityDashboardService()

print("TESTING SOURCE QUALITY DASHBOARD")

dashboard = service.get_dashboard_data(company_id=1)

summary = dashboard["summary"]

print("\nDASHBOARD SUMMARY")
for key, value in summary.items():
    print(f"{key}: {value}")

print("\nSOURCE COUNTS")
print("All evaluations:", len(dashboard["all_evaluations"]))
print("High quality:", len(dashboard["high_quality_sources"]))
print("Medium quality:", len(dashboard["medium_quality_sources"]))
print("Low quality:", len(dashboard["low_quality_sources"]))


assert summary["total_evaluated_sources"] == 15

assert len(dashboard["all_evaluations"]) == 15

assert (
    len(dashboard["high_quality_sources"])
    + len(dashboard["medium_quality_sources"])
    + len(dashboard["low_quality_sources"])
    == 15
)

print("\nAll dashboard tests passed!")
