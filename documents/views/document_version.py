from django.forms import BaseModelForm
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _

from base.views.generic.detail import BaseDetailView
from base.views.generic.edit import BaseDeleteView
from base.views.generic.edit import BaseSubModelCreateView
from base.views.generic.edit import BaseUpdateRedirectView
from base.views.generic.edit import BaseUpdateView
from documents.forms import DocumentVersionApproveForm
from documents.forms import DocumentVersionForm
from documents.managers import DocumentVersionQuerySet
from documents.models.document import Document
from documents.models.document_version import DocumentVersion


class DocumentVersionGetObjectMixin:
    def get_object(
        self, queryset: DocumentVersionQuerySet | None = None
    ) -> DocumentVersion:
        if queryset is None:
            queryset = self.get_queryset()

        document_code = self.kwargs.get("document_code")
        version = self.kwargs.get("version")

        queryset = queryset.filter(document__code=document_code, version=version)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except DocumentVersion.DoesNotExist as exc:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            ) from exc
        return obj


class DocumentVersionCreateView(BaseSubModelCreateView):
    parent_model = Document
    model = DocumentVersion
    form_class = DocumentVersionForm
    template_name = "documents/documentversion/create.html"
    permission_required = "documents.add_documentversion"
    parent_slug_field = "code"

    def get_parent_queryset(self):
        return super().get_parent_queryset().exclude(versions__is_approved=False)


class DocumentVersionDetailView(DocumentVersionGetObjectMixin, BaseDetailView):
    model = DocumentVersion
    template_name = "documents/documentversion/detail.html"
    permission_required = "documents.view_documentversion"

    def get_context_data(self, **kwargs):
        show_mark_as_read = (
            self.object.is_approved
            and not self.object.is_read_by_user(self.request.user)
            and self.object.verification_code
            == self.request.GET.get("verification_code")
        )
        return {
            **super().get_context_data(**kwargs),
            "show_mark_as_read": show_mark_as_read,
        }


class DocumentVersionUpdateView(DocumentVersionGetObjectMixin, BaseUpdateView):
    model = DocumentVersion
    form_class = DocumentVersionForm
    template_name = "documents/documentversion/update.html"
    permission_required = "documents.change_documentversion"

    def get_queryset(self) -> DocumentVersionQuerySet:
        return super().get_queryset().not_approved()


class DocumentVersionDeleteView(DocumentVersionGetObjectMixin, BaseDeleteView):
    model = DocumentVersion
    template_name = "documents/documentversion/delete.html"
    permission_required = "documents.delete_documentversion"

    def get_queryset(self) -> DocumentVersionQuerySet:
        return super().get_queryset().not_approved()

    def get_success_url(self):
        return self.object.document.get_absolute_url()


class DocumentVersionApproveView(DocumentVersionGetObjectMixin, BaseUpdateView):
    model = DocumentVersion
    form_class = DocumentVersionApproveForm
    template_name = "documents/documentversion/update.html"
    permission_required = "documents.approve_documentversion"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object.mark_as_approved(self.request.user, form)
        return HttpResponseRedirect(self.get_success_url())

    def get_title(self):
        return _("Approve document version")

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "submit_button_text": _("Approve"),
        }


class DocumentVersionMarkAsReadView(
    DocumentVersionGetObjectMixin, BaseUpdateRedirectView
):
    model = DocumentVersion
    permission_required = "documents.add_documentversionreadbyuser"

    def get_queryset(self) -> DocumentVersionQuerySet:
        return super().get_queryset().approved()

    def do_action(self):
        if self.request.POST.get("verification_code") != self.object.verification_code:
            raise Http404(_("Verification code is not correct"))
        self.object.mark_as_read(self.request.user)
