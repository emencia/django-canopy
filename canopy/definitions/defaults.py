from .kinds import (
    BooleanKind,
    ChoiceListKind,
    ChoiceRadioKind,
    DateKind,
    DatetimeKind,
    DecimalKind,
    EmailKind,
    FileKind,
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
    FileKind,
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
Default Kind definition objects enable every available kinds.
"""
