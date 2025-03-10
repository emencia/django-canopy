"""
TODO:  This should be removed, it is useless since it enable the sames than 'defaults'
and there is no reasons anymore to limit the test definitions because we want to test
them ALL.
"""
from .kinds import (
    BooleanKind,
    ChoiceListKind,
    ChoiceRadioKind,
    DateKind,
    DatetimeKind,
    DecimalKind,
    EmailKind,
    IntegerKind,
    IPAddressKind,
    IP4AddressKind,
    IP6AddressKind,
    MultipleChoiceListKind,
    MultipleChoiceCheckboxKind,
    TextKind,
    TextareaKind,
    TimeKind,
)


DEFAULT = "text-simple"
"""
Default kind is defined with its ``name`` attribute value.
"""


DEFINITIONS = (
    BooleanKind,
    ChoiceListKind,
    ChoiceRadioKind,
    DateKind,
    DatetimeKind,
    DecimalKind,
    EmailKind,
    IntegerKind,
    IPAddressKind,
    IP4AddressKind,
    IP6AddressKind,
    MultipleChoiceListKind,
    MultipleChoiceCheckboxKind,
    TextKind,
    TextareaKind,
    TimeKind,
)
"""
Kind definition objects enable every available kinds.
"""
