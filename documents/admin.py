from django.contrib import admin

from documents.models.document import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass
