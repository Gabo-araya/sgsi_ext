"""
Tests for the user app
"""

from http import HTTPStatus
from urllib.parse import urlparse

from django.test import override_settings
from django.urls import reverse

import pytest

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
