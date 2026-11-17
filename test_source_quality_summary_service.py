
from services.source_quality_summary_service import SourceQualitySummaryService

service = SourceQualitySummaryService()

print("TESTING SOURCE QUALITY SUMMARY SERVICE")

summary = service.get_summary(company_id=1)

print("\nSOURCE QUALITY SUMMARY:")
for key, value in summary.items():
    print(f"{key}: {value}")

assert summary["company_id"] == 1
assert summary["total_evaluated_sources"] >= 1
assert summary["average_quality_score"] >= 0
assert summary["high_quality_sources"] >= 0
assert summary["medium_quality_sources"] >= 0
assert summary["low_quality_sources"] >= 0


quality_total = (
    summary["high_quality_sources"]
    + summary["medium_quality_sources"]
    + summary["low_quality_sources"]
)

assert quality_total == summary["total_evaluated_sources"]

print("\nAll summary tests passed!")
