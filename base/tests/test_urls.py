import datetime
import re

from http import HTTPStatus

from django.conf import settings
from django.db.models import Model

import pytest
import pytz

from inflection import underscore

from base.fixtures import MODEL_FIXTURE_CUSTOM_NAMES
from base.tests.url_helper import UrlTestHelper
from base.utils import get_our_models
from base.utils import get_slug_fields

PK_PARAM_RE = re.compile(r"([a-z_]+)_(?:pk|id)")

EXCLUDED_NAMESPACES = [
    *settings.URLS_TEST_IGNORED_NAMESPACES,
]
EXCLUDED_PATTERNS = ["admin:view_on_site"]


@pytest.fixture
def default_objects(request) -> dict[str, Model]:
    """
    Return a dictionary of underscored model names to models.

    By default, it attempts to automatically build this list by traversing the models
    list and dynamically importing a fixture based on its name or a custom fixture
    as defined on base.fixtures.MODEL_FIXTURE_CUSTOM_NAMES.
    """

    objects_dict = {}

    for model_class in get_our_models():
        model_name = underscore(model_class.__name__)
        django_name = f"{model_class._meta.app_label}.{model_class.__name__}"
        # Try using custom name first, then use default name
        fixture_name = MODEL_FIXTURE_CUSTOM_NAMES.get(django_name, model_name)
        objects_dict[model_name] = request.getfixturevalue(fixture_name)

    return objects_dict


@pytest.fixture
def extra_objects(request) -> dict[str, Model]:
    """
    Same as default_objects but allows to define extra objects for external apps.
    """

    from django.contrib.admin.models import CHANGE
    from django.contrib.admin.models import LogEntry
    from django.contrib.contenttypes.models import ContentType

    user = request.getfixturevalue("staff_user")

    return {
        "log_entry": LogEntry.objects.create(
            user_id=user.pk,
            action_time=datetime.datetime(2007, 1, 9, 9, 41, tzinfo=pytz.UTC),
            content_type=ContentType.objects.get_by_natural_key("users", "user"),
            object_id=user.pk,
            action_flag=CHANGE,
        )
    }


@pytest.fixture
def default_parameter_values(default_objects):
    """Return a dictionary of parameter names to values."""

    default_params = {}

    for model_name, obj in default_objects.items():
        param_name = f"{model_name}_id"
        default_params[param_name] = obj.id
        for slug_field in get_slug_fields(obj.__class__):
            value = getattr(obj, slug_field.name)
            param_name = f"{model_name}_{slug_field.name}_slug"
            default_params[param_name] = value

    return default_params


@pytest.fixture
def extra_parameter_values(extra_objects):
    """Same as default_parameter_values but allows to define extra parameter values for
    external apps."""

    return {}


@pytest.mark.slow
@pytest.mark.django_db(transaction=True, databases=["default", "logs"])
def test_responses(
    superuser_user,
    superuser_client,
    default_objects,
    extra_objects,
    default_parameter_values,
    extra_parameter_values,
):
    """Test all URLs."""

    helper_objects = {**default_objects, **extra_objects}
    helper_params = {**default_parameter_values, **extra_parameter_values}
    url_helper = UrlTestHelper(
        excluded_namespaces=EXCLUDED_NAMESPACES,
        excluded_patterns=EXCLUDED_PATTERNS,
        default_objects=helper_objects,
        default_params=helper_params,
    )

    for url in url_helper.get_urls_to_test():
        superuser_client.force_login(superuser_user)
        response = superuser_client.get(url)

        msg = f'url "{url}" returned {response.status_code}'
        assert response.status_code in (
            HTTPStatus.OK,  # 200
            HTTPStatus.FOUND,  # 302
            HTTPStatus.FORBIDDEN,  # 403
            HTTPStatus.METHOD_NOT_ALLOWED,  # 405
        ), msg
