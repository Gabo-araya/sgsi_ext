import datetime
import ipaddress

from contextlib import contextmanager

from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES

import pytest

from parameters.definitions import ParameterDefinitionList
from parameters.models import Parameter
from parameters.utils.ip import IPv4Range
from parameters.utils.ip import IPv6Range
from parameters.utils.parsers import parse_bool_value
from parameters.utils.parsers import parse_date_value
from parameters.utils.parsers import parse_hostname_value
from parameters.utils.parsers import parse_int_value
from parameters.utils.parsers import parse_ip_address_value
from parameters.utils.parsers import parse_ip_network_value
from parameters.utils.parsers import parse_ip_prefix_value
from parameters.utils.parsers import parse_ip_range_value
from parameters.utils.parsers import parse_json_value
from parameters.utils.parsers import parse_single_hostname_value
from parameters.utils.parsers import parse_single_ip_network_value
from parameters.utils.parsers import parse_str_value
from parameters.utils.parsers import parse_time_value
from parameters.utils.parsers import parse_url_value
from parameters.validators import validate_protocol

EXPECTED_INT = 1
EXPECTED_STR = "test"
EXPECTED_DATE = datetime.date(2007, 1, 9)
EXPECTED_TIME = datetime.time(9, 41)

EXPECTED_IPV4_RANGE = IPv4Range(
    ipaddress.IPv4Address("10.26.40.1"),
    ipaddress.IPv4Address("10.26.40.16"),
)
EXPECTED_IPV4_RANGE_SAME = IPv4Range(
    ipaddress.IPv4Address("10.26.40.1"),
    ipaddress.IPv4Address("10.26.40.1"),
)
EXPECTED_IPV6_RANGE = IPv6Range(
    ipaddress.IPv6Address("2800:6D61:676E:6574::1"),
    ipaddress.IPv6Address("2800:6D61:676E:6574::2640"),
)
EXPECTED_IPV6_RANGE_SAME = IPv6Range(
    ipaddress.IPv6Address("2800:6D61:676E:6574::1"),
    ipaddress.IPv6Address("2800:6D61:676E:6574::1"),
)
EXPECTED_IPV4_PREFIX = ipaddress.IPv4Network("10.26.40.0/24")
EXPECTED_IPV6_PREFIX = ipaddress.IPv6Network("2800:6D61:676E:6574::/64")


@contextmanager
def does_not_raise():
    yield


def test_create_all_parameters(db):
    Parameter.create_all_parameters()
    assert len(ParameterDefinitionList.definitions) == Parameter.objects.count()


@pytest.mark.parametrize(
    ("value", "expectation"),
    (
        ("http", does_not_raise()),
        ("https", does_not_raise()),
        ("gopher", pytest.raises(ValidationError)),
    ),
)
def test_validate_protocol(value, expectation):
    with expectation:
        validate_protocol(value)


@pytest.mark.parametrize(
    ("raw_value", "expected_value"),
    (
        *((empty_val, None) for empty_val in EMPTY_VALUES),
        ("   ", ""),
        ("test", "test"),
        ("test  ", "test"),
        (" test ", "test"),
        ("  test", "test"),
    ),
    ids=[
        *(f"empty-{n}" for n, _ in enumerate(EMPTY_VALUES)),
        "whitespace",
        "string",
        "space-string",
        "space-string-space",
        "string-space",
    ],
)
def test_parse_str_value(raw_value, expected_value):
    assert parse_str_value(raw_value) == expected_value


@pytest.mark.parametrize(
    ("raw_value", "expected_value", "expectation"),
    (
        *((empty_val, None, does_not_raise()) for empty_val in EMPTY_VALUES),
        ("   ", None, does_not_raise()),
        ("1  ", 1, does_not_raise()),
        (" 1 ", 1, does_not_raise()),
        ("  1", 1, does_not_raise()),
        ("x", 1, pytest.raises(ValidationError)),
    ),
    ids=[
        *(f"empty-{n}" for n, _ in enumerate(EMPTY_VALUES)),
        "whitespace",
        "1-spaces",
        "space-1-space",
        "spaces-1",
        "non-int-string",
    ],
)
def test_parse_int_value(raw_value, expected_value, expectation):
    with expectation:
        assert parse_int_value(raw_value) == expected_value


