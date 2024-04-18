from django.contrib import admin

from processes.models.process import Process
from processes.models.process_activity import ProcessActivity
from processes.models.process_activity_instance import ProcessActivityInstance
from processes.models.process_instance import ProcessInstance


@admin.register(ProcessInstance)
class ProcessInstanceAdmin(admin.ModelAdmin):
    pass


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    pass


@admin.register(ProcessActivity)
class ProcessActivityAdmin(admin.ModelAdmin):
    pass


@admin.register(ProcessActivityInstance)
class ProcessActivityInstanceAdmin(admin.ModelAdmin):
    pass
