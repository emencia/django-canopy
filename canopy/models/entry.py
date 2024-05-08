from django.db import models
from django.utils.translation import gettext_lazy as _


def empty_fresh_dictionnary():
    return dict()


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

    data = models.JSONField(null=False, default=empty_fresh_dictionnary)
    """
    Required JSON value Where is saved data from a request.
    """

    created = models.DateTimeField(auto_now_add=True)
    """
    Datetime of object creation, automatically filled.
    """

    class Meta:
        ordering = ["-created"]
        verbose_name = _("Form entry")
        verbose_name_plural = _("Form entries")

    def __str__(self):
        return "{controller}: {created}".format(
            controller=self.controller.title,
            created=self.created.isoformat(timespec="seconds")
        )
