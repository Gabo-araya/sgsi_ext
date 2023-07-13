from contextlib import nullcontext as does_not_raise
from http import HTTPStatus
from unittest.mock import MagicMock
from unittest.mock import patch
from urllib.parse import urlparse

from django.forms import ValidationError
from django.urls import reverse

import pytest

from users.forms import AdminAuthenticationForm
from users.forms import AuthenticationForm
from users.forms import CaptchaAuthenticationForm
from users.forms import UserChangeForm
from users.forms import UserCreationForm
from users.models import User


@pytest.fixture
def duplicated_user(db):
    return User.objects.create_user(
        first_name="Alex", last_name="Smith", email="dupetest@example.com"
    )


def test_lower_case_emails(regular_user):
    """
    Test that users are created with lower case emails
    """
    regular_user.email = "Hello@magnet.cl"
    regular_user.save()
    assert regular_user.email == "hello@magnet.cl"


def test_force_logout(regular_user_client, regular_user):
    """
    Test that `force_logout` actually logs out user
    """
    url = reverse("password_change")
    login_url = reverse("login")
    response = regular_user_client.get(url)

    # test that the user is logged in
    assert response.status_code == HTTPStatus.OK

    regular_user.force_logout()

    response = regular_user_client.get(url)

    # user is logged out, so it will redirect to login
    assert response.status_code == HTTPStatus.FOUND

    parsed_location = urlparse(response.url)
    assert parsed_location.path == login_url


def test_user_creation_form_cleaning(db):
    input_data = {
        "email": "test@example.com",
        "first_name": "Alex",
        "last_name": "Schmidt",
        "password1": "verysecretpleasedontcopy(c)magnet",
        "password2": "verysecretpleasedontcopy(c)magnet",
    }
    form = UserCreationForm(data=input_data)
    form.full_clean()
    assert not form.errors


def test_user_creation_form_clean_duplicated_user(duplicated_user):
    input_data = {
        "email": "dupetest@example.com",
        "first_name": "Alex",
        "last_name": "Schmidt",
        "password1": "verysecretpleasedontcopy(c)magnet",
        "password2": "verysecretpleasedontcopy(c)magnet",
    }
    form = UserCreationForm(data=input_data)
    form.full_clean()
    assert "email" in form.errors


def test_user_creation_form_clean_password_mismatch(db):
    input_data = {
        "email": "test@example.com",
        "first_name": "Alex",
        "last_name": "Schmidt",
        "password1": "verysecretpleasedontcopy(c)magnet",
        "password2": "verysecretpleasedontsteal(c)magnet",
    }
    form = UserCreationForm(data=input_data)
    form.full_clean()
    errors = form.errors
    assert "password2" in errors
    password_error = errors["password2"]
    assert password_error.data[0].code == "password_mismatch"


@pytest.mark.parametrize(
    ("set_parameter", "expected"),
    (
        ("set_parameter_recaptcha_false_definition", AuthenticationForm),
        ("set_parameter_recaptcha_true_definition", CaptchaAuthenticationForm),
    ),
)
def test_user_login_form_show_correct_form(
    set_parameter, expected, client, request, db
):
    request.getfixturevalue(set_parameter)
    response = client.post(reverse("login"))
    assert isinstance(response.context["form"], expected)


@pytest.mark.parametrize(
    ("verify_email", "verify_email_calls", "commit", "commit_calls"),
    (
        (True, 1, True, 1),
        (False, 0, True, 1),
    ),
    ids=["verify_email_and_commit", "no_verify_email_and_dont_commit"],
)
def test_user_create_form_save(verify_email, verify_email_calls, commit, commit_calls):
    user_mock = MagicMock()
    with (
        patch("users.forms.BaseModelForm.save", return_value=user_mock),
        patch(
            "users.forms.UserCreationForm.send_verify_email"
        ) as send_verify_email_mock,
    ):
        form = UserCreationForm()
        form.cleaned_data = {
            "password1": "test",
            "first_name": "test",
            "last_name": "test",
        }
        user_mock.save.return_value = "test"
        assert form.save(verify_email_address=verify_email, commit=commit) == user_mock
        assert user_mock.first_name == "test"
        assert user_mock.last_name == "test"
        user_mock.set_password.assert_called_once_with("test")
        assert send_verify_email_mock.call_count == verify_email_calls
        assert user_mock.save.call_count == commit_calls


@pytest.mark.parametrize(
    ("override", "domain"),
    (
        (False, None),
        (True, "override.com"),
    ),
)
def test_user_create_form_send_verify_email(override, domain, regular_user):
    current_site = MagicMock()
    current_site.name = "test"
    current_site.domain = "test.com"
    with (
        patch(
            "users.forms.get_current_site", return_value=current_site
        ) as get_current_site_mock,
        patch("django.core.mail.send_mail") as send_mail_mock,
        patch(
            "users.forms.default_token_generator.make_token", return_value="test_token"
        ),
        patch("users.forms.int_to_base36", return_value="test_int"),
    ):
        UserCreationForm.send_verify_email(regular_user, domain_override=domain)
        assert get_current_site_mock.call_count == int(not override)
        assert send_mail_mock.call_count == 1


