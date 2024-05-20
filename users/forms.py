from collections.abc import Iterable

from django import forms
from django.conf import settings
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.contrib.auth.models import Permission
from django.contrib.auth.tokens import default_token_generator
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.template import loader
from django.utils.http import int_to_base36
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

from base.forms import BaseModelForm
from documents.models.control import Control
from documents.models.control_category import ControlCategory
from documents.models.document import Document
from documents.models.document_version import DocumentVersion
from documents.models.evidence import Evidence
from information_assets.models.asset import Asset
from information_assets.models.asset_type import AssetType
from parameters.models import Parameter
from processes.models.process import Process
from processes.models.process_activity import ProcessActivity
from processes.models.process_activity_instance import ProcessActivityInstance
from processes.models.process_instance import ProcessInstance
from processes.models.process_version import ProcessVersion
from risks.models.risk import Risk
from users.models.group import Group
from users.models.user import User


class CaptchaWidgetConfigurationMixin:
    def _configure_recaptcha_widget(self, field_name):
        """Configures the captcha field widget in accordance to app settings."""
        widget_class_name = getattr(
            settings, "RECAPTCHA_WIDGET", "django_recaptcha.widgets.ReCaptchaV3"
        )
        widget_class = import_string(widget_class_name)

        captcha_field = self.fields[field_name]
        widget = widget_class()

        if captcha_field.localize:
            widget.is_localized = True
        widget.is_required = captcha_field.required
        # Update widget attrs with data-sitekey.
        widget.attrs["data-sitekey"] = captcha_field.public_key
        # Set required score from parameters, v3 only
        if issubclass(widget_class, ReCaptchaV3):
            widget.attrs["required_score"] = Parameter.value_for(
                "RECAPTCHA_V3_REQUIRED_SCORE"
            )

        captcha_field.widget = widget


class AuthenticationForm(forms.Form):
    """Custom class for authenticating users. Takes the basic
    AuthenticationForm and adds email as an alternative for login
    """

    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": _("Email")},
        ),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": _("Password")},
        ),
    )

    error_messages = {
        "invalid_login": _(
            "Please enter a correct email and password. "
            "Note that both fields may be case-sensitive.",
        ),
        "no_cookies": _(
            "Your Web browser doesn't appear to have cookies "
            "enabled. Cookies are required for logging in.",
        ),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        self.email_field = get_user_model()._meta.get_field(
            get_user_model().USERNAME_FIELD,
        )
        super().__init__(*args, **kwargs)

    def clean(self):
        """
        validates the email and password.
        """
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if not (email and password):
            return self.cleaned_data

        self.user_cache = authenticate(email=email, password=password)
        if self.user_cache is None:
            raise self.get_invalid_login_error()
        self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.

        Notes:
            If you use the default ``ModelBackend``, inactive users will be considered
            as non-existing and the default implementation of this method won't be
            reachable. If you really want to warn inactive users, you must use a
            backend supporting inactive users such as ``AllowAllUsersModelBackend``.
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def full_clean(self):
        super().full_clean()
        for field_name in self._errors:
            try:
                attrs = self.fields[field_name].widget.attrs
            except KeyError:
                continue

            if "class" not in attrs:
                attrs["class"] = "is-invalid"
            else:
                attrs["class"] += " is-invalid"

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"email": self.email_field.verbose_name},
        )


