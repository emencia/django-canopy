from django import forms
from django.utils.translation import gettext_lazy as _

from ..base import Kind, KindField


BooleanKind = Kind(
    identifier="boolean",
    name="Boolean",
    field=KindField(klass=forms.BooleanField)
)
