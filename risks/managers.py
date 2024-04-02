from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from risks.models.risk import Risk


class RiskQuerySet(models.QuerySet):
    def get_residual_risk_for_queryset(self, risk: Risk) -> RiskQuerySet:
        return self.exclude(pk=risk.pk).exclude(residual_risk_for=risk)
