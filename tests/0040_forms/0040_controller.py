from freezegun import freeze_time

from django import forms

from canopy.factories import ControllerFactory, SlotFactory
from canopy.forms import SlotAdminForm
from canopy.forms.forge import FormClassForge
from canopy.models import Controller, Slot
from canopy.utils.tests import build_post_data_from_object


def test_fields(db):
    """
    Built form should contains all fields from Controller slots.
    """
    controller = ControllerFactory()
    SlotFactory(
        controller=controller,
        kind="text-simple",
        label="Full name",
        name="fullname",
        required=True,
    )
    SlotFactory(
        controller=controller,
        kind="text-simple",
        label="Email",
        name="email",
        required=False,
    )

    forge = FormClassForge()
    ControllerForm = forge.get_form(controller)
    form = ControllerForm(None, controller=controller)

    fields = [
        (k, v.__class__)
        for k, v in form.fields.items()
    ]
    assert fields == [
        ("fullname", forms.CharField),
        ("email", forms.CharField),
    ]


@freeze_time("2012-10-15 10:00:00")
def test_form_save(db):
    """
    Validated data should be saved as an Entry object.
    """
    controller = ControllerFactory()
    SlotFactory(
        controller=controller,
        kind="text-simple",
        label="Full name",
        name="fullname",
        required=True,
    )
    SlotFactory(
        controller=controller,
        kind="text-simple",
        label="Email",
        name="email",
        required=False,
    )

    forge = FormClassForge()
    ControllerForm = forge.get_form(controller)

    # A dummy entry that should not be saved
    form = ControllerForm({"fullname": "Anne Onymous"}, controller=controller)
    assert form.is_valid() is True
    form.save(commit=False)

    # Data with non required email field with a blank value
    form = ControllerForm({"fullname": "Donald Duck"}, controller=controller)
    assert form.is_valid() is True
    donald = form.save()
    assert donald.data == {"fullname": "Donald Duck", "email": ""}

    # Data with all field filled
    form = ControllerForm(
        {"fullname": "Picsou McDuck", "email": "picsou@picsou.com"},
        controller=controller
    )
    assert form.is_valid() is True
    picsou = form.save()
    assert picsou.data == {"fullname": "Picsou McDuck", "email": "picsou@picsou.com"}

    # Only commited objects should exist
    ids = controller.entry_set.all().values_list("id", flat=True).order_by("id")
    assert list(ids) == [donald.id, picsou.id]
