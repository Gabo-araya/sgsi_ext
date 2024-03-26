from base.views.generic.detail import BaseDetailView
from base.views.generic.edit import BaseCreateView
from base.views.generic.edit import BaseDeleteView
from base.views.generic.edit import BaseUpdateView
from base.views.generic.list import BaseListView
from documents.forms import ControlForm
from documents.models.control import Control


class ControlListView(BaseListView):
    model = Control
    template_name = "documents/control/list.html"
    permission_required = "documents.view_control"


class ControlCreateView(BaseCreateView):
    model = Control
    form_class = ControlForm
    template_name = "documents/control/create.html"
    permission_required = "documents.add_control"


class ControlDetailView(BaseDetailView):
    model = Control
    template_name = "documents/control/detail.html"
    permission_required = "documents.view_control"


class ControlUpdateView(BaseUpdateView):
    model = Control
    form_class = ControlForm
    template_name = "documents/control/update.html"
    permission_required = "documents.change_control"


class ControlDeleteView(BaseDeleteView):
    model = Control
    template_name = "documents/control/delete.html"
    permission_required = "documents.delete_control"
