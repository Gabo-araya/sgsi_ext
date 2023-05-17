# others libraries
from celery.utils.log import get_task_logger

from api_client.models import ClientLog
from project.celeryconf import app

logger = get_task_logger(__name__)


@app.task
def client_log_cleanup():
    old_logs = ClientLog.objects.old()
    logger.info(f"Deleting {old_logs}...")
    old_logs.delete()
    logger.info("Logs deleted!")
