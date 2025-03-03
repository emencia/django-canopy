from django import forms
from django.utils.translation import gettext_lazy as _

from ..base import Kind, KindField, KindWidget


TextKind = Kind(
    identifier="text-simple",
    name=_("Simple text"),
    field=KindField(
        klass=forms.CharField,
        initials={"max_length": 255},
        options={
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
    name=_("Email"),
    field=KindField(
        klass=forms.EmailField,
        options={
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
    name=_("Textarea"),
    field=KindField(
        klass=forms.CharField,
        initials={"max_length": 3000}
    ),
    widget=KindWidget(klass=forms.Textarea)
)
