from django.contrib.admin.forms import AdminAuthenticationForm
from django.urls import reverse

import pytest

from users.forms import AdminCaptchaAuthenticationForm


@pytest.mark.parametrize(
    ("parameter_fixture", "expected_form"),
    (
        ("set_parameter_recaptcha_false_definition", AdminAuthenticationForm),
        ("set_parameter_recaptcha_true_definition", AdminCaptchaAuthenticationForm),
    ),
)
@pytest.mark.django_db
def test_admin_login_form(parameter_fixture, expected_form, request, rf, client):
    request.getfixturevalue(parameter_fixture)
    url = reverse("admin:login")
    response = client.get(url)
    assert response.context["view"].authentication_form == expected_form
