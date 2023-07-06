from django.core.cache import cache

import pytest

from parameters.definitions import ParameterDefinition
from parameters.definitions import ParameterDefinitionList
from parameters.models import Parameter


def validator(value):
    if value == "RAISE":
        raise ValueError


@pytest.fixture
def parameter_definition_with_validators() -> ParameterDefinition:
    return ParameterDefinition(
        name="TEST_DEFINITION",
        default="TEST",
        kind="str",
        verbose_name="test",
        validators=(validator,),
    )


@pytest.fixture
def set_parameter_test_definition_with_validators(parameter_definition_with_validators):
    cache.delete(Parameter.cache_key(parameter_definition_with_validators.name))
    ParameterDefinitionList.definitions = [parameter_definition_with_validators]


@pytest.fixture
def parameter_definition() -> ParameterDefinition:
    return ParameterDefinition(
        name="TEST_DEFINITION",
        default="TEST",
        kind="str",
        verbose_name="test",
    )


@pytest.fixture
def set_parameter_test_definition(parameter_definition):
    cache.delete(Parameter.cache_key(parameter_definition.name))
    ParameterDefinitionList.definitions = [parameter_definition]
