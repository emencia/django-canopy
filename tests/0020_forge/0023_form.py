import pytest

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


@pytest.mark.skip("Expect the definition refactoring to continue further")
def test_bound_field_options(db):
    """
    TODO
    """
    controller = ControllerFactory()
    SlotFactory(
        controller=controller,
        kind="text-multiline",
        label="Full name",
        name="fullname",
        required=True,
        options={"foo":  "bar"}
    )

    forge = FormClassForge()

    ControllerForm = forge.get_form(controller)
    form = ControllerForm(controller=controller)

    print(form["fullname"])
    print(dir(form["fullname"]))

    assert 1 == 42
