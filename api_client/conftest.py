import pytest

from api_client.models import ClientLog


@pytest.fixture
def client_log():
    return ClientLog.objects.create(
        client_code="test",
        method="GET",
        url="http://example.com/test/5/",
    )
