from typing import Any

from django.db.models.query import QuerySet
from django.forms import ModelForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

from base.views.generic.detail import BaseDetailView
from base.views.generic.edit import BaseUpdateView
from processes.forms import ProcessActivityInstanceCompleteForm
from processes.models.process_activity_instance import ProcessActivityInstance


class ProcessActivityInstanceDetailView(BaseDetailView):
    model = ProcessActivityInstance
    template_name = "processes/processactivityinstance/detail.html"
    permission_required = "processes.view_processactivityinstance"


class ProcessActivityInstanceCompleteView(BaseUpdateView):
    model = ProcessActivityInstance
    form_class = ProcessActivityInstanceCompleteForm
    template_name = "processes/processactivityinstance/update.html"
    permission_required = "processes.change_processactivityinstance"

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().not_completed().filter(assignee=self.request.user)

    def form_valid(self, form: type[ModelForm]) -> HttpResponse:
        self.object.mark_as_completed(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.get_processinstance_detail_url()

    def get_cancel_url(self):
        return self.get_processinstance_detail_url()

    def get_processinstance_detail_url(self) -> str:
        return reverse(
            "processinstance_detail", args=(self.object.process_instance.pk,)
        )
