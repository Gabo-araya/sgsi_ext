import logging
import os

# others libraries
from celery import Celery
from celery.signals import setup_logging

CELERY_LOGGER_NAME = "celery"


@setup_logging.connect
def setup_celery_logging(loglevel=None, **kwargs):
    """Skip default Celery logging configuration.

    Will rely on Django to set up the base root logger.
    Celery loglevel will be set if provided as Celery command argument.
    """
    if loglevel:
        logging.getLogger(CELERY_LOGGER_NAME).setLevel(loglevel)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")


app = Celery("project-name-placeholder")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
