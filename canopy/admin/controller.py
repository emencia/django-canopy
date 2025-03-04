from django.contrib import admin

from adminsortable2.admin import SortableAdminBase

from ..models import Controller
from .slot import SlotAdminInline


@admin.register(Controller)
class ControllerAdmin(SortableAdminBase, admin.ModelAdmin):
    """
    TODO:
    Admin form edit view will have to display its slots.

    This could be done with a custom context variable and customized form template to
    include the listing.

    Listing would include the slot name, its kind and should be clickable to go
    directly to the slot form edit view.

    Also, an additional button to create a new slot would be nice.

    We may start with inline items to start with something and look if it can be
    customized enough for our needs.
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
