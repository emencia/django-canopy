from keyword import iskeyword

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from canopy.definitions.registry import get_registry
registry = get_registry()


# Reserved controller keywords to not override form class properties/methods, it may
# includes also the ones from 'forms.Form'
FORBIDDEN_SLOT_NAMES = ("controller", "save")


def empty_fresh_dictionnary():
    """
    A shortand to return a simple empty dictionnary ensured to not be shared and avoid
    mutation between definitions.
    """
    return {}


class Slot(models.Model):
    """
    Slot defines a field for a Controller, generally a form input.

    NOTE: Documentation should have a dedicated part to list all the
    rules for slot name in a comprehensive way so it can be used for users.
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
        choices=registry.get_choices(),
        default=registry.get_default(),
        help_text=_(
            "If you change this after initial save, all field and widget options "
            "will be lost."
        ),
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
    Optional JSON value to hold option input values.
    """

    widget_options = models.JSONField(blank=True, default=empty_fresh_dictionnary)
    """
    Optional JSON value to hold option widget values.
    """

    class Meta:
        ordering = ["label"]
        verbose_name = _("Controller slot")
        verbose_name_plural = _("Controllers slots")
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
        super().clean_fields(exclude=exclude)

        self.clean_name()
        self.clean_field_options()
        self.clean_widget_options()

    def clean_name(self):
        """
        Apply validation for the ``name`` value.

        .. Note::
            We don't need to validate conflict between field names and ``forms.Form``
            attributes since field are not set as attribute in final form class see
            ``django.forms.DeclarativeFieldsMetaclass.__new__()`` for details.
        """
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

    def clean_field_options(self):
        """
        NOTE: Registry would have to validate values against field options from the
        slot kind definition
        """
        if not isinstance(self.field_options, dict):
            raise ValidationError({
                "field_options": _(
                    "Slot field options must be a dictionnary."
                ),
            })

    def clean_widget_options(self):
        """
        NOTE: Registry would have to validate values against widget options from the
        slot kind definition
        """
        if not isinstance(self.widget_options, dict):
            raise ValidationError({
                "widget_options": _(
                    "Slot widget options must be a dictionnary."
                ),
            })
