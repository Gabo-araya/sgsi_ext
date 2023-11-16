import datetime
import ipaddress
import json
import math
import re

from django.conf import settings
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils import formats
from django.utils.timezone import get_current_timezone
from django.utils.translation import gettext_lazy as _

from pytz import timezone

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
    + r")$",
)


def parse_str_value(value):
    if value in EMPTY_VALUES:
        return None

    return str(value).strip()


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
    except (ValueError, TypeError) as error:
        raise ValidationError(_("Enter a whole number."), code="invalid") from error
    return value


def parse_float_value(value):
    if value in EMPTY_VALUES:
        return None

    value = str(value).strip()
    if value in EMPTY_VALUES:
        return None
    try:
        number = float(value)
        if math.isfinite(number):
            return number

        raise ValidationError(
            _("Enter a number"), code="invalid", params={"value": value}
        )
    except (TypeError, ValueError) as error:
        raise ValidationError(
            _("Enter a number"), code="invalid", params={"value": value}
        ) from error


def base_parse_temporal_value(value, input_formats, strptime):
    value = value.strip()
    # Try to strptime against each input format.
    for fmt in input_formats:
        try:
            return strptime(value, fmt)
        except (ValueError, TypeError):
            continue
    raise ValidationError(_("Enter a valid value."), code="invalid")


def parse_date_value(value):
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
            lambda v, f: (
                datetime.datetime.strptime(v, f)
                .astimezone(timezone(settings.TIME_ZONE))
                .date()
            ),
        )
    except ValidationError as error:
        raise ValidationError(_("Enter a valid date."), code="invalid") from error


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
            lambda v, f: (
                datetime.datetime.strptime(v, f)  # noqa: DTZ007
                .time()
                .replace(tzinfo=get_current_timezone())
            ),
        )
    except ValidationError as error:
        raise ValidationError(_("Enter a valid time."), code="invalid") from error


def parse_json_value(value, json_decoder=None):
    """Validator for time parameters.
    Taken from Django's forms.JSONField `to_python`.
    """
    if value in EMPTY_VALUES:
        return None
    if isinstance(value, (list, dict, int, float)):
        return value
    try:
        value = str(value).strip()
        converted = json.loads(value, cls=json_decoder)
    except json.JSONDecodeError as error:
        raise ValidationError(
            _("Enter a valid JSON."),
            code="invalid",
            params={"value": value},
        ) from error
    if isinstance(converted, str):
        return str(converted)
    return converted


def parse_url_value(value):
    if value in EMPTY_VALUES:
        return None
    value = str(value).strip()

    if value:
        # try the URL validator
        URLValidator()(value)
    return value


def parse_single_hostname_value(value):
    """Validates a single hostname"""
    if value in EMPTY_VALUES:
        return None

    value = str(value).strip()
    if value:
        if HOSTNAME_RE.fullmatch(value):
            return value
        raise ValidationError(_("Enter a valid hostname."), code="invalid")
    return value


def parse_hostname_value(value):
    """
    Validator for hostnames. A hostname can be either an IPv4, IPv6 or a name.
    """
    if value in EMPTY_VALUES:
        return None
    return parse_single_hostname_value(str(value).strip())


def parse_multiple_hostname_value(value):
    if value in EMPTY_VALUES:
        return None
    values = str(value).strip().split("\n")
    hostnames = (parse_single_hostname_value(_value) for _value in values)
    return [hostname for hostname in hostnames if hostname]


def parse_ip_address_value(value):
    if value in EMPTY_VALUES:
        return None

    if isinstance(value, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
        return value

    value = value.strip()
    if ":" in value:
        try:
            return ipaddress.IPv6Address(value)
        except ValueError as error:
            msg = _("Enter a valid IPv6 address.")
            raise ValidationError(msg, code="invalid") from error

    try:
        return ipaddress.IPv4Address(value)
    except ValueError as error:
        msg = _("Enter a valid IPv4 address.")
        raise ValidationError(msg, code="invalid") from error


def parse_ip_prefix_value(value):
    if value in EMPTY_VALUES:
        return None

    if isinstance(value, (ipaddress.IPv4Network, ipaddress.IPv6Network)):
        return value

    value = value.strip()
    if ":" in value:
        try:
            return ipaddress.IPv6Network(value)
        except ValueError as error:
            msg = _("Enter a valid IPv6 prefix.")
            raise ValidationError(msg, code="invalid") from error

    try:
        return ipaddress.IPv4Network(value)
    except ValueError as error:
        msg = _("Enter a valid IPv4 prefix.")
        raise ValidationError(msg, code="invalid") from error


def parse_ip_range_value(value):  # noqa: C901
    if value in EMPTY_VALUES:
        return None

    if isinstance(value, (IPv4Range, IPv6Range)):
        return value

    value = value.strip()
    range_values = value.split("-")
    if not range_values or len(range_values) > 2:  # noqa: PLR2004
        msg = _("Enter a valid address range.")
        raise ValidationError(msg, code="invalid")
    elif len(range_values) == 1:  # noqa: RET506
        address = parse_ip_address_value(range_values[0])
        if isinstance(address, ipaddress.IPv4Address):
            return IPv4Range(address, address)
        if isinstance(address, ipaddress.IPv6Address):
            return IPv6Range(address, address)
        raise ValidationError(_("Unknown address family."), code="invalid")

    range_lower, range_higher = (
        parse_ip_address_value(range_values[0]),
        parse_ip_address_value(range_values[1]),
    )
    if type(range_lower) is not type(range_higher):
        msg = _("Both values must belong to the same address family.")
        raise ValidationError(msg, code="family_mismatch")
    if range_lower > range_higher:
        msg = _("Lower address must be put first.")
        raise ValidationError(msg, code="ordering")

    if isinstance(range_lower, ipaddress.IPv4Address):
        return IPv4Range(range_lower, range_higher)
    if isinstance(range_lower, ipaddress.IPv6Address):
        return IPv6Range(range_lower, range_higher)
    raise ValidationError(_("Unknown address family."), code="invalid")


def parse_single_ip_network_value(value):
    """Validates a single IP range or prefix."""
    if value in EMPTY_VALUES:
        return None

    if isinstance(
        value, (IPv4Range, IPv6Range, ipaddress.IPv4Network, ipaddress.IPv6Network)
    ):
        return value

    value = value.strip()
    if "-" in value:
        return parse_ip_range_value(value)
    return parse_ip_prefix_value(value)


def parse_ip_network_value(value):
    """
    Validator for ip prefix or range parameters. Both IPv6 and IPv4 addresses are
    supported.
    """
    valid_values = (IPv4Range, IPv6Range, ipaddress.IPv4Network, ipaddress.IPv6Network)
    if value in EMPTY_VALUES:
        return None
    if isinstance(value, valid_values):
        return value
    return parse_single_ip_network_value(value.strip())


def parse_multiple_ip_network_value(value):
    valid_values = (IPv4Range, IPv6Range, ipaddress.IPv4Network, ipaddress.IPv6Network)
    if value in EMPTY_VALUES:
        return None
    if isinstance(value, (tuple, list)) and all(
        isinstance(item, valid_values) for item in value
    ):
        return value
    values = value.strip().split("\n")
    networks = (parse_single_ip_network_value(_value) for _value in values)
    return [network for network in networks if network]


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
