from django.db import models
from django.utils.translation import gettext_lazy as _


class Entry(models.Model):
    """
    Entry contains user submitted data from a request on a Controller.
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

    version = models.PositiveSmallIntegerField(
        _("version"),
        default=1,
    )
    """
    Required version positive integer. This would be the current controller version.
    """

    data = models.JSONField(null=True)
    """
    Where is saved data from a request
    """

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = _("Form slot")
        verbose_name_plural = _("Form slots")

    def __str__(self):
        return self.label
