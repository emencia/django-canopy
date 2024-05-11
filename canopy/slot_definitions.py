"""
Slot definitions
----------------

The base definitions is used as available slot kinds and by the forge to build fields
for given slots.

A definition includes field parameters and possibly also widget parameters.

Slot field and widget are defined directly as classes but never as object instances
since the form forge will instanciate them itself and apply options.

"""
from django import forms
from django.utils.translation import gettext_lazy as _


BASE_DEFINITIONS = {
    "boolean": {
        "name": _("Boolean"),
        "field": {
            "class": forms.BooleanField,
            "options": {},
        },
    },
    "email": {
        "name": _("Email"),
        "field": {
            "class": forms.EmailField,
            "options": {},
        },
    },
    # Date format would need to be set, here formatted for the default language.
    # Another definition could be "localized-date" to format depending current
    # language
    "date": {
        "name": _("Date"),
        "field": {
            "class": forms.DateField,
            "options": {},
        },
    },
    "text-simple": {
        "name": _("Simple text"),
        "field": {
            "class": forms.CharField,
            "options": {
                "max_length": 255,
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
        },
        "widget": {
            "class": forms.Textarea,
            "options": {},
        },
    },
}
"""
Definition of slot kinds with their options used to bind form fields.
"""
