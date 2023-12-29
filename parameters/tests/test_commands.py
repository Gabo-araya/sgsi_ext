from io import StringIO

from django.core.management import CommandError
from django.core.management import call_command

import pytest

from parameters.models import Parameter


@pytest.mark.usefixtures("set_parameter_test_definition_with_validators")
def test_setparameter_modifies_parameters(db):
    out = StringIO()
    call_command("setparameter", "TEST_DEFINITION", "new value", stdout=out)
    assert "changed successfully" in out.getvalue()

    parameter_value = Parameter.value_for("TEST_DEFINITION")
    assert parameter_value == "new value"


@pytest.mark.usefixtures("set_parameter_test_definition_with_validators")
def test_setparameter_fails_with_invalid_value(db):
    err = StringIO()
    call_command("setparameter", "TEST_DEFINITION", "RAISE", stderr=err)
    assert "Incorrect value" in err.getvalue()


@pytest.mark.usefixtures("set_parameter_test_definition_with_validators")
def test_setparameter_fails_with_invalid_parameter(db):
    err = StringIO()
    with pytest.raises(CommandError) as cm:
        call_command("setparameter", "NOT_EXISTS", "value", stderr=err)
        assert "does not exist" in cm.value
