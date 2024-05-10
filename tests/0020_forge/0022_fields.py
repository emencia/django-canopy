from django import forms

from canopy.forms.forge import FormClassForge


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
                "options": {},
            },
        }
    )

    assert isinstance(fields["foo"], forms.Field) is True
    assert fields["foo"].label == "Foo"
    assert fields["foo"].help_text == "Helping"
    assert fields["foo"].required is False
    assert fields["foo"].initial == "Lorem ipsum"