@pytest.mark.parametrize(
    ("raw_value", "expected_value", "expectation"),
    (
        *((empty_val, None, does_not_raise()) for empty_val in EMPTY_VALUES),
        ("2007-01-09  ", EXPECTED_DATE, does_not_raise()),
        (" 2007-01-09 ", EXPECTED_DATE, does_not_raise()),
        ("  2007-01-09", EXPECTED_DATE, does_not_raise()),
        (datetime.date(2007, 1, 9), EXPECTED_DATE, does_not_raise()),
        (
            datetime.datetime(2007, 1, 9, 9, 41),  # noqa: DTZ001
            EXPECTED_DATE,
            does_not_raise(),
        ),
        (" ", None, pytest.raises(ValidationError)),
        ("x", None, pytest.raises(ValidationError)),
    ),
    ids=[
        *(f"empty-{n}" for n, _ in enumerate(EMPTY_VALUES)),
        "date-spaces",
        "space-date-space",
        "spaces-date",
        "date-obj",
        "datetime-obj",
        "whitespace",
        "non-date-string",
    ],
)
def test_parse_date_value(raw_value, expected_value, expectation):
    with expectation:
        assert parse_date_value(raw_value) == expected_value


@pytest.mark.parametrize(
    ("raw_value", "expected_value", "expectation"),
    (
        *((empty_val, None, does_not_raise()) for empty_val in EMPTY_VALUES),
        ("09:41  ", EXPECTED_TIME, does_not_raise()),
        (" 09:41 ", EXPECTED_TIME, does_not_raise()),
        ("  09:41", EXPECTED_TIME, does_not_raise()),
        (datetime.time(9, 41), EXPECTED_TIME, does_not_raise()),
        (" ", None, pytest.raises(ValidationError)),
        ("x", None, pytest.raises(ValidationError)),
    ),
    ids=[
        *(f"empty-{n}" for n, _ in enumerate(EMPTY_VALUES)),
        "time-spaces",
        "space-time-space",
        "spaces-time",
        "time-obj",
        "whitespace",
        "non-date-string",
    ],
)
def test_parse_time_value(raw_value, expected_value, expectation):
    with expectation:
        assert parse_time_value(raw_value) == expected_value


@pytest.mark.parametrize(
    ("raw_value", "expected_value", "expectation"),
    (
        *((empty_val, None, does_not_raise()) for empty_val in EMPTY_VALUES),
        # should not raise
        ("https://www.magnet.cl", "https://www.magnet.cl", does_not_raise()),
        ("https://magnet.cl", "https://magnet.cl", does_not_raise()),
        ("https://magnet.cl/", "https://magnet.cl/", does_not_raise()),
        (
            "https://admin:secret@www.magnet.cl:8443/",
            "https://admin:secret@www.magnet.cl:8443/",
            does_not_raise(),
        ),
        # should raise
        ("www.magnet.cl", "www.magnet.cl", pytest.raises(ValidationError)),
        ("magnet.cl", "magnet.cl", pytest.raises(ValidationError)),
        ("x", None, pytest.raises(ValidationError)),
    ),
    ids=[
        *(f"empty-{n}" for n, _ in enumerate(EMPTY_VALUES)),
        "full-www-url",
        "full-url",
        "full-url-trailing-slash",
        "full-url-with-auth-port",
        "www-without-scheme",
        "without-scheme",
        "non-url-string",
    ],
)
def test_parse_url_value(raw_value, expected_value, expectation):
    with expectation:
        assert parse_url_value(raw_value) == expected_value


@pytest.mark.parametrize(
    ("raw_value", "expected_value", "expectation"),
    (
        *((empty_val, None, does_not_raise()) for empty_val in EMPTY_VALUES),
        # should not raise
        (" True ", True, does_not_raise()),
        ("True", True, does_not_raise()),
        (" False ", False, does_not_raise()),
        ("False", False, does_not_raise()),
        ("false", False, does_not_raise()),
        ("true", True, does_not_raise()),
        ("1", True, does_not_raise()),
        ("0", False, does_not_raise()),
        (True, True, does_not_raise()),
        (False, False, does_not_raise()),
        (1, True, does_not_raise()),
        (0, False, does_not_raise()),
        # should raise
        ("x", None, pytest.raises(ValidationError)),
    ),
    ids=[
        *(f"empty-{n}" for n, _ in enumerate(EMPTY_VALUES)),
        "True-str-whitespace",
        "True-str",
        "False-str-whitespace",
        "False-str",
        "True-str-lower",
        "False-str-lower",
        "1-str",
        "0-str",
        "True-bool",
        "False-bool",
        "1-int",
        "0-int",
        "non-bool-string",
    ],
)
def test_parse_bool_value(raw_value, expected_value, expectation):
    with expectation:
        assert parse_bool_value(raw_value) == expected_value


