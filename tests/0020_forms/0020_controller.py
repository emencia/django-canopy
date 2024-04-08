from django import forms

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


def test_get_form_fields():
    """
    Method should return a dict of form fields built from given slot scheme.
    """
    forge = FormClassForge()

    # Directly from a dict
    fields = forge.get_form_fields({
        "foo": {
            "kind": "text-simple",
            "label": "Foo",
            "name": "foo",
            "required": False,
            "position": 1,
            "help_text": "Helping",
            "initial": "Lorem ipsum",
        },
    })

    assert isinstance(fields["foo"], forms.Field) is True
    assert fields["foo"].label == "Foo"
    assert fields["foo"].help_text == "Helping"
    assert fields["foo"].required is False
    assert fields["foo"].initial == "Lorem ipsum"


def test_get_form():
    """
    Method should return a form class.
    """
    forge = FormClassForge()

    ControllerForm = forge.get_form({
        "foo": {
            "kind": "text-simple",
            "label": "Foo",
            "name": "foo",
            "required": False,
            "position": 1,
            "help_text": "",
            "initial": ""
        },
    })

    # Init unbound form and check basic form field render
    form = ControllerForm()
    dom = html_pyquery(form.as_p())
    input_foo = dom.find("input#id_foo")
    assert len(input_foo) == 1
    assert input_foo.attr("name") == "foo"
    label_foo = dom.find("label[for=id_foo]")
    assert len(label_foo) == 1
    assert label_foo.text() == "Foo:"

    # Init form with data
    form = ControllerForm({"foo": "Hello world!"})
    dom = html_pyquery(form.as_p())
    input_foo = dom.find("input#id_foo")
    assert input_foo.attr("value") == "Hello world!"


def test_form_save():
    """
    TODO
    """
    forge = FormClassForge()

    ControllerForm = forge.get_form({
        "foo": {
            "kind": "text-simple",
            "label": "Foo",
            "name": "foo",
            "required": False,
            "position": 1,
            "help_text": "",
            "initial": ""
        },
    })

    # Init form with data
    form = ControllerForm({"foo": "Hello world!"})
    dom = html_pyquery(form.as_p())
    input_foo = dom.find("input#id_foo")
    assert input_foo.attr("value") == "Hello world!"

    created = form.save()
    print(created)

    assert 1 == 42

