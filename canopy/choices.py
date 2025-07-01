from django.conf import settings


def get_controller_handler_choices():
    """
    Callable to get choice list of Controller handlers.
    """
    return settings.CANOPY_CONTROLLER_DATA_HANDLERS


def get_controller_handler_order():
    """
    Return the order of handler processing.
    """
    if getattr(settings, "CANOPY_CONTROLLER_DATA_HANDLER_ORDER", None):
        return [k for k in settings.CANOPY_CONTROLLER_DATA_HANDLER_ORDER]
    else:
        return [k for k, v in settings.CANOPY_CONTROLLER_DATA_HANDLERS]


def get_controller_handler_default():
    """
    Callable to get default choice value of Controller handlers.
    """
    return settings.CANOPY_CONTROLLER_DATA_HANDLERS[0][0]


def get_controller_form_template_choices():
    """
    Callable to get choice list of Controller form templates.
    """
    return settings.CANOPY_CONTROLLER_FORM_TEMPLATES


def get_controller_form_template_default():
    """
    Callable to get default choice value of Controller form templates.
    """
    return settings.CANOPY_CONTROLLER_FORM_TEMPLATES[0][0]


def get_controller_success_template_choices():
    """
    Callable to get choice list of Controller success page templates.
    """
    return settings.CANOPY_CONTROLLER_SUCCESS_TEMPLATES


def get_controller_success_template_default():
    """
    Callable to get default choice value of Controller success page templates.
    """
    return settings.CANOPY_CONTROLLER_SUCCESS_TEMPLATES[0][0]