@pytest.mark.parametrize(
    ("raw_value", "expected_value", "expectation"),
    (
        *((empty_val, None, does_not_raise()) for empty_val in EMPTY_VALUES),
        (123, 123, does_not_raise()),
        (1.234, 1.234, does_not_raise()),
        (True, True, does_not_raise()),
        ([1, 2, 3], [1, 2, 3], does_not_raise()),
        (
            {"a": 1, "b": True, "c": [1, 2]},
            {"a": 1, "b": True, "c": [1, 2]},
            does_not_raise(),
        ),
    ),
    ids=[
        *(f"empty-{n}" for n, _ in enumerate(EMPTY_VALUES)),
        "int",
        "float",
        "bool",
        "list",
        "dict",
    ],
)
def test_parse_json_value_python_values(raw_value, expected_value, expectation):
    with expectation:
        assert parse_json_value(raw_value) == expected_value


@pytest.mark.parametrize(
    ("raw_value", "expected_value", "expectation"),
    (
        ('"test"', "test", does_not_raise()),
        ("123", 123, does_not_raise()),
        ("1.234", 1.234, does_not_raise()),
        ("true", True, does_not_raise()),
        ("false", False, does_not_raise()),
        ("[1,2,3]", [1, 2, 3], does_not_raise()),
        (
            '{"a": 1, "b": "abc", "c": true, "d": [1,2,3], "e":{"x": "y"}}',
            {"a": 1, "b": "abc", "c": True, "d": [1, 2, 3], "e": {"x": "y"}},
            does_not_raise(),
        ),
        (" [1,2,3] ", [1, 2, 3], does_not_raise()),
        ("{a: 123}", None, pytest.raises(ValidationError)),
    ),
    ids=[
        "str",
        "int",
        "float",
        "bool-true",
        "bool-false",
        "list",
        "dict",
        "trailing-leading-space",
        "invalid",
    ],
)
def test_parse_json_value(raw_value, expected_value, expectation):
    with expectation:
        assert parse_json_value(raw_value) == expected_value


@pytest.mark.parametrize(
    ("raw_value", "expected_value", "expectation"),
    (
        *((empty_val, None, does_not_raise()) for empty_val in EMPTY_VALUES),
        ("  ", "", does_not_raise()),
        ("magnet.cl", "magnet.cl", does_not_raise()),
        ("www.magnet.cl", "www.magnet.cl", does_not_raise()),
        ("d3pt.dev.magnet.cl", "d3pt.dev.magnet.cl", does_not_raise()),
        ("8.8.8.8", "8.8.8.8", does_not_raise()),
        ("[::1]", "[::1]", does_not_raise()),
        ("ñandú.cl", "ñandú.cl", does_not_raise()),
        ("256.1.562.6", None, pytest.raises(ValidationError)),
    ),
    ids=[
        *(f"empty-{n}" for n, _ in enumerate(EMPTY_VALUES)),
        "whitespace-empty",
        "two-component",
        "three-component",
        "four-component",
        "ipv4",
        "ipv6",
        "idn",
        "invalid",
    ],
)
def test_parse_single_hostname_value(raw_value, expected_value, expectation):
    with expectation:
        assert parse_single_hostname_value(raw_value) == expected_value


