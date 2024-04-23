from django.contrib import admin

from processes.models.process_activity import ProcessActivity
from processes.models.process_activity_instance import ProcessActivityInstance
from processes.models.process_instance import ProcessInstance
from processes.models.process_version import ProcessVersion


@admin.register(ProcessInstance)
class ProcessInstanceAdmin(admin.ModelAdmin):
    pass


@admin.register(ProcessVersion)
class ProcessVersionAdmin(admin.ModelAdmin):
    pass


@admin.register(ProcessActivity)
class ProcessActivityAdmin(admin.ModelAdmin):
    pass


@admin.register(ProcessActivityInstance)
class ProcessActivityInstanceAdmin(admin.ModelAdmin):
    pass
