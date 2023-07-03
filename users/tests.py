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


class UserTests(BaseTestCase):
    def test_lower_case_emails(self):
        """
        Test that users are created with lower case emails
        """
        self.user.email = "Hello@magnet.cl"
        self.user.save()
        self.assertEqual("hello@magnet.cl", self.user.email)

    def test_force_logout(self):
        """
        Test that `force_logout` actually logs out user
        """
        url = reverse("password_change")
        login_url = reverse("login")
        response = self.client.get(url)

        # test that the user is logged in
        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.user.force_logout()

        response = self.client.get(url)

        # user is logged out, so it will redirect to login
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        parsed_location = urlparse(response.url)
        self.assertEqual(login_url, parsed_location.path)


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
