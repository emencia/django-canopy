from canopy.definitions import DefinitionsRegistry


def test_get_kind_attr_initials():
    """
    Method should returns field options initial values for given kind.
    """
    registry = DefinitionsRegistry()
    registry.load("canopy.definitions.defaults")

    assert registry.get_kind_attr_initials("boolean") == {}

    assert registry.get_kind_attr_initials("textarea") == {"max_length": 3000}


def test_get_kind_attr_options():
    """
    Method should returns field options for given kind.
    """
    registry = DefinitionsRegistry()
    registry.load("canopy.definitions.defaults")

    assert registry.get_kind_attr_options("field", "boolean") == {}

    options = registry.get_kind_attr_options("field", "email")

    assert options["max_length"].__class__.__name__ == "IntegerField"
