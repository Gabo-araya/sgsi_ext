import pytest

from base.utils import format_rut
from base.utils import validate_rut


@pytest.mark.parametrize(
    ("raw_value", "expected_value"),
    (
        ("", ""),
        ("invalidrut", ""),
        ("19", "1-9"),
        ("272", "27-2"),
        ("1031", "103-1"),
        ("11053", "1.105-3"),
        ("123501", "12.350-1"),
        ("6542786", "654.278-6"),
        ("444444444", "44.444.444-4"),
    ),
)
def test_format_rut(raw_value, expected_value):
    assert format_rut(raw_value) == expected_value


@pytest.mark.parametrize(
    "raw_value, expected_result",
    (
        ("1-9", True),
        ("27-2", True),
        ("27-1", False),
        ("103-1", True),
        ("103-K", False),
        ("1105-3", True),
        ("1105-0", False),
        ("12350-1", True),
        ("12350-5", False),
        ("654278-6", True),
        ("654278-1", False),
        ("44444444-4", True),
        ("44444444-K", False),
    ),
)
def test_validate_rut(raw_value, expected_result):
    assert validate_rut(raw_value) == expected_result
