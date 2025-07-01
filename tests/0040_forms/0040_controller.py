from freezegun import freeze_time

from django import forms

from canopy.factories import ControllerFactory, SlotFactory
from canopy.forms.forge import FormClassForge


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


def test_form_save_uncommited(db):
    """
    When form validated the field values its save method should return an Entry object
    that include the data but not processed for save when commit is not enabled.
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

    # A dummy entry that is not validated from form
    form = ControllerForm({}, controller=controller)
    assert form.is_valid() is False

    # Data with non required email field with a blank value
    form = ControllerForm({"fullname": "Donald Duck"}, controller=controller)
    assert form.is_valid() is True
    donald = form.save(commit=False)
    assert donald.data == {"fullname": "Donald Duck", "email": ""}

    # Data with all field filled
    form = ControllerForm(
        {"fullname": "Picsou McDuck", "email": "picsou@picsou.com"},
        controller=controller
    )
    assert form.is_valid() is True
    picsou = form.save(commit=False)
    assert picsou.data == {"fullname": "Picsou McDuck", "email": "picsou@picsou.com"}

    # No Entry has been saved because commit was not enabled
    ids = controller.entry_set.all().values_list("id", flat=True).order_by("id")
    assert list(ids) == []


@freeze_time("2012-10-15 10:00:00")
def test_form_save_handler_processing(db, mailoutbox, settings):
    """
    TODO:
    * Validate results from handlers
    * Handlers test (in its own) that will just try to load every available handler
      class to ensure they have no basic errors from definitions.
    """
    settings.ADMINS = [("John", "john@example.com")]

    controller = ControllerFactory(fill_handlers=[
        "canopy.handlers.SendEmailToStaffHandler",
        "canopy.handlers.SaveInDbHandler",
    ])
    SlotFactory(
        controller=controller,
        kind="text-simple",
        label="Full name",
        name="fullname",
        required=True,
    )

    forge = FormClassForge()
    ControllerForm = forge.get_form(controller)

    # Data with all field filled
    form = ControllerForm({"fullname": "Picsou McDuck"}, controller=controller)
    assert form.is_valid() is True
    picsou = form.save(commit=False)
    assert picsou.data == {"fullname": "Picsou McDuck"}

    # Explicitely goes through '_process_handlers' (temporarily?)
    form._process_handlers(picsou)

    # Entry has been saved
    ids = controller.entry_set.all().values_list("id", flat=True).order_by("id")
    assert list(ids) == [picsou.id]

    assert len(mailoutbox) == 1
    sent = mailoutbox[0]

    print("from_email:", sent.from_email)
    print("to:", sent.to)
    print("subject:", sent.subject)
    print(sent.body)

    assert 1 == 42
