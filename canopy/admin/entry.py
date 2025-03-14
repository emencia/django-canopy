from django.contrib import admin

from ..models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = (
        "controller",
        "created",
        "version",
    )
    list_filter = ("controller", "created")
