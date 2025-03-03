from django import forms

from canopy.forms.forge import FormClassForge
# from canopy.definitions.registry import get_registry


def test_get_form_fields(settings):
    """
    Method should return a dict of form fields built from given slot scheme.
    """
    forge = FormClassForge()

    # TODO: Load test registry, currently this test run with the default registry which
    # is not desired
    # registry = get_registry()
    # definitions = registry.get_all()
    fields = forge.get_form_fields(
        {
            "foo": {
                "kind": "text-simple",
                "label": "Foo",
                "name": "foo",
                "required": False,
                "position": 1,
                "help_text": "Helping",
                "initial": "Lorem ipsum",
                "field_options": {},
                "widget_options": {},
            },
        }
    )

    assert isinstance(fields["foo"], forms.Field) is True
    assert fields["foo"].label == "Foo"
    assert fields["foo"].help_text == "Helping"
    assert fields["foo"].required is False
    assert fields["foo"].initial == "Lorem ipsum"
