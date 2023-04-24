# django
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.http import HttpResponseForbidden


class LoginPermissionRequiredMixin(PermissionRequiredMixin):
    """
    Verify that the current user is authenticated (if required)
    and has the required permission (if authenticated)
    """

    login_required = None

    def is_login_required(self) -> bool:
        if self.login_required is None or not isinstance(self.login_required, bool):
            msg = (
                "{0} is missing or has misconfigured the login_required attribute. "
                "Define {0}.login_required correctly, or override "
                "{0}.is_login_required().".format(self.__class__.__name__)
            )
            raise ImproperlyConfigured(msg)
        return self.login_required

    def dispatch(self, request, *args, **kwargs):
        if self.is_login_required() and not request.user.is_authenticated:
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
