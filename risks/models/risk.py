from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel
from documents.models.control import Control
from information_assets.models.asset import Asset
from risks.enums import LikelihoodChoices
from risks.enums import SeverityChoices
from risks.enums import TreatmentChoices
from risks.managers import RiskQuerySet
from users.models import User


class Risk(BaseModel):
    assets = models.ManyToManyField(
        Asset, verbose_name=_("asset"), related_name="risks"
    )
    controls = models.ManyToManyField(
        Control,
        verbose_name=_("control"),
        related_name="risks",
    )
    title = models.CharField(verbose_name=_("title"), max_length=255)
    description = models.TextField(verbose_name=_("description"), blank=True)
    responsible = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_("responsible"),
        related_name="risks",
    )
    severity = models.CharField(
        verbose_name=_("severity"), max_length=255, choices=SeverityChoices.choices
    )
    likelihood = models.CharField(
        verbose_name=_("likelihood"), max_length=255, choices=LikelihoodChoices.choices
    )
    treatment = models.CharField(
        verbose_name=_("treatment"), max_length=255, choices=TreatmentChoices.choices
    )
    residual_risks = models.ManyToManyField(
        "self",
        verbose_name=_("residual risk for"),
        related_name="residual_risk_for",
        symmetrical=False,
        blank=True,
    )

    objects = RiskQuerySet.as_manager()

    class Meta:
        verbose_name = _("risk")
        verbose_name_plural = _("risks")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("risk_detail", args=(self.pk,))
