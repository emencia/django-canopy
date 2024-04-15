"""
Choices for model fields and their getters.

* ``get_***_choices()`` is to list available choices;
* ``get_***_default()`` is to get default choice, this is the first item from available
  choices;

You can not add, edit or remove entries just like that or it may result to data loss.

Migration that include fields that use these choices will need to be rewritten to use
these getters instead of Django hardcoded choice list and default.
"""
from .slot_definitions import BASE_DEFINITIONS


CANOPY_SLOT_KIND_CHOICES = [
    (k, v["name"])
    for k, v in BASE_DEFINITIONS.items()
]


def get_kind_choices():
    return CANOPY_SLOT_KIND_CHOICES


def get_kind_default():
    return CANOPY_SLOT_KIND_CHOICES[0][0]
