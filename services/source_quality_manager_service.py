
from services.research_service import ResearchService
from services.source_quality_service import SourceQualityService
from services.source_quality_storage_service import SourceQualityStorageService


class SourceQualityManagerService:

    def __init__(self):
        self.research_service = ResearchService()
        self.quality_service = SourceQualityService()
        self.storage_service = SourceQualityStorageService()

    def evaluate_and_save(self, source):

        page_data = self.research_service.research_website(
            source["url"]
        )

        evaluation = self.quality_service.evaluate_source(
            source,
            page_data
        )

        if source.get("id") is None:
            raise ValueError("Source must contain an ID.")

        self.storage_service.save_evaluation(
            source_id=source["id"],
            company_id=source["company_id"],
            evaluation=evaluation
        )

        return evaluation

    def get_saved_evaluation(self, source_id):

        return self.storage_service.get_evaluation(source_id)

    def get_company_evaluations(self, company_id):

        return self.storage_service.get_company_evaluations(
            company_id
        )
