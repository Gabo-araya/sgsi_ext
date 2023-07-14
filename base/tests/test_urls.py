import datetime

from http import HTTPStatus

from django.conf import settings
from django.db.models import Model
from django.urls import NoReverseMatch
from django.urls import reverse
from django.urls.converters import SlugConverter

import pytest
import pytz

from inflection import underscore

from base.fixtures import MODEL_FIXTURE_CUSTOM_NAMES
from base.utils import get_our_models
from base.utils import get_slug_fields

EXCLUDED_NAMESPACES = [
    *settings.URLS_TEST_IGNORED_NAMESPACES,
]


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


def get_url_using_param_names(
    url_pattern,
    namespace,
    default_objects,
    default_parameter_values,
):
    """
    Using the dictionary of parameters defined on ``default_parameter_values`` and the
    list of objects defined on ``default_objects``, construct urls with valid params.

    This method assumes that nested urls name their parents ids as ``{model}_id``

    Thus something like the comments of a user should be in the format of
    ``/users/{user_id}/comments/``
    """
    param_converter_name = url_pattern.pattern.converters.items()

    params = {}
    if not param_converter_name:
        return None

    callback = url_pattern.callback

    obj = None

    for param_name, converter in param_converter_name:
        if param_name == "pk" and hasattr(callback, "view_class"):
            model_name = underscore(callback.view_class.model.__name__)
            params["pk"] = default_parameter_values[f"{model_name}_id"]
            obj = default_objects[model_name]
        elif isinstance(converter, SlugConverter) and hasattr(callback, "view_class"):
            model_name = underscore(callback.view_class.model.__name__)
            params[param_name] = default_parameter_values[
                f"{model_name}_{param_name}_slug"
            ]
            obj = default_objects[model_name]
        else:
            try:
                params[param_name] = default_parameter_values[param_name]
            except KeyError:
                return None

    if obj:
        # if the object has an attribute named as the parameter
        # assume it should be used on the url, since many views
        # filter nested objects
        for param in params:
            if hasattr(obj, param) and getattr(obj, param):
                params[param] = getattr(obj, param)

    return reverse_pattern(url_pattern, namespace, kwargs=params)


def reverse_pattern(pattern, namespace, args=None, kwargs=None):
    try:
        if namespace:
            return reverse(f"{namespace}:{pattern.name}")
        return reverse(pattern.name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        return None


def reverse_urlpattern(
    url_pattern, namespace, default_objects, default_parameter_values
):
    url = get_url_using_param_names(
        url_pattern, namespace, default_objects, default_parameter_values
    )
    if url:
        return url

    param_names = url_pattern.pattern.regex.groupindex.keys()
    url_params = {}

    for param in param_names:
        try:
            url_params[param] = default_parameter_values[param]
        except KeyError:
            url_params[param] = 1

    return reverse_pattern(url_pattern, namespace, kwargs=url_params)


@pytest.mark.slow
@pytest.mark.django_db(transaction=True, databases=["default", "logs"])
def test_responses(
    superuser_user,
    superuser_client,
    default_objects,
    extra_objects,
    default_parameter_values,
):
    """Test all URLs."""

    from django.contrib import admin

    from project.urls import urlpatterns

    def test_url_patterns(tested_patterns, namespace=None):
        if namespace in EXCLUDED_NAMESPACES:
            return

        for pattern in tested_patterns:
            if hasattr(pattern, "name"):
                url = reverse_urlpattern(
                    pattern, namespace, default_objects, default_parameter_values
                )

                if not url:
                    continue

                try:
                    superuser_client.force_login(superuser_user)
                    response = superuser_client.get(url)
                except Exception:
                    raise

                msg = f'url "{url}" ({pattern.name}) returned {response.status_code}'
                assert response.status_code in (
                    HTTPStatus.OK,  # 200
                    HTTPStatus.FOUND,  # 302
                    HTTPStatus.FORBIDDEN,  # 403
                    HTTPStatus.METHOD_NOT_ALLOWED,  # 405
                ), msg

            else:
                test_url_patterns(pattern.url_patterns, pattern.namespace)

    test_url_patterns(urlpatterns)
    for _, model_admin in admin.site._registry.items():
        patterns = model_admin.get_urls()
        test_url_patterns(patterns, namespace="admin")
