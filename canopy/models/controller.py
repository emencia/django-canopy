from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ..choices import (
    get_controller_form_template_choices, get_controller_form_template_default,
    get_controller_success_template_choices, get_controller_success_template_default,
)


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

    form_template = models.CharField(
        _("form page template"),
        choices=get_controller_form_template_choices(),
        default=get_controller_form_template_default(),
        help_text=_(
            "Template that will be used to render the form page."
        ),
        max_length=255,
    )

    success_template = models.CharField(
        _("success page template"),
        choices=get_controller_success_template_choices(),
        default=get_controller_success_template_default(),
        help_text=_(
            "Template that will be used to render the success page."
        ),
        max_length=255,
    )

    version = models.PositiveSmallIntegerField(
        _("version"),
        default=0,
        blank=False,
        null=False,
    )
    """
    Required version positive integer. This will be automatically updated on slot
    changes.
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

    def get_success_url(self):
        """
        Return absolute URL to the controller success view.

        Returns:
            string: An URL.
        """
        return reverse("canopy:controller-success", kwargs={"slug": self.slug})

    def get_data(self):
        return self.entry_set.all().order_by("created")

    def get_slots(self):
        return self.slot_set.all().order_by("position")

    def save(self, *args, **kwargs):
        # Auto update 'last_update' value on each save
        self.last_update = timezone.now()
        self.version = self.version + 1

        super().save(*args, **kwargs)
