""" Admin page configuration for the users app """
import logging

from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.sessions.models import Session
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

# forms
from users.forms import UserChangeForm
from users.forms import UserCreationForm
from users.models.user import User

logger = logging.getLogger(__name__)


@admin.action(permissions=("logout",), description=_("Log out from all devices"))
def force_logout(modeladmin, request, queryset):
    user_id = request.user.pk
    requested_user_ids = set(queryset.values_list("pk", flat=True))
    logged_out_count = 0

    logger.info(
        "User #{:d} has requested forced logout of user(s): {:s}.".format(
            user_id,
            ", ".join(str(uid) for uid in requested_user_ids),
        ),
    )

    for s in Session.objects.all():
        user_id = int(s.get_decoded().get("_auth_user_id"))
        if user_id in requested_user_ids:
            logger.info(f"Logged out user #{user_id}")
            s.delete()
            logged_out_count += 1

    if logged_out_count > 0:
        info_msg = _(f"{logged_out_count:d} user(s) where logged out.")
    else:
        info_msg = _("No active sessions were found for the selected users.")

    messages.add_message(request, messages.SUCCESS, info_msg)


class UserAdmin(DjangoUserAdmin):
    """Configuration for the User admin page"""

    add_form_template = "admin/users/user/add_form.html"
    change_form_template = "loginas/change_form.html"
    actions = [force_logout]

    add_form = UserCreationForm
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "change_password_link",
    )
    form = UserChangeForm

    search_fields = ("first_name", "last_name", "email")

    list_filter = ("last_login",)

    fieldsets = (
        (None, {"fields": ("email",)}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "groups",
                ),
            },
        ),
    )
    ordering = ("email",)

    @admin.display(description=_("change password"))
    def change_password_link(self, obj):
        return format_html(f'<a href="{obj.id}/password/">{_("change password")}</a>')

    change_password_link.allow_tags = True

    def has_logout_permission(self, request):
        return request.user.is_superuser


admin.site.register(User, UserAdmin)
