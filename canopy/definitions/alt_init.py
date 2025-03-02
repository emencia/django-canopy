import copy

from django.conf import settings
from django.db import models
from django.utils.module_loading import import_string

from ..exceptions import DefinitionRegistryError


class DefinitionsRegistry:
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
        self.default_kind = None
        self.definitions = {}

    def check_default(self, value):
        """
        Check given default definition key name.

        * Default value must be a string;
        * Default value must be an available key name from loaded definitions;

        Arguments:
            definitions (string): Value to validate as a default definition key name.

        Raises:
            DefinitionRegistryError: In case of invalid value, this exceptions is
            raised. Note that it will regroup all items errors but the exception
            message is just a basic error message. To retrieve detail errors you will
            need to use the exception method ``.get_payload_details()``.

        Returns:
            boolean: True if given default key name is valid.
        """
        errors = []

        # Definition value must be a dict
        if not isinstance(value, str):
            msg = "Default value must be a string, not {}."
            errors.append(msg.format(type(value)))
        elif value not in self.definitions:
            msg = (
                "Default value must be an available key from definitions, '{}' does "
                "not exist in definitions."
            )
            errors.append(msg.format(value))

        if errors:
            raise DefinitionRegistryError(error_messages=errors)

        return True

    def set_default(self, value):
        """
        Set a new default definition key name.

        Given value will be validated before to be set.
        """
        if value and self.check_default(value):
            self.default_kind = value

    def load(self, definitions, default=None):
        """
        Load definitions from a module or a dictionnary.

        Each call to load does not reset previously loaded definitions, it is
        cumulative. However subsequent loads can override previously loaded
        definitions.

        TODO: Follow refactoring of Slot kinds

        Arguments:
            definitions (iterable or string): Either an iterable of definitions to
                append or a string for a Python path to module to import to get
                definitions to append. Definitions are expected to be in a
                ``DEFINITIONS`` variable from the imported module.

        Keyword Arguments:
            default (string): Set value as default if it is a string. Else if value
                is empty this will try to get it from imported definitions module if
                any, the default value is expected in ``DEFAULT`` variable from the
                imported module.
        """
        imported_modulepath = None

        # Either try to import Python module path to import from given definitions
        # value if it is a string else assume it is the definitions dict itself
        if isinstance(definitions, str):
            defs = import_string(definitions + ".DEFINITIONS")
            imported_modulepath = definitions
        elif isinstance(definitions, list) or isinstance(definitions, tuple):
            defs = definitions
        else:
            msg = (
                "Definitions must be provided either as a list, a tuple or a string "
                "(for a module Python path) not '{}'"
            )
            raise ValueError(msg.format(type(definitions).__name__))

        self.definitions.update({
            item.identifier: item
            for item in defs
        })

        if default is None and imported_modulepath:
            try:
                default = import_string(imported_modulepath + ".DEFAULT")
            except ImportError:
                default = None

        self.set_default(default)

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
            (k, v.name)
            for k, v in self.definitions.items()
        ]

    def get_default(self):
        """
        Get default definition key name.

        Returns:
            string: The default definition name is either the defined default (from
            loading) or the first one from definitions if there is no default.
        """
        return self.default_kind or self.names()[0]

    def get_kind_definition(self, kind=None):
        """
        Get a definition from a Slot object or a ``kind`` name.

        Keyword Arguments:
            kind (string or Slot): the kind key name or Slot instance to search for
                definition. If this argument is an empty value, the default kind choice
                key will be used if available.

        Returns:
            dict: Kind definition. This is a copy of the registred definition to avoid
            registry mutations. Return can be None if no kind has been given and there
            is no defined default definition name.
        """
        # Use default kind if argument is an empty value
        kind = kind or self.get_default()

        # If kind is model instance with "kind" attribute get the kind name from it
        if isinstance(kind, models.Model) and hasattr(kind, "kind"):
            kind = kind.kind

        return self.get(kind)

    def get_kind_field_attributes_fields(self, attrname, kind=None):
        """
        Get all attributes for field or widget according to a kind (given or default).

        Arguments:
            attrname (string): The Slot attribute name for the related option field
                for which we search a definition. Can be either ``field`` or ``widget``.

        Keyword Arguments:
            kind (string or Slot): the Slot kind key to search for definition. On
                default this is the default kind choice key.

        Returns:
            dict: Possible field attributes if any else an empty dict.
        """
        kind = self.get_kind_definition(kind=kind)
        if not getattr(kind, attrname):
            return {}

        return getattr(kind, attrname).attributes_fields

    def get_kind_field_attributes_initials(self, kind=None):
        """
        Get initial field attributes values for given kind key or Slot.

        This is only about kind field since widget does not manage any initials.

        Keyword Arguments:
            kind (string or Slot): the Slot kind key to search for definition. On
                default this is the default kind choice key.

        Returns:
            dict:
        """
        kind = self.get_kind_definition(kind=kind)
        return kind.field.get("attributes_initials", {})

    def validate_field_attributes(self, attrname, kind, values):
        """
        TODO: Field attributes initial values should be validated here
        """
        return True