@pytest.mark.parametrize(
    ("raw_value", "multiple", "expected_value", "expectation"),
    (
        *((empty_val, False, None, does_not_raise()) for empty_val in EMPTY_VALUES),
        *((empty_val, True, None, does_not_raise()) for empty_val in EMPTY_VALUES),
        ("  ", False, None, does_not_raise()),
        ("magnet.cl", False, "magnet.cl", does_not_raise()),
        ("magnet.cl\nwww.magnet.cl", False, None, pytest.raises(ValidationError)),
        ("256.1.562.6", False, None, pytest.raises(ValidationError)),
        ("   ", True, [], does_not_raise()),
        ("magnet.cl", True, ["magnet.cl"], does_not_raise()),
        (
            "magnet.cl\nwww.magnet.cl",
            True,
            ["magnet.cl", "www.magnet.cl"],
            does_not_raise(),
        ),
        ("256.1.562.6", True, None, pytest.raises(ValidationError)),
    ),
    ids=[
        *(f"single-empty-{n}" for n, _ in enumerate(EMPTY_VALUES)),
        *(f"multiple-empty-{n}" for n, _ in enumerate(EMPTY_VALUES)),
        "single-whitespace-empty",
        "single-single",
        "single-multiple",
        "single-invalid",
        "multiple-whitespace-empty",
        "multiple-single",
        "multiple-multiple",
        "multiple-invalid",
    ],
)
def test_parse_hostname_value(raw_value, multiple, expected_value, expectation):
    with expectation:
        assert parse_hostname_value(raw_value, multiple) == expected_value


@pytest.mark.parametrize(
    ("raw_value", "expected_value", "expectation"),
    (
        *((empty_val, None, does_not_raise()) for empty_val in EMPTY_VALUES),
        (
            ipaddress.IPv4Address("8.8.8.8"),
            ipaddress.IPv4Address("8.8.8.8"),
            does_not_raise(),
        ),
        (
            ipaddress.IPv6Address("::1"),
            ipaddress.IPv6Address("::1"),
            does_not_raise(),
        ),
        ("8.8.8.8", ipaddress.IPv4Address("8.8.8.8"), does_not_raise()),
        ("::1", ipaddress.IPv6Address("::1"), does_not_raise()),
        ("256.257.258.1", None, pytest.raises(ValidationError)),
        ("::fffff", None, pytest.raises(ValidationError)),
    ),
    ids=[
        *(f"empty-{n}" for n, _ in enumerate(EMPTY_VALUES)),
        "ipv4-object",
        "ipv6-object",
        "ipv4-str",
        "ipv6-str",
        "invalid-ipv4-str",
        "invalid-ipv6-str",
    ],
)
def test_parse_ip_address_value(raw_value, expected_value, expectation):
    with expectation:
        assert parse_ip_address_value(raw_value) == expected_value


@pytest.mark.parametrize(
    ("raw_value", "expected_value", "expectation"),
    (
        *((empty_val, None, does_not_raise()) for empty_val in EMPTY_VALUES),
        (EXPECTED_IPV4_PREFIX, EXPECTED_IPV4_PREFIX, does_not_raise()),
        (EXPECTED_IPV6_PREFIX, EXPECTED_IPV6_PREFIX, does_not_raise()),
        ("10.26.40.0/24", EXPECTED_IPV4_PREFIX, does_not_raise()),
        ("2800:6D61:676E:6574::/64", EXPECTED_IPV6_PREFIX, does_not_raise()),
        ("   10.26.40.0/24", EXPECTED_IPV4_PREFIX, does_not_raise()),
        ("2800:6D61:676E:6574::/64   ", EXPECTED_IPV6_PREFIX, does_not_raise()),
        ("320.0.0.0/36", None, pytest.raises(ValidationError)),
        ("fffff::/128", None, pytest.raises(ValidationError)),
    ),
    ids=[
        *(f"empty-{n}" for n, _ in enumerate(EMPTY_VALUES)),
        "ipv4-object",
        "ipv6-object",
        "ipv4-str",
        "ipv6-str",
        "ipv4-str-whitespace",
        "ipv6-str-whitespace",
        "invalid-ipv4-str",
        "invalid-ipv6-str",
    ],
)
def test_parse_ip_prefix_value(raw_value, expected_value, expectation):
    with expectation:
        assert parse_ip_prefix_value(raw_value) == expected_value


