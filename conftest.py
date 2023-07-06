import pytest


@pytest.fixture(scope="session", autouse=True)
def faker_session_locale():
    return ["es_CL"]


# To make fixtures available to all test functions, add them here.
pytest_plugins = [
    "base.fixtures",
    "users.fixtures",
]
