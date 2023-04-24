# standard library
import collections

# django
from django.utils.translation import gettext_lazy as _

from parameters.validators import validate_protocol

ParameterDefinition = collections.namedtuple(
    "Parameter",
    [
        "name",
        "default",
        "kind",
        "verbose_name",
        "validators",
    ],
    defaults=((),),
)


class ParameterDefinitionList:
    definitions = [
        ParameterDefinition(
            name="DEFAULT_URL_PROTOCOL",
            default="https",
            kind="str",
            verbose_name=_("Default url protocol"),
            validators=(validate_protocol,),
        ),
    ]

    choices = tuple((x.name, x.verbose_name) for x in definitions)

    @classmethod
    def get_definition(cls, name):
        for parameter_definition in cls.definitions:
            if parameter_definition.name == name:
                return parameter_definition
