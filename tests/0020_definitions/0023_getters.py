import pytest

from canopy.definitions import DefinitionsRegistry
from canopy.factories import ControllerFactory, SlotFactory
from canopy.exceptions import DefinitionRegistryError


def test_definition_names():
    """
    'names' method should returns all available definition names.
    """
    registry = DefinitionsRegistry()
    assert registry.names() == []

    registry.load("canopy.definitions.tests")
    assert sorted(registry.names()) == ["boolean", "email", "text-simple", "textarea"]


def test_has_kind_definition():
    """
    'has' method check if definition name exists in registry.
    """
    registry = DefinitionsRegistry()
    registry.load("canopy.definitions.tests")
    assert registry.has("boolean") is True
    assert registry.has("nope") is False


def test_get_definition():
    """
    'get' method should returns definition from its name, if it exists else a default
    value.
    """
    registry = DefinitionsRegistry()
    registry.load("canopy.definitions.tests")

    assert registry.get("nope") is None
    assert registry.get("nope", "niet") == "niet"
    assert registry.get("nope", default="niet") == "niet"
    assert registry.get("boolean").name == "Boolean"


def test_get_definition_from_controller(db):
    """
    'get_definition' method returns the definition for given kind.
    """
    registry = DefinitionsRegistry()
    registry.load("canopy.definitions.tests")

    # Without argument, the default definition is returned
    default_def = registry.get_definition()
    assert default_def.name == registry.get(registry.get_default()).name

    controller = ControllerFactory()
    slot = SlotFactory(controller=controller, kind="text-simple")
    text_def = registry.get_definition(kind=slot)
    assert text_def.name == "Simple text"


def test_get_choices():
    """
    'get_choices' method should returns definition in the same format expected
    for  'choices' field attribute.
    """
    registry = DefinitionsRegistry()
    assert registry.get_choices() == []

    registry.load("canopy.definitions.tests")
    assert registry.get_choices() == [
        ("boolean", "Boolean"),
        ("email", "Email"),
        ("textarea", "Textarea"),
        ("text-simple", "Simple text"),
    ]


def test_get_set_default():
    """
    'get_default' method should returns the default definition. Also there is different
    way to define the default value.
    """
    registry = DefinitionsRegistry()

    # Empty registry does not have any default kind
    with pytest.raises(IndexError):
        registry.get_default()

    # Definitions module can define a default kind
    registry.load("canopy.definitions.tests")
    assert registry.get_default() == "text-simple"

    # Default kind can also be defined directly from loader, overriding possible
    # default from module
    registry.reset()
    registry.load("canopy.definitions.tests", default="boolean")
    assert registry.get_default() == "boolean"

    # A specific method allow to define a default kind without loader
    registry.set_default("email")
    assert registry.get_default() == "email"

    # Default value must be a registered definition key name
    with pytest.raises(DefinitionRegistryError):
        registry.set_default("nope")


def test_get_kind_field_options(db):
    """
    'get_kind_field_options' method field or widget options for given kind
    """
    registry = DefinitionsRegistry()
    registry.load("canopy.definitions.tests")

    controller = ControllerFactory()
    slot = SlotFactory(controller=controller, kind="text-simple")
    field_fields = registry.get_kind_field_options("field", kind=slot.kind)

    assert "max_length" in field_fields
    assert "strip" in field_fields
