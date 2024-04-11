from base.views.generic.detail import BaseDetailView
from base.views.generic.edit import BaseCreateView
from base.views.generic.edit import BaseDeleteView
from base.views.generic.edit import BaseUpdateView
from base.views.generic.list import BaseListView
from processes.forms import ProcessDefinitionForm
from processes.models.process_definition import ProcessDefinition


class ProcessDefinitionListView(BaseListView):
    model = ProcessDefinition
    template_name = "processes/processdefinition/list.html"
    permission_required = "processes.view_processdefinition"


class ProcessDefinitionCreateView(BaseCreateView):
    model = ProcessDefinition
    form_class = ProcessDefinitionForm
    template_name = "processes/processdefinition/create.html"
    permission_required = "processes.add_processdefinition"


class ProcessDefinitionDetailView(BaseDetailView):
    model = ProcessDefinition
    template_name = "processes/processdefinition/detail.html"
    permission_required = "processes.view_processdefinition"


class ProcessDefinitionUpdateView(BaseUpdateView):
    model = ProcessDefinition
    form_class = ProcessDefinitionForm
    template_name = "processes/processdefinition/update.html"
    permission_required = "processes.change_processdefinition"


class ProcessDefinitionDeleteView(BaseDeleteView):
    model = ProcessDefinition
    template_name = "processes/processdefinition/delete.html"
    permission_required = "processes.delete_processdefinition"
