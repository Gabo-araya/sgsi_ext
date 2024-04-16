from base.views.generic import BaseCreateView
from base.views.generic import BaseDeleteView
from base.views.generic import BaseDetailView
from base.views.generic import BaseListView
from base.views.generic import BaseUpdateView
from documents.forms import DocumentForm
from documents.models.document import Document


class DocumentListView(BaseListView):
    model = Document
    template_name = "documents/document/list.html"
    permission_required = "documents.view_document"


class DocumentCreateView(BaseCreateView):
    model = Document
    form_class = DocumentForm
    template_name = "documents/document/create.html"
    permission_required = "documents.add_document"


class DocumentDetailView(BaseDetailView):
    model = Document
    template_name = "documents/document/detail.html"
    permission_required = "documents.view_document"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["read_by_user"] = self.object.last_approved_version.was_read_by_user(
            self.request.user
        )
        return context


class DocumentUpdateView(BaseUpdateView):
    model = Document
    form_class = DocumentForm
    template_name = "documents/document/update.html"
    permission_required = "documents.change_document"


class DocumentDeleteView(BaseDeleteView):
    model = Document
    permission_required = "documents.delete_document"
    template_name = "documents/document/delete.html"
