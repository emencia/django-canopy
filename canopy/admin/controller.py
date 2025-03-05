from django.contrib import admin

from adminsortable2.admin import SortableAdminBase

from ..models import Controller
from .slot import SlotAdminInline


@admin.register(Controller)
class ControllerAdmin(SortableAdminBase, admin.ModelAdmin):
    """
    Controller admin
    """
    list_display = (
        "title",
        "slug",
        "version",
    )
    prepopulated_fields = {"slug": ("title",)}
    search_fields = [
        "title",
    ]
    inlines = [
        SlotAdminInline,
    ]
