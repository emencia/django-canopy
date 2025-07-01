from django.contrib import admin

from ..models import Handler
from ..forms import HandlerAdminForm, HandlerAdminInlineForm


@admin.register(Handler)
class HandlerAdmin(admin.ModelAdmin):
    """
    Handler model admin for Controller admin.
    """
    form = HandlerAdminForm
    list_display = (
        "controller",
        "name",
    )
    list_filter = ("name", "controller")


class HandlerAdminInline(admin.TabularInline):
    """
    Handler inline model admin for Controller admin.
    """
    form = HandlerAdminInlineForm
    model = Handler
    extra = 0
