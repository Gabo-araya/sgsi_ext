from messaging.email_manager import send_emails


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


def test_send_email_no_context(settings, mailoutbox):
    settings.TEST = False
    send_emails(
        ["test@example.com"],
        "test_email",
        "Testing email",
        "mailer@example.com",
    )

    assert len(mailoutbox) > 0
