from django.contrib import admin

from ..models import Slot


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = (
        "label",
        "controller",
        "kind",
        "required",
    )
    list_filter = ("kind", "controller", "required")
    search_fields = [
        "label",
    ]
