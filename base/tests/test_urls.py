from http import HTTPStatus

from django.conf import settings
from django.urls import NoReverseMatch
from django.urls import reverse
from django.urls.converters import SlugConverter

import pytest

from inflection import underscore

from base.utils import get_slug_fields

EXCLUDED_NAMESPACES = [
    *settings.URLS_TEST_IGNORED_NAMESPACES,
    "admin",
]


@pytest.fixture
def default_objects(regular_user):
    """
    Return a dictionary of underscore model names to models.

    Each time a model is defined, a fixture must be defined and added to the signature.
    Also, a mapping of underscored model name to fixture value must be appended.
    """
    return {
        "user": regular_user,
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
    Using the dictionary of parameters defined on self.default_params and
    the list of objects defined on self.default_objects, construct urls
    with valid parameters.

    This method assumes that nested urls name their parents ids as
    {model}_id

    Thus something like the comments of a user should be in the format of

    '/users/{user_id}/comments/'
    """
    param_converter_name = url_pattern.pattern.converters.items()

    params = {}
    if not param_converter_name:
        return None

    callback = url_pattern.callback

    obj = None

    for param_name, converter in param_converter_name:
        if param_name == "pk" and hasattr(callback, "view_class"):
            model_name = underscore(url_pattern.callback.view_class.model.__name__)
            params["pk"] = default_parameter_values[f"{model_name}_id"]
            obj = default_objects[model_name]
        elif isinstance(converter, SlugConverter) and hasattr(
            callback,
            "view_class",
        ):
            model_name = underscore(url_pattern.callback.view_class.model.__name__)
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


@pytest.mark.django_db(transaction=True)
def test_responses(
    superuser_user, superuser_client, default_objects, default_parameter_values
):
    """Test all URLs."""

    from django.contrib import admin

    from project.urls import urlpatterns

    def test_url_patterns(patterns, namespace=""):
        if namespace in EXCLUDED_NAMESPACES:
            return

        for pattern in patterns:
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
