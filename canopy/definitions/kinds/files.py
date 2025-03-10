from django import forms
from django.utils.translation import gettext_lazy as _

from ..base import Kind, KindField, KindWidget


FileKind = Kind(
    identifier="file",
    name=_("File upload"),
    field=KindField(
        klass=forms.FileField,
    ),
    widget=KindWidget(klass=forms.FileInput)
)
