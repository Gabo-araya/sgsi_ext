from typing import Any

from base.views.generic import BaseCreateView
from base.views.generic import BaseDeleteView
from base.views.generic import BaseDetailView
from base.views.generic import BaseListView
from base.views.generic import BaseUpdateView
from processes.forms import ProcessInstanceForm
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
        process_pk = self.kwargs.get("process_pk")
        if process_pk is not None:
            initial["process"] = Process.objects.get(pk=process_pk)
        return initial


class ProcessInstanceDetailView(BaseDetailView):
    model = ProcessInstance
    template_name = "processes/processinstance/detail.html"
    permission_required = "processes.view_processinstance"


class ProcessInstanceUpdateView(BaseUpdateView):
    model = ProcessInstance
    form_class = ProcessInstanceForm
    template_name = "processes/processinstance/update.html"
    permission_required = "processes.change_processinstance"


class ProcessInstanceDeleteView(BaseDeleteView):
    model = ProcessInstance
    permission_required = "processes.delete_processinstance"
    template_name = "processes/processinstance/delete.html"
