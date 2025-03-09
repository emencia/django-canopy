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
    """
    def __init__(self, default_klass=None):
        self.default_klass = default_klass or ControllerBaseForm

    def DEPRECATED_normalize_to_schema(self, content):
        """
        DEPRECATED

        Normalize given content as a proper slot schema.

        This is somewhat of a shortand to get a slot schema from multiple supported
        types.

        Arguments:
            content (object): Either a dict, a list or a Controller instance. Dict or
                list format must be a valid slot schema.

        Returns:
            dict: A slot schema suitable for ``get_form_fields``.
        """
        if isinstance(content, list) or isinstance(content, tuple):
            content = dict(content)
        elif isinstance(content, Controller):
            content = content.slot_values()

        return content

    def build_slot_widget(self, widget, slot_options=None):
        """
        Build widget class for given widget definition.

        Arguments:
            widget (KindWidget): Widget definition object.
            slot_options (dict): Dictionnary of options to overrides the default ones
                from the ``KindWidget`` object.

        Returns:
            django.forms.Widget: Widget class.
        """
        if not widget:
            return None

        slot_options = slot_options or {}

        attrs = widget.options
        widget = widget.klass

        attrs.update(slot_options)

        return widget(attrs=attrs)

    def build_slot_field(self, slot):
        """
        Build field for a given slot.

        Arguments:
            slot (canopy.models.Slot): Slot object.

        Returns:
            django.forms.Field: Built (unbound) field object.
        """
        if not registry.has(slot.kind):
            msg = _("Slot definition does not exists for given name: {}")
            raise ControllerError(msg.format(slot.kind))

        kind = registry.get(slot.kind)

        # Get the field definition
        field_definition = kind.field
        field_kwargs = registry.get_kind_attr_initials(kind=slot.kind)
        # NOTE: Currently we just pass initial field attribute values from the Kind
        # definition but concretely they should be updated with the corresponding Slot
        # json values. Alike already do.
        # slot_field_options = slot.field_options

        # Update field options with slot object values
        field_kwargs.update({
            "label": slot.label,
            "initial": slot.initial,
            "help_text": slot.help_text,
            "required": slot.required,
        })

        # Append possible widget with possible slot options
        widget = self.build_slot_widget(kind.widget, slot.widget_options)
        if widget:
            field_kwargs["widget"] = widget

        # Initialize and register field with its options
        return field_definition.klass(**field_kwargs)

    def get_form_fields(self, slots):
        """
        Returns a dict of form fields for given slot schema.

        Arguments:
            slots (list): List of Slot objects.

        Returns:
            dict: All built slot fields indexed on their slot name.
        """
        return {
            slot.name: self.build_slot_field(slot)
            for slot in slots
        }

    def get_form(self, controller, klass=None, extra_attrs={}):
        """
        Build the form class from given slot schema.

        Arguments:
            controller (canopy.models.Controller): Controller object.

        Keyword Arguments:
            klass (class): Controller form class to inherit in addition to
                ``forms.Form``. On default this use the one defined from
                ``FormClassForge.default_klass``.
            extra_attrs (dict): Additional attributes to add to built class form. This
                is mostly to carry controller options or non field. Do not add fields
                by this way.

        Returns:
            class: The form class built from given slot schema.
        """
        self.klass = klass or self.default_klass

        attrs = self.get_form_fields(controller.get_slots())
        if extra_attrs:
            attrs.update(extra_attrs)
        # NOTE: Maybe we could directly attach the controller object instead of having
        # to pass it as argument

        # Build class
        base_classes = (self.klass, forms.Form,)

        return type("ControllerForm", base_classes, attrs)
