"""
Slot definitions
----------------

A definition is a shortand to a specific field behaviors with pre-defined options, not
only a simple form field.

"""
from django import forms
from django.utils.translation import gettext_lazy as _


BASE_DEFINITIONS = {
    "text-simple": {
        "name": _("Simple text"),
        "field": forms.CharField,
        "kwargs": {
            "max_length": 255,
        },
    },
    "text-multiline": {
        "name": _("Multiline text"),
        "field": forms.CharField,
        "kwargs": {
            "max_length": 3000,
            "widget": forms.Textarea,
        },
    },
    "date": {
        "name": _("Date"),
        "field": forms.DateField,
        # Date format would need to be set, here formatted for the default language.
        # Another definition could be "localized-date" to format depending current
        # language
        "kwargs": {},
    },
}
"""
Definition of slot kinds with their options used to bind form fields.
"""
