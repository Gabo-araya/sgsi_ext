from base.views.generic.detail import BaseDetailView
from base.views.generic.edit import BaseCreateView
from base.views.generic.edit import BaseDeleteView
from base.views.generic.edit import BaseUpdateView
from base.views.generic.list import BaseListView
from processes.forms import ProcessVersionForm
from processes.models.process_version import ProcessVersion


class ProcessVersionListView(BaseListView):
    model = ProcessVersion
    template_name = "processes/processversion/list.html"
    permission_required = "processes.view_processversion"


class ProcessVersionCreateView(BaseCreateView):
    model = ProcessVersion
    form_class = ProcessVersionForm
    template_name = "processes/processversion/create.html"
    permission_required = "processes.add_processversion"


class ProcessVersionDetailView(BaseDetailView):
    model = ProcessVersion
    template_name = "processes/processversion/detail.html"
    permission_required = "processes.view_processversion"


class ProcessVersionUpdateView(BaseUpdateView):
    model = ProcessVersion
    form_class = ProcessVersionForm
    template_name = "processes/processversion/update.html"
    permission_required = "processes.change_processversion"


class ProcessVersionDeleteView(BaseDeleteView):
    model = ProcessVersion
    template_name = "processes/processversion/delete.html"
    permission_required = "processes.delete_processversion"
