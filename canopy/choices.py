from django.conf import settings


def get_controller_form_template_choices():
    """
    Callable to get choice list.
    """
    return settings.CANOPY_CONTROLLER_FORM_TEMPLATES


def get_controller_form_template_default():
    """
    Callable to get default choice value.
    """
    return settings.CANOPY_CONTROLLER_FORM_TEMPLATES[0][0]


def get_controller_success_template_choices():
    """
    Callable to get choice list.
    """
    return settings.CANOPY_CONTROLLER_SUCCESS_TEMPLATES


def get_controller_success_template_default():
    """
    Callable to get default choice value.
    """
    return settings.CANOPY_CONTROLLER_SUCCESS_TEMPLATES[0][0]
