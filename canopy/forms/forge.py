import copy

from django import forms
from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from ..exceptions import ControllerError
from ..models import Controller
from .controller import ControllerBaseForm


class FormClassForge:
    """
    Forge to build a form from given definitions and slots.
    """
    def __init__(self, default_klass=None):
        self.default_klass = default_klass or ControllerBaseForm

    def get_definitions(self, definitions=None):
        """
        Returns available slot definitions.

        On default if no definitions are given the default ones from
        ``settings.CANOPY_SLOT_DEFINITIONS`` are used.

        Keyword Arguments:
            definitions (dict): Definitions to use instead of the default ones. This
                is not cumulative, it replaces the whole default definitions.

        Returns:
            dict:
        """
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

        for name, slot in scheme.items():
            if slot["kind"] not in definitions:
                msg = _("Slot definition does not exists for given name: {}")
                raise ControllerError(msg.format(slot["kind"]))

            definition = definitions[slot["kind"]]

            # Get the base defined options from definitions
            field_options = copy.deepcopy(definition["field_options"])
            # Then update options with some from slot attributes
            field_options.update({
                "label": slot["label"],
                "initial": slot["initial"],
                "help_text": slot["help_text"],
                "required": slot["required"],
            })
            # TODO: manage an item "widget_options"
            # TODO: field (and widget) option from JSONfield

            # Register built field in field map
            fields[name] = definition["field"](**field_options)

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

        base_classes = (self.klass, forms.Form,)

        return type("ControllerForm", base_classes, attrs)
