from django import forms

from dataclasses import field
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class KindField:
    """
    Kind field declare what Django form field to use for a slot
    """
    klass: type(forms.Field)
    # Previously named 'options'
    initials: dict = field(default_factory=dict)
    # Previously named 'options_fields'
    options: dict = field(default_factory=dict)


@dataclass(frozen=True)
class KindWidget:
    """
    Kind field declare what Django form widget to use for a Django form a field from
    a KindField.

    Opposed to KindField, there is no ``initials`` since a Widget itself does
    not have initial value.
    """
    klass: type(forms.MediaDefiningClass)
    options: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Kind:
    """
    Slot kind definition
    """
    identifier: str
    name: str
    field: KindField
    widget: KindWidget = field(default=None)
