from typing import Union, Any

from django import forms

from dataclasses import field
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class KindField:
    """
    Object to declare the Django form field to use for a slot.

    Attributes:
        klass (class): A Django form field class object.
        initials (dict): Initials values for field attributes.
        options (dict): Form fields to manage slot field options.
    """
    klass: type(forms.Field)
    # Previously named 'options'
    initials: dict = field(default_factory=dict)
    # Previously named 'options_fields'
    options: dict = field(default_factory=dict)


@dataclass(frozen=True)
class KindWidget:
    """
    Object to declare the Django form widget to use for a slot field.

    Attributes:
        klass (class): A Django form field class object.
        initials (dict): Initials values for field attributes.
    """
    klass: type(forms.MediaDefiningClass)
    options: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Kind:
    """
    Slot kind definition

    .. Todo::
        We currently use ``Any`` for ``name`` attribute since ``gettext_lazy`` is a
        proxy function that i can't get to work with Pydantic yet.

    Attributes:
        identifier (string): Unique identifier amongst all kinds. Used to index and
            retrieve the kind in the registry.
        name (Any): Label name. This expect a string or a translatable string (gettext).
        field (KindField): The Kind field object.
        widget (KindWidget): The Kind widget object.
    """
    identifier: str
    name: Union[str, Any]
    field: KindField
    widget: KindWidget = field(default=None)
