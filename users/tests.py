"""
Tests for the user app
"""
# standard library
from http import HTTPStatus

# django
from django.urls import reverse

# tests
from base.tests import BaseTestCase


class UserTests(BaseTestCase):
    def test_lower_case_emails(self):
        """
        Tests that users are created with lower case emails
        """
        self.user.email = "Hello@magnet.cl"
        self.user.save()
        self.assertEqual("hello@magnet.cl", self.user.email)

    def test_force_logout(self):
        """
        Tests that users are created with lower case emails
        """
        url = reverse("password_change")
        response = self.client.get(url, follow=True)

        # test that the user is logged in
        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.user.force_logout()

        response = self.client.get(url, follow=True)

        # user is logged out, sow redirects to login
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
