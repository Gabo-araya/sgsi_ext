from unittest.mock import patch

from parameters.admin import ParameterAdmin
from parameters.models import Parameter


def test_parameter_admin_create_all_parameters_in_get_changelist_instance(db):
    with (
        patch("django.contrib.admin.ModelAdmin.get_changelist_instance"),
        patch(
            "parameters.models.Parameter.create_all_parameters"
        ) as mock_create_params,
    ):
        admin_view = ParameterAdmin(Parameter, None)
        admin_view.get_changelist_instance(None)
        assert mock_create_params.call_count == 1


def test_parameter_admin_dont_re_create_all_parameters_in_get_changelist_instance(db):
    Parameter.create_all_parameters()
    with (
        patch("django.contrib.admin.ModelAdmin.get_changelist_instance"),
        patch(
            "parameters.models.Parameter.create_all_parameters"
        ) as mock_create_params,
    ):
        admin_view = ParameterAdmin(Parameter, None)
        admin_view.get_changelist_instance(None)
        assert mock_create_params.call_count == 0


def test_parameter_admin_does_not_have_add_permission():
    admin_view = ParameterAdmin(Parameter, None)
    assert not admin_view.has_add_permission(None)
