import pytest

from base.templatetags.order_by_querystring import get_order_by_querystring


@pytest.mark.parametrize(
    ("params", "expected_ordering"),
    (
        ((("a", "b"), "b", False), "o=a&o=-b"),
        ((("a", "-b"), "b", False), "o=a&o=b"),
        ((("a", "-b"), "-b", False), "o=a&o=b"),
        ((("a", "b"), "b", True), "o=a"),
        ((("a", "b"), "c", False), "o=a&o=b&o=c"),
        ((("a", "b"), "-c", False), "o=a&o=b&o=-c"),
        ((("a", "b"), "c", True), "o=a&o=b&o=c"),
        ((("a", "b"), None, False), "o=a&o=b"),
    ),
)
def test_order_by_querystring(params, expected_ordering):
    assert get_order_by_querystring(*params) == expected_ordering
