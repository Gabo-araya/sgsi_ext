from contextlib import nullcontext as does_not_raise
from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.views import View

import pytest

from base.views.mixins import LoginPermissionRequiredMixin
from base.views.mixins import SuperuserRestrictedMixin


class ExampleSuperuserView(SuperuserRestrictedMixin, View):
    pass


@pytest.mark.parametrize(
    ("login_required", "expectation"),
    (
        (True, does_not_raise()),
        (False, does_not_raise()),
        (None, pytest.raises(ImproperlyConfigured)),
        ("", pytest.raises(ImproperlyConfigured)),
    ),
)
def test_login_required_mixin_is_login_required(login_required, expectation):
    with expectation:
        mixin = LoginPermissionRequiredMixin()
        mixin.login_required = login_required
        assert mixin.is_login_required() == login_required


@pytest.mark.parametrize(
    ("user", "login_required", "output_patch", "expected"),
    (
        (
            "anonymous_user",
            True,
            "base.views.mixins.PermissionRequiredMixin.handle_no_permission",
            "no_permission",
        ),
        (
            "anonymous_user",
            False,
            "base.views.mixins.PermissionRequiredMixin.dispatch",
            "permission",
        ),
        (
            "regular_user",
            True,
            "base.views.mixins.PermissionRequiredMixin.dispatch",
            "permission",
        ),
        (
            "regular_user",
            False,
            "base.views.mixins.PermissionRequiredMixin.dispatch",
            "permission",
        ),
    ),
)
def test_login_required_mixin_dispatch(
    user, login_required, output_patch, expected, rf, request
):
    with patch(output_patch, return_value=expected):
        mixin = LoginPermissionRequiredMixin()
        mixin.login_required = login_required
        req = rf.get("/")
        req.user = request.getfixturevalue(user)
        assert mixin.dispatch(req) == expected


@pytest.mark.parametrize(
    ("user", "expectation"),
    (
        ("anonymous_user", pytest.raises(Http404)),
        ("regular_user", pytest.raises(Http404)),
        ("superuser_user", does_not_raise()),
    ),
)
def test_superuser_restricted_mixin(user, expectation, rf, request):
    with (
        expectation,
        patch(
            "django.views.View.dispatch",
        ),
    ):
        req = rf.get("/")
        req.user = request.getfixturevalue(user)
        ExampleSuperuserView().dispatch(req)
