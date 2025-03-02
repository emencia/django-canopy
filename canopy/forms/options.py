from django import forms


from canopy.definitions.registry import get_registry
registry = get_registry()


class BaseSlotOptionsForm:
    """
    TODO
    This form should allow us to build inputs for each field or widget options that we
    could inject into the Slot model admin form. The idea is to avoid to use Schema and
    json-editor to edit the JSON for options fields.

    Concretely these form fields will be virtual fields, we just want to stand on
    natural Django form validation and rendering but at the end the form values will
    be serialized so it can be saved in a JSONField from Slot form.

    Choice field will be a problem because it is a dynamical thing (like Django
    InlineFormSet is doing).

    We will have to tweak the Slot admin form to inject Option fields in the Slot model
    form instead of the JSONField input. But the admin form will also need to intercept
    the Options form values to pass him the data for validation and possible save()
    method then push its JSON to the field or widget options field.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, commit=True, **kwargs):
        """
        Output validated option values as a JSON payload suitable to save into a
        JSONField.

        Returns:
            string: Option values as a JSON payload.
        """
        return


def build_options_form(attrname, slot=None):
    """
    Build form class for Slot field options.

    TODO: It seems something that should be part of registry.

    Arguments:
        attrname (string): The Slot attribute name for the related option field
            for which we search a definition. Can be either ``field`` or ``widget``.

    Returns:
        dict:
    """
    base_classes = (BaseSlotOptionsForm, forms.Form)

    return type(
        "SlotOptionsForm",
        base_classes,
        registry.get_kind_field_attributes_fields(attrname, kind=slot.kind if slot else None)
    )