class CaptchaAuthenticationForm(CaptchaWidgetConfigurationMixin, AuthenticationForm):
    captcha = ReCaptchaField(
        error_messages={
            "captcha_invalid": _("Error verifying reCAPTCHA, please try again."),
            "captcha_error": _("Error verifying reCAPTCHA, please try again."),
            "required": _("Error verifying reCAPTCHA, please try again."),
        },
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self._configure_recaptcha_widget("captcha")


class AdminCaptchaAuthenticationForm(
    CaptchaWidgetConfigurationMixin, AdminAuthenticationForm
):
    """
    A custom authentication form used in the admin app, with reCAPTCHA.
    """

    error_messages = {
        **AdminAuthenticationForm.error_messages,
        "required": _("Please log in again, because your session has expired."),
        "invalid_login": _(
            "Please enter the correct %(username)s and password for a staff "
            "account. Note that both fields may be case-sensitive."
        ),
    }
    required_css_class = "required"

    captcha = ReCaptchaField(
        error_messages={
            "captcha_invalid": _("Error verifying reCAPTCHA, please try again."),
            "captcha_error": _("Error verifying reCAPTCHA, please try again."),
            "required": _("Error verifying reCAPTCHA, please try again."),
        },
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self._configure_recaptcha_widget("captcha")


class UserRegisterForm(BaseModelForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    error_messages = {
        "duplicate_email": _("A user with that email already exists."),
        "password_mismatch": _("The two password fields didn't match."),
    }

    password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

    def clean_email(self):
        """checks that the email is unique"""
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise ValidationError(self.error_messages["duplicate_email"])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        self.instance.username = self.cleaned_data.get("username")
        password_validation.validate_password(
            self.cleaned_data.get("password2"),
            self.instance,
        )
        return password2

    def save(  # noqa: PLR0913
        self,
        verify_email_address=False,
        commit=True,
        domain_override=None,
        subject_template_name="emails/user_new_subject.txt",
        email_template_name="emails/user_new.txt",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
    ):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        self.instance.set_password(self.cleaned_data["password1"])
        self.instance.is_active = not verify_email_address
        user = super().save(commit=commit)

        if commit and verify_email_address:
            self.send_verify_email(
                user,
                domain_override,
                subject_template_name,
                email_template_name,
                use_https,
                token_generator,
                from_email,
                request,
            )
        return user

    @staticmethod
    def send_verify_email(  # noqa: PLR0913
        user,
        domain_override=None,
        subject_template_name="emails/user_new_subject.txt",
        email_template_name="emails/user_new.txt",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
    ):
        from django.core.mail import send_mail

        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override

        context = {
            "email": user.email,
            "domain": domain,
            "site_name": site_name,
            "uid": int_to_base36(user.id),
            "user": user,
            "token": token_generator.make_token(user),
            "protocol": use_https and "https" or "http",
        }
        subject = loader.render_to_string(subject_template_name, context)
        subject = "".join(subject.splitlines())  # delete newlines
        email = loader.render_to_string(email_template_name, context)
        send_mail(subject, email, from_email, [user.email])


class UserForm(BaseModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class UserWithGroupsForm(BaseModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "is_active", "groups")


class UserCreationForm(UserWithGroupsForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["groups"].initial = Group.get_default_group_queryset()

    def save(
        self, commit: bool = True, *, send_recover_password_email: bool = False
    ) -> User:
        random_password = User.objects.make_random_password(length=30)
        self.instance.set_password(random_password)
        user: User = super().save(commit)
        if commit and send_recover_password_email:
            user.send_recover_password_email()
        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "is_active", "is_staff")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_permissions = self.fields.get("user_permissions", None)
        self.set_user_permissions_queryset(user_permissions)

    @staticmethod
    def set_user_permissions_queryset(user_permissions):
        if user_permissions is None:
            return
        user_permissions.queryset = user_permissions.queryset.select_related(
            "content_type"
        )


class GroupForm(BaseModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
    )

    class Meta:
        model = Group
        fields = ("name", "users", "permissions")

    def __init__(self, *args, user: User, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["users"].label_from_instance = lambda obj: obj.get_label()
        if user.has_perm("auth.view_permission"):
            self.configure_permission_field()
        else:
            self.hide_permission_field()
        if self.instance.pk:
            self.fields["users"].initial = self.instance.user_set.all()

    def configure_permission_field(self) -> None:
        permission_field = self.fields["permissions"]
        permission_field.queryset = Permission.objects.filter(
            content_type__in=self.get_permissible_content_types()
        )
        if self.instance.pk:
            permission_field.queryset |= self.instance.permissions.all()
        permission_field.label_from_instance = (
            lambda obj: f"{obj.content_type.name.title()}: {obj.name}"
        )

    def get_permissible_content_types(self) -> Iterable[ContentType]:
        permissible_models = (
            # users
            User,
            Group,
            # documents
            ControlCategory,
            Control,
            DocumentVersion,
            Document,
            Evidence,
            # information assets
            AssetType,
            Asset,
            # risks
            Risk,
            # processes
            ProcessActivityInstance,
            ProcessActivity,
            ProcessInstance,
            ProcessVersion,
            Process,
        )
        return ContentType.objects.get_for_models(*permissible_models).values()

    def hide_permission_field(self) -> None:
        self.fields["permissions"].widget = forms.HiddenInput()

    def save(self, commit: bool = True) -> Group:
        instance = super().save(commit)
        if not commit:
            return instance
        instance.user_set.set(self.cleaned_data["users"])
        return instance
