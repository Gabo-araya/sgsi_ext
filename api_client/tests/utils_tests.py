from contextlib import contextmanager

import pytest

from api_client.services.client.errors import InvalidCallbackError
from api_client.services.client.utils import validate_callback


@contextmanager
def does_not_raise():
    yield


def callback_to_check(response, error):
    return


class CallbackCheck:
    def callback(self, response, error):
        pass


uncallable_callback = "not_callable"
callback_check_instance = CallbackCheck()


@pytest.mark.parametrize(
    ("cb", "expectation"),
    (
        (callback_to_check, does_not_raise()),
        (uncallable_callback, pytest.raises(InvalidCallbackError)),
        (callback_check_instance.callback, pytest.raises(InvalidCallbackError)),
        (lambda a, b: None, pytest.raises(InvalidCallbackError)),
    ),
    ids=("valid-function", "non-callable", "instance-method", "lambda"),
)
def test_validate_callback(cb, expectation):
    with expectation:
        validate_callback(cb)
