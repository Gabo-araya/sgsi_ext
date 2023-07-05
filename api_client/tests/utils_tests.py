from contextlib import nullcontext as does_not_raise

import pytest

from api_client.services.client.errors import InvalidCallbackError
from api_client.services.client.utils import validate_callback
from api_client.services.client.utils import validate_nonblocking_callbacks


def callback_to_check(response, error):
    return


class CallbackCheck:
    def callback(self, response, error):
        pass


uncallable_callback = "not_callable"
callback_check_instance = CallbackCheck()


@pytest.mark.parametrize(
    ("callback", "expectation"),
    (
        (callback_to_check, does_not_raise()),
        (uncallable_callback, pytest.raises(InvalidCallbackError)),
        (callback_check_instance.callback, pytest.raises(InvalidCallbackError)),
        (lambda a, b: None, pytest.raises(InvalidCallbackError)),
    ),
    ids=("valid-function", "non-callable", "instance-method", "lambda"),
)
def test_validate_callback(callback, expectation):
    with expectation:
        validate_callback(callback)


@pytest.mark.parametrize(
    ("on_success", "on_error", "expectation"),
    (
        (callback_to_check, callback_to_check, does_not_raise()),
        (uncallable_callback, callback_to_check, pytest.raises(InvalidCallbackError)),
        (callback_to_check, uncallable_callback, pytest.raises(InvalidCallbackError)),
        (uncallable_callback, uncallable_callback, pytest.raises(InvalidCallbackError)),
    ),
)
def test_validate_nonblocking_callbacks(on_success, on_error, expectation):
    with expectation:
        validate_nonblocking_callbacks(on_success, on_error)
