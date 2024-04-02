from django import forms
from django.utils.translation import gettext_lazy as _

from base.forms import BaseModelForm
from risks.models.risk import Risk


class RiskForm(BaseModelForm):
    residual_risk_for = forms.ModelMultipleChoiceField(
        queryset=Risk.objects.all(),
        required=False,
        label=_("Residual risk for"),
    )

    class Meta:
        model = Risk
        fields = (
            "assets",
            "controls",
            "title",
            "description",
            "responsible",
            "severity",
            "likelihood",
            "treatment",
            "residual_risk_for",
        )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields[
            "responsible"
        ].label_from_instance = lambda user: user.get_label_for_instance()
        if self.instance.pk is not None:
            residual_risk_for_field = self.fields["residual_risk_for"]
            residual_risk_for_field.queryset = (
                Risk.objects.get_residual_risk_for_queryset(self.instance)
            )
            residual_risk_for_field.initial = self.instance.residual_risk_for.all()

    def save(self, commit: bool = True) -> Risk:
        obj = super().save(commit)
        if not commit:
            return obj
        for risk in self.cleaned_data["residual_risk_for"]:
            risk.residual_risks.add(obj)
        return obj
