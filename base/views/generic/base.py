# django
from django.views.generic import RedirectView
from django.views.generic import TemplateView

from ..mixins import LoginPermissionRequiredMixin


class BaseTemplateView(LoginPermissionRequiredMixin, TemplateView):
    login_required = True
    permission_required = ()

    def get_context_data(self, **kwargs):
        context = super(BaseTemplateView, self).get_context_data(**kwargs)

        context["title"] = self.title

        return context


class BaseRedirectView(LoginPermissionRequiredMixin, RedirectView):
    login_required = True
    permission_required = ()
