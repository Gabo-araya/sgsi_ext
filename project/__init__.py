import os

from dateutil.parser import isoparse

from .celeryconf import app as celery_app

_GIT_COMMIT = os.environ.get("GIT_COMMIT", "<unknown>")
_RAW_BUILD_TIME = os.environ.get("BUILD_TIME", "")
try:
    _BUILD_TIME = isoparse(_RAW_BUILD_TIME)
except ValueError:
    _BUILD_TIME = None

__all__ = ["celery_app"]
