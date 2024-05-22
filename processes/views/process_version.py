from typing import Any

from base.views.generic.detail import BaseDetailView
from base.views.generic.edit import BaseDeleteView
from base.views.generic.edit import BaseSubModelCreateView
from base.views.generic.edit import BaseUpdateRedirectView
from base.views.generic.edit import BaseUpdateView
from processes.forms import ProcessVersionForm
from processes.managers import ProcessVersionQuerySet
from processes.models.process import Process
from processes.models.process_version import ProcessVersion


class ProcessVersionCreateView(BaseSubModelCreateView):
    model = ProcessVersion
    parent_model = Process
    form_class = ProcessVersionForm
    template_name = "processes/processversion/create.html"
    permission_required = "processes.add_processversion"

    def get_parent_queryset(self):
        return super().get_parent_queryset().exclude(versions__is_published=False)

    def get_initial(self) -> dict[str, Any]:
        last_version = self.parent_object.last_version
        if last_version is None:
            return super().get_initial()
        initial = {
            "defined_in": last_version.defined_in,
            "controls": last_version.controls.all(),
            "recurrency": last_version.recurrency,
        }
        initial.update(super().get_initial())
        return initial


class ProcessVersionDetailView(BaseDetailView):
    model = ProcessVersion
    template_name = "processes/processversion/detail.html"
    permission_required = "processes.view_processversion"


class ProcessVersionUpdateView(BaseUpdateView):
    model = ProcessVersion
    form_class = ProcessVersionForm
    template_name = "processes/processversion/update.html"
    permission_required = "processes.change_processversion"

    def get_queryset(self) -> ProcessVersionQuerySet:
        return super().get_queryset().not_published()


class ProcessVersionDeleteView(BaseDeleteView):
    model = ProcessVersion
    template_name = "processes/processversion/delete.html"
    permission_required = "processes.delete_processversion"

    def get_queryset(self) -> ProcessVersionQuerySet:
        return super().get_queryset().not_published()

    def get_success_url(self):
        return self.object.process.get_absolute_url()


class ProcessVersionPublishView(BaseUpdateRedirectView):
    model = ProcessVersion
    permission_required = "processes.publish_processversion"

    def do_action(self):
        if not self.object.is_published:
            self.object.publish(self.request.user)
