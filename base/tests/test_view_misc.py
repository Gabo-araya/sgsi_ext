from unittest.mock import patch

from django.conf import settings

from base.views.misc import StatusView
from base.views.misc import bad_request_view
from base.views.misc import server_error_view


def test_status_view_context_data():
    view = StatusView()
    context = view.get_context_data()
    assert context["settings"] == settings


def test_bad_request_view():
    with patch("base.views.misc.bad_request") as mock_bad_request:
        mock_bad_request.return_value = "bad_request"
        assert bad_request_view("request", "exception", "template") == "bad_request"


def test_server_error_view():
    with patch("base.views.misc.server_error") as mock_server_error:
        mock_server_error.return_value = "server_error"
        assert server_error_view("request", "template") == "server_error"
