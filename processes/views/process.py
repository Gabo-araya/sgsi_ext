from typing import Any

from base.views.generic import BaseCreateView
from base.views.generic import BaseDeleteView
from base.views.generic import BaseDetailView
from base.views.generic import BaseListView
from base.views.generic import BaseUpdateView
from processes.forms import ProcessForm
from processes.models.process import Process
from processes.models.process_definition import ProcessDefinition


class ProcessListView(BaseListView):
    model = Process
    template_name = "processes/process/list.html"
    permission_required = "processes.view_process"


class ProcessCreateView(BaseCreateView):
    model = Process
    form_class = ProcessForm
    template_name = "processes/process/create.html"
    permission_required = "processes.add_process"

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        process_definition_pk = self.kwargs.get("process_definition_pk")
        if process_definition_pk is not None:
            initial["process_definition"] = ProcessDefinition.objects.get(
                pk=process_definition_pk
            )
        return initial


class ProcessDetailView(BaseDetailView):
    model = Process
    template_name = "processes/process/detail.html"
    permission_required = "processes.view_process"


class ProcessUpdateView(BaseUpdateView):
    model = Process
    form_class = ProcessForm
    template_name = "processes/process/update.html"
    permission_required = "processes.change_process"


class ProcessDeleteView(BaseDeleteView):
    model = Process
    permission_required = "processes.delete_process"
    template_name = "processes/process/delete.html"
