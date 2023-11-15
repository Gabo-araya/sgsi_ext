import collections

from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
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
        ParameterDefinition(
            name="ENABLE_LOGIN_RECAPTCHA",
            default=False,
            kind="bool",
            verbose_name=_("Enable login recaptcha"),
        ),
        ParameterDefinition(
            name="RECAPTCHA_V3_REQUIRED_SCORE",
            default=0.65,
            kind="float",
            verbose_name=_("reCAPTCHA v3 minimum required score"),
            validators=(MinValueValidator(0), MaxValueValidator(1)),
        ),
    ]

    choices = tuple((x.name, x.verbose_name) for x in definitions)

    @classmethod
    def get_definition(cls, name):
        for parameter_definition in cls.definitions:
            if parameter_definition.name == name:
                return parameter_definition
        return None
