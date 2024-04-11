from base.views.generic.detail import BaseDetailView
from base.views.generic.edit import BaseDeleteView
from base.views.generic.edit import BaseSubModelCreateView
from base.views.generic.edit import BaseUpdateView
from base.views.generic.list import BaseListView
from processes.forms import ProcessActivityDefinitionForm
from processes.models.process_activity_definition import ProcessActivityDefinition
from processes.models.process_definition import ProcessDefinition


class ProcessActivityDefinitionListView(BaseListView):
    model = ProcessActivityDefinition
    template_name = "processes/processactivitydefinition/list.html"
    permission_required = "processes.view_processactivitydefinition"


class ProcessActivityDefinitionCreateView(BaseSubModelCreateView):
    model = ProcessActivityDefinition
    parent_model = ProcessDefinition
    form_class = ProcessActivityDefinitionForm
    template_name = "processes/processactivitydefinition/create.html"
    permission_required = "processes.add_processactivitydefinition"


class ProcessActivityDefinitionDetailView(BaseDetailView):
    model = ProcessActivityDefinition
    template_name = "processes/processactivitydefinition/detail.html"
    permission_required = "processes.view_processactivitydefinition"


class ProcessActivityDefinitionUpdateView(BaseUpdateView):
    model = ProcessActivityDefinition
    form_class = ProcessActivityDefinitionForm
    template_name = "processes/processactivitydefinition/update.html"
    permission_required = "processes.change_processactivitydefinition"


class ProcessActivityDefinitionDeleteView(BaseDeleteView):
    model = ProcessActivityDefinition
    template_name = "processes/processactivitydefinition/delete.html"
    permission_required = "processes.delete_processactivitydefinition"
