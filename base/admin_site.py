from django.contrib import admin
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache


class BaseAdminSite(admin.AdminSite):
    """
    Custom admin site that allows for further customization than the allowed
    by the default site...
    """

    @never_cache
    def login(self, request, extra_context=None):
        """
        Display the login form for the given HttpRequest. Uses reCAPTCHA depending
        on the application config.
        """
        if request.method == "GET" and self.has_permission(request):
            # Already logged-in, redirect to admin index
            index_path = reverse("admin:index", current_app=self.name)
            return HttpResponseRedirect(index_path)

        # Since this module gets imported in the application's root package,
        # it cannot import models from other applications at the module level,
        # and django.contrib.admin.forms eventually imports User.
        from django.contrib.auth.views import LoginView

        context = {
            **self.each_context(request),
            "title": _("Log in"),
            "app_path": request.get_full_path(),
            "username": request.user.get_username(),
        }
        if (
            REDIRECT_FIELD_NAME not in request.GET
            and REDIRECT_FIELD_NAME not in request.POST
        ):
            context[REDIRECT_FIELD_NAME] = reverse("admin:index", current_app=self.name)
        context.update(extra_context or {})

        defaults = {
            "extra_context": context,
            "authentication_form": self._get_login_form_class(),
            "template_name": self.login_template or "admin/login.html",
        }
        request.current_app = self.name
        return LoginView.as_view(**defaults)(request)

    def _get_login_form_class(self):
        from django.contrib.admin.forms import AdminAuthenticationForm

        from parameters.models import Parameter
        from users.forms import AdminCaptchaAuthenticationForm

        parameter = Parameter.value_for("ACTIVATE_LOGIN_RECAPTCHA")
        if parameter:
            return AdminCaptchaAuthenticationForm
        return self.login_form or AdminAuthenticationForm
