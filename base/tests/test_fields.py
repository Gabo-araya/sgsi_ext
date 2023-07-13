from contextlib import nullcontext as does_not_raise
from datetime import date
from unittest.mock import patch

from django.core.exceptions import ValidationError

import pytest

from base.fields import ChileanRUTField
from base.fields.functions import file_path


class TestModel:
    pass


@pytest.mark.parametrize(
    ("raw_value", "expected_value", "expectation"),
    (
        ("", "", does_not_raise()),
        ("1", None, pytest.raises(ValidationError)),
        ("19", "1-9", does_not_raise()),
        ("103-1", "103-1", does_not_raise()),
        ("1105-3", "1.105-3", does_not_raise()),
        ("444444444", "44.444.444-4", does_not_raise()),
        ("48395858-7", "48.395.858-7", does_not_raise()),
        ("69.290.603-9", "69.290.603-9", does_not_raise()),
        ("44444444-K", None, pytest.raises(ValidationError)),
        ("invalidrut", None, pytest.raises(ValidationError)),
    ),
)
def test_clean_rut(raw_value, expected_value, expectation):
    field = ChileanRUTField(blank=True)
    with expectation:
        assert field.clean(raw_value, None) == expected_value


def test_file_path():
    with patch(
        "base.fields.functions.utils.today", return_value=date(2007, 1, 9)
    ), patch("base.fields.functions.uuid.uuid4", return_value="uuid"):
        assert (
            file_path(TestModel(), "testfile.txt")
            == "TestModel/2007/01/09/uuid/testfile.txt"
        )
