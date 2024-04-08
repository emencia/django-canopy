import pytest

from django.core.exceptions import ValidationError

from canopy.factories import ControllerFactory, EntryFactory
from canopy.models import Entry


def test_model_basic(settings, db):
    """
    Basic model validation with required fields should not fail.
    """
    controller = ControllerFactory()

    entry = Entry(
        controller=controller,
        data="{}",
    )
    entry.full_clean()
    entry.save()

    assert Entry.objects.filter(pk=entry.id).count() == 1


def test_model_required_fields(db):
    """
    Basic model validation with missing required fields should fail.
    """
    entry = Entry()

    with pytest.raises(ValidationError) as excinfo:
        entry.full_clean()

    # import json
    # print(json.dumps(excinfo.value.message_dict, indent=4))
    assert excinfo.value.message_dict == {
        "controller": [
            "This field cannot be blank."
        ],
        "data": [
            "This field cannot be blank."
        ]
    }


def test_factory_basic(db, settings):
    """
    Factory should create Entry object without any required arguments.
    """
    entry = EntryFactory()
    # Force model validation since factory bypass it
    entry.full_clean()
    assert Entry.objects.filter(pk=entry.id).count() == 1
