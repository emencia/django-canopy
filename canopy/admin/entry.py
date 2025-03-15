import json

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from ..models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = (
        "controller",
        "created",
        "version",
    )
    list_filter = ("controller", "created")
    readonly_fields = [
        "formatted_data",
    ]

    @admin.display(description=_("data"))
    def formatted_data(self, obj):
        """
        Format JSON data to humanized display.

        TODO:
            - Data key names are slot field names but it would be better to display the
              slot label;
            - Kind need to define a possible "rendering" function instead of default
              one (a str());
            - HTML should be built from a template so it's easier to improve and can
              overrided (like for with admin styles);
        """
        if not obj.data:
            return mark_safe("<p>Stored data is empty</p>")

        # slots = obj.controller.get_slots()

        content = "<dl>{}</dl>"
        items = ""
        for k, v in obj.data.items():
            items += "<dt>{}</dt><dd>{}</dd>".format(
                k,
                (v if v else "-")
            )

        return mark_safe(content.format(items))
