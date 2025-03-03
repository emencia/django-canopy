from django import forms
from django.utils.translation import gettext_lazy as _

from ..base import Kind, KindField


DateKind = Kind(
    identifier="date",
    name=_("Date"),
    field=KindField(klass=forms.DateField)
)
