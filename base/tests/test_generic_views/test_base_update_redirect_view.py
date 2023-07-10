from unittest.mock import patch

import pytest

from base.tests.test_generic_views.mock_model import MockModel
from base.views.generic import BaseUpdateRedirectView


class MockUpdateRedirectView(BaseUpdateRedirectView):
    model = MockModel


@pytest.mark.parametrize(
    ("patch_verb_str", "verb", "do_action_call_count"),
    (
        ("django.views.generic.base.RedirectView.get", "get", 0),
        ("django.views.generic.base.RedirectView.post", "post", 1),
    ),
)
def test_base_redirect_view_verbs(patch_verb_str, verb, do_action_call_count, rf):
    with (
        patch(patch_verb_str, return_value="TEST"),
        patch(
            "base.views.generic.edit.BaseUpdateRedirectView.get_object"
        ) as get_object,
        patch("base.views.generic.edit.BaseUpdateRedirectView.do_action") as do_action,
    ):
        view = MockUpdateRedirectView()
        view.object = MockModel()
        view.request = rf.get("/")
        assert getattr(view, verb)(rf.get("/")) == "TEST"
        assert get_object.call_count == 1
        assert do_action.call_count == do_action_call_count


@pytest.mark.parametrize(
    ("next_url", "expected"),
    (
        (None, "/mockmodel/1/"),
        ("/test/", "/test/"),
    ),
)
def test_base_redirect_view_get_redirect_url(next_url, expected, rf):
    with patch("base.views.generic.edit.BaseUpdateRedirectView.get_object"):
        view = MockUpdateRedirectView()
        view.object = MockModel()
        view.request = rf.get(f"/?next={next_url}" if next_url else "/")
        assert view.get_redirect_url() == expected
