from base.views.generic.detail import BaseDetailView
from documents.models.evidence import Evidence


class EvidenceDetailView(BaseDetailView):
    model = Evidence
    template_name = "documents/evidence/detail.html"
    permission_required = "documents.view_evidence"
