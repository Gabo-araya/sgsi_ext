from base.views.generic.detail import BaseDetailView
from base.views.generic.edit import BaseDeleteView
from base.views.generic.edit import BaseSubModelCreateView
from base.views.generic.edit import BaseUpdateView
from base.views.generic.list import BaseListView
from processes.forms import ProcessActivityForm
from processes.models.process_activity import ProcessActivity
from processes.models.process_version import ProcessVersion


class ProcessActivityListView(BaseListView):
    model = ProcessActivity
    template_name = "processes/processactivity/list.html"
    permission_required = "processes.view_processactivity"


class ProcessActivityCreateView(BaseSubModelCreateView):
    model = ProcessActivity
    parent_model = ProcessVersion
    form_class = ProcessActivityForm
    template_name = "processes/processactivity/create.html"
    permission_required = "processes.add_processactivity"

    def get_parent_queryset(self):
        return super().get_parent_queryset().filter(is_published=False)


class ProcessActivityDetailView(BaseDetailView):
    model = ProcessActivity
    template_name = "processes/processactivity/detail.html"
    permission_required = "processes.view_processactivity"


class ProcessActivityUpdateView(BaseUpdateView):
    model = ProcessActivity
    form_class = ProcessActivityForm
    template_name = "processes/processactivity/update.html"
    permission_required = "processes.change_processactivity"

    def get_queryset(self):
        return super().get_queryset().filter(process_version__is_published=False)


class ProcessActivityDeleteView(BaseDeleteView):
    model = ProcessActivity
    template_name = "processes/processactivity/delete.html"
    permission_required = "processes.delete_processactivity"

    def get_queryset(self):
        return super().get_queryset().filter(process_version__is_published=False)
