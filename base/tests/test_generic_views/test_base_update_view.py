from unittest.mock import patch

from django.utils import translation

import pytest

from base.tests.test_generic_views.mock_model import MockModel
from base.views.generic import BaseUpdateView


class MockUpdateView(BaseUpdateView):
    model = MockModel


@pytest.mark.parametrize(
    (
        "title",
        "expected_title",
        "next_url",
        "expected_next_url",
        "expected_cancel_url",
        "expected_success_url",
    ),
    (
        ("Test Title", "Test Title", "Test", "Test", "Test", "Test"),
        (None, "Update Object", None, None, "/mockmodel/1/", "/mockmodel/1/"),
    ),
    ids=("title_and_next_url", "no_title_and_no_next_url"),
)
def test_base_update_view(
    title,
    expected_title,
    next_url,
    expected_next_url,
    expected_cancel_url,
    expected_success_url,
    rf,
):
    with (
        patch("base.views.generic.edit.reverse", return_value="mockmodel_list"),
        patch("django.views.generic.UpdateView.get_context_data", return_value={}),
        translation.override("en"),
    ):
        view = MockUpdateView()
        view.title = title
        view.object = MockModel
        view.request = rf.get(f"/?next={next_url}" if next_url else "/")
        context_data = view.get_context_data()
        assert context_data["title"] == expected_title
        assert context_data["next"] == expected_next_url
        assert context_data["opts"] == MockModel._meta
        assert context_data["cancel_url"] == expected_cancel_url
        view.request = rf.post("/", {"next": next_url or ""})
        assert view.get_success_url() == expected_success_url


@pytest.mark.parametrize(
    ("patch_verb_str", "verb"),
    (
        ("django.views.generic.edit.ProcessFormView.get", "get"),
        ("django.views.generic.edit.ProcessFormView.post", "post"),
    ),
)
def test_base_update_view_verbs(patch_verb_str, verb, rf):
    obj = MockModel()
    title = "Test Title"
    with (
        patch(patch_verb_str, return_value="TEST"),
        patch("base.views.generic.edit.UpdateView.get_object", return_value=obj),
        patch("base.views.generic.edit.BaseUpdateView.get_title", return_value=title),
    ):
        view = MockUpdateView()
        assert getattr(view, verb)(rf.get("/")) == "TEST"
        assert view.object == obj
        assert view.title == title
