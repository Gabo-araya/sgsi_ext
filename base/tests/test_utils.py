import pytest

from base.utils import format_rut


@pytest.mark.parametrize(
    "rut,expected_value",
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
def test_format_rut(rut, expected_value):
    assert format_rut(rut) == expected_value
