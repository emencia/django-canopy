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
    assert sorted(registry.names()) == [
        "boolean",
        "choice-list",
        "choice-radio",
        "date",
        "datetime",
        "decimal",
        "email",
        "integer",
        "ip-address",
        "ip4-address",
        "ip6-address",
        "multiple-choice-checkbox",
        "multiple-choice-list",
        "text-simple",
        "textarea",
        "time",
    ]


def test_has_kind_definition():
    """
    'has' method check if definition name exists in registry.
    """
    registry = DefinitionsRegistry()
    registry.load("canopy.definitions.tests")
    assert registry.has("boolean") is True
    assert registry.has("nope") is False


def test_get_definition_from_controller(db):
    """
    'get_definition' method returns the definition for given kind.
    """
    registry = DefinitionsRegistry()
    registry.load("canopy.definitions.tests")

    # Without argument, the default definition is returned
    default_def = registry.get_definition()
    assert default_def.identifier == registry.get_default()

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
        ("choice-list", "Choice list for a single selection"),
        ("choice-radio", "Radio buttons for a single selection"),
        ("date", "Date"), ("datetime", "Date and time"),
        ("decimal", "Decimal"),
        ("email", "Email"),
        ("integer", "Integer"),
        ("ip-address", "IPv4 or IPv6 address"),
        ("ip4-address", "IPv4 address"), ("ip6-address", "IPv6 address"),
        ("multiple-choice-list", "Choice list for multiple selection"),
        ("multiple-choice-checkbox", "Checkboxes for multiple selection"),
        ("text-simple", "Simple text"),
        ("textarea", "Textarea"),
        ("time", "Time"),
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


def test_get_kind_attr_options(db):
    """
    'get_kind_attr_options' method field or widget options for given kind
    """
    registry = DefinitionsRegistry()
    registry.load("canopy.definitions.tests")

    controller = ControllerFactory()
    slot = SlotFactory(controller=controller, kind="text-simple")
    field_fields = registry.get_kind_attr_options("field", kind=slot.kind)

    assert "max_length" in field_fields
    assert "strip" in field_fields
