from django.core.cache import cache

import pytest

from parameters.definitions import ParameterDefinition
from parameters.definitions import ParameterDefinitionList
from parameters.enums import ParameterKind
from parameters.models import Parameter


@pytest.fixture
def test_parameter() -> Parameter:
    return Parameter.objects.create(
        name="TEST_PARAMETER",
        raw_value="test",
        kind=ParameterKind.STR,
        cache_seconds=60,
    )


@pytest.fixture
def recaptcha_false_parameter_definition() -> ParameterDefinition:
    return ParameterDefinition(
        name="ACTIVATE_LOGIN_RECAPTCHA",
        default=False,
        kind="bool",
        verbose_name="Activate login recaptcha",
    )


@pytest.fixture
def recaptcha_true_parameter_definition() -> ParameterDefinition:
    return ParameterDefinition(
        name="ACTIVATE_LOGIN_RECAPTCHA",
        default=True,
        kind="bool",
        verbose_name="Activate login recaptcha",
    )


@pytest.fixture
def set_parameter_recaptcha_false_definition(recaptcha_false_parameter_definition):
    cache.delete(Parameter.cache_key(recaptcha_false_parameter_definition.name))
    ParameterDefinitionList.definitions = [recaptcha_false_parameter_definition]


@pytest.fixture
def set_parameter_recaptcha_true_definition(recaptcha_true_parameter_definition):
    cache.delete(Parameter.cache_key(recaptcha_true_parameter_definition.name))
    ParameterDefinitionList.definitions = [recaptcha_true_parameter_definition]
