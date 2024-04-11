from django.core.files import File
from django.forms import ModelForm
from django.http import HttpResponse
from django.urls import reverse

from base.views.generic.edit import BaseUpdateView
from documents.models.evidence import Evidence
from processes.forms import ProcessActivityCompleteForm
from processes.models.process_activity import ProcessActivity


class ProcessActivityCompleteView(BaseUpdateView):
    model = ProcessActivity
    form_class = ProcessActivityCompleteForm
    template_name = "processes/processactivity/update.html"
    permission_required = "processes.change_processactivity"

    def get_process_detail_url(self) -> str:
        return reverse("process_detail", args=(self.object.process.pk,))

    def get_success_url(self):
        return self.get_process_detail_url()

    def get_cancel_url(self):
        return self.get_process_detail_url()

    def form_valid(self, form: type[ModelForm]) -> HttpResponse:
        response = super().form_valid(form)
        self.create_evidence(form.cleaned_data["evidence"], self.object)
        self.object.mark_as_completed(self.request.user)
        return response

    def create_evidence(self, evidence_file: File, activity: ProcessActivity) -> None:
        Evidence.objects.create(
            document_version=activity.get_latest_document_version(),
            activity=activity,
            file=evidence_file,
        )