def test_user_change_form_set_user_permissions_queryset():
    user_permission_patch = MagicMock()
    user_permission_patch.queryset.select_related.return_value = "test"
    UserChangeForm.Meta.fields = (user_permission_patch,)
    form = UserChangeForm()
    form.set_user_permissions_queryset(user_permission_patch)
    assert user_permission_patch.queryset == "test"


@pytest.mark.parametrize(
    ("email", "password", "is_active", "is_staff", "auth_result", "expectation"),
    (
        ("test", "test", False, False, None, pytest.raises(ValidationError)),
        ("test", "test", True, True, None, pytest.raises(ValidationError)),
        ("test", "test", False, False, True, pytest.raises(ValidationError)),
        ("test", "test", True, False, True, pytest.raises(ValidationError)),
        ("test", "test", False, True, True, pytest.raises(ValidationError)),
        ("test", "test", True, True, True, does_not_raise()),
        ("test", "test", True, True, True, does_not_raise()),
        (None, "test", True, True, True, does_not_raise()),
        ("test", None, True, True, True, does_not_raise()),
        (None, None, False, False, None, does_not_raise()),
    ),
)
def test_admin_authentication_form_clean(
    email, password, is_active, is_staff, auth_result, expectation, regular_user
):
    regular_user.is_active = is_active
    regular_user.is_staff = is_staff
    auth_result = regular_user if auth_result else None
    with (
        expectation,
        patch("users.forms.authenticate", return_value=auth_result),
    ):
        form = AdminAuthenticationForm()
        form.cleaned_data = {
            "email": email,
            "password": password,
        }
        form.clean()


def test_authentication_form_get_invalid_login_error():
    form = AuthenticationForm()
    form.error_messages = {"invalid_login": "Invalid email or password"}
    form.email_field = MagicMock()
    form.email_field.verbose_name = "Email"
    error = form.get_invalid_login_error()
    assert isinstance(error, ValidationError)
    assert str(error) == "['Invalid email or password']"


def test_authentication_form_get_user():
    form = AuthenticationForm()
    form.user_cache = "test"
    assert form.get_user() == "test"


@pytest.mark.parametrize("has_user_cache", (True, False))
def test_authentication_form_get_user_id(has_user_cache, regular_user):
    form = AuthenticationForm()
    form.user_cache = regular_user if has_user_cache else None
    expected = regular_user.id if has_user_cache else None
    assert form.get_user_id() == expected


def test_authentication_form_full_clean():
    error_1_mock = MagicMock()
    error_1_mock.widget.attrs = {"class": "previous_class"}
    error_2_mock = MagicMock()
    error_2_mock.widget.attrs = {}
    with patch("django.forms.Form.full_clean") as full_clean_mock:
        form = AuthenticationForm()
        form._errors = ["error_1", "error_2", "error_non_existant"]
        form.fields = {"error_1": error_1_mock, "error_2": error_2_mock}
        form.full_clean()
        full_clean_mock.assert_called_once()
        assert error_1_mock.widget.attrs["class"] == "previous_class is-invalid"
        assert error_2_mock.widget.attrs["class"] == "is-invalid"


@pytest.mark.parametrize(
    ("is_active", "expectation"),
    (
        (True, does_not_raise()),
        (False, pytest.raises(ValidationError)),
    ),
)
def test_authentication_form_confirm_login_allowed(
    is_active, expectation, regular_user
):
    with expectation:
        regular_user.is_active = is_active
        form = AuthenticationForm()
        form.confirm_login_allowed(regular_user)


@pytest.mark.parametrize(
    ("email", "password", "auth_result", "expectation"),
    (
        ("test", "test", None, pytest.raises(ValidationError)),
        ("test", "test", True, does_not_raise()),
        (None, "test", None, does_not_raise()),
        ("test", None, None, does_not_raise()),
        (None, None, None, does_not_raise()),
    ),
)
def test_authentication_form_clean(email, password, auth_result, expectation):
    auth_result = MagicMock() if auth_result else None
    with (
        expectation,
        patch("users.forms.authenticate", return_value=auth_result),
        patch(
            "users.forms.AuthenticationForm.confirm_login_allowed"
        ) as confirm_login_allowed_mock,
    ):
        form = AuthenticationForm()
        form.cleaned_data = {"email": email, "password": password}
        form.clean()
        assert confirm_login_allowed_mock.call_count == int(bool(auth_result))


def test_user_send_example_email(regular_user):
    with patch("users.models.email_manager.send_example_email") as send_example_email:
        regular_user.send_example_email()
        send_example_email.assert_called_once_with(regular_user.email)


def test_send_recover_password_email(regular_user):
    with patch("users.models.email_manager.send_emails") as send_emails:
        regular_user.send_recover_password_email()
        send_emails.assert_called_once()
