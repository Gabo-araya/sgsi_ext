from django import forms  # noqa: F401

from base.forms import BaseModelForm
from documents.models.control import Control
from documents.models.control_category import ControlCategory
from documents.models.document import Document
from documents.models.document_version import DocumentVersion


class DocumentForm(BaseModelForm):
    class Meta:
        model = Document
        fields = ("title", "description")


class DocumentVersionForm(BaseModelForm):
    class Meta:
        model = DocumentVersion
        fields = ("file",)


class ControlForm(BaseModelForm):
    class Meta:
        model = Control
        fields = ("category", "title", "description", "document")


class ControlCategoryForm(BaseModelForm):
    class Meta:
        model = ControlCategory
        fields = ("name",)
