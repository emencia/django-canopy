import pytest

from django.core.exceptions import ValidationError

from canopy.factories import ControllerFactory
from canopy.models import Controller


def test_model_basic(settings, db):
    """
    Basic model validation with required fields should not fail.
    """
    controller = Controller(
        title="Contact",
        slug="contact",
    )
    controller.full_clean()
    controller.save()

    assert Controller.objects.filter(pk=controller.id).count() == 1
    assert controller.title == "Contact"


def test_model_required_fields(db):
    """
    Basic model validation with missing required fields should fail.
    """
    controller = Controller()

    with pytest.raises(ValidationError) as excinfo:
        controller.full_clean()

    # import json
    # print(json.dumps(excinfo.value.message_dict, indent=4))
    assert excinfo.value.message_dict == {
        "title": [
            "This field cannot be blank."
        ],
        "slug": [
            "This field cannot be blank."
        ]
    }


def test_factory_basic(db, settings):
    """
    Factory should create Controller object without any required arguments.
    """
    controller = ControllerFactory()
    # Force model validation since factory bypass it
    controller.full_clean()
    assert Controller.objects.filter(pk=controller.id).count() == 1
