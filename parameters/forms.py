""" Forms for the parameters application. """
# standard library

# django
from django import forms

# views
from base.forms import BaseModelForm

# models
from .models import Parameter


class ParameterForm(BaseModelForm):
    """
    Form Parameter model.
    """

    class Meta:
        model = Parameter
        exclude = ()
