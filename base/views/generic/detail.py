# django
from django.views.generic import DetailView

from ..mixins import LoginPermissionRequiredMixin


class BaseDetailView(LoginPermissionRequiredMixin, DetailView):
    login_required = True
    permission_required = ()

    def get_title(self):
        verbose_name = self.model._meta.verbose_name
        return "{}: {}".format(verbose_name, self.object).title()

    def get_context_data(self, **kwargs):
        context = super(BaseDetailView, self).get_context_data(**kwargs)

        context["opts"] = self.model._meta
        context["title"] = self.get_title()

        return context
