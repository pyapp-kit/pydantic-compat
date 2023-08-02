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


@pytest.mark.parametrize("post", ["items", "length"])
@pytest.mark.parametrize("pre", ["min", "max"])
def test_field_min_max_items(pre: str, post: str) -> None:
    class Foo(BaseModel):
        bar: list[int] = Field(..., **{f"{pre}_{post}": 2})  # type: ignore

    bad_val = [1, 2, 3] if pre == "max" else [1]
    with pytest.raises((TypeError, ValueError)):  # (v1, v2)
        Foo(bar=bad_val)


def test_field_allow_mutation() -> None:
    # used in v1
    class Foo(BaseModel):
        bar: int = Field(default=1, allow_mutation=False)

        class Config:
            validate_assignment = True

    foo = Foo()
    with pytest.raises((TypeError, ValueError)):  # (v1, v2)
        foo.bar = 2


def test_field_frozen() -> None:
    # used in v2
    class Foo(BaseModel):
        bar: int = Field(default=1, frozen=True)
        model_config = {"validate_assignment": True}

    foo = Foo()
    with pytest.raises((TypeError, ValueError)):  # (v1, v2)
        foo.bar = 2
