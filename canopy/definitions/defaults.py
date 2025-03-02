"""
Slot definitions
----------------

The base definitions is used as available slot kinds and by the forge to build fields
for given slots.

A definition includes field options parameters and widget options parameters. Option
parameter contains form fields to represent it in Controler form and form fields to
edit it in Slot form.

The purpose is to use Django form fields and widgets to manage value for the Slot
options, it means Slot options will be managed throught virtual fields. Since this
change to Slot kind to another, we store the option value in a JSON fields.

Slot field and widget are defined directly as classes but never as object instances
since the form forge will instanciate them itself and apply options.
"""
from django import forms
from django.utils.translation import gettext_lazy as _


DEFAULT = "text-simple"


# Unused sample of a full featured Slot kind definition
# NOTE: 'options' and 'options_fields' should have be named 'attributes' and
# 'attributes_fields', it better defines their nature and purpose
DOCTYPE = {
    # Unique kind name
    "text-multiline": {
        # Kind always have a display name
        "name": _("Multiline text"),
        # Kind always have a 'field' item to define the Django form field to use
        "field": {
            # Class object is always required
            "class": forms.CharField,
            # Options are optional, these will be the Django form field attributes
            "options": {
                "max_length": 200,
            },
            # These are the optional form field to manage the slot field options from
            # admin.
            "options_fields": {
                "max_length": forms.IntegerField(
                    min_value=1,
                    max_value=255,
                    required=False
                ),
            },
        },
        # 'widget' is optional and it would allow to define a different widget than the
        # default one from a Django form field
        "widget": {
            # Class object is always required
            "class": forms.Textarea,
            # These are the optional form field to manage the slot widget options from
            # admin.
            # NOTE: Pay attention that field and widget options are merged
            # Using the same field name for both field and widget options will make
            # conflict leading to widget options overriding the field options
            "options_fields": {},
        },
    },
}


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
