
from services.source_service import SourceService
from services.source_quality_storage_service import SourceQualityStorageService
from services.source_approval_recommendation_service import (
    SourceApprovalRecommendationService
)


class SourceApprovalWorkflowService:

    def __init__(self):
        self.source_service = SourceService()
        self.quality_storage = SourceQualityStorageService()
        self.recommendation_service = SourceApprovalRecommendationService()

    def get_pending_sources_with_recommendations(self, company_id):

        pending_sources = self.source_service.get_pending_sources(
            company_id
        )

        recommendations = self.recommendation_service.get_recommendations(
            company_id
        )

        recommendation_lookup = {}

        for category_sources in recommendations.values():
            for source in category_sources:
                recommendation_lookup[source["source_id"]] = source

        results = []

        for source in pending_sources:

            source = dict(source)

            quality_data = self.quality_storage.get_evaluation(
                source["id"]
            )

            results.append({
                "source_id": source["id"],
                "name": source["name"],
                "url": source["url"],
                "category": source["category"],
                "reason": source["reason"],
                "quality_evaluation": quality_data,
                "recommendation": recommendation_lookup.get(
                    source["id"],
                    None
                )
            })

        return results

    def approve_source(self, source_id):

        return self.source_service.approve_source(source_id)

    def reject_source(self, source_id):

        return self.source_service.reject_source(source_id)
