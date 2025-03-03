from canopy.forms.forge import FormClassForge
from canopy.factories import ControllerFactory, SlotFactory
from canopy.models import empty_fresh_dictionnary


def test_normalize_scheme_from_dict():
    """
    Method normalize_scheme should return a slot scheme from a dict.
    """
    forge = FormClassForge()

    assert forge.normalize_scheme({
        "foo": {
            "kind": "text-simple",
            "label": "Foo",
            "name": "foo",
            "required": False,
            "position": 1,
            "help_text": "",
            "initial": ""
        },
    }) == {
        "foo": {
            "kind": "text-simple",
            "label": "Foo",
            "name": "foo",
            "required": False,
            "position": 1,
            "help_text": "",
            "initial": ""
        },
    }


def test_normalize_scheme_from_iterable():
    """
    Method normalize_scheme should return a slot scheme from an iterable.
    """
    forge = FormClassForge()

    assert forge.normalize_scheme((
        (
            "foo", {
                "kind": "text-simple",
                "label": "Foo",
                "name": "foo",
                "required": False,
                "position": 1,
                "help_text": "",
                "initial": ""
            },
        ),
    )) == {
        "foo": {
            "kind": "text-simple",
            "label": "Foo",
            "name": "foo",
            "required": False,
            "position": 1,
            "help_text": "",
            "initial": ""
        },
    }


def test_normalize_scheme_from_controller(db):
    """
    Method should returns a slot scheme from Controller object.
    """
    forge = FormClassForge()

    # Create a controller object with some slot objectss
    controller = ControllerFactory()
    SlotFactory(label="Foo", name="foo", controller=controller, position=1)
    SlotFactory(label="Bar", name="bar", controller=controller, position=2)

    assert forge.normalize_scheme(controller) == {
        "foo": {
            "kind": "text-simple",
            "label": "Foo",
            "name": "foo",
            "required": False,
            "position": 1,
            "help_text": "",
            "initial": "",
            "field_options": empty_fresh_dictionnary(),
            "widget_options": empty_fresh_dictionnary(),
        },
        "bar": {
            "kind": "text-simple",
            "label": "Bar",
            "name": "bar",
            "required": False,
            "position": 2,
            "help_text": "",
            "initial": "",
            "field_options": empty_fresh_dictionnary(),
            "widget_options": empty_fresh_dictionnary(),
        }
    }
