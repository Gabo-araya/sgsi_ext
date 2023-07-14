from unittest.mock import patch

import pytest

from base.tests.test_generic_views.mock_model import MockModel
from base.views.generic import BaseCreateView


class MockCreateView(BaseCreateView):
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
        (None, "Create Mock Model", None, None, "mockmodel_list", "success_url"),
    ),
    ids=("title_and_next_url", "no_title_and_no_next_url"),
)
def test_base_create_view(  # noqa: PLR0913
    title,
    expected_title,
    next_url,
    expected_next_url,
    expected_cancel_url,
    expected_success_url,
    no_translations,
    rf,
):
    with (
        patch("base.views.generic.edit.reverse", return_value="mockmodel_list"),
        patch("django.views.generic.CreateView.get_context_data", return_value={}),
        patch(
            "django.views.generic.CreateView.get_success_url",
            return_value="success_url",
        ),
    ):
        view = MockCreateView()
        view.title = title
        view.request = rf.get(f"/?next={next_url}" if next_url else "/")
        context_data = view.get_context_data()
        assert context_data["title"] == expected_title
        assert context_data["next"] == expected_next_url
        assert context_data["opts"] == MockModel._meta
        assert context_data["cancel_url"] == expected_cancel_url
        view.request = rf.post("/", {"next": next_url or ""})
        assert view.get_success_url() == expected_success_url
