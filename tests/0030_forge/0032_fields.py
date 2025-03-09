from django import forms

from canopy.factories import ControllerFactory, SlotFactory
from canopy.forms.forge import FormClassForge


def test_get_form_fields(db):
    """
    Method should return a dict of form fields built from given slot scheme.
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
