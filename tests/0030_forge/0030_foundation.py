from django import forms

from canopy.utils.tests import flatten_form_errors


def test_construct_form_class_with_type():
    """
    Demonstrate usage of ``type()`` to build class with given arguments. It is
    the way to programmatically build a form class.
    """
    attrs = {
        "your-name": forms.CharField(max_length=50, required=True),
        "your-number": forms.IntegerField(min_value=5, max_value=15),
    }

    # Build a concrete form using type() and giving fields as attributes instead of
    # defining them into class
    DummyForm = type("DummyForm", (forms.Form,), attrs)

    f = DummyForm()
    # print(f.as_p())

    # Check form is valid
    validation = f.is_valid()
    assert validation is False
    assert flatten_form_errors(f) == {}

    # The given fields should be there
    assert ("id_your-name" in f.as_p()) is True
    assert ("id_your-number" in f.as_p()) is True
