import re
import warnings

from collections.abc import Iterable
from re import Match
from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib.admin import ModelAdmin
from django.db.models import ForeignKey
from django.db.models import Model
from django.urls import NoReverseMatch
from django.urls import URLPattern
from django.urls import URLResolver
from django.urls import get_resolver
from django.urls import reverse
from django.urls.converters import SlugConverter

from inflection import underscore

from base.utils import get_our_models

if TYPE_CHECKING:
    from typing import Protocol

    class Converter(Protocol):
        def to_python(self, value):
            ...

        def to_url(self, value):
            ...


class SkipUrl(Exception):  # noqa: N818
    """Signals a certain URL pattern should be skipped due to missing data."""


class UrlTestHelper:
    """Helper class for the test_responses test."""

    PK_PARAM_RE = re.compile(r"([a-z_]+)_(?:pk|id)")
    SLUG_PARAM_RE = re.compile(r"(?P<model_name>[a-z]+)_(?P<field_name>[a-z_]+)")

    def __init__(
        self,
        urlconf=None,
        excluded_namespaces=None,
        excluded_patterns=None,
        pattern_overrides=None,
        custom_param_to_model_name=None,
        default_params=None,
        default_objects=None,
    ):
        self._urlconf = settings.ROOT_URLCONF if urlconf is None else urlconf
        self.excluded_namespaces = (
            settings.URLS_TEST_IGNORED_NAMESPACES
            if excluded_namespaces is None
            else excluded_namespaces
        )
        self.excluded_patterns = excluded_patterns or []
        self.pattern_overrides = pattern_overrides or {}
        self.custom_param_to_model_name = custom_param_to_model_name or {}
        self.default_objects = default_objects or {}
        self.default_params = default_params or {}

        self.resolver = get_resolver()

        self._our_models = tuple(get_our_models())

    def get_default_object(self, model_name_key: str) -> "Model":
        """
        Given a model name, returns an initialized model instance from the
        `default_objects` mapping.

        In case your model is defined under a custom key, add your overrides to this
        method.

        Args:
            model_name_key: Key in `default_objects` containing the object instance.

        Returns:
            A model instance.
        """
        try:
            return self.default_objects[model_name_key]
        except KeyError:
            msg = f'Failed to get a default object with key "{model_name_key}"'
            raise SkipUrl(msg)  # noqa: TRY200, B904

    def _get_admin_object_id_param(self, param_name: str, obj: Model, view_class):
        model = view_class.model
        if model not in self._our_models and model not in (
            type(obj) for obj in self.default_objects.values()
        ):
            msg = (
                f"Model {model._meta.app_label}.{model.__name__} "
                "does not belong to our models"
            )
            raise SkipUrl(msg)

        model_name = underscore(model.__name__)
        param_value_key = f"{model_name}_id"

        param_value = self.default_params.get(param_value_key, None)
        obj = self.get_default_object(model_name)
        return param_value, obj

    def _get_pk_param(self, param_name: str, obj: Model, view_class):
        if view_class is not None:
            model_name = underscore(view_class.model.__name__)
            param_value_key = f"{model_name}_id"

            param_value = self.default_params.get(param_value_key, None)
            obj = self.get_default_object(model_name)
        else:
            msg = "No view class was passed."
            raise SkipUrl(msg)

        return param_value, obj

    def _get_regex_param(
        self,
        param_name: str,
        obj: Model,
        view_class,
        regex_match: Match,
    ) -> tuple[str, Model]:
        model_name = regex_match[1]
        model_name_key = self.custom_param_to_model_name.get(model_name, model_name)

        param_value = self.default_params.get(f"{model_name_key}_id", None)
        obj = self.get_default_object(model_name_key)
        return param_value, obj

    def _get_slug_param(self, param_name: str, obj: Model, view_class):
        """
        Get a value for a slug parameter.

        If an object is passed to this method it will try to get a parent object based
        on the parameter name and then the slug value. On the other hand, if a view
        class is passed instead of an object, it will try to infer the slug and model.

        """
        re_match = self.SLUG_PARAM_RE.fullmatch(param_name)
        if obj is not None:
            if re_match:
                model_name, slug_field = re_match.groups()
                model_name = self.custom_param_to_model_name.get(
                    re_match[1], re_match[1]
                )
                # Find a field linking to the related model and access it to get
                # to the instance.
                for field in obj._meta.get_fields():
                    if isinstance(field, ForeignKey):
                        related_model = field.related_model
                        if model_name == underscore(related_model.__name__):
                            related_obj = getattr(obj, field.name)
                            return getattr(related_obj, slug_field), related_obj

                model_display_name = f"{obj._meta.app_label}.{obj.__class__.__name__}"
                msg = (
                    f"Could not find a direct relationship from {model_display_name}"
                    " to the parent object or slug field does not exist"
                )
                raise SkipUrl(msg)
            msg = (
                f'Cannot infer model name and slug field from parameter "{param_name}"'
            )
            raise SkipUrl(msg)
        elif view_class is not None:  # noqa: RET506
            model_class = view_class.model
            model_name = underscore(model_class.__name__)
            # If view model matches with parameter name, use a value stored in
            # default_params, otherwise extract model and field from the name.
            if model_name == param_name:
                param_value_key = f"{model_name}_{param_name}_slug"
                param_value = self.default_params.get(param_value_key, None)
                obj = self.get_default_object(model_name)
            elif re_match := self.SLUG_PARAM_RE.fullmatch(param_name):
                model_name, slug_field = re_match.groups()
                param_value_key = f"{param_name}_slug"
                param_value = self.default_params.get(param_value_key, None)
                obj_class = self.get_default_object(model_name).__class__
                obj = obj_class.objects.get(**{slug_field: param_value})
            else:
                msg = f'Cannot infer model from parameter "{param_name}"'
                raise SkipUrl(msg)

            return param_value, obj
        else:
            msg = "No view class or object was passed"
            raise SkipUrl(msg)

    def _get_params_for_pattern(  # noqa: C901
        self, pattern: URLPattern, pattern_name, converters: dict[str, "Converter"]
    ):
        """
        Using the dictionary of parameters defined on self.default_params and
        the list of objects defined on self.default_objects, get valid params for the
        specified URL pattern and converter.

        Args:
            pattern: URL pattern.
            pattern_name: Full pattern name.
            converters: Mapping of parameter names to param converters.

        Notes:
            This method has several constraints regarding the URL naming scheme.

            First, it assumes simple RUD views name their primary keys as ``pk`` or
            ``slug``.

            Secondly, URLs require to have a strict scheme where all intermediate
            models must be used in order to correctly assign their parameters.

            As an example, consider an application that keeps companies, stock series
            and quotes for each series. A company has several series and each series
            have several quotes. The URL to update the value of a quote should be in
            the format of::

                /company/{company_id}/series/{series_id}/quotes/{quote_id}/update

            While a shortened URL won't work::

                /company/{company_id}/series-quotes/{quote_id}/update

            Although for a developer it may be as simple of accessing the ``series``
            attribute of the quote and then ``company``, this algorithm is incapable
            of doing that because it does not know your model structure and
            implementing such a strategy, while magical would make this helper class
            extremely complex as implies complex data structures such as model graphs
            and pattern handling sophisticated enough to properly infer models from
            URL segments.

            In case this method fails to retrieve all the parameters, it will raise
            a special SkipUrl exception which in turn will cause _resolve_pattern to
            skip the URL and issue a warning detailing the reason of failure.

            If your application does not follow the suggested scheme, consider to define
            custom overrides for those patterns to avoid getting untested URLs.
        """
        obj = None
        params = {}
        callback = pattern.callback

        if pattern_name and pattern_name in self.pattern_overrides:
            return self.pattern_overrides[pattern_name]

        # If url is an admin view, callback will contain a `model_admin` attribute which
        # in turn, contains a reference to the model class.
        if hasattr(callback, "model_admin"):
            view_class = callback.model_admin
        elif hasattr(callback, "view_class"):
            view_class = callback.view_class
        else:
            view_class = None

        for param_name, converter in reversed(converters.items()):
            # Handle admin case first
            if isinstance(view_class, ModelAdmin):
                param_value, obj = self._get_admin_object_id_param(
                    param_name, obj, view_class
                )
                params[param_name] = param_value
                continue

            re_match = self.PK_PARAM_RE.fullmatch(param_name)
            if re_match is not None:
                param_value, obj = self._get_regex_param(
                    param_name, obj, view_class, re_match
                )
            elif param_name == "pk":
                if "pk" in params:
                    msg = "The pk parameter is meant to be the last one of the pattern"
                    raise SkipUrl(msg)
                param_value, obj = self._get_pk_param(param_name, obj, view_class)
            elif isinstance(converter, SlugConverter):
                param_value, obj = self._get_slug_param(param_name, obj, view_class)
            else:
                msg = (
                    f'Cannot resolve parameter "{param_name}" as it uses an '
                    "unsupported converter"
                )
                raise SkipUrl(msg)

            if param_value is None:
                msg = (
                    f'Cannot resolve parameter "{param_name}" as there is no default '
                    "value for it"
                )
                raise SkipUrl(msg)
            params[param_name] = param_value

        return params

    def _resolve_pattern(
        self,
        pattern: URLPattern | URLResolver,
        namespace: str | None = None,
        base: str | None = None,
        base_converters: dict[str, "Converter"] | None = None,
    ) -> Iterable[str]:
        """
        For a given URLPattern or URLResolver, collects format converters and recurse
        over URLResolvers until a pattern instance is found, which it is then resolved
        using the collected converters.

        Args:
            pattern: URLPattern or URLResolver
            namespace: URLResolver's namespace
            base_converters: URL parameter format converters

        Yields:
            A valid URL that can be used with the test client.
        """
        base_converters = base_converters if base_converters is not None else {}
        base = base if base is not None else r""

        converters = {**base_converters, **pattern.pattern.converters}

        if isinstance(pattern, URLResolver):
            for subpattern in pattern.url_patterns:
                sub_namespace = getattr(subpattern, "namespace", None)
                namespace = (
                    f"{namespace}:{sub_namespace}" if sub_namespace else namespace
                )
                if namespace and namespace in self.excluded_namespaces:
                    continue

                new_base = base + str(subpattern.pattern)
                yield from self._resolve_pattern(
                    subpattern, namespace, new_base, converters
                )
        elif pattern.name:
            pattern_name = f"{namespace}:{pattern.name}" if namespace else pattern.name
            if pattern_name in self.excluded_patterns:
                return

            try:
                params = self._get_params_for_pattern(pattern, pattern_name, converters)
                yield self._reverse_pattern(pattern_name, **params)
            except SkipUrl as e:
                msg = f'At pattern "{base}" [{pattern_name}]: {e}'
                warnings.warn(msg, stacklevel=2)
                return

    @staticmethod
    def _reverse_pattern(
        pattern_name: str,
        *args,
        **kwargs,
    ) -> str:
        """
        For a given URLPattern, it calls Django's `reverse` method to generate a proper
        URL.

        Args:
            pattern: URLPattern
            namespace: URLPattern's namespace
            args: args for `reverse`
            kwargs: kwargs for `reverse`

        Returns:
            A valid URL that can be used with the test client.
        """

        try:
            return reverse(pattern_name, args=args, kwargs=kwargs)
        except NoReverseMatch as e:
            msg = f'Reverse for pattern "{pattern_name}" failed'
            raise SkipUrl(msg) from e

    def get_urls_to_test(self) -> Iterable[str]:
        """
        Generates valid URLs for testing.

        Given a valid URLconf, it traverses all paths, interpolates URL parameters
        and yields a full URL that the test client can request.
        """
        for pattern in self.resolver.url_patterns:
            namespace = getattr(pattern, "namespace", None)
            if namespace and namespace in self.excluded_namespaces:
                continue

            pattern_str = str(pattern.pattern)
            yield from self._resolve_pattern(pattern, namespace, pattern_str)
