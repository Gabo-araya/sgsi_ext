# others libraries
from celery.utils.log import get_task_logger

from project.celeryconf import app

logger = get_task_logger(__name__)


@app.task
def sample_scheduled_task():
    logger.info("This task runs every minute!")
