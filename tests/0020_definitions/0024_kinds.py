import pytest

from canopy.definitions import DefinitionsRegistry
from canopy.factories import ControllerFactory, SlotFactory


@pytest.mark.skip("Do not work yet since model does not use registry yet")
def test_get_kind_definition_from_controller(db):
    registry = DefinitionsRegistry()

    slot_foo = SlotFactory(controller=ControllerFactory(), kind="dummy")
    slot_foo.full_clean()

    assert registry.get_definition("dummy").name == "Dummy"


def test_get_kind_field_initials():
    """
    Method should returns field options initial values for given kind.
    """
    registry = DefinitionsRegistry()
    registry.load("canopy.definitions.tests")

    assert registry.get_kind_field_initials("boolean") == {}

    assert registry.get_kind_field_initials("textarea") == {"max_length": 3000}


def test_get_kind_field_options():
    """
    Method should returns field options for given kind.
    """
    registry = DefinitionsRegistry()
    registry.load("canopy.definitions.tests")

    assert registry.get_kind_field_options("field", "boolean") == {}

    options = registry.get_kind_field_options("field", "email")

    assert options["max_length"].__class__.__name__ == "IntegerField"
