# standard library
import logging
import threading

# django
from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)
health_logger = logging.getLogger(__name__ + ".ReadinessCheckMiddleware")


class RequestMiddleware:
    """
    Middleware that stores the user that made a request. This is used when logging
    object creations/updates/deletions to obtain the user performing such action.
    """

    thread_local = threading.local()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Save the user that makes the request
        self.thread_local.user = request.user
        return self.get_response(request)


class ReadinessCheckMiddleware(MiddlewareMixin):
    """
    Middleware that allows to run readiness checks before any database access is
    performed.
    """

    def process_request(self, request):
        if request.method == "GET" and request.path == "/_ready/":
            try:
                # django
                from django.db import connections

                for name in connections:
                    cursor = connections[name].cursor()
                    cursor.execute("SELECT 1;")
                    if cursor.fetchone() is None:
                        return HttpResponseServerError(
                            "Got invalid response from DB", content_type="text/plain"
                        )
            except Exception as e:
                health_logger.exception("Failure connecting to database", exc_info=e)
                return HttpResponseServerError(
                    "Failure connecting to the DB", content_type="text/plain"
                )

            return HttpResponse()

        return self.get_response(request)