@pytest.mark.parametrize(
    ("raw_value", "expected_value", "expectation"),
    (
        *((empty_val, None, does_not_raise()) for empty_val in EMPTY_VALUES),
        (EXPECTED_IPV4_RANGE, EXPECTED_IPV4_RANGE, does_not_raise()),
        (EXPECTED_IPV6_RANGE, EXPECTED_IPV6_RANGE, does_not_raise()),
        (
            "10.26.40.1-10.26.40.16",
            EXPECTED_IPV4_RANGE,
            does_not_raise(),
        ),
        (
            "2800:6D61:676E:6574::1-2800:6D61:676E:6574::2640",
            EXPECTED_IPV6_RANGE,
            does_not_raise(),
        ),
        (
            "10.26.40.1",
            EXPECTED_IPV4_RANGE_SAME,
            does_not_raise(),
        ),
        (
            "2800:6D61:676E:6574::1",
            EXPECTED_IPV6_RANGE_SAME,
            does_not_raise(),
        ),
        (
            "10.26.40.1-10.26.40.1",
            EXPECTED_IPV4_RANGE_SAME,
            does_not_raise(),
        ),
        (
            "2800:6D61:676E:6574::1-2800:6D61:676E:6574::1",
            EXPECTED_IPV6_RANGE_SAME,
            does_not_raise(),
        ),
        (
            "10.26.40.16-10.26.40.1",
            None,
            pytest.raises(ValidationError),
        ),
        (
            "10.26.40.1-10.26.40.1-10.26.40.3",
            EXPECTED_IPV4_RANGE_SAME,
            pytest.raises(ValidationError),
        ),
        (
            "2800:6D61:676E:6574::ffff-2800:6D61:676E:6574::0",
            ipaddress.IPv6Network("2800:6D61:676E:6574::/64"),
            pytest.raises(ValidationError),
        ),
        (
            "10.26.40.16-2800:6D61:676E:6574::2640",
            None,
            pytest.raises(ValidationError),
        ),
        ("320.0.0.0/36-384.0.0.0/36", None, pytest.raises(ValidationError)),
        ("fffff::/128-fffff::ffff/128", None, pytest.raises(ValidationError)),
    ),
    ids=[
        *(f"empty-{n}" for n, _ in enumerate(EMPTY_VALUES)),
        "ipv4-range",
        "ipv6-range",
        "ipv4-str",
        "ipv6-str",
        "single-ipv4",
        "single-ipv6",
        "same-ipv4-range",
        "same-ipv6-range",
        "many-addresses",
        "inverted-ipv4-str",
        "inverted-ipv6-str",
        "mixed-family",
        "invalid-ipv4-str",
        "invalid-ipv6-str",
    ],
)
def test_parse_ip_range_value(raw_value, expected_value, expectation):
    with expectation:
        assert parse_ip_range_value(raw_value) == expected_value


@pytest.mark.parametrize(
    ("raw_value", "expected_value", "expectation"),
    (
        *((empty_val, None, does_not_raise()) for empty_val in EMPTY_VALUES),
        (EXPECTED_IPV4_RANGE, EXPECTED_IPV4_RANGE, does_not_raise()),
        (EXPECTED_IPV6_RANGE, EXPECTED_IPV6_RANGE, does_not_raise()),
        (EXPECTED_IPV4_PREFIX, EXPECTED_IPV4_PREFIX, does_not_raise()),
        (EXPECTED_IPV6_PREFIX, EXPECTED_IPV6_PREFIX, does_not_raise()),
        ("10.26.40.1-10.26.40.16", EXPECTED_IPV4_RANGE, does_not_raise()),
        (
            "2800:6D61:676E:6574::1-2800:6D61:676E:6574::2640",
            EXPECTED_IPV6_RANGE,
            does_not_raise(),
        ),
        ("10.26.40.0/24", EXPECTED_IPV4_PREFIX, does_not_raise()),
        ("2800:6D61:676E:6574::/64", EXPECTED_IPV6_PREFIX, does_not_raise()),
    ),
    ids=[
        *(f"empty-{n}" for n, _ in enumerate(EMPTY_VALUES)),
        "ipv4-range",
        "ipv6-range",
        "ipv4-prefix",
        "ipv6-prefix",
        "ipv4-range-str",
        "ipv6-range-str",
        "ipv4-prefix-str",
        "ipv6-prefix-str",
    ],
)
def test_parse_single_ip_network_value(raw_value, expected_value, expectation):
    with expectation:
        assert parse_single_ip_network_value(raw_value) == expected_value


