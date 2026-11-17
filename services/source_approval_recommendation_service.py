
from services.source_quality_storage_service import SourceQualityStorageService


class SourceApprovalRecommendationService:

    def __init__(self):
        self.storage_service = SourceQualityStorageService()

    def get_recommendations(self, company_id):

        evaluations = self.storage_service.get_company_evaluations(
            company_id
        )

        recommendations = {
            "recommended_for_review": [],
            "needs_human_review": [],
            "do_not_approve_yet": []
        }

        for evaluation in evaluations:

            recommendation = evaluation["recommendation"]

            source_info = {
                "source_id": evaluation["source_id"],
                "source_name": evaluation["source_name"],
                "url": evaluation["url"],
                "category": evaluation["category"],
                "score": evaluation["score"],
                "quality": evaluation["quality"],
                "recommendation": recommendation
            }

            if recommendation == "Recommended for Review":
                recommendations["recommended_for_review"].append(
                    source_info
                )

            elif recommendation == "Needs Human Review":
                recommendations["needs_human_review"].append(
                    source_info
                )

            elif recommendation == "Do Not Approve Yet":
                recommendations["do_not_approve_yet"].append(
                    source_info
                )

        return recommendations
