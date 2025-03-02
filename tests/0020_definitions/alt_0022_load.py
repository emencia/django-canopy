from django import forms

from canopy.definitions.alt_init import DefinitionsRegistry
from canopy.definitions.slots import Kind, KindField, KindWidget
from canopy.definitions.kinds import BooleanKind, EmailKind, TextareaKind, TextKind


def test_load_dict(settings):
    """
    Loading definitions from a dictionnary will properly fill registry.
    """
    registry = DefinitionsRegistry()

    # It is ok to give an empty dict
    registry.load(())
    assert registry.definitions == {}

    registry.load((BooleanKind,))
    assert registry.has("nope") is False
    assert registry.has("boolean") is True

    assert sorted(registry.names()) == ["boolean"]


def test_load_module():
    """
    Definitions can be loaded from a module when given as a Python path in a string.
    """
    registry = DefinitionsRegistry()

    # It is ok to give an empty dict
    registry.load("canopy.definitions.alt_tests")
    assert registry.has("boolean") is True
    assert registry.has("email") is True

    assert sorted(registry.names()) == ["boolean", "email", "text-simple", "textarea"]


def test_load_reset():
    """
    Registry can be reset so we can empty the definitions.
    """
    registry = DefinitionsRegistry()

    registry.load((BooleanKind,))
    registry.reset()

    assert registry.definitions == {}
