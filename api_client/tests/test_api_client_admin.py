from unittest.mock import MagicMock
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


@pytest.mark.parametrize(
    ("func_name", "obj", "expected"),
    (
        (
            "request_headers_pretty",
            MagicMock(request_headers={"a": 1, "b": 2}),
            "<pre>a: 1\nb: 2</pre>",
        ),
        (
            "response_headers_pretty",
            MagicMock(response_headers={"a": 1, "b": 2}),
            "<pre>a: 1\nb: 2</pre>",
        ),
        (
            "request_content_pretty",
            MagicMock(request_content={"a": 1, "b": 2}),
            "<pre>{&#x27;a&#x27;: 1, &#x27;b&#x27;: 2}</pre>",
        ),
        (
            "response_content_pretty",
            MagicMock(response_content={"a": 1, "b": 2}),
            "<pre>{&#x27;a&#x27;: 1, &#x27;b&#x27;: 2}</pre>",
        ),
    ),
)
def test_request_pretty(func_name, obj, expected):
    admin_view = ClientLogAdmin(model=ClientLog, admin_site="test")
    assert getattr(admin_view, func_name)(obj) == expected
