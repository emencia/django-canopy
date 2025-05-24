import datetime
import json
import types
from pathlib import Path


class ExtendedJsonEncoder(json.JSONEncoder):
    """
    Add support to serialize a Callable

    Usage sample: ::

        json.dumps(..., cls=ExtendedJsonEncoder)
    """
    def default(self, obj):
        # Support for bytes to unicode string
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        # Support for pathlib.Path to a string
        if isinstance(obj, Path):
            return str(obj)
        # Support for set to a list
        if isinstance(obj, set):
            return list(obj)
        # Support for dates/times in ISO format string
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        # Support for a callable to its name as a string
        if callable(obj):
            return obj.__name__
        # Support for a generator to its name as a string
        if isinstance(obj, types.GeneratorType):
            return obj.__name__

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
