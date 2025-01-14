import pytest

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.db import transaction

from canopy.factories import ControllerFactory, SlotFactory
from canopy.models import Slot


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
            "This field cannot be blank."
        ],
        "kind": [
            "This field cannot be blank."
        ],
        "label": [
            "This field cannot be blank."
        ],
        "name": [
            "This field cannot be blank."
        ]
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
