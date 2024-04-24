from base.views.generic.detail import BaseDetailView
from base.views.generic.edit import BaseCreateView
from base.views.generic.edit import BaseDeleteView
from base.views.generic.edit import BaseUpdateView
from base.views.generic.list import BaseListView
from processes.forms import ProcessForm
from processes.models.process import Process


class ProcessListView(BaseListView):
    model = Process
    template_name = "processes/process/list.html"
    permission_required = "processes.view_process"


class ProcessCreateView(BaseCreateView):
    model = Process
    form_class = ProcessForm
    template_name = "processes/process/create.html"
    permission_required = "processes.add_process"


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
    template_name = "processes/process/confirm_delete.html"
    permission_required = "processes.delete_process"
