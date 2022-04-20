# django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404
from django.http import HttpResponseForbidden


class LoginPermissionRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
    """
    Verify that the current user is authenticated (if required)
    and has the required permission (if authenticated)
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not self.has_permission():
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class SuperuserRestrictedMixin:
    """Restricts a view to superusers only. Optionally hide it with 404."""

    hide_with_404 = False

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not (user.is_authenticated and user.is_superuser):
            if self.hide_with_404:
                raise Http404
            else:
                raise HttpResponseForbidden
        return super().dispatch(request, *args, **kwargs)
