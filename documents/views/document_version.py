from base.views.generic.detail import BaseDetailView
from base.views.generic.edit import BaseDeleteView
from base.views.generic.edit import BaseSubModelCreateView
from base.views.generic.edit import BaseUpdateView
from documents.forms import DocumentVersionForm
from documents.managers import DocumentVersionQuerySet
from documents.models.document import Document
from documents.models.document_version import DocumentVersion


class DocumentVersionCreateView(BaseSubModelCreateView):
    parent_model = Document
    model = DocumentVersion
    form_class = DocumentVersionForm
    template_name = "documents/documentversion/create.html"
    permission_required = "documents.add_documentversion"


class DocumentVersionDetailView(BaseDetailView):
    model = DocumentVersion
    template_name = "documents/documentversion/detail.html"
    permission_required = "documents.view_documentversion"


class DocumentVersionUpdateView(BaseUpdateView):
    model = DocumentVersion
    form_class = DocumentVersionForm
    template_name = "documents/documentversion/update.html"
    permission_required = "documents.change_documentversion"

    def get_queryset(self) -> DocumentVersionQuerySet:
        return super().get_queryset().not_approved()

    def has_permission(self) -> bool:
        return super().has_permission() and self.get_object().can_be_updated


class DocumentVersionDeleteView(BaseDeleteView):
    model = DocumentVersion
    template_name = "documents/documentversion/delete.html"
    permission_required = "documents.delete_documentversion"

    def get_queryset(self) -> DocumentVersionQuerySet:
        return super().get_queryset().not_approved()
