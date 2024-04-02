from __future__ import annotations

import os

from shutil import copyfile
from typing import TYPE_CHECKING

from django.core.files import File

import pytest

from base.middleware import RequestMiddleware

if TYPE_CHECKING:
    from collections.abc import Generator

    from django.test.client import Client


# If you defined fixtures for a model, but they use a non-standard name, please
# add them to the following mapping. Keys follow the `app_label.model_name` scheme.
MODEL_FIXTURE_CUSTOM_NAMES = {
    "users.User": "regular_user",
    "parameters.Parameter": "test_parameter",
}


@pytest.fixture
def superuser_client(db, superuser_user) -> Generator[Client, None, None]:
    """A Django test client logged in as an admin user."""
    from django.test.client import Client

    client = Client()
    client.force_login(superuser_user)
    yield client
    if hasattr(RequestMiddleware.thread_local, "user"):
        del RequestMiddleware.thread_local.user


@pytest.fixture
def staff_client(db, staff_user) -> Generator[Client, None, None]:
    """A Django test client logged in as an admin user."""
    from django.test.client import Client

    client = Client()
    client.force_login(staff_user)
    yield client
    if hasattr(RequestMiddleware.thread_local, "user"):
        del RequestMiddleware.thread_local.user


@pytest.fixture
def regular_user_client(db, regular_user) -> Generator[Client, None, None]:
    """A Django test client logged in as an admin user."""
    from django.test.client import Client

    client = Client()
    client.force_login(regular_user)
    yield client
    if hasattr(RequestMiddleware.thread_local, "user"):
        del RequestMiddleware.thread_local.user


@pytest.fixture
def django_file(settings) -> Generator[File, None, None]:
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)

    file_path = os.path.join(settings.BASE_DIR, "base/test_assets/gondola.jpg")
    filename = os.path.basename(file_path)

    final_path = os.path.join(settings.MEDIA_ROOT, filename)

    copyfile(file_path, final_path)

    with open(final_path, "rb") as file:
        yield File(file, name=filename)
