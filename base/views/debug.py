# django
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache

from base.serializers import StringFallbackJSONEncoder

from .mixins import SuperuserRestrictedMixin


@method_decorator(never_cache, name="dispatch")
class HttpRequestPrintView(SuperuserRestrictedMixin, View):
    """View that displays the raw request cookies and META."""

    hide_with_404 = True

    def get(self, request, *args, **kwargs):
        params = {"sort_keys": True, "indent": 4}

        request_dict = {
            "COOKIES": get_sorted_request_variable(request.COOKIES),
            "META": get_sorted_request_variable(request.META),
        }
        return JsonResponse(
            request_dict,
            encoder=StringFallbackJSONEncoder,
            safe=False,
            json_dumps_params=params,
        )


def get_sorted_request_variable(variable):
    if isinstance(variable, dict):
        return {k: variable.get(k) for k in sorted(variable)}
    else:
        return {k: variable.getlist(k) for k in sorted(variable)}
