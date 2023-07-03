from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin.widgets import AdminTimeWidget

from base.forms import BaseModelForm
from parameters.enums import ParameterKind

from .models import Parameter


class ParameterForm(BaseModelForm):
    class Meta:
        model = Parameter
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["raw_value"].widget = self.get_widget(self.instance.kind)

    def get_widget(self, kind: ParameterKind) -> forms.Widget:
        return {
            ParameterKind.INT: forms.NumberInput(),
            ParameterKind.TIME: AdminTimeWidget(),
            ParameterKind.DATE: AdminDateWidget(),
            ParameterKind.JSON: forms.Textarea(),
            ParameterKind.URL: forms.URLInput(),
            ParameterKind.BOOL: forms.Select(
                choices=(
                    ("True", "True"),
                    ("False", "False"),
                )
            ),
            ParameterKind.STR: forms.Textarea(),
        }.get(kind, forms.Textarea())
