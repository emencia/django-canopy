from django.contrib import admin

from adminsortable2.admin import SortableTabularInline

from ..models import Slot
from ..forms import SlotAdminForm


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    """
    This includes some code to tweak the admin form process that is not as simple as
    non admin form (because model admin needs to introspect a lot). Original code
    idea comes from https://stackoverflow.com/a/62719818 with some adjustments.

    TODO:
        We tried to inject some field inputs for the Slot options
        (field&widget). I dont really remember the stage of advancement of this way.

        With the definition registry interface it may be easier to retrieve options
        datas to build fields, but i don't know about to fill them with data from JSON,
        how to validate their value.
    """
    form = SlotAdminForm
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

    def get_fields(self, request, obj=None):
        """
        Slot options are currently not managed since we currently dont have the proper
        final solution yet.

        It may be better first to ensure the Definition registry is fully featured to
        stand on and helps to implement final option management from admin.
        """
        # Slot has no '_default_options_***()' methods
        field_options_fields = (
            obj.field_options
            if obj
            else {}
        )

        # widget_options_fields = (
        #     obj.options_fields("widget")
        #     if obj
        #     else Slot._default_options_fields("widget")
        # )

        # We should merge 'widget_options_fields' also
        self.form.declared_fields = {} if not obj else field_options_fields

        return super().get_fields(request, obj=obj)

    def get_fieldsets(self, request, obj=None):
        """
        Hook for specifying fieldsets.
        """
        items = super().get_fieldsets(request, obj=obj)
        return items

    def get_readonly_fields(self, request, obj=None):
        """
        Theorically field_options and widget_options should be hidden. But during
        development we still want to see what they are holding.
        """
        return self.readonly_fields + ("field_options", "widget_options")


class SlotAdminInline(SortableTabularInline):
    """
    Slot inline model admin for Controller admin.
    """
    model = Slot
    exclude = ["help_text", "initial", "field_options", "widget_options", ]
    extra = 0
