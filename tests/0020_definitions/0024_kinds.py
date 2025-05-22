from canopy.definitions import DefinitionsRegistry


def test_get_definition_initials():
    """
    Method should returns field options initial values for given kind.
    """
    registry = DefinitionsRegistry()
    registry.load("canopy.definitions.defaults")

    assert registry.get_definition_initials("boolean") == {}

    assert registry.get_definition_initials("textarea") == {"max_length": 3000}


def test_get_definition_options():
    """
    Method should returns field options for given kind.
    """
    registry = DefinitionsRegistry()
    registry.load("canopy.definitions.defaults")

    assert registry.get_definition_options("field", "boolean") == {}

    options = registry.get_definition_options("field", "email")

    assert options["max_length"].__class__.__name__ == "IntegerField"
