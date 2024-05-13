from freezegun import freeze_time

from canopy.forms.forge import FormClassForge
from canopy.factories import ControllerFactory, SlotFactory


@freeze_time("2012-10-15 10:00:00")
def test_form_save(db):
    """
    Valid submited data should be saved as Entry object.
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
