from django.contrib import admin

from ..models import Controller


@admin.register(Controller)
class ControllerAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "version",
    )
    prepopulated_fields = {"slug": ("title",)}
    search_fields = [
        "title",
    ]
