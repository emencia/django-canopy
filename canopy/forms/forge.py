import copy

from django import forms
from django.utils.translation import gettext_lazy as _

from ..exceptions import ControllerError
from ..models import Controller
from .controller import ControllerBaseForm


from canopy.definitions.registry import get_registry
registry = get_registry()


class FormClassForge:
    """
    Forge to build a form from given definitions and slots.

    TODO: Use registry instead of manually loading definitions.
    """
    def __init__(self, default_klass=None):
        self.default_klass = default_klass or ControllerBaseForm

    def get_slot_scheme(self, scheme):
        """
        Normalize given content as a proper slot scheme.

        This is somewhat of a shortand to get a slot scheme from multiple supported
        types.

        Arguments:
            scheme (object): Either a dict, a list or a Controller instance. Dict or
                list format must be a valid slot scheme.

        Returns:
            dict: A slot scheme suitable for ``get_form_fields``.
        """
        if isinstance(scheme, list) or isinstance(scheme, tuple):
            scheme = dict(scheme)
        elif isinstance(scheme, Controller):
            scheme = scheme.slot_schemes()

        return scheme

    def build_slot_widget(self, definition, slot):
        """
        Build field widget for given slot and definition.

        TODO: Shouldn't this done (fully or partially) with registry instead ?

        Arguments:
            definition (dict):
            slot (dict):

        Returns:
            django.forms.Field:
        """
        klass = definition.get("class", None)
        attrs = copy.deepcopy(definition.get("options", {}))
        # TODO: Not applied yet
        slot_options = slot.get("widget_options", {})

        if not klass:
            return None

        if not attrs:
            widget = klass
        else:
            attrs.update(slot_options)
            widget = klass(attrs=attrs)

        return widget

    def build_slot_field(self, definitions, slot):
        """
        Build field for given slot.

        TODO: Shouldn't this be done (fully or partially) with registry instead ?

        Arguments:
            definitions (dict):
            slot (dict):

        Returns:
            django.forms.Field:
        """
        if slot["kind"] not in definitions:
            msg = _("Slot definition does not exists for given name: {}")
            raise ControllerError(msg.format(slot["kind"]))

        slot_definition = definitions[slot["kind"]]

        # Get the field definition
        field_definition = slot_definition["field"]
        field_kwargs = copy.deepcopy(field_definition.get("options", {}))

        # Get the slot field options values
        # TODO: Not applied yet
        # slot_field_options = slot["field_options"]

        # Then update field options with slot object values
        field_kwargs.update({
            "label": slot["label"],
            "initial": slot["initial"],
            "help_text": slot["help_text"],
            "required": slot["required"],
        })

        # Append possible widget with options if any
        widget = self.build_slot_widget(slot_definition.get("widget", {}), slot)
        if widget:
            field_kwargs["widget"] = widget

        # Initialize and register field with its options
        return field_definition["class"](**field_kwargs)

    def get_form_fields(self, definitions, scheme):
        """
        Returns a dict of form fields for given slot scheme and available definitions.

        Arguments:
            definitions (dict):
            scheme (dict):

        Returns:
            dict:
        """
        return {
            name: self.build_slot_field(definitions, slot)
            for name, slot in scheme.items()
        }

    def get_form(self, scheme, klass=None, extra_attrs={}, definitions=None):
        """
        Build the form class from given slot scheme.

        Arguments:
            scheme (object): Either a dict, a list or a Controller instance. Dict or
                list format must be a valid slot scheme.

        Keyword Arguments:
            klass (class): Controller form class to inherit in addition to
                ``forms.Form``. On default this use the one defined from
                ``FormClassForge.default_klass``.
            extra_attrs (dict): Additional attributes to add to built class form. This
                is mostly to carry controller options or non field. Do not add fields
                by this way. Be aware that these extra attributes can override the
                field attributes with the same name. A naming policy should be
                enforced.
            definitions (dict): Definitions to use instead of the default ones. This
                is not cumulative, it replaces the whole default definitions. Be aware
                that is mostly for testing usage since canopy is not really intended to
                work with definitions that does not come from module defined in
                ``settings.CANOPY_SLOT_DEFINITIONS``.

        Returns:
            class: The form class built from given slot scheme.
        """
        self.klass = klass or self.default_klass
        definitions = (
            definitions if isinstance(definitions, dict) else registry.get_all()
        )

        scheme = self.get_slot_scheme(scheme)

        attrs = self.get_form_fields(definitions, scheme)
        if extra_attrs:
            attrs.update(extra_attrs)

        # Build class
        base_classes = (self.klass, forms.Form,)

        return type("ControllerForm", base_classes, attrs)
