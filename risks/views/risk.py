from base.views.generic import BaseCreateView
from base.views.generic import BaseDeleteView
from base.views.generic import BaseDetailView
from base.views.generic import BaseListView
from base.views.generic import BaseUpdateView

from ..forms import RiskForm
from ..models.risk import Risk


class RiskListView(BaseListView):
    model = Risk
    template_name = "risks/risk/list.html"
    permission_required = "risks.view_risk"


class RiskCreateView(BaseCreateView):
    model = Risk
    form_class = RiskForm
    template_name = "risks/risk/create.html"
    permission_required = "risks.add_risk"


class RiskDetailView(BaseDetailView):
    model = Risk
    template_name = "risks/risk/detail.html"
    permission_required = "risks.view_risk"


class RiskUpdateView(BaseUpdateView):
    model = Risk
    form_class = RiskForm
    template_name = "risks/risk/update.html"
    permission_required = "risks.change_risk"


class RiskDeleteView(BaseDeleteView):
    model = Risk
    permission_required = "risks.delete_risk"
    template_name = "risks/risk/delete.html"
