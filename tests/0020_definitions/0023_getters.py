import pytest

from canopy.definitions import SlotDefinitionsRegistry


def test_definition_names():
    """
    'names' method should returns all available definition names.
    """
    registry = SlotDefinitionsRegistry()
    assert registry.names() == []

    registry.load("canopy.definitions.tests")
    assert sorted(registry.names()) == ["boolean", "email", "text-simple", "textarea"]


def test_has_definition():
    """
    'has' method check if definition name exists in registry.
    """
    registry = SlotDefinitionsRegistry()
    registry.load("canopy.definitions.tests")
    assert registry.has("boolean") is True
    assert registry.has("nope") is False


def test_get_definition():
    """
    'get' method should returns definition from its name, if it exists else a default
    value.
    """
    registry = SlotDefinitionsRegistry()
    registry.load("canopy.definitions.tests")
    assert registry.get("nope") is None
    assert registry.get("nope", "niet") == "niet"
    assert registry.get("nope", default="niet") == "niet"
    assert registry.get("boolean")["name"] == "Boolean"


def test_get_choices():
    """
    'get_choices' method should returns definition in the same format expected
    for  'choices' field attribute.
    """
    registry = SlotDefinitionsRegistry()
    assert registry.get_choices() == []

    registry.load("canopy.definitions.tests")
    assert registry.get_choices() == [
        ("boolean", "Boolean"),
        ("text-simple", "Simple text"),
        ("email", "Email"),
        ("textarea", "Textarea")
    ]


def test_get_default():
    """
    'get_default' method should returns the default definition that is the first
    item from definition registry.

    This will change once set_default() is implemented in registry.
    """
    registry = SlotDefinitionsRegistry()
    with pytest.raises(IndexError):
        registry.get_default()

    registry.load("canopy.definitions.tests")
    assert registry.get_default() == "boolean"
