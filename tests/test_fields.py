from typing import Literal

import pytest

from pydantic_compat import BaseModel, Field


def test_field_const() -> None:
    with pytest.raises(TypeError, match="use `Literal\\['bar'\\]` instead"):
        Field(..., const="bar")

    class Foo(BaseModel):
        bar: Literal["bar"] = "bar"

    with pytest.raises(ValueError, match="validation error"):
        Foo(bar="baz")  # type: ignore


def test_field_min_items() -> None:
    class Foo(BaseModel):
        bar: list[int] = Field(..., min_items=2)

    with pytest.raises((TypeError, ValueError)):  # (v1, v2)
        Foo(bar=[1])

def test_field_max_items() -> None:
    class Foo(BaseModel):
        bar: list[int] = Field(..., max_items=2)

    with pytest.raises((TypeError, ValueError)):  # (v1, v2)
        Foo(bar=[1, 2, 3, 4])


def test_field_allow_mutation() -> None:
    # used in v1
    class Foo(BaseModel):
        bar: int = Field(default=1, allow_mutation=False)

        class Config:
            validate_assignment = True  # required for allow_mutation in v1

    foo = Foo()
    with pytest.raises((TypeError, ValueError)):  # (v1, v2)
        foo.bar = 2


def test_field_frozen() -> None:
    # used in v2
    class Foo(BaseModel):
        bar: int = Field(default=1, frozen=True)

        class Config:
            validate_assignment = True  # required for allow_mutation in v1

    foo = Foo()
    with pytest.raises((TypeError, ValueError)):  # (v1, v2)
        foo.bar = 2
