from django import forms

import pytest

from base.forms import BaseFormMixin


class ExampleBaseForm(BaseFormMixin):
    def __init__(self, *args, **kwargs):
        self.fields = {
            "date": forms.DateField(),
            "datetime": forms.DateTimeField(),
            "time": forms.TimeField(
                widget=forms.TimeInput(attrs={"class": "test-class"})
            ),
            "file": forms.FileField(),
            "checkbox": forms.BooleanField(
                widget=forms.CheckboxInput(attrs={"class": "test-class"})
            ),
            "text": forms.CharField(),
        }
        super().__init__(*args, **kwargs)


@pytest.mark.parametrize(
    (
        "field_name",
        "expected_class",
        "expected_widget_variables",
        "expected_widget_attrs",
    ),
    (
        (
            "date",
            "form-control",
            {"input_type": "date", "format": "%Y-%m-%d"},
            {},
        ),
        (
            "time",
            "test-class form-control",
            {"input_type": "time", "format": "%H:%M:%S"},
            {},
        ),
        (
            "datetime",
            "form-control",
            {"input_type": "datetime-local", "format": "%Y-%m-%d %H:%M:%S"},
            {},
        ),
        (
            "file",
            "form-control",
            {},
            {},
        ),
        (
            "checkbox",
            "test-class form-check-input",
            {},
            {"role": "switch"},
        ),
        (
            "text",
            "form-control",
            {},
            {},
        ),
    ),
)
def test_base_form_init(
    field_name, expected_class, expected_widget_variables, expected_widget_attrs
):
    form = ExampleBaseForm()
    widget = form.fields[field_name].widget
    assert widget.attrs["class"] == expected_class
    for attr, value in expected_widget_variables.items():
        assert getattr(widget, attr) == value
    for attr, value in expected_widget_attrs.items():
        assert widget.attrs[attr] == value


def test_base_form_hide_field():
    form = ExampleBaseForm()
    form.hide_field("text")
    assert isinstance(form.fields["text"].widget, forms.HiddenInput)
