import copy

from django.conf import settings
from django.db import models
from django.utils.module_loading import import_string

from ..exceptions import DefinitionRegistryError


class SlotDefinitionsRegistry:
    """
    Definition registry for slot kinds.

    Attributes:
        initialized (boolean): A flag attribute to indicate if registry has already
            been initialized with initial definitions, commonly those ones from
            setting ``CANOPY_SLOT_DEFINITIONS``.

            Registry itself don't edit this variable it is the role of the routine in
            charge to initialize it, so either the internal canopy init if setting
            ``CANOPY_REGISTRY_AUTOLOAD`` is true else your own custom code.

            In fact if you don't use the internal canopy init, you may not need to care
            about this attribute, it will depends if your code care about it or not. Be
            aware that some Django routine like development server can load model twice
            for some reasons, so take care your code is ready for that to avoid loading
            definitions twice.
    """
    initialized = None

    def __init__(self):
        self.reset()

    def reset(self):
        """
        Shortcut method to boot/reset registry.
        """
        self.default = None
        self.definitions = {}

    def check_definitions(self, definitions):
        """
        Check given definitions.

        * All definition must have a "name" and "field" items.
        * Field item must have a "class" item;
        * If widget item exists, it must include a "class" item;

        Arguments:
            definitions (dict): All definition items to validate.

        Raises:
            DefinitionRegistryError: In case of invalid items, this exceptions is
            raised. Note that it will regroup all items errors but the exception
            message is just a basic error message. To retrieve detail errors you will
            need to use the exception method ``.get_payload_details()``.

        Returns:
            bool: True if all definitions are valid.
        """
        errors = []

        for key, data in definitions.items():
            # Definition value must be a dict
            if not isinstance(data, dict):
                msg = "{key}: value must be a dictionnary."
                errors.append(msg.format(key=key))
                continue

            # Definition name is required
            if "name" not in data:
                errors.append("{key}: is missing 'name' item.".format(key=key))

            # Definition field is required
            if "field" not in data:
                errors.append("{key}: is missing 'field' item.".format(key=key))
            else:
                # Definition field class is required (but not checked for its type)
                if "class" not in data["field"]:
                    errors.append(
                        "{key}: 'field' is missing 'class' item.".format(key=key)
                    )
                # TODO: Validate "options_fields" so option names could not override
                # existing Slot attribute, especially its model fields.

            # Definition widget is optional
            if "widget" in data:
                # Definition widget class is required (but not checked for its type)
                if "class" not in data["widget"]:
                    errors.append(
                        "{key}: 'widget' is missing 'class' item.".format(key=key)
                    )

        if errors:
            raise DefinitionRegistryError(error_messages=errors)

        return True

    def load(self, definitions, default=None):
        """
        Load definitions from a module or a dictionnary.

        Each call to load does not reset previously loaded definitions, it is
        cumulative. However subsequent loads can override previously loaded
        definitions.

        Arguments:
            definitions (dict or string): Either a dict of definitions to append or
                a string for a Python path to module to load to get definitions to
                append.

        Keyword Arguments:
            default (string): yet to come. May be not accurate as a kwarg, maybe get it
                from import if available, else need to use set_default()

        """
        # TODO: Not fully implement yet, still need to be validated then set and used
        if default is None:
            try:
                default = import_string(
                    settings.CANOPY_SLOT_DEFINITIONS + ".DEFAULT"
                )
            except ImportError:
                default = None

        if isinstance(definitions, str):
            defs = import_string(definitions + ".DEFINITIONS")
        elif isinstance(definitions, dict):
            defs = definitions

        if self.check_definitions(defs):
            self.definitions.update(defs)

    def names(self):
        """
        Return all available definition key names.

        Returns:
            list: List of name strings.
        """
        return list(self.definitions.keys())

    def has(self, name):
        """
        Check if given definition key name exists in registry.

        Arguments:
            name (string): Key name to check.

        Returns:
            boolean: True if given key name exists.
        """
        return name in self.definitions

    def get(self, name, default=None):
        """
        Get definition from given key name.

        .. Warning::
            This is only to be used when you are sure the returned definition won't be
            altered further from your code else you will mutate its content during
            current Python session.

            Prefer to use ``SlotDefinitionsRegistry.get_kind_definition(..)`` instead
            that is safe against mutations. If you are not able to do so, use
            ``copy.deepcopy()`` on returned definition.

        Arguments:
            name (string): Key name to get.

        Keyword Arguments:
            default (string): Default value to return if given key name does not
                exists. On default, the default value is None.

        Returns:
            dict: The definition for given key name if it exists else the default
                value.
        """
        return self.definitions.get(name, default)

    def get_all(self):
        """
        Shortcut method to definitions attribute.
        """
        return self.definitions

    def get_choices(self):
        """
        Build kind choices from available definitions.

        Returns:
            list: List of tuples for available definitions. Each tuple is pair of
            definition key and definition name.
        """
        return [
            (k, v["name"])
            for k, v in self.definitions.items()
        ]

    def get_default(self):
        """
        Get default definition key name.

        The default definition is the first one from definitions.

        NOTE: We may have possibility to define a specific default from a variable
        along '.set_default()' method. However it will need to restructure how we load
        definitions, the module path won't target anymore 'DEFINITIONS' var but only
        the module containing it and so we could seek also for an optional "DEFAULT"
        variable.

        Returns:
            name:
        """
        return list(self.definitions.keys())[0]

    def get_kind_definition(self, kind=None):
        """
        Get a definition from a Slot kind or a kind name.

        Keyword Arguments:
            kind (string or Slot): the kind key name or Slot instance to search for
                definition. On default this is the default kind choice key.

        Returns:
            dict: Kind definition. This is a copy of the registred definition to avoid
            registry mutations. Return can be None if no kind has been given and there
            is not defined default definition name.
        """
        kind = kind or self.get_default()

        # If kind is model instance with "kind" attribute get the kind name from it
        if isinstance(kind, models.Model) and hasattr(self, "kind"):
            kind = kind.kind

        return copy.deepcopy(self.get(kind))

    def get_kind_field_options(self, attrname, kind=None):
        """
        Get field options for field or widget according to given kind.

        Arguments:
            attrname (string): The Slot attribute name for the related option field
                for which we search a definition. Can be either ``field`` or ``widget``.

        Keyword Arguments:
            kind (string or Slot): the Slot kind key to search for definition. On
                default this is the default kind choice key.

        Returns:
            dict: Possible field options if any else an empty dict.
        """
        kind = self.get_kind_definition(kind=kind)
        return kind.get(attrname, {}).get("options_fields", {})

    def get_kind_field_options_initials(self, kind=None):
        """
        Get initial fields values for field options for given kind key or Slot.

        This is only about kind field since widget does not manage any value.

        Keyword Arguments:
            kind (string or Slot): the Slot kind key to search for definition. On
                default this is the default kind choice key.

        Returns:
            dict:
        """
        kind = self.get_kind_definition(kind=kind)
        return kind["field"].get("options", {})
