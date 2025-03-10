from canopy.factories import SlotFactory
from canopy.forms.forge import FormClassForge
from canopy.definitions import DefinitionsRegistry


def test_build_slot_widget_basic(db):
    """
    Method should build a correct Widget object from a slot.
    """
    registry = DefinitionsRegistry()
    registry.load("canopy.definitions.tests")

    textarea = SlotFactory(label="Foo", name="foo", kind="textarea")

    forge = FormClassForge()

    # Field attributes are not included when built directly from widget itself
    kind = registry.get_definition(textarea.kind)
    text_widget = forge.build_slot_widget(kind.widget)
    assert text_widget.render("foofield", "") == (
        '<textarea name="foofield" cols="40" rows="10">\n</textarea>'
    )

    # Extra options can be given to overrides the defaults or add new ones
    kind = registry.get_definition(textarea.kind)
    text_widget = forge.build_slot_widget(kind.widget, slot_options={
        "rows": 42,
        "required": "true",
    })
    assert text_widget.render("foofield", "") == (
        '<textarea name="foofield" cols="40" rows="42" required="true">\n</textarea>'
    )


def test_build_slot_field_basic(db):
    """
    Method should build a correct Field object from a slot.
    """
    text = SlotFactory(label="Foo", name="foo", kind="text-simple")

    forge = FormClassForge()

    text_field = forge.build_slot_field(text)

    # Empty value
    assert text_field.widget.render("foofield", "") == (
        '<input type="text" name="foofield" maxlength="255">'
    )

    # Non empty value
    assert text_field.widget.render("foofield", "foovalue") == (
        '<input type="text" name="foofield" value="foovalue" maxlength="255">'
    )
