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
        default=1,
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

    def definitions_scheme(self, queryset=None):
        """
        Returns all controller slot definitions.

        TODO: Rename to "slot_definitions"

        .. Note::
            Since hee we use ``Queryset.values()`` to get slots, the options value will
            be the plain string for the JSON data. You will need to decode (like
            with ``json.loads``) yourself if needed.

        Keyword Arguments:
            queryset (Queryset): A custom queryset to use instead of the default one
                which get all controller slot objects.

        Returns:
            dict: Slot definitions.
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
                "options",
            )
        }

    @cached_property
    def fields_definitions(self):
        """
        Returns the field slot definitions.

        This property exists because we plan to have non field slots.

        Returns:
            dict: Slot definitions.
        """
        return self.definitions_scheme()

    def get_absolute_url(self):
        """
        Return absolute URL to the category detail view.

        Returns:
            string: An URL.
        """
        return reverse("canopy:controller-form", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        # Auto update 'last_update' value on each save
        self.last_update = timezone.now()

        super().save(*args, **kwargs)
