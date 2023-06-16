from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    import django.test.client


@pytest.fixture
def superuser_client(db, superuser_user) -> "django.test.client.Client":
    """A Django test client logged in as an admin user."""
    from django.test.client import Client

    client = Client()
    client.force_login(superuser_user)
    return client


@pytest.fixture
def staff_client(db, staff_user) -> "django.test.client.Client":
    """A Django test client logged in as an admin user."""
    from django.test.client import Client

    client = Client()
    client.force_login(staff_user)
    return client


@pytest.fixture
def regular_user_client(db, regular_user) -> "django.test.client.Client":
    """A Django test client logged in as an admin user."""
    from django.test.client import Client

    client = Client()
    client.force_login(regular_user)
    return client
