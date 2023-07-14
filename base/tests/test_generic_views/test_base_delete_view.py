from unittest.mock import patch

from django.db.models import ProtectedError

import pytest

from base.tests.test_generic_views.mock_model import MockModel
from base.views.generic import BaseDeleteView


class MockDeleteView(BaseDeleteView):
    model = MockModel


@pytest.mark.parametrize(
    (
        "title",
        "expected_title",
        "next_url",
        "expected_next_url",
        "expected_success_url",
    ),
    (
        ("Test Title", "Test Title", "Test", "Test", "Test"),
        (None, "Delete Object", None, None, "mockmodel_list"),
    ),
    ids=("title_and_next_url", "no_title_and_no_next_url"),
)
def test_base_delete_view(  # noqa: PLR0913
    title,
    expected_title,
    next_url,
    expected_next_url,
    expected_success_url,
    rf,
):
    with (
        patch("base.views.generic.edit.reverse", return_value="mockmodel_list"),
        patch("django.views.generic.DeleteView.get_context_data", return_value={}),
    ):
        view = MockDeleteView()
        view.object = MockModel
        view.title = title
        view.request = rf.get(f"/?next={next_url}" if next_url else "/")
        context_data = view.get_context_data()
        assert context_data["title"] == expected_title
        assert context_data["next"] == expected_next_url
        assert context_data["opts"] == MockModel._meta
        view.request = rf.post("/", {"next": next_url or ""})
        assert view.get_success_url() == expected_success_url


def test_base_delete_view_delete_action(rf):
    with patch("django.views.generic.edit.DeletionMixin.delete", return_value="TEST"):
        view = MockDeleteView()
        view.object = MockModel()
        assert view.delete(rf.get("/")) == "TEST"


def test_base_delete_view_delete_action_handle_protected_error(rf):
    with (
        patch(
            "django.views.generic.edit.DeletionMixin.delete",
            return_value="TEST",
            side_effect=ProtectedError("Error", ""),
        ),
        patch("django.contrib.messages.add_message"),
        patch(
            "base.views.generic.edit.HttpResponseRedirect", return_value="TEST"
        ) as mock_redirect,
    ):
        view = MockDeleteView()
        view.object = MockModel()
        new_var = view.delete(rf.get("/"))
        assert new_var == mock_redirect.return_value
