import pytest


@pytest.mark.django_db(databases=["default", "logs"])
def test_old_client_log_queryset(client_log_queryset, settings):
    settings.API_CLIENT_LOG_MAX_AGE_DAYS = 1
    assert client_log_queryset.old().count() == 1
