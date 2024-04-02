from django.contrib import admin

from risks.models.risk import Risk


@admin.register(Risk)
class RiskAdmin(admin.ModelAdmin):
    pass
