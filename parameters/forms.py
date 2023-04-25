from base.forms import BaseModelForm

from .models import Parameter


class ParameterForm(BaseModelForm):
    class Meta:
        model = Parameter
        exclude = ()
