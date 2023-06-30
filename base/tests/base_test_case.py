from django.test import TestCase

from base.middleware import RequestMiddleware
from base.mockups import Mockup
from base.utils import random_string


class BaseTestCase(TestCase):
    mockup = Mockup()

    @classmethod
    def setUpTestData(cls):
        cls.password = random_string()
        cls.user = cls.mockup.create_user(cls.password)

    def setUp(self):
        super().setUp()
        self.login()

    def tearDown(self, *args, **kwargs):
        super().tearDown(*args, **kwargs)
        thread_local = RequestMiddleware.thread_local
        thread_local.user = None

    def login(self, user=None, password=None):
        if user is None:
            user = self.user
            password = self.password

        username = getattr(user, user.USERNAME_FIELD)

        self.assertTrue(self.client.login(username=username, password=password))
