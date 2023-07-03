import datetime
import ipaddress

from contextlib import contextmanager

from django.core import validators
from django.core.exceptions import ValidationError

# base
from base.tests import BaseTestCase
from base.utils import random_string

# enums
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


@contextmanager
def does_not_raise():
    yield


class ParameterTestCase(BaseTestCase):
    def test_create_all_parammeters(self):
        Parameter.create_all_parameters()
        self.assertEqual(
            len(ParameterDefinitionList.definitions),
            Parameter.objects.count(),
        )

    def test_parse_str_value(self):
        for value in validators.EMPTY_VALUES:
            self.assertIsNone(parse_str_value(value))
        for _ in range(3):
            value = random_string()
            self.assertEqual(parse_str_value(value), value)

    def test_parse_int_value(self):
        for value in validators.EMPTY_VALUES:
            self.assertIsNone(parse_int_value(value))
        space = " "
        self.assertIsNone(parse_int_value(space))
        int_with_space = "1 "
        self.assertEqual(parse_int_value(int_with_space), 1)
        int_with_space = " 1"
        self.assertEqual(parse_int_value(int_with_space), 1)
        int_with_space = " 1 "
        self.assertEqual(parse_int_value(int_with_space), 1)
        # TODO: test for strings, could not figure out what 'sanitize_separators' does

    def test_parse_bool_value(self):
        for value in validators.EMPTY_VALUES:
            self.assertIsNone(parse_bool_value(value))

        values_to_test = (
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
            ("x", None, self.assertRaises(ValidationError)),
        )

        for raw_value, expected_value, expectation in values_to_test:
            with expectation:
                self.assertEqual(parse_bool_value(raw_value), expected_value)

    def test_parse_date_value(self):
        expected_date = datetime.date(2007, 1, 9)

        for value in validators.EMPTY_VALUES:
            self.assertIsNone(parse_date_value(value))

        values_to_test = (
            ("2007-01-09  ", expected_date, does_not_raise()),
            (" 2007-01-09 ", expected_date, does_not_raise()),
            ("  2007-01-09", expected_date, does_not_raise()),
            (datetime.date(2007, 1, 9), expected_date, does_not_raise()),
            (
                datetime.datetime(2007, 1, 9, 9, 41),  # noqa: DTZ001
                expected_date,
                does_not_raise(),
            ),
            (" ", None, self.assertRaises(ValidationError)),
            ("x", None, self.assertRaises(ValidationError)),
        )

        for raw_value, expected_value, expectation in values_to_test:
            with expectation:
                self.assertEqual(parse_date_value(raw_value), expected_value)

    def test_parse_time_value(self):
        expected_time = datetime.time(9, 41)

        for value in validators.EMPTY_VALUES:
            self.assertIsNone(parse_time_value(value))

        values_to_test = (
            ("09:41  ", expected_time, does_not_raise()),
            (" 09:41 ", expected_time, does_not_raise()),
            ("  09:41", expected_time, does_not_raise()),
            (datetime.time(9, 41), expected_time, does_not_raise()),
            (" ", None, self.assertRaises(ValidationError)),
            ("x", None, self.assertRaises(ValidationError)),
        )

        for raw_value, expected_value, expectation in values_to_test:
            with expectation:
                self.assertEqual(parse_time_value(raw_value), expected_value)

    def test_parse_url_value(self):
        for value in validators.EMPTY_VALUES:
            self.assertIsNone(parse_url_value(value))

        values_to_test = (
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
            ("www.magnet.cl", "www.magnet.cl", self.assertRaises(ValidationError)),
            ("magnet.cl", "magnet.cl", self.assertRaises(ValidationError)),
            ("x", None, self.assertRaises(ValidationError)),
        )

        for raw_value, expected_value, expectation in values_to_test:
            with expectation:
                self.assertEqual(parse_url_value(raw_value), expected_value)

    def test_parse_json_value_python_values(self):
        for value in validators.EMPTY_VALUES:
            self.assertIsNone(parse_json_value(value))

        values_to_test = (
            (123, 123, does_not_raise()),
            (1.234, 1.234, does_not_raise()),
            (True, True, does_not_raise()),
            ([1, 2, 3], [1, 2, 3], does_not_raise()),
            (
                {"a": 1, "b": True, "c": [1, 2]},
                {"a": 1, "b": True, "c": [1, 2]},
                does_not_raise(),
            ),
        )

        for raw_value, expected_value, expectation in values_to_test:
            with expectation:
                self.assertEqual(parse_json_value(raw_value), expected_value)

    def test_parse_json_value(self):
        values_to_test = (
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
            ("{a: 123}", None, self.assertRaises(ValidationError)),
        )

        for raw_value, expected_value, expectation in values_to_test:
            with expectation:
                self.assertEqual(parse_json_value(raw_value), expected_value)

    def test_parse_single_hostname_value(self):
        for value in validators.EMPTY_VALUES:
            self.assertIsNone(parse_single_hostname_value(value))

        values_to_test = (
            ("  ", "", does_not_raise()),
            ("magnet.cl", "magnet.cl", does_not_raise()),
            ("www.magnet.cl", "www.magnet.cl", does_not_raise()),
            ("d3pt.dev.magnet.cl", "d3pt.dev.magnet.cl", does_not_raise()),
            ("8.8.8.8", "8.8.8.8", does_not_raise()),
            ("[::1]", "[::1]", does_not_raise()),
            ("ñandú.cl", "ñandú.cl", does_not_raise()),
            ("256.1.562.6", None, self.assertRaises(ValidationError)),
        )

        for raw_value, expected_value, expectation in values_to_test:
            with expectation:
                self.assertEqual(parse_single_hostname_value(raw_value), expected_value)

    def test_parse_hostname_value(self):
        for value in validators.EMPTY_VALUES:
            self.assertIsNone(parse_hostname_value(value, multiple=False))
            self.assertIsNone(parse_hostname_value(value, multiple=True))

        values_to_test = (
            ("  ", False, None, does_not_raise()),
            ("magnet.cl", False, "magnet.cl", does_not_raise()),
            (
                "magnet.cl\nwww.magnet.cl",
                False,
                None,
                self.assertRaises(ValidationError),
            ),
            ("256.1.562.6", False, None, self.assertRaises(ValidationError)),
            ("   ", True, [], does_not_raise()),
            ("magnet.cl", True, ["magnet.cl"], does_not_raise()),
            (
                "magnet.cl\nwww.magnet.cl",
                True,
                ["magnet.cl", "www.magnet.cl"],
                does_not_raise(),
            ),
            ("256.1.562.6", True, None, self.assertRaises(ValidationError)),
        )

        for raw_value, multiple, expected_value, expectation in values_to_test:
            with expectation:
                self.assertEqual(
                    parse_hostname_value(raw_value, multiple), expected_value
                )

    def test_parse_ip_address_value(self):
        for value in validators.EMPTY_VALUES:
            self.assertIsNone(parse_ip_address_value(value))

        values_to_test = (
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
            ("256.257.258.1", None, self.assertRaises(ValidationError)),
            ("::fffff", None, self.assertRaises(ValidationError)),
        )

        for raw_value, expected_value, expectation in values_to_test:
            with expectation:
                self.assertEqual(parse_ip_address_value(raw_value), expected_value)

    def test_parse_ip_prefix_value(self):
        expected_ipv4_prefix = ipaddress.IPv4Network("10.26.40.0/24")
        expected_ipv6_prefix = ipaddress.IPv6Network("2800:6D61:676E:6574::/64")

        for value in validators.EMPTY_VALUES:
            self.assertIsNone(parse_ip_prefix_value(value))

        values_to_test = (
            (expected_ipv4_prefix, expected_ipv4_prefix, does_not_raise()),
            (expected_ipv6_prefix, expected_ipv6_prefix, does_not_raise()),
            ("10.26.40.0/24", expected_ipv4_prefix, does_not_raise()),
            ("2800:6D61:676E:6574::/64", expected_ipv6_prefix, does_not_raise()),
            ("   10.26.40.0/24", expected_ipv4_prefix, does_not_raise()),
            ("2800:6D61:676E:6574::/64   ", expected_ipv6_prefix, does_not_raise()),
            ("320.0.0.0/36", None, self.assertRaises(ValidationError)),
            ("fffff::/128", None, self.assertRaises(ValidationError)),
        )

        for raw_value, expected_value, expectation in values_to_test:
            with expectation:
                self.assertEqual(parse_ip_prefix_value(raw_value), expected_value)

    def test_parse_ip_range_value(self):
        expected_ipv4_range = IPv4Range(
            ipaddress.IPv4Address("10.26.40.1"),
            ipaddress.IPv4Address("10.26.40.16"),
        )
        expected_ipv4_range_same = IPv4Range(
            ipaddress.IPv4Address("10.26.40.1"),
            ipaddress.IPv4Address("10.26.40.1"),
        )
        expected_ipv6_range = IPv6Range(
            ipaddress.IPv6Address("2800:6D61:676E:6574::1"),
            ipaddress.IPv6Address("2800:6D61:676E:6574::2640"),
        )
        expected_ipv6_range_same = IPv6Range(
            ipaddress.IPv6Address("2800:6D61:676E:6574::1"),
            ipaddress.IPv6Address("2800:6D61:676E:6574::1"),
        )

        for value in validators.EMPTY_VALUES:
            self.assertIsNone(parse_ip_range_value(value))

        values_to_test = (
            (expected_ipv4_range, expected_ipv4_range, does_not_raise()),
            (expected_ipv6_range, expected_ipv6_range, does_not_raise()),
            (
                "10.26.40.1-10.26.40.16",
                expected_ipv4_range,
                does_not_raise(),
            ),
            (
                "2800:6D61:676E:6574::1-2800:6D61:676E:6574::2640",
                expected_ipv6_range,
                does_not_raise(),
            ),
            (
                "10.26.40.1",
                expected_ipv4_range_same,
                does_not_raise(),
            ),
            (
                "2800:6D61:676E:6574::1",
                expected_ipv6_range_same,
                does_not_raise(),
            ),
            (
                "10.26.40.1-10.26.40.1",
                expected_ipv4_range_same,
                does_not_raise(),
            ),
            (
                "2800:6D61:676E:6574::1-2800:6D61:676E:6574::1",
                expected_ipv6_range_same,
                does_not_raise(),
            ),
            (
                "10.26.40.16-10.26.40.1",
                None,
                self.assertRaises(ValidationError),
            ),
            (
                "10.26.40.1-10.26.40.1-10.26.40.3",
                expected_ipv4_range_same,
                self.assertRaises(ValidationError),
            ),
            (
                "2800:6D61:676E:6574::ffff-2800:6D61:676E:6574::0",
                ipaddress.IPv6Network("2800:6D61:676E:6574::/64"),
                self.assertRaises(ValidationError),
            ),
            (
                "10.26.40.16-2800:6D61:676E:6574::2640",
                None,
                self.assertRaises(ValidationError),
            ),
            ("320.0.0.0/36-384.0.0.0/36", None, self.assertRaises(ValidationError)),
            ("fffff::/128-fffff::ffff/128", None, self.assertRaises(ValidationError)),
        )

        for raw_value, expected_value, expectation in values_to_test:
            with expectation:
                self.assertEqual(parse_ip_range_value(raw_value), expected_value)

    def test_parse_single_ip_network_value(self):
        expected_ipv4_range = IPv4Range(
            ipaddress.IPv4Address("10.26.40.1"),
            ipaddress.IPv4Address("10.26.40.16"),
        )
        expected_ipv6_range = IPv6Range(
            ipaddress.IPv6Address("2800:6D61:676E:6574::1"),
            ipaddress.IPv6Address("2800:6D61:676E:6574::2640"),
        )
        expected_ipv4_prefix = ipaddress.IPv4Network("10.26.40.0/24")
        expected_ipv6_prefix = ipaddress.IPv6Network("2800:6D61:676E:6574::/64")

        for value in validators.EMPTY_VALUES:
            self.assertIsNone(parse_single_ip_network_value(value))

        values_to_test = (
            (expected_ipv4_range, expected_ipv4_range, does_not_raise()),
            (expected_ipv6_range, expected_ipv6_range, does_not_raise()),
            (expected_ipv4_prefix, expected_ipv4_prefix, does_not_raise()),
            (expected_ipv6_prefix, expected_ipv6_prefix, does_not_raise()),
            ("10.26.40.1-10.26.40.16", expected_ipv4_range, does_not_raise()),
            (
                "2800:6D61:676E:6574::1-2800:6D61:676E:6574::2640",
                expected_ipv6_range,
                does_not_raise(),
            ),
            ("10.26.40.0/24", expected_ipv4_prefix, does_not_raise()),
            ("2800:6D61:676E:6574::/64", expected_ipv6_prefix, does_not_raise()),
        )

        for raw_value, expected_value, expectation in values_to_test:
            with expectation:
                self.assertEqual(
                    parse_single_ip_network_value(raw_value), expected_value
                )

    def test_parse_ip_network_value_single(self):
        expected_ipv4_range = IPv4Range(
            ipaddress.IPv4Address("10.26.40.1"),
            ipaddress.IPv4Address("10.26.40.16"),
        )
        expected_ipv6_range = IPv6Range(
            ipaddress.IPv6Address("2800:6D61:676E:6574::1"),
            ipaddress.IPv6Address("2800:6D61:676E:6574::2640"),
        )
        expected_ipv4_prefix = ipaddress.IPv4Network("10.26.40.0/24")
        expected_ipv6_prefix = ipaddress.IPv6Network("2800:6D61:676E:6574::/64")

        for value in validators.EMPTY_VALUES:
            self.assertIsNone(parse_ip_network_value(value))

        values_to_test = (
            (expected_ipv4_range, expected_ipv4_range, does_not_raise()),
            (expected_ipv6_range, expected_ipv6_range, does_not_raise()),
            (expected_ipv4_prefix, expected_ipv4_prefix, does_not_raise()),
            (expected_ipv6_prefix, expected_ipv6_prefix, does_not_raise()),
            ("10.26.40.1-10.26.40.16", expected_ipv4_range, does_not_raise()),
            (
                "2800:6D61:676E:6574::1-2800:6D61:676E:6574::2640",
                expected_ipv6_range,
                does_not_raise(),
            ),
            ("10.26.40.0/24", expected_ipv4_prefix, does_not_raise()),
            ("2800:6D61:676E:6574::/64", expected_ipv6_prefix, does_not_raise()),
        )

        for raw_value, expected_value, expectation in values_to_test:
            with expectation:
                self.assertEqual(parse_ip_network_value(raw_value), expected_value)

    def test_parse_ip_network_value(self):
        expected_ipv4_range = IPv4Range(
            ipaddress.IPv4Address("10.26.40.1"),
            ipaddress.IPv4Address("10.26.40.16"),
        )
        expected_ipv6_range = IPv6Range(
            ipaddress.IPv6Address("2800:6D61:676E:6574::1"),
            ipaddress.IPv6Address("2800:6D61:676E:6574::2640"),
        )
        expected_ipv4_prefix = ipaddress.IPv4Network("10.26.40.0/24")
        expected_ipv6_prefix = ipaddress.IPv6Network("2800:6D61:676E:6574::/64")

        for value in validators.EMPTY_VALUES:
            self.assertIsNone(parse_ip_network_value(value))

        values_to_test = (
            ((expected_ipv4_range,), (expected_ipv4_range,), does_not_raise()),
            ((expected_ipv6_range,), (expected_ipv6_range,), does_not_raise()),
            ((expected_ipv4_prefix,), (expected_ipv4_prefix,), does_not_raise()),
            ((expected_ipv6_prefix,), (expected_ipv6_prefix,), does_not_raise()),
            ("10.26.40.1-10.26.40.16", [expected_ipv4_range], does_not_raise()),
            (
                "2800:6D61:676E:6574::1-2800:6D61:676E:6574::2640",
                [expected_ipv6_range],
                does_not_raise(),
            ),
            ("10.26.40.0/24", [expected_ipv4_prefix], does_not_raise()),
            ("2800:6D61:676E:6574::/64", [expected_ipv6_prefix], does_not_raise()),
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
        )

        for raw_value, expected_value, expectation in values_to_test:
            with expectation:
                self.assertEqual(
                    parse_ip_network_value(raw_value, True), expected_value
                )
