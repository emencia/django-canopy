import copy

from django import forms
from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from ..exceptions import ControllerError
from ..models import Controller, Slot
from .controller import ControllerBaseForm


class FormClassForge:
    """
    Forge to build a form from given definitions and slots.
    """
    def __init__(self, default_klass=None):
        self.default_klass = default_klass or ControllerBaseForm
        self.slot_options_decoder = Slot._meta.get_field("options").decoder

    def get_definitions(self, definitions=None):
        """
        Returns available slot definitions.

        On default if no definitions are given the default ones from
        ``settings.CANOPY_SLOT_DEFINITIONS`` are used.

        Keyword Arguments:
            definitions (dict or string): Definitions to use instead of the default
                ones. This is not cumulative, it replaces the whole default definitions.
                This can be either the definitions dictionnary or a string for a
                module Python path to load.

        Returns:
            dict:
        """
        if isinstance(definitions, dict):
            return definitions

        return import_string(definitions or settings.CANOPY_SLOT_DEFINITIONS)

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
            scheme = scheme.definitions_scheme()

        return scheme

    def build_slot_field(self, definitions, slot):
        """
        Build field for given slot.

        Arguments:
            definitions (dict):
            slot (dict):

        Returns:
            django.forms.Field:
        """
        # Get the field definition
        field_definition = definitions[slot["kind"]]["field"]
        field_kwargs = copy.deepcopy(field_definition.get("options", {}))

        # Get the widget definition
        widget_definition = definitions[slot["kind"]].get("widget", {})
        widget_class = widget_definition.get("class", None)
        widget_attrs = copy.deepcopy(widget_definition.get("options", {}))

        # Then update field options with slot object values
        field_kwargs.update({
            "label": slot["label"],
            "initial": slot["initial"],
            "help_text": slot["help_text"],
            "required": slot["required"],
        })

        """
        TODO: Now we have the slot options, we will have to unpack its content to
        distinct field options and widget options.
        """
        # print("📌 get_form_fields Slot:", slot)
        # print("📌 get_form_fields Slot options:", slot["options"])
        # extra_field_options = slot["options"].pop("field", {})
        # extra_widget_options = slot["options"].pop("widget", {})

        # Append possible widget with optional if any
        if widget_class:
            if not widget_attrs:
                widget = widget_class
            else:
                widget = widget_class(attrs=widget_attrs)

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
        fields = {}

        # Build field for each slot
        for name, slot in scheme.items():
            if slot["kind"] not in definitions:
                msg = _("Slot definition does not exists for given name: {}")
                raise ControllerError(msg.format(slot["kind"]))

            # Initialize and register field with its options
            fields[name] = self.build_slot_field(definitions, slot)

        return fields

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
                is not cumulative, it replaces the whole default definitions.

        Returns:
            class: The form class built from given slot scheme.
        """
        self.klass = klass or self.default_klass
        definitions = self.get_definitions(definitions)

        scheme = self.get_slot_scheme(scheme)

        attrs = self.get_form_fields(definitions, scheme)
        if extra_attrs:
            attrs.update(extra_attrs)

        # Build class
        base_classes = (self.klass, forms.Form,)

        return type("ControllerForm", base_classes, attrs)
