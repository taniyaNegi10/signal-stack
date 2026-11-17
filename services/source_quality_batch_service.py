
from services.source_quality_manager_service import SourceQualityManagerService
from services.source_service import SourceService


class SourceQualityBatchService:

    def __init__(self):
        self.manager = SourceQualityManagerService()
        self.source_service = SourceService()

    def evaluate_all_sources(self, company_id):

        sources = self.source_service.get_sources(company_id)

        results = {
            "company_id": company_id,
            "total_sources": len(sources),
            "successful": 0,
            "failed": 0,
            "evaluations": [],
            "errors": []
        }

        for source in sources:

            source = dict(source)

            try:
                evaluation = self.manager.evaluate_and_save(source)

                results["successful"] += 1

                results["evaluations"].append({
                    "source_id": source["id"],
                    "source_name": source["name"],
                    "score": evaluation["score"],
                    "quality": evaluation["quality"],
                    "recommendation": evaluation["recommendation"]
                })

            except Exception as error:

                results["failed"] += 1

                results["errors"].append({
                    "source_id": source.get("id"),
                    "source_name": source.get("name"),
                    "error": str(error)
                })

        return results
