import pytest

from canopy.factories import SlotFactory
from canopy.forms.forge import FormClassForge


@pytest.mark.parametrize("name, empty, filled", [
    (
        "text-simple",
        '<input type="text" name="foofield" maxlength="255">',
        '<input type="text" name="foofield" value="foovalue" maxlength="255">',
    ),
    (
        "textarea",
        '<textarea name="foofield" cols="40" rows="10" maxlength="3000">\n</textarea>',
        (
            '<textarea name="foofield" cols="40" rows="10" maxlength="3000">\n'
            'foovalue</textarea>'
        ),
    ),
    (
        "email",
        '<input type="email" name="foofield" maxlength="320">',
        '<input type="email" name="foofield" value="foovalue" maxlength="320">',
    ),
    (
        "boolean",
        '<input type="checkbox" name="foofield">',
        '<input type="checkbox" name="foofield" value="foovalue" checked>',
    ),
    (
        "date",
        '<input type="text" name="foofield" value="">',
        '<input type="text" name="foofield" value="foovalue">',
    ),
    (
        "datetime",
        '<input type="text" name="foofield" value="">',
        '<input type="text" name="foofield" value="foovalue">',
    ),
    (
        "time",
        '<input type="text" name="foofield" value="">',
        '<input type="text" name="foofield" value="foovalue">',
    ),
    (
        "ip-address",
        '<input type="text" name="foofield" maxlength="39">',
        '<input type="text" name="foofield" value="foovalue" maxlength="39">',
    ),
    (
        "ip4-address",
        '<input type="text" name="foofield" maxlength="39">',
        '<input type="text" name="foofield" value="foovalue" maxlength="39">',
    ),
    (
        "ip6-address",
        '<input type="text" name="foofield" maxlength="39">',
        '<input type="text" name="foofield" value="foovalue" maxlength="39">',
    ),
    (
        "integer",
        '<input type="number" name="foofield">',
        '<input type="number" name="foofield" value="foovalue">',
    ),
    (
        "decimal",
        '<input type="number" name="foofield" step="any">',
        '<input type="number" name="foofield" value="foovalue" step="any">',
    ),
    (
        "choice-list",
        '<select name="foofield">\n</select>',
        '<select name="foofield">\n</select>',
    ),
    (
        "choice-radio",
        '<div>\n</div>',
        '<div>\n</div>',
    ),
    (
        "multiple-choice-list",
        '<select name="foofield" multiple>\n</select>',
        '<select name="foofield" multiple>\n</select>',
    ),
    (
        "multiple-choice-checkbox",
        '<div>\n</div>',
        '<div>\n</div>',
    ),
])
def test_kind_render(name, empty, filled):
    """
    Every kind should render as expected.
    """
    slot = SlotFactory.build(label="Foo", name="foo", kind=name)
    text_field = FormClassForge().build_slot_field(slot)
    assert text_field.widget.render("foofield", "") == empty
    assert text_field.widget.render("foofield", "foovalue") == filled
