import pytest

from django import forms

from canopy.definitions import SlotDefinitionsRegistry
from canopy.factories import ControllerFactory, SlotFactory
from canopy.exceptions import DefinitionRegistryError


def test_get_kind_definition(db):
    """
    'get_kind_definition' method should returns definition from given name, if any.
    """
    registry = SlotDefinitionsRegistry()

    # There is not any available definition and so no default
    with pytest.raises(IndexError):
        registry.get_kind_definition()

    registry.load({
        "boolean": {
            "name": "Boolean",
            "field": {
                "class": forms.BooleanField,
            },
        },
    })
    assert registry.get_kind_definition()["name"] == "Boolean"

    registry.load({
        "dummy": {
            "name": "Dummy",
            "field": {
                "class": forms.CharField,
            },
        },
    })

    assert registry.get_kind_definition()["name"] == "Boolean"

    assert registry.get_kind_definition("dummy")["name"] == "Dummy"


@pytest.mark.skip("Do not work yet since model does not use registry yet")
def test_get_kind_definition_from_controller(db):
    registry = SlotDefinitionsRegistry()

    slot_foo = SlotFactory(controller=ControllerFactory(), kind="dummy")
    slot_foo.full_clean()

    assert registry.get_kind_definition("dummy")["name"] == "Dummy"


def test_get_kind_field_options_initials():
    """
    Method should returns field options initial values for given kind.
    """
    registry = SlotDefinitionsRegistry()
    registry.load("canopy.definitions.tests")

    assert registry.get_kind_field_options_initials("boolean") == {}

    assert registry.get_kind_field_options_initials("textarea") == {"max_length": 3000}


def test_get_kind_field_options():
    """
    Method should returns field options for given kind.
    """
    registry = SlotDefinitionsRegistry()
    registry.load("canopy.definitions.tests")

    assert registry.get_kind_field_options("boolean") == {}

    options = registry.get_kind_field_options("field", "email")

    assert options["max_length"].__class__.__name__ == "IntegerField"
