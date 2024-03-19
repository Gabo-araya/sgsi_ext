from django import forms  # noqa: F401

from base.forms import BaseModelForm
from documents.models.document import Document


class DocumentForm(BaseModelForm):
    class Meta:
        model = Document
        fields = ()
