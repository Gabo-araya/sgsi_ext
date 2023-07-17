from contextlib import nullcontext as does_not_raise
from unittest.mock import MagicMock
from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured
from django.utils import translation

import pytest

from base.tests.test_generic_views.mock_model import MockChildModel
from base.tests.test_generic_views.mock_model import MockModel
from base.views.generic import BaseSubModelCreateView


class MockBaseSubModelCreateView(BaseSubModelCreateView):
    parent_model = MockModel
    model = MockChildModel


@pytest.mark.parametrize(
    ("patch_verb_str", "patch_verb_pre_action_str", "verb"),
    (
        (
            "django.views.generic.edit.ProcessFormView.get",
            "base.views.generic.BaseSubModelCreateView.pre_get",
            "get",
        ),
        (
            "django.views.generic.edit.ProcessFormView.post",
            "base.views.generic.BaseSubModelCreateView.pre_post",
            "post",
        ),
    ),
)
def test_base_sub_model_create_view_verbs(
    patch_verb_str, patch_verb_pre_action_str, verb, rf
):
    with (
        patch(patch_verb_str, return_value="TEST"),
        patch(patch_verb_pre_action_str, return_value=None) as patch_verb_pre_action,
        patch(
            "base.views.generic.BaseSubModelCreateView.get_parent_object",
            return_value="parent_object",
        ) as get_parent_object,
        patch(
            "base.views.generic.BaseSubModelCreateView.get_initial_object",
            return_value="initial_object",
        ) as get_initial_object,
    ):
        view = BaseSubModelCreateView()
        assert getattr(view, verb)(rf.get("/")) == "TEST"
        assert view.parent_object == "parent_object"
        assert get_parent_object.call_count == 1
        assert view.object == "initial_object"
        assert get_initial_object.call_count == 1
        assert patch_verb_pre_action.call_count == 1


@pytest.mark.parametrize(
    ("context_parent_object_name", "parent_obj", "expected"),
    (
        ("parent_object", None, "parent_object"),
        (None, MockModel, "mockmodel"),
        (None, None, None),
    ),
)
def test_base_sub_model_create_view_get_context_parent_object_name(
    context_parent_object_name, parent_obj, expected
):
    view = MockBaseSubModelCreateView()
    view.context_parent_object_name = context_parent_object_name
    assert view.get_context_parent_object_name(parent_obj) == expected


def test_base_sub_model_create_view_get_context_data(rf):
    with (
        patch(
            "base.views.generic.edit.BaseSubModelCreateView.get_context_parent_object_name",
            return_value="parent_name",
        ),
        patch(
            "base.views.generic.edit.BaseSubModelCreateView.get_title",
            return_value="title",
        ),
        patch(
            "base.views.generic.edit.BaseSubModelCreateView.get_cancel_url",
            return_value="cancel_url",
        ),
        patch("django.views.generic.CreateView.get_context_data", return_value={}),
    ):
        view = MockBaseSubModelCreateView()
        view.parent_object = "test"
        view.request = rf.get("/?next=next")
        context_data = view.get_context_data()
        assert context_data["parent_object"] == "test"
        assert context_data["parent_name"] == "test"
        assert context_data["title"] == "title"
        assert context_data["next"] == "next"
        assert context_data["cancel_url"] == "cancel_url"
        assert view.next_url == "next"


@pytest.mark.parametrize(
    ("next_url", "expected"),
    (
        ("next", "next"),
        (None, "success_url"),
    ),
)
def test_base_sub_model_create_view_get_success_url(next_url, expected, rf):
    with patch(
        "django.views.generic.CreateView.get_success_url", return_value="success_url"
    ):
        view = MockBaseSubModelCreateView()
        view.request = rf.post("/", {"next": next_url or ""})
        view.parent_object = "parent_object"
        assert view.get_success_url() == expected


@pytest.mark.parametrize(
    ("title", "expected"),
    (
        ("title", "title"),
        (None, "Create Mock Child Model"),
    ),
)
def test_base_sub_model_create_view_get_title(title, expected):
    with translation.override("en"):
        view = MockBaseSubModelCreateView()
        view.title = title
        assert view.get_title() == expected


@pytest.mark.parametrize(
    ("next_url", "expected"),
    (
        ("next", "next"),
        (None, "/mockmodel/1/"),
    ),
)
def test_base_sub_model_create_get_cancel_url(next_url, expected, rf):
    with translation.override("en"):
        view = MockBaseSubModelCreateView()
        view.next_url = next_url
        view.parent_object = MockModel
        assert view.get_cancel_url() == expected


def test_base_sub_model_create_get_parent_object():
    with patch(
        "base.views.generic.edit.get_object_or_404", return_value="parent_object"
    ) as get_object_or_404:
        view = MockBaseSubModelCreateView()
        view.parent_pk_url_kwarg = "parent_pk"
        view.kwargs = {"parent_pk": 1}
        assert view.get_parent_object() == "parent_object"
        get_object_or_404.assert_called_once_with(MockModel, pk=1)


@pytest.mark.parametrize(
    ("is_generic_relation", "expected_call_kwargs"),
    (
        (True, {"object_id": 1, "content_type": "content_type"}),
        (False, {"field_name": 1}),
    ),
)
def test_base_sub_model_create_get_initial_object(
    is_generic_relation, expected_call_kwargs
):
    with (
        patch("base.views.generic.edit.ContentType") as mock_content_type,
        patch(
            "base.views.generic.edit.BaseSubModelCreateView.get_model_related_field_name",
            return_value="field_name",
        ),
    ):
        mock_content_type.objects.get_for_model.return_value = "content_type"
        view = MockBaseSubModelCreateView()
        view.is_generic_relation = is_generic_relation
        view.parent_pk_url_kwarg = "parent_pk"
        view.kwargs = {"parent_pk": 1}
        view.parent_object = 1
        assert isinstance(view.get_initial_object(), MagicMock)


@pytest.mark.parametrize(
    ("model_parent_fk_field", "model", "expected", "expectation"),
    (
        ("test", MockModel, "test", does_not_raise()),
        (None, MockModel, "parent", does_not_raise()),
        (None, MockChildModel, "parent", pytest.raises(ImproperlyConfigured)),
    ),
)
def test_base_sub_model_create_get_model_related_field_name(
    model_parent_fk_field, model, expected, expectation
):
    with expectation:
        view = MockBaseSubModelCreateView()
        view.model_parent_fk_field = model_parent_fk_field
        view.parent_model = model
        assert view.get_model_related_field_name() == expected
