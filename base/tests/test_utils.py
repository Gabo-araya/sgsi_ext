from contextlib import nullcontext as does_not_raise

import pytest

from base.utils import build_absolute_url_wo_req
from base.utils import format_rut
from base.utils import validate_rut


@pytest.mark.parametrize(
    ("raw_value", "expected_value", "expectation"),
    (
        ("", "", does_not_raise()),
        ("invalidrut", "", does_not_raise()),
        ("1", None, pytest.raises(ValueError)),
        ("19", "1-9", does_not_raise()),
        ("272", "27-2", does_not_raise()),
        ("1031", "103-1", does_not_raise()),
        ("11053", "1.105-3", does_not_raise()),
        ("123501", "12.350-1", does_not_raise()),
        ("6542786", "654.278-6", does_not_raise()),
        ("444444444", "44.444.444-4", does_not_raise()),
    ),
)
def test_format_rut(raw_value, expected_value, expectation):
    with expectation:
        assert format_rut(raw_value) == expected_value


@pytest.mark.parametrize(
    ("raw_value", "expected_result"),
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


@pytest.mark.parametrize(
    ("ssl_redirect", "expected"),
    ((True, "https://example.com/test"), (False, "http://example.com/test")),
)
def test_build_absolute_url_wo_req(ssl_redirect, expected, settings, db):
    settings.SECURE_SSL_REDIRECT = ssl_redirect
    assert build_absolute_url_wo_req("/test") == expected
