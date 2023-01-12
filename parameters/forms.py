from base.forms import BaseModelForm

# models
from .models import Parameter


class ParameterForm(BaseModelForm):
    class Meta:
        model = Parameter
        exclude = ()
