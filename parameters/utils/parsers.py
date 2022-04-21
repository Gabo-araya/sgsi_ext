# standard library
import datetime
import json
import re

# django
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _
from django.utils import formats

EMPTY_VALUES = list(validators.EMPTY_VALUES)

DECIMAL_RE = re.compile(r'\.0*\s*$')
HOSTNAME_RE = re.compile(
    r"^("
    + URLValidator.ipv4_re
    + "|"
    + URLValidator.ipv6_re
    + "|"
    + URLValidator.host_re
    + "|"
    + URLValidator.hostname_re
    + r")$"
)


def parse_int_value(value):
    if value in EMPTY_VALUES:
        return None

    value = str(value).strip()
    if value in EMPTY_VALUES:
        return None
    value = formats.sanitize_separators(value)
    # Strip trailing decimal and zeros.
    try:
        value = int(DECIMAL_RE.sub('', str(value)))
    except (ValueError, TypeError):
        raise ValidationError(_('Enter a whole number.'), code='invalid')
    return value


def base_parse_temporal_value(value, input_formats, strptime):
    value = value.strip()
    # Try to strptime against each input format.
    for format in input_formats:
        try:
            return strptime(value, format)
        except (ValueError, TypeError):
            continue
    raise ValidationError(_("Enter a valid value."), code="invalid")


def parse_date_value(value):
    """Validator for date parameters.
    Taken from Django's forms.DateField `to_python`.
    """
    input_formats = formats.get_format_lazy("DATE_INPUT_FORMATS")

    if value in EMPTY_VALUES:
        return None
    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, datetime.date):
        return value
    try:
        return base_parse_temporal_value(
            value,
            input_formats,
            lambda v, f: datetime.datetime.strptime(v, f).date(),
        )
    except ValidationError:
        raise ValidationError(_("Enter a valid date."), code="invalid")


def parse_time_value(value):
    """Validator for time parameters.
    Taken from Django's forms.TimeField `to_python`.
    """
    input_formats = formats.get_format_lazy("TIME_INPUT_FORMATS")

    if value in EMPTY_VALUES:
        return None
    if isinstance(value, datetime.time):
        return value
    try:
        return base_parse_temporal_value(
            value,
            input_formats,
            lambda v, f: datetime.datetime.strptime(v, f).time(),
        )
    except ValidationError:
        raise ValidationError(_("Enter a valid time."), code="invalid")


def parse_json_value(value, json_decoder=None):
    """Validator for time parameters.
    Taken from Django's forms.JSONField `to_python`.
    """
    if value in EMPTY_VALUES:
        return None
    elif isinstance(value, (list, dict, int, float)):
        return value
    try:
        value = str(value).strip()
        converted = json.loads(value, cls=json_decoder)
    except json.JSONDecodeError:
        raise ValidationError(
            _('Enter a valid JSON.'),
            code="invalid",
            params={"value": value},
        )
    if isinstance(converted, str):
        return str(converted)
    else:
        return converted


def parse_url_value(value):
    if value in EMPTY_VALUES:
        return None
    value = str(value).strip()

    if value:
        # try the URL validator
        URLValidator()(value)
    return value


def parse_hostname_value(value):
    """Validator for hostnames.

    A hostname can be either an IPv4, IPv6 or a name."""
    if value in EMPTY_VALUES:
        return None

    value = str(value).strip()
    if value:
        if HOSTNAME_RE.fullmatch(value):
            return value
        else:
            raise ValidationError(_("Enter a valid hostname."), code="invalid")
    return value


def parse_bool_value(value):
    """Validator for bool parameters.
    Taken from Django's forms.BooleanField `to_python`.
    """
    if value in EMPTY_VALUES:
        return None

    value = str(value).strip().lower()
    if value in ('false', '0'):
        value = False
    elif value in ('true', '1'):
        value = True
    else:
        raise ValidationError(
            _('Enter a valid boolean value. Valid values are "True", "False", 0 or 1.'),
            code="invalid"
        )
    return value
