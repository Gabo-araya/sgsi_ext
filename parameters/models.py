""" Models for the parameters application. """
#  standard library
# standard library
import datetime
import json
import time

# django
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# models
from base.models import BaseModel

# definitions
from parameters.definitions import ParameterDefinitionList

# enums
from parameters.enums import ParameterKind
from parameters.utils import parsers


class Parameter(BaseModel):
    raw_value = models.TextField(
        verbose_name=_("value"),
    )
    name = models.CharField(
        max_length=50,
        verbose_name=_("name"),
        unique=True,
        editable=False,
    )
    kind = models.CharField(
        max_length=255,
        verbose_name=_("kind"),
        editable=False,
        choices=ParameterKind.choices,
    )
    cache_seconds = models.PositiveIntegerField(
        verbose_name=_("cache seconds"),
        default=3600,
    )

    def clean(self):
        if self.kind == ParameterKind.INT:
            parsers.parse_int_value(self.raw_value)
        elif self.kind == ParameterKind.TIME:
            parsers.parse_time_value(self.raw_value)
        elif self.kind == ParameterKind.DATE:
            parsers.parse_date_value(self.raw_value)
        elif self.kind == ParameterKind.JSON:
            parsers.parse_json_value(self.raw_value)
        elif self.kind == ParameterKind.URL:
            parsers.parse_url_value(self.raw_value)
        elif self.kind == ParameterKind.HOSTNAME:
            parsers.parse_hostname_value(self.raw_value)
        elif self.kind == ParameterKind.BOOL:
            parsers.parse_bool_value(self.raw_value)

        self.run_validators()

    def run_validators(self):
        parameter_definition = ParameterDefinitionList.get_definition(self.name)
        value = self.value
        for validator in parameter_definition.validators:
            validator(value)

    @property
    def value(self):
        return self.__class__.process_value(self.kind, self.raw_value)

    @classmethod
    def process_value(cls, kind, raw_value):
        if kind == ParameterKind.INT:
            return parsers.parse_int_value(raw_value)
        elif kind == ParameterKind.TIME:
            return parsers.parse_time_value(raw_value)
        elif kind == ParameterKind.DATE:
            return parsers.parse_date_value(raw_value)
        elif kind == ParameterKind.JSON:
            return parsers.parse_json_value(raw_value)
        elif kind == ParameterKind.URL:
            return parsers.parse_url_value(raw_value)
        elif kind == ParameterKind.HOSTNAME:
            return parsers.parse_hostname_value(raw_value)
        elif kind == ParameterKind.BOOL:
            return parsers.parse_bool_value(raw_value)
        else:
            return raw_value

    @value.setter
    def value(self, value):
        self.raw_value = value

    @classmethod
    def cache_key(cls, name):
        return "parameters-{}".format(slugify(name))

    @classmethod
    def value_for(cls, name):
        cache_key = cls.cache_key(name)

        cached_parameter = cache.get(cache_key)

        if cached_parameter:
            raw_value, kind = json.loads(cached_parameter)
            return cls.process_value(kind, raw_value)

        try:
            parameter = Parameter.objects.get(name=name)
        except Parameter.DoesNotExist:
            parameter = Parameter.create_parameter(name)

        parameter.store_in_cache()

        return parameter.value

    @classmethod
    def create_all_parameters(cls):
        for parameter_definition in ParameterDefinitionList.definitions:
            cls.objects.get_or_create(
                name=parameter_definition.name,
                defaults={
                    "kind": parameter_definition.kind,
                    "raw_value": parameter_definition.default,
                },
            )

    @classmethod
    def create_parameter(cls, name):
        parameter_definition = ParameterDefinitionList.get_definition(name)

        return cls.objects.create(
            name=name,
            kind=parameter_definition.kind,
            raw_value=parameter_definition.default,
        )

    # django methods
    def save(self, *args, **kwargs):
        self.store_in_cache()
        super(Parameter, self).save(*args, **kwargs)

    # public methods
    def store_in_cache(self):
        cache_key = Parameter.cache_key(self.name)

        cache.set(
            cache_key,
            json.dumps([self.raw_value, self.kind]),
            self.cache_seconds,  # the time in seconds to store the value
        )
