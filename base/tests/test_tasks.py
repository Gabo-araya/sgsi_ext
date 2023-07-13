from unittest.mock import patch

from base.tasks import sample_scheduled_task


def test_sample_scheduled_task():
    with patch("base.tasks.logger.info") as mock_info:
        sample_scheduled_task()
        mock_info.assert_called_once_with("This task runs every minute!")
