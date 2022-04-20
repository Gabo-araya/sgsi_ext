# django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


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
