from base.views.generic import BaseCreateView
from base.views.generic import BaseDeleteView
from base.views.generic import BaseDetailView
from base.views.generic import BaseListView
from base.views.generic import BaseUpdateView
from documents.forms import DocumentTypeForm
from documents.models.document_type import DocumentType


class DocumentTypeListView(BaseListView):
    model = DocumentType
    template_name = "documents/documenttype/list.html"
    permission_required = "documents.view_documenttype"


class DocumentTypeCreateView(BaseCreateView):
    model = DocumentType
    form_class = DocumentTypeForm
    template_name = "documents/documenttype/create.html"
    permission_required = "documents.add_documenttype"


class DocumentTypeDetailView(BaseDetailView):
    model = DocumentType
    template_name = "documents/documenttype/detail.html"
    permission_required = "documents.view_documenttype"


class DocumentTypeUpdateView(BaseUpdateView):
    model = DocumentType
    form_class = DocumentTypeForm
    template_name = "documents/documenttype/update.html"
    permission_required = "documents.change_documenttype"


class DocumentTypeDeleteView(BaseDeleteView):
    model = DocumentType
    permission_required = "documents.delete_documenttype"
    template_name = "documents/documenttype/delete.html"
