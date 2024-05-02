from typing import Any

from base.views.generic import BaseCreateView
from base.views.generic import BaseDeleteView
from base.views.generic import BaseDetailView
from base.views.generic import BaseListView
from processes.forms import ProcessInstanceForm
from processes.managers import ProcessInstanceQuerySet
from processes.models.process import Process
from processes.models.process_instance import ProcessInstance


class ProcessInstanceListView(BaseListView):
    model = ProcessInstance
    template_name = "processes/processinstance/list.html"
    permission_required = "processes.view_processinstance"


class ProcessInstanceCreateView(BaseCreateView):
    model = ProcessInstance
    form_class = ProcessInstanceForm
    template_name = "processes/processinstance/create.html"
    permission_required = "processes.add_processinstance"

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        process_pk = self.request.GET.get("process_pk")
        process = Process.objects.filter(pk=process_pk).first()
        if process is not None:
            initial["process"] = process
        return initial

    def get_form_kwargs(self) -> dict[str, Any]:
        return {**super().get_form_kwargs(), "user": self.request.user}


class ProcessInstanceDetailView(BaseDetailView):
    model = ProcessInstance
    template_name = "processes/processinstance/detail.html"
    permission_required = "processes.view_processinstance"


class ProcessInstanceDeleteView(BaseDeleteView):
    model = ProcessInstance
    permission_required = "processes.delete_processinstance"
    template_name = "processes/processinstance/delete.html"

    def get_queryset(self) -> ProcessInstanceQuerySet:
        return super().get_queryset().not_completed()
