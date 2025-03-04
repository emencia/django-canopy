from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
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
        default=0,
        blank=False,
        null=False,
    )
    """
    Required version positive integer. This would be automatically updated on
    slot changes.
    """

    created = models.DateTimeField(auto_now_add=True)
    """
    Datetime of object creation, automatically filled.
    """

    last_update = models.DateTimeField(default=timezone.now)
    """
    Datetime of last object update, automatically filled.
    """

    class Meta:
        ordering = ["title"]
        verbose_name = _("Form controller")
        verbose_name_plural = _("Form controllers")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Return absolute URL to the controller detail view.

        Returns:
            string: An URL.
        """
        return reverse("canopy:controller-form", kwargs={"slug": self.slug})

    def slot_values(self, queryset=None):
        """
        Returns a dictionnary which contains all controller slot values.

        Keyword Arguments:
            queryset (Queryset): A custom queryset to use instead of the default one
                which get all controller slot objects.

        Returns:
            dict: Slot values, each item key is the slot name and value is a dict of
            values.
        """
        queryset = queryset or self.slot_set.all()

        return {
            item["name"]: item
            for item in queryset.values(
                "kind",
                "label",
                "name",
                "required",
                "position",
                "help_text",
                "initial",
                "field_options",
                "widget_options",
            )
        }

    @cached_property
    def slot_fields_values(self):
        """
        Returns the slots fields values.

        NOTE: This property exists because we plan to have non field slots. In future
        we would have non field slot that we would distinct here to only return fields
        values

        Returns:
            dict: Fields values.
        """
        return self.slot_values()

    def save(self, *args, **kwargs):
        # Auto update 'last_update' value on each save
        self.last_update = timezone.now()
        self.version = self.version + 1

        super().save(*args, **kwargs)
