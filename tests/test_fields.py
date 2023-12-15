from typing import ClassVar, List, Tuple

import pytest
from typing_extensions import Literal

from pydantic_compat import PYDANTIC2, BaseModel, Field


def test_field_const() -> None:
    with pytest.raises(TypeError, match="use `Literal\\['bar'\\]` instead"):
        Field(..., const="bar")  # type: ignore

    class Foo(BaseModel):
        bar: Literal["bar"] = "bar"

    with pytest.raises(ValueError, match="validation error"):
        Foo(bar="baz")  # type: ignore


@pytest.mark.parametrize("post", ["items", "length"])
@pytest.mark.parametrize("pre", ["min", "max"])
def test_field_min_max_items(pre: str, post: str) -> None:
    class Foo(BaseModel):
        bar: List[int] = Field(..., **{f"{pre}_{post}": 2})  # type: ignore

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
        model_config: ClassVar[dict] = {"validate_assignment": True}  # type: ignore

    foo = Foo()
    with pytest.raises((TypeError, ValueError)):  # (v1, v2)
        foo.bar = 2


@pytest.mark.parametrize("key", ["regex", "pattern"])
def test_regex_pattern(key: str) -> None:
    class Foo(BaseModel):
        bar: str = Field(..., **{key: "^bar$"})  # type: ignore

    Foo(bar="bar")
    with pytest.raises(ValueError):
        Foo(bar="baz")


@pytest.mark.parametrize(
    "keys",
    [
        ("min_items", "min_length"),
        ("max_items", "max_length"),
        ("allow_mutation", "frozen"),
        ("regex", "pattern"),
    ],
)
def test_double_usage_raises(keys: Tuple[str, str]) -> None:
    with pytest.raises(ValueError, match="Cannot specify both"):
        Field(..., **dict.fromkeys(keys))  # type: ignore


# not attempting unique_items yet...
# see https://github.com/pydantic/pydantic-core/issues/296
# @pytest.mark.skipif(
#     pydantic.version.VERSION.startswith("1.8"),
#     reason="pydantic 1.8 does not support unique_items",
# )
# def test_unique_items() -> None:
#     class Foo(BaseModel):
#         bar: List[int] = Field(..., unique_items=True)
#     with pytest.raises(ValueError):
#         Foo(bar=[1, 2, 3, 1])


def test_field_extras() -> None:
    class Foo(BaseModel):
        bar: int = Field(..., metadata={"foo": "bar"})  # type: ignore

    assert Foo.model_fields["bar"].json_schema_extra["metadata"] == {"foo": "bar"}
