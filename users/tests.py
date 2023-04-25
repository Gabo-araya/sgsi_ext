"""
Tests for the user app
"""

from http import HTTPStatus
from urllib.parse import urlparse

from django.urls import reverse

# tests
from base.tests import BaseTestCase


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
