from base.views.generic.detail import BaseDetailView
from base.views.generic.edit import BaseDeleteView
from base.views.generic.edit import BaseSubModelCreateView
from base.views.generic.edit import BaseUpdateView
from base.views.generic.list import BaseListView
from processes.forms import ProcessActivityForm
from processes.models.process import Process
from processes.models.process_activity import ProcessActivity


class ProcessActivityListView(BaseListView):
    model = ProcessActivity
    template_name = "processes/processactivity/list.html"
    permission_required = "processes.view_processactivity"


class ProcessActivityCreateView(BaseSubModelCreateView):
    model = ProcessActivity
    parent_model = Process
    form_class = ProcessActivityForm
    template_name = "processes/processactivity/create.html"
    permission_required = "processes.add_processactivity"


class ProcessActivityDetailView(BaseDetailView):
    model = ProcessActivity
    template_name = "processes/processactivity/detail.html"
    permission_required = "processes.view_processactivity"


class ProcessActivityUpdateView(BaseUpdateView):
    model = ProcessActivity
    form_class = ProcessActivityForm
    template_name = "processes/processactivity/update.html"
    permission_required = "processes.change_processactivity"


class ProcessActivityDeleteView(BaseDeleteView):
    model = ProcessActivity
    template_name = "processes/processactivity/delete.html"
    permission_required = "processes.delete_processactivity"
