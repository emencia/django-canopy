import pytest

from canopy.definitions import SlotDefinitionsRegistry
from canopy.exceptions import DefinitionRegistryError


def test_check_definitions():
    """
    Definitions check should raise exception with errors.
    """
    registry = SlotDefinitionsRegistry()

    # It is ok to give an empty dict
    assert registry.check_definitions({}) is True

    with pytest.raises(DefinitionRegistryError) as excinfo:
        registry.check_definitions({"foo": "plop"})

    assert str(excinfo.value) == "Some definitions have errors."
    assert excinfo.value.get_payload_details() == [
        "foo: value must be a dictionnary.",
    ]

    with pytest.raises(DefinitionRegistryError) as excinfo:
        registry.check_definitions({
            "foo": {},
            "bar": {
                "field": {},
                "widget": {},
            },
            "yep": {
                "name": "Yep",
                "field": {"class": "value is not checked"},
                "widget": {"class": "value is not checked"},
            },
        })

    assert excinfo.value.get_payload_details() == [
        "foo: is missing 'name' item.",
        "foo: is missing 'field' item.",
        "bar: is missing 'name' item.",
        "bar: 'field' is missing 'class' item.",
        "bar: 'widget' is missing 'class' item.",
    ]
