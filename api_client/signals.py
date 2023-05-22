from django.db.models.signals import post_save
from django.dispatch import receiver

from api_client.models import ClientLog


@receiver(post_save, sender=ClientLog)
def send_error_email(
    sender: type[ClientLog],
    instance: ClientLog,
    **kwargs,
):
    if instance.should_send_error_email():
        instance.send_error_email()
