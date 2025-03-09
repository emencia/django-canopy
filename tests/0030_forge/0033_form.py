from canopy.factories import ControllerFactory, SlotFactory
from canopy.forms.forge import FormClassForge
from canopy.utils.tests import html_pyquery


def test_get_form(db):
    """
    Method should return a form class.
    """
    ctrl = ControllerFactory()
    textarea = SlotFactory(
        controller=ctrl,
        kind="textarea",
        label="Bar",
        name="bar",
        position=2,
    )
    email = SlotFactory(
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
