from django import forms

from canopy.forms.forge import FormClassForge
from canopy.factories import ControllerFactory, SlotFactory
from canopy.utils.tests import html_pyquery


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
            "initial": "",
            "options": {},
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


def test_bound_field_options(db):
    """
    Input field should be properly built from its definitions and slot options
    """
    controller = ControllerFactory()
    SlotFactory(
        controller=controller,
        kind="text-simple",
        label="Full name",
        name="fullname",
    )
    SlotFactory(
        controller=controller,
        kind="text-multiline",
        label="Commentary",
        name="commentary",
    )
    SlotFactory(
        controller=controller,
        kind="list-choices",
        label="My choices",
        name="my-choices",
    )

    forge = FormClassForge()
    ControllerForm = forge.get_form(controller, definitions={
        "text-simple": {
            "name": "Simple text",
            "field": {
                "class": forms.CharField,
            },
        },
        "list-choices": {
            "name": "Choice list",
            "field": {
                "class": forms.ChoiceField,
            },
        },
        "text-multiline": {
            "name": "Multiline text",
            "field": {
                "class": forms.CharField,
                "options": {
                    "max_length": 3000,
                },
                "schema": {
                    "max_length": "integer",
                },
            },
            "widget": {
                "class": forms.Textarea,
                "options": {
                    "class": "hello-world",
                },
            },
        },
    })
    form = ControllerForm(controller=controller)

    assert str(form["fullname"]).startswith("<input")
    input_element = html_pyquery(str(form["fullname"]))
    assert input_element.attr("name") == "fullname"
    assert input_element.attr("class") is None
    assert input_element.attr("maxlength") is None

    assert str(form["commentary"]).startswith("<textarea")
    input_element = html_pyquery(str(form["commentary"]))
    assert input_element.attr("name") == "commentary"
    assert input_element.attr("class") == "hello-world"
    assert input_element.attr("maxlength") == "3000"

    # print()
    # print(str(form["my-choices"]))

    # assert 1 == 42
