"""
Slot definitions
----------------

The base definitions is used as available slot kinds and by the forge to build fields
for given slots.

A definition includes field options parameters and widget options parameters. Option
parameter contains form fields to represent it in Controler form and form fields to
edit it in Slot form.

Slot field and widget are defined directly as classes but never as object instances
since the form forge will instanciate them itself and apply options.
"""
from django import forms
from django.utils.translation import gettext_lazy as _


DEFAULT = "text-simple"


DEFINITIONS = {
    "boolean": {
        "name": _("Boolean"),
        "field": {
            "class": forms.BooleanField,
        },
    },
    "email": {
        "name": _("Email"),
        "field": {
            "class": forms.EmailField,
            "options": {
                "max_length": None,
            },
            # The virtual fields to use for option values edition in Slot admin
            "options_fields": {
                "max_length": forms.IntegerField(
                    min_value=1,
                    max_value=255,
                    required=False
                ),
            },
        },
    },
    # Date format would need to be set, here formatted for the default language.
    # Another definition could be "localized-date" to format depending current
    # language
    "date": {
        "name": _("Date"),
        "field": {
            "class": forms.DateField,
        },
    },
    "text-simple": {
        "name": _("Simple text"),
        "field": {
            "class": forms.CharField,
            "options": {
                "max_length": 255,
            },
            # The virtual fields to use for option values edition in Slot admin
            # TODO: This should be checked or validated to ensure field names does not
            # override any real Slot fields
            "options_fields": {
                "max_length": forms.IntegerField(
                    min_value=1,
                    max_value=255,
                    required=False
                ),
                "strip": forms.BooleanField(required=False),
            },
        },
    },
    "text-multiline": {
        "name": _("Multiline text"),
        "field": {
            "class": forms.CharField,
            "options": {
                "max_length": 3000,
            },
            "options_fields": {},
        },
        "widget": {
            "class": forms.Textarea,
            # NOTE: Pay attention that field and widget options are merged
            # Using the same field name for both field and widget options will make
            # conflict leading to widget options overriding the field options
            "options_fields": {},
        },
    },
}
"""
Definition of slot kinds with their options used to bind form fields.
"""
