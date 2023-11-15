from unittest.mock import patch

import pytest

from parameters.definitions import ParameterDefinitionList
from parameters.models import Parameter


@pytest.mark.usefixtures("set_parameter_test_definition")
def test_process_cached_parameter(parameter_definition, db):
    Parameter.value_for(parameter_definition.name)
    assert parameter_definition.default == Parameter.value_for(
        parameter_definition.name
    )


@pytest.mark.usefixtures("set_parameter_test_definition")
def test_use_parameter_cache(parameter_definition, db):
    with patch(
        "parameters.models.Parameter.process_cached_parameter"
    ) as mock_process_cached_parameter:
        Parameter.value_for(parameter_definition.name)
        assert mock_process_cached_parameter.call_count == 0
        Parameter.value_for(parameter_definition.name)
        assert mock_process_cached_parameter.call_count == 1


@pytest.mark.usefixtures("set_parameter_test_definition")
def test_parameter_value_for_creates_parameter_if_does_not_exist(
    parameter_definition, db
):
    assert Parameter.objects.count() == 0
    Parameter.value_for(parameter_definition.name)
    assert Parameter.objects.count() == 1


@pytest.mark.usefixtures("set_parameter_test_definition")
def test_create_parameter(parameter_definition, db):
    assert Parameter.objects.count() == 0
    Parameter.create_parameter(parameter_definition.name)
    assert Parameter.objects.count() == 1


@pytest.mark.usefixtures("set_parameter_test_definition")
def test_get_parameter_definition(parameter_definition):
    definition = ParameterDefinitionList.get_definition(parameter_definition.name)
    assert parameter_definition == definition
    assert ParameterDefinitionList.get_definition("DOESNT_EXIST") is None


def test_get_parameter_str(test_parameter):
    assert str(test_parameter) == "TEST_PARAMETER"


def test_create_all_parameters(db):
    Parameter.create_all_parameters()
    assert len(ParameterDefinitionList.definitions) == Parameter.objects.count()
