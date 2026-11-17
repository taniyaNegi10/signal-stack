
from services.source_quality_storage_service import SourceQualityStorageService


class SourceQualitySummaryService:

    def __init__(self):
        self.storage_service = SourceQualityStorageService()

    def get_summary(self, company_id):

        evaluations = self.storage_service.get_company_evaluations(
            company_id
        )

        total_sources = len(evaluations)

        high_quality = 0
        medium_quality = 0
        low_quality = 0
        human_review = 0
        do_not_approve = 0

        total_score = 0

        for evaluation in evaluations:

            quality = evaluation["quality"]
            recommendation = evaluation["recommendation"]

            total_score += evaluation["score"]

            if quality == "High":
                high_quality += 1

            elif quality == "Medium":
                medium_quality += 1

            elif quality == "Low":
                low_quality += 1

            if recommendation == "Needs Human Review":
                human_review += 1

            elif recommendation == "Do Not Approve Yet":
                do_not_approve += 1

        average_score = (
            round(total_score / total_sources, 2)
            if total_sources > 0
            else 0
        )

        return {
            "company_id": company_id,
            "total_evaluated_sources": total_sources,
            "high_quality_sources": high_quality,
            "medium_quality_sources": medium_quality,
            "low_quality_sources": low_quality,
            "sources_needing_human_review": human_review,
            "sources_not_ready_for_approval": do_not_approve,
            "average_quality_score": average_score
        }
