""" The users app views"""


from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import base36_to_int
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import CreateView

# views
from base.views.generic import BaseListView
from base.views.mixins import ReactContextMixin
from parameters.models import Parameter

# forms
from users.forms import AuthenticationForm
from users.forms import CaptchaAuthenticationForm
from users.forms import UserCreationForm
from users.forms import UserForm
from users.models import User


class LoginView(auth_views.LoginView, ReactContextMixin):
    """view that renders the login"""

    template_name = "registration/login.html"
    form_class = AuthenticationForm
    title = _("Login")

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("home")
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        self.add_react_context(context)

        return context

    def get_form_class(self):
        parameter = Parameter.value_for("ENABLE_LOGIN_RECAPTCHA")
        if parameter:
            return CaptchaAuthenticationForm
        return super().get_form_class()


class PasswordChangeView(auth_views.PasswordChangeView):
    """view that renders the password change form"""

    template_name = "registration/password_change_form.html"


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = "registration/password_change_done.html"


class PasswordResetView(auth_views.PasswordResetView):
    """view that handles the recover password process"""

    template_name = "registration/password_reset_form.html"
    email_template_name = "emails/password_reset.txt"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """view that handles the recover password process"""

    template_name = "registration/password_reset_confirm.html"


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    """View that shows a success message to the user"""

    template_name = "registration/password_reset_done.html"


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    """View that shows a success message to the user"""

    template_name = "registration/password_reset_complete.html"


class UserCreateView(CreateView, ReactContextMixin):
    template_name = "users/create.html"
    form_class = UserCreationForm  # TODO Consider using captcha
    title = _("Registration")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        self.add_react_context(context)

        return context

    def form_valid(self, form):
        form.save(verify_email_address=True, request=self.request)
        messages.add_message(
            self.request,
            messages.INFO,
            _(
                "An email has been sent to you. Please "
                "check it to verify your email.",
            ),
        )

        return redirect("home")


@login_required
def user_edit(request):
    if request.method == "POST":
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                _("Your data has been successfully saved."),
            )
            return redirect("home")
    else:
        form = UserForm(instance=request.user)

    context = {
        "cancel_url": reverse("user_profile"),
        "form": form,
    }

    return render(request, "users/edit.html", context)


@login_required
def user_profile(request):
    context = {"title": _("My profile")}

    return render(request, "users/detail.html", context)


# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
def user_new_confirm(  # noqa: PLR0913
    request,
    uidb36=None,
    token=None,
    token_generator=default_token_generator,
    current_app=None,
    extra_context=None,
):
    """
    View that checks the hash in a email confirmation link and activates
    the user.
    """
    if uidb36 is None or token is None:
        msg = "uidb36 and token are required"
        raise ValueError(msg)
    try:
        uid_int = base36_to_int(uidb36)
        user = User.objects.get(id=uid_int)
    except (ValueError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.update(is_active=True)
        messages.add_message(
            request,
            messages.INFO,
            _("Your email address has been verified."),
        )
    else:
        messages.add_message(request, messages.ERROR, _("Invalid verification link"))

    return redirect("login")


class UserListView(BaseListView):
    model = User
    template_name = "users/list.html"
    ordering = ("first_name", "last_name")

    def get_queryset(self):
        queryset = super().get_queryset()

        # search users
        q = self.request.GET.get("q")
        if q:
            queryset = queryset.search(q)

        return queryset.prefetch_related("groups")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # we want to show a list of groups in each user, so we
        # iterate through each user, and create a string with the groups
        for obj in context["object_list"]:
            obj.group_names = " ".join([g.name for g in obj.groups.all()])

        return context
