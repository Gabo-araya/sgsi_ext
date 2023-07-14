from unittest.mock import patch

from project.celeryconf import CELERY_LOGGER_NAME
from project.celeryconf import setup_celery_logging


def test_setup_celery_logging():
    with patch("logging.getLogger") as mock_get_logger:
        setup_celery_logging(loglevel="INFO")
        mock_get_logger.assert_called_once_with(CELERY_LOGGER_NAME)
        mock_get_logger.return_value.setLevel.assert_called_once_with("INFO")
