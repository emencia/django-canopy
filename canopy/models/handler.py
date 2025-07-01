from django.db import models
from django.utils.translation import gettext_lazy as _

from ..choices import get_controller_handler_choices, get_controller_handler_default
from ..exceptions import HandlerError
from ..utils.loaders import get_handler_processor_class


class Handler(models.Model):
    """
    Handler manage how the Entry data should be process after a form success.

    TODO: It will probably include also a
    JSONField specific to each type but we didn't materialized a proper interface to
    manage JSON yet so it will be ignored for now.
    """
    controller = models.ForeignKey(
        "canopy.controller",
        null=True,
        default=None,
        on_delete=models.CASCADE,
    )
    """
    Required controller relation.
    """

    name = models.CharField(
        _("name"),
        choices=get_controller_handler_choices(),
        default=get_controller_handler_default(),
        help_text=_(
            "Handler type."
        ),
        max_length=255,
    )
    """
    Required Python path string to the handler class.
    """

    class Meta:
        ordering = ["controller", "name"]
        verbose_name = _("Data handler")
        verbose_name_plural = _("Data handlers")

    def __str__(self):
        return self.get_name_display()

    def get_processor_class(self):
        """
        Load and return the handler processor class.

        Returns:
            Class: The class object of the handler processor.
        """
        return get_handler_processor_class(self.name)
