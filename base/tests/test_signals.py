from unittest.mock import MagicMock
from unittest.mock import patch

from base.signals import audit_delete_log
from base.signals import audit_log


def test_audit_log_not_in_our_models():
    with (
        patch("base.signals.get_user", return_value="user"),
        patch("base.signals.get_our_models", return_value=[]),
    ):
        instance_mock = MagicMock()
        model = MagicMock()
        audit_log(model, instance_mock, created=False, raw=False)
        instance_mock._save_addition.assert_not_called()
        instance_mock._save_edition.assert_not_called()


def test_audit_log_in_our_models_raw():
    model = MagicMock()
    with (
        patch("base.signals.get_user", return_value="user"),
        patch("base.signals.get_our_models", return_value=[model]),
    ):
        instance_mock = MagicMock()
        audit_log(model, instance_mock, created=False, raw=True)
        instance_mock._save_addition.assert_not_called()
        instance_mock._save_edition.assert_not_called()


def test_audit_delete_log_in_our_models():
    model = MagicMock()
    with (
        patch("base.signals.get_user", return_value="user"),
        patch("base.signals.get_our_models", return_value=[model]),
    ):
        instance_mock = MagicMock()
        audit_delete_log(model, instance_mock)
        instance_mock._save_deletion.assert_called_once_with("user")


def test_audit_delete_log_not_in_our_models():
    with (
        patch("base.signals.get_user", return_value="user"),
        patch("base.signals.get_our_models", return_value=[]),
    ):
        instance_mock = MagicMock()
        model = MagicMock()
        audit_delete_log(model, instance_mock)
        instance_mock._save_deletion.assert_not_called()
