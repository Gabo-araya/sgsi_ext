from django import forms
from django.utils.translation import gettext_lazy as _

from base.forms import BaseModelForm
from processes.models.process import Process
from processes.models.process_activity import ProcessActivity
from processes.models.process_activity_instance import ProcessActivityInstance
from processes.models.process_instance import ProcessInstance


class ProcessForm(BaseModelForm):
    class Meta:
        model = Process
        fields = (
            "name",
            "control",
            "recurrency",
        )


class ProcessActivityForm(BaseModelForm):
    class Meta:
        model = ProcessActivity
        fields = ("description", "asignee", "asignee_group")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["asignee"].label_from_instance = lambda user: user.get_label()


class ProcessInstanceForm(BaseModelForm):
    class Meta:
        model = ProcessInstance
        fields = ("process",)


class ProcessActivityInstanceCompleteForm(BaseModelForm):
    evidence = forms.FileField(
        label=_("Evidence"),
        required=True,
        help_text=_("Upload a file as evidence of the activity completion."),
    )

    class Meta:
        model = ProcessActivityInstance
        fields = ("evidence",)
