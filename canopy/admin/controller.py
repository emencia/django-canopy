from django.contrib import admin

from ..models import Controller


@admin.register(Controller)
class ControllerAdmin(admin.ModelAdmin):
    """
    TODO:
    Admin form edit view will have to display its slots.

    This could be done with a custom context variable and customized form template to
    include the listing.

    Listing would include the slot name, its kind and should be clickable to go
    directly to the slot form edit view.

    Also, an additional button to create a new slot would be nice.

    This probably won't be achieved with inline Slot form.
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
