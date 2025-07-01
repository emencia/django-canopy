from django.utils.module_loading import import_string

from ..choices import get_controller_handler_choices


def get_handler_processor_class(path):
    """
    Load and return a handler processor class.

    Arguments:
        path (string): The Python path to the class.

    Returns:
        Class: The class object of the handler.
    """
    if not path:
        raise HandlerError("Handler 'path' is empty")
    elif path not in [v[0] for v in get_controller_handler_choices()]:
        raise HandlerError(
            "Handler 'path' value is not in available handler choices: {}".format(path)
        )

    return import_string(path)
