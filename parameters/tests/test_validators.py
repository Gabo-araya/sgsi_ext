from contextlib import nullcontext as does_not_raise

from django.core.exceptions import ValidationError

import pytest

from parameters.models import Parameter
from parameters.validators import validate_protocol


@pytest.mark.parametrize(
    ("value", "expectation"),
    (
        ("http", does_not_raise()),
        ("https", does_not_raise()),
        ("gopher", pytest.raises(ValidationError)),
    ),
)
def test_validate_protocol(value, expectation):
    with expectation:
        validate_protocol(value)


@pytest.mark.usefixtures("set_parameter_test_definition_with_validators")
def test_run_validators(db):
    Parameter.create_all_parameters()
    parameter = Parameter.objects.first()
    with does_not_raise():
        parameter.clean()
    parameter.value = "RAISE"
    with pytest.raises(ValidationError):
        parameter.clean()
