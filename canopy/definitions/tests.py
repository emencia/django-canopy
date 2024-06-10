"""
Default definitions used in tests. It only involves a few set of definitions and it is
not intended to be used outside of tests.
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
    "text-simple": {
        "name": _("Simple text"),
        "field": {
            "class": forms.CharField,
            "options": {
                "max_length": 255,
            },
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
    "email": {
        "name": _("Email"),
        "field": {
            "class": forms.EmailField,
            "options": {
                # Seems useless since empty won't change input in Controller form
                # render or on Slot form options fields.
                # "max_length": None,
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
    "textarea": {
        "name": _("Textarea"),
        "field": {
            "class": forms.CharField,
            "options": {
                "max_length": 3000,
            },
            "options_fields": {},
        },
        "widget": {
            "class": forms.Textarea,
            "options_fields": {},
        },
    },
}
"""
Definition of slot kinds with their options used to bind form fields.
"""
