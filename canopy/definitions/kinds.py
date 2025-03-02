from django import forms
from django.utils.translation import gettext_lazy as _

from .slots import Kind, KindField, KindWidget


BooleanKind = Kind(
    identifier="boolean",
    name="Boolean",
    field=KindField(klass=forms.BooleanField)
)


TextKind = Kind(
    identifier="text-simple",
    name="Simple text",
    field=KindField(
        klass=forms.CharField,
        attributes_initials={"max_length": 255},
        attributes_fields={
            "max_length": forms.IntegerField(
                min_value=1,
                max_value=255,
                required=False
            ),
            "strip": forms.BooleanField(required=False)
        }
    )
)


EmailKind = Kind(
    identifier="email",
    name="Email",
    field=KindField(
        klass=forms.EmailField,
        attributes_fields={
            "max_length": forms.IntegerField(
                min_value=1,
                max_value=255,
                required=False
            )
        }
    )
)


TextareaKind = Kind(
    identifier="textarea",
    name="Textarea",
    field=KindField(
        klass=forms.CharField,
        attributes_initials={"max_length": 3000}
    ),
    widget=KindWidget(klass=forms.Textarea)
)
