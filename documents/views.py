from base.views.generic import BaseCreateView
from base.views.generic import BaseDeleteView
from base.views.generic import BaseDetailView
from base.views.generic import BaseListView
from base.views.generic import BaseUpdateView
from documents.forms import DocumentForm
from documents.models import Document


class DocumentListView(BaseListView):
    model = Document
    template_name = "documents/document_list.html"
    permission_required = "documents.view_document"


class DocumentCreateView(BaseCreateView):
    model = Document
    form_class = DocumentForm
    template_name = "documents/document_create.html"
    permission_required = "documents.add_document"


class DocumentDetailView(BaseDetailView):
    model = Document
    template_name = "documents/document_detail.html"
    permission_required = "documents.view_document"


class DocumentUpdateView(BaseUpdateView):
    model = Document
    form_class = DocumentForm
    template_name = "documents/document_update.html"
    permission_required = "documents.change_document"


class DocumentDeleteView(BaseDeleteView):
    model = Document
    permission_required = "documents.delete_document"
    template_name = "documents/document_delete.html"