@pytest.mark.parametrize(
    ("raw_value", "expected_value", "expectation"),
    (
        *((empty_val, None, does_not_raise()) for empty_val in EMPTY_VALUES),
        (EXPECTED_IPV4_RANGE, EXPECTED_IPV4_RANGE, does_not_raise()),
        (EXPECTED_IPV6_RANGE, EXPECTED_IPV6_RANGE, does_not_raise()),
        (EXPECTED_IPV4_PREFIX, EXPECTED_IPV4_PREFIX, does_not_raise()),
        (EXPECTED_IPV6_PREFIX, EXPECTED_IPV6_PREFIX, does_not_raise()),
        ("10.26.40.1-10.26.40.16", EXPECTED_IPV4_RANGE, does_not_raise()),
        (
            "2800:6D61:676E:6574::1-2800:6D61:676E:6574::2640",
            EXPECTED_IPV6_RANGE,
            does_not_raise(),
        ),
        ("10.26.40.0/24", EXPECTED_IPV4_PREFIX, does_not_raise()),
        ("2800:6D61:676E:6574::/64", EXPECTED_IPV6_PREFIX, does_not_raise()),
    ),
    ids=[
        *(f"empty-{n}" for n, _ in enumerate(EMPTY_VALUES)),
        "ipv4-range",
        "ipv6-range",
        "ipv4-prefix",
        "ipv6-prefix",
        "ipv4-range-str",
        "ipv6-range-str",
        "ipv4-prefix-str",
        "ipv6-prefix-str",
    ],
)
def test_parse_ip_network_value_single(raw_value, expected_value, expectation):
    with expectation:
        assert parse_ip_network_value(raw_value, False) == expected_value


@pytest.mark.parametrize(
    ("raw_value", "expected_value", "expectation"),
    (
        *((empty_val, None, does_not_raise()) for empty_val in EMPTY_VALUES),
        ((EXPECTED_IPV4_RANGE,), (EXPECTED_IPV4_RANGE,), does_not_raise()),
        ((EXPECTED_IPV6_RANGE,), (EXPECTED_IPV6_RANGE,), does_not_raise()),
        ((EXPECTED_IPV4_PREFIX,), (EXPECTED_IPV4_PREFIX,), does_not_raise()),
        ((EXPECTED_IPV6_PREFIX,), (EXPECTED_IPV6_PREFIX,), does_not_raise()),
        ("10.26.40.1-10.26.40.16", [EXPECTED_IPV4_RANGE], does_not_raise()),
        (
            "2800:6D61:676E:6574::1-2800:6D61:676E:6574::2640",
            [EXPECTED_IPV6_RANGE],
            does_not_raise(),
        ),
        ("10.26.40.0/24", [EXPECTED_IPV4_PREFIX], does_not_raise()),
        ("2800:6D61:676E:6574::/64", [EXPECTED_IPV6_PREFIX], does_not_raise()),
        (
            (
                "10.26.40.0/24\n"
                "2800:6D61:676E:6574::/64\n"
                "10.40.26.0-10.40.26.40\n"
                "2800:6D61:676E:6574::0-2800:6D61:676E:6574::2640"
            ),
            [
                ipaddress.IPv4Network("10.26.40.0/24"),
                ipaddress.IPv6Network("2800:6D61:676E:6574::/64"),
                IPv4Range(
                    ipaddress.IPv4Address("10.40.26.0"),
                    ipaddress.IPv4Address("10.40.26.40"),
                ),
                IPv6Range(
                    ipaddress.IPv6Address("2800:6D61:676E:6574::0"),
                    ipaddress.IPv6Address("2800:6D61:676E:6574::2640"),
                ),
            ],
            does_not_raise(),
        ),
    ),
    ids=[
        *(f"empty-{n}" for n, _ in enumerate(EMPTY_VALUES)),
        "ipv4-range-tuple",
        "ipv6-range-tuple",
        "ipv4-prefix-tuple",
        "ipv6-prefix-tuple",
        "single-ipv4-range-str",
        "single-ipv6-range-str",
        "single-ipv4-prefix-str",
        "single-ipv6-prefix-str",
        "multiple-mixed-range-str",
    ],
)
def test_parse_ip_network_value(raw_value, expected_value, expectation):
    with expectation:
        assert parse_ip_network_value(raw_value, True) == expected_value
