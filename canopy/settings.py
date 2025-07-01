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

CANOPY_CONTROLLER_EXCEPTION_WHEN_DISABLED = False
"""
When ``True`` form and success pages will raise a Http404 if controller is disabled else
when this setting is ``False`` the pages render the template dedicated to disabled
controller.
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

CANOPY_CONTROLLER_DATA_HANDLERS = (
    ("canopy.handlers.SaveInDbHandler", _("Save in database")),
    ("canopy.handlers.SendEmailToStaffHandler", _("Send email to staff")),
    ("canopy.handlers.SendEmailToWriterHandler", _("Send email to writer")),
)
"""
A list of the available handlers to enable on a Controller to manage submitted data.

The first item must be a valid Python path to the handler class to load.

It is used as the handler choices for Controller and also as the order of processing
them during form save. This order can be overriden by setting
``CANOPY_CONTROLLER_DATA_HANDLER_ORDER`` if not empty.

.. Hint::
    The handler to save Entry in database is commonly the first one to avoid data loss
    on failure from other handler processing.
"""

CANOPY_CONTROLLER_DATA_HANDLER_ORDER = None
"""
A tuple of controller names (their class path) to defined the priority of handler
processing. If empty the order from ``CANOPY_CONTROLLER_DATA_HANDLERS`` is used instead.

An example with the default handler choices would be: ::

    CANOPY_CONTROLLER_DATA_HANDLER_ORDER = (
        "canopy.handlers.SaveInDbHandler",
        "canopy.handlers.SendEmailToStaffHandler",
        "canopy.handlers.SendEmailToWriterHandler",
    )

.. Warning::
    Any item names from ``CANOPY_CONTROLLER_DATA_HANDLERS`` that are not present in the
    priorities is simply ignored and won't be processed.
"""
