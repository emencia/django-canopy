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


class DefinitionRegistryError(CanopyBaseException):
    """
    When the definition registry encounter an error.

    Attribute ``error_messages`` contains a dict of applications error messages.

    Keyword Arguments:
        error_messages (dict): A dictionnary of all application errors. It
            won't output as exception message from traceback, you need to exploit it
            yourself if needed.
    """
    def __init__(self, *args, **kwargs):
        self.error_messages = kwargs.pop("error_messages", [])
        self.message = self.get_payload_message(*args)
        super().__init__(*args, **kwargs)

    def get_payload_message(self, *args):
        if self.error_messages:
            return "Some definitions have errors."
        elif len(args) > 0:
            return args[0]

        return "Unexpected error"

    def get_payload_details(self):
        return self.error_messages

    def __str__(self):
        return self.message
