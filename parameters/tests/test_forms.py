from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin.widgets import AdminTimeWidget

import pytest

from parameters.enums import ParameterKind
from parameters.forms import ParameterForm
from parameters.models import Parameter

EXPECTED_PARAMETER_WIDGET = {
    ParameterKind.INT: forms.NumberInput,
    ParameterKind.TIME: AdminTimeWidget,
    ParameterKind.DATE: AdminDateWidget,
    ParameterKind.JSON: forms.Textarea,
    ParameterKind.URL: forms.URLInput,
    ParameterKind.HOSTNAME: forms.Textarea,
    ParameterKind.IP_NETWORK: forms.Textarea,
    ParameterKind.HOSTNAME_LIST: forms.Textarea,
    ParameterKind.IP_NETWORK_LIST: forms.Textarea,
    ParameterKind.BOOL: forms.Select,
    ParameterKind.STR: forms.Textarea,
}


@pytest.mark.parametrize(
    ("kind", "expected_widget_class"),
    EXPECTED_PARAMETER_WIDGET.items(),
)
def test_parameter_form(db, kind, expected_widget_class):
    parameter = Parameter.objects.create(name="test_parameter", kind=kind)
    form = ParameterForm(instance=parameter)
    assert isinstance(form.fields["raw_value"].widget, expected_widget_class)
