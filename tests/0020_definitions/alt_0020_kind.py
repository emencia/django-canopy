from dataclasses import FrozenInstanceError

import pytest

from django import forms
from pydantic import ValidationError

from canopy.definitions.base import Kind, KindField


def test_init_empty():
    """
    Definition class expect some arguments.
    """
    with pytest.raises(ValidationError) as exc_info:
        Kind()

    errors = [
        {"type": item["type"], "loc": item["loc"], "msg": item["msg"]}
        for item in exc_info.value.errors()
    ]
    assert errors == [
        {
            "type": "missing",
            "loc": ("identifier",),
            "msg": "Field required",
        },
        {
            "type": "missing",
            "loc": ("name",),
            "msg": "Field required",
        },
        {
            "type": "missing",
            "loc": ("field",),
            "msg": "Field required",
        }
    ]


def test_init_args_types():
    """
    Definition expect specific types for its arguments values
    """
    with pytest.raises(ValidationError) as exc_info:
        Kind(identifier=42, name=77, field="niet")

    # print(exc_info.value.json(indent=4))
    errors = [
        {"type": item["type"], "loc": item["loc"], "msg": item["msg"]}
        for item in exc_info.value.errors()
    ]
    assert errors == [
        {
            "type": "string_type",
            "loc": ("identifier",),
            "msg": "Input should be a valid string"
        },
        {
            "type": "string_type",
            "loc": ("name",),
            "msg": "Input should be a valid string",
        },
        {
            "type": "dataclass_type",
            "loc": ("field",),
            "msg": "Input should be a dictionary or an instance of KindField",
        }
    ]


def test_init_basic():
    """
    With correct arguments the definition should be as expected
    """
    foo = Kind(
        identifier="my-kind",
        name="My kind",
        field=KindField(
            klass=forms.CharField,
            initials={"max_length": 42}
        ),
    )

    assert foo.identifier == "my-kind"
    assert foo.field.initials == {"max_length": 42}

    with pytest.raises(FrozenInstanceError):
        foo.identifier = "nope"
