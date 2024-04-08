"""
Specific application exceptions.
"""


class CanopyBaseException(Exception):
    """
    Exception base.

    You should never use it directly except for test purpose. Instead make or
    use a dedicated exception related to the error context.
    """
    pass


class AppOperationError(CanopyBaseException):
    """
    Sample exception to raise from your code.
    """
    pass


class ControllerError(CanopyBaseException):
    """
    When the controller encounter an error or invalid data.
    """
    pass
