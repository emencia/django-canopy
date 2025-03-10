from canopy.definitions import DefinitionsRegistry
from canopy.definitions.kinds import BooleanKind


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
    registry.load("canopy.definitions.tests")
    assert registry.has("boolean") is True
    assert registry.has("email") is True

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


def test_load_reset():
    """
    Registry can be reset so we can empty the definitions.
    """
    registry = DefinitionsRegistry()

    registry.load((BooleanKind,))
    registry.reset()

    assert registry.definitions == {}
