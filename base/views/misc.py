# django
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.defaults import bad_request
from django.views.defaults import page_not_found
from django.views.defaults import permission_denied
from django.views.defaults import server_error

from base.views.generic import BaseTemplateView


def index(request):
    """view that renders a default home"""
    return render(request, "index.pug")


def bad_request_view(request, exception, template=None):
    return bad_request(request, exception, "exceptions/400.pug")


def permission_denied_view(request, exception, template=None):
    return permission_denied(request, exception, "exceptions/403.pug")


def page_not_found_view(request, exception, template=None):
    return page_not_found(request, exception, "exceptions/404.pug")


def server_error_view(request, template=None):
    return server_error(request, "exceptions/500.pug")


@method_decorator(staff_member_required, name="dispatch")
class StatusView(BaseTemplateView):
    template_name = "status.pug"
    title = _("status").title()

    def get_context_data(self, **kwargs):
        context = super(StatusView, self).get_context_data(**kwargs)

        context["settings"] = settings

        return context
