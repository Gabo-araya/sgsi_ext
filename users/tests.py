"""
Tests for the user app
"""

from http import HTTPStatus
from urllib.parse import urlparse

from django.urls import reverse

# tests
from base.tests import BaseTestCase
from users.forms import UserCreationForm
from users.models import User


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


class UserCreationFormTests(BaseTestCase):
    def test_user_creation_form_cleaning(self):
        input_data = {
            "email": "test@example.com",
            "first_name": "Alex",
            "last_name": "Schmidt",
            "password1": "verysecretpleasedontcopy(c)magnet",
            "password2": "verysecretpleasedontcopy(c)magnet",
        }
        form = UserCreationForm(data=input_data)
        form.full_clean()
        self.assertFalse(form.errors)

    def test_user_creation_form_clean_duplicated_user(self):
        User.objects.create_user(
            first_name="Alex", last_name="Smith", email="dupetest@example.com"
        )

        input_data = {
            "email": "dupetest@example.com",
            "first_name": "Alex",
            "last_name": "Schmidt",
            "password1": "verysecretpleasedontcopy(c)magnet",
            "password2": "verysecretpleasedontcopy(c)magnet",
        }
        form = UserCreationForm(data=input_data)
        form.full_clean()
        self.assertIn("email", form.errors)

    def test_user_creation_form_clean_password_mismatch(self):
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
        self.assertIn("password2", form.errors)
        password_error = errors["password2"]
        self.assertEqual(password_error.data[0].code, "password_mismatch")
