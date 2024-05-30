from django.contrib import admin

from ..models import Slot
from ..forms import SlotAdminForm


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    """
    This includes some code to tweak the admin form process that is not as simple as
    non admin form (because model admin needs to introspect a lot). Original code
    idea comes from https://stackoverflow.com/a/62719818 with some adjustments.
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
        TODO: It does not care yet about widget options fields.
        """
        field_options_fields = (
            obj.options_fields("field")
            if obj
            else Slot._default_options_fields("field")
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
        print("🤡 fieldset items:", items)
        return items

    def get_readonly_fields(self, request, obj=None):
        """
        Originally field_options and widget_options should be hidden but during
        development we want to see what they hold
        """
        return self.readonly_fields + ("field_options", "widget_options")
