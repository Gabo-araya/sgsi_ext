from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel
from base.utils import build_absolute_url_wo_req
from documents.models.evidence import Evidence
from messaging.email_manager import send_emails
from processes.managers import ProcessActivityInstanceQuerySet
from processes.models.process_activity import ProcessActivity
from processes.models.process_instance import ProcessInstance
from processes.tasks import send_activity_instance_completion_notification
from processes.tasks import send_activity_instance_notification

if TYPE_CHECKING:
    from processes.forms import ProcessActivityInstanceCompleteForm


class ProcessActivityInstance(BaseModel):
    process_instance = models.ForeignKey(
        verbose_name=_("process instance"),
        to=ProcessInstance,
        on_delete=models.PROTECT,
        related_name="activity_instances",
    )
    activity = models.ForeignKey(
        verbose_name=_("activity"),
        to=ProcessActivity,
        on_delete=models.PROTECT,
        related_name="activity_instances",
    )
    assignee = models.ForeignKey(
        verbose_name=_("assignee"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="activity_instances",
    )
    is_completed = models.BooleanField(
        verbose_name=_("is completed"),
        default=False,
    )
    completed_at = models.DateTimeField(
        verbose_name=_("completed at"),
        null=True,
        blank=True,
    )
    evidence = models.OneToOneField(
        verbose_name=_("evidence"),
        to=Evidence,
        on_delete=models.PROTECT,
        related_name="process_activity_instance",
        null=True,
    )

    objects = ProcessActivityInstanceQuerySet.as_manager()

    class Meta:
        verbose_name = _("process activity instance")
        verbose_name_plural = _("process activity instances")
        ordering = ("-pk",)

    def __str__(self) -> str:
        return str(self.activity)

    def send_email_notification(self) -> None:
        context = {
            "process_instance": self.process_instance,
            "process_instance_url": build_absolute_url_wo_req(
                self.process_instance.get_absolute_url()
            ),
            "previous_activity_instance": self.get_previous_activity_instance(),
            "activity_instance": self,
            "activity_instance_url": build_absolute_url_wo_req(self.get_absolute_url()),
        }
        send_emails(
            emails=(self.get_email_to_notify(),),
            template_name="processactivityinstance_notification",
            subject=str(self),
            context=context,
        )

    def get_email_to_notify(self) -> str:
        return (
            self.activity.email_to_notify
            if self.activity.email_to_notify
            else self.assignee.email
        )

    def send_email_completion_notification(self, email_to_notify) -> None:
        context = {
            "process_instance": self.process_instance,
            "process_instance_url": build_absolute_url_wo_req(
                self.process_instance.get_absolute_url()
            ),
            "activity_instance": self,
            "activity_instance_url": build_absolute_url_wo_req(self.get_absolute_url()),
        }
        send_emails(
            emails=(email_to_notify,),
            template_name="processactivityinstance_completion_notification",
            subject=f"{self.process_instance.process_version.process.name} finalizado",
            context=context,
        )

    def get_next_activity(self) -> ProcessActivity | None:
        return self.activity.get_next_activity()

    def get_previous_activity_instance(self) -> ProcessActivityInstance | None:
        qs = self.process_instance.activity_instances.filter(
            activity__order__lt=self.activity.order
        )
        if qs.exists():
            return qs.latest("activity__order")
        return None

    def get_absolute_url(self) -> str:
        return reverse("processactivityinstance_detail", args=(self.pk,))

    def mark_as_completed(self, form: ProcessActivityInstanceCompleteForm) -> None:
        evidence = Evidence.create_from_form(form)
        next_activity_instance = self.create_next_activity_instance_if_exists(form)
        self.update(evidence=evidence, is_completed=True, completed_at=timezone.now())
        self.notify_if_required(form, next_activity_instance)
        self.process_instance.check_if_completed()

    def create_next_activity_instance_if_exists(
        self, form: ProcessActivityInstanceCompleteForm
    ) -> ProcessActivityInstance | None:
        next_activity = self.get_next_activity()
        if next_activity is None:
            return None
        return next_activity.create_instance(
            process_instance=self.process_instance,
            assignee=form.cleaned_data["next_activity_assignee"],
        )

    def notify_if_required(
        self,
        form: ProcessActivityInstanceCompleteForm,
        next_activity_instance: ProcessActivityInstance,
    ) -> None:
        if next_activity_instance is not None:
            send_activity_instance_notification.delay(next_activity_instance.pk)
        elif email_to_notify := form.cleaned_data["email_to_notify"]:
            send_activity_instance_completion_notification.delay(
                self.pk, email_to_notify
            )
