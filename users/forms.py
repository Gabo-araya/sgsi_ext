from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.template import loader
from django.utils.http import int_to_base36
from django.utils.translation import gettext_lazy as _

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

from base.forms import BaseModelForm
from users.models import User


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


class CaptchaAuthenticationForm(AuthenticationForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV3,
        error_messages={
            "captcha_invalid": _("Error verifying reCAPTCHA, please try again."),
            "captcha_error": _("Error verifying reCAPTCHA, please try again."),
            "required": _("Error verifying reCAPTCHA, please try again."),
        },
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        # define captcha widget as hidden to avoid unwanted labels
        self.fields["captcha"].widget.input_type = "hidden"


class AdminCaptchaAuthenticationForm(AdminAuthenticationForm):
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
        widget=ReCaptchaV3,
        error_messages={
            "captcha_invalid": _("Error verifying reCAPTCHA, please try again."),
            "captcha_error": _("Error verifying reCAPTCHA, please try again."),
            "required": _("Error verifying reCAPTCHA, please try again."),
        },
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        # define captcha widget as hidden to avoid unwanted labels
        self.fields["captcha"].widget.input_type = "hidden"

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_staff:
            raise ValidationError(
                self.error_messages["invalid_login"],
                code="invalid_login",
                params={"username": self.username_field.verbose_name},
            )


class UserCreationForm(BaseModelForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    error_messages = {
        "duplicate_email": _("A user with that email already exists."),
        "password_mismatch": _("The two password fields didn't match."),
    }

    first_name = forms.CharField(
        label=_("first name").capitalize(),
    )
    last_name = forms.CharField(
        label=_("last name").capitalize(),
    )
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
        fields = ("email",)

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
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.is_active = not verify_email_address

        if commit:
            user.save()

        if verify_email_address:
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


class UserForm(BaseModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
