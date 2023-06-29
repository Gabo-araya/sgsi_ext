from django.core import mail

from base.tests import BaseTestCase
from messaging.email_manager import send_emails


class EmailManagerTests(BaseTestCase):
    def test_send_email(self):
        with self.settings(TEST=False):
            context = {
                "value_a": 123,
                "value_b": "test",
                "value_c": True,
            }

            send_emails(
                ["test@example.com"],
                "test_email",
                "Testing email",
                "mailer@example.com",
                context,
            )

            self.assertGreater(len(mail.outbox), 0)

    def test_send_email_no_context(self):
        with self.settings(TEST=False):
            send_emails(
                ["test@example.com"],
                "test_email",
                "Testing email",
                "mailer@example.com",
            )

            self.assertGreater(len(mail.outbox), 0)
