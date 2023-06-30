from django.test import TestCase


class CheckErrorPagesTest(TestCase):
    def test_404(self):
        response = self.client.get("/this-url-does-not-exist")
        self.assertTemplateUsed(response, "exceptions/404.pug")
