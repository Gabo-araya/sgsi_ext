from http import HTTPStatus

from django.contrib import admin
from django.urls import NoReverseMatch
from django.urls import reverse
from django.urls.converters import SlugConverter

from inflection import underscore

from base.tests import BaseTestCase
from base.utils import get_our_models
from base.utils import get_slug_fields
from base.utils import random_string
from project.urls import urlpatterns


def reverse_pattern(pattern, namespace, args=None, kwargs=None):
    try:
        if namespace:
            return reverse(f"{namespace}:{pattern.name}")
        return reverse(pattern.name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        return None


class UrlsTest(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        # create a superuser account
        cls.password = random_string()
        cls.user = cls.mockup.create_user(
            password=cls.password,
            is_superuser=True,
        )

    def setUp(self):
        super().setUp()

        # store default values for urls. E.g. user_id
        self.default_params = {}

        # store default objects to get foreign key parameters
        self.default_objects = {}

        for model in get_our_models():
            model_name = underscore(model.__name__)
            method_name = f"create_{model_name}"

            # store the created object
            obj = getattr(self.mockup, method_name)(**self.get_obj_kwargs(model))
            self.default_objects[model_name] = obj

            self.assertIsNotNone(obj, f"{method_name} returns None")

            # store the object id with the expected name a url should use
            # when using object ids:
            param_name = f"{model_name}_id"
            self.default_params[param_name] = obj.id
            for slug_field in get_slug_fields(model):
                value = getattr(obj, slug_field.name)
                param_name = f"{model_name}_{slug_field.name}_slug"
                self.default_params[param_name] = value

    def get_obj_kwargs(self, model):
        """
        When testing all urls, there are business logic that require certain
        values on the objects we are creating. This method returns a kwrags
        diciontary to be passed to the create_X method that creaates an
        instance of model.

        For example, imagine that APP has the url /message/1/
        It is reasonable that the view will return 404 if the logged in user
        has no nothing to do with.
        This method will be called when creating the test objects to be used
        on the UrlsTest, in our example a solution would be to return a
        dictionary where the user is the logged in user
        return {"user": self.user}
        """
        return {}

    def get_url_using_param_names(self, url_pattern, namespace):
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
                params["pk"] = self.default_params[f"{model_name}_id"]
                obj = self.default_objects[model_name]
            elif isinstance(converter, SlugConverter) and hasattr(
                callback,
                "view_class",
            ):
                model_name = underscore(url_pattern.callback.view_class.model.__name__)
                params[param_name] = self.default_params[
                    f"{model_name}_{param_name}_slug"
                ]
                obj = self.default_objects[model_name]
            else:
                try:
                    params[param_name] = self.default_params[param_name]
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

    def reverse_pattern(self, url_pattern, namespace):
        url = self.get_url_using_param_names(url_pattern, namespace)
        if url:
            return url

        param_names = url_pattern.pattern.regex.groupindex.keys()
        url_params = {}

        for param in param_names:
            try:
                url_params[param] = self.default_params[param]
            except KeyError:
                url_params[param] = 1

        return reverse_pattern(url_pattern, namespace, kwargs=url_params)

    def test_responses(self):

        ignored_namespaces = [
            "admin",
        ]

        def test_url_patterns(patterns, namespace=""):

            if namespace in ignored_namespaces:
                return

            for pattern in patterns:
                self.login()

                if hasattr(pattern, "name"):
                    url = self.reverse_pattern(pattern, namespace)

                    if not url:
                        continue

                    try:
                        response = self.client.get(url)
                    except Exception:
                        print(f"Url {url} failed: ")  # noqa: T201
                        raise

                    msg = 'url "{}" ({})returned {}'.format(
                        url,
                        pattern.name,
                        response.status_code,
                    )
                    self.assertIn(
                        response.status_code,
                        (
                            HTTPStatus.OK,  # 200
                            HTTPStatus.FOUND,  # 302
                            HTTPStatus.FORBIDDEN,  # 403
                            HTTPStatus.METHOD_NOT_ALLOWED,  # 405
                        ),
                        msg,
                    )
                else:
                    test_url_patterns(pattern.url_patterns, pattern.namespace)

        test_url_patterns(urlpatterns)

        for _, model_admin in admin.site._registry.items():
            patterns = model_admin.get_urls()
            test_url_patterns(patterns, namespace="admin")
