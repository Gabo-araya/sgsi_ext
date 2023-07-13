import ipaddress

from ipaddress import IPv4Address
from ipaddress import IPv6Address

import pytest

from parameters.utils.ip import IPv4Range
from parameters.utils.ip import IPv6Range


@pytest.mark.parametrize(
    ("addr_range", "expected_repr"),
    (
        (
            IPv4Range("10.26.40.1", "10.26.40.127"),
            "IPv4Range('10.26.40.1', '10.26.40.127')",
        ),
        (
            IPv6Range("2800:6d61:676e:6574::", "2800:6d61:676e:6574::00ff"),
            "IPv6Range('2800:6d61:676e:6574::', '2800:6d61:676e:6574::ff')",
        ),
    ),
    ids=("v4", "v6"),
)
def test_addressrange_repr(addr_range, expected_repr):
    assert repr(addr_range) == expected_repr


@pytest.mark.parametrize(
    ("addr_range", "expected_str"),
    (
        (
            IPv4Range("10.26.40.1", "10.26.40.127"),
            "10.26.40.1-10.26.40.127",
        ),
        (
            IPv6Range("2800:6d61:676e:6574::", "2800:6d61:676e:6574::00ff"),
            "2800:6d61:676e:6574::-2800:6d61:676e:6574::ff",
        ),
    ),
    ids=("v4", "v6"),
)
def test_addressrange_str(addr_range, expected_str):
    assert str(addr_range) == expected_str


@pytest.mark.parametrize(
    ("addr_range", "address", "expected_value"),
    (
        (IPv4Range("10.26.40.1", "10.26.40.127"), IPv4Address("10.26.40.1"), True),
        (IPv4Range("10.26.40.1", "10.26.40.127"), IPv4Address("10.26.40.10"), True),
        (IPv4Range("10.26.40.1", "10.26.40.127"), IPv4Address("10.26.40.127"), True),
        (IPv4Range("10.26.40.1", "10.26.40.127"), IPv4Address("10.26.40.0"), False),
        (IPv4Range("10.26.40.1", "10.26.40.127"), IPv4Address("10.26.40.128"), False),
        (IPv4Range("10.26.40.1", "10.26.40.127"), IPv4Address("10.26.38.5"), False),
        (IPv4Range("10.26.40.1", "10.26.40.127"), IPv4Address("10.26.41.5"), False),
    ),
)
def test_addressrange_contains_v4(addr_range, address, expected_value):
    assert (address in addr_range) == expected_value


@pytest.mark.parametrize(
    ("addr_range", "address", "expected_value"),
    (
        (
            IPv6Range("2800:6d61:676e:6574::1", "2800:6d61:676e:6574::00ff"),
            IPv6Address("2800:6d61:676e:6574::1"),
            True,
        ),
        (
            IPv6Range("2800:6d61:676e:6574::1", "2800:6d61:676e:6574::00ff"),
            IPv6Address("2800:6d61:676e:6574::00ff"),
            True,
        ),
        (
            IPv6Range("2800:6d61:676e:6574::1", "2800:6d61:676e:6574::00ff"),
            IPv6Address("2800:6d61:676e:6574::007f"),
            True,
        ),
        (
            IPv6Range("2800:6d61:676e:6574::1", "2800:6d61:676e:6574::00ff"),
            IPv6Address("2800:6d61:676e:6574::"),
            False,
        ),
        (
            IPv6Range("2800:6d61:676e:6574::1", "2800:6d61:676e:6574::00ff"),
            IPv6Address("2800:6d61:676e:6574::ffff"),
            False,
        ),
        (
            IPv6Range("2800:6d61:676e:6574::1", "2800:6d61:676e:6574::00ff"),
            IPv6Address("2800:6d61:676e:6573::ffff"),
            False,
        ),
        (
            IPv6Range("2800:6d61:676e:6574::1", "2800:6d61:676e:6574::00ff"),
            IPv6Address("2800:6d61:676e:6575::"),
            False,
        ),
    ),
)
def test_addressrange_contains_v6(addr_range, address, expected_value):
    assert (address in addr_range) == expected_value


def test_addressrange_contains_mixed_should_fail_v4():
    addr_range = IPv4Range("10.26.40.1", "10.26.40.127")
    with pytest.raises(TypeError):
        assert IPv6Address("64:ff9b::a1a:2801") in addr_range


def test_addressrange_contains_mixed_should_fail_v6():
    addr_range = IPv6Range("64:ff9b::a1a:2801", "64:ff9b::a1a:28ff")
    with pytest.raises(TypeError):
        assert IPv4Address("10.26.40.10") in addr_range


@pytest.mark.parametrize(
    ("range_class", "range_start", "range_end", "exc_class"),
    (
        (IPv4Range, "10.26.40.10", "10.26.40.1", ValueError),
        (IPv6Range, "64:ff9b::a1a:28ff", "64:ff9b::a1a:2801", ValueError),
        (IPv4Range, "10.26.40.1", "64:ff9b::a1a:28ff", ipaddress.AddressValueError),
        (
            IPv4Range,
            IPv4Address("10.26.40.1"),
            IPv6Address("64:ff9b::a1a:28ff"),
            TypeError,
        ),
        (IPv6Range, "10.26.40.1", "64:ff9b::a1a:28ff", ipaddress.AddressValueError),
        (
            IPv6Range,
            IPv4Address("10.26.40.1"),
            IPv6Address("64:ff9b::a1a:28ff"),
            TypeError,
        ),
    ),
)
def test_addressrange_incorrect_initialization(
    range_class, range_start, range_end, exc_class
):
    with pytest.raises(exc_class):
        range_class(range_start, range_end)
