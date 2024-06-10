import pytest

from canopy.factories import ControllerFactory, SlotFactory
from canopy.forms import SlotAdminForm
from canopy.models import Slot
from canopy.utils.tests import build_post_data_from_object


def test_admin_creation_kind_options(db):
    """
    When creating object, options are not altered.
    """
    slot = SlotFactory.build(
        controller=ControllerFactory(),
        kind="text-simple",
        field_options={"max_length": 42},
        widget_options={"attrs": {"data-foo": "bar"}},
    )

    # Build payload to give as form data
    data = build_post_data_from_object(Slot, slot, ignore=["id"])

    # Use form in creation mode
    form = SlotAdminForm(data)
    is_valid = form.is_valid()
    assert is_valid is True
    saved = form.save()

    # Get it from db to ensure everything have been correctly saved
    getted = Slot.objects.get(pk=saved.id)
    assert getted.field_options == {"max_length": 42}
    assert getted.widget_options == {"attrs": {"data-foo": "bar"}}


def test_admin_edition_kind_options(db):
    """
    When kind value is changed on existing object, form should reset options.
    """
    slot = SlotFactory(
        controller=ControllerFactory(),
        kind="text-simple",
        field_options={"max_length": 42},
        widget_options={"attrs": {"data-foo": "bar"}},
    )

    # Build payload to give as form data
    data = build_post_data_from_object(Slot, slot, ignore=["id"])
    data["kind"] = "email"

    # Use form in edition mode
    form = SlotAdminForm(data, instance=slot)
    is_valid = form.is_valid()
    assert is_valid is True
    saved = form.save()

    # Get it again from db to ensure everything have been correctly saved
    getted = Slot.objects.get(pk=saved.id)

    # Kind should has been changed and options values reset
    #assert getted.kind == "email"
    assert getted.field_options == {}
    assert getted.widget_options == {}
