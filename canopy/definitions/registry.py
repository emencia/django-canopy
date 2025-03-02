from functools import cache

from django.conf import settings
from django.utils.functional import lazy

from . import DefinitionsRegistry


@cache
def _get_registry():
    """
    Cached function to initialize the registry interface.

    This is also where registry is filled with default definitions if setting
    ``CANOPY_REGISTRY_AUTOLOAD`` allows it.
    """
    registry = DefinitionsRegistry()

    if (
        settings.CANOPY_REGISTRY_AUTOLOAD is True and
        (registry.initialized is None or registry.initialized is False)
    ):
        registry.load(settings.CANOPY_SLOT_DEFINITIONS)
        registry.initialized = True

    return registry


get_registry = lazy(_get_registry, DefinitionsRegistry)
