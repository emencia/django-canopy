"""
Slot definitions
----------------

The base definitions is used as available slot kinds and by the forge to build fields
for given slots.

A definition includes field parameters, widget parameters and a validation schema for
field and widget.

Slot field and widget are defined directly as classes but never as object instances
since the form forge will instanciate them itself and apply options.

Validation schemas are implemented with the Python library ``schema`` and are used
to validate the JSON content in field and widget options.

.. Todo::
    Definitions needs to be validated, either automatically from Django system check
    or a commandline, or whatever.

    * All definition must have a "name" and "field" items.
    * Field item must have a "class" item;
    * If widget item exists, it must include a "class" item;
    * If field or widget have an "options" item it must be followed with a "schema"
      item non-empty or identical to the options structure (if options have max_length,
      schema must have it too, and schema must not have item for undefined options;

TODO: Hold on !
https://github.com/emencia/django-canopy/issues/5#issuecomment-2109766420

"""
from django import forms
from django.utils.translation import gettext_lazy as _

from schema import And, Or, Optional


BASE_DEFINITIONS = {
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
            "schema": {
                Optional("max_length"): And(int, lambda n: n > 0),
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
            "schema": {
                Optional("max_length"): And(int, lambda n: n > 0),
            }
        },
    },
    "text-multiline": {
        "name": _("Multiline text"),
        "field": {
            "class": forms.CharField,
            "options": {
                "max_length": 3000,
            },
        },
        "widget": {
            "class": forms.Textarea,
        },
    },
}
"""
Definition of slot kinds with their options used to bind form fields.
"""
