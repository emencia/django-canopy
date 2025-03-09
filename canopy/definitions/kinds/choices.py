from django import forms
from django.utils.translation import gettext_lazy as _

from ..base import Kind, KindField, KindWidget


ChoiceListKind = Kind(
    identifier="choice-list",
    name=_("Choice list for a single selection"),
    field=KindField(
        klass=forms.ChoiceField,
        initials={"max_length": 255},
        options={
            "choices": forms.CharField(
                required=True
            ),
        }
    )
)


ChoiceRadioKind = Kind(
    identifier="choice-radio",
    name=_("Radio buttons for a single selection"),
    field=KindField(
        klass=forms.ChoiceField,
        initials={"max_length": 255},
        options={
            "choices": forms.CharField(
                required=True
            ),
        }
    ),
    widget=KindWidget(klass=forms.RadioSelect)
)


MultipleChoiceListKind = Kind(
    identifier="multiple-choice-list",
    name=_("Choice list for multiple selection"),
    field=KindField(
        klass=forms.MultipleChoiceField,
        initials={},
        options={
            "choices": forms.CharField(
                required=True
            ),
        }
    )
)


MultipleChoiceCheckboxKind = Kind(
    identifier="multiple-choice-checkbox",
    name=_("Checkboxes for multiple selection"),
    field=KindField(
        klass=forms.MultipleChoiceField,
        initials={},
        options={
            "choices": forms.CharField(
                required=True
            ),
        }
    ),
    widget=KindWidget(klass=forms.CheckboxSelectMultiple)
)
