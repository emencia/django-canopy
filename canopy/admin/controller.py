from django.contrib import admin
from django.urls import path

from adminsortable2.admin import SortableAdminBase

from ..models import Controller
from ..views import ControllerAdminDataVisualizerView
from .slot import SlotAdminInline


@admin.register(Controller)
class ControllerAdmin(SortableAdminBase, admin.ModelAdmin):
    """
    Controller admin
    """
    list_display = (
        "title",
        "slug",
        "enabled",
        "form_template",
        "success_template",
    )
    prepopulated_fields = {"slug": ("title",)}
    search_fields = [
        "title",
    ]
    inlines = [
        SlotAdminInline,
    ]
    readonly_fields = [
        "version",
        "created",
        "last_update",
    ]

    def get_urls(self):
        """
        Set some additional custom admin views
        """
        urls = super().get_urls()

        extra_urls = [
            path(
                "<int:pk>/data/",
                self.admin_site.admin_view(
                    ControllerAdminDataVisualizerView.as_view(),
                ),
                name="canopy_controller_data_visualizer",
            ),
        ]

        return extra_urls + urls
