# django
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import RedirectView
from django.views.generic import TemplateView

from ..mixins import LoginPermissionRequiredMixin


class BaseTemplateView(LoginPermissionRequiredMixin, TemplateView):
    login_required = True
    permission_required = ()
    title = None

    def get_title(self):
        if self.title is not None:
            return self.title

        raise ImproperlyConfigured(
            "self.title cannot be null. Define self.title or override get_title()",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = self.get_title()

        return context


class BaseRedirectView(LoginPermissionRequiredMixin, RedirectView):
    login_required = True
    permission_required = ()
