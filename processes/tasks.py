from celery import shared_task


@shared_task
def send_activity_instance_notification(activity_instance_pk: int) -> None:
    from processes.models.process_activity_instance import ProcessActivityInstance

    activity_instance = ProcessActivityInstance.objects.get(pk=activity_instance_pk)
    activity_instance.send_email_notification()


@shared_task
def send_activity_instance_completion_notification(
    activity_instance_pk: int, email_to_notify: str
) -> None:
    from processes.models.process_activity_instance import ProcessActivityInstance

    activity_instance = ProcessActivityInstance.objects.get(pk=activity_instance_pk)
    activity_instance.send_email_completion_notification(
        email_to_notify=email_to_notify
    )
