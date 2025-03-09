from django import forms
from django.utils.translation import gettext_lazy as _

from ..base import Kind, KindField


IntegerKind = Kind(
    identifier="integer",
    name=_("Integer"),
    field=KindField(
        klass=forms.IntegerField,
        options={
            "min_value": forms.IntegerField(required=False),
            "max_value": forms.IntegerField(required=False),
            "step_size": forms.IntegerField(required=False)
        }
    )
)


DecimalKind = Kind(
    identifier="decimal",
    name=_("Decimal"),
    field=KindField(
        klass=forms.DecimalField,
        options={
            "min_value": forms.IntegerField(required=False),
            "max_value": forms.IntegerField(required=False),
            "decimal_places": forms.IntegerField(required=False),
            "step_size": forms.IntegerField(required=False)
        }
    )
)
