from typing import Any

from django import forms
from django.utils.translation import gettext_lazy as _

from base.forms import BaseForm
from base.forms import BaseModelForm
from documents.models.control import Control
from documents.models.control_category import ControlCategory
from documents.models.document import Document
from documents.models.document_version import DocumentVersion


class DocumentForm(BaseModelForm):
    class Meta:
        model = Document
        fields = ("title", "code", "description", "drive_folder", "documented_controls")


class DocumentVersionForm(BaseModelForm):
    class Meta:
        model = DocumentVersion
        fields = ("file", "comment")


class ControlForm(BaseModelForm):
    class Meta:
        model = Control
        fields = ("category", "title", "description")


class ControlCategoryForm(BaseModelForm):
    class Meta:
        model = ControlCategory
        fields = ("name",)


class EvidenceForm(BaseForm):
    evidence_file = forms.FileField(
        label=_("Evidence file"),
        required=False,
        help_text=_("File with the evidence of the activity completion."),
    )
    evidence_url = forms.URLField(
        label=_("Evidence URL"),
        required=False,
        help_text=_("URL to the evidence of the activity completion."),
    )

    class Meta:
        fields = ("evidence_file", "evidence_url")

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        self.evidence_file_xor_url(cleaned_data)
        return cleaned_data

    def evidence_file_xor_url(self, cleaned_data: dict[str, Any]):
        evidence_file = cleaned_data.get("evidence_file")
        evidence_url = cleaned_data.get("evidence_url")
        if bool(evidence_file) ^ bool(evidence_url):
            return
        msg = _("You must provide either a file or a URL as evidence.")
        self.add_error(None, msg)


class DocumentVersionApproveForm(EvidenceForm, BaseModelForm):
    class Meta:
        model = DocumentVersion
        fields = ("evidence_file", "evidence_url")
