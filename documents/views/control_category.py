from base.views.generic.detail import BaseDetailView
from base.views.generic.edit import BaseCreateView
from base.views.generic.edit import BaseDeleteView
from base.views.generic.edit import BaseUpdateView
from base.views.generic.list import BaseListView
from documents.forms import ControlCategoryForm
from documents.models.control_category import ControlCategory


class ControlCategoryListView(BaseListView):
    model = ControlCategory
    template_name = "documents/controlcategory/list.html"
    permission_required = "documents.view_controlcategory"


class ControlCategoryCreateView(BaseCreateView):
    model = ControlCategory
    form_class = ControlCategoryForm
    template_name = "documents/controlcategory/create.html"
    permission_required = "documents.add_controlcategory"


class ControlCategoryDetailView(BaseDetailView):
    model = ControlCategory
    template_name = "documents/controlcategory/detail.html"
    permission_required = "documents.view_controlcategory"


class ControlCategoryUpdateView(BaseUpdateView):
    model = ControlCategory
    form_class = ControlCategoryForm
    template_name = "documents/controlcategory/update.html"
    permission_required = "documents.change_controlcategory"


class ControlCategoryDeleteView(BaseDeleteView):
    model = ControlCategory
    template_name = "documents/controlcategory/delete.html"
    permission_required = "documents.delete_controlcategory"
