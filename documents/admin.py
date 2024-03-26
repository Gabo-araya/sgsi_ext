from django.contrib import admin

from documents.models.control import Control
from documents.models.control_category import ControlCategory
from documents.models.document import Document
from documents.models.document_read_by_user import DocumentReadByUser
from documents.models.document_version import DocumentVersion


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    pass


@admin.register(DocumentReadByUser)
class DocumentReadByUserAdmin(admin.ModelAdmin):
    pass


@admin.register(ControlCategory)
class ControlCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Control)
class ControlAdmin(admin.ModelAdmin):
    pass
