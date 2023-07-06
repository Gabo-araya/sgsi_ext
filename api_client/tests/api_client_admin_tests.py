from unittest.mock import patch

import pytest

from api_client.admin import ClientConfigAdmin
from api_client.admin import ClientLogAdmin
from api_client.models import ClientConfig
from api_client.models import ClientLog


def test_cant_add_client_config_in_admin_if_full(client_config):
    with patch("django.contrib.admin.ModelAdmin.has_add_permission") as mock_add_perm:
        mock_add_perm.return_value = True
        admin_view = ClientConfigAdmin(model=ClientConfig, admin_site="test")
        assert not admin_view.has_add_permission(None)


def test_client_config_admin_respects_has_add_permission(db):
    with patch("django.contrib.admin.ModelAdmin.has_add_permission") as mock_add_perm:
        mock_add_perm.return_value = True
        admin_view = ClientConfigAdmin(model=ClientConfig, admin_site="test")
        assert admin_view.has_add_permission(None)


def test_cant_delete_client_config_in_admin():
    admin_view = ClientConfigAdmin(model=ClientConfig, admin_site="test")
    assert not admin_view.has_delete_permission(None)


@pytest.mark.parametrize(
    ("permission_func", "expected_result"),
    (
        ("has_add_permission", False),
        ("has_change_permission", False),
        ("has_delete_permission", False),
    ),
    ids=["has-add-permission", "has-change-permission", "has-delete-permission"],
)
@pytest.mark.django_db(databases=["default"])
def test_client_log_admin_permissions(permission_func, expected_result):
    admin_view = ClientLogAdmin(model=ClientLog, admin_site="test")
    assert expected_result == getattr(admin_view, permission_func)(None)
