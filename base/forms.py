from __future__ import annotations

from django import forms
from django.forms import HiddenInput
from django.forms import ModelForm

forms.fields.Field.is_checkbox = lambda self: isinstance(
    self.widget,
    forms.CheckboxInput,
)

forms.fields.Field.is_file_input = lambda self: isinstance(self.widget, forms.FileInput)


class BaseModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            attrs = field.widget.attrs
            if "class" not in attrs:
                attrs["class"] = ""

            # TODO: Install Tempus Dominus for date/time inputs
            # https://getdatepicker.com/6/

            if isinstance(field.widget, forms.widgets.DateTimeInput):
                attrs["class"] += " datetimepicker-input form-control"
                attrs["data-format"] = "DD/MM/YYYY HH:mm:s"
                attrs["data-toggle"] = "datetimepicker"

            elif isinstance(field.widget, forms.widgets.DateInput):
                attrs["class"] += " datetimepicker-input form-control"
                attrs["data-format"] = "DD/MM/YYYY"
                attrs["data-toggle"] = "datetimepicker"

            elif isinstance(field.widget, forms.widgets.TimeInput):
                attrs["class"] += " datetimepicker-input form-control"
                attrs["data-format"] = "HH:mm:s"
                attrs["data-toggle"] = "datetimepicker"

            elif isinstance(field.widget, forms.widgets.FileInput):
                attrs["class"] += " form-control is-invalid"

            elif isinstance(field.widget, forms.widgets.CheckboxInput):
                attrs["class"] += " form-check-input"
            else:
                attrs["class"] += " form-control"

    def hide_field(self, field_name):
        self.fields[field_name].widget = HiddenInput()
