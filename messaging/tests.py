from unittest.mock import patch

from django.utils.translation import gettext_lazy as _

from messaging.email_manager import send_emails
from messaging.email_manager import send_example_email


def test_send_email(mailoutbox):
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

    assert len(mailoutbox) > 0


def test_send_email_no_context(mailoutbox):
    send_emails(
        ["test@example.com"],
        "test_email",
        "Testing email",
        "mailer@example.com",
    )

    assert len(mailoutbox) > 0


def test_send_example_email():
    with patch("messaging.email_manager.send_emails") as mock_send_emails:
        send_example_email("email@email.com")
        mock_send_emails.assert_called_once_with(
            emails=("email@email.com",),
            template_name="example_email",
            subject=_("Hello"),
            context={},
        )
