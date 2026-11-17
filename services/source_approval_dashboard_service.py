
from services.source_service import SourceService
from services.source_approval_workflow_service import (
    SourceApprovalWorkflowService
)


class SourceApprovalDashboardService:

    def __init__(self):
        self.source_service = SourceService()
        self.workflow_service = SourceApprovalWorkflowService()

    def get_dashboard_data(self, company_id):

        all_sources = self.source_service.get_sources(company_id)

        pending_sources = (
            self.workflow_service
            .get_pending_sources_with_recommendations(company_id)
        )

        approved_sources = [
            dict(source)
            for source in all_sources
            if source["approved"] == 1
        ]

        pending_count = len(pending_sources)
        approved_count = len(approved_sources)

        return {
            "company_id": company_id,
            "total_sources": len(all_sources),
            "approved_count": approved_count,
            "pending_count": pending_count,
            "approved_sources": approved_sources,
            "pending_sources": pending_sources
        }
