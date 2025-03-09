from django import forms
from django.utils.translation import gettext_lazy as _

from ..base import Kind, KindField


DateKind = Kind(
    identifier="date",
    name=_("Date"),
    field=KindField(klass=forms.DateField)
)


DatetimeKind = Kind(
    identifier="datetime",
    name=_("Date and time"),
    field=KindField(klass=forms.DateTimeField)
)


TimeKind = Kind(
    identifier="time",
    name=_("Time"),
    field=KindField(klass=forms.TimeField)
)
