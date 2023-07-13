import pytest
import requests

from api_client.services.client.auth import BearerAuth


@pytest.mark.parametrize(
    ("params1", "params2", "not_equal"),
    (
        (("token1",), ("token1",), False),
        (("token1",), ("token2",), True),
        (("token1",), ("token1", "Special-Type"), True),
        (("token1",), ("token2", "Bearer", "X-Auth"), True),
    ),
    ids=(
        "same-token",
        "different-token",
        "different-token-type",
        "different-header-name",
    ),
)
def test_bearer_auth_equality_comparison(params1, params2, not_equal):
    auth1 = BearerAuth(*params1)
    auth2 = BearerAuth(*params2)
    if not_equal:
        assert auth1 != auth2
    else:
        assert auth1 == auth2


def test_bearer_auth_equality_comparison_mismatch_types():
    with pytest.raises(TypeError):
        auth1 = BearerAuth("token")
        auth2 = "token"
        assert auth1 == auth2


@pytest.mark.parametrize(
    ("auth_params", "expected_header", "expected_value"),
    (
        (("token1",), "Authorization", "Bearer token1"),
        (("token1", "Special-Type"), "Authorization", "Special-Type token1"),
        (("token2", "Token", "X-Auth"), "X-Auth", "Token token2"),
    ),
    ids=(
        "token",
        "different-token-type",
        "different-header-name",
    ),
)
def test_bearer_auth_call(auth_params, expected_header, expected_value):
    auth = BearerAuth(*auth_params)
    request = requests.Request("GET", "https://testurl/", auth=auth)
    prepared_request = request.prepare()
    assert expected_header in prepared_request.headers
    assert prepared_request.headers[expected_header] == expected_value


@pytest.mark.parametrize(
    ("auth_params", "expected_dict"),
    (
        (
            ("token1",),
            {
                "auth_header": "Authorization",
                "token": "token1",
                "auth_type": "Bearer",
            },
        ),
        (
            ("token1", "Special-Type"),
            {
                "auth_header": "Authorization",
                "token": "token1",
                "auth_type": "Special-Type",
            },
        ),
        (
            ("token1", "Token", "X-Auth"),
            {
                "auth_header": "X-Auth",
                "token": "token1",
                "auth_type": "Token",
            },
        ),
    ),
    ids=(
        "token",
        "different-token-type",
        "different-header-name",
    ),
)
def test_bearer_auth_get_init_kwargs(auth_params, expected_dict):
    auth = BearerAuth(*auth_params)
    serialized = auth.get_init_kwargs()
    assert serialized == expected_dict
