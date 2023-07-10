from http import HTTPStatus

from django.conf import settings
from django.urls import NoReverseMatch
from django.urls import reverse
from django.urls.converters import SlugConverter

import pytest

from inflection import underscore

from base.utils import get_our_models
from base.utils import get_slug_fields

EXCLUDED_NAMESPACES = [
    *settings.URLS_TEST_IGNORED_NAMESPACES,
]


class SkipUrl(Exception):  # noqa: N818
    pass


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


def get_url_using_param_names(  # noqa: C901, PLR0912
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
            try:
                params["pk"] = default_parameter_values[f"{model_name}_id"]
                obj = default_objects[model_name]
            except KeyError:
                raise SkipUrl from KeyError
        elif isinstance(converter, SlugConverter) and hasattr(callback, "view_class"):
            model_name = underscore(callback.view_class.model.__name__)
            try:
                params[param_name] = default_parameter_values[
                    f"{model_name}_{param_name}_slug"
                ]
                obj = default_objects[model_name]
            except KeyError:
                raise SkipUrl from KeyError
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
    superuser_user, superuser_client, default_objects, default_parameter_values
):
    """Test all URLs."""

    from django.contrib import admin

    from project.urls import urlpatterns

    skipped_patterns = []

    def test_url_patterns(tested_patterns, namespace=None):
        if namespace in EXCLUDED_NAMESPACES:
            return

        for pattern in tested_patterns:
            if hasattr(pattern, "name"):
                try:
                    url = reverse_urlpattern(
                        pattern, namespace, default_objects, default_parameter_values
                    )
                except SkipUrl:
                    skipped_patterns.append(pattern)
                    continue

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

    assert not skipped_patterns, (
        "Skipped URL patterns due to missing fixtures:\n"
        + "\n".join(f"* {pattern.pattern.describe()}" for pattern in skipped_patterns)
        + "\nAdd them to base.tests.conftest.default_objects."
    )


def test_all_fixtures_are_defined(default_objects):
    models = tuple(get_our_models())
    models_without_fixtures = []

    def test_url_patterns(patterns):
        for pat in patterns:
            if hasattr(pat, "name"):
                param_converter_name = pat.pattern.converters.items()
                if not param_converter_name:
                    continue

                callback = pat.callback
                for param_name, converter in param_converter_name:
                    if hasattr(callback, "view_class") and (
                        param_name == "pk" or isinstance(converter, SlugConverter)
                    ):
                        model_class = callback.view_class.model
                        model_name = underscore(model_class.__name__)
                        if model_class not in models:
                            continue
                        if model_name not in default_objects:
                            models_without_fixtures.append(model_class)
            else:
                test_url_patterns(pat.url_patterns)

    from project.urls import urlpatterns

    test_url_patterns(urlpatterns)
    assert not models_without_fixtures, (
        "Found model(s) without defined test fixture(s): \n"
        + "\n".join(
            f"* {model._meta.app_label}.{model.__name__}"
            for model in models_without_fixtures
        )
        + "\nAdd them to base.tests.conftest.default_objects."
    )
