from django.contrib import admin
from django.contrib.admin.models import ADDITION
from django.contrib.admin.models import CHANGE
from django.contrib.admin.models import DELETION
from django.contrib.admin.models import LogEntry
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect
from django.urls import NoReverseMatch
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache

from users.models import User

action_names = {
    ADDITION: "Addition",
    CHANGE: "Change",
    DELETION: "Deletion",
}


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


class FilterBase(admin.SimpleListFilter):
    def queryset(self, request, queryset):
        if self.value():
            dictionary = {
                self.parameter_name: self.value(),
            }
            return queryset.filter(**dictionary)
        return None


class UserFilter(FilterBase):
    """Use this filter to only show current users, who appear in the log."""

    title = "user"
    parameter_name = "user_id"

    def lookups(self, request, model_admin):
        return tuple(
            (u.id, u.__str__)
            for u in User.objects.filter(
                pk__in=LogEntry.objects.values_list("user_id").distinct(),
            )
        )


class ActionFilter(FilterBase):
    title = "action"
    parameter_name = "action_flag"

    def lookups(self, request, model_admin):
        return action_names.items()


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """
    Class added to show logEntries objects in the admin view.
    """

    date_hierarchy = "action_time"
    list_filter = [
        UserFilter,
        ActionFilter,
        "content_type",
    ]

    search_fields = ["object_repr", "change_message", "object_id"]

    list_display = [
        "action_time",
        "user",
        "object_link",
        "__str__",
        "content_type",
        "object_id",
    ]

    # keep only view permission
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(ordering="object_repr", description=_("object"))
    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = obj.object_repr
        else:
            ct = obj.content_type
            try:
                history_link = reverse(
                    f"admin:{ct.app_label}_{ct.model}_history",
                    args=[obj.object_id],
                )
                history_repr = escape(obj.object_repr)
                link = mark_safe(  # noqa: S308
                    f'<a href="{history_link}">{history_repr}</a>',
                )
            except NoReverseMatch:
                link = obj.object_repr
        return link

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("content_type")
