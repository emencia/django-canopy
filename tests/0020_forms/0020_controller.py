from django import forms

from freezegun import freeze_time

from canopy.forms.forge import FormClassForge
from canopy.factories import ControllerFactory, SlotFactory
from canopy.models import Entry
from canopy.utils.tests import flatten_form_errors, html_pyquery


def test_construct_form_class_with_type():
    """
    Demonstrate usage of ``type()`` to build class with given arguments. It is
    the way to programmatically build a form class.
    """
    attrs = {
        "your-name": forms.CharField(max_length=50, required=True),
        "your-number": forms.IntegerField(min_value=5, max_value=15),
    }

    # Build a concrete form using type() and giving fields as attributes instead of
    # defining them into class
    DummyForm = type("DummyForm", (forms.Form,), attrs)

    f = DummyForm()
    # print(f.as_p())

    # Check form is valid
    validation = f.is_valid()
    assert validation is False
    assert flatten_form_errors(f) == {}

    # The given fields should be there
    assert ("id_your-name" in f.as_p()) is True
    assert ("id_your-number" in f.as_p()) is True


def test_get_slot_scheme_from_dict():
    """
    Method get_slot_scheme should return a slot scheme from a dict.
    """
    forge = FormClassForge()

    assert forge.get_slot_scheme({
        "foo": {
            "kind": "text-simple",
            "label": "Foo",
            "name": "foo",
            "required": False,
            "position": 1,
            "help_text": "",
            "initial": ""
        },
    }) == {
        "foo": {
            "kind": "text-simple",
            "label": "Foo",
            "name": "foo",
            "required": False,
            "position": 1,
            "help_text": "",
            "initial": ""
        },
    }


def test_get_slot_scheme_from_iterable():
    """
    Method get_slot_scheme should return a slot scheme from an iterable.
    """
    forge = FormClassForge()

    assert forge.get_slot_scheme((
        (
            "foo", {
                "kind": "text-simple",
                "label": "Foo",
                "name": "foo",
                "required": False,
                "position": 1,
                "help_text": "",
                "initial": ""
            },
        ),
    )) == {
        "foo": {
            "kind": "text-simple",
            "label": "Foo",
            "name": "foo",
            "required": False,
            "position": 1,
            "help_text": "",
            "initial": ""
        },
    }


def test_get_slot_scheme_from_controller(db):
    """
    Method should returns a slot scheme from Controller object.
    """
    forge = FormClassForge()

    # Create a controller object with some slot objectss
    controller = ControllerFactory()
    SlotFactory(label="Foo", name="foo", controller=controller, position=1)
    SlotFactory(label="Bar", name="bar", controller=controller, position=2)

    assert forge.get_slot_scheme(controller) == {
        "foo": {
            "kind": "text-simple",
            "label": "Foo",
            "name": "foo",
            "required": False,
            "position": 1,
            "help_text": "",
            "initial": ""
        },
        "bar": {
            "kind": "text-simple",
            "label": "Bar",
            "name": "bar",
            "required": False,
            "position": 2,
            "help_text": "",
            "initial": ""
        }
    }


def test_get_form_fields(settings):
    """
    Method should return a dict of form fields built from given slot scheme.
    """
    forge = FormClassForge()

    # Directly from a dict
    definitions = forge.get_definitions()
    fields = forge.get_form_fields(
        definitions,
        {
            "foo": {
                "kind": "text-simple",
                "label": "Foo",
                "name": "foo",
                "required": False,
                "position": 1,
                "help_text": "Helping",
                "initial": "Lorem ipsum",
            },
        }
    )

    assert isinstance(fields["foo"], forms.Field) is True
    assert fields["foo"].label == "Foo"
    assert fields["foo"].help_text == "Helping"
    assert fields["foo"].required is False
    assert fields["foo"].initial == "Lorem ipsum"


def test_get_form(db):
    """
    Method should return a form class.
    """
    controller = ControllerFactory()

    forge = FormClassForge()

    ControllerForm = forge.get_form({
        "foo": {
            "kind": "text-simple",
            "label": "Foo",
            "name": "foo",
            "required": True,
            "position": 1,
            "help_text": "",
            "initial": ""
        },
    })

    # Init unbound form and check basic form field render
    form = ControllerForm(controller=controller)
    dom = html_pyquery(form.as_p())
    input_foo = dom.find("input#id_foo")
    assert len(input_foo) == 1
    assert input_foo.attr("name") == "foo"
    label_foo = dom.find("label[for=id_foo]")
    assert len(label_foo) == 1
    assert label_foo.text() == "Foo:"

    # Init form without any data
    form = ControllerForm({}, controller=controller)
    assert form.is_valid() is False

    # Init form with data
    form = ControllerForm({"foo": "Hello world!"}, controller=controller)
    dom = html_pyquery(form.as_p())
    input_foo = dom.find("input#id_foo")
    assert input_foo.attr("value") == "Hello world!"
    assert form.is_valid() is True


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
