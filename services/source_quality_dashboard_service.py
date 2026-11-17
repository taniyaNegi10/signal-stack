
from services.source_quality_summary_service import SourceQualitySummaryService
from services.source_quality_storage_service import SourceQualityStorageService


class SourceQualityDashboardService:

    def __init__(self):
        self.summary_service = SourceQualitySummaryService()
        self.storage_service = SourceQualityStorageService()

    def get_dashboard_data(self, company_id):

     
        summary = self.summary_service.get_summary(company_id)

      
        evaluations = self.storage_service.get_company_evaluations(
            company_id
        )

       
        high_quality = []
        medium_quality = []
        low_quality = []

        for evaluation in evaluations:

            if evaluation["quality"] == "High":
                high_quality.append(evaluation)

            elif evaluation["quality"] == "Medium":
                medium_quality.append(evaluation)

            elif evaluation["quality"] == "Low":
                low_quality.append(evaluation)

     
        return {
            "summary": summary,
            "all_evaluations": evaluations,
            "high_quality_sources": high_quality,
            "medium_quality_sources": medium_quality,
            "low_quality_sources": low_quality
        }
