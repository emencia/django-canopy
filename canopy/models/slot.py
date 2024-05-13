from keyword import iskeyword

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..choices import get_kind_choices, get_kind_default


# Reserved controller keywords to not override form class properties/methods, it should
# include also the ones from 'forms.Form'
FORBIDDEN_SLOT_NAMES = ("controller", "save")


def empty_fresh_dictionnary():
    return {}


class Slot(models.Model):
    """
    Slot defines a field for a Controller, generally a form input.
    """
    controller = models.ForeignKey(
        "canopy.controller",
        on_delete=models.CASCADE,
    )
    """
    Required controller relation.
    """

    kind = models.CharField(
        _("element type"),
        max_length=50,
        choices=get_kind_choices(),
        default=get_kind_default(),
    )
    """
    Required slot kind string. Determine the kind of slot.
    """

    label = models.CharField(
        _("field label"),
        max_length=100,
    )
    """
    Required label string. This is the label showed to users. Label is unique for a
    same controller.
    """

    name = models.CharField(
        _("field name"),
        max_length=100,
    )
    """
    Required name string. This is the input name used in HTML and slot
    representation. Name is unique for a same controller.
    """

    required = models.BooleanField(
        verbose_name=_("required"),
        default=False,
        blank=True,
    )
    """
    Optional boolean to make slot required.
    """

    position = models.IntegerField(
        _("position"),
        default=0
    )
    """
    Required position order in slot list.
    """

    help_text = models.TextField(_("help text"), blank=True, null=False)
    """
    Optional help text to show.
    """

    initial = models.CharField(
        _("initial"),
        blank=True,
        max_length=100,
    )
    """
    Optional initial value.
    """

    field_options = models.JSONField(blank=True, default=empty_fresh_dictionnary)
    """
    Optional JSON value to hold input extra options.
    """

    widget_options = models.JSONField(blank=True, default=empty_fresh_dictionnary)
    """
    Optional JSON value to hold widget extra options.
    """

    class Meta:
        ordering = ["label"]
        verbose_name = _("Form slot")
        verbose_name_plural = _("Form slots")
        constraints = [
            models.UniqueConstraint(
                name="canopy_unique_slot_label",
                fields=["controller", "label"],
            ),
            models.UniqueConstraint(
                name="canopy_unique_slot_name",
                fields=["controller", "name"],
            ),
        ]

    def __str__(self):
        return self.label

    def clean_fields(self, exclude=None):
        """
        Apply custom validation on field, especially for the ``name`` value.

        TODO:
        Current name field value validation is possibly not enough, a name can
        actually be something from ``forms.Form``. We could use dir() on 'forms.Form'
        and reserve everything that does not start with '_'.

        By the way, the documentation should have a dedicated part to list all the
        rules for slot name in a comprehensive way so it can be used for users.
        """
        super().clean_fields(exclude=exclude)

        if self.name.startswith("_"):
            raise ValidationError({
                "name": _("Slot name can not start with underscore character."),
            })

        if not self.name.isidentifier():
            raise ValidationError({
                "name": _("Slot name must be a valid Python identifier."),
            })

        if iskeyword(self.name):
            raise ValidationError({
                "name": _("Slot name can not be a reserved Python keyword."),
            })

        if self.name in FORBIDDEN_SLOT_NAMES:
            raise ValidationError({
                "name": _("Slot name can not be a reserved Controller keyword."),
            })

        # TODO: Field and widget option JSONs are to be validated with schema
        if not isinstance(self.field_options, dict):
            raise ValidationError({
                "field_options": _(
                    "Slot field options must be a dictionnary."
                ),
            })

        if not isinstance(self.widget_options, dict):
            raise ValidationError({
                "widget_options": _(
                    "Slot widget options must be a dictionnary."
                ),
            })
