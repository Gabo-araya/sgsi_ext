from django.views.generic import DetailView

from ..mixins import LoginPermissionRequiredMixin
from ..mixins import ReactContextMixin


class BaseDetailView(LoginPermissionRequiredMixin, ReactContextMixin, DetailView):
    login_required = True
    permission_required = ()

    def get_title(self):
        verbose_name = self.model._meta.verbose_name
        return f"{verbose_name}: {self.object}".title()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["opts"] = self.model._meta
        context["title"] = self.get_title()
        self.add_react_context(context)

        return context
