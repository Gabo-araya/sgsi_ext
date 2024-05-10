from django import forms
from django.utils.translation import gettext_lazy as _

from base.forms import BaseModelForm
from documents.forms import EvidenceForm
from processes.models.process import Process
from processes.models.process_activity import ProcessActivity
from processes.models.process_activity_instance import ProcessActivityInstance
from processes.models.process_instance import ProcessInstance
from processes.models.process_version import ProcessVersion
from users.models.user import User


class ProcessForm(BaseModelForm):
    class Meta:
        model = Process
        fields = ("name",)


class ProcessVersionForm(BaseModelForm):
    class Meta:
        model = ProcessVersion
        fields = (
            "defined_in",
            "controls",
            "recurrency",
        )


class ProcessActivityForm(BaseModelForm):
    class Meta:
        model = ProcessActivity
        fields = ("description", "assignee_group", "email_to_notify")


class ProcessInstanceForm(BaseModelForm):
    process = forms.ModelChoiceField(
        label=_("Process"),
        queryset=Process.objects.all(),
        required=True,
    )

    class Meta:
        model = ProcessInstance
        fields = ("process",)

    def __init__(self, user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["process"].queryset = user.get_instantiable_processes()

    def save(self, commit: bool = True) -> ProcessInstance:
        self.instance.process_version = self.cleaned_data.get(
            "process"
        ).last_published_version
        return super().save(commit)


class ProcessActivityInstanceCompleteForm(EvidenceForm, BaseModelForm):
    class Meta:
        model = ProcessActivityInstance
        fields = ("evidence_file", "evidence_url")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        next_activity = self.instance.get_next_activity()
        if next_activity is not None:
            self.add_next_activity_fields(next_activity)

    def add_next_activity_fields(self, next_activity: ProcessActivity):
        users_qs = next_activity.assignee_group.user_set.all()
        self.fields["next_activity_assignee"] = forms.ModelChoiceField(
            label=_("Next activity assignee"),
            queryset=users_qs,
            required=True,
            help_text=_(
                "Next activity: {next_activity_description}, assignee group: "
                "{next_activity_asginee_group}."
            ).format(
                next_activity_description=next_activity.description,
                next_activity_asginee_group=next_activity.assignee_group,
            ),
        )
        if users_qs.count() == 1:
            self.fields["next_activity_assignee"].initial = users_qs.first()
