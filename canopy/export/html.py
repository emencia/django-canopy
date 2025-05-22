from django.template.loader import render_to_string

from .base import BaseExporter


class HtmlExporter(BaseExporter):
    """
    Export all Entry objects to HTML output from a template.
    """
    RENDER_TEMPLATE = "canopy/admin/entry/export.html"

    def get_render(self, context, template=None):
        """
        Render data from a template.
        """
        template = template or self.RENDER_TEMPLATE
        return render_to_string(template, context)

    def export(self, controller, template=None):
        context = super().export(controller)

        return self.get_render(context, template=template)
