from django import forms

from canopy.forms.forge import FormClassForge
from canopy.factories import ControllerFactory, SlotFactory
from canopy.utils.tests import html_pyquery

import pytest


@pytest.mark.skip("Finish slot options validation first")
def test_bound_field_options(db):
    """
    Input field should be properly built from its definitions and slot options

    TODO: Should test again form build including options, schema validation from
    Slot model must be done first, then the forge could implement options applying.
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
