# standard library
import datetime
import ipaddress
import json
import re

# django
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils import formats
from django.utils.translation import gettext_lazy as _

from parameters.utils.ip import IPv4Range
from parameters.utils.ip import IPv6Range

EMPTY_VALUES = list(validators.EMPTY_VALUES)

DECIMAL_RE = re.compile(r"\.0*\s*$")
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


def parse_str_value(value):
    if value in EMPTY_VALUES:
        return None

    return value


def parse_int_value(value):
    if value in EMPTY_VALUES:
        return None

    value = str(value).strip()
    if value in EMPTY_VALUES:
        return None
    value = formats.sanitize_separators(value)
    # Strip trailing decimal and zeros.
    try:
        value = int(DECIMAL_RE.sub("", str(value)))
    except (ValueError, TypeError):
        raise ValidationError(_("Enter a whole number."), code="invalid")
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
            _("Enter a valid JSON."),
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


def _parse_single_hostname_value(value):
    """Validates a single hostname"""
    if value in EMPTY_VALUES:
        return None

    value = str(value).strip()
    if value:
        if HOSTNAME_RE.fullmatch(value):
            return value
        else:
            raise ValidationError(_("Enter a valid hostname."), code="invalid")
    return value


def parse_hostname_value(value, multiple=False):
    """Validator for hostnames. A hostname can be either an IPv4, IPv6 or a name.

    Multiple values are supported by setting `multiple=True`. In this case, the
    return value will always be a list."""
    if value in EMPTY_VALUES:
        return None

    value = str(value).strip()
    if multiple:
        values = value.split("\n")
        hostnames = (_parse_single_hostname_value(_value) for _value in values)
        return [hostname for hostname in hostnames if hostname]
    else:
        return _parse_single_hostname_value(value)


def _parse_ip_address_value(value):
    if value in EMPTY_VALUES:
        return None

    value = value.strip()
    if ":" in value:
        try:
            return ipaddress.IPv6Address(value)
        except ValueError:
            msg = _("Enter a valid IPv6 address.")
            raise ValidationError(msg, code="invalid")

    try:
        return ipaddress.IPv4Address(value)
    except ValueError:
        msg = _("Enter a valid IPv4 address.")
        raise ValidationError(msg, code="invalid")


def _parse_ip_prefix_value(value):
    if value in EMPTY_VALUES:
        return None

    value = value.strip()
    if ":" in value:
        try:
            return ipaddress.IPv6Network(value)
        except ValueError:
            msg = _("Enter a valid IPv6 prefix.")
            raise ValidationError(msg, code="invalid")

    try:
        return ipaddress.IPv4Network(value)
    except ValueError:
        msg = _("Enter a valid IPv4 prefix.")
        raise ValidationError(msg, code="invalid")


def _parse_ip_range_value(value):
    if value in EMPTY_VALUES:
        return None

    value = value.strip()
    range_values = value.split("-")
    if len(range_values) != 2:
        msg = _("Enter a valid address range.")
        raise ValidationError(msg, code="invalid")

    range_lower, range_higher = (
        _parse_ip_address_value(range_values[0]),
        _parse_ip_address_value(range_values[1]),
    )
    if type(range_lower) is not type(range_higher):
        msg = _("Both values must belong to the same address family.")
        raise ValidationError(msg, code="family_mismatch")
    if range_lower >= range_higher:
        msg = _("Lower address must be put first.")
        raise ValidationError(msg, code="ordering")

    if isinstance(range_lower, ipaddress.IPv4Address):
        return IPv4Range(range_lower, range_higher)
    elif isinstance(range_lower, ipaddress.IPv6Address):
        return IPv6Range(range_lower, range_higher)
    else:
        raise ValidationError(_("Unknown address family."), code="invalid")


def _parse_single_ip_network_value(value):
    """Validates a single IP range or prefix."""
    if value in EMPTY_VALUES:
        return None

    value = value.strip()
    if "-" in value:
        return _parse_ip_range_value(value)
    else:
        return _parse_ip_prefix_value(value)


def parse_ip_network_value(value, multiple=False):
    """Validator for ip prefix or range parameters. Both IPv6 and IPv4 addresses are
    supported.

    Multiple values are supported by setting `multiple=True`. In this case, the
    return value will always be a list."""
    if value in EMPTY_VALUES:
        return None

    value = value.strip()
    if multiple:
        values = value.split("\n")
        networks = (_parse_single_ip_network_value(_value) for _value in values)
        return [network for network in networks if network]
    else:
        return _parse_single_ip_network_value(value)


def parse_bool_value(value):
    """Validator for bool parameters.
    Taken from Django's forms.BooleanField `to_python`.
    """
    if value in EMPTY_VALUES:
        return None

    value = str(value).strip().lower()
    if value in ("false", "0"):
        value = False
    elif value in ("true", "1"):
        value = True
    else:
        raise ValidationError(
            _('Enter a valid boolean value. Valid values are "True", "False", 0 or 1.'),
            code="invalid",
        )
    return value
