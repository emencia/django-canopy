"""
Slot definitions
----------------

The base definitions is used as available slot kinds and by the forge to build fields
from given slots.

A definition includes field options and possibly also widget options.

Slot field and widget are defined directly as classes but never as object instances
since the form forge will instanciate them itself and apply options.

"""
from django import forms
from django.utils.translation import gettext_lazy as _


BASE_DEFINITIONS = {
    # TODO: New definition to implement, more obvious and well structured
    # "foobar": {
    #     "name": _("Boolean"),
    #     "field": {
    #         "class": forms.BooleanField,
    #         "options": {},
    #         "widget": {
    #             "class": forms.Textarea,
    #             "options": {},
    #         },
    #     },
    # },
    "boolean": {
        "name": _("Boolean"),
        "field": forms.BooleanField,
        "field_options": {},
    },
    "email": {
        "name": _("Email"),
        "field": forms.EmailField,
        "field_options": {},
    },
    "date": {
        "name": _("Date"),
        "field": forms.DateField,
        # Date format would need to be set, here formatted for the default language.
        # Another definition could be "localized-date" to format depending current
        # language
        "field_options": {},
    },
    "text-simple": {
        "name": _("Simple text"),
        "field": forms.CharField,
        "field_options": {
            "max_length": 255,
        },
    },
    "text-multiline": {
        "name": _("Multiline text"),
        "field": forms.CharField,
        "field_options": {
            "max_length": 3000,
            "widget": forms.Textarea,
            # "widget_options": {},
        },
    },
}
"""
Definition of slot kinds with their options used to bind form fields.
"""
