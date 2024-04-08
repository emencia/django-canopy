from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Controller(models.Model):
    """
    Controller defines form data structure and options.
    """
    title = models.CharField(
        _("title"),
        blank=False,
        null=False,
        unique=True,
        max_length=100,
    )
    """
    Required unique title string.
    """

    slug = models.SlugField(
        _("slug"),
        max_length=100,
        unique=True,
        help_text=_(
            "Used to build the URL."
        ),
    )
    """
    Required unique slug string.
    """

    version = models.PositiveSmallIntegerField(
        _("version"),
        default=1,
    )
    """
    Required version positive integer. This would be automatically updated on
    slot changes.
    """

    created = models.DateTimeField(auto_now_add=True)

    last_update = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["title"]
        verbose_name = _("Form controller")
        verbose_name_plural = _("Form controllers")

    def __str__(self):
        return self.title

    def as_scheme(self):
        return {
            item["name"]: item
            for item in self.slot_set.all().values(
                "kind",
                "label",
                "name",
                "required",
                "position",
                "help_text",
                "initial",
            )
        }

    def save(self, *args, **kwargs):
        # Auto update 'last_update' value on each save
        self.last_update = timezone.now()

        super().save(*args, **kwargs)
