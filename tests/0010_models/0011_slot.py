import pytest

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.db import transaction

from canopy.factories import ControllerFactory, SlotFactory
from canopy.models import empty_fresh_dictionnary, Slot


def test_model_basic(settings, db):
    """
    Basic model validation with required fields should not fail.
    """
    controller = ControllerFactory()

    slot = Slot(
        controller=controller,
        label="name",
        name="Name",
        kind="text-simple",
    )
    slot.full_clean()
    slot.save()

    assert Slot.objects.filter(name="Name").count() == 1
    assert slot.name == "Name"


def test_model_required_fields(db):
    """
    Basic model validation with missing required fields should fail.
    """
    slot = Slot()

    with pytest.raises(ValidationError) as excinfo:
        slot.full_clean()

    # import json
    # print(json.dumps(excinfo.value.message_dict, indent=4))
    assert excinfo.value.message_dict == {
        "controller": [
            "This field cannot be null."
        ],
        "label": [
            "This field cannot be blank."
        ],
        "name": [
            "This field cannot be blank."
        ],
    }


def test_factory_basic(db, settings):
    """
    Factory should create Slot object without any required arguments.
    """
    slot = SlotFactory()
    # Force model validation since factory bypass it
    slot.full_clean()
    assert Slot.objects.filter(pk=slot.id).count() == 1


def test_factory_uniqueness(db, settings):
    """
    Slot name and label must be unique within a same controller but possible for other
    controllers.
    """
    controller_1 = ControllerFactory()
    controller_2 = ControllerFactory()

    slot_foo = SlotFactory(controller=controller_1, name="Foo", label="foo")
    slot_foo.full_clean()

    with transaction.atomic():
        with pytest.raises(IntegrityError) as excinfo:
            SlotFactory(controller=controller_1, name="Foo")

        assert str(excinfo.value) == (
            "UNIQUE constraint failed: canopy_slot.controller_id, "
            "canopy_slot.name"
        )

    with transaction.atomic():
        with pytest.raises(IntegrityError) as excinfo:
            SlotFactory(controller=controller_1, label="foo")

        assert str(excinfo.value) == (
            "UNIQUE constraint failed: canopy_slot.controller_id, "
            "canopy_slot.label"
        )

    slot_foo_bis = SlotFactory(controller=controller_2, name="Foo", label="foo")
    slot_foo_bis.full_clean()

    assert Slot.objects.count() == 2


@pytest.mark.parametrize("name, message", [
    ("_plop", "Slot name can not start with underscore character."),
    ("plop-plip", "Slot name must be a valid Python identifier."),
    ("plop plip", "Slot name must be a valid Python identifier."),
    ("1plop", "Slot name must be a valid Python identifier."),
    ("pass", "Slot name can not be a reserved Python keyword."),
    ("False", "Slot name can not be a reserved Python keyword."),
    ("controller", "Slot name can not be a reserved Controller keyword."),
])
def test_name_validation(db, name, message):
    """
    Invalid name should raise a validation error from model.
    """
    slot = SlotFactory(name=name)

    with pytest.raises(ValidationError) as excinfo:
        slot.full_clean()

    assert excinfo.value.message_dict == {"name": [message]}


@pytest.mark.parametrize("value", [
    "{}",
    [],
])
def test_options_validation(db, value):
    """
    Invalid field or widget options value should raise a validation error from model.
    """
    slot = SlotFactory(field_options=value)

    with pytest.raises(ValidationError) as excinfo:
        slot.full_clean()

    assert excinfo.value.message_dict == {
        "field_options": [
            "Slot field options must be a dictionnary."
        ]
    }

    slot = SlotFactory(widget_options=value)

    with pytest.raises(ValidationError) as excinfo:
        slot.full_clean()

    assert excinfo.value.message_dict == {
        "widget_options": [
            "Slot widget options must be a dictionnary."
        ]
    }


def test_options_json(db):
    """
    Demonstrate JSONfield basic behaviors.

    .. Warning::
        This bypass model custom validation or the attempts would fails. This test
        could go to trash if it brings test failures.
    """
    controller = ControllerFactory()

    slot = Slot(
        controller=controller,
        label="name",
        name="Name",
        kind="text-simple",
    )
    slot.full_clean()
    slot.save()
    # Without any value, slot options is an empty dict
    assert isinstance(slot.field_options, dict) is True
    assert slot.field_options == empty_fresh_dictionnary()

    # There is no magic coercing on string
    slot.field_options = "{}"
    # slot.full_clean()
    slot.save()
    assert isinstance(slot.field_options, str) is True

    # Giving proper type like dict is respected and well saved
    slot.field_options = {"plip": "plop"}
    # slot.full_clean()
    slot.save()
    assert isinstance(slot.field_options, dict) is True
    assert slot.field_options["plip"] == "plop"
    # There is not magic attribute getter on the JSON value
    assert hasattr(slot.field_options, "plip") is False
