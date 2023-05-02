""" Administration classes for the parameters application. """


from django.contrib import admin

from .definitions import ParameterDefinitionList
from .models import Parameter


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ("name", "raw_value", "cache_seconds")

    fields = (
        "name",
        "kind",
        "raw_value",
        "cache_seconds",
    )

    readonly_fields = (
        "name",
        "kind",
    )

    def get_changelist_instance(self, request):
        """
        Return the ChangeList class for use on the changelist page.
        """
        expected_parameters_count = len(ParameterDefinitionList.definitions)

        if Parameter.objects.count() != expected_parameters_count:
            Parameter.create_all_parameters()

        return super().get_changelist_instance(request)

    def has_add_permission(self, request, obj=None):
        return False
