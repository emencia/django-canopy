"""
This is a demonstration and tutorial for "schema" library until its implementation is
finished since library documentation is painful to understand.

Schema validate data values and possibly coerces them if instructed to do so.

Basically schema respect given scheme structure. A callable item (like list or dict) is
followed recursively, a type object (like int or str) expect a value in this right type
and almost everything (like "foo" or 42) else is assumed as an exact value expected.

Then there are validatatable operators to combine the basics in more advanced
validation.


Basic value validation
**********************

Basically, the scheme can define allowed values or possible type, like this: ::

    Schema([1, 0]).validate([1, 1, 0, 1])

It will succeeds because we defined 0 and 1 in list as allowed values but: ::

    Schema([1, 0]).validate([1, 2, 0, 1])

It will fails since 2 is not an allowed value. Or: ::

    Schema([1, 0]).validate(1)

Fails because this is just not a list.


Basic type validation
*********************

We can allow to validate against value type: ::

    Schema((int, float)).validate((5, 7, 8.5)

Here, any integer or float values are allowed. If we try: ::

    Schema((int, float)).validate((5, "foo", 8.5)

It will fails with an error about ``foo`` that is not an integer or a float.


Operator classes
****************

There are schema operator classes that allow to combine validation rules for more
advanced needs.

Use
    Use(arg) is to coerce value with 'arg' callable.

And
    ``And(arg1, arg2)`` is to perform boolean assertion with ``arg2`` callable
    on ``arg1`` value, like for ``And(str, len)`` the given value must be a string
    with length greater than 0.

    With ``And(int, lambda n: n > 0)`` the given value must be an integer greater
    than 0.

Or
    ``Or(*args)`` Allows for a list of possible rules, the value must validate against
    one of them.

Optional
    ``Optional(arg)`` Allows to make the condition as optional.

"""
from django import forms

import pytest

from schema import Schema, And, Or, Use, Optional, SchemaError

from canopy.forms.forge import FormClassForge
from canopy.factories import ControllerFactory, SlotFactory
from canopy.utils.tests import html_pyquery


def test_schema_basic_value():
    # Require an unique exact value
    Schema(42).validate(42)
    with pytest.raises(SchemaError):
        Schema(42).validate(0)
        Schema(42).validate("nope")

    # Require three possible exact values in a list
    allowed = ["yep", 42, None]
    Schema(allowed).validate(["yep", 42, None])
    Schema(allowed).validate(["yep"])
    Schema(allowed).validate([42, 42, 42])
    Schema(allowed).validate([None, None])
    # Does not match allowed values
    with pytest.raises(SchemaError):
        Schema(allowed).validate(["42"])
        Schema(allowed).validate([0])
        Schema(allowed).validate(["nope", 1, True])


def test_schema_basic_type():
    # Required integer type
    Schema(int).validate(-42)
    Schema(int).validate(0)
    Schema(int).validate(42)
    # Not an integer
    with pytest.raises(SchemaError):
        Schema(int).validate(4.2)
    with pytest.raises(SchemaError):
        Schema(int).validate("nope")


def test_schema_validatable_and():
    # Required integer greater than 0
    # We use a lambda to validate positiveness
    print()
    res = Schema(And(int, lambda n: n > 0)).validate(3000)
    print(res)
    # Not an integer
    with pytest.raises(SchemaError):
        Schema(And(int, lambda n: n > 0)).validate("")
    # Less than 1 will result in False
    with pytest.raises(SchemaError):
        Schema(And(int, lambda n: n > 0)).validate(0)
    with pytest.raises(SchemaError):
        Schema(And(int, lambda n: n > 0)).validate(-42)

    # Required string longer than 0
    # We just use len() function that will be always True until an empty string
    print()
    Schema(And(str, len).validate("yep"))
    # Empty
    with pytest.raises(SchemaError):
        Schema(And(str, len)).validate("")
    # Not a string
    with pytest.raises(SchemaError):
        Schema(And(str, len)).validate(42)


def test_schema_validatable_or():
    # Required integer greater than 0
    # We use a lambda to validate positiveness
    print()
    allowed = [42, "yep"]
    Schema(Or(*allowed)).validate("yep")
    # Not an integer
    with pytest.raises(SchemaError):
        Schema(And(int, lambda n: n > 0)).validate("")

    # Require either a positive integer or exact string "yep"
    allowed = Or(
        And(int, lambda n: n > 0),
        "yep"
    )
    Schema(allowed).validate("yep")
    with pytest.raises(SchemaError):
        Schema(allowed).validate("nope")
    with pytest.raises(SchemaError):
        Schema(allowed).validate(-42)


def test_schema_advanced():
    schema = Schema(
        {
            Optional("max_length"): And(int, lambda n: n > 0),
            "choices": [[str, str]],
            Optional("unexpected"): And(str, len),
        }
    )

    print(schema.validate({
        "max_length": 3000,
        "choices": [
            ["fookey", "Foo label"],
            ["harari-soul-fire", "Harari - Soul Fire"],
        ],
    }))

    # Only 'choices' is required but can be empty
    print(schema.validate({
        "choices": [],
    }))

    # max_length must be greater than 0
    with pytest.raises(SchemaError):
        schema.validate({
            "choices": [],
            "max_length": 0,
        })

    # Choice items must be list of 'string, string'
    with pytest.raises(SchemaError):
        schema.validate({
            "choices": ["one", "two"],
        })

    # assert 1 == 42
