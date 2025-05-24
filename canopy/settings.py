from django.utils.translation import gettext_lazy as _


CANOPY_SLOT_DEFINITIONS = "canopy.definitions.defaults"
"""
Python path to slot definitions dict variable. Default use the one included from this
applications. Give another valid Python path to dict with your custom definitions.
"""

CANOPY_REGISTRY_AUTOLOAD = True
"""
Define if registry should automatically load definitions from settings
``CANOPY_SLOT_DEFINITIONS`` once it is imported from ``canopy.definitions.registry``.

Disabling this setting is for very specific usage and especially when Canopy is only
used programmatically.
"""

CANOPY_ADMIN_CONTROLLER_DATA_PAGINATION = 100
"""
Entry per page limit for pagination in Controller data admin, you can set it to ``None``
to disable pagination but it is not recommended.
"""

CANOPY_CONTROLLER_FORM_TEMPLATES = (
    ("canopy/controller/form/default.html", _("default")),
)
"""
Available templates to render Controller form page.
"""

CANOPY_CONTROLLER_SUCCESS_TEMPLATES = (
    ("canopy/controller/success/default.html", _("default")),
)
"""
Available templates to render Controller success page.
"""
