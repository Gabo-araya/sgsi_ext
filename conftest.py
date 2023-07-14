import pytest


@pytest.fixture(scope="session", autouse=True)
def faker_session_locale():
    return ["es_CL"]


@pytest.fixture
def no_translations(settings):
    """
    Resets language to English to ensure localizable strings can be reliably compared.
    """
    settings.LANGUAGE_CODE = "en"
    return settings


# To make fixtures available to all test functions, add them here.
pytest_plugins = [
    "base.fixtures",
    "api_client.fixtures",
    "parameters.fixtures",
    "regions.fixtures",
    "users.fixtures",
]
