# standard library
import contextlib

# django
from django.views.generic import ListView

from base.view_utils import clean_query_string

from ..mixins import LoginPermissionRequiredMixin


class BaseListView(LoginPermissionRequiredMixin, ListView):
    login_required = True
    permission_required = ()
    paginate_by = 25
    page_kwarg = "p"
    ignore_kwargs_on_filter = ("q", page_kwarg, "o")
    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["opts"] = self.model._meta
        context["clean_query_string"] = clean_query_string(self.request)
        context["q"] = self.request.GET.get("q")
        context["title"] = self.get_title()
        context["ordering"] = self.request.GET.getlist("o")
        return context

    def get_title(self):
        if self.title is not None:
            return self.title
        return self.model._meta.verbose_name_plural.title()

    def get_ordering(self):
        """
        Return the field or fields to use for ordering the queryset.
        """
        order = self.request.GET.getlist("o")
        if order:
            return order

        return self.ordering

    def get_queryset(self):
        """
        return the queryset to use on the list and filter by what comes on the
        query string
        """
        queryset = super().get_queryset()

        # obtain non ignored kwargs for the filter method
        items = self.request.GET.items()
        params = {k: v for k, v in items if k not in self.ignore_kwargs_on_filter}

        # filter
        for key, value in params.items():
            with contextlib.suppress(Exception):
                queryset = queryset.filter(**{key: value})

        return queryset
