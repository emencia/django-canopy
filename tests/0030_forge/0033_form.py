from django import forms

from canopy.factories import ControllerFactory, SlotFactory
from canopy.forms.forge import FormClassForge
from canopy.utils.tests import html_pyquery


def test_get_form_fields(db):
    """
    Method should return a dict of form fields built from given slot scheme.
    """
    ctrl = ControllerFactory()
    SlotFactory(
        controller=ctrl,
        kind="textarea",
        label="Bar",
        name="bar",
        position=2,
    )
    SlotFactory(
        controller=ctrl,
        kind="email",
        label="Foo",
        name="foo",
        help_text="Helping",
        initial="Lorem ipsum",
        position=1
    )

    forge = FormClassForge()

    fields = forge.get_form_fields(ctrl.slot_set.all())

    assert list(fields.keys()) == ["foo", "bar"]

    assert isinstance(fields["foo"], forms.Field) is True
    assert fields["foo"].label == "Foo"
    assert fields["foo"].help_text == "Helping"
    assert fields["foo"].required is False
    assert fields["foo"].initial == "Lorem ipsum"

    assert isinstance(fields["bar"], forms.Field) is True


def test_get_form(db):
    """
    Method should return a form class.
    """
    ctrl = ControllerFactory()
    SlotFactory(
        controller=ctrl,
        kind="textarea",
        label="Bar",
        name="bar",
        position=2,
    )
    SlotFactory(
        controller=ctrl,
        kind="email",
        label="Foo",
        name="foo",
        help_text="Helping",
        initial="Lorem ipsum",
        required=True,
        position=1
    )

    forge = FormClassForge()

    ControllerForm = forge.get_form(ctrl)

    # Init unbound form and check basic form field render
    form = ControllerForm(controller=ctrl)
    dom = html_pyquery(form.as_p())
    input_foo = dom.find("input#id_foo")
    assert len(input_foo) == 1
    assert input_foo.attr("name") == "foo"
    label_foo = dom.find("label[for=id_foo]")
    assert len(label_foo) == 1
    assert label_foo.text() == "Foo:"

    # Init form without any data
    form = ControllerForm({}, controller=ctrl)
    assert form.is_valid() is False

    # Not a valid email
    form = ControllerForm({"foo": "Hello world!"}, controller=ctrl)
    dom = html_pyquery(form.as_p())
    input_foo = dom.find("input#id_foo")
    assert input_foo.attr("value") == "Hello world!"
    assert form.is_valid() is False

    # With a valid email
    form = ControllerForm({"foo": "foo@foo.com"}, controller=ctrl)
    dom = html_pyquery(form.as_p())
    input_foo = dom.find("input#id_foo")
    assert input_foo.attr("value") == "foo@foo.com"
    assert form.is_valid() is True
