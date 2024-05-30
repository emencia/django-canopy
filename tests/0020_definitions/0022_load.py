from django import forms

from canopy.definitions import SlotDefinitionsRegistry


def test_load_dict(settings):
    """
    Loading definitions from a dictionnary will properly fill registry.
    """
    registry = SlotDefinitionsRegistry()

    # It is ok to give an empty dict
    registry.load({})
    assert registry.definitions == {}

    registry.load({
        "boolean": {
            "name": "Boolean",
            "field": {
                "class": forms.BooleanField,
            },
        },
    })
    assert registry.has("boolean") is True

    assert sorted(registry.names()) == ["boolean"]


def test_load_module():
    """
    Definitions can be loaded from a module when given as a Python path in a string.
    """
    registry = SlotDefinitionsRegistry()

    # It is ok to give an empty dict
    registry.load("canopy.definitions.tests")
    assert registry.has("boolean") is True
    assert registry.has("email") is True

    assert sorted(registry.names()) == ["boolean", "email", "text-simple", "textarea"]


def test_load_reset():
    """
    Registry can be reset so we can empty the definitions.
    """
    registry = SlotDefinitionsRegistry()

    registry.load({
        "boolean": {
            "name": "Boolean",
            "field": {
                "class": forms.BooleanField,
            },
        },
    })
    registry.reset()

    assert registry.definitions == {}
